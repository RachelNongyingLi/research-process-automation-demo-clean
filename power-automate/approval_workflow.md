# Approval Workflow

## Business Rule

If `approval_needed` is `yes`, the task should be routed to the supervisor before analysis or reporting starts.

## Flow Logic

```text
New task created
  -> Check approval_needed
  -> If yes, send approval request
  -> Wait for approval response
  -> Update approval_status
  -> Notify owner
```

## Example Approval Message

```text
Project: Causal Inference Literature Review
Task: Prepare benchmark comparison table
Owner: Research Assistant
Due date: 2026-06-14
Reason for approval: Supervisor confirmation required before reporting benchmark claims.
```

