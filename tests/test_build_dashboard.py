from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

from scripts import build_dashboard
from scripts import generate_progress_report as reporter


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class BuildDashboardTests(unittest.TestCase):
    def test_dashboard_contains_key_sections_and_metrics(self) -> None:
        paths = reporter.ledger_paths(PROJECT_ROOT / "data")
        html = build_dashboard.build_dashboard(
            reporter.load_rows(paths["tasks"]),
            reporter.load_rows(paths["agent_outputs"]),
            reporter.load_rows(paths["claims"]),
            reporter.load_rows(paths["evidence"]),
            reporter.load_rows(paths["agent_roles"]),
            reporter.load_rows(paths["handoffs"]),
            date(2026, 6, 6),
        )

        self.assertIn("Research-Agent Quality Gate", html)
        self.assertIn('data-testid="approval-queue"', html)
        self.assertIn('data-testid="claim-gate"', html)
        self.assertIn('data-testid="literature-gate"', html)
        self.assertIn("No live LLM/RAG runtime in this PoC", html)

    def test_cli_writes_dashboard(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output_path = Path(directory) / "dashboard.html"

            result = subprocess.run(
                [
                    sys.executable,
                    str(PROJECT_ROOT / "scripts" / "build_dashboard.py"),
                    "--data-dir",
                    str(PROJECT_ROOT / "data"),
                    "--output",
                    str(output_path),
                    "--report-date",
                    "2026-06-14",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0)
            self.assertTrue(output_path.exists())
            self.assertIn(
                "Report date: 2026-06-14",
                output_path.read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
