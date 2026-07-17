# Koori Meta Ads — what's still to apply + the optimisation program

_Compiled 2026-07-17 from SharePoint marketing research (05-Ad-Creative-Library,
the 4 Jun creative-rotation refresh, the Toronto before/after pack). Meta ad tools were
offline when this was written — the live numbers below are the last verified state (4 Jun);
re-pull today's figures once Meta access is back._

## 1. Current state of your ads (last verified 4 Jun 2026)
- **Account** `299674387566012` · **Page** `108846045545067` · **Lead Form** "Koori
  Residential Reno Quote — v1".
- **Live:** campaign `120245899937730190` → Cold ad set `120245899937740190` ($50/day) →
  one incumbent ad `120245899937750190` = **Toronto bathroom, after-only, price/timeframe
  hook ($19,990 / 12 days)**.
- **Performance (30d):** CTR 3.20% but **decaying** (3.93%→2.71%), **frequency 2.77**,
  **CPL A$46.75** (target <$35), Meta **under-spending the $50/day cap ~28%**.
- **Diagnosis:** single-creative monoculture — 1 ad, 1 cold ad set, **no retarget, no
  lookalike**. ⚠️ Ads run on Meta independent of the Mac fleet and haven't been actively
  managed since — **re-check the incumbent is still live and not burning at a fatigued CPL.**

## 2. The research that already exists (done — just not live)
- `05-Ad-Creative-Library.md` — campaign types, creative templates A–F, A/B rules, spend
  ramp, monthly review, UTM tracking.
- `10-Campaign-Blueprint` — the **4-creative × Cold/Retarget/Lookalike** structure (designed).
- `12-Meta-Ads-Concept-Briefs` / `13-Merewether-Deck-Pergola-Ad-Creative-Pack` — video
  concepts + locked copy (HERO: "Deck + pergola. 6 days. Fixed price.").
- **Toronto before/after pack** — 41 media vision-labelled; 3 before/after pairs + the best
  transformation Reel (`IMG_1930.MOV`) shortlisted and staged.
- `Reports/meta-ads-refresh-2026-06-04.md` — the fatigue diagnosis + rotation plan.

## 3. WHAT WE STILL NEED TO APPLY (research → live) — priority order
1. **Break the monoculture — launch the staged rotation** into the existing Cold ad set
   (no new budget): HERO Merewether deck+pergola video, **Toronto BEFORE/AFTER split
   (Pair 1)** + transformation Reel. Proof/before-after creative is the missing lever —
   converts ~1.5–2× vs beauty-shot ads.
2. **Build the Retarget ad set ($10/day)** — needs the **Meta Pixel live** on Linktree/site.
   Warm audience = the single biggest CPL drop.
3. **Build the Lookalike ad set ($5/day)** — needs a **Xero past-customer export** uploaded
   as the seed audience. (HubSpot was dropped 14 Jun — use Xero/SharePoint, not HubSpot.)
4. **Copy fixes across all captions:** "**within the hour**" speed-to-lead (not 24h),
   price-led headlines, **suburb-level geo** (Toronto, Wangi, Belmont, Warners Bay…).
5. **Fix tracking/form flow:** the old UTM→**HubSpot** path is dead (HubSpot gone) — re-point
   lead flow to **brad@ + SharePoint register + GoHighLevel**; confirm the Meta Lead Form
   still lands somewhere live.
6. **Clear the creation blockers (page-config, NOT a token issue):** accept the Page's
   **Lead-gen Terms** (`leadgen_tos_accepted=false` blocks lead ad-set creation) + install
   the **Pixel**. Note: the Meta MCP can read performance but **can't create lead-form
   creatives** — so building these stays **manual in Ads Manager** (Toni/Brad hands-on).

## 4. THE ADS PROGRAM — signals for when to change creative / form / audience
Watch each signal; when it hits the trigger, take the action. This is the decision tree.

| Signal | Healthy | Change trigger | Action |
|---|---|---|---|
| **CPL (cost/lead)** | < $35 | $35–50 amber · **> $50 for 7d** red | Replace that creative; if ALL creatives high → fix offer/form, not creative |
| **CTR (outbound)** | > 2% | decaying **>25% peak→now**, or < 1.5% | Rotate in fresh creative (fatigue) |
| **Frequency (7d)** | < 2.5 | **> 2.5–3** | New creative and/or widen the audience |
| **Hook rate / 3-sec video views** | > 30% | < 25% | Re-cut the **first 3 seconds** (the hook) |
| **Daily spend pacing** | ~100% of cap | Meta under-spends **>20%** | Creative/audience too narrow → refresh or broaden |
| **Lead → qualified %** | most usable | high volume, **junk quality** | **Change the FORM** — add qualifying Qs (budget, timeframe, job type) |
| **Lead volume** | steady | too few | **Simplify the form** (fewer fields) / stronger hook + offer |
| **Cost per booked quote** | set a baseline | rising | The real KPI — trace which creative/audience drives booked jobs, not just leads |

**When to change the FORM specifically:** lots of leads but few turn into booked quotes →
form is too loose, add 2–3 qualifying questions. Too few leads → form too heavy, cut fields
to one-tap. **If CTR is fine but CPL is high, the leak is the form/offer — not the creative.**

**Cadence:**
- **Daily (automated):** `koori-meta-ads-monitor` already checks CPL/CTR/fatigue (alerts if
  CPL >$60 or CTR drops >20% WoW) — it's down with the fleet; **revive it**.
- **Weekly:** creative-rotation review — pause anything with frequency >2.5, launch the next
  bench concept (#7 Just Moved In, #6 Granny Flat, #5 Forever Home).
- **Test rhythm:** 2 variants, **7 days minimum**, **≥30% better** wins and replaces the
  loser; refresh creative every ~2–3 weeks regardless of winner.
- **Monthly (60 min):** spend · CPL · lead→qualified · ROI → scale winners, kill losers.

## 5. Blockers to clear first (yours)
- Meta Business Manager / 2FA + ad-account access (handoff §6).
- Page: accept **Lead-gen Terms**; install the **Pixel**.
- Revive the fleet (Graph token) so `koori-meta-ads-monitor` runs the daily watch again.

**Bottom line:** the strategy, creative and structure are already built and sitting staged.
The gap is 100% *execution* — launch the rotation, add retarget + lookalike, fix the copy +
form flow, and run the weekly change-triggers above. Nothing here needs more research.
