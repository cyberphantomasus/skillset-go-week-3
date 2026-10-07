import re

_TOKEN = re.compile(r"(\d+)\s*([hms])", re.IGNORECASE)
_VALID = re.compile(r"\s*(?:\d+\s*[hms]\s*)+", re.IGNORECASE)

def parse_duration(s):
    if not _VALID.fullmatch(s):
        raise ValueError(f"invalid duration: {s!r}")
    units = {"h": 3600, "m": 60, "s": 1}
    return sum(int(n) * units[u.lower()] for n, u in _TOKEN.findall(s))
