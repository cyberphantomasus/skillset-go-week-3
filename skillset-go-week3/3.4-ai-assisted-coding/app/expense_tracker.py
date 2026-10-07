"""Command-line expense tracker (corrected version, after audit of v1).

Usage:
    python expense_tracker.py add --amount 12.50 --category food --desc "lunch" [--date 2026-10-06]
    python expense_tracker.py list [--category food]
    python expense_tracker.py delete ID
    python expense_tracker.py summary

Data is stored in expenses.json in the current directory (override with the EXPENSES_FILE
environment variable).
"""
import argparse
import json
import os
import sys
import tempfile
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

CENT = Decimal("0.01")
MAX_AMOUNT = Decimal("1000000000")
MAX_CATEGORY_LEN = 30
MAX_DESC_LEN = 200
REQUIRED_FIELDS = {"id", "date", "category", "description", "amount"}


class ExpenseError(Exception):
    """A user-facing error: reported as a one-line message with a non-zero exit status."""


def data_file():
    return os.environ.get("EXPENSES_FILE", "expenses.json")


# ---------------------------------------------------------------- validation
def parse_amount(text):
    """Return a positive, finite Decimal with at most 2 decimal places."""
    try:
        value = Decimal(str(text).strip())
    except InvalidOperation:
        raise ExpenseError(f"invalid amount: {text!r}")
    if not value.is_finite():
        raise ExpenseError(f"invalid amount: {text!r}")
    if value <= 0:
        raise ExpenseError("amount must be greater than zero")
    if value > MAX_AMOUNT:
        raise ExpenseError(f"amount must not exceed {MAX_AMOUNT}")
    if value != value.quantize(CENT):
        raise ExpenseError("amount can have at most 2 decimal places")
    return value.quantize(CENT)


def parse_date(text):
    """Return an ISO date string (YYYY-MM-DD); default is today."""
    if text is None:
        return date.today().isoformat()
    try:
        return datetime.strptime(text.strip(), "%Y-%m-%d").date().isoformat()
    except ValueError:
        raise ExpenseError(f"invalid date: {text!r} (use a real date as YYYY-MM-DD)")


def normalize_category(text):
    value = text.strip().lower()
    if not value:
        raise ExpenseError("category must not be empty")
    if len(value) > MAX_CATEGORY_LEN:
        raise ExpenseError(f"category must be at most {MAX_CATEGORY_LEN} characters")
    return value


def clean_description(text):
    value = text.strip()
    if not value:
        raise ExpenseError("description must not be empty")
    if len(value) > MAX_DESC_LEN:
        raise ExpenseError(f"description must be at most {MAX_DESC_LEN} characters")
    return value


# ---------------------------------------------------------------- storage
def load_expenses():
    path = data_file()
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            expenses = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError, OSError) as exc:
        raise ExpenseError(f"cannot read {path}: {exc.__class__.__name__}. The file was not modified; "
                           "fix or move it and try again.")
    if not isinstance(expenses, list) or not all(isinstance(e, dict) and REQUIRED_FIELDS <= e.keys()
                                                 for e in expenses):
        raise ExpenseError(f"{path} does not look like an expense file. It was not modified.")
    return expenses


def save_expenses(expenses):
    """Write atomically: build a temp file in the same directory, then replace the original."""
    path = data_file()
    directory = os.path.dirname(os.path.abspath(path))
    fd, tmp_path = tempfile.mkstemp(dir=directory, prefix=".expenses-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(expenses, f, indent=2, allow_nan=False)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


# ---------------------------------------------------------------- commands
def add_expense(amount, category, description, when=None):
    amount = parse_amount(amount)
    category = normalize_category(category)
    description = clean_description(description)
    when = parse_date(when)

    expenses = load_expenses()
    new_id = max((e["id"] for e in expenses), default=0) + 1
    expenses.append({"id": new_id, "date": when, "category": category,
                     "description": description, "amount": str(amount)})
    save_expenses(expenses)
    print(f"Added expense #{new_id}: {amount} for {category}")


def list_expenses(category=None):
    expenses = load_expenses()
    if category:
        wanted = normalize_category(category)
        expenses = [e for e in expenses if e["category"] == wanted]
    if not expenses:
        print("No expenses found.")
        return
    for e in expenses:
        print(f"{e['id']:>3}  {e['date']}  {e['category']:<12} {Decimal(e['amount']):>10}  {e['description']}")


def delete_expense(expense_id):
    expenses = load_expenses()
    remaining = [e for e in expenses if e["id"] != expense_id]
    if len(remaining) == len(expenses):
        raise ExpenseError(f"no expense with id {expense_id}")
    save_expenses(remaining)
    print(f"Deleted expense #{expense_id}")


def summary():
    totals = {}
    for e in load_expenses():
        totals[e["category"]] = totals.get(e["category"], Decimal("0")) + Decimal(e["amount"])
    for cat, total in sorted(totals.items()):
        print(f"{cat:<12} {total:>10}")
    print(f"{'TOTAL':<12} {sum(totals.values(), Decimal('0')):>10}")


# ---------------------------------------------------------------- CLI
def build_parser():
    parser = argparse.ArgumentParser(description="Simple expense tracker")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="add an expense")
    p_add.add_argument("--amount", required=True, help="positive amount, at most 2 decimals")
    p_add.add_argument("--category", required=True)
    p_add.add_argument("--desc", required=True)
    p_add.add_argument("--date", help="YYYY-MM-DD (default: today)")

    p_list = sub.add_parser("list", help="list expenses")
    p_list.add_argument("--category")

    p_del = sub.add_parser("delete", help="delete an expense by id")
    p_del.add_argument("id", type=int)

    sub.add_parser("summary", help="totals by category")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.command == "add":
            add_expense(args.amount, args.category, args.desc, args.date)
        elif args.command == "list":
            list_expenses(args.category)
        elif args.command == "delete":
            delete_expense(args.id)
        elif args.command == "summary":
            summary()
    except ExpenseError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
