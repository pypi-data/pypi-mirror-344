from __future__ import annotations

import json
import logging
from pathlib import Path
from types import MappingProxyType

from juice_scheduler.common.date_utils import datestr_to_timestamp


class Unit:

    base_rate_unit = MappingProxyType({
        "DATA_RATE": "bps",
        "DATA_VOLUME": "bps",
        "POWER": "W",
        "ENERGY": "W",
    })

    base_rate_category = MappingProxyType({
        "DATA_VOLUME": "DATA_RATE",
        "ENERGY": "POWER",
    })

    def __init__(self, name: str, mnemonic: str, category: str, ratio: float) -> None:
        self.name: str = name
        self.mnemonic: str = mnemonic
        self.category: str = category
        self.ratio: float = ratio

    def is_rate(self):
        return self.category in ["DATA_RATE", "POWER"]

    def get_rate_base_unit(self):
        return Unit.base_rate_unit.get(self.category)

    def get_rate_base_category(self):
        return Unit.base_rate_category.get(self.category, self.category)



class UnitHandler:

    def __init__(self) -> None:
        self.units_map: dict[str, Unit] = {}
        unit_description: Path = Path(__file__).parent / "data" / "units.json"
        with unit_description.open("r") as json_file:
            descriptions = json.load(json_file)
            for description in descriptions:
                self.add_unit(description.get("name"),
                              description.get("mnemonic"),
                              description.get("category"),
                              description.get("ratio"))

    def add_unit(self, name: str, mnemonic: str, category: str, ratio: float):
        self.units_map[mnemonic] = Unit(name, mnemonic, category, ratio)

    def get_unit(self, unit_mnemonic: str) -> Unit:
        return self.units_map[unit_mnemonic]


class ResourceType:

    def __init__(self, name: str, mnemonic: str, category: str) -> None:
        self.name: str = name
        self.mnemonic: str = mnemonic
        self.category: str | None = category

    def __eq__(self, value) -> bool:
        if isinstance(value, ResourceType):
            return value.mnemonic == self.mnemonic
        return False

    def is_instrument_type(self):
        return self.category is None

class ResourceTypeHandler:

    def __init__(self) -> None:
        self.types_map: dict[str, ResourceType] = {}
        type_description: Path = Path(__file__).parent / "data" / "types.json"
        with type_description.open("r") as json_file:
            descriptions = json.load(json_file)
            for description in descriptions:
                self.add_resource(description.get("name"),
                                  description.get("mnemonic"),
                                  None)
                for instrument in description.get("instrument_set", []):
                    self.add_resource(instrument,
                                      instrument,
                                      description.get("mnemonic"))

    def add_resource(self, name: str, mnemonic: str, category: str | None):
        self.types_map[mnemonic] = ResourceType(name, mnemonic, category)

    def get_resource_type(self, type_mnemonic: str) -> ResourceType:
        return self.types_map[type_mnemonic]


class Resource:

    def __init__(self, resource_type: ResourceType, target: str, value: float, unit: Unit) -> None:
        self.resource_type: ResourceType = resource_type
        self.target: str = target
        self.value: float = value
        self.unit: Unit = unit

    def is_rate(self):
        return self.unit.is_rate()

    def to_rate(self, duration: float) -> float:
        if self.is_rate():
            return self.value * self.unit.ratio
        return (self.value * self.unit.ratio) / duration

    def __repr__(self) -> str:
        return f"Resource({self.resource_type}, {self.target}, {self.value}, {self.unit.mnemonic})"



class ResourceInstance:

    def __init__(self, start: float, end: float, resource: Resource) -> None:
        self.start: float = start
        self.end: float = end
        self.resource: Resource = resource

    def get_value_basic_unit(self) -> float:
        return self.resource.value * self.resource.unit.ratio

    def get_rate(self) -> float:
        return self.resource.to_rate(self.end - self.start)

    def is_instrument_type(self):
        return self.resource.resource_type.is_instrument_type()

    def __repr__(self) -> str:
        return f"ResourceInstance( {self.resource.resource_type.mnemonic} {self.start}, {self.end}, {self.get_rate()})"

    def to_json(self):
        json_obj = {
            "target": self.resource.target,
            "value": self.get_rate(),
            "unit": self.resource.unit.get_rate_base_unit(),
            "category" : self.resource.unit.get_rate_base_category(),
        }
        field = "instrument_type" if self.resource.resource_type.is_instrument_type() else "instrument"
        json_obj[field] = self.resource.resource_type.mnemonic
        return json_obj

class ResourceHandler:

    def __init__(self) -> None:
        self.resources_map: dict[str, list[ResourceInstance]] = {}

    def add_resource(self, segment_name: str, start: float, end: float, resource: Resource):
        if segment_name not in self.resources_map:
            self.resources_map[segment_name] = []
        resource_instance = ResourceInstance(start, end, resource)
        self.resources_map[segment_name].append(resource_instance)

    def get_resources(self, segment_name: str, start: float, end: float):
        instances = self.resources_map.get(segment_name, [])
        return [instance for instance in instances \
                if instance.start <= start and instance.end >= end]


    @staticmethod
    def from_sht_struct(plan_json) -> ResourceHandler:
        handler = ResourceHandler()
        unit_handler = UnitHandler()
        resource_type_handler = ResourceTypeHandler()
        segment_list = plan_json.get("segments")

        for segment in segment_list:
            mnemonic = segment.get("segment_definition")
            start = segment.get("start")
            end = segment.get("end")
            resource_list: list[Resource] = []

            resource_list.extend(
                ResourceHandler.extract_resources(segment, "resources", unit_handler, resource_type_handler))
            resource_list.extend(
                ResourceHandler.extract_resources(segment, "instrument_resources", unit_handler, resource_type_handler))
            for resource in resource_list:
                handler.add_resource(mnemonic,
                                     datestr_to_timestamp(start),
                                     datestr_to_timestamp(end), resource)

        return handler

    @staticmethod
    def extract_resources(segment, resource_type: str, unit_handler: UnitHandler, type_handler: ResourceTypeHandler):

        type_field = "instrument_type" if resource_type == "resources" else "instrument"
        return [Resource(type_handler.get_resource_type(resource.get(type_field)),
                         resource.get("target"),
                         float(resource.get("value")),
                         unit_handler.get_unit(resource.get("unit")))
                for resource in segment.get(resource_type, [])]


    @staticmethod
    def from_sht_file(plan_path: Path) -> ResourceHandler:
        logging.info("Reading resources from: %s", plan_path.name)
        with plan_path.open("r") as plan_file:
            plan_json = json.load(plan_file)
        return ResourceHandler.from_sht_struct(plan_json)
