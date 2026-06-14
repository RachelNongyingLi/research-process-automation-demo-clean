from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

from scripts import generate_progress_report as reporter


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class GenerateProgressReportTests(unittest.TestCase):
    def test_sample_report_contains_quality_gate_sections(self) -> None:
        paths = reporter.ledger_paths(PROJECT_ROOT / "data")
        report = reporter.build_report(
            reporter.load_rows(paths["tasks"]),
            reporter.load_rows(paths["agent_outputs"]),
            reporter.load_rows(paths["claims"]),
            reporter.load_rows(paths["evidence"]),
            reporter.load_rows(paths["agent_roles"]),
            reporter.load_rows(paths["handoffs"]),
            date(2026, 6, 6),
        )

        self.assertIn("## Claim Quality Gate", report)
        self.assertIn("## Evidence Gate", report)
        self.assertIn("## Literature Quality Gate", report)
        self.assertIn("## Multi-Agent Delivery Gate", report)
        self.assertIn("C003", report)
        self.assertIn("binary_contrast", report)

    def test_cli_writes_custom_report_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output_path = Path(directory) / "readiness.md"

            result = subprocess.run(
                [
                    sys.executable,
                    str(PROJECT_ROOT / "scripts" / "generate_progress_report.py"),
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
