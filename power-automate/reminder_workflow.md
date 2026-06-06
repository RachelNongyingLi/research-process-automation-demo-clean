# Reminder Workflow

## Business Rule

If a task is not completed and the due date is within three days, a reminder should be sent to the owner.

## Flow Logic

```text
Daily scheduled trigger
  -> Read open tasks
  -> Check due date
  -> If due date is within 3 days and status is not done
  -> Send Teams or email reminder
  -> Update reminder_count
```

## Example Reminder

```text
Reminder: The task "Validate simulation output table" is due in 2 days.
Current status: in_progress
Owner: Nongying Li
Next action: Upload cleaned output or mark blocker in the tracker.
```

