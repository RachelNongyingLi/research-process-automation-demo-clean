# Interface Blueprint

This workflow needs an interface because the target user should not have to run scripts or inspect CSV files to understand project state. The interface should expose the workflow decisions: what was drafted, what was checked, what failed, who needs to approve it, and what can still ship by the deadline.

## MVP Screen

```mermaid
flowchart LR
  A["Task Intake<br/>owner, deadline, output type"] --> B["Gate Dashboard<br/>claim / literature / evidence / style / deadline"]
  B --> C["Literature Triage Queue<br/>stale, unknown, rejected, weak, off-topic"]
  B --> D["Approval Panel<br/>accept, revise, downgrade, block"]
  D --> E["Weekly Report<br/>ready, risky, blocked, deferred"]

  classDef intake fill:#dbeafe,stroke:#2563eb,color:#0f172a,stroke-width:2px;
  classDef gate fill:#fed7aa,stroke:#ea580c,color:#111827,stroke-width:2px;
  classDef risk fill:#fee2e2,stroke:#dc2626,color:#111827,stroke-width:2px;
  classDef approval fill:#dcfce7,stroke:#16a34a,color:#111827,stroke-width:2px;
  classDef report fill:#fef9c3,stroke:#ca8a04,color:#111827,stroke-width:2px;

  class A intake;
  class B gate;
  class C risk;
  class D approval;
  class E report;
```

## Panels

| Panel | User question | Data source |
| --- | --- | --- |
| Task Intake | What needs to be produced, by whom, and by when? | `data/sample_research_tasks.csv` |
| Agent Output Review | What did the agent produce, and does it need human review? | `data/sample_agent_outputs.csv` |
| Claim Gate | Which claims are approved, provisional, blocked, or too strong? | `data/sample_claim_ledger.csv` |
| Literature Triage | Which search hits are stale, unaccepted, rejected, weak, or off-topic? | `data/sample_evidence_ledger.csv` |
| Approval Panel | What decision should the human owner make now? | task + claim + evidence ledgers |
| Weekly Report | What can ship, what is risky, and what is deferred? | `reports/sample_weekly_report.md` |

## M365 Version

For a Bosch-style Microsoft 365 workflow, the interface can be:

- SharePoint or Excel table as the structured task/evidence store.
- Power Apps form for task intake and approval decisions.
- Power Automate flow for reminders, approvals, escalations, and report generation.
- Power BI dashboard for status, blockers, and source-quality risk.

## GitHub Demo Version

For this repository, the same interface can start smaller:

- Static HTML dashboard for visual walkthrough.
- Streamlit app for interactive filtering.
- CLI report for reproducible audit output.

The important point is that the interface should not hide the gates. It should make the gates visible.
