# To-Be Process

The proposed process wraps agent outputs in a quality-control workflow. The agent still drafts and analyzes, but the workflow decides whether the output is accepted, revised, partially delivered, or blocked.

```mermaid
flowchart TD
  A["Research task intake"] --> B["Select reusable skill checklist"]
  B --> C["Assign responsible agent role"]
  C --> D["Record typed handoff"]
  D --> E["Agent draft or analysis"]
  E --> F["Extract material claims"]
  F --> G["Claim ledger"]
  G --> H["Literature quality gate"]
  H --> I["Formal evidence gate"]
  I --> J["Rhetorical rule checker"]
  J --> K["Independent reviewer critique"]
  K --> L["Deadline readiness check"]
  L --> M["Human approval boundary"]
  M --> N["Accepted deliverable"]
  M --> O["Needs revision"]
  M --> P["Partial delivery with visible limits"]
  M --> Q["Blocked by missing evidence or review"]
```

## Expected Improvements

- Repeated research expectations become explicit skill gates.
- Claims are reviewed before entering final reports.
- Evidence quality is visible rather than implied by fluent prose.
- Literature candidates are checked for recency, venue decision, source quality, and claim relevance before supporting a claim.
- Agent-to-agent handoffs expose sender, receiver, artifact, precondition, acceptance check, and delivery impact.
- Weak rhetorical patterns are flagged and rewritten with scope and mechanism.
- Reviewer roles are separated to reduce single-agent aesthetic drift.
- Deadline state determines when to stop iterating and package a useful artifact.
