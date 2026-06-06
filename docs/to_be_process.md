# To-Be Process

The proposed process wraps agent outputs in a quality-control workflow. The agent still drafts and analyzes, but the workflow decides whether the output is accepted, revised, partially delivered, or blocked.

```mermaid
flowchart TD
  A["Research task intake"] --> B["Select reusable skill checklist"]
  B --> C["Agent draft or analysis"]
  C --> D["Extract material claims"]
  D --> E["Claim ledger"]
  E --> F["Literature quality gate"]
  F --> G["Formal evidence gate"]
  G --> H["Rhetorical rule checker"]
  H --> I["Rotating reviewer critique"]
  I --> J["Deadline readiness check"]
  J --> K["Accepted deliverable"]
  J --> L["Needs revision"]
  J --> M["Partial delivery with visible limits"]
  J --> N["Blocked by missing evidence or review"]
```

## Expected Improvements

- Repeated research expectations become explicit skill gates.
- Claims are reviewed before entering final reports.
- Evidence quality is visible rather than implied by fluent prose.
- Literature candidates are checked for recency, venue decision, source quality, and claim relevance before supporting a claim.
- Weak rhetorical patterns are flagged and rewritten with scope and mechanism.
- Reviewer roles are separated to reduce single-agent aesthetic drift.
- Deadline state determines when to stop iterating and package a useful artifact.
