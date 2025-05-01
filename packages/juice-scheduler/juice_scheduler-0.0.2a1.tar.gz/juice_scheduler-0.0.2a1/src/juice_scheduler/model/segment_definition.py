from __future__ import annotations

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


class SegmentDefinitionHandler:
    def __init__(self) -> None:
        self.mnemonic_map: dict[str, SegmentDefinition] = {}
        self.working_group_map: dict[str, list[SegmentDefinition]] = {}

    def add_definition(self, mnemonic:str, working_group: str) -> None:
        definition = SegmentDefinition(mnemonic, working_group)
        if mnemonic in self.mnemonic_map:
            raise DuplicateDefinitionError

        if working_group not in self.working_group_map:
            self.working_group_map[working_group] = []

        self.mnemonic_map[mnemonic] = definition
        self.working_group_map[working_group].append(definition)

    def get_definition(self, mnemonic: str) -> SegmentDefinition:
        if mnemonic not in self.mnemonic_map:
            raise NonExistingDefinitionError(mnemonic)
        return self.mnemonic_map[mnemonic]

    @staticmethod
    def from_sht_struct(sht_json):
        handler = SegmentDefinitionHandler()
        for json_definition in sht_json:
            handler.add_definition(json_definition["mnemonic"], json_definition["group"])
        return handler

    @staticmethod
    def from_sht_file(sht_path: Path):
        with sht_path.open("r") as sht_file:
            sht_json = json.load(sht_file)
            return SegmentDefinitionHandler.from_sht_struct(sht_json)

class SegmentDefinition:
    def __init__(self, name: str, working_group: str):
        self.name = name
        self.working_group = working_group

class DuplicateDefinitionError(Exception):
    pass

class NonExistingDefinitionError(Exception):
    def __init__(self, mnemonic) -> None:
        super().__init__(f"Definition {mnemonic} does not exist")
