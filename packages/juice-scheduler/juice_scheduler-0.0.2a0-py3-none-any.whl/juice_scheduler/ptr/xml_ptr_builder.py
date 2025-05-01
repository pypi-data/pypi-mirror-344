from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from juice_scheduler.model.interval_list import ResourceInterval

from defusedxml import minidom

from juice_scheduler.common.date_utils import timestamp_to_datestr
from juice_scheduler.ptr.xml_ptr import PtrXml


class XMLPtrBuilder:

    def __init__(self, block_cache: dict[str, str]):
        self.block_cache = block_cache

    def generate_ptr(self, segments: list[ResourceInterval]):

        xml = PtrXml()
        previous_end = "1999"


        for index, segment in enumerate(segments):
            start = timestamp_to_datestr(segment.lower)
            end = timestamp_to_datestr(segment.upper)
            mnemonic = segment.name
            if previous_end > start:
                raise OverlappingBlockError(index)
            block_snippet = self.get_pointing_request_snippet(mnemonic)
            previous_end = end

            xml.add_block(
                start, end,
                block_snippet, index == len(segments) - 1)

        return minidom.parseString(xml.to_string()).toprettyxml(indent="   ")


    def get_pointing_request_snippet(self, mnemonic: str):
        return self.block_cache.get(mnemonic)


class OverlappingBlockError(Exception):
    def __init__(self, index: int) -> None:
        super().__init__(f"Overlapping block {index}")
