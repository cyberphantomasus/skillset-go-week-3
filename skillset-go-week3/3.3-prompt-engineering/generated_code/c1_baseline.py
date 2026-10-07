import re

def parse_duration(s):
    total = 0
    units = {"h": 3600, "m": 60, "s": 1}
    for value, unit in re.findall(r"(\d+)([hms])", s):
        total += int(value) * units[unit]
    return total

print(parse_duration("1h30m"))  # 5400
