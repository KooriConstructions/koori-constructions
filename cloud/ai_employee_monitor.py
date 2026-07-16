#!/usr/bin/env python3
"""
Koori AI-Employee Monitor — the watchdog over every autonomous worker.

Purpose: answer one question on demand — "is each AI employee alive, running on
schedule, and actually producing output?" — and fail loudly when the answer is no.

Design goals:
- ZERO external dependencies (stdlib only) so it always runs, even when the
  workers it watches cannot (the recipe miner needs requests/anthropic/graph;
  this monitor needs nothing).
- Self-describing registry: add a worker to EMPLOYEES and it is monitored.
- Honest health, not vanity: a worker whose code is still TODO stubs is reported
  as SKELETON (not WORKING), and a worker that has never really run is STALE.

Exit code is non-zero if any employee is unhealthy, so CI / a scheduled run can
surface the alert instead of going green on a dead fleet.

Run:  python cloud/ai_employee_monitor.py
Env:  REPO_ROOT (default '.'),  STALE_GRACE_DAYS (default 1)
"""

import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, List

# =============================================================================
# REGISTRY — every AI employee the business runs. Add a dict here to monitor it.
# =============================================================================
# cadence_days: how often this worker is EXPECTED to produce output.
#   7  = weekly (e.g. Friday miner), 1 = daily, 0 = on-demand (never "stale").
# source: path scanned to decide WORKING vs SKELETON (TODO-stub detection).
# state:  path to the worker's state json; used for "last real output" + dedup.
# output_key / output_ts_key: keys inside state that prove real output happened.

EMPLOYEES: List[Dict] = [
    {
        "id": "recipe-miner",
        "name": "Friday Recipe Miner",
        "role": "Mines Invoiced jobs into KRV0 recipes + KCI0 catalogue, drafts to Brad",
        "cadence_days": 7,
        "source": "cloud/koori_recipe_miner.py",
        "state": "cloud/recipe-miner-state.json",
        "output_key": "mined_jobs",       # non-empty list == it produced something
        "output_ts_key": "last_run",       # ISO timestamp of last real run
        "workflow": ".github/workflows/friday-recipe-miner.yml",
    },
    {
        "id": "email-admin",
        "name": "Email Admin (inbox triage + draft)",
        "role": "Reads every incoming email, drafts replies for human-needed mail, flags bills/compliance, lists marketing to unsubscribe",
        "cadence_days": 1,
        "source": "cloud/koori_email_admin.py",
        "state": "cloud/email-admin-state.json",
        "output_key": "drafted",
        "output_ts_key": "checked_at",
        "workflow": "(Zapier real-time + scheduled digest — activation pending Graph Mail.ReadWrite)",
    },
]

# A worker is SKELETON if its source still carries this many unfinished markers.
SKELETON_MARKER = re.compile(r"TODO|mock return|Wire up|placeholder", re.IGNORECASE)
SKELETON_THRESHOLD = 3


# =============================================================================
# HEALTH CHECKS
# =============================================================================

def _read_json(path: str) -> Optional[Dict]:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _parse_ts(value) -> Optional[datetime]:
    if not value or not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _detect_skeleton(source_path: str) -> Dict:
    """Scan a worker's source for unfinished-integration markers."""
    try:
        with open(source_path, "r") as f:
            text = f.read()
    except OSError:
        return {"exists": False, "markers": 0, "skeleton": True}
    markers = len(SKELETON_MARKER.findall(text))
    return {"exists": True, "markers": markers, "skeleton": markers >= SKELETON_THRESHOLD}


