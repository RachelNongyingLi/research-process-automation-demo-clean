import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path


def load_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


DEMO_REPORT_DATE = date(2026, 6, 6)


def build_report(
    rows: list[dict[str, str]],
    agent_outputs: list[dict[str, str]],
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
    upcoming = [
        row for row in rows
        if row["status"] != "done"
        and 0 <= (
            datetime.strptime(row["due_date"], "%Y-%m-%d").date() - report_date
        ).days <= 3
    ]

    lines = [
        "# Sample Weekly Research Progress Report",
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

    lines.extend(["", "## Blockers"])
    blockers = [row for row in rows if row.get("blocker", "").strip()]
    if blockers:
        for row in blockers:
            lines.append(f"- {row['task_id']}: {row['blocker']}")
    else:
        lines.append("- No blockers recorded.")

    return "\n".join(lines) + "\n"


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    rows = load_rows(project_root / "data" / "sample_research_tasks.csv")
    agent_outputs = load_rows(project_root / "data" / "sample_agent_outputs.csv")
    report = build_report(rows, agent_outputs)
    output_path = project_root / "reports" / "sample_weekly_report.md"
    output_path.write_text(report, encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
