from __future__ import annotations

import re
from typing import TYPE_CHECKING

from juice_scheduler.common.date_utils import datestr_to_timestamp, timestamp_to_datestr

if TYPE_CHECKING:
    from pathlib import Path

import logging


def flyby_processor(_name: str, epoch: float, context: str,
                    handler: EventsHandler, _block_dict : dict[str, float]) -> None:
    flyby_name = context.split(";")[0].split()[-1]
    handler.add_flyby(flyby_name, epoch)

def perijove_processor(name: str, epoch: float, _context: str,
                       handler: EventsHandler, _block_dict : dict[str, float]) -> None:
    pj_name = name.replace("PJ", "").replace("PERIJOVE_", "PJ")
    handler.add_perijove(pj_name, epoch)

def range_event_processor(name: str, epoch: float, _context: str,
                          handler: EventsHandler, block_dict : dict[str, float]) -> None:
    event = "_".join(name.split("_")[:-1])
    if name.endswith("_START"):
        if event in block_dict:
            raise NonPairedRangeEventError(name, epoch)
        block_dict[event] = epoch
        return

    if event not in block_dict:
        raise NonPairedRangeEventError(name, epoch)

    start = block_dict[event]
    del block_dict[event]
    if event == "SUN_CONJUNCTION_SUP":
        handler.add_sun_conjuction(start, epoch)
    elif event == "SUN_OCC_BY_JUPITER_TRANSIT":
        handler.add_sun_occulation(start, epoch)


PROCESSORS = [
    (r"FLYBY_.*", flyby_processor),
    (r"PERIJOVE_.*", perijove_processor),
    (r"SUN_CONJUNCTION_SUP_*", range_event_processor),
    (r"SUN_OCC_BY_JUPITER_TRANSIT_.*", range_event_processor),
]


class EventsHandler:

    def __init__(self):
        self.flybys: list[InstantEvent] = []
        self.perijoves: list[InstantEvent] = []
        self.sun_conjuctions: list[RangeEvent] = []
        self.sun_occultations: list[RangeEvent] = []

    def add_flyby(self, name: str, epoch: float):
        if name in self.flybys:
            raise DuplicatedEventError(name)
        self.flybys.append(InstantEvent(name, epoch))

    def add_perijove(self, name: str, epoch: float):
        if name in self.perijoves:
            raise DuplicatedEventError(name)
        self.perijoves.append(InstantEvent(name, epoch))

    def add_sun_conjuction(self, start: float, end: float):
        self.sun_conjuctions.append(RangeEvent(start, end))

    def add_sun_occulation(self, start: float, end: float):
        self.sun_occultations.append(RangeEvent(start, end))

    def search_flyby_name(self, start: float, end: float) -> str | None:
        event = EventsHandler.get_event(self.flybys, start, end)
        if event is None:
            return None
        return event.name

    def search_flyby(self, start: float, end: float) -> InstantEvent | None:
        return EventsHandler.get_event(self.flybys, start, end)

    def get_flyby(self, name: str) -> InstantEvent | None:
        return EventsHandler.get_event_by_name(self.flybys, name)

    def search_perijove_name(self, start: float, end: float) -> str | None:
        event = EventsHandler.get_event(self.perijoves, start, end)
        if event is None:
            return None
        return event.name

    def search_perijove(self, start: float, end: float) -> InstantEvent | None:
        return EventsHandler.get_event(self.perijoves, start, end)

    def get_perijove(self, name: str) -> InstantEvent | None:
        return EventsHandler.get_event_by_name(self.perijoves, name)

    @staticmethod
    def get_event_by_name(events: list[InstantEvent], name:str) -> InstantEvent | None:
        candidates = [event for event in events if event.name == name]
        if len(candidates) > 1:
            raise DuplicatedEventError(name)
        if len(candidates) == 1:
            return candidates[0]
        return None

    @staticmethod
    def get_event(events: list[InstantEvent], start: float, end: float) -> InstantEvent | None :
        candidates = [event for event in events if start <= event.epoch <= end]
        if len(candidates) > 1:
            raise SearchRangeError(start, end)
        if len(candidates) == 1:
            return candidates[0]
        return None

    @staticmethod
    def from_file(event_path: Path) -> EventsHandler:
        logging.info("Reading Events: %s", event_path.name)
        handler = EventsHandler()
        block_dict : dict[str, float] = {}
        with event_path.open("r") as f:
            lines = f.readlines()
            # Skip header line
            for line in lines[1:]:
                name, epoch_str, context = line.strip().split(",")
                epoch = datestr_to_timestamp(epoch_str)
                handler.process_event(name, epoch, context, handler, block_dict)
        return handler

    @staticmethod
    def process_event(name: str, epoch: float, context: str,
                      handler: EventsHandler, block_dict : dict[str, float]) -> None:
        for pattern, func in PROCESSORS:
            if re.match(pattern, name):
                func(name, epoch, context, handler, block_dict)
                break


class DuplicatedEventError(Exception):

    def __init__(self, name: str) -> None:
        super().__init__(f"Duplicated event {name}")

class NonPairedRangeEventError(Exception):

    def __init__(self, name: str, epoch: float) -> None:
        super().__init__(f"Non-paired range event {name} at {timestamp_to_datestr(epoch)}")

class SearchRangeError(Exception):
    def __init__(self, start: float, end: float) -> None:
        super().__init__(f"Search range too broad {start} / {end}")


class InstantEvent:

    def __init__(self, name: str, epoch: float):
        """
        Initialize an InstantEvent.

        :param name: The name of the event.
        :param epoch: The timestamp of the event.
        """
        self.name = name
        self.epoch = epoch

    def __repr__(self):
        return f"{self.name} {timestamp_to_datestr(self.epoch)}"

    def __eq__(self, other):

        if isinstance(other, str):
            return self.name == other

        if isinstance(other, InstantEvent):
            return self.name == other.name
        return False


class RangeEvent:

    def __init__(self, start: float, end: float):
        self.start = start
        self.end = end

    def __repr__(self):
        return f"[{timestamp_to_datestr(self.start)} , {timestamp_to_datestr(self.end)}]"