def check_employee(emp: Dict, repo_root: str, now: datetime, grace_days: int) -> Dict:
    """Return a health record for one employee: WORKING / SKELETON / STALE / DEAD."""
    source_path = os.path.join(repo_root, emp["source"])
    state_path = os.path.join(repo_root, emp["state"])

    code = _detect_skeleton(source_path)
    state = _read_json(state_path)

    issues: List[str] = []
    last_run = _parse_ts((state or {}).get(emp.get("output_ts_key", ""), None))
    output = (state or {}).get(emp.get("output_key", ""), None)
    produced = bool(output) if output is not None else False

    # 1. Does the code exist and is it actually wired?
    if not code["exists"]:
        issues.append("source file missing")
    elif code["skeleton"]:
        issues.append(f"source is a skeleton ({code['markers']} TODO/stub markers) — cannot produce real output")

    # 2. Has it ever produced output?
    if state is None:
        issues.append("no state file — worker has never recorded a run")
    elif not produced:
        issues.append("state shows zero output ever produced")

    # 3. Is it running on schedule? (cadence_days == 0 means on-demand, never stale)
    stale = False
    if emp["cadence_days"] > 0:
        deadline_days = emp["cadence_days"] + grace_days
        if last_run is None:
            issues.append("no real last-run timestamp")
            stale = True
        else:
            age = now - last_run
            if age > timedelta(days=deadline_days):
                issues.append(
                    f"last output {age.days}d ago — overdue (expected every {emp['cadence_days']}d)"
                )
                stale = True

    # Verdict — worst wins.
    if not code["exists"] or state is None:
        status = "DEAD"
    elif code["skeleton"]:
        status = "SKELETON"
    elif stale or not produced:
        status = "STALE"
    else:
        status = "WORKING"

    return {
        "id": emp["id"],
        "name": emp["name"],
        "role": emp["role"],
        "status": status,
        "healthy": status == "WORKING",
        "last_run": last_run.isoformat() if last_run else None,
        "produced_output": produced,
        "cadence_days": emp["cadence_days"],
        "issues": issues,
    }


# =============================================================================
# REPORTING
# =============================================================================

_ICON = {"WORKING": "✅", "STALE": "⚠️ ", "SKELETON": "🚧", "DEAD": "❌"}


def render_report(records: List[Dict], now: datetime) -> str:
    lines = []
    lines.append("=" * 68)
    lines.append("KOORI AI-EMPLOYEE MONITOR")
    lines.append(f"Checked: {now.isoformat()}")
    lines.append("=" * 68)

    working = sum(1 for r in records if r["status"] == "WORKING")
    lines.append(f"Fleet: {len(records)} employee(s) — {working} WORKING, "
                 f"{len(records) - working} needing attention")
    lines.append("")

    for r in records:
        lines.append(f"{_ICON[r['status']]} {r['name']}  [{r['status']}]")
        lines.append(f"     role: {r['role']}")
        lines.append(f"     last real output: {r['last_run'] or 'NEVER'}  |  "
                     f"produced output: {'yes' if r['produced_output'] else 'no'}")
        if r["issues"]:
            for issue in r["issues"]:
                lines.append(f"       - {issue}")
        lines.append("")

    lines.append("=" * 68)
    return "\n".join(lines)


def main() -> int:
    repo_root = os.environ.get("REPO_ROOT", ".")
    grace_days = int(os.environ.get("STALE_GRACE_DAYS", "1"))
    now = datetime.now(timezone.utc)

    records = [check_employee(emp, repo_root, now, grace_days) for emp in EMPLOYEES]

    report = render_report(records, now)
    print(report)

    # Persist machine-readable status for dashboards / alerting.
    status_path = os.path.join(repo_root, "cloud", "monitor-status.json")
    try:
        with open(status_path, "w") as f:
            json.dump({
                "checked_at": now.isoformat(),
                "fleet_size": len(records),
                "healthy": sum(1 for r in records if r["healthy"]),
                "employees": records,
            }, f, indent=2)
        print(f"\nStatus written: {status_path}")
    except OSError as e:
        print(f"WARN: could not write status file: {e}")

    unhealthy = [r for r in records if not r["healthy"]]
    if unhealthy:
        print(f"\n❌ {len(unhealthy)} employee(s) unhealthy: "
              f"{', '.join(r['id'] for r in unhealthy)}")
        return 1
    print("\n✅ All employees healthy.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
