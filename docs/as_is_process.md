# As-Is Process

The current process depends on repeated prompting and ad hoc review. Agents can draft quickly, but the review criteria live in the user's memory rather than in the workflow.

```mermaid
flowchart TD
  A["Research task or writing request"] --> B["Agent drafts fluent output"]
  B --> C["User notices expectation mismatch"]
  C --> D["Prompt again: do not overclaim"]
  D --> E["Prompt again: find formal published evidence"]
  E --> F["User manually filters old, rejected, or weakly related search hits"]
  F --> G["Prompt again: avoid weak binary contrast wording"]
  G --> H["Another agent reviews with similar model taste"]
  H --> I["Agent-to-agent ownership remains unclear"]
  I --> J["Draft becomes more polished but not necessarily more acceptable"]
  J --> K["Deadline approaches"]
  K --> L["User manually decides what can be shipped, revised, or blocked"]
```

## Pain Points

- The agent treats fluency as a proxy for readiness.
- Evidence quality is not tracked claim by claim.
- Search results are not separated from accepted evidence.
- Old, unaccepted, rejected, unknown, or off-topic literature can slip into a draft.
- Repeated writing rules are retyped instead of encoded as skills.
- Multi-agent review can converge on the same aesthetic rather than independent critique.
- Agent handoffs happen inside conversation context rather than an auditable workflow record.
- Deadline pressure is invisible to the agent unless restated in the prompt.
- The final artifact may be large and polished but still unsuitable for the actual research decision.
