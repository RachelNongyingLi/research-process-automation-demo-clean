# Sample Research-Agent Readiness Report

Report date: 2026-06-06

## Status Summary
- in_progress: 4
- not_started: 2

## Owner Summary
- Nongying Li: 6 task(s)

## Approval Queue
- T002 | Research Agent Quality Control | Verify formal published evidence for method claims | approval status: pending
- T003 | Research Agent Quality Control | Rewrite binary contrast claims into qualified research claims | approval status: pending
- T006 | Research Agent Quality Control | Triage literature search hits by recency venue decision quality and relevance | approval status: pending

## Deadline Reminders
- T001 | Define reusable skill checklist for claim discipline | due 2026-06-09 | status: in_progress
- T002 | Verify formal published evidence for method claims | due 2026-06-08 | status: in_progress
- T003 | Rewrite binary contrast claims into qualified research claims | due 2026-06-09 | status: in_progress

## Claim Quality Gate
- C002 | task T002 | review: pending | evidence: partial | phrasing: ok | sources: 2
  - action: Needs a second source if generalized beyond this demo.
- C003 | task T003 | review: needs_rewrite | evidence: not_required | phrasing: binary_contrast | sources: 0
  - action: Avoid not-A-but-B framing; rewrite as a qualified contrast.
- C004 | task T004 | review: pending | evidence: partial | phrasing: ok | sources: 2
  - action: Current evidence supports agent difficulty and feedback loops, but the model-aesthetic drift claim should stay cautious.
- C005 | task T005 | review: pending | evidence: internal | phrasing: ok | sources: 1
  - action: Supported as a project design claim, not as a general empirical claim.

## Evidence Gate
- C002 | moderate claim | partial | NeurIPS 2020, EMNLP 2023
- C004 | moderate claim | partial | ICLR 2024, NeurIPS 2023

## Literature Quality Gate
- S001 -> C006 | Unverified old search hit returned by an agent literature search | year: 2017 | venue: unknown | age: stale | quality: unusable | relevance: off_topic | verification: rejected

## Rhetorical Rewrite Queue
- C003: This project is not a chatbot but a workflow control plane.
  - rewrite target: qualify the contrast through mechanism, scope, and evidence instead of using a not-A-but-B frame.

## Deadline Delivery Risks
- T002 | due 2026-06-08 | unresolved claims: C002 | blocker: Need one more peer-reviewed source for broad method claim
- T003 | due 2026-06-09 | unresolved claims: C003 | blocker: Contains not-A-but-B style phrasing

## Agent Review Queue
- T001 | Research Agent Quality Control | skill_agent produced skill_checklist: Converted repeated writing expectations into reusable checks for claim strength, evidence type, and phrasing.
- T002 | Research Agent Quality Control | evidence_agent produced source_audit: Found formal venues for ReAct, Toolformer, RAG, Reflexion, Self-Refine, SelfCheckGPT, and AgentBench.
- T003 | Research Agent Quality Control | style_reviewer produced rhetorical_rewrite: Flagged binary contrast phrasing and proposed a qualified alternative based on mechanism and evidence.
- T004 | Research Agent Quality Control | critic_agent produced review_rotation: Separated generator, evidence reviewer, style reviewer, and delivery reviewer roles to reduce one-model taste convergence.
- T005 | Research Agent Quality Control | delivery_agent produced timebox_plan: Converted open-ended improvement into deadline-aware acceptance criteria and a shippable report state.
- T006 | Research Agent Quality Control | literature_agent produced source_triage: Separated candidate search hits from accepted evidence by checking recency, venue decision status, source quality, and claim relevance.

## Blockers
- T002: Need one more peer-reviewed source for broad method claim
- T003: Contains not-A-but-B style phrasing
- T006: Some agent-discovered sources are old unaccepted or only weakly relevant

## Evidence Ledger
- P001 -> C001 | ReAct: Synergizing Reasoning and Acting in Language Models | ICLR 2023 | verified | strong | direct
- P002 -> C001 | Toolformer: Language Models Can Teach Themselves to Use Tools | NeurIPS 2023 | verified | strong | direct
- P003 -> C002 | Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks | NeurIPS 2020 | verified | usable_with_limits | background
- P004 -> C002 | SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models | EMNLP 2023 | verified | strong | indirect
- P005 -> C004 | AgentBench: Evaluating LLMs as Agents | ICLR 2024 | verified | strong | indirect
- P006 -> C004 | Reflexion: Language Agents with Verbal Reinforcement Learning | NeurIPS 2023 | verified | usable_with_limits | background
- P007 -> C005 | Self-Refine: Iterative Refinement with Self-Feedback | NeurIPS 2023 | verified | usable_with_limits | background
- P008 -> C006 | Do Language Models Know When They're Hallucinating References? | Findings of EACL 2024 | verified | strong | direct
- P009 -> C006 | Synthesizing scientific literature with retrieval-augmented language models | Nature 2026 | verified | strong | direct
- S001 -> C006 | Unverified old search hit returned by an agent literature search | Search log 2017 | rejected | unusable | off_topic
