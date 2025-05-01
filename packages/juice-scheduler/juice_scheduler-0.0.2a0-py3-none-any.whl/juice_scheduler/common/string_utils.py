from __future__ import annotations

import re


def filter_strings(strings: list[str], patterns:list[str]) -> list[str]:
    """
    Filter a list of strings based on a list of regular expression patterns.

    Args:
        strings (list[str]): The list of strings to filter.
        patterns (list[str]): The list of regular expression patterns.

    Returns:
        list[str]: The strings that match any of the patterns.
    """
    return [s for s in strings if any(re.match(p, s) for p in patterns)]
