# AI Admin — Activation Runbook (#2 Graph draft access · #3 Zapier real-time + SMS)

The classify-and-draft engine (`koori_email_admin.py`) is built and tested. To make it
run 24/7 and place drafts in your Outlook, two things need **your** account/admin consent
— I can't provision them from here. Below is exactly what to do; where I need a value
back from you, it says **→ send me**.

---

## #2 — Graph token with Mail.ReadWrite (so the admin can create Outlook drafts)

The current Outlook connection is **read-only**. Creating drafts needs the
`Mail.ReadWrite` scope. Two routes:

### Option A — fastest (Microsoft 365 admin, ~10 min)
1. Go to **portal.azure.com → Microsoft Entra ID → App registrations**.
2. Open the app already used for Koori's Graph access (or **New registration** →
   name "Koori Email Admin", single tenant).
3. **API permissions → Add a permission → Microsoft Graph → Delegated →** add
   `Mail.ReadWrite`, `Mail.Read`, `offline_access`, `User.Read`.
4. Click **Grant admin consent** (the button must go green).
5. **Certificates & secrets → New client secret** → copy the value.
6. **→ send me**: the **Client ID**, **Tenant ID**, and confirm the secret is stored as
   the `GRAPH_TOKEN` / client-credential secret in the runner's environment (GitHub
   Actions secret or Zapier connection). Never paste the secret into chat — put it in the
   secret store; just tell me it's set.

### Option B — via Zapier's Outlook connection (no Azure work)
If you wire #3 below, Zapier's Microsoft Outlook app already holds a `Mail.ReadWrite`
token when you connect your account and grant the "create draft" permission — so #2 is
satisfied automatically by #3. **Recommended** unless you want the standalone cloud runner.

---

## #3 — Zapier: real-time drafting + SMS capture

### Zap A — "Every incoming email → drafted reply" (real-time)
1. In **Zapier → Create Zap**.
2. **Trigger:** Microsoft Outlook → **New Email** (Inbox). Connect your
   brad@kooriconstructions.com.au account (this grants the mailbox access, incl. drafts).
3. **Action (filter, optional):** skip if sender matches marketing / `qa-test@` /
   `[JARVIS]` (keeps drafts clean — mirrors the engine's policy).
4. **Action:** **Code by Zapier (Run Python)** → paste the body of `classify()` +
   `draft_reply()` from `koori_email_admin.py`; input = the email's sender/subject/body;
   set `ANTHROPIC_API_KEY` in the Zap's env. Output = category + draft text.
5. **Action:** Microsoft Outlook → **Create Draft Reply** (only when category =
   `reply_needed`), body = the draft text. **Never** "Send Email" — draft only.
6. Turn the Zap on. Now every real email gets a draft within minutes; you review + send.
   **→ send me**: confirm the Zap is on, and I'll tune the filters against your real senders.

### Zap B — "Every text/SMS → into the admin"
Pick the channel that matches your phone:
- **Simplest:** set your mobile to **forward SMS to brad@kooriconstructions.com.au**
  (most Android + iPhone-via-shortcut can). Then Zap A already covers texts.
- **Or dedicated:** Zapier → Trigger **SMS by Zapier / Twilio / ClickSend → New SMS**;
  Action = same Code step → then either create an Outlook draft or a task.
  **→ send me**: which SMS service your business number uses (Twilio? carrier? none yet?),
  and I'll give you the exact zap.

### Bonus Zap C — de-noise the inbox (recommended)
Outlook rule / Zap: move `[JARVIS]` digests to a **"Fleet"** folder and `qa-test@` /
`Undeliverable` to **"System"** — so your inbox shows only real people. This alone will
cut the "I miss things" problem hugely.

---

## What happens once #2 + #3 are in
- Real-time: every genuine email → a ready draft in your Outlook Drafts.
- Marketing → flagged for the weekly unsubscribe review (never auto-clicked).
- Bills/compliance → a short FYI so nothing operational slips.
- The fleet monitor flips **email-admin** from DEAD → WORKING once it records drafts.

## Still blocking everything: the Anthropic spend cap
Your API is paused at the **$1,400** monthly cap (inbox alert 15 Jul). Drafting needs the
API — **raise the cap** or none of the above (or your JARVIS fleet) can generate text.
