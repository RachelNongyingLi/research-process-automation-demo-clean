# As-Is Process

The current process depends on repeated prompting and ad hoc review. Agents can draft quickly, but the review criteria live in the user's memory rather than in the workflow.

```mermaid
flowchart TD
  A["Research task or writing request"] --> B["Agent drafts fluent output"]
  B --> C["User notices expectation mismatch"]
  C --> D["Prompt again: do not overclaim"]
  D --> E["Prompt again: find formal published evidence"]
  E --> F["Prompt again: avoid weak binary contrast wording"]
  F --> G["Another agent reviews with similar model taste"]
  G --> H["Draft becomes more polished but not necessarily more acceptable"]
  H --> I["Deadline approaches"]
  I --> J["User manually decides what can be shipped, revised, or blocked"]
```

## Pain Points

- The agent treats fluency as a proxy for readiness.
- Evidence quality is not tracked claim by claim.
- Repeated writing rules are retyped instead of encoded as skills.
- Multi-agent review can converge on the same aesthetic rather than independent critique.
- Deadline pressure is invisible to the agent unless restated in the prompt.
- The final artifact may be large and polished but still unsuitable for the actual research decision.

