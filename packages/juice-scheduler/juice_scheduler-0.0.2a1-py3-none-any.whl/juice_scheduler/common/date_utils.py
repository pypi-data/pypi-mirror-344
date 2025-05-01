from datetime import datetime, timezone

GEOPIPELINE_FORMAT_SIZE = 19
SECONDS_FORMAT_SIZE = 20
MILLISECONDS_FORMAT_SIZE = 24

def datestr_to_timestamp(datestr: str) -> float:

    # Geopipeline date format
    if len(datestr) == GEOPIPELINE_FORMAT_SIZE:
        date = datetime.strptime(datestr, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
        return date.timestamp()

    if len(datestr) == SECONDS_FORMAT_SIZE:
        date = datetime.strptime(datestr, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        return date.timestamp()

    if len(datestr) == MILLISECONDS_FORMAT_SIZE:
        date = datetime.strptime(datestr, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
        return date.timestamp()

    raise InvalidDateFormatError(datestr)


class InvalidDateFormatError(Exception):
    def __init__(self, datestr: str) -> None:
        super().__init__(f"Invalid date format {datestr}")

def timestamp_to_datestr(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat(timespec="milliseconds")[:23] + "Z"

def filename_timestamp() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y%m%d-%H%M%S")
