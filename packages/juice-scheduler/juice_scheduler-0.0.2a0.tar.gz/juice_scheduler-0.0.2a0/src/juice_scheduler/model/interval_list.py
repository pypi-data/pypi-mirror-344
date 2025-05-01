from __future__ import annotations

from copy import deepcopy
from datetime import timedelta
from typing import TYPE_CHECKING

from portion import Interval, closed, to_data
from portion import open as open_interval

if TYPE_CHECKING:
    from juice_scheduler.model.prime import PrimeNameExpander
    from juice_scheduler.model.resources import ResourceHandler

from juice_scheduler.common.date_utils import timestamp_to_datestr


class IntervalList:
    def __init__(self, name: str, working_group: str) -> None:
        self.name = name
        self.working_group = working_group
        self.instances: DateStrInterval = DateStrInterval()
        self.expanded: dict[str, ExpandedIntervalList] = {}

    def add_instance(self, start: float, end: float) -> None:
        if start > end:
            raise InvalidIntervalError
        self.instances = self.instances.union(closed(start, end))

    def add_all_instances(self, other: IntervalList):
        self.instances = self.instances.union(other.instances)

    def substract(self, interval: DateStrInterval) -> None:
        self.instances = self.instances - interval

    def deep_copy(self) -> IntervalList:
        return deepcopy(self)

    def do_expansion(self, expander: PrimeNameExpander):
        for interval in to_data(self.instances):
            instance_name = expander.expand(interval[1], interval[2])
            if instance_name not in self.expanded:
                self.expanded[instance_name] = ExpandedIntervalList(instance_name, self.working_group, self.name)
            self.expanded[instance_name].add_instance(interval[1], interval[2])
        return self.expanded

    def __repr__(self) -> str:
        return repr(self.instances)

    def to_sht_struct(self) -> list[object]:
        segments = []
        for instance in self.instances:
            for interval in to_data(instance):
                segments.append({
                    "start": timestamp_to_datestr(interval[1]),
                    "end":  timestamp_to_datestr(interval[2]),
                    "timeline": "PRIME",
                    "segment_definition": self.name,
                    "resources": [],
                    "instrument_resources": [],
                    "overwritten": False,
                    "instrument_overwritten": False,
                })
        return segments

    def total_duration_secs(self):
        return self.instances.total_duration_secs()

    def summary(self):
        segment_duration = self.total_duration_secs()
        duration_formatted = timedelta(seconds=segment_duration)
        return (f"| {self.name:24s} | {len(self.instances):>4} "
                f"| {duration_formatted!s:20s} | {segment_duration:>12} |")

    def probably_equal(self, other: IntervalList):
        return (self.instances == other.instances) and \
                (self.total_duration_secs() == other.total_duration_secs())

class ExpandedIntervalList(IntervalList):
    def __init__(self, name: str, working_group: str, parent: str):
        super().__init__(name, working_group)
        self.parent = parent

    def deep_copy(self) -> ExpandedIntervalList:
        return deepcopy(self)

    def do_expansion(self, _expander: PrimeNameExpander):
        raise ValueError

class InvalidIntervalError(Exception):
    pass


class DateStrInterval(Interval):
    def __repr__(self):
        if self.empty:
            return "[]"
        string = []
        for interval in self._intervals:
            if interval.lower == interval.upper:
                string.append("[" + timestamp_to_datestr(interval.lower) + "]")
            else:
                string.append(
                    ("[")
                    + timestamp_to_datestr(interval.lower)
                    + ","
                    + timestamp_to_datestr(interval.upper)
                    + ("]"),
                )
        return " | ".join(string)

    def total_duration_secs(self):
        return sum((interval.upper - interval.lower) for interval in self._intervals)

class ResourceInterval(DateStrInterval):

    def __init__(self, start: float, end: float, name: str):
        super().__init__(closed(start, end))
        self.resources = []
        self.name = name

    def set_resources(self, resources: list[ResourceInterval]):
        self.resources = resources

    def get_duration(self):
        return self.upper - self.lower

    def __repr__(self):
        return super().__repr__() + f" {self.resources}"

    def to_json(self):
        return {
                    "start": timestamp_to_datestr(self.lower),
                    "end":  timestamp_to_datestr(self.upper),
                    "timeline": "PRIME",
                    "segment_definition": self.name,
                    "resources": [resource.to_json() for resource in self.resources if resource.is_instrument_type()],
                    "instrument_resources": [
                        resource.to_json() for resource in self.resources if not resource.is_instrument_type()],
                    "overwritten": False,
                    "instrument_overwritten": False,
                }


def merge(resource_handler: ResourceHandler,
          merged: list[ResourceInterval], segment_list: ExpandedIntervalList) -> list[ResourceInterval]:
    """
    Merges a list of ResourceIntervals with an ExpandedSegmentList, resolving overlaps
    and restoring original non-overlapping intervals, while merging resources where needed.

    Args:
        resource_handler (ResourceHandler): Handler for managing resources associated with segments.
        merged (list[ResourceInterval]): List of ResourceIntervals to be merged.
        segment_list (ExpandedSegmentList): The segment list with which to merge the intervals.

    Returns:
        list[ResourceInterval]: A list of ResourceIntervals after merging and resolving overlaps.
    """

    result = []
    # Create a copy of the segment list
    copy = segment_list.deep_copy()

    originals: dict[ResourceInterval, DateStrInterval] = {}
    overlaps: dict[ResourceInterval, DateStrInterval] = {}

    # We get the overlaps of each merged instance
    for item in merged:
        # Open interval, we avoid instant overlaps
        interval = DateStrInterval()
        interval = interval.union(open_interval(item.lower, item.upper))
        if copy.instances.overlaps(interval):
            intersection = copy.instances.intersection(interval)
            overlaps[item] = intersection
            originals[item] = interval - intersection
            copy.substract(intersection)
        else:
            result.append(item)

    # We restore the original items
    for item in originals:
        for interval in to_data(originals[item]):
            ri = ResourceInterval(interval[1], interval[2], item.name)
            ri.set_resources(item.resources)
            result.append(ri)

    # Include overlaps
    for item in overlaps:
        for overlap in to_data(overlaps[item]):
            start = overlap[1]
            end = overlap[2]
            ri = ResourceInterval(start, end, item.name)
            item_resources = item.resources
            segment_list_resources = resource_handler.get_resources(copy.parent, start, end)
            ri.set_resources(merge_resources(item_resources, segment_list_resources))
            result.append(ri)

    # Finally the non overlaping intervals in the segment list are added to the merged result
    for copy_interval in to_data(copy.instances):
        start = copy_interval[1]
        end = copy_interval[2]
        ri = ResourceInterval(start, end, copy.name)
        ri.set_resources(
            resource_handler.get_resources(copy.parent, start, end))
        result.append(ri)

    return result


def merge_resources(res1: list[ResourceInterval], _res2: list[ResourceInterval]) -> list[ResourceInterval]:
    return res1
