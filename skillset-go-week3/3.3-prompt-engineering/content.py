"""Test inputs, prompts and verbatim model outputs for Task 3.3.

Outputs were produced by Claude (the assistant used to prepare this sheet) in response to
each prompt exactly as written below. They are stored verbatim and scored by code in score.py.
"""

REASONING_Q = ("A bakery sells muffins at $3 each, or a box of 6 for $15. Sam wants exactly 20 muffins "
               "at the lowest total cost. How much will Sam pay?")

EMAIL = ("Hi team, this is Priya Nair from Brightline Logistics. Our order #48213 (placed 3 March) arrived "
         "damaged - 2 of the 12 monitors have cracked screens. We paid $3,480 in total and would like a "
         "replacement for the two units, not a refund. Please reply to priya.nair@brightline.example. "
         "Also, I'll be out of office from the 20th.")

ARTICLE = ("The city of Marlow ran a six-month bike-share pilot from April to September. The program placed 300 "
           "bikes at 40 docking stations, mostly near the university and the central train station. Riders made "
           "an average of 4,200 trips per day, and a follow-up survey of 1,100 riders found that 18% said they "
           "used the bikes in place of a car trip. Operating costs came to $410,000, about $90,000 over budget, "
           "mainly because of vandalism and the cost of redistributing bikes between stations. The council noted "
           "that the pilot ran only during the warmest months, so winter demand is unknown. A vote on whether to "
           "expand the program to 120 stations is scheduled for November.")

CODING_TASK = "Write a Python function that converts a duration string like '1h30m' into seconds."

R2_SUFFIX = "\n\nThink step by step before giving your answer."
R3_SUFFIX = ("\n\nSolve this by:\n"
             "1. Listing every way to buy exactly 20 muffins using boxes of 6 and single muffins.\n"
             "2. Calculating the total cost of each way.\n"
             "3. Choosing the cheapest and checking that it totals exactly 20 muffins.\n"
             "End with a final line in exactly this format: ANSWER: $<amount>")

E2_PROMPT = ("Extract these fields from the email below as JSON, using exactly these keys: customer_name, company, "
             "order_id, order_date, issue, total_paid, resolution_requested, phone.\n\nEmail:\n" + EMAIL)
E3_PROMPT = ("Extract information from the email below and return ONLY a JSON object (no code fences, no commentary) "
             "with exactly these keys:\n"
             "- customer_name (string)\n- company (string)\n- order_id (string, digits only, no '#')\n"
             "- order_date (string, as written in the email)\n- issue (string, one sentence)\n"
             "- total_paid (number, no currency symbol)\n- resolution_requested (string)\n- phone (string)\n\n"
             "Rules: use null for any field the email does not state; never guess or invent values; ignore details "
             "unrelated to these fields.\n\nEmail:\n" + EMAIL)

S3_PROMPT = ("Summarize the text below for a busy city manager.\n\nRequirements:\n"
             "- Maximum 40 words, in 2 sentences\n"
             "- Must include: the usage result, the cost overrun, the winter-demand caveat, and the November vote\n"
             "- Use only facts stated in the text; do not add anything new\n\nText:\n" + ARTICLE)

C2_SUFFIX = ("\n\nRequirements: support h, m and s in any combination (e.g. '1h30m', '45s', '90m', '1h 30m 15s'); "
             "allow optional spaces; be case-insensitive; raise ValueError for empty, malformed or negative input "
             "(e.g. '', 'abc', '1x', '-5m', '1h30').")
C3_SUFFIX = (C2_SUFFIX + "\n\nAlso: add type hints and a docstring, and include a small set of pytest tests covering "
             "normal and invalid inputs. Return only code blocks, with no explanation.")

ITEMS = []

# ---------------------------------------------------------------- Reasoning
ITEMS.append(dict(
    id="R-1", category="Reasoning", version="v1 (baseline)",
    prompt=REASONING_Q,
    change="Baseline: the bare question, no instructions.",
    output="""Sam pays $51.

A box of 6 costs $15 ($2.50 per muffin), which beats the $3 single price, so use as many boxes as fit into 20 muffins: 3 boxes = 18 muffins = $45. The remaining 2 muffins are bought singly: 2 x $3 = $6.

Total: $45 + $6 = $51."""))

ITEMS.append(dict(
    id="R-2", category="Reasoning", version="v2",
    prompt=REASONING_Q + R2_SUFFIX,
    change="Added 'Think step by step' to encourage visible reasoning.",
    output="""Step 1: A box of 6 costs $15, which is $2.50 per muffin - cheaper than the $3 single price - so boxes should be used wherever possible.
Step 2: 20 / 6 = 3 boxes with a remainder of 2. Three boxes give 18 muffins.
Step 3: The last 2 muffins can't be another box (that would give 24, not exactly 20), so they are bought singly: 2 x $3 = $6.
Step 4: Cost = 3 x $15 + $6 = $45 + $6 = $51.

Sam pays $51."""))

ITEMS.append(dict(
    id="R-3", category="Reasoning", version="v3",
    prompt=REASONING_Q + R3_SUFFIX,
    change=("Replaced the generic instruction with an explicit procedure (enumerate every option, cost each, verify "
            "the count) and a fixed final-line format so the answer can be checked automatically."),
    output="""1. Ways to buy exactly 20 muffins (6b + s = 20, b = boxes, s = singles):
   - 0 boxes + 20 singles
   - 1 box + 14 singles
   - 2 boxes + 8 singles
   - 3 boxes + 2 singles
   (4 boxes would be 24 muffins, which is more than 20.)
2. Costs:
   - 0 boxes: 20 x $3 = $60
   - 1 box: $15 + 14 x $3 = $57
   - 2 boxes: $30 + 8 x $3 = $54
   - 3 boxes: $45 + 2 x $3 = $51
3. Cheapest is 3 boxes + 2 singles at $51. Check: 3 x 6 + 2 = 20 muffins.

ANSWER: $51"""))

