from __future__ import annotations

import argparse
import html
from collections import Counter
from datetime import date, datetime
from pathlib import Path

try:
    from .generate_progress_report import DEMO_REPORT_DATE, ledger_paths, load_rows
except ImportError:
    from generate_progress_report import DEMO_REPORT_DATE, ledger_paths, load_rows


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def status_class(value: str) -> str:
    normalized = value.strip().lower()
    if normalized in {"approved", "verified", "accepted", "done", "ok"}:
        return "good"
    if normalized in {"pending", "partial", "needs_revision", "needs_rewrite"}:
        return "warn"
    if normalized in {"blocked", "rejected", "missing", "unusable", "off_topic"}:
        return "bad"
    if normalized in {"not_required", "internal", "foundational", "background"}:
        return "neutral"
    return "info"


def badge(value: str) -> str:
    label = esc(value or "none")
    return f'<span class="badge {status_class(value)}">{label}</span>'


def table(headers: list[str], rows: list[list[str]], empty: str) -> str:
    if not rows:
        return f'<p class="empty">{esc(empty)}</p>'
    head = "".join(f"<th>{esc(header)}</th>" for header in headers)
    body = "\n".join(
        "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
        for row in rows
    )
    return f"""
      <div class="table-wrap">
        <table>
          <thead><tr>{head}</tr></thead>
          <tbody>{body}</tbody>
        </table>
      </div>
    """


def metric(label: str, value: int, tone: str = "info") -> str:
    return f"""
      <div class="metric {tone}">
        <span>{esc(label)}</span>
        <strong>{value}</strong>
      </div>
    """


def progress_bar(label: str, value: int, total: int, tone: str) -> str:
    percent = int((value / total) * 100) if total else 0
    return f"""
      <div class="bar-row">
        <div class="bar-label"><span>{esc(label)}</span><strong>{value}</strong></div>
        <div class="bar-track"><div class="bar-fill {tone}" style="width:{percent}%"></div></div>
      </div>
    """


