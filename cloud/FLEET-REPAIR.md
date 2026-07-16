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

## What I need to actually fix it (can't from this repo alone)
**Where does JARVIS run?** Its 8 employees aren't in `koori-constructions`. To repair them I
need one of:
- the repo/environment that hosts the JARVIS fleet (add it to this session), or
- confirmation that the fleet SHOULD be rebuilt here (then I build real employees on the
  monitor + email-admin foundation already committed).

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
