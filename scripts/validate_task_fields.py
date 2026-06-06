import csv
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

VALID_STATUSES = {"not_started", "in_progress", "blocked", "done"}
VALID_APPROVAL_FLAGS = {"yes", "no"}
VALID_APPROVAL_STATUSES = {"not_required", "pending", "approved", "rejected"}
VALID_PRIORITIES = {"low", "medium", "high"}


def load_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def is_iso_date(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def validate_tasks(task_csv_path: Path, agent_csv_path: Path | None = None) -> list[str]:
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

            needs_review = row.get("needs_human_review", "").strip().lower()
            if needs_review and needs_review not in VALID_APPROVAL_FLAGS:
                issues.append(
                    f"Agent row {row_number}: needs_human_review must be yes or no"
                )

    return issues


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    task_csv_path = project_root / "data" / "sample_research_tasks.csv"
    agent_csv_path = project_root / "data" / "sample_agent_outputs.csv"
    issues = validate_tasks(task_csv_path, agent_csv_path)

    if not issues:
        print("All task records passed validation.")
        return

    print("Validation issues:")
    for issue in issues:
        print(f"- {issue}")


if __name__ == "__main__":
    main()