# ---------------------------------------------------------------- Extraction
ITEMS.append(dict(
    id="E-1", category="Extraction", version="v1 (baseline)",
    prompt="Get the important details from this email.\n\nEmail:\n" + EMAIL,
    change="Baseline: vague request, no output format.",
    output="""Here are the key details:

- Sender: Priya Nair of Brightline Logistics
- Order: #48213, placed 3 March
- Problem: the order arrived damaged - 2 of the 12 monitors have cracked screens
- Amount paid: $3,480
- Request: replacement of the two damaged units (not a refund)
- Contact: priya.nair@brightline.example
- Note: she will be out of office from the 20th"""))

ITEMS.append(dict(
    id="E-2", category="Extraction", version="v2",
    prompt=E2_PROMPT,
    change="Asked for JSON with exactly named keys so the output has a fixed structure.",
    output="""```json
{
  "customer_name": "Priya Nair",
  "company": "Brightline Logistics",
  "order_id": "48213",
  "order_date": "3 March",
  "issue": "2 of the 12 monitors arrived with cracked screens",
  "total_paid": 3480,
  "resolution_requested": "Replacement of the two damaged units",
  "phone": null
}
```
The email doesn't include a phone number, so I set that field to null."""))

ITEMS.append(dict(
    id="E-3", category="Extraction", version="v3",
    prompt=E3_PROMPT,
    change=("Added field types, null-for-missing and no-guessing rules, 'JSON only' (no fences or commentary) and "
            "an instruction to ignore unrelated details, so the output can be parsed directly."),
    output="""{
  "customer_name": "Priya Nair",
  "company": "Brightline Logistics",
  "order_id": "48213",
  "order_date": "3 March",
  "issue": "2 of the 12 monitors arrived with cracked screens.",
  "total_paid": 3480,
  "resolution_requested": "Replacement of the two damaged units, not a refund",
  "phone": null
}"""))

# ---------------------------------------------------------------- Summarization
ITEMS.append(dict(
    id="S-1", category="Summarization", version="v1 (baseline)",
    prompt="Summarize this.\n\n" + ARTICLE,
    change="Baseline: 'Summarize this.'",
    output=("Marlow's six-month bike-share pilot (300 bikes, 40 stations, April to September) averaged 4,200 trips a "
            "day, and 18% of surveyed riders said they replaced a car trip with a bike. It cost $410,000, roughly "
            "$90,000 over budget because of vandalism and the expense of moving bikes between stations. Because it "
            "only ran in warm months, winter demand is unknown, and the council votes in November on expanding to "
            "120 stations.")))

ITEMS.append(dict(
    id="S-2", category="Summarization", version="v2",
    prompt="Summarize this for a busy city manager in two sentences.\n\n" + ARTICLE,
    change="Added an audience (busy city manager) and a sentence limit.",
    output=("Marlow's six-month bike-share pilot averaged 4,200 trips a day, with 18% of surveyed riders replacing a "
            "car trip, but it cost $410,000, about $90,000 over budget, due to vandalism and bike redistribution. "
            "Winter demand is untested because the pilot ran only in warm months, and the council votes in November "
            "on expanding to 120 stations.")))

ITEMS.append(dict(
    id="S-3", category="Summarization", version="v3",
    prompt=S3_PROMPT,
    change=("Replaced the sentence limit with a word cap plus a required-content list and an instruction to add "
            "nothing new."),
    output=("Marlow's bike-share pilot averaged 4,200 trips a day but ran about $90,000 over budget. Winter demand is "
            "unknown because it ran only in warm months, and the council votes in November on expanding to 120 "
            "stations.")))

# ---------------------------------------------------------------- Coding
ITEMS.append(dict(
    id="C-1", category="Coding", version="v1 (baseline)",
    prompt=CODING_TASK,
    change="Baseline: the bare task.",
    output='''```python
import re

def parse_duration(s):
    total = 0
    units = {"h": 3600, "m": 60, "s": 1}
    for value, unit in re.findall(r"(\\d+)([hms])", s):
        total += int(value) * units[unit]
    return total

print(parse_duration("1h30m"))  # 5400
```
This finds each number-plus-unit pair and adds up its value in seconds.'''))

ITEMS.append(dict(
    id="C-2", category="Coding", version="v2",
    prompt=CODING_TASK + C2_SUFFIX,
    change=("Specified supported units and formats, case-insensitivity, and an error contract (ValueError for "
            "invalid input, with examples)."),
    output='''```python
import re

_TOKEN = re.compile(r"(\\d+)\\s*([hms])", re.IGNORECASE)
_VALID = re.compile(r"\\s*(?:\\d+\\s*[hms]\\s*)+", re.IGNORECASE)

def parse_duration(s):
    if not _VALID.fullmatch(s):
        raise ValueError(f"invalid duration: {s!r}")
    units = {"h": 3600, "m": 60, "s": 1}
    return sum(int(n) * units[u.lower()] for n, u in _TOKEN.findall(s))
```
The whole string is validated first, then each number-plus-unit pair is summed.'''))

ITEMS.append(dict(
    id="C-3", category="Coding", version="v3",
    prompt=CODING_TASK + C3_SUFFIX,
    change="Added deliverable requirements: type hints, a docstring, pytest tests, and code only.",
    output='''```python
import re

import pytest

_TOKEN = re.compile(r"(\\d+)\\s*([hms])", re.IGNORECASE)
_VALID = re.compile(r"\\s*(?:\\d+\\s*[hms]\\s*)+", re.IGNORECASE)
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
```'''))
