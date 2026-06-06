# Power Automate Flow Description

This flow is a Microsoft 365-oriented blueprint for routing research-agent artifacts through quality gates. The local Python demo implements the same logic with CSV files.

## Trigger

The workflow starts when a new research task, agent output, or report draft is submitted through Microsoft Forms, Teams, email, or a tracker update.

## Main Steps

1. Parse request fields:
   - Project name
   - Task title
   - Owner
   - Due date
   - Artifact type
   - Review required
   - Notes
2. Create or update the task tracker.
3. Select the relevant skill checklist.
4. Register material claims in the claim ledger.
5. Attach evidence records or mark evidence as missing.
6. Route claims with partial or missing evidence to the evidence reviewer.
7. Route binary contrast, overclaim, or vague certainty flags to the style reviewer.
8. Route high-risk or approval-required claims to the supervisor.
9. Send deadline reminders when unresolved quality gates are close to due date.
10. Generate a readiness report showing accepted, revised, deferred, and blocked items.

## Output

- Updated task tracker
- Claim ledger entries
- Evidence ledger entries
- Style and overclaim flags
- Reviewer decisions
- Deadline readiness status
- Readiness report input
- Audit log entry

