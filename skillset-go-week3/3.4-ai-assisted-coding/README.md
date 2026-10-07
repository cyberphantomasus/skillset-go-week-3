# Week 3 - Task 3.4: AI-Assisted Coding Task

Skill Set Go EduTech — AI/ML Internship (Offer ID: SSG/AIML/B1/0291)

## Objective
Build a small app with an AI coding assistant; review, correct and audit the generated code (Week 3 Task 3.4).

## The app
A command-line expense tracker (Python standard library only): add, list (optionally by category), delete, and summarize expenses by category, stored in a JSON file.

```bash
cd app
python expense_tracker.py add --amount 12.50 --category food --desc "lunch" --date 2026-10-06
python expense_tracker.py add --amount 3.20 --category transport --desc "bus"
python expense_tracker.py list
python expense_tracker.py list --category food
python expense_tracker.py summary
python expense_tracker.py delete 2
```

Data is saved to `expenses.json` in the current folder (set the `EXPENSES_FILE` environment variable to use another path).

## What is in this folder
| Path | What it is |
|---|---|
| `app/expense_tracker.py` | the corrected, final app |
| `app/expense_tracker_v1_generated.py` | the AI assistant's first version, kept unmodified for the audit trail |
| `tests/test_audit.py` | 17 black-box tests written from 7 stated requirements; run against either version |
| `audit_results_v1.txt` | v1 results: **5 passed, 12 failed** |
| `audit_results_v2.txt` | corrected app results: **17 passed** |
| `AUDIT_NOTES.md` | the audit: how it was done, 9 findings with evidence and fixes, limitations, takeaways |

## Run the tests
```bash
pip install pytest
python -m pytest tests/test_audit.py -v                                             # corrected app
APP_UNDER_TEST=app/expense_tracker_v1_generated.py python -m pytest tests/test_audit.py -v   # v1 (12 failures are expected)
```

## Headline finding
v1 worked on the happy path but, after one delete followed by one add, produced duplicate IDs (`[2, 3, 3]`), and deleting one of them silently removed both expenses. See `AUDIT_NOTES.md` for the full list.

## Tools
Python 3, pytest. Code generated with Claude (AI assistant) and reviewed/corrected as documented.
