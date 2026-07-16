# Fleet Repair — standing background workstream

**Status: OPEN — but now DIAGNOSED** (Master Handoff read 2026-07-16).

## What "JARVIS" / the fleet actually is
Per `Handoff/Koori-Master-Handoff.md`, the fleet is **101 scheduled "AI employees"** on a
deliberate **two-layer** architecture — NOT in this GitHub repo:

- **Layer 1 — 24/7 launchd Python on Brad's Mac.** ~22 high-frequency deterministic agents
  migrated (1 Jun 2026) to native `com.koori.*.plist` launch agents in
  `~/Library/LaunchAgents` on Brad's Mac (speed-to-lead, Xero recon, AR chaser, QS-1/3/4/5,
  subbie RFQ, marketing-outreach, etc.). **These live only on the Mac — not synced, not here.**
- **Layer 2 — Cowork-session SKILL.md prompt tasks.** The judgement/drafting agents
  (`/Scheduled/*/SKILL.md`) run inside Cowork sessions (exec brief, goal-guardian, tender
  retros, content). The `[JARVIS]` digests are the **daily-exec-brief / signoff-queue-digest**
  agents.

## Why it looks like "it doesn't work" — the real reasons
1. **It runs on Brad's Mac, not in the cloud.** If the Mac is asleep / launchd agents aren't
   loaded / it's not running, Layer 1 is silent. Layer 2 needs Cowork sessions to be opened.
2. **The Graph token gates 40+ agents.** The handoff's own P0 (9 Jun) was
   *"GRAPH TOKEN RENEWAL — 2-min fix — unlocks 40+ AI agents."* If that token lapsed, most of
   the fleet can't touch Outlook/SharePoint → they no-op or fail. This is the #1 suspect.
3. **Everything is draft-only by design** ("never send/post/spend/submit unattended — stage
   for Brad"). Output piles into the **sign-off queue**; if Brad doesn't clear it, it reads as
   "nothing happened" even when drafts were produced.
4. **Credential blockers never cleared** (handoff §6): Meta 2FA/BM, Buildxact API key,
   supplier price logins, Anthropic verify. Each stalls its slice of the fleet.

So the digests claiming "8 employees, ~100 artifacts/day" aren't pure theatre — they're the
**brief agents still firing while the working agents are stalled at token + approvals**.

## The fix (mostly on the Mac, not here)
1. **Revive the Graph token** on the Mac (`koori_graph_token_health.py` live refresh) — the
   handoff says this alone unlocks 40+ agents. **Highest-leverage single action.**
2. **Confirm launchd agents are loaded + the Mac is awake/online** (`launchctl list | grep koori`).
3. **Clear the sign-off queue** so produced drafts actually go out (that's the "output" Brad
   isn't seeing).
4. Clear the standing cred blockers (Meta BM, Buildxact key, supplier logins).
5. API spend cap: **raised 15 Jul (Brad)** — no longer the blocker.

## What this session (cloud) can and can't do
- **Can't** reach or repair the Mac launchd fleet or Cowork Layer-2 from here.
- **Can** act as a cloud-side inbox triage/draft aid (the email-admin here) and monitor — but
  that partly **duplicates** the fleet's existing inbox-triage + signoff-digest agents. Better
  to **revive the real fleet** than rebuild it here.

## Next action
Ask Brad: is the **Mac running and are the `com.koori.*` launchd agents loaded**, and **when
did the Graph token last pass its live health check**? That points straight at the fix.
