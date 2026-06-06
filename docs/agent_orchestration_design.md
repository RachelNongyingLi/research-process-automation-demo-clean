# Agent Orchestration Design

This case study treats AI agents as analysis and summarization modules, not as the only process manager.

## Agent Role

The agent can:

- Summarize research task updates
- Extract blockers from notes or messages
- Draft progress summaries
- Suggest next actions
- Convert raw outputs into structured report sections

## Workflow Layer Role

The workflow layer can:

- Trigger when new tasks arrive
- Validate required fields
- Track dates and status
- Route approvals
- Send reminders
- Store task updates in a shared tracker
- Generate auditable logs

## Design Principle

AI agents should support research work, while the workflow layer provides accountability, time awareness, and process continuity.

