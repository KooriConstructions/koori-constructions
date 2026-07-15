# Koori AI-Employee Status & Launch Brief

_Prepared by the monitoring session. Snapshot: 2026-07-15._

## TL;DR

You asked me to watch over "all running AI employees" and make sure they're
working 24/7 and producing output. Here is the honest picture:

- **The fleet is one employee, and it has never produced a single output.**
- The gap between the plan ("24/7 autonomous AI employees") and reality is large
  but the path to close it is short and concrete (below).
- I've added the missing piece you actually asked for: a **monitor** that checks
  the fleet daily and goes red the moment a worker is dead, stale, or fake.

## What actually exists (full inventory)

| Item | Reality |
|------|---------|
| AI employees | **1** — the Friday Recipe Miner |
| Other agents / sessions / branches / PRs | **None** in scope |
| Scheduled `/loop` jobs | **None** |
| Docs / SKILL.md / transcripts | **None** in the repo |
| Monitoring | **None** — until this brief |

## Health of the one employee: Friday Recipe Miner

**Status: 🚧 SKELETON — not working.** Three independent failures, any one of
which alone means zero output:

1. **It's a skeleton, not a worker.** Every integration function
   (`read_job_pipeline`, `read_xero_invoices`, `read_buildxact_quote`,
   `create_outlook_draft`) is a `TODO` stub that returns empty/mock data. The
   monitor counts 29 unfinished markers in the source. Even a flawless run emits
   nothing — `read_job_pipeline` returns `[]`, so `main()` prints "No jobs ready
   to mine" and exits. **By construction it cannot produce output yet.**

2. **Its only run failed at startup.** The single GitHub Actions execution
   (2026-06-25) has `conclusion: failure` with **0 jobs** — the run never
   executed a single step. No successful run has ever occurred.

3. **The schedule isn't firing.** Committed ~3 weeks ago with cron `0 7 * * 5`
   (Fridays), yet **zero scheduled runs exist**. The `last_run` value in
   `recipe-miner-state.json` is still the hard-coded placeholder
   (`2026-06-25T00:00:00Z`) — no real run has ever updated it.

## Recommendations — prioritized path to "live"

### P0 — Make _something_ actually run (this week)
1. **Confirm Actions scheduling is on.** Settings → Actions → General: Actions
   enabled, and scheduled workflows allowed. The absence of *any* scheduled run
   across 3 Fridays points to a repo-level scheduling problem, not a code bug.
   The new monitor workflow is a second scheduled job — if it also never fires,
   that confirms the setting is the blocker.
2. **Verify the two secrets exist:** `ANTHROPIC_API_KEY`, `GRAPH_TOKEN`. A
   startup failure with 0 jobs is consistent with a workflow/secret setup issue.
3. **Re-run the miner manually** (`workflow_dispatch`) and read the logs. It will
   run green but produce nothing — that's expected until P1.

### P1 — Wire one real integration end-to-end (next)
Pick the **thinnest vertical slice** and make it real before broadening:
- Wire `read_job_pipeline` to the SharePoint list (fill in the site-id/list-id
  the code TODO already sketches), filtered to `Status='Invoiced'`.
- Wire `create_outlook_draft` to the Graph draft endpoint (already stubbed).
- Leave Xero/Buildxact mocked for one job, so you get a real draft to Brad from a
  real job. **One working draft beats six half-wired integrations.**
- The monitor will flip that employee from 🚧 SKELETON to ✅ WORKING automatically
  once the stubs are gone and it records real output.

### P2 — Only then scale the fleet
- Add the next employee (whatever's next on the plan) as a new `cloud/*.py` +
  workflow, and **register it in `EMPLOYEES`** in `ai_employee_monitor.py`. That
  one line is all the monitoring it needs.
- Consider a shared `daily-build-state.json` cost ledger (the miner workflow
  already writes to it) so spend is tracked as the fleet grows.

## The monitor (added this session)

- **`cloud/ai_employee_monitor.py`** — stdlib-only, always runs. Reads each
  registered employee's source + state and classifies it WORKING / STALE /
  SKELETON / DEAD. Exits non-zero if any are unhealthy. Add a worker to the
  `EMPLOYEES` registry and it's watched.
- **`.github/workflows/ai-employee-monitor.yml`** — runs the monitor daily
  (~06:30 AEST), commits `monitor-status.json`, and **goes red in the Actions
  tab** the moment the fleet is unhealthy. Zero secrets, zero external services.
- **`cloud/monitor-status.json`** — machine-readable heartbeat for a future
  dashboard or email alert.

### Honest limitation
The monitor's schedule depends on the same GitHub Actions scheduling that isn't
currently firing (P0). It works on-demand today (`workflow_dispatch` or locally:
`python cloud/ai_employee_monitor.py`); it becomes truly 24/7 once P0 is fixed.
