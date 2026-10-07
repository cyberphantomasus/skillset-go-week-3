"""Simple command-line expense tracker.

v1: first version produced by the AI assistant in a single pass from this prompt:
"Build a small command-line expense tracker in Python: add, list, delete, and summarize
expenses by category, stored in a JSON file."
Kept unmodified as the starting point for the audit.
"""
import argparse
import json
import os
from datetime import date

DATA_FILE = "expenses.json"


def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f:
        return json.load(f)


def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def add_expense(amount, category, description, when=None):
    expenses = load_expenses()
    expense = {
        "id": len(expenses) + 1,
        "date": when or str(date.today()),
        "category": category,
        "description": description,
        "amount": amount,
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Added expense #{expense['id']}: {amount:.2f} for {category}")


def list_expenses(category=None):
    expenses = load_expenses()
    if category:
        expenses = [e for e in expenses if e["category"] == category]
    if not expenses:
        print("No expenses found.")
        return
    for e in expenses:
        print(f"{e['id']:>3}  {e['date']}  {e['category']:<12} {e['amount']:>9.2f}  {e['description']}")


def delete_expense(expense_id):
    expenses = load_expenses()
    remaining = [e for e in expenses if e["id"] != expense_id]
    if len(remaining) == len(expenses):
        print("Expense not found.")
        return
    save_expenses(remaining)
    print(f"Deleted expense #{expense_id}")


def summary():
    expenses = load_expenses()
    totals = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
    for cat, total in sorted(totals.items()):
        print(f"{cat:<12} {total:>9.2f}")
    print(f"{'TOTAL':<12} {sum(totals.values()):>9.2f}")


def main():
    parser = argparse.ArgumentParser(description="Simple expense tracker")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="add an expense")
    p_add.add_argument("--amount", type=float, required=True)
    p_add.add_argument("--category", required=True)
    p_add.add_argument("--desc", required=True)
    p_add.add_argument("--date", help="YYYY-MM-DD (default: today)")

    p_list = sub.add_parser("list", help="list expenses")
    p_list.add_argument("--category")

    p_del = sub.add_parser("delete", help="delete an expense by id")
    p_del.add_argument("id", type=int)

    sub.add_parser("summary", help="totals by category")

    args = parser.parse_args()
    if args.command == "add":
        add_expense(args.amount, args.category, args.desc, args.date)
    elif args.command == "list":
        list_expenses(args.category)
    elif args.command == "delete":
        delete_expense(args.id)
    elif args.command == "summary":
        summary()


if __name__ == "__main__":
    main()
