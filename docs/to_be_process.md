# To-Be Process

The proposed process uses Microsoft 365 workflow automation as the coordination layer. Power Automate handles triggers, validation, routing, reminders, and tracker updates. Python or AI-agent modules can then support analysis and reporting.

```mermaid
flowchart TD
  A["New research request submitted via Forms, Teams, or Email"] --> B["Power Automate trigger"]
  B --> C["Validate required fields"]
  C --> D["Create or update task in Excel or SharePoint tracker"]
  D --> E["Assign responsible researcher or agent"]
  E --> F["Route approval request if needed"]
  F --> G["Monitor due date and status"]
  G --> H["Send reminder for open tasks near deadline"]
  H --> I["Run Python or agent analysis module"]
  I --> J["Generate progress report"]
  J --> K["Send Teams or email update"]
  K --> L["Update dashboard and audit log"]
```

## Expected Improvements

- More transparent task ownership
- Faster approval routing
- Better deadline awareness
- Standardized progress reporting
- Clearer integration between agent outputs and project workflow

