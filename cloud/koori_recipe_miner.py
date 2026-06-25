#!/usr/bin/env python3
"""
Koori Recipe Miner — Cloud Runner
Runs Friday 5pm AEST. Reads Job Pipeline, mines completed jobs into KRV0 recipes + KCI0 catalogue.
6-step workflow per koori-recipe-miner SKILL.md.

Required env:
- ANTHROPIC_API_KEY (for prompt orchestration)
- GRAPH_TOKEN (for SharePoint Job Pipeline read)
- REPO_ROOT (workspace root)
"""

import json
import os
import sys
from datetime import datetime
from typing import Optional, Dict, List

# =============================================================================
# 1. GRAPH CLIENT — Read Job Pipeline from SharePoint
# =============================================================================

def read_job_pipeline(graph_token: str) -> List[Dict]:
    """
    Read Job Pipeline list from SharePoint.
    Filter: Status='Invoiced' (clean, complete jobs ready to mine).
    Return: [{"Q-ref": "Q-1234", "customer": "Smith", "status": "Invoiced", ...}, ...]

    TODO: Wire up Graph API call once SharePoint list ID confirmed.
    For now, return mock data or read from local SharePoint export.
    """
    try:
        import requests
    except ImportError:
        print("ERROR: requests library required. pip install requests")
        return []

    # TODO: Replace with real Graph API call
    # endpoint = "https://graph.microsoft.com/v1.0/sites/{site-id}/lists/{list-id}/items"
    # headers = {"Authorization": f"Bearer {graph_token}"}
    # response = requests.get(endpoint, headers=headers)
    # items = response.json().get("value", [])

    # For now, mock return
    print("⚠️  TODO: Wire up Graph API to read Job Pipeline from SharePoint")
    return []


# =============================================================================
# 2. XERO + BUILDXACT INTEGRATION — Read cost data
# =============================================================================

def read_xero_invoices(q_ref: str) -> Optional[Dict]:
    """
    Read Xero invoices for a given job (Q-ref).
    Return: {"total_cost": 5432.10, "labour": 2100, "materials": 2800, "subs": 532.10, ...}

    TODO: Wire up Xero API or read from exported file.
    """
    # TODO: Implement Xero API read or file-based lookup
    print(f"⚠️  TODO: Wire up Xero data read for {q_ref}")
    return None


def read_buildxact_quote(q_ref: str) -> Optional[Dict]:
    """
    Read Buildxact quote for a given job.
    Return: {"quoted_value": 6000, "items": [...], "recipes_used": []}

    TODO: Wire up Buildxact API or read from exported file.
    """
    # TODO: Implement Buildxact API read or file-based lookup
    print(f"⚠️  TODO: Wire up Buildxact data read for {q_ref}")
    return None


# =============================================================================
# 3. 6-STEP WORKFLOW — Per-job recipe mining
# =============================================================================

def step1_job_decomposition(q_ref: str, quote: Optional[Dict], actuals: Optional[Dict]) -> Dict:
    """Step 1: Break job into sub-scope elements (bathroom, kitchen, etc.)."""
    return {
        "q_ref": q_ref,
        "subscopes": [],  # TODO: Extract from quote + actuals
        "raw_data": {"quote": quote, "actuals": actuals}
    }


def step2_variance_analysis(decomp: Dict) -> Dict:
    """Step 2: Compute estimate vs actual variance. Flag if >10%."""
    return {
        "subscopes_clean": [],  # TODO: Filter >10% variance
        "subscopes_noisy": [],  # TODO: Subscopes with >10% delta (don't promote yet)
        "variance_details": {}
    }


def step3_krv0_draft(variance: Dict) -> List[Dict]:
    """Step 3: Draft KRV0 recipe rows (one per clean subscope)."""
    # TODO: Generate KRV0 naming (KR-{category}-{subscope}-{tier}-V1)
    return []


def step4_kci0_draft(krv0_rows: List[Dict]) -> List[Dict]:
    """Step 4: Draft KCI0 catalogue items (new line items not in catalogue)."""
    # TODO: Identify missing items, generate KCI0 naming (KC-{category}-{item}-{unit})
    return []


def step5_rate_card_flags(variance: Dict, actuals: Dict) -> Dict:
    """Step 5: Flag rate-card updates needed (wet-area, bathroom, fence, day-rates)."""
    # TODO: Cross-reference actuals against published rate cards
    return {
        "wet_area_updates": [],
        "bathroom_allowance_updates": [],
        "fence_rate_updates": [],
        "day_rate_updates": []
    }


def step6_output_package(q_ref: str, krv0: List[Dict], kci0: List[Dict],
                        rate_flags: Dict, actuals: Dict) -> Dict:
    """
    Step 6: Assemble output package ready for Outlook draft to Brad.
    Return markdown blocks + Brad's action items.
    """
    package = {
        "q_ref": q_ref,
        "section1_summary": f"Q {q_ref} — {len(krv0)} recipes, {len(kci0)} new items",
        "section2_krv0_drafts": krv0,
        "section3_kci0_additions": kci0,
        "section4_rate_card_proposals": rate_flags,
        "section5_reference_updates": {},  # TODO: Generate reference file edits
        "section6_brad_actions": []  # TODO: Prioritized action list
    }
    return package


