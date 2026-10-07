"""Black-box audit tests for the expense tracker CLI.

The same tests run against any version of the app, chosen with the APP_UNDER_TEST env var
(default: the corrected app). Each test runs the CLI in a fresh temporary directory.

Requirements being checked (written before running the tests against v1):
  R1  Amounts must be finite, greater than zero, with at most 2 decimal places.
  R2  Dates must be valid calendar dates (YYYY-MM-DD).
  R3  Expense IDs must be unique among stored expenses, including after deletions.
  R4  Categories are case-insensitive ("Food" and "food" are one category).
  R5  A corrupted data file produces a clean error (no traceback) and is never overwritten.
  R6  Failures exit with a non-zero status (including deleting an ID that does not exist).
  R7  Descriptions must not be empty or whitespace only.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

DEFAULT_APP = Path(__file__).resolve().parent.parent / "app" / "expense_tracker.py"
APP = Path(os.environ.get("APP_UNDER_TEST", DEFAULT_APP)).resolve()


def run(cwd, *args):
    env = {k: v for k, v in os.environ.items() if k != "EXPENSES_FILE"}
    return subprocess.run([sys.executable, str(APP), *args], cwd=cwd, capture_output=True, text=True, env=env)


def add(cwd, amount="10.00", category="food", desc="lunch", date=None):
    args = ["add", "--amount", amount, "--category", category, "--desc", desc]
    if date:
        args += ["--date", date]
    return run(cwd, *args)


def stored(cwd):
    path = Path(cwd) / "expenses.json"
    return json.loads(path.read_text()) if path.exists() else []


# ------------------------------------------------------------------ happy paths (should hold in every version)
def test_add_valid_expense_succeeds(tmp_path):
    r = add(tmp_path, "12.50", "food", "lunch")
    assert r.returncode == 0
    assert "12.50" in r.stdout
    assert len(stored(tmp_path)) == 1


def test_summary_totals(tmp_path):
    add(tmp_path, "10.10", "food", "a")
    add(tmp_path, "20.20", "transport", "b")
    r = run(tmp_path, "summary")
    assert r.returncode == 0
    assert "30.30" in r.stdout


def test_list_filters_by_category(tmp_path):
    add(tmp_path, "10.00", "food", "lunch")
    add(tmp_path, "5.00", "transport", "bus")
    r = run(tmp_path, "list", "--category", "food")
    assert "lunch" in r.stdout and "bus" not in r.stdout


# ------------------------------------------------------------------ R1 amounts
@pytest.mark.parametrize("bad", ["-5", "0", "1.239", "nan", "inf", "abc"])
def test_invalid_amount_rejected(tmp_path, bad):
    r = add(tmp_path, bad)
    assert r.returncode != 0, f"amount {bad!r} was accepted"
    assert "Traceback" not in r.stderr
    assert stored(tmp_path) == []


# ------------------------------------------------------------------ R2 dates
@pytest.mark.parametrize("bad", ["2026-13-45", "yesterday"])
def test_invalid_date_rejected(tmp_path, bad):
    r = add(tmp_path, date=bad)
    assert r.returncode != 0, f"date {bad!r} was accepted"
    assert stored(tmp_path) == []


# ------------------------------------------------------------------ R3 ids
def test_ids_unique_after_delete(tmp_path):
    for name in ("a", "b", "c"):
        add(tmp_path, desc=name)
    run(tmp_path, "delete", "1")
    add(tmp_path, desc="d")
    ids = [e["id"] for e in stored(tmp_path)]
    assert len(ids) == len(set(ids)), f"duplicate ids: {ids}"


# ------------------------------------------------------------------ R4 categories
def test_category_case_insensitive_summary(tmp_path):
    add(tmp_path, "10.00", "Food", "a")
    add(tmp_path, "5.00", "food", "b")
    out = run(tmp_path, "summary").stdout
    food_lines = [line for line in out.splitlines() if "food" in line.lower()]
    assert len(food_lines) == 1, f"category split across lines: {food_lines}"
    assert "15.00" in out


# ------------------------------------------------------------------ R5 corrupted storage
def test_corrupted_file_gives_clean_error(tmp_path):
    (tmp_path / "expenses.json").write_text("{not valid json")
    r = run(tmp_path, "list")
    assert r.returncode != 0
    assert "Traceback" not in r.stderr
    assert r.stderr.strip() != ""


def test_corrupted_file_not_overwritten_by_add(tmp_path):
    bad = "{not valid json"
    (tmp_path / "expenses.json").write_text(bad)
    add(tmp_path)
    assert (tmp_path / "expenses.json").read_text() == bad


# ------------------------------------------------------------------ R6 exit codes
def test_delete_missing_id_fails(tmp_path):
    add(tmp_path)
    r = run(tmp_path, "delete", "99")
    assert r.returncode != 0
    assert "Traceback" not in r.stderr


# ------------------------------------------------------------------ R7 description
def test_blank_description_rejected(tmp_path):
    r = add(tmp_path, desc="   ")
    assert r.returncode != 0
    assert stored(tmp_path) == []
