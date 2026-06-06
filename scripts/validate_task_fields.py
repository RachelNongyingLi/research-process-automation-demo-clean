from __future__ import annotations

import csv
import re
from datetime import datetime
from pathlib import Path


REQUIRED_FIELDS = [
    "task_id",
    "project_name",
    "task_title",
    "owner",
    "due_date",
    "status",
    "approval_needed",
]

REQUIRED_AGENT_FIELDS = [
    "task_id",
    "agent_name",
    "output_type",
    "summary",
    "needs_human_review",
]

REQUIRED_CLAIM_FIELDS = [
    "claim_id",
    "task_id",
    "claim_text",
    "claim_strength",
    "evidence_requirement",
    "evidence_status",
    "publication_status",
    "phrasing_status",
    "review_status",
]

REQUIRED_EVIDENCE_FIELDS = [
    "evidence_id",
    "claim_id",
    "title",
    "venue",
    "year",
    "publication_type",
    "source_location",
    "usage_role",
    "verification_status",
    "source_age_status",
    "venue_decision_status",
    "source_quality_status",
    "relevance_status",
]

REQUIRED_AGENT_ROLE_FIELDS = [
    "agent_name",
    "role_type",
    "primary_responsibility",
    "can_delegate",
    "can_approve_own_output",
    "required_input",
    "required_output",
    "approval_boundary",
]

REQUIRED_HANDOFF_FIELDS = [
    "handoff_id",
    "task_id",
    "from_agent",
    "to_agent",
    "handoff_type",
    "artifact_id",
    "artifact_type",
    "precondition",
    "acceptance_check",
    "status",
    "delivery_impact",
]

VALID_STATUSES = {"not_started", "in_progress", "blocked", "done"}
VALID_APPROVAL_FLAGS = {"yes", "no"}
VALID_APPROVAL_STATUSES = {"not_required", "pending", "approved", "rejected"}
VALID_PRIORITIES = {"low", "medium", "high"}
VALID_CLAIM_STRENGTHS = {"low", "moderate", "strong"}
VALID_EVIDENCE_REQUIREMENTS = {"none", "project_evidence", "formal_publication"}
VALID_EVIDENCE_STATUSES = {"not_required", "internal", "missing", "partial", "verified"}
VALID_PUBLICATION_STATUSES = {"not_required", "unknown", "peer_reviewed"}
VALID_PHRASING_STATUSES = {"ok", "binary_contrast", "needs_qualification"}
VALID_REVIEW_STATUSES = {"pending", "approved", "needs_rewrite", "blocked"}
VALID_PUBLICATION_TYPES = {
    "conference",
    "journal",
    "workshop",
    "book",
    "official_document",
    "preprint",
    "search_result",
    "internal_log",
}
VALID_VERIFICATION_STATUSES = {"pending", "verified", "rejected"}
VALID_SOURCE_AGE_STATUSES = {"current", "foundational", "dated", "stale", "unknown"}
VALID_VENUE_DECISION_STATUSES = {
    "accepted",
    "preprint_only",
    "rejected",
    "unknown",
    "official",
    "internal",
}
VALID_SOURCE_QUALITY_STATUSES = {
    "strong",
    "usable_with_limits",
    "weak",
    "unusable",
}
VALID_RELEVANCE_STATUSES = {
    "direct",
    "indirect",
    "background",
    "contradictory",
    "off_topic",
}
VALID_ROLE_TYPES = {
    "orchestrator",
    "worker",
    "reviewer",
    "delivery_owner",
    "approver",
}
VALID_HANDOFF_TYPES = {
    "manager_call",
    "sequential",
    "peer_review",
    "return_to_manager",
    "human_approval",
}
VALID_HANDOFF_STATUSES = {
    "accepted",
    "pending",
    "needs_revision",
    "blocked",
    "rejected",
}

