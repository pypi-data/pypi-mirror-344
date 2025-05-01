from __future__ import annotations

from typing import TYPE_CHECKING

from juice_scheduler.common.date_utils import datestr_to_timestamp
from juice_scheduler.common.string_utils import filter_strings

if TYPE_CHECKING:
    from pathlib import Path

    from juice_scheduler.model.interval_list import ExpandedIntervalList
    from juice_scheduler.model.prime import PrimeHandler, PrimeNameExpander
    from juice_scheduler.model.resources import ResourceHandler

import csv
import json
import logging

from juice_scheduler.model.interval_list import IntervalList, ResourceInterval, merge

logger = logging.getLogger(__name__)

class Segmentation:

    def __init__(self, name: str):
        self.name : str = name
        self.base_map: dict[str, IntervalList] = {}
        self.expanded_map: dict[str, list[ExpandedIntervalList]] = {}
        self.segment_list: list[ResourceInterval] = []

    def add_instance(self, working_group: str, definition: str, start: float, end: float) -> None:
        """
        Adds an instance of the given segment instance to the segmentation plan.

        :param working_group: The working group to which the segment definition belongs.
        :param definition: The name of the segment definition.
        :param start: The start time of the segment.
        :param end: The end time of the segment.
        """
        if definition not in self.base_map:
            self.base_map[definition] = IntervalList(definition, working_group)
        self.base_map[definition].add_instance(start, end)

    def select_segment(self, segment_names: list[str] | str) -> list[IntervalList]:
        """
        Select the segment lists which names match any of the given segment names.

        :param segment_names: A string or a list of strings with the names of the segment lists to select.
        :return: A list of SegmentList objects which names match the given segment names.
        """
        if isinstance(segment_names, str):
            segment_names = [segment_names]

        expanded_segment_names = filter_strings(list(self.base_map.keys()), segment_names)
        return [self.base_map[segment_name] for segment_name in expanded_segment_names]

    def compare(self, other: Segmentation):

        segment_map =  self.index_segments()
        other_segment_map = other.index_segments()

        added = [definition for definition in segment_map if definition not in other_segment_map]
        missing = [definition for definition in other_segment_map if definition not in segment_map]

        summary = f"{self.name} vs {other.name}\n"
        summary += f"Added: {added}\n"
        summary += f"Missing: {missing}\n"
        similar = 0
        total = 0
        for mnemonic in [definition for definition in segment_map if definition in other_segment_map]:
            segments = segment_map[mnemonic]
            other_segments = other_segment_map[mnemonic]

            duration = sum((segment.upper - segment.lower) for segment in segments)
            other_duration = sum((segment.upper - segment.lower) for segment in other_segments)

            if len(segments) == len(other_segments):
                similar += 1

            summary += f"| {self.name:16s} | {mnemonic:32s} | {len(segments):>4d} | {duration:>12.3f} |\n"
            summary += f"| {other.name:16s} | {mnemonic:32s} | {len(other_segments):>4d} | {other_duration:>12.3f} |\n"
            total += 1
        summary += f"Probably identical: {similar}/{total}\n"
        return summary


    def index_segments(self):
        segment_map: dict[str, list[ResourceInterval]] = {}
        for segment in self.segment_list:
            name = segment.name
            if name not in segment_map:
                segment_map[name] = []
            segment_map[name].append(segment)
        return segment_map

    def expand_with_primes(self, prime_handler: PrimeHandler, resource_handler: ResourceHandler):
        # Expand all the original
        for definition_name in self.base_map:
            expander = prime_handler.get_expander(definition_name)
            self.expand_definition_name(definition_name, expander)
        # We merge all the expansions and include the results
        self.segment_list = []
        for expanded_key in self.expanded_map:
            merged = []
            for seg_list in self.expanded_map[expanded_key]:
                merged = merge(resource_handler, merged, seg_list)
            self.segment_list.extend(merged)
        self.segment_list.sort(key=lambda item : item.lower)

    def expand_definition_name(self, name: str, expander: PrimeNameExpander):

        definition = self.base_map[name]
        expanded_dict = definition.do_expansion(expander)
        # repopulate with expanded
        # the definition could be in the segmentation: several opportunities could map to
        # the same prime segment.
        for expand in expanded_dict:
            if expand not in self.expanded_map:
                self.expanded_map[expand] = []
            else:
                logger.warning("Capture of definition: %s -> %s", name, expand)
            self.expanded_map[expand].append(expanded_dict[expand])

    @staticmethod
    def from_sht_struct(plan_json, segment_definition_filters:list[str] | None= None) -> Segmentation:
        seg = Segmentation("sht")
        segment_list = plan_json.get("segments")
        for segment in segment_list:
            mnemonic = segment.get("segment_definition")
            if (segment_definition_filters is None) or (filter_strings([mnemonic], segment_definition_filters)):
                working_group = segment.get("source")
                start = segment.get("start")
                end = segment.get("end")
                seg.add_instance(working_group, mnemonic, datestr_to_timestamp(start), datestr_to_timestamp(end))

        return seg


    def add_csv_file(self, csv_path: Path):
        logger.info("Reading segments from: %s", csv_path.name)
        with csv_path.open("r") as plan_file:
            csv_reader = csv.reader(plan_file)
            for row in csv_reader:
                mnemonic = row[0]
                start = row[1]
                end = row[2]
                working_group = row[3]
                self.add_instance(working_group, mnemonic, datestr_to_timestamp(start), datestr_to_timestamp(end))

    @staticmethod
    def from_sht_file(sht_file_path: Path, segment_definition_filters:list[str] | None= None) -> Segmentation:
        logger.info("Reading segments from: %s", sht_file_path.name)
        with sht_file_path.open("r") as sht_file:
            plan_json = json.load(sht_file)
        return Segmentation.from_sht_struct(plan_json, segment_definition_filters)

    def to_sht_struct(self):
        segments = [s.to_json() for s in sorted(self.segment_list, key=lambda item : item.lower)]
        return {
            "creationDate": "2025-03-06T07:06:59.020Z",
            "name": "Checkpoint 2025-03-06T07:06:59.020Z",
            "segment_groups": [],
            "trajectory": "CREMA_5_0",
            "segments": segments,
        }

    def dissolve_gaps(self, gap_size: float):
        """
        Eliminates gaps between consecutive segments in the segment list
        that are smaller than the specified gap size.

        :param gap_size: The maximum size of a gap between segments
                        that should be dissolved.
        """
        self.segment_list.sort(key=lambda item : item.lower)
        i=1
        while i < len(self.segment_list):
            previous = self.segment_list[i - 1]
            element = self.segment_list[i]
            if 0 < element.lower - previous.upper < gap_size:
                new_item = ResourceInterval(previous.lower, element.lower, previous.name)
                new_item.set_resources(previous.resources)
                self.segment_list[i - 1] = new_item
            i+=1

    def dissolve_tiny_slots(self, minimum_size: float):
        """
        Eliminates segments that are smaller than the specified minimum size
        by redistributing their duration to the adjacent segments.

        :param minimum_size: The minimum size of a segment
                            that should not be dissolved.
        """
        self.segment_list.sort(key=lambda item : item.lower)
        i=1
        while i < len(self.segment_list) - 1:
            previous = self.segment_list[i - 1]
            next_ = self.segment_list[i + 1]
            element = self.segment_list[i]
            if 0 < element.upper - element.lower < minimum_size:
                half_duration = (element.upper - element.lower) / 2
                # Recreate the previous with the updated duration
                new_previous = ResourceInterval(previous.lower, previous.upper + half_duration, previous.name)
                new_previous.set_resources(previous.resources)
                self.segment_list[i - 1] = new_previous
                # Recreate the next with the updated duration
                new_next = ResourceInterval(next_.lower - half_duration, next_.upper , next_.name)
                new_next.set_resources(next_.resources)
                self.segment_list[i + 1] = new_next
                # Remove the tiny slot
                del self.segment_list[i]
            else:
                i+=1



    def dump_sht_file(self, plan_path: Path):
        sht_struct = self.to_sht_struct()
        with plan_path.open("w") as plan_file:
            json.dump(sht_struct, plan_file, indent=2)

    def summary(self):
        summary = "=== Summary ===\n"
        for segment in self.base_map.values():
            summary += segment.summary()
        return summary


class ExistingDefinitionError(Exception):

    def __init__(self, name: str) -> None:
        super().__init__(f"Previously existing {name}")
