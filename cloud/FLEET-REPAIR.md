# Fleet Repair — standing background workstream

**Status: OPEN. The AI fleet does not actually work.** (Confirmed by Brad, 2026-07-16.)

## The gap
- JARVIS emails digests claiming "**8 employees running, ~20–107 artifacts/day**" — but
  the output is **hollow**: no real deliverables land. The digests are theatre.
- In THIS repo the only fleet worker is the **recipe miner**, which is a TODO skeleton
  that has never produced output and whose schedule doesn't fire (see AI-EMPLOYEE-STATUS.md).
- So "fleet is running" is a false green. Real functioning employees = **0**.

## Known blockers (what I can see from here)
1. **Anthropic API cap maxed** — spend paused repeatedly ($1k→$1.1k→$1.4k alerts, 13–15 Jul).
   Any employee that calls the API is dead in the water until the cap is raised. **Blocker #0.**
2. **GitHub Actions scheduling not firing** — no scheduled run has ever executed (repo setting
   or inactivity disable). Nothing recurring actually triggers.
3. **Integrations unwired** — recipe miner (SharePoint/Xero/Buildxact/Graph) are all stubs.
4. **No health signal** — until the monitor added here, nothing reported a dead employee,
   so hollow digests read as success.

## Where JARVIS runs (investigated 2026-07-16)
- **Not a GitHub repo.** The KooriConstructions GitHub org has **exactly one** repo —
  `koori-constructions` (this one). There is no `jarvis` repo to add.
- Strong signal it runs via **Cowork** (claude.ai): SharePoint holds
  `Handoff/Koori-Master-Handoff.md` — "the single source-of-truth for any Claude / Cowork
  session" — plus a `_Cowork-Archive/` tree of daily briefs. The fleet is almost certainly
  **Cowork sessions/agents defined by that handoff + SharePoint**, not committed code.

## What I need to actually fix it
1. **Read `Koori-Master-Handoff.md`** (the fleet's operating doc) — I can do this next; it
   likely names the 8 employees and how JARVIS orchestrates them.
2. Then either: point the monitor at those employees' real outputs, or rebuild them as real
   scheduled workers on the monitor + email-admin foundation already committed here.
3. Confirm from Brad: is JARVIS a **Cowork** setup, a script on a **server/PC**, or something
   else? That determines where the fix lands.

## Plan (once the above is answered)
1. Raise the API cap (Brad) — unblocks everything.
2. Point the monitor at the real fleet employees (one registry line each) so hollow output
   is caught immediately (SKELETON/STALE/DEAD).
3. Fix one employee end-to-end (thin vertical slice) and prove real output before scaling —
   same discipline as the recipe-miner P1.
4. Kill or fix the JARVIS digest so "artifacts shipped" reflects verified output, not claims.

## Next action
Ask Brad: **which repo/environment is the JARVIS fleet in** — so it can be added and actually
repaired, rather than reported on from the outside.
