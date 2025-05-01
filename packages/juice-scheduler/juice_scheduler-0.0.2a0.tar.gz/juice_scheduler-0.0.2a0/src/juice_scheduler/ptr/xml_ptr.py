import xml.etree.ElementTree as ET

from defusedxml.ElementTree import fromstring


class PtrXml:

    def __init__(self):
        self.blocks = []

    @staticmethod
    def time_formatter(date_str):
        return date_str[:19]

    @staticmethod
    def add_or_replace(parent, tag, text=None):
        item = parent.find(tag)
        if item is None:
            item = ET.SubElement(parent, tag)
        if text:
            item.text = text
        return item

    @staticmethod
    def add(parent, tag, text=None):
        item = ET.SubElement(parent, tag)
        if text:
            item.text = text
        return item

    @staticmethod
    def clean_xml(block):
        for item in block.iter():
            if item.text and len(item.text.strip()) == 0:
                item.text = ""
            if item.tail:
                item.tail = ""
        return block

    @staticmethod
    def remove(parent, tag):
        item = parent.find(tag)
        if item is not None:
            parent.remove(item)

    @staticmethod
    def get(parent, tag):
        item = parent.find(tag)
        if item is None:
            return None
        return item.text

    def add_block(
            self, start, end, snippet, last):

        try:
            block = fromstring(snippet)
            block = PtrXml.clean_xml(block)
        except ET.ParseError as err :
            raise NonValidSnippetError(PtrXml.time_formatter(start)) from err

        block_type = block.attrib.get("ref")
        slew_included = block_type in ["MWOL", "MTCM"]

        # Ensure that there is not time hardcoded in the block
        PtrXml.remove(block, "startTime")
        PtrXml.remove(block, "endTime")


        PtrXml.add_or_replace(block, "startTime", PtrXml.time_formatter(start))

        # If the block has slew included ant previous block was a slew, remove it
        if slew_included:
            previous_block = self.blocks[-1]
            previous_ref = previous_block.attrib.get("ref")
            if previous_ref == "SLEW":
                self.blocks.pop()
            elif previous_ref in ["MWOL", "MTCM"]:
                previous_start = PtrXml.get(previous_block, "startTime")
                PtrXml.add_or_replace(block, "startTime", PtrXml.time_formatter(previous_start))
                block.set("ref", "MWOL")
                self.blocks.pop()

        self.blocks.append(block)

        if (not last) and (not slew_included):
            slew = ET.Element("block")
            slew.set("ref", "SLEW")
            self.blocks.append(slew)
        else:
            PtrXml.add_or_replace(block, "endTime", PtrXml.time_formatter(end))

    def to_string(self):
        prm = ET.Element("prm")
        body = ET.SubElement(prm, "body")
        segment = ET.SubElement(body, "segment")
        data = ET.SubElement(segment, "data")
        timeline = ET.SubElement(data, "timeline")
        timeline.set("frame", "SC")
        for index, block in enumerate(self.blocks, 1):
            timeline.append(ET.Comment(f"Block ({index})"))
            timeline.append(block)

        return ET.tostring(prm, "unicode")


class NonValidSnippetError(Exception):
    def __init__(self, start: str) -> None:
        super().__init__(f"Not valid XML snipped {start}")
