#!/usr/bin/env python3
"""
Koori AI Admin — standalone worker (runs on Brad's Mac).

Does what Brad asked, in one self-contained script that does NOT depend on the
broken engine token store:
  1. Signs in to Microsoft Graph ONCE (device-code flow; token cached to disk).
  2. Reads recent unread inbox emails.
  3. For each: an LLM analyses it → {category, needs_reply, draft_reply, event}.
  4. Creates a REPLY DRAFT in Outlook (never sends).
  5. If a date/booking is found (trade/supplier/delivery), creates a colour-coded
     calendar event on the Koori Active Jobs calendar, and invites the trade.

NOTHING is sent or auto-accepted. Replies land in Drafts; you review + send.

──────────────────────────────────────────────────────────────────────────────
ONE-TIME SETUP (5 min)
1. Azure app: portal.azure.com → Entra ID → App registrations → your Koori app
   (or New registration, single tenant). Under "Authentication" turn ON
   "Allow public client flows". Under "API permissions → Microsoft Graph →
   Delegated" add: Mail.ReadWrite, Calendars.ReadWrite, User.Read, offline_access
   → Grant admin consent. Copy the Application (client) ID and Directory (tenant) ID.
2. In Terminal:
      export KOORI_CLIENT_ID="<application-client-id>"
      export KOORI_TENANT_ID="<directory-tenant-id>"
      export ANTHROPIC_API_KEY="<your key>"
      pip3 install msal requests anthropic
3. Run:  python3 koori_admin.py
   First run prints a code + URL — sign in as brad@kooriconstructions.com.au, approve.
   The token is cached in ~/.koori_admin_token.json; later runs are silent.

TIP: your existing engine already uses an Azure app — reuse that Client/Tenant ID
(find it with:  grep -rIiE "client_id|tenant" "~/Library/Application Support/KooriEngine").
Just make sure Calendars.ReadWrite is added to its delegated permissions.

Schedule it (every 20 min, business hours) with launchd/cron once it works.
──────────────────────────────────────────────────────────────────────────────
"""

import json
import os
import sys
from datetime import datetime, timedelta, timezone

GRAPH = "https://graph.microsoft.com/v1.0"
SCOPES = ["Mail.ReadWrite", "Calendars.ReadWrite", "User.Read"]
TOKEN_CACHE = os.path.expanduser("~/.koori_admin_token.json")
ACTIVE_JOBS_CALENDAR = "Koori Active Jobs"   # events land here (visible on your main view)

# Category → colour is set once in Outlook (Categorize → New Category). The names
# here MUST match the category names you create so the colour applies.
CATEGORIES = {
    "Quotes": "Blue",
    "Trades": "Green",
    "Suppliers/Deliveries": "Orange",
    "Crew": "Purple",
    "Personal": "Grey",
}

# =============================================================================
# AUTH — device-code flow, token cached to disk (no dependency on the engine)
# =============================================================================

def get_token() -> str:
    import msal
    client_id = os.environ.get("KOORI_CLIENT_ID")
    tenant = os.environ.get("KOORI_TENANT_ID", "common")
    if not client_id:
        sys.exit("Set KOORI_CLIENT_ID (and KOORI_TENANT_ID). See setup notes at top.")

    cache = msal.SerializableTokenCache()
    if os.path.exists(TOKEN_CACHE):
        cache.deserialize(open(TOKEN_CACHE).read())

    app = msal.PublicClientApplication(
        client_id, authority=f"https://login.microsoftonline.com/{tenant}", token_cache=cache)

    result = None
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
    if not result:
        flow = app.initiate_device_flow(scopes=SCOPES)
        print(flow["message"])            # "go to microsoft.com/devicelogin and enter CODE"
        result = app.acquire_token_by_device_flow(flow)

    if cache.has_state_changed:
        open(TOKEN_CACHE, "w").write(cache.serialize())
    if "access_token" not in result:
        sys.exit(f"Auth failed: {result.get('error_description', result)}")
    return result["access_token"]


def _headers(token):
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


# =============================================================================
# LLM — analyse one email → structured action (needs ANTHROPIC_API_KEY)
# =============================================================================

ANALYSE_PROMPT = """You are Brad Robinson's assistant at Koori Constructions (100%
Aboriginal-owned NSW builder; Central Coast/Newcastle/Hunter). Categories: Quotes,
Trades, Suppliers/Deliveries, Crew, Personal.

Given ONE email, return STRICT JSON:
{
 "category": one of Quotes|Trades|Suppliers/Deliveries|Crew|Personal|Ignore,
 "needs_reply": true/false,
 "draft_reply": "Brad's reply, warm+concise, signed 'Brad Robinson · Koori Constructions'.
   Never invent prices/dates/measurements — use [CONFIRM: ...] if unknown. '' if no reply.",
 "event": null OR {
   "title": "Q-ref — scope — who",
   "start": "ISO8601 with +10:00 AEST", "end": "ISO8601",
   "invite_email": "trade/supplier email if the booking is WITH them, else null"
 }
}
Only make an "event" if the email states or confirms a real date/time for a booking,
delivery, trade attendance, or site day. Ignore marketing/newsletters/receipts (category Ignore)."""


