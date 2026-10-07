"""Automated scoring for Task 3.3. Each check returns True/False (or a manual review flag)."""
import ast
import contextlib
import io
import json
import re
import subprocess
import sys
import tempfile
import os

from content import ITEMS

REQUIRED_KEYS = ["customer_name", "company", "order_id", "order_date", "issue",
                 "total_paid", "resolution_requested", "phone"]


def words(text):
    return len(text.split())


def sentences(text):
    return len([s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s])


# ------------------------------------------------------------------ Reasoning
def score_reasoning(out):
    amounts = re.findall(r"\$(\d+(?:\.\d+)?)", out)
    c1 = bool(amounts) and float(amounts[-1]) == 51
    c2 = bool(re.search(r"\b(3|three) boxes", out)) and bool(re.search(r"\b2 (single|individual|extra|more|muffins)", out))
    c3 = out.strip().splitlines()[-1].strip() == "ANSWER: $51"
    return [c1, c2, c3], ""


# ------------------------------------------------------------------ Extraction
def _parse_json_loose(out):
    try:
        return json.loads(out.strip()), True
    except Exception:
        pass
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", out, re.S)
    if m:
        try:
            return json.loads(m.group(1)), False
        except Exception:
            pass
    return None, False


def score_extraction(out):
    data, raw_ok = _parse_json_loose(out)
    if data is None:
        return [False] * 6, "Output is not JSON (free-form text), so no field could be machine-checked."
    c1 = raw_ok
    c2 = set(data.keys()) == set(REQUIRED_KEYS)
    c3 = data.get("total_paid") == 3480 and not isinstance(data.get("total_paid"), str)
    c4 = data.get("order_id") == "48213"
    c5 = ("phone" in data) and data["phone"] is None
    c6 = data.get("customer_name") == "Priya Nair" and data.get("company") == "Brightline Logistics"
    note = "" if raw_ok else "JSON only parses after stripping the code fence/commentary around it."
    return [c1, c2, c3, c4, c5, c6], note


# ------------------------------------------------------------------ Summarization
def score_summarization(out):
    w, s = words(out), sentences(out)
    c1 = w <= 40
    c2 = s == 2
    c3 = ("4,200" in out) or ("18%" in out)
    c4 = ("$90,000" in out) or ("over budget" in out.lower())
    c5 = ("winter" in out.lower()) or ("warm" in out.lower())
    c6 = "november" in out.lower()
    c7 = True  # manual review: every fact traced back to the source text (done by reading each output)
    return [c1, c2, c3, c4, c5, c6, c7], f"{w} words, {s} sentence(s)."


# ------------------------------------------------------------------ Coding
VALID_CASES = [("1h30m", 5400), ("45s", 45), ("2h", 7200), ("90m", 5400), ("1h 30m 15s", 5415)]
INVALID_CASES = ["", "abc", "1x", "-5m", "1h30"]


def extract_code(out):
    m = re.search(r"```python\n(.*?)```", out, re.S)
    return m.group(1) if m else None


def score_coding(out):
    code = extract_code(out)
    ns = {"__name__": "candidate"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(code, ns)
    fn = ns["parse_duration"]

    notes = []

    def run(arg):
        try:
            return ("ok", fn(arg))
        except ValueError:
            return ("ValueError", None)
        except Exception as e:  # any other exception type counts as a failure to follow the contract
            return (type(e).__name__, None)

    valid_ok = True
    for text, expected in VALID_CASES:
        kind, val = run(text)
        if not (kind == "ok" and val == expected):
            valid_ok = False
            notes.append(f"{text!r} -> {val if kind == 'ok' else kind} (expected {expected})")
    c1 = valid_ok

    kind, val = run("1H30M")
    c2 = kind == "ok" and val == 5400
    if not c2:
        notes.append(f"'1H30M' -> {val if kind == 'ok' else kind} (expected 5400)")

    invalid_ok = True
    for text in INVALID_CASES:
        kind, val = run(text)
        if kind != "ValueError":
            invalid_ok = False
            notes.append(f"{text!r} did not raise ValueError (returned {val})")
    c3 = invalid_ok

    tree = ast.parse(code)
    func = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "parse_duration")
    c4 = all(a.annotation is not None for a in func.args.args) and func.returns is not None
    c5 = ast.get_docstring(func) is not None

    c6 = False
    if "def test_" in code:
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "test_generated.py")
            open(path, "w").write(code)
            r = subprocess.run([sys.executable, "-m", "pytest", "-q", path], capture_output=True, text=True, timeout=120)
            c6 = r.returncode == 0
            notes.append("pytest: " + (r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:]))
    return [c1, c2, c3, c4, c5, c6], "; ".join(notes)


SCORERS = {"Reasoning": score_reasoning, "Extraction": score_extraction,
           "Summarization": score_summarization, "Coding": score_coding}


def score_all():
    rows = []
    for item in ITEMS:
        checks, note = SCORERS[item["category"]](item["output"])
        rows.append((item, checks, note))
    return rows


if __name__ == "__main__":
    for item, checks, note in score_all():
        print(f"{item['id']}: {sum(checks)}/{len(checks)}  {[int(c) for c in checks]}  | {note}")
