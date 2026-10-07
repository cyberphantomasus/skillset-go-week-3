# Week 3 - Task 3.3: Prompt Engineering Portfolio

Skill Set Go EduTech — AI/ML Internship (Offer ID: SSG/AIML/B1/0291)

## Objective
Design and test LLM prompts for reasoning, extraction, summarization and coding, and record each iteration and its outcome (Week 3 Task 3.3).

## Deliverable
`3.3_prompt_evaluation.xlsx` — the prompt evaluation sheet:
- **Summary** — score table, chart and key findings
- **Evaluation Log** — all 12 runs: prompt (verbatim), what changed and why, model output (verbatim), per-check results, score
- **Rubrics** — exactly what each check measures and whether it was automated or manual
- **Test Inputs** — the email, text, question and coding task used, with ground truth

## Design
4 task types x 3 prompt versions (baseline, then two iterations). Every version is scored against a fixed rubric of objective checks, so improvement is measured rather than judged by eye.

| Task type | v1 (baseline) | v2 | v3 |
|---|---|---|---|
| Reasoning (bakery cost puzzle) | 67% | 67% | 100% |
| Extraction (email to JSON) | 0% | 83% | 100% |
| Summarization (city report) | 71% | 86% | 100% |
| Coding (duration parser) | 17% | 50% | 100% |

## Main findings
- The gains came from **stating checkable constraints** (output format, length, error behaviour, deliverables), not from clever wording.
- Reasoning was correct in all three versions; iteration changed how checkable the work was, not accuracy. The problem was too easy to show a benefit from "think step by step".
- "Two sentences" did not limit length (55 words); a word cap plus a required-content list did (36 words, all required points).
- The baseline parser silently returned 0 for `''`, `'abc'`, `'1x'` and 300 for `'-5m'`; naming the error contract fixed it.

## Method and limitations (please read)
- Each prompt was run **once**. The outputs were produced by Claude while this sheet was prepared, in response to each prompt exactly as written, and then scored by script. They are **not** from a blind, independent run, and the rubrics were written alongside the prompts, so baseline results may look better than a cold run would.
- Scoring is automated (JSON parsing, word/sentence counts, keyword checks, executing the generated function on test cases, running the generated pytest file). One summarization check per row ("no invented facts") was done manually.
- One task per category and one run per prompt: this demonstrates the evaluate-and-iterate method, not a benchmark.

## Reproduce the scoring
```bash
pip install pytest
python score.py     # prints the check results for all 12 stored outputs
```

## Files
- `3.3_prompt_evaluation.xlsx` — the evaluation sheet
- `content.py` — test inputs, prompts and the verbatim outputs
- `score.py` — the automated scoring checks
- `generated_code/` — the three code outputs from the coding runs, as runnable files
