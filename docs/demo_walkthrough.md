# Demo Walkthrough

This walkthrough shows the current local PoC end to end. It is intentionally small: CSV ledgers act as the system of record, Python validates the quality gates, and a Markdown report exposes what can ship, what is risky, and what needs review.

## What This Demo Proves

- Tasks, agent outputs, claims, evidence, roles, and handoffs are tracked as structured records.
- Drafted claims are not automatically accepted.
- Weak, stale, rejected, unknown, or off-topic sources stay visible in the literature gate.
- Reviewer and delivery handoffs are auditable.
- Deadline and approval risks appear in the generated readiness report.

## What This Demo Does Not Yet Prove

- It does not call a live LLM.
- It does not build embeddings or a vector database.
- It does not run a deployed Power Automate flow.
- It does not compare real model quality.

Those items are next-phase work tracked in `docs/implementation_roadmap_with_papers.md`.

## Quick Start

Run the full local demo:

```bash
python3 scripts/run_demo.py
```

Expected output:

```text
Research-Agent Quality Gate demo
Scope: local CSV ledgers + Python validation/reporting PoC.

== Validate ledgers ==
All task records passed validation.

== Generate readiness report ==
Wrote .../reports/sample_weekly_report.md

== Build static dashboard ==
Wrote .../docs/dashboard.html

Demo complete.
```

Open the generated artifacts:

```text
reports/sample_weekly_report.md
docs/dashboard.html
```

## Run The Steps Separately

Validate the ledger records:

```bash
python3 scripts/validate_task_fields.py
```

Generate the report:

```bash
python3 scripts/generate_progress_report.py
```

Generate a report with custom inputs:

```bash
python3 scripts/generate_progress_report.py \
  --data-dir data \
  --output /tmp/research_agent_report.md \
  --report-date 2026-06-14
```

Build the dashboard separately:

```bash
python3 scripts/build_dashboard.py \
  --data-dir data \
  --output docs/dashboard.html \
  --report-date 2026-06-14
```

## Run Tests

Install the development dependency if needed:

```bash
python3 -m pip install -r requirements.txt
```

Run the tests:

```bash
python3 -m pytest
```

If pytest is not installed, the same tests also run with the Python standard
library:

```bash
python3 -m unittest discover
```

## Interview Demo Script

1. Start with `README.md` and say this is a quality-gate PoC, not a production LLM platform.
2. Run `python3 scripts/run_demo.py`.
3. Open `docs/dashboard.html`.
4. Point to `Approval Queue`: approval-required tasks remain visible.
5. Point to `Claim Gate`: unresolved or risky claims are visible.
6. Point to `Evidence Gate`: broad method claims need stronger evidence before approval.
7. Point to `Literature Gate`: search hits are treated as candidates, not evidence.
8. Point to `Handoff Trail`: role boundaries and handoffs are explicit.
9. Close with `docs/implementation_roadmap_with_papers.md` to explain how you would add real LLM/RAG/cloud deployment next.

## Safe One-Sentence Positioning

This project is a working local PoC for research-agent quality control: it turns provisional agent outputs into auditable claim, evidence, review, handoff, and deadline records before they can become a final research deliverable.
