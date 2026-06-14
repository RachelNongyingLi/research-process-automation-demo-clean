from __future__ import annotations

import argparse
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path


def load_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


DEMO_REPORT_DATE = date(2026, 6, 6)


def default_project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def ledger_paths(data_dir: Path) -> dict[str, Path]:
    return {
        "tasks": data_dir / "sample_research_tasks.csv",
        "agent_outputs": data_dir / "sample_agent_outputs.csv",
        "claims": data_dir / "sample_claim_ledger.csv",
        "evidence": data_dir / "sample_evidence_ledger.csv",
        "agent_roles": data_dir / "sample_agent_roles.csv",
        "handoffs": data_dir / "sample_handoff_ledger.csv",
    }


def build_report(
    rows: list[dict[str, str]],
    agent_outputs: list[dict[str, str]],
    claims: list[dict[str, str]],
    evidence: list[dict[str, str]],
    agent_roles: list[dict[str, str]],
    handoffs: list[dict[str, str]],
    report_date: date = DEMO_REPORT_DATE,
) -> str:
    status_counts = Counter(row["status"] for row in rows)
    owner_counts = Counter(row["owner"] for row in rows)
    approval_tasks = [
        row for row in rows
        if row["approval_needed"].lower() == "yes" and row["approval_status"] != "approved"
    ]
    task_lookup = {row["task_id"]: row for row in rows}
    review_queue = [
        output
        for output in agent_outputs
        if output.get("needs_human_review", "").lower() == "yes"
        and output.get("task_id") in task_lookup
    ]
    claim_lookup = {claim["claim_id"]: claim for claim in claims}
    evidence_by_claim: dict[str, list[dict[str, str]]] = {}
    for record in evidence:
        evidence_by_claim.setdefault(record["claim_id"], []).append(record)
    role_lookup = {role["agent_name"]: role for role in agent_roles}

    unresolved_claims = [
        claim
        for claim in claims
        if claim["review_status"] != "approved"
        or claim["evidence_status"] in {"missing", "partial"}
        or claim["phrasing_status"] != "ok"
    ]
    evidence_risks = [
        claim
        for claim in claims
        if claim["evidence_requirement"] == "formal_publication"
        and claim["evidence_status"] != "verified"
    ]
    literature_risks = [
        record
        for record in evidence
        if record.get("verification_status") != "verified"
        or record.get("source_age_status") in {"dated", "stale", "unknown"}
        or record.get("venue_decision_status") in {
            "preprint_only",
            "rejected",
            "unknown",
        }
        or record.get("source_quality_status") in {"weak", "unusable"}
        or record.get("relevance_status") in {"contradictory", "off_topic"}
    ]
    rhetorical_flags = [
        claim for claim in claims if claim["phrasing_status"] != "ok"
    ]
    upcoming = [
        row for row in rows
        if row["status"] != "done"
        and 0 <= (
            datetime.strptime(row["due_date"], "%Y-%m-%d").date() - report_date
        ).days <= 3
    ]
    open_handoffs = [
        handoff for handoff in handoffs
        if handoff["status"] in {"pending", "needs_revision", "blocked"}
    ]
    delivery_handoffs = [
        handoff for handoff in handoffs
        if handoff["handoff_type"] in {"return_to_manager", "human_approval"}
        or handoff["artifact_type"] in {"gate_summary", "delivery_package"}
    ]

    lines = [
        "# Sample Research-Agent Readiness Report",
        "",
        f"Report date: {report_date.isoformat()}",
        "",
        "## Status Summary",
    ]

    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")

    lines.extend(["", "## Owner Summary"])
    for owner, count in sorted(owner_counts.items()):
        lines.append(f"- {owner}: {count} task(s)")

    lines.extend(["", "## Approval Queue"])
    if approval_tasks:
        for row in approval_tasks:
            lines.append(
                f"- {row['task_id']} | {row['project_name']} | {row['task_title']} | "
                f"approval status: {row['approval_status']}"
            )
    else:
        lines.append("- No pending approvals.")

    lines.extend(["", "## Deadline Reminders"])
    if upcoming:
        for row in upcoming:
            lines.append(
                f"- {row['task_id']} | {row['task_title']} | due {row['due_date']} | "
                f"status: {row['status']}"
            )
    else:
        lines.append("- No open tasks due within three days.")

    lines.extend(["", "## Claim Quality Gate"])
    if unresolved_claims:
        for claim in unresolved_claims:
            evidence_count = len(evidence_by_claim.get(claim["claim_id"], []))
            lines.append(
                f"- {claim['claim_id']} | task {claim['task_id']} | "
                f"review: {claim['review_status']} | evidence: {claim['evidence_status']} | "
                f"phrasing: {claim['phrasing_status']} | sources: {evidence_count}"
            )
            if claim.get("issue", "").strip():
                lines.append(f"  - action: {claim['issue']}")
    else:
        lines.append("- All tracked claims are approved.")

    lines.extend(["", "## Evidence Gate"])
    if evidence_risks:
        for claim in evidence_risks:
            evidence_records = evidence_by_claim.get(claim["claim_id"], [])
            source_labels = [
                f"{record['venue']} {record['year']}" for record in evidence_records
            ]
            sources = ", ".join(source_labels) if source_labels else "no formal source"
            lines.append(
                f"- {claim['claim_id']} | {claim['claim_strength']} claim | "
                f"{claim['evidence_status']} | {sources}"
            )
    else:
        lines.append("- No formal-publication evidence risks.")

    lines.extend(["", "## Literature Quality Gate"])
    if literature_risks:
        for record in literature_risks:
            lines.append(
                f"- {record['evidence_id']} -> {record['claim_id']} | "
                f"{record['title']} | year: {record['year']} | "
                f"venue: {record['venue_decision_status']} | "
                f"age: {record['source_age_status']} | "
                f"quality: {record['source_quality_status']} | "
                f"relevance: {record['relevance_status']} | "
                f"verification: {record['verification_status']}"
            )
    else:
        lines.append("- No stale, rejected, weak, or off-topic literature candidates.")

    lines.extend(["", "## Rhetorical Rewrite Queue"])
    if rhetorical_flags:
        for claim in rhetorical_flags:
            lines.append(f"- {claim['claim_id']}: {claim['claim_text']}")
            lines.append(
                "  - rewrite target: qualify the contrast through mechanism, scope, "
                "and evidence instead of using a not-A-but-B frame."
            )
    else:
        lines.append("- No rhetorical pattern flags.")

    lines.extend(["", "## Deadline Delivery Risks"])
    if upcoming:
        for row in upcoming:
            task_claims = [
                claim for claim in unresolved_claims if claim["task_id"] == row["task_id"]
            ]
            if task_claims:
                claim_ids = ", ".join(claim["claim_id"] for claim in task_claims)
                lines.append(
                    f"- {row['task_id']} | due {row['due_date']} | unresolved claims: "
                    f"{claim_ids} | blocker: {row.get('blocker', '') or 'none'}"
                )
    else:
        lines.append("- No deadline delivery risks.")

    lines.extend(["", "## Agent Review Queue"])
    if review_queue:
        for output in review_queue:
            task = task_lookup[output["task_id"]]
            lines.append(
                f"- {output['task_id']} | {task['project_name']} | "
                f"{output['agent_name']} produced {output['output_type']}: "
                f"{output['summary']}"
            )
    else:
        lines.append("- No agent outputs waiting for human review.")

    lines.extend(["", "## Multi-Agent Delivery Gate"])
    lines.append(
        "- Relationship model: orchestrator owns workflow state; worker and reviewer "
        "agents produce bounded artifacts; human owner controls final approval."
    )
    if open_handoffs:
        for handoff in open_handoffs:
            lines.append(
                f"- {handoff['handoff_id']} | task {handoff['task_id']} | "
                f"{handoff['from_agent']} -> {handoff['to_agent']} | "
                f"{handoff['handoff_type']} | status: {handoff['status']} | "
                f"impact: {handoff['delivery_impact']}"
            )
    else:
        lines.append("- No open handoff issues.")

    lines.extend(["", "## Agent Role Boundaries"])
    for role in agent_roles:
        lines.append(
            f"- {role['agent_name']} | {role['role_type']} | "
            f"delegates: {role['can_delegate']} | "
            f"self-approval: {role['can_approve_own_output']} | "
            f"output: {role['required_output']} | "
            f"approval boundary: {role['approval_boundary']}"
        )

    lines.extend(["", "## Delivery Handoff Trail"])
    if delivery_handoffs:
        for handoff in delivery_handoffs:
            receiver = role_lookup.get(handoff["to_agent"], {})
            receiver_role = receiver.get("role_type", "unknown_role")
            lines.append(
                f"- {handoff['handoff_id']} | {handoff['artifact_type']} | "
                f"{handoff['from_agent']} -> {handoff['to_agent']} "
                f"({receiver_role}) | status: {handoff['status']}"
            )
    else:
        lines.append("- No delivery handoffs recorded.")

    lines.extend(["", "## Blockers"])
    blockers = [row for row in rows if row.get("blocker", "").strip()]
    if blockers:
        for row in blockers:
            lines.append(f"- {row['task_id']}: {row['blocker']}")
    else:
        lines.append("- No blockers recorded.")

    lines.extend(["", "## Evidence Ledger"])
    for record in evidence:
        claim = claim_lookup.get(record["claim_id"])
        if claim is None:
            continue
        lines.append(
            f"- {record['evidence_id']} -> {record['claim_id']} | "
            f"{record['title']} | {record['venue']} {record['year']} | "
            f"{record['verification_status']} | "
            f"{record.get('source_quality_status', 'quality_unknown')} | "
            f"{record.get('relevance_status', 'relevance_unknown')}"
        )

    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a readiness report from quality-gate CSV ledgers."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=default_project_root() / "data",
        help="Directory containing the sample_* ledger CSV files.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=default_project_root() / "reports" / "sample_weekly_report.md",
        help="Markdown report path to write.",
    )
    parser.add_argument(
        "--report-date",
        type=lambda value: datetime.strptime(value, "%Y-%m-%d").date(),
        default=DEMO_REPORT_DATE,
        help="Report date in YYYY-MM-DD format.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = ledger_paths(args.data_dir)
    rows = load_rows(paths["tasks"])
    agent_outputs = load_rows(paths["agent_outputs"])
    claims = load_rows(paths["claims"])
    evidence = load_rows(paths["evidence"])
    agent_roles = load_rows(paths["agent_roles"])
    handoffs = load_rows(paths["handoffs"])
    report = build_report(
        rows,
        agent_outputs,
        claims,
        evidence,
        agent_roles,
        handoffs,
        args.report_date,
    )
    output_path = args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
