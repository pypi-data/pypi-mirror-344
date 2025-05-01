from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from juice_scheduler.common.date_utils import InvalidDateFormatError, datestr_to_timestamp
from juice_scheduler.common.exception import JuiceParsingError

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)


class MissionPhase:
    def __init__(self, name, description: str, start: float, end: float):
        self.name: str = name
        self.description: str = description
        self.start: float = start
        self.end: float = end

class MissionPhaseHandler:
    """Handler for mission phases. It is a dictionary of mission phases indexed by name.
    """
    def __init__(self):
        self.phases: dict[str, MissionPhase] = {}

    def add_phase(self, name: str, description: str, start: float, end: float):
        if name in self.phases:
            raise DuplicatedMissionPhaseError
        if start >= end:
            raise MissionPhaseDurationError

        self.phases[name] = MissionPhase(name, description, start, end)

    def get_mission_phase(self, name: str) -> MissionPhase:
        if name not in self.phases:
            raise NonExistingMissionPhaseError
        return self.phases[name]

    def get_mission_phases(self) -> list[str]:
        return list(self.phases.keys())

    @staticmethod
    def from_file(mission_phases_path: Path) :
        """
        Creates a MissionPhaseHandler from a CSV file.

        The CSV file should contain a header line, and each subsequent line should contain the name, description,
        start and end times of a mission phase, separated by commas.
        The start and end times are in the format "YYYY-MM-DD HH:MM:SS".

        If a mission phase has an invalid duration (i.e. start time >= end time), a warning is logged and the
        mission phase is skipped.

        :param mission_phases_path: The path to the CSV file
        :return: A MissionPhaseHandler with the mission phases from the CSV file
        """
        logger.info("Reading Mission Phases: %s", mission_phases_path.name)
        handler = MissionPhaseHandler()
        try:
            with mission_phases_path.open("r") as f:
                lines = f.readlines()
                # Skip header line
                for line in lines[1:]:
                    # Force reading only the first 4 columns
                    name, description, start, end = line.strip().split(",")[:4]
                    start_timestamp = datestr_to_timestamp(start)
                    end_timestamp = datestr_to_timestamp(end)
                    if start_timestamp >= end_timestamp:
                        logger.warning("Mission phase %s has an invalid duration", name)
                        continue
                    handler.add_phase(name, description, start_timestamp, end_timestamp)
        except (FileNotFoundError,
                ValueError,
                InvalidDateFormatError) as e:
            raise JuiceParsingError from e
        return handler


class DuplicatedMissionPhaseError(Exception):
    pass

class NonExistingMissionPhaseError(Exception):
    pass

class MissionPhaseDurationError(Exception):
    pass
