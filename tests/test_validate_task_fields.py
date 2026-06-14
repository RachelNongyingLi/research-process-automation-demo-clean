from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from scripts import validate_task_fields as validator


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0])
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def valid_task() -> dict[str, str]:
    return {
        "task_id": "T100",
        "project_name": "Demo",
        "task_title": "Validate demo row",
        "owner": "Nongying Li",
        "due_date": "2026-06-09",
        "status": "in_progress",
        "approval_needed": "no",
        "approval_status": "not_required",
        "priority": "high",
        "blocker": "",
    }


class ValidateTaskFieldsTests(unittest.TestCase):
    def test_sample_ledgers_pass_validation(self) -> None:
        paths = validator.ledger_paths(PROJECT_ROOT / "data")

        issues = validator.validate_tasks(
            paths["tasks"],
            paths["agent_outputs"],
            paths["claims"],
            paths["evidence"],
            paths["agent_roles"],
            paths["handoffs"],
        )

        self.assertEqual(issues, [])

    def test_missing_required_task_field_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tmp_path = Path(directory)
            row = valid_task()
            row["owner"] = ""
            task_path = tmp_path / "sample_research_tasks.csv"
            write_csv(task_path, [row])

            issues = validator.validate_tasks(task_path)

        self.assertIn("Row 2: missing required field 'owner'", issues)

    def test_worker_self_approval_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tmp_path = Path(directory)
            task_path = tmp_path / "sample_research_tasks.csv"
            roles_path = tmp_path / "sample_agent_roles.csv"
            write_csv(task_path, [valid_task()])
            write_csv(
                roles_path,
                [
                    {
                        "agent_name": "draft_agent",
                        "role_type": "worker",
                        "primary_responsibility": "Drafts provisional artifacts.",
                        "can_delegate": "no",
                        "can_approve_own_output": "yes",
                        "required_input": "task_record",
                        "required_output": "draft_artifact",
                        "approval_boundary": "critic_agent",
                    }
                ],
            )

            issues = validator.validate_tasks(
                task_path,
                agent_roles_csv_path=roles_path,
            )

        self.assertTrue(
            any("worker/reviewer agents cannot approve" in issue for issue in issues)
        )

    def test_rejected_source_cannot_be_verified(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tmp_path = Path(directory)
            task_path = tmp_path / "sample_research_tasks.csv"
            claim_path = tmp_path / "sample_claim_ledger.csv"
            evidence_path = tmp_path / "sample_evidence_ledger.csv"
            write_csv(task_path, [valid_task()])
            write_csv(
                claim_path,
                [
                    {
                        "claim_id": "C100",
                        "task_id": "T100",
                        "claim_text": "A tracked claim needs evidence.",
                        "claim_strength": "moderate",
                        "evidence_requirement": "formal_publication",
                        "evidence_status": "partial",
                        "publication_status": "peer_reviewed",
                        "phrasing_status": "ok",
                        "review_status": "pending",
                        "issue": "",
                    }
                ],
            )
            write_csv(
                evidence_path,
                [
                    {
                        "evidence_id": "E100",
                        "claim_id": "C100",
                        "title": "Rejected candidate source",
                        "venue": "Search log",
                        "year": "2024",
                        "publication_type": "search_result",
                        "source_location": "search_log:test",
                        "usage_role": "Negative candidate example",
                        "verification_status": "verified",
                        "source_age_status": "current",
                        "venue_decision_status": "rejected",
                        "source_quality_status": "strong",
                        "relevance_status": "direct",
                    }
                ],
            )

            issues = validator.validate_tasks(
                task_path,
                claim_csv_path=claim_path,
                evidence_csv_path=evidence_path,
            )

        self.assertTrue(
            any("rejected sources cannot be verified" in issue for issue in issues)
        )


if __name__ == "__main__":
    unittest.main()
