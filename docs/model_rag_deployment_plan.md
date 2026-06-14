# Model, RAG, Deployment, and Scalability Plan

This document records what is implemented today, what should not be overclaimed, and what would be required to turn the current quality-gate PoC into a deployed LLM/RAG system.

## Current Status

Implemented:

- CSV ledgers for tasks, agent outputs, claims, evidence, agent roles, and handoffs.
- Python validation over ledger fields, joins, enum values, dates, evidence status, and approval boundaries.
- Python readiness report generation from the ledgers.
- Microsoft 365 workflow architecture notes for intake, approvals, reminders, and reporting.

Not implemented yet:

- Live LLM calls.
- Prompt execution framework.
- Model comparison benchmark.
- Embedding generation.
- Vector index or vector database.
- RAG retriever.
- Cloud model deployment.
- Importable Power Automate flow export.

## Model Evaluation Plan

The model evaluation should answer two interview questions:

- Which LLMs were tested?
- Which model worked best for this project, and by what metric?

Recommended evaluation setup:

| Component | Plan |
| --- | --- |
| Candidate models | Start with one strong hosted model, one cheaper hosted model, and one local/open model if available. |
| Fixed tasks | Use 10-20 representative research-agent tasks: claim extraction, evidence checking, source triage, style review, and weekly summary drafting. |
| Prompt templates | Keep role prompts stable across models. |
| Outputs stored | Save raw model output, parsed structured output, validation result, and human review decision. |
| Metrics | Evidence traceability, unsupported claim rate, citation accuracy, required human edits, latency, and cost. |
| Best-model criterion | Prefer the model with the best review-passing rate under acceptable cost and latency, not simply the most fluent prose. |

Minimum files to add later:

- `prompts/`
- `data/eval_tasks.csv`
- `data/model_eval_results.csv`
- `scripts/run_model_eval.py`
- `docs/model_evaluation.md`

## Hallucination Mitigation Plan

The current PoC already models the controls, but does not yet run them over live model outputs.

Controls:

- Treat model outputs as provisional.
- Register material statements in the claim ledger.
- Require evidence records for decision-impacting claims.
- Separate candidate search hits from accepted evidence.
- Reject stale, unknown, weak, rejected, contradictory, or off-topic sources before they support a claim.
- Route risky phrasing and unsupported certainty to reviewer roles.
- Keep final approval with a human owner.

Next implementation step:

1. Save raw LLM outputs to an output ledger.
2. Extract claims into `data/sample_claim_ledger.csv` format.
3. Attach retrieved or manually verified evidence.
4. Run existing validation and report generation.
5. Compare final report state before and after evidence review.

## Retrieval and RAG Plan

The current repository includes RAG and source-quality concepts, but no actual RAG implementation.

Why retrieval matters:

- The project needs traceable evidence, not just fluent generation.
- Model memory can be stale or unsupported.
- Research claims need source-level review before inclusion in a deliverable.

Baseline methods to compare:

| Method | Why compare it |
| --- | --- |
| Pure prompt / model memory | Fastest baseline, but highest risk of unsupported claims. |
| Manual source search | Strong control baseline, but slow and hard to scale. |
| Keyword search | Simple and explainable, but may miss semantic matches. |
| Agent search with ledger triage | Good for exploration, but needs source-quality controls. |
| RAG with vector retrieval | Better for grounded drafting once indexing and evaluation exist. |

Vector database decision:

- Current demo: no vector database.
- Local PoC option: Chroma or FAISS for quick iteration.
- Azure/M365 production option: Azure AI Search vector index, because it aligns better with enterprise identity, SharePoint content, and Power Automate workflows.
- Managed SaaS option: Pinecone or similar when independent scaling and managed vector operations matter more than M365 integration.

Minimum RAG implementation path:

1. Add a small document corpus under `data/corpus/`.
2. Add a chunking script.
3. Generate embeddings.
4. Build a local vector index.
5. Add a retriever query script.
6. Store retrieved source IDs in the evidence ledger.
7. Evaluate retrieval precision and evidence sufficiency.

## Deployment Plan

Current deployment status:

- Local only.
- Run with `python3 scripts/validate_task_fields.py`.
- Run with `python3 scripts/generate_progress_report.py`.
- Power Automate files are design blueprints, not importable cloud flows.

Target cloud architecture:

| Layer | Target |
| --- | --- |
| Intake | Microsoft Forms, Teams, or email trigger. |
| Workflow state | SharePoint list or Excel table for task and review records. |
| Orchestration | Power Automate for approvals, reminders, escalation, and report distribution. |
| Processing | Python service or scheduled job for validation, aggregation, and model/RAG calls. |
| Model access | Hosted LLM API or Azure OpenAI endpoint. |
| Retrieval | Azure AI Search or local/managed vector DB, depending on environment. |
| Review UI | Power Apps, SharePoint view, Power BI, or a lightweight dashboard. |

Minimum deployable artifacts to add later:

- `requirements.txt` or `pyproject.toml`
- `.env.example`
- service entry point or scheduled-job wrapper
- Dockerfile if containerized
- cloud deployment notes
- Power Automate export or detailed import steps

## Scalability Plan

The current PoC scales conceptually through state separation: agents produce bounded artifacts, but durable state lives in ledgers. Production scalability needs execution infrastructure.

Planned scalability controls:

| Concern | Control |
| --- | --- |
| Many tasks | Queue agent jobs by `task_id` and process independently. |
| Long-running model calls | Use async workers and store `workflow_run_id`. |
| Duplicate work | Cache embeddings, retrieved source sets, and completed gate decisions. |
| Failed calls | Retry with backoff and record failure reason. |
| Human bottlenecks | Escalate stale approvals and summarize review queues. |
| Reporting cost | Generate incremental reports from changed task/claim/evidence records. |
| Auditability | Keep immutable run logs and link each decision to task, claim, evidence, and handoff IDs. |
| Observability | Track latency, cost, failure rate, review-pass rate, and unresolved blocker count. |

Practical next step:

Add CLI parameters and tests to the existing scripts before introducing LLM calls. That keeps the deterministic core stable while the model layer changes.