# =============================================================================
# 4. OUTLOOK DRAFT OUTPUT — Create email to Brad (not sent)
# =============================================================================

def create_outlook_draft(packages: List[Dict], graph_token: str) -> bool:
    """
    Create Outlook draft email to brad@kooriconstructions.com.au with all recipe outputs.
    Never auto-send — Brad reviews + approves before import.

    TODO: Wire up Graph API email draft creation.
    """
    try:
        import requests
    except ImportError:
        print("ERROR: requests library required")
        return False

    if not packages:
        print("No recipes to output.")
        return True

    subject = f"Recipe Miner — {len(packages)} jobs ({datetime.now().strftime('%Y-%m-%d')})"
    body = _build_email_body(packages)

    # TODO: Replace with real Graph API call
    # endpoint = "https://graph.microsoft.com/v1.0/me/messages"
    # payload = {"subject": subject, "bodyPreview": body[0:100], "body": {"contentType": "HTML", "content": body}}
    # headers = {"Authorization": f"Bearer {graph_token}", "Content-Type": "application/json"}
    # response = requests.post(endpoint, json=payload, headers=headers)

    print(f"⚠️  TODO: Wire up Outlook draft creation for {subject}")
    print(f"\nDraft body preview:\n{body[0:500]}...")
    return True


def _build_email_body(packages: List[Dict]) -> str:
    """Generate HTML email body from packages."""
    html = "<html><body>"
    for pkg in packages:
        html += f"<h2>{pkg['section1_summary']}</h2>"
        html += f"<p>KRV0 recipes: {len(pkg['section2_krv0_drafts'])}</p>"
        html += f"<p>KCI0 additions: {len(pkg['section3_kci0_additions'])}</p>"
    html += "</body></html>"
    return html


# =============================================================================
# 5. DEDUP LOGIC — Track mined jobs
# =============================================================================

def load_mined_jobs(state_path: str) -> set:
    """Load set of Q-refs already mined."""
    try:
        with open(state_path, 'r') as f:
            state = json.load(f)
            return set(state.get("mined_jobs", []))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()


def save_mined_jobs(state_path: str, q_refs: set) -> None:
    """Save mined jobs to state file."""
    state = {
        "mined_jobs": sorted(list(q_refs)),
        "last_run": datetime.utcnow().isoformat() + "Z"
    }
    with open(state_path, 'w') as f:
        json.dump(state, f, indent=2)


# =============================================================================
# 6. MAIN ORCHESTRATION
# =============================================================================

def main():
    repo_root = os.environ.get("REPO_ROOT", ".")
    graph_token = os.environ.get("GRAPH_TOKEN", "")

    state_path = os.path.join(repo_root, "cloud", "recipe-miner-state.json")

    print("=== Koori Recipe Miner ===")
    print(f"Start: {datetime.utcnow().isoformat()}Z")

    # Step 1: Read Job Pipeline
    print("\n[1] Reading Job Pipeline...")
    jobs = read_job_pipeline(graph_token)

    if not jobs:
        print("No jobs ready to mine.")
        return 0

    # Step 2: Load previously mined jobs (dedup)
    mined = load_mined_jobs(state_path)
    print(f"[2] Loaded {len(mined)} previously mined jobs")

    # Step 3: Process each new job
    packages = []
    newly_mined = set()

    for job in jobs:
        q_ref = job.get("Q-ref", "UNKNOWN")

        if q_ref in mined:
            print(f"   SKIP {q_ref} (already mined)")
            continue

        print(f"   PROCESS {q_ref}...")

        # Read cost data
        xero_data = read_xero_invoices(q_ref)
        bx_data = read_buildxact_quote(q_ref)

        if not xero_data or not bx_data:
            print(f"   SKIP {q_ref} (missing data)")
            continue

        # Run 6-step workflow
        decomp = step1_job_decomposition(q_ref, bx_data, xero_data)
        variance = step2_variance_analysis(decomp)
        krv0 = step3_krv0_draft(variance)
        kci0 = step4_kci0_draft(krv0)
        rate_flags = step5_rate_card_flags(variance, xero_data)
        package = step6_output_package(q_ref, krv0, kci0, rate_flags, xero_data)

        packages.append(package)
        newly_mined.add(q_ref)
        print(f"   MINED {q_ref} → {len(krv0)} recipes, {len(kci0)} items")

    # Step 4: Output Outlook draft
    if packages:
        print(f"\n[3] Creating Outlook draft for {len(packages)} jobs...")
        success = create_outlook_draft(packages, graph_token)
        if success:
            newly_mined_updated = mined | newly_mined
            save_mined_jobs(state_path, newly_mined_updated)
            print(f"[4] Saved {len(newly_mined)} new jobs to state")
            print(f"\n✓ Recipe miner completed: {len(packages)} jobs → Outlook draft")
            return 0

    print("\n✓ Recipe miner completed: 0 jobs ready")
    return 0


if __name__ == "__main__":
    sys.exit(main())
