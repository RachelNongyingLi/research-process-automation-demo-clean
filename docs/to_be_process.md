# To-Be Process

The proposed process wraps agent outputs in a quality-control workflow. The agent still drafts and analyzes, but the workflow decides whether the output is accepted, revised, partially delivered, or blocked.

```mermaid
flowchart TD
  A["Research task intake"] --> B["Select reusable skill checklist"]
  B --> C["Agent draft or analysis"]
  C --> D["Extract material claims"]
  D --> E["Claim ledger"]
  E --> F["Formal evidence gate"]
  F --> G["Rhetorical rule checker"]
  G --> H["Rotating reviewer critique"]
  H --> I["Deadline readiness check"]
  I --> J["Accepted deliverable"]
  I --> K["Needs revision"]
  I --> L["Partial delivery with visible limits"]
  I --> M["Blocked by missing evidence or review"]
```

## Expected Improvements

- Repeated research expectations become explicit skill gates.
- Claims are reviewed before entering final reports.
- Evidence quality is visible rather than implied by fluent prose.
- Weak rhetorical patterns are flagged and rewritten with scope and mechanism.
- Reviewer roles are separated to reduce single-agent aesthetic drift.
- Deadline state determines when to stop iterating and package a useful artifact.