BINARY_CONTRAST_PATTERNS = [
    re.compile(r"\bnot\b.{0,80}\bbut\b", re.IGNORECASE),
    re.compile(r"\brather than\b", re.IGNORECASE),
]


def load_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def is_iso_date(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def has_binary_contrast(text: str) -> bool:
    if "不是" in text and "而是" in text:
        return True
    return any(pattern.search(text) for pattern in BINARY_CONTRAST_PATTERNS)


def validate_tasks(
    task_csv_path: Path,
    agent_csv_path: Path | None = None,
    claim_csv_path: Path | None = None,
    evidence_csv_path: Path | None = None,
    agent_roles_csv_path: Path | None = None,
    handoff_csv_path: Path | None = None,
) -> list[str]:
    issues: list[str] = []
    rows = load_rows(task_csv_path)
    seen_task_ids: set[str] = set()

    for row_number, row in enumerate(rows, start=2):
        for field in REQUIRED_FIELDS:
            if not row.get(field, "").strip():
                issues.append(f"Row {row_number}: missing required field '{field}'")

        task_id = row.get("task_id", "").strip()
        if task_id in seen_task_ids:
            issues.append(f"Row {row_number}: duplicate task_id '{task_id}'")
        seen_task_ids.add(task_id)

        due_date = row.get("due_date", "").strip()
        if due_date and not is_iso_date(due_date):
            issues.append(f"Row {row_number}: due_date must use YYYY-MM-DD format")

        status = row.get("status", "").strip().lower()
        if status and status not in VALID_STATUSES:
            issues.append(f"Row {row_number}: unknown status '{status}'")

        approval_needed = row.get("approval_needed", "").strip().lower()
        if approval_needed and approval_needed not in VALID_APPROVAL_FLAGS:
            issues.append(f"Row {row_number}: approval_needed must be yes or no")

        approval_status = row.get("approval_status", "").strip().lower()
        if approval_status and approval_status not in VALID_APPROVAL_STATUSES:
            issues.append(f"Row {row_number}: unknown approval_status '{approval_status}'")

        if approval_needed == "yes" and approval_status in {"", "not_required"}:
            issues.append(
                f"Row {row_number}: approval is needed but approval_status is not set"
            )

        priority = row.get("priority", "").strip().lower()
        if priority and priority not in VALID_PRIORITIES:
            issues.append(f"Row {row_number}: unknown priority '{priority}'")

    agent_output_names: list[tuple[int, str]] = []
    if agent_csv_path is not None:
        agent_rows = load_rows(agent_csv_path)
        for row_number, row in enumerate(agent_rows, start=2):
            for field in REQUIRED_AGENT_FIELDS:
                if not row.get(field, "").strip():
                    issues.append(
                        f"Agent row {row_number}: missing required field '{field}'"
                    )

            task_id = row.get("task_id", "").strip()
            if task_id and task_id not in seen_task_ids:
                issues.append(
                    f"Agent row {row_number}: task_id '{task_id}' is not in task tracker"
                )

            agent_name = row.get("agent_name", "").strip()
            if agent_name:
                agent_output_names.append((row_number, agent_name))

            needs_review = row.get("needs_human_review", "").strip().lower()
            if needs_review and needs_review not in VALID_APPROVAL_FLAGS:
                issues.append(
                    f"Agent row {row_number}: needs_human_review must be yes or no"
                )

    agent_registry: dict[str, dict[str, str]] = {}
    if agent_roles_csv_path is not None:
        agent_role_rows = load_rows(agent_roles_csv_path)
        for row_number, row in enumerate(agent_role_rows, start=2):
            for field in REQUIRED_AGENT_ROLE_FIELDS:
                if not row.get(field, "").strip():
                    issues.append(
                        f"Agent role row {row_number}: missing required field '{field}'"
                    )

            agent_name = row.get("agent_name", "").strip()
            if agent_name in agent_registry:
                issues.append(
                    f"Agent role row {row_number}: duplicate agent_name '{agent_name}'"
                )
            agent_registry[agent_name] = row

            role_type = row.get("role_type", "").strip().lower()
            if role_type and role_type not in VALID_ROLE_TYPES:
                issues.append(
                    f"Agent role row {row_number}: unknown role_type '{role_type}'"
                )

            can_delegate = row.get("can_delegate", "").strip().lower()
            if can_delegate and can_delegate not in VALID_APPROVAL_FLAGS:
                issues.append(
                    f"Agent role row {row_number}: can_delegate must be yes or no"
                )

            can_approve_own_output = (
                row.get("can_approve_own_output", "").strip().lower()
            )
            if (
                can_approve_own_output
                and can_approve_own_output not in VALID_APPROVAL_FLAGS
            ):
                issues.append(
                    f"Agent role row {row_number}: can_approve_own_output must be "
                    "yes or no"
                )

            if role_type in {"worker", "reviewer"} and can_approve_own_output == "yes":
                issues.append(
                    f"Agent role row {row_number}: worker/reviewer agents cannot "
                    "approve their own output"
                )

        for row_number, agent_name in agent_output_names:
            if agent_name not in agent_registry:
                issues.append(
                    f"Agent row {row_number}: agent_name '{agent_name}' is not in "
                    "agent role registry"
                )

    seen_claim_ids: set[str] = set()
    if claim_csv_path is not None:
        claim_rows = load_rows(claim_csv_path)
        for row_number, row in enumerate(claim_rows, start=2):
            for field in REQUIRED_CLAIM_FIELDS:
                if not row.get(field, "").strip():
                    issues.append(
                        f"Claim row {row_number}: missing required field '{field}'"
                    )

            claim_id = row.get("claim_id", "").strip()
            if claim_id in seen_claim_ids:
                issues.append(f"Claim row {row_number}: duplicate claim_id '{claim_id}'")
            seen_claim_ids.add(claim_id)

            task_id = row.get("task_id", "").strip()
            if task_id and task_id not in seen_task_ids:
                issues.append(
                    f"Claim row {row_number}: task_id '{task_id}' is not in task tracker"
                )

            claim_strength = row.get("claim_strength", "").strip().lower()
            if claim_strength and claim_strength not in VALID_CLAIM_STRENGTHS:
                issues.append(
                    f"Claim row {row_number}: unknown claim_strength '{claim_strength}'"
                )

            evidence_requirement = row.get("evidence_requirement", "").strip().lower()
            if evidence_requirement and evidence_requirement not in VALID_EVIDENCE_REQUIREMENTS:
                issues.append(
                    f"Claim row {row_number}: unknown evidence_requirement "
                    f"'{evidence_requirement}'"
                )

            evidence_status = row.get("evidence_status", "").strip().lower()
            if evidence_status and evidence_status not in VALID_EVIDENCE_STATUSES:
                issues.append(
                    f"Claim row {row_number}: unknown evidence_status '{evidence_status}'"
                )

            publication_status = row.get("publication_status", "").strip().lower()
            if publication_status and publication_status not in VALID_PUBLICATION_STATUSES:
                issues.append(
                    f"Claim row {row_number}: unknown publication_status "
                    f"'{publication_status}'"
                )

            phrasing_status = row.get("phrasing_status", "").strip().lower()
            if phrasing_status and phrasing_status not in VALID_PHRASING_STATUSES:
                issues.append(
                    f"Claim row {row_number}: unknown phrasing_status '{phrasing_status}'"
                )

            review_status = row.get("review_status", "").strip().lower()
            if review_status and review_status not in VALID_REVIEW_STATUSES:
                issues.append(
                    f"Claim row {row_number}: unknown review_status '{review_status}'"
                )

            claim_text = row.get("claim_text", "")
            if has_binary_contrast(claim_text) and phrasing_status == "ok":
                issues.append(
                    f"Claim row {row_number}: binary contrast pattern is not flagged"
                )

            if review_status == "approved" and phrasing_status != "ok":
                issues.append(
                    f"Claim row {row_number}: approved claim has unresolved phrasing"
                )

            if (
                review_status == "approved"
                and evidence_requirement == "formal_publication"
                and evidence_status != "verified"
            ):
                issues.append(
                    f"Claim row {row_number}: approved formal-publication claim is "
                    "not evidence-verified"
                )

    if evidence_csv_path is not None:
        evidence_rows = load_rows(evidence_csv_path)
        seen_evidence_ids: set[str] = set()
        for row_number, row in enumerate(evidence_rows, start=2):
            for field in REQUIRED_EVIDENCE_FIELDS:
                if not row.get(field, "").strip():
                    issues.append(
                        f"Evidence row {row_number}: missing required field '{field}'"
                    )

            evidence_id = row.get("evidence_id", "").strip()
            if evidence_id in seen_evidence_ids:
                issues.append(
                    f"Evidence row {row_number}: duplicate evidence_id '{evidence_id}'"
                )
            seen_evidence_ids.add(evidence_id)

            claim_id = row.get("claim_id", "").strip()
            if claim_id and claim_id not in seen_claim_ids:
                issues.append(
                    f"Evidence row {row_number}: claim_id '{claim_id}' is not in claim ledger"
                )

            year = row.get("year", "").strip()
            if year and not year.isdigit():
                issues.append(f"Evidence row {row_number}: year must be numeric")

            publication_type = row.get("publication_type", "").strip().lower()
            if publication_type and publication_type not in VALID_PUBLICATION_TYPES:
                issues.append(
                    f"Evidence row {row_number}: unknown publication_type "
                    f"'{publication_type}'"
                )

            verification_status = row.get("verification_status", "").strip().lower()
            if verification_status and verification_status not in VALID_VERIFICATION_STATUSES:
                issues.append(
                    f"Evidence row {row_number}: unknown verification_status "
                    f"'{verification_status}'"
                )

            source_age_status = row.get("source_age_status", "").strip().lower()
            if source_age_status and source_age_status not in VALID_SOURCE_AGE_STATUSES:
                issues.append(
                    f"Evidence row {row_number}: unknown source_age_status "
                    f"'{source_age_status}'"
                )

            venue_decision_status = (
                row.get("venue_decision_status", "").strip().lower()
            )
            if (
                venue_decision_status
                and venue_decision_status not in VALID_VENUE_DECISION_STATUSES
            ):
                issues.append(
                    f"Evidence row {row_number}: unknown venue_decision_status "
                    f"'{venue_decision_status}'"
                )

            source_quality_status = (
                row.get("source_quality_status", "").strip().lower()
            )
            if (
                source_quality_status
                and source_quality_status not in VALID_SOURCE_QUALITY_STATUSES
            ):
                issues.append(
                    f"Evidence row {row_number}: unknown source_quality_status "
                    f"'{source_quality_status}'"
                )

            relevance_status = row.get("relevance_status", "").strip().lower()
            if relevance_status and relevance_status not in VALID_RELEVANCE_STATUSES:
                issues.append(
                    f"Evidence row {row_number}: unknown relevance_status "
                    f"'{relevance_status}'"
                )

            if verification_status == "verified":
                if venue_decision_status in {"rejected", "unknown"}:
                    issues.append(
                        f"Evidence row {row_number}: verified evidence has unresolved "
                        "venue decision status"
                    )
                if source_quality_status in {"weak", "unusable"}:
                    issues.append(
                        f"Evidence row {row_number}: verified evidence has weak or "
                        "unusable quality status"
                    )
                if relevance_status in {"contradictory", "off_topic"}:
                    issues.append(
                        f"Evidence row {row_number}: verified evidence is not relevant "
                        "to the claim"
                    )

            if venue_decision_status == "rejected" and verification_status == "verified":
                issues.append(
                    f"Evidence row {row_number}: rejected sources cannot be verified"
                )

    if handoff_csv_path is not None:
        handoff_rows = load_rows(handoff_csv_path)
        seen_handoff_ids: set[str] = set()
        for row_number, row in enumerate(handoff_rows, start=2):
            for field in REQUIRED_HANDOFF_FIELDS:
                if not row.get(field, "").strip():
                    issues.append(
                        f"Handoff row {row_number}: missing required field '{field}'"
                    )

            handoff_id = row.get("handoff_id", "").strip()
            if handoff_id in seen_handoff_ids:
                issues.append(
                    f"Handoff row {row_number}: duplicate handoff_id '{handoff_id}'"
                )
            seen_handoff_ids.add(handoff_id)

            task_id = row.get("task_id", "").strip()
            if task_id and task_id not in seen_task_ids:
                issues.append(
                    f"Handoff row {row_number}: task_id '{task_id}' is not in task tracker"
                )

            from_agent = row.get("from_agent", "").strip()
            to_agent = row.get("to_agent", "").strip()
            if from_agent and from_agent not in agent_registry:
                issues.append(
                    f"Handoff row {row_number}: from_agent '{from_agent}' is not in "
                    "agent role registry"
                )
            if to_agent and to_agent not in agent_registry:
                issues.append(
                    f"Handoff row {row_number}: to_agent '{to_agent}' is not in "
                    "agent role registry"
                )

            if from_agent == to_agent:
                issues.append(
                    f"Handoff row {row_number}: from_agent and to_agent must differ"
                )

            handoff_type = row.get("handoff_type", "").strip().lower()
            if handoff_type and handoff_type not in VALID_HANDOFF_TYPES:
                issues.append(
                    f"Handoff row {row_number}: unknown handoff_type '{handoff_type}'"
                )

            status = row.get("status", "").strip().lower()
            if status and status not in VALID_HANDOFF_STATUSES:
                issues.append(
                    f"Handoff row {row_number}: unknown status '{status}'"
                )

            from_role = agent_registry.get(from_agent, {})
            to_role = agent_registry.get(to_agent, {})
            if handoff_type == "manager_call" and from_role.get("role_type") != "orchestrator":
                issues.append(
                    f"Handoff row {row_number}: manager_call must start from an "
                    "orchestrator"
                )
            if handoff_type == "human_approval" and to_role.get("role_type") != "approver":
                issues.append(
                    f"Handoff row {row_number}: human_approval must hand off to an "
                    "approver"
                )
            if handoff_type == "peer_review" and to_role.get("role_type") != "reviewer":
                issues.append(
                    f"Handoff row {row_number}: peer_review must hand off to a reviewer"
                )
            if (
                row.get("artifact_type", "").strip().lower() == "delivery_package"
                and status == "accepted"
                and to_role.get("role_type") != "approver"
            ):
                issues.append(
                    f"Handoff row {row_number}: accepted delivery packages require "
                    "an approver boundary"
                )

    return issues


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    task_csv_path = project_root / "data" / "sample_research_tasks.csv"
    agent_csv_path = project_root / "data" / "sample_agent_outputs.csv"
    claim_csv_path = project_root / "data" / "sample_claim_ledger.csv"
    evidence_csv_path = project_root / "data" / "sample_evidence_ledger.csv"
    agent_roles_csv_path = project_root / "data" / "sample_agent_roles.csv"
    handoff_csv_path = project_root / "data" / "sample_handoff_ledger.csv"
    issues = validate_tasks(
        task_csv_path,
        agent_csv_path,
        claim_csv_path,
        evidence_csv_path,
        agent_roles_csv_path,
        handoff_csv_path,
    )

    if not issues:
        print("All task records passed validation.")
        return

    print("Validation issues:")
    for issue in issues:
        print(f"- {issue}")


if __name__ == "__main__":
    main()