def build_dashboard(
    tasks: list[dict[str, str]],
    agent_outputs: list[dict[str, str]],
    claims: list[dict[str, str]],
    evidence: list[dict[str, str]],
    agent_roles: list[dict[str, str]],
    handoffs: list[dict[str, str]],
    report_date: date = DEMO_REPORT_DATE,
) -> str:
    task_lookup = {row["task_id"]: row for row in tasks}
    evidence_by_claim: dict[str, list[dict[str, str]]] = {}
    for record in evidence:
        evidence_by_claim.setdefault(record["claim_id"], []).append(record)

    status_counts = Counter(row["status"] for row in tasks)
    approval_queue = [
        row
        for row in tasks
        if row["approval_needed"].lower() == "yes"
        and row["approval_status"].lower() != "approved"
    ]
    review_queue = [
        row
        for row in agent_outputs
        if row.get("needs_human_review", "").lower() == "yes"
    ]
    unresolved_claims = [
        row
        for row in claims
        if row["review_status"] != "approved"
        or row["evidence_status"] in {"missing", "partial"}
        or row["phrasing_status"] != "ok"
    ]
    evidence_risks = [
        row
        for row in claims
        if row["evidence_requirement"] == "formal_publication"
        and row["evidence_status"] != "verified"
    ]
    literature_risks = [
        row
        for row in evidence
        if row.get("verification_status") != "verified"
        or row.get("source_age_status") in {"dated", "stale", "unknown"}
        or row.get("venue_decision_status") in {
            "preprint_only",
            "rejected",
            "unknown",
        }
        or row.get("source_quality_status") in {"weak", "unusable"}
        or row.get("relevance_status") in {"contradictory", "off_topic"}
    ]
    open_handoffs = [
        row
        for row in handoffs
        if row["status"] in {"pending", "needs_revision", "blocked"}
    ]
    due_soon = []
    for row in tasks:
        if row["status"] == "done":
            continue
        days = (datetime.strptime(row["due_date"], "%Y-%m-%d").date() - report_date).days
        if 0 <= days <= 3:
            due_soon.append(row)

    task_rows = [
        [
            f"<strong>{esc(row['task_id'])}</strong>",
            esc(row["task_title"]),
            badge(row["status"]),
            badge(row["approval_status"]),
            badge(row["priority"]),
            esc(row.get("blocker", "") or "-"),
        ]
        for row in tasks
    ]
    approval_rows = [
        [
            f"<strong>{esc(row['task_id'])}</strong>",
            esc(row["task_title"]),
            badge(row["approval_status"]),
            esc(row.get("blocker", "") or "-"),
        ]
        for row in approval_queue
    ]
    claim_rows = [
        [
            f"<strong>{esc(row['claim_id'])}</strong>",
            esc(row["task_id"]),
            esc(row["claim_text"]),
            badge(row["evidence_status"]),
            badge(row["phrasing_status"]),
            badge(row["review_status"]),
            esc(row.get("issue", "") or "-"),
        ]
        for row in unresolved_claims
    ]
    evidence_rows = [
        [
            f"<strong>{esc(row['claim_id'])}</strong>",
            badge(row["claim_strength"]),
            badge(row["evidence_status"]),
            esc(", ".join(
                f"{record['venue']} {record['year']}"
                for record in evidence_by_claim.get(row["claim_id"], [])
            ) or "no source"),
        ]
        for row in evidence_risks
    ]
    literature_rows = [
        [
            f"<strong>{esc(row['evidence_id'])}</strong>",
            esc(row["title"]),
            badge(row["verification_status"]),
            badge(row["source_age_status"]),
            badge(row["venue_decision_status"]),
            badge(row["source_quality_status"]),
            badge(row["relevance_status"]),
        ]
        for row in literature_risks
    ]
    handoff_rows = [
        [
            f"<strong>{esc(row['handoff_id'])}</strong>",
            esc(f"{row['from_agent']} -> {row['to_agent']}"),
            badge(row["handoff_type"]),
            badge(row["status"]),
            esc(row["delivery_impact"]),
        ]
        for row in open_handoffs
    ]
    role_rows = [
        [
            f"<strong>{esc(row['agent_name'])}</strong>",
            badge(row["role_type"]),
            esc(row["required_input"]),
            esc(row["required_output"]),
            esc(row["approval_boundary"]),
        ]
        for row in agent_roles
    ]
    review_rows = [
        [
            f"<strong>{esc(row['task_id'])}</strong>",
            esc(row["agent_name"]),
            badge(row["output_type"]),
            esc(row["summary"]),
        ]
        for row in review_queue
        if row.get("task_id") in task_lookup
    ]

    total_tasks = len(tasks)
    bars = "\n".join(
        progress_bar(status, count, total_tasks, status_class(status))
        for status, count in sorted(status_counts.items())
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Research-Agent Quality Gate Dashboard</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f6f8fb;
      --surface: #ffffff;
      --line: #d8dee8;
      --text: #172033;
      --muted: #667085;
      --blue: #2563eb;
      --green: #0f8a5f;
      --amber: #b45309;
      --red: #b42318;
      --teal: #0f766e;
      --gray: #5f6b7a;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      font-size: 15px;
      line-height: 1.45;
    }}
    header {{
      background: var(--surface);
      border-bottom: 1px solid var(--line);
      padding: 22px 28px;
    }}
    main {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 24px 28px 40px;
    }}
    h1, h2 {{
      margin: 0;
      letter-spacing: 0;
    }}
    h1 {{ font-size: 28px; font-weight: 760; }}
    h2 {{ font-size: 18px; font-weight: 720; }}
    .subline {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 8px;
      color: var(--muted);
    }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(6, minmax(130px, 1fr));
      gap: 12px;
      margin: 0 0 18px;
    }}
    .metric {{
      background: var(--surface);
      border: 1px solid var(--line);
      border-left: 4px solid var(--blue);
      border-radius: 8px;
      padding: 14px 14px 12px;
      min-height: 88px;
    }}
    .metric.good {{ border-left-color: var(--green); }}
    .metric.warn {{ border-left-color: var(--amber); }}
    .metric.bad {{ border-left-color: var(--red); }}
    .metric.neutral {{ border-left-color: var(--gray); }}
    .metric span {{
      display: block;
      color: var(--muted);
      font-size: 13px;
      min-height: 34px;
    }}
    .metric strong {{
      display: block;
      margin-top: 4px;
      font-size: 30px;
      line-height: 1;
    }}
    .grid {{
      display: grid;
      grid-template-columns: minmax(280px, 0.85fr) minmax(0, 1.15fr);
      gap: 16px;
    }}
    section {{
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      margin-bottom: 16px;
      overflow: hidden;
    }}
    section > h2 {{
      padding: 15px 16px;
      border-bottom: 1px solid var(--line);
      background: #fbfcfe;
    }}
    .section-body {{ padding: 16px; }}
    .bar-row + .bar-row {{ margin-top: 12px; }}
    .bar-label {{
      display: flex;
      justify-content: space-between;
      color: var(--muted);
      font-size: 13px;
      margin-bottom: 6px;
    }}
    .bar-label strong {{ color: var(--text); }}
    .bar-track {{
      height: 10px;
      background: #edf1f7;
      border-radius: 999px;
      overflow: hidden;
    }}
    .bar-fill {{
      height: 100%;
      background: var(--blue);
    }}
    .bar-fill.good {{ background: var(--green); }}
    .bar-fill.warn {{ background: var(--amber); }}
    .bar-fill.bad {{ background: var(--red); }}
    .bar-fill.neutral {{ background: var(--gray); }}
    .table-wrap {{ overflow-x: auto; }}
    table {{
      width: 100%;
      border-collapse: collapse;
      min-width: 720px;
    }}
    th, td {{
      padding: 10px 12px;
      border-bottom: 1px solid #e7ebf1;
      text-align: left;
      vertical-align: top;
    }}
    th {{
      color: var(--muted);
      font-size: 12px;
      font-weight: 720;
      text-transform: uppercase;
      background: #fbfcfe;
    }}
    tr:last-child td {{ border-bottom: 0; }}
    .badge {{
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      border-radius: 999px;
      padding: 3px 9px;
      font-size: 12px;
      font-weight: 680;
      white-space: nowrap;
      background: #e8eefb;
      color: #21468f;
    }}
    .badge.good {{ background: #dcfce7; color: var(--green); }}
    .badge.warn {{ background: #fef3c7; color: var(--amber); }}
    .badge.bad {{ background: #fee2e2; color: var(--red); }}
    .badge.neutral {{ background: #edf1f7; color: var(--gray); }}
    .empty {{ margin: 0; color: var(--muted); }}
    .full {{ grid-column: 1 / -1; }}
    @media (max-width: 1000px) {{
      .metrics {{ grid-template-columns: repeat(3, minmax(130px, 1fr)); }}
      .grid {{ grid-template-columns: 1fr; }}
    }}
    @media (max-width: 620px) {{
      header, main {{ padding-left: 16px; padding-right: 16px; }}
      h1 {{ font-size: 23px; }}
      .metrics {{ grid-template-columns: repeat(2, minmax(120px, 1fr)); }}
      .metric strong {{ font-size: 26px; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Research-Agent Quality Gate</h1>
    <div class="subline">
      <span>Report date: {esc(report_date.isoformat())}</span>
      <span>CSV ledgers + Python gates</span>
      <span>No live LLM/RAG runtime in this PoC</span>
    </div>
  </header>
  <main>
    <div class="metrics" data-testid="dashboard-metrics">
      {metric("Tasks", len(tasks), "info")}
      {metric("Pending approvals", len(approval_queue), "warn")}
      {metric("Unresolved claims", len(unresolved_claims), "warn")}
      {metric("Evidence risks", len(evidence_risks), "bad" if evidence_risks else "good")}
      {metric("Literature risks", len(literature_risks), "bad" if literature_risks else "good")}
      {metric("Open handoffs", len(open_handoffs), "warn" if open_handoffs else "good")}
    </div>

    <div class="grid">
      <section data-testid="status-distribution">
        <h2>Status Distribution</h2>
        <div class="section-body">{bars}</div>
      </section>
      <section data-testid="deadline-queue">
        <h2>Deadline Queue</h2>
        {table(
            ["Task", "Title", "Status", "Approval", "Priority", "Blocker"],
            [
                [
                    f"<strong>{esc(row['task_id'])}</strong>",
                    esc(row["task_title"]),
                    badge(row["status"]),
                    badge(row["approval_status"]),
                    badge(row["priority"]),
                    esc(row.get("blocker", "") or "-"),
                ]
                for row in due_soon
            ],
            "No open tasks due within three days.",
        )}
      </section>
      <section data-testid="approval-queue">
        <h2>Approval Queue</h2>
        {table(["Task", "Title", "Approval", "Blocker"], approval_rows, "No pending approvals.")}
      </section>
      <section data-testid="agent-review-queue">
        <h2>Agent Review Queue</h2>
        {table(["Task", "Agent", "Output", "Summary"], review_rows, "No agent outputs waiting for review.")}
      </section>
      <section class="full" data-testid="claim-gate">
        <h2>Claim Gate</h2>
        {table(["Claim", "Task", "Text", "Evidence", "Phrasing", "Review", "Action"], claim_rows, "All tracked claims are approved.")}
      </section>
      <section class="full" data-testid="evidence-gate">
        <h2>Evidence Gate</h2>
        {table(["Claim", "Strength", "Evidence", "Sources"], evidence_rows, "No formal-publication evidence risks.")}
      </section>
      <section class="full" data-testid="literature-gate">
        <h2>Literature Gate</h2>
        {table(["Evidence", "Title", "Verification", "Age", "Venue", "Quality", "Relevance"], literature_rows, "No stale, rejected, weak, or off-topic literature candidates.")}
      </section>
      <section class="full" data-testid="handoff-trail">
        <h2>Handoff Trail</h2>
        {table(["Handoff", "Route", "Type", "Status", "Impact"], handoff_rows, "No open handoff issues.")}
      </section>
      <section class="full" data-testid="agent-roles">
        <h2>Agent Role Boundaries</h2>
        {table(["Agent", "Role", "Input", "Output", "Approval Boundary"], role_rows, "No agent roles recorded.")}
      </section>
      <section class="full" data-testid="task-ledger">
        <h2>Task Ledger</h2>
        {table(["Task", "Title", "Status", "Approval", "Priority", "Blocker"], task_rows, "No tasks recorded.")}
      </section>
    </div>
  </main>
</body>
</html>
"""


def parse_args() -> argparse.Namespace:
    project_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="Build a static HTML dashboard from quality-gate CSV ledgers."
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
        default=project_root / "docs" / "dashboard.html",
        help="HTML dashboard path to write.",
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
    dashboard = build_dashboard(
        load_rows(paths["tasks"]),
        load_rows(paths["agent_outputs"]),
        load_rows(paths["claims"]),
        load_rows(paths["evidence"]),
        load_rows(paths["agent_roles"]),
        load_rows(paths["handoffs"]),
        args.report_date,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(dashboard, encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
