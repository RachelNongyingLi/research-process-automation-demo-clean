from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def default_project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def run_step(command: list[str], label: str) -> int:
    print(f"\n== {label} ==")
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip(), file=sys.stderr)
    return result.returncode


def parse_args() -> argparse.Namespace:
    project_root = default_project_root()
    parser = argparse.ArgumentParser(
        description="Run the local research-agent quality-gate demo."
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=project_root / "data",
        help="Directory containing the sample_* ledger CSV files.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=project_root / "reports" / "sample_weekly_report.md",
        help="Markdown report path to write.",
    )
    parser.add_argument(
        "--dashboard-output",
        type=Path,
        default=project_root / "docs" / "dashboard.html",
        help="Static HTML dashboard path to write.",
    )
    parser.add_argument(
        "--report-date",
        default="2026-06-06",
        help="Report date in YYYY-MM-DD format.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = default_project_root()
    python = sys.executable

    print("Research-Agent Quality Gate demo")
    print("Scope: local CSV ledgers + Python validation/reporting PoC.")
    print(f"Data directory: {args.data_dir}")
    print(f"Report output: {args.output}")
    print(f"Dashboard output: {args.dashboard_output}")

    validation_status = run_step(
        [
            python,
            str(project_root / "scripts" / "validate_task_fields.py"),
            "--data-dir",
            str(args.data_dir),
        ],
        "Validate ledgers",
    )
    if validation_status != 0:
        return validation_status

    report_status = run_step(
        [
            python,
            str(project_root / "scripts" / "generate_progress_report.py"),
            "--data-dir",
            str(args.data_dir),
            "--output",
            str(args.output),
            "--report-date",
            args.report_date,
        ],
        "Generate readiness report",
    )
    if report_status != 0:
        return report_status

    dashboard_status = run_step(
        [
            python,
            str(project_root / "scripts" / "build_dashboard.py"),
            "--data-dir",
            str(args.data_dir),
            "--output",
            str(args.dashboard_output),
            "--report-date",
            args.report_date,
        ],
        "Build static dashboard",
    )
    if dashboard_status != 0:
        return dashboard_status

    print("\nDemo complete.")
    print("Open the generated report to review claim, evidence, literature,")
    print("handoff, approval, and deadline gates.")
    print("Open the generated dashboard for a visual review console.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
