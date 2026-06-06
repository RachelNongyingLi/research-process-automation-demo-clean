# Problem Statement

Agent-assisted research work often fails after the draft is already fluent. The agent produces a polished answer, but the output still misses the research expectation: a claim is too strong, evidence is weak or unpublished, literature search hits are old or unsuitable, the wording hides uncertainty, or the response keeps following the model's preferred style rather than the deliverable needed by the deadline.

The repeated correction loop is the real cost. Each new task requires the same reminders:

- Do not overclaim.
- Use formally published evidence for method claims.
- Do not treat every search result as evidence; check recency, venue status, source quality, and claim relevance.
- Separate observation, inference, recommendation, and limitation.
- Avoid binary contrast rhetoric when a scoped, mechanism-based claim is better.
- Do not let multiple agents simply polish toward the same style.
- Stop open-ended refinement when a smaller deadline-ready deliverable is needed.

## Core Problem

The workflow needs a quality-control layer that can:

- Convert repeated expectations into reusable skills and checklist gates.
- Track material claims before they enter a report.
- Require evidence records for claims that affect decisions.
- Flag weak, unpublished, stale, rejected, unknown, or off-topic support.
- Detect rhetorical patterns that make claims sound stronger than they are.
- Rotate reviewer roles so the drafting agent does not approve itself.
- Preserve deadline state and decide when to ship, revise, defer, or block.

## Target Users

- Research assistants using LLM agents for drafting or synthesis
- Supervisors reviewing agent-assisted research artifacts
- Data science students preparing reports under deadlines
- Teams experimenting with multi-agent research workflows
- Anyone who needs agent outputs to become auditable research deliverables
