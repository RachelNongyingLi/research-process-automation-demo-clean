# Reminder Workflow

## Business Rule

Reminders should be triggered by unresolved quality gates near a deadline, not only by open task status.

## Flow Logic

```text
Daily scheduled trigger
  -> Read open tasks, claim ledger, and evidence ledger
  -> Find tasks due within 3 days
  -> Check unresolved evidence, phrasing, approval, and review states
  -> Route reminder to the responsible reviewer
  -> If deadline is close and evidence is missing, mark partial or blocked
  -> Update reminder_count and readiness status
```

## Example Reminder

```text
Quality gate reminder: T003 is due in 2 days.
Issue: Claim C003 uses binary contrast phrasing.
Required action: Rewrite into a scoped, mechanism-based claim before it can enter the final report.
Current delivery state: needs_revision
```

