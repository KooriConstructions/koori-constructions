# Email Employee + Voice/Clone Agents — status & answer

_From the Agent Fleet Inventory (101 agents, 4 Jun 2026) + Master Handoff. This answers
"where are the email-learning / voice / AI-clone employees up to, and if not running, why."_

## The email employee you want ALREADY EXISTS
**`koori-ai-admin-inbox-triage`** — *"Triage/classify inbox, draft brand-voice replies
(drafts only) — every 20 min, Mon–Sat 7am–6pm."* This is exactly the "draft every email in
my voice, drafts-only until it learns me" employee. It's already designed and drafts-only.

So the cloud `koori_email_admin.py` I built this week is, honestly, a **stop-gap
reimplementation of an agent you already own.** The right move is to **revive the real one**,
not run a parallel.

## The "learn my voice" pieces (already in the fleet)
Voice/brand-voice drafting is spread across several agents, all drafts-only:
- `koori-ai-admin-inbox-triage` — brand-voice reply drafts.
- `koori-gbp-review-responder` — "Draft **Brad-voice** GBP review responses."
- `koori-mkt-daily-content-prompt` — content drafts into Toni's inbox.
- The **Cowork `MEMORY.md` auto-memory system** (Master Handoff §intro) is the persistence
  layer that accumulates your voice/decisions across sessions.

## The "AI clone"
Per the Master Handoff, the **"AI Director clone"** is listed as a **build-out / goal**
("agents that run more of the business autonomously") — **not a single running agent yet.**
It's the end-state of the brand-voice agents + MEMORY.md learning your decisions. There is
no standalone "clone" process to check the status of; its progress = how well the voice
agents + memory are trained, which stalls when the fleet is down.

## Why none of it is "running" — same root cause as the whole fleet
`koori-ai-admin-inbox-triage` and the voice agents are **Cowork Layer-2 tasks**. They only
run when:
1. the **Graph token is healthy** (the P0 that gates 40+ agents — prime suspect if lapsed), and
2. the **Cowork schedule / Mac fleet is actually active**.
If the token lapsed or the Mac/Cowork scheduler isn't running, these agents silently stop —
which matches exactly what you're seeing (inbox piling up, "clone" not progressing).
**I can't start or fix them from this cloud session — they live on your Mac / in Cowork.**

> ⚠️ This inventory is dated **4 Jun 2026**. You said JARVIS was "made from another session"
> and there may be newer docs/agents. Anything created after 4 Jun (incl. a dedicated
> "read back through all emails to learn voice" agent) won't be in this list — I can only see
> what's in SharePoint, not the live `launchctl` state on your Mac.

## What actually unblocks all of it (yours — I can't do these from here)
1. **Revive the Graph token** on the Mac (`koori_graph_token_health.py` live refresh) +
   confirm `launchctl list | grep koori`. Unlocks 40+ agents incl. the inbox-triage employee.
2. **Clear the sign-off queue** so the drafts these agents produce actually go out.
3. If you'd rather I run the draft-only email employee **from the cloud** instead of the Mac,
   wire write access (Graph Mail.ReadWrite) and I'll activate `koori_email_admin.py` on a
   schedule — but that duplicates `koori-ai-admin-inbox-triage`, so reviving the Mac one is better.

## Triage status
Caught up on **actionables**: the top ~225 of 972 inbox emails (back to ~13 Jul) contain every
client/supplier/tender item that needs a reply; drafts for all are in
`INBOX-TRIAGE-2026-07-16.md`. The remaining ~750 older emails are the three noise buckets
(JARVIS digests, `qa-test`/`KC-2026-…` self-leads, marketing) — near-zero actionable yield.
