from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

import re


class FileResources:

    def __init__(self, conf_repo_path: Path, crema_id: str) -> None:
        self.conf_repo_path = conf_repo_path
        self.crema_id = crema_id
        self.crema_path = self.conf_repo_path / "internal" / "geopipeline" / "output" / crema_id

        if not self.crema_path.is_dir():
            raise MissingResourceError(str(self.crema_path))


    def get_event_file(self) -> Path:
        return self.__search_file__(self.crema_path, r"^mission_timeline_event_file((?!ganymede).)*$")

    def get_mission_phases_file(self) -> Path:
        return self.__search_file__(self.crema_path, r"^Mission_Phases$")

    def get_spice_files(self) -> list[Path]:
        return self.__search_files__(self.crema_path, r"^juice_sc_crema.*$")

    def __search_file__(self, parent_path: Path, pattern: re.Pattern) -> Path:
        matches = self.__search_files__(parent_path, pattern)
        if len(matches) == 0:
            raise MissingResourceError(pattern)
        if len(matches) > 1:
            raise DuplicatedResourceError(pattern)
        return matches[0]

    def __search_files__(self, parent_path: Path, pattern: re.Pattern) -> list[Path]:
        matches = []
        for file in parent_path.iterdir():
            match = re.search(pattern, file.stem)
            if match is not None:
                matches.append(file)
        return matches


class MissingResourceError(Exception):
    def __init__(self, resource: str) -> None:
        super().__init__(f"Missing Resource Error {resource}")


class DuplicatedResourceError(Exception):
    def __init__(self, resource: str) -> None:
        super().__init__(f"Duplicated Resource Error {resource}")
