import re

import pytest

_TOKEN = re.compile(r"(\d+)\s*([hms])", re.IGNORECASE)
_VALID = re.compile(r"\s*(?:\d+\s*[hms]\s*)+", re.IGNORECASE)
_SECONDS = {"h": 3600, "m": 60, "s": 1}


def parse_duration(text: str) -> int:
    """Convert a duration string such as '1h30m' or '1h 30m 15s' into total seconds.

    Supports h, m and s units in any combination, optional whitespace, and
    upper- or lower-case letters.

    Raises:
        ValueError: if the text is empty, malformed, or contains a negative value.
    """
    if not _VALID.fullmatch(text):
        raise ValueError(f"invalid duration: {text!r}")
    return sum(int(n) * _SECONDS[u.lower()] for n, u in _TOKEN.findall(text))


@pytest.mark.parametrize(
    "text, expected",
    [("1h30m", 5400), ("45s", 45), ("2h", 7200), ("90m", 5400), ("1h 30m 15s", 5415), ("1H30M", 5400)],
)
def test_valid(text, expected):
    assert parse_duration(text) == expected


@pytest.mark.parametrize("text", ["", "abc", "1x", "-5m", "1h30"])
def test_invalid(text):
    with pytest.raises(ValueError):
        parse_duration(text)
