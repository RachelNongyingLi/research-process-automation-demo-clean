# Approval Workflow

## Business Rule

Approval is required when a claim affects a report decision, has high impact, has partial evidence, or has unresolved rhetorical/overclaim flags. The approval target is the artifact or claim, not just the task row.

## Flow Logic

```text
Agent output submitted
  -> Extract claim ledger entries
  -> Check evidence_status, phrasing_status, and claim_strength
  -> If risk is high or approval_needed = yes
  -> Send approval request to supervisor or assigned reviewer
  -> Wait for approve / revise / reject / defer
  -> Update review_status and approval_status
  -> Notify task owner with required revision or accepted scope
```

## Example Approval Message

```text
Project: Research Agent Quality Control
Task: Verify formal published evidence for method claims
Claim: Research-agent method claims should be treated as accepted project claims only after formally published evidence has been checked.
Evidence status: partial
Phrasing status: ok
Requested decision: approve with limits, request another source, or defer the claim.
```

