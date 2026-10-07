# Audit Notes - AI-Assisted Coding Task (3.4)

Skill Set Go EduTech - AI/ML Internship, Week 3 (Offer ID: SSG/AIML/B1/0291)

## How the app was made
- **Tool:** Claude (AI assistant).
- **Prompt:** "Build a small command-line expense tracker in Python: add, list, delete, and summarize expenses by category, stored in a JSON file."
- **v1** (`app/expense_tracker_v1_generated.py`) is the assistant's first answer, kept unmodified. It was produced in one pass and was **not run before review**.
- **Audit method:** (1) read v1 line by line; (2) wrote seven requirements (R1-R7, listed in `tests/test_audit.py`) after reading v1 and before running any tests; (3) turned them into 17 black-box tests that run the CLI in a fresh folder; (4) reviewed the code for risks that tests cannot easily show; (5) fixed the code and re-ran the same tests.
- **Result:** v1 passed **5 of 17** tests; the corrected app passes **17 of 17** (`audit_results_v1.txt`, `audit_results_v2.txt`).

## Findings

| # | Severity | Finding | Evidence | Fix in corrected app |
|---|---|---|---|---|
| F1 | High | Duplicate IDs. New ID is `len(expenses) + 1`, so it collides after any delete. Deleting that ID then removes **every** expense carrying it (silent data loss). | Add 3, delete #1, add one more: IDs were `[2, 3, 3]`. `delete 3` then removed both entries. Test: `test_ids_unique_after_delete`. | `max(existing ids) + 1` |
| F2 | High | No amount validation: negative, zero, more than 2 decimals, `nan` and `inf` are all accepted. `nan` is written to the file as `NaN`, which is not valid standard JSON. | 5 parametrized tests failed (`-5`, `0`, `1.239`, `nan`, `inf`); file contained `"amount":NaN`. | `parse_amount()`: finite, > 0, <= 1,000,000,000, at most 2 decimals; `allow_nan=False` when saving |
| F3 | Medium | Dates are not validated; `--date yesterday` and `2026-13-45` are stored as-is. | 2 tests failed. | `parse_date()` using strict `YYYY-MM-DD` |
| F4 | Medium | A corrupted data file produces a raw Python traceback. (The file itself was left untouched, which is good.) | `test_corrupted_file_gives_clean_error` failed. | Clean one-line error, exit status 1, file not modified; also checks the file has the expected structure |
| F5 | Medium | Categories are case-sensitive, so "Food" and "food" are summarized on separate lines. | `test_category_case_insensitive_summary` failed. | Categories are stripped and lower-cased |
| F6 | Low | Deleting a non-existent ID prints "not found" but exits with status 0, so scripts cannot detect the failure. | `test_delete_missing_id_fails` failed. | Error message on stderr, exit status 1 |
| F7 | Low | Empty or whitespace-only descriptions are accepted. | `test_blank_description_rejected` failed. | Stripped and validated (1-200 characters) |
| F8 | Medium | **Found by code review, not demonstrated by a test.** `save_expenses` opens the file with mode `"w"`, which truncates it before writing. If the process dies mid-write, all data is lost. | Code reading only. | Write to a temp file in the same folder, `fsync`, then `os.replace`. A normal run leaves no temp files behind; the crash case itself was not simulated. |
| F9 | Low | **Found by code review, latent.** Money is stored as floating-point numbers. | No test failed: sums such as 10.10 + 20.20 still displayed correctly at 2 decimals. It is a rounding risk, not an observed bug. | `Decimal` arithmetic; amounts stored in the file as strings (e.g. `"12.50"`) |

## What held up in v1
- Overall structure and the `argparse` sub-command design.
- The happy path for add / list / summary, and filtering by category.
- Non-numeric amounts (`abc`) are rejected cleanly by `argparse`.
- A failed load never overwrote a corrupted file (the crash happened before any write).

## Known limitations (not fixed)
- **No file locking.** Atomic writes prevent half-written files, but two simultaneous runs can still overwrite each other's changes.
- **IDs are unique among stored expenses only.** If the highest ID is deleted, the next add reuses that number.
- The 1,000,000,000 amount cap and the 30/200 character limits are arbitrary choices.
- No edit command, no currency handling, and the whole file is loaded into memory (fine for personal use).
- The tests were written by the same assistant that wrote the code. They check the stated requirements, but an independent reviewer could find cases they miss.

## Takeaways on working with an AI coding assistant
1. The generated code looked correct on the happy path, yet failed 12 of 17 requirement checks. Passing a quick manual run says very little.
2. State requirements in the prompt (validation rules, error behaviour, tests); everything missing from the prompt was missing from v1.
3. Write the requirements as tests first, then run them, so the review does not depend on how convincing the code looks.
