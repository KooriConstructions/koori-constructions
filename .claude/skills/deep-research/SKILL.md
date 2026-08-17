---
name: deep-research
description: Run a full deep-research sweep for Koori Constructions — live/upcoming building & carpentry opportunities (tenders, EOIs, panels, subcontract packages, grants-as-partnering plays) across government portals, councils, Indigenous channels, head contractors and aggregators, with verified decision-makers and a ranked, decision-ready report. Use whenever Brad invokes /deep-research, says "deep research", "find opportunities", "scan the portals", "what tenders are open", "who do I talk to at [org]", asks for a pipeline/opportunity report, or wants decision-makers + LinkedIn for a target list. Also use for deep research on any other business question (suppliers, competitors, partners) — the method generalises; only the source universe changes.
---

# Deep Research — Koori Constructions

Produce a decision-ready opportunities report Brad can act on the same week: what's open, what it's worth, when it closes, who controls it, and why Koori wins it. This is capture research, not browsing — every line in the output should let Brad either bid, register, or contact a named human.

## Client context (bake into every relevance judgement)

Koori Constructions Pty Ltd — Brad Robinson, sole director. 100% Aboriginal-owned, Supply Nation registered, NSW unrestricted builder licence 477499C. Base: NSW Central Coast; service area Central Coast · Lake Macquarie · Newcastle · Hunter (Maitland, Cessnock, Port Stephens, Singleton). Works: new builds, renovations, extensions, granny flats, insurance, maintenance, NDIS, commercial, government, defence, education, aged care, child care, health — all carpentry and building construction. Scale: suits packages/jobs roughly $50k–$5M; panels and recurring maintenance are worth more than one-off bids of equal value.

Strategic moat: federal Indigenous Procurement Policy (IPP — Exemption 16, Mandatory Set-Aside $80k–$200k) and NSW Aboriginal Procurement Policy (APP). Since 1 Jul 2026 the 51%+ Indigenous-ownership rule applies — Brad is 100%, so he clears every threshold. Any opportunity where Indigenous ownership is scored, set aside, or fills a head contractor's RAP/IPP target ranks higher than its face value suggests.

## Execution

1. **Timestamp the run** (AEST) at the top of the report — tenders close continuously, so the report is only valid as of its search time.
2. **Read the previous report first** if one exists (repo `Handoff/` folder, or a file Brad uploads). The new run is a delta on it: re-verify its open items, carry forward what's still live, mark what closed, and hunt what it flagged as gaps. Never silently drop a previously-reported open opportunity.
3. **Sweep the source universe** in `references/source-universe.md`. Cast wider than the list — it is examples plus known-good URLs, not a boundary. If parallel subagents are available, fan out one per source family; otherwise sweep inline, government portals first (they gate the most value).
4. **Expect blocked sources.** Many portals are JS-rendered, login-gated, or blocked by the environment's egress proxy. Try WebFetch; on failure fall back to WebSearch snippets (aggregator listings often mirror portal items). Never guess what a blocked page contains — record it in the "blocked" list so Brad can pull it logged-in.
5. **Capture per opportunity:** title, reference/ID, issuing agency or head contractor, scope (building/carpentry relevance), value or band if shown, region, release date, close date+time, portal + direct link, Indigenous set-aside / IPP/APP eligibility, and named contact officer if visible.
6. **Find the decision-maker(s)** per opportunity — procurement lead, estimator, contracts manager, project manager, or BDM. Verification rules below are non-negotiable.
7. **Score and rank** (rubric below), write the report (format below), save it, and commit/push if working in the repo.

## Honesty rules (non-negotiable)

Real, current, verifiable only. These rules exist because a single fabricated tender reference or LinkedIn profile poisons Brad's outreach and his trust in the whole report.

- Every opportunity, reference number, date, name, and URL must have been actually seen on a fetched page or in a live search result. No exceptions, no "probably exists".
- A close date sourced from an aggregator card rather than the primary portal gets flagged **"reconfirm on portal"**.
- A LinkedIn URL may only be reported if the URL itself appeared in a search result or fetched page, matching name + company. Grade every person: **VERIFIED** (URL seen, name+title+company match) · **PARTIAL** (name+title from a non-LinkedIn source, e.g. company site, ZoomInfo listing, news) · **UNCONFIRMED — needs check**. When no human is findable, name the role and the verified contact inbox/phone instead, and say so.
- Conflicting sources (e.g. two different titles for one person) → report the conflict, don't pick one.
- Close every report with: sources reached and read, sources blocked/gated, and the honest count of each.

## Scoring rubric

**Fit (0–5):** trade relevance (carpentry/building/fitout/maintenance) + region + band suitability for Koori's scale + Indigenous-eligibility leverage. **Urgency (0–5):** how soon it closes or how time-sensitive registration is. **Score = Fit + Urgency /10**, ranked highest first. Recurring panels and registration channels score Fit as if won repeatedly — a maintenance panel at rates beats a same-sized one-off.

## Report structure

ALWAYS use this exact template, saved as `Handoff/Building-Opportunities-Deep-Research-<YYYYMMDD>.md` in the repo (destination on Brad's Mac: `/Users/bradrobinson/Documents/Claude/Handoff/`):

```
# Building & Carpentry Opportunities — Deep Research
Prepared for / search timestamp / research path used
## Read this first — honesty & coverage notes
## Scoring rubric
## MASTER TABLE — ranked by fit + urgency
| # | Opportunity | Agency/HC | Scope | Est. value | Region | Close/status | IPP/APP? | Score | Link |
## TOP 5 TO ACT ON THIS WEEK  (owner + suggested next step + by-when)
## PER-OPPORTUNITY DETAIL  (why Koori fits / angle in · decision-maker(s) with verification grade)
## STANDING CHANNELS TO LOCK IN  (panels, registrations, prequalification — the things that gate everything)
## SOURCES & METHOD  (reached vs blocked, counts, timestamp)
## MENTOR'S NOTES  (capture strategy: panels compound, moat-not-subsidy framing, one question to sit with)
```

After saving: hand the top-ranked bid-type items toward `koori-bid-no-bid-gate` before any proposal hours commit, and named humans toward `koori-outreach-orchestrator` for first contact. Changed decision-maker or opportunity facts from a previous run get called out explicitly ("was X, now Y").

## Follow-ups worth offering (not auto-running)

- Re-run on a schedule (the daily/weekly portal scan) with delta-only reporting.
- A gated-portal pull list for Brad's logged-in session (EstimateOne, buy.nsw, VendorPanel, Supply Nation member board).
- Outreach drafts for the top 3 named humans via koori-outreach-orchestrator.
