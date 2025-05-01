from __future__ import annotations

from typing import TYPE_CHECKING

from portion import closed, to_data

from juice_scheduler.common.date_utils import timestamp_to_datestr

if TYPE_CHECKING:
    from juice_scheduler.model.events import EventsHandler
    from juice_scheduler.model.mission_phase import MissionPhaseHandler


import logging

from juice_scheduler.model.interval_list import DateStrInterval, IntervalList


def adjust_calibration_windows(ev_handler: EventsHandler,
                               calib: IntervalList,
                               start_offet: float=6 * 3600, end_offset: float=6 * 3600) -> IntervalList:
    """
    Adjust calibration windows to be centered around perijoves.

    Parameters
    ----------
    ev_handler : EventsHandler
        Handler for events.
    calib : SegmentList
        Segment list with calibration instances.
    start_offet : float, optional
        Offset in seconds from the perijove to the start of the instance, by default 6 hours.
    end_offset : float, optional
        Offset in seconds from the perijove to the end of the instance, by default 6 hours.

    Returns
    -------
    SegmentList
        New segment list with adjusted calibration windows.
    """
    new_calib = IntervalList(calib.name, calib.working_group)
    for interval in calib.instances:
        _, start, end, _ = to_data(interval)[0]
        perijove = ev_handler.search_perijove(start, end)
        if perijove is None:
            logging.warning("Perijove not found for instance %s %s",
                            timestamp_to_datestr(start), timestamp_to_datestr(end))
        else:
            epoch = perijove.epoch
            lower_limit = epoch - start_offet
            upper_limit = epoch + end_offset

            new_start = max(lower_limit, start)
            new_end = min(upper_limit, end)

            new_calib.add_instance(new_start, new_end)

    return new_calib


def select_calibrations(phase_handler: MissionPhaseHandler,
                        phase_calib_selector: dict[str, list[int]],
                        calib: IntervalList) -> IntervalList:

    new_calib = IntervalList(calib.name, calib.working_group)

    for phase_name in phase_calib_selector:
        phase = phase_handler.get_mission_phase(phase_name)
        phase_interval = DateStrInterval(closed(phase.start, phase.end))
        candidates = to_data(phase_interval.intersection(calib.instances))
        phase_indices = phase_calib_selector[phase_name]

        # We use a set, to avoid repeated indexing (e.g. 3 element list, index 1 and -2 point to the same)
        for _, interval_start, interval_end, _ in {candidates[i] for i in phase_indices}:
            new_calib.add_instance(interval_start, interval_end)

    return new_calib