def analyse(email: dict, anthropic_key: str) -> dict:
    import anthropic
    client = anthropic.Anthropic(api_key=anthropic_key)
    user = (f"From: {email.get('from')}\nSubject: {email.get('subject')}\n"
            f"Received: {email.get('received')}\n\n{email.get('preview')}")
    msg = client.messages.create(
        model="claude-sonnet-5", max_tokens=900, system=ANALYSE_PROMPT,
        messages=[{"role": "user", "content": user}])
    text = msg.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```")[1].lstrip("json").strip()
    return json.loads(text)


# =============================================================================
# GRAPH ACTIONS — read mail, create reply draft, create calendar event
# =============================================================================

def recent_unread(token, hours=48, top=25):
    import requests
    since = (datetime.now(timezone.utc) - timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ")
    url = (f"{GRAPH}/me/mailFolders/inbox/messages?$top={top}"
           f"&$filter=receivedDateTime ge {since}"
           f"&$select=id,subject,from,receivedDateTime,bodyPreview,isRead")
    r = requests.get(url, headers=_headers(token))
    r.raise_for_status()
    out = []
    for m in r.json().get("value", []):
        out.append({"id": m["id"], "subject": m.get("subject", ""),
                    "from": (m.get("from", {}).get("emailAddress", {}) or {}).get("address", ""),
                    "received": m.get("receivedDateTime"),
                    "preview": m.get("bodyPreview", "")})
    return out


def create_reply_draft(token, message_id, body_text, category):
    import requests
    r = requests.post(f"{GRAPH}/me/messages/{message_id}/createReply", headers=_headers(token))
    r.raise_for_status()
    draft_id = r.json()["id"]
    patch = {"body": {"contentType": "Text", "content": body_text}}
    if category in CATEGORIES:
        patch["categories"] = [category]
    requests.patch(f"{GRAPH}/me/messages/{draft_id}", headers=_headers(token), json=patch).raise_for_status()
    return draft_id


def _calendar_id(token, name):
    import requests
    r = requests.get(f"{GRAPH}/me/calendars?$select=id,name", headers=_headers(token))
    r.raise_for_status()
    for c in r.json().get("value", []):
        if c.get("name", "").strip().lower() == name.strip().lower():
            return c["id"]
    return None   # falls back to default calendar


def create_event(token, ev, category):
    import requests
    payload = {
        "subject": ev["title"],
        "start": {"dateTime": ev["start"], "timeZone": "AUS Eastern Standard Time"},
        "end": {"dateTime": ev["end"], "timeZone": "AUS Eastern Standard Time"},
        "categories": [category] if category in CATEGORIES else [],
    }
    if ev.get("invite_email"):
        payload["attendees"] = [{"emailAddress": {"address": ev["invite_email"]}, "type": "required"}]
    cal_id = _calendar_id(token, ACTIVE_JOBS_CALENDAR)
    endpoint = f"{GRAPH}/me/calendars/{cal_id}/events" if cal_id else f"{GRAPH}/me/events"
    requests.post(endpoint, headers=_headers(token), json=payload).raise_for_status()


# =============================================================================
# MAIN
# =============================================================================

def main() -> int:
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    if not anthropic_key:
        sys.exit("Set ANTHROPIC_API_KEY.")
    token = get_token()

    emails = recent_unread(token)
    print(f"Scanning {len(emails)} recent emails...\n")
    drafted = events = 0
    for e in emails:
        try:
            a = analyse(e, anthropic_key)
        except Exception as ex:
            print(f"  skip (analyse error): {e['subject'][:50]} — {ex}")
            continue
        cat = a.get("category", "Ignore")
        if cat == "Ignore":
            continue
        if a.get("needs_reply") and a.get("draft_reply"):
            create_reply_draft(token, e["id"], a["draft_reply"], cat)
            drafted += 1
            print(f"  ✏️  draft [{cat}] → {e['subject'][:55]}")
        if a.get("event"):
            try:
                create_event(token, a["event"], cat)
                events += 1
                who = a["event"].get("invite_email") or "no invite"
                print(f"  📅 event [{cat}] {a['event']['title'][:40]} (invite: {who})")
            except Exception as ex:
                print(f"  event error: {ex}")

    print(f"\n✓ Done: {drafted} reply drafts, {events} calendar events. "
          f"Review drafts in Outlook before sending. Nothing was sent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
