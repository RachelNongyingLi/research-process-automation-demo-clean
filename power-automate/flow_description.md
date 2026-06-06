# Power Automate Flow Description

## Trigger

The workflow starts when a new research request is submitted through Microsoft Forms, Teams, or email.

## Main Steps

1. Parse request fields:
   - Project name
   - Task title
   - Owner
   - Due date
   - Approval needed
   - Priority
   - Notes
2. Validate required fields.
3. Create or update a row in the Excel or SharePoint tracker.
4. If approval is needed, start an approval action.
5. Send Teams or email notification to the responsible owner.
6. Add the task to the weekly reporting queue.
7. Log the workflow execution status.

## Output

- Updated task tracker
- Approval status
- Owner notification
- Weekly report input
- Audit log entry

