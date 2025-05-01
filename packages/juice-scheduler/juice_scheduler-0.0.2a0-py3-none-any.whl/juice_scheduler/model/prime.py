from __future__ import annotations

from typing import TYPE_CHECKING

from portion import closed, to_data

from juice_scheduler.common.exception import JuiceParsingError
from juice_scheduler.model.interval_list import DateStrInterval

if TYPE_CHECKING:
    from pathlib import Path

    from juice_scheduler.model.events import EventsHandler
    from juice_scheduler.model.interval_list import IntervalList
    from juice_scheduler.model.segmentation import Segmentation

import logging


class PrimeHandler:

    def __init__(self) -> None:
        self.map: dict[str, str] = {}
        self.expanders: dict[str, PrimeNameExpander] = {}

    def add_mapping(self, opportunity: str, prime: str) -> None:
        if opportunity in self.map:
            raise DuplicatedOpportunityError(opportunity)
        self.map[opportunity] = prime

    def load_segmentation(self, segmentation: Segmentation, event_handler: EventsHandler):
        for segment_name in segmentation.base_map:
            prime = self.map.get(segment_name)
            expander = PrimeNameExpander.from_name(segment_name, prime)
            segment = segmentation.base_map[segment_name]
            expander.populate(event_handler, segment)
            self.expanders[segment.name] = expander

    def get_expander(self, segment_name: str):
        return self.expanders.get(segment_name, NullNameExpander(segment_name, None))

    @staticmethod
    def from_file(mapp_path: Path) -> PrimeHandler:
        logging.info("Reading Prime/Opportunity mapping: %s", mapp_path.name)
        field_delimiter = ";"
        inner_delimiter = ","
        handler = PrimeHandler()
        try:
            with mapp_path.open("r") as f:
                lines = f.readlines()
                # Skip header line
                for line in lines[1:]:
                    # Skip empty and commented lines
                    if  (field_delimiter not in line) or line.strip().startswith("#"):
                        continue
                    _, opportunities, primes, _ = line.strip().split(";")
                    # Skip lines without opportunity definition
                    if len(opportunities.strip()) == 0:
                        continue
                    for opportunity in opportunities.split(inner_delimiter):
                        for prime in primes.split(inner_delimiter):
                            handler.add_mapping(opportunity, prime)
        except (FileNotFoundError,
                ValueError) as e:
            raise JuiceParsingError from e
        return handler


class DuplicatedOpportunityError(Exception):
    def __init__(self, name: str) -> None:
        super().__init__(f"Duplicated opportunity {name}")

class PrimeNameExpander:

    def __init__(self, opp_name: str, prime_name: str) -> None:
        self.opp_name = opp_name
        self.prime_name = prime_name

    def expand(self, _start: float, _end: float):
        """
        Abstract
        """

    def populate(self, _event_handler: EventsHandler, segments: IntervalList):
        """
        Abstract
        """

    @staticmethod
    def from_name(opportunity: str, prime: str) -> PrimeNameExpander:
        if prime is None:
            return NullNameExpander(opportunity, prime)
        if prime.endswith("_xx"):
            return FlybyExpander(opportunity, prime)
        if prime.endswith("_PExx"):
            return PerijoveExpander(opportunity, prime)
        return SimpleExpander(opportunity, prime)



class NullNameExpander(PrimeNameExpander):

    def expand(self, _start: float, _end: float):
        return self.opp_name

class SimpleExpander(PrimeNameExpander):

    def expand(self, _start: float, _end: float):
        return self.prime_name

class RangeExpander(PrimeNameExpander):

    def __init__(self, opp_name: str, prime_name: str) -> None:
        super().__init__(opp_name, prime_name)
        self.expansions : dict[DateStrInterval, str] = {}

    def expand(self, start: float, end: float) -> str | None:
        interval = DateStrInterval(closed(start, end))
        for expansion in self.expansions:
            if expansion.contains(interval):
                return self.expansions[expansion]
        return None


class FlybyExpander(RangeExpander):

    def populate(self, event_handler: EventsHandler, segments: IntervalList):
        for instance in segments.instances:
            interval = to_data(instance)[0]
            flyby = event_handler.search_flyby_name(interval[1], interval[2])
            instance_name = self.prime_name.replace("xx", flyby)
            if flyby is not None:
                self.expansions[instance] = instance_name
            else:
                logging.warning("Missing flyby %s (%s) %s ", self.opp_name, self.prime_name, instance)

class PerijoveExpander(RangeExpander):

    def populate(self, event_handler: EventsHandler, segments: IntervalList):
        for instance in segments.instances:
            interval = to_data(instance)[0]
            perijove = event_handler.search_perijove_name(interval[1], interval[2])
            if perijove is not None:
                self.expansions[instance] = self.prime_name.replace("_PExx", "_PE" + perijove[2:])
            else:
                logging.warning("Missing perijove %s (%s) %s ", self.opp_name, self.prime_name, instance)
                self.expansions[instance] = self.opp_name
