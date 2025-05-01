from __future__ import annotations

from portion import to_data

from juice_scheduler.model.interval_list import IntervalList


def filter_minimum_duration(segment: IntervalList):
    """
    Filter a SegmentList to remove segments with duration less than minimum_duration.

    If the segment name starts with 'DL_', the minimum_duration is set to 3 hours, otherwise it is set to 1 minute.

    Args:
        segment: The SegmentList to filter.

    Returns:
        The filtered SegmentList.
    """
    filtered = IntervalList(segment.name, segment.working_group)
    minimum_duration = 60
    if "DL_" in segment.name:
        minimum_duration = 3 * 3600
    filtered_instances = [item for item in to_data(segment.instances) if (item[2] - item[1]) >= minimum_duration]
    for _, start, end, _ in filtered_instances:
        filtered.add_instance(start, end)
    return filtered
