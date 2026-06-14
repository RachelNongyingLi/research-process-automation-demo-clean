# Team Contributions

This file separates human team responsibilities from the agent roles in the workflow.

## Current Repository Evidence

The current sample data records `Nongying Li` as the owner for all sample tasks in `data/sample_research_tasks.csv`. The repository does not yet contain evidence for a multi-person human team such as commit ownership, PR reviews, task assignments, or delivery approval records.

Safe interview wording:

> This version is a solo PoC. I handled the problem framing, ledger schema, Python validation/reporting scripts, multi-agent role and handoff design, Power Automate architecture blueprint, and interview-prep documentation. The agent roles in the repo are system roles, not human teammates.

## Human Workstreams

| Workstream | Current owner | Evidence in repo | Notes |
| --- | --- | --- | --- |
| Problem framing | Nongying Li | `docs/problem_statement.md`, `README.md` | Defines research-agent quality-control pain points. |
| Data model | Nongying Li | `data/*.csv`, `README.md` | Defines task, output, claim, evidence, role, and handoff ledgers. |
| Validation logic | Nongying Li | `scripts/validate_task_fields.py` | Checks schema, enum values, dates, joins, evidence state, and role boundaries. |
| Report generation | Nongying Li | `scripts/generate_progress_report.py`, `reports/sample_weekly_report.md` | Produces readiness report from the ledgers. |
| Multi-agent design | Nongying Li | `docs/agent_orchestration_design.md`, `data/sample_agent_roles.csv`, `data/sample_handoff_ledger.csv` | Models agent roles and typed handoffs. |
| M365 workflow design | Nongying Li | `docs/solution_architecture.md`, `power-automate/*.md` | Describes Power Automate, approval, reminder, and reporting architecture. |
| Interview readiness | Nongying Li | `docs/interview_qa_playbook.md`, `docs/model_rag_deployment_plan.md` | Records safe answers, gaps, and next implementation steps. |

## If This Becomes a Team Project

Replace or extend the table below with real names and evidence before using it in an interview.

| Member | Responsibility | Evidence to add |
| --- | --- | --- |
| TBD | LLM integration and prompt runner | PR, script, prompt templates, model output samples. |
| TBD | RAG/vector database implementation | Indexing script, retriever, evaluation results. |
| TBD | Cloud deployment | Docker/service config, deployment notes, endpoint screenshots or logs. |
| TBD | UI/dashboard | Static dashboard, Streamlit app, Power Apps screen, or Power BI report. |
| TBD | QA and evaluation | Tests, review rubric, model evaluation results. |

## Agent Roles Are Not Human Team Members

The project defines these system roles in `data/sample_agent_roles.csv`:

- `orchestrator_agent`
- `skill_agent`
- `draft_agent`
- `literature_agent`
- `evidence_agent`
- `style_reviewer`
- `critic_agent`
- `delivery_agent`
- `human_owner`

These roles describe workflow responsibilities and approval boundaries. They should not be presented as separate people on the project team.

