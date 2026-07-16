#!/usr/bin/env python3
"""
Koori Email Admin — the AI admin that reads every incoming email and drafts a reply
so nothing slips.

Policy (set by Brad, 2026-07-16):
- DRAFT a reply for anything a human must answer (clients, quote leads, suppliers,
  agencies, tenders).
- FLAG (FYI/action note, no draft) for bills, compliance, renewals, payments.
- MARKETING → add to an unsubscribe review list. NEVER auto-click unsubscribe links.
- NEVER auto-send. Every reply lands in Outlook Drafts for Brad to review.

Two ways this runs:
1. REAL-TIME (recommended): a Zapier "New Outlook Email" trigger calls classify() +
   draft_reply() and creates the Outlook draft via Zapier's Outlook action. This is how
   "every email that comes through" gets actioned within minutes.
2. BATCH/DIGEST: a scheduled cloud run pulls the day's mail via Graph, classifies,
   creates drafts, and emails Brad a digest. Good for backfill + a morning summary.

Activation needs (not live until these exist):
- GRAPH_TOKEN with **Mail.ReadWrite** (to create drafts) + Mail.Read.
- ANTHROPIC_API_KEY (and headroom under the monthly spend cap — currently maxed).
- Either the Zapier zap (real-time) or a scheduled runner (batch).
"""

import json
import os
import re
import sys
from datetime import datetime
from typing import Dict, List, Optional

# =============================================================================
# 1. CLASSIFICATION — the reusable core (no external deps, safe to run anywhere)
# =============================================================================

# Senders / patterns that are marketing → unsubscribe review, never a draft.
MARKETING_MARKERS = re.compile(
    r"no-?reply|newsletter|edm\.|marketing@|insider@|announce@|"
    r"info@email\.|hello@recruitshop|investments@fundrise|ads-noreply|"
    r"feedbackemail|hubspotemail|hubspotstarter|mailchimp|campaign",
    re.IGNORECASE,
)

# Transactional/operational senders → FYI flag, not a draft.
FLAG_MARKERS = re.compile(
    r"post\.xero\.com|messaging-service|invoice|receipt|remittance|"
    r"icare\.nsw\.gov\.au|notifications@github\.com|no-reply.*anthropic",
    re.IGNORECASE,
)

# Subjects that signal a real human ask needing a reply.
REPLY_HINTS = re.compile(
    r"\b(quote|RFQ|RFT|tender|enquiry|inquiry|site visit|invitation|"
    r"lead|deposit|invoice due|available|interested|follow[- ]?up|measure)\b",
    re.IGNORECASE,
)

# Possible phishing → flag as suspicious, never draft, never click.
SUSPICIOUS_MARKERS = re.compile(
    r"testflight|hacked asset|verify your account|gpt ads|crypto|"
    r"unusual login|account suspended",
    re.IGNORECASE,
)

# Calendar responses ("Accepted:/Declined:/Tentative:/Canceled:" prefix) are meeting
# RSVPs — NOT a customer accepting a quote/price. Treat as calendar, never a draft.
# (Correction 2026-07-16: "Accepted: Quote - ..." is a booking RSVP, not a sale.)
CALENDAR_RSVP = re.compile(r"^\s*(Accepted|Declined|Tentative|Cancell?ed):", re.IGNORECASE)

# Self-generated / system noise: NDRs, the site's own quote-lead + confirmation emails,
# JARVIS fleet digests, QS-3 scans, SharePoint list dumps. Never a draft; suppress.
SYSTEM_NOISE = re.compile(
    r"^\s*(Undeliverable|Delivery has failed)|New Quote Lead — KC-|"
    r"Your Koori Constructions Quote Request|\[JARVIS\]|QS-3 nightly|"
    r"Renewals expiring in next",
    re.IGNORECASE,
)


def classify(email: Dict) -> Dict:
    """
    Classify one email. `email` = {sender, subject, body_preview, is_reply}.
    Returns {category, priority, reason}.
    category ∈ {reply_needed, flag, marketing, suspicious, ignore}
    """
    sender = (email.get("sender") or "").lower()
    subject = email.get("subject") or ""
    preview = email.get("body_preview") or ""
    blob = f"{subject} {preview}"

    # System/self-generated noise and calendar RSVPs are checked FIRST — they must never
    # be mistaken for a client reply or a quote acceptance.
    if SYSTEM_NOISE.search(subject):
        return {"category": "system", "priority": "low",
                "reason": "self-generated / system notice → file to System, no reply"}
    if CALENDAR_RSVP.search(subject):
        return {"category": "calendar", "priority": "low",
                "reason": "calendar RSVP (meeting accept/decline) — a booking, NOT a quote acceptance"}

    if SUSPICIOUS_MARKERS.search(blob):
        return {"category": "suspicious", "priority": "review",
                "reason": "matches phishing/scam pattern — do not click, verify independently"}

    if MARKETING_MARKERS.search(sender):
        return {"category": "marketing", "priority": "low",
                "reason": "bulk/marketing sender → unsubscribe review"}

    if FLAG_MARKERS.search(sender):
        return {"category": "flag", "priority": "medium",
                "reason": "transactional/compliance → FYI flag, no reply drafted"}

    # From a real person (personal/business domain) OR a subject that asks something.
    looks_human = bool(re.search(r"@(gmail|hotmail|bigpond|outlook|live|"
                                 r"[a-z0-9-]+\.com\.au|[a-z0-9-]+\.gov\.au)", sender)) \
        and not MARKETING_MARKERS.search(sender)
    if looks_human or REPLY_HINTS.search(subject):
        # Priority: deadline/opportunity words bump it up.
        hot = re.search(r"\b(deposit|today|urgent|overdue|by \d|installed by|"
                        r"preferred contractor|tender|site access)\b", blob, re.IGNORECASE)
        return {"category": "reply_needed",
                "priority": "high" if hot else "normal",
                "reason": "human correspondence requiring a reply"}

    return {"category": "ignore", "priority": "low", "reason": "no action detected"}


# =============================================================================
# 2. DRAFT GENERATION — compose a reply (needs ANTHROPIC_API_KEY)
# =============================================================================

DRAFT_SYSTEM_PROMPT = """You are Brad Robinson's email assistant at Koori Constructions
(100% Aboriginal-owned NSW building company; Central Coast / Lake Macquarie / Newcastle /
Hunter). Write a concise, warm, professional reply Brad can send as-is. Sign off:
"Brad Robinson · Koori Constructions". Never invent prices, dates, measurements, or
commitments — if a specific figure is needed, leave a clearly-bracketed [CONFIRM: ...]
placeholder. Keep it short."""


def draft_reply(email: Dict, anthropic_key: str) -> Optional[str]:
    """Generate a draft reply body. Returns text or None on failure."""
    if not anthropic_key:
        print("⚠️  ANTHROPIC_API_KEY missing — cannot generate draft")
        return None
    try:
        import anthropic
    except ImportError:
        print("ERROR: anthropic package required (pip install anthropic)")
        return None

    client = anthropic.Anthropic(api_key=anthropic_key)
    user = (f"From: {email.get('sender')}\n"
            f"Subject: {email.get('subject')}\n\n"
            f"{email.get('body_preview') or email.get('body') or ''}\n\n"
            f"Draft Brad's reply.")
    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=600,
            system=DRAFT_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user}],
        )
        return msg.content[0].text
    except Exception as e:  # spend cap / network / auth
        print(f"⚠️  draft generation failed: {e}")
        return None


# =============================================================================
# 3. OUTLOOK DRAFT CREATION — place reply in Brad's Drafts (needs Mail.ReadWrite)
# =============================================================================

def create_outlook_draft(email: Dict, reply_body: str, graph_token: str) -> bool:
    """
    Create a reply draft in Brad's Outlook Drafts folder (never sends).
    Uses Graph: POST /me/messages/{id}/createReply then PATCH the body.

    TODO(activation): confirm GRAPH_TOKEN has Mail.ReadWrite, then enable the calls
    below. Left gated so this file never sends anything until Brad switches it on.
    """
    try:
        import requests  # noqa: F401
    except ImportError:
        print("ERROR: requests required")
        return False

    # endpoint = f"https://graph.microsoft.com/v1.0/me/messages/{email['id']}/createReply"
    # headers = {"Authorization": f"Bearer {graph_token}", "Content-Type": "application/json"}
    # r = requests.post(endpoint, headers=headers)         # creates a reply draft
    # draft_id = r.json()["id"]
    # patch = f"https://graph.microsoft.com/v1.0/me/messages/{draft_id}"
    # requests.patch(patch, headers=headers,
    #                json={"body": {"contentType": "Text", "content": reply_body}})
    print(f"⚠️  TODO(activation): would create Outlook draft reply to "
          f"{email.get('sender')} — '{email.get('subject')}'")
    return True


# =============================================================================
# 4. ORCHESTRATION
# =============================================================================

def process_inbox(emails: List[Dict], graph_token: str, anthropic_key: str) -> Dict:
    """Run the full policy over a batch of emails. Returns a digest summary."""
    digest = {"drafted": [], "flagged": [], "marketing": [], "suspicious": [],
              "checked_at": datetime.utcnow().isoformat() + "Z", "count": len(emails)}

    for email in emails:
        c = classify(email)
        cat = c["category"]
        subj = email.get("subject", "(no subject)")

        if cat == "reply_needed":
            body = draft_reply(email, anthropic_key)
            if body:
                create_outlook_draft(email, body, graph_token)
            digest["drafted"].append({"subject": subj, "from": email.get("sender"),
                                      "priority": c["priority"]})
        elif cat == "flag":
            digest["flagged"].append({"subject": subj, "reason": c["reason"]})
        elif cat == "marketing":
            digest["marketing"].append({"subject": subj, "from": email.get("sender")})
        elif cat == "suspicious":
            digest["suspicious"].append({"subject": subj, "from": email.get("sender")})

    return digest


def main() -> int:
    graph_token = os.environ.get("GRAPH_TOKEN", "")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")

    print("=== Koori Email Admin ===")
    if not graph_token:
        print("⚠️  GRAPH_TOKEN not set — read/draft against Outlook is disabled.")
    # TODO(activation): fetch unread mail via Graph here and pass to process_inbox().
    # emails = fetch_recent_unread(graph_token)
    emails: List[Dict] = []
    digest = process_inbox(emails, graph_token, anthropic_key)

    print(json.dumps(digest, indent=2))
    print(f"\n✓ Processed {digest['count']} emails: {len(digest['drafted'])} drafted, "
          f"{len(digest['flagged'])} flagged, {len(digest['marketing'])} marketing, "
          f"{len(digest['suspicious'])} suspicious.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
