# Session Index — everything from this session (2026-07-16/17)

Master list of what was produced. All committed to branch
`claude/ai-employees-monitoring-sgj52y` in `/cloud/`. Grouped by area.

## A. Fleet health & the AI-employee system
| File | What it is |
|---|---|
| `AI-EMPLOYEE-STATUS.md` | Fleet audit — recipe miner is a skeleton; nothing produced output; P0/P1 launch path |
| `ai_employee_monitor.py` + `.github/workflows/ai-employee-monitor.yml` | Watchdog that flags WORKING/STALE/SKELETON/DEAD employees; daily red/green |
| `FLEET-REPAIR.md` | Diagnosis: JARVIS = 101 agents on Brad's Mac (launchd) + Cowork; **down since ~14 Jul** (last digest #29); root cause = lapsed Graph token + uncleared sign-off queue + Mac asleep |
| `EMAIL-EMPLOYEE-AND-VOICE-STATUS.md` | The "draft-in-my-voice" employee already exists (`koori-ai-admin-inbox-triage`); the "AI clone" is a build-out goal; all stalled on the token |
| `monitor-status.json` | Machine-readable fleet heartbeat |

## B. Email admin + calendar + notes (the tools)
| File | What it is |
|---|---|
| `koori_admin.py` | Standalone Mac worker: reads email → LLM analyses → drafts reply (never sends) + creates colour-coded calendar events with trades invited. Device-code Graph sign-in |
| `koori_email_admin.py` | Classify-and-draft engine (draft human-needed / flag bills / list marketing / catch phishing) |
| `koori_notes.py` | Record a call/quote → local transcription → structured Koori job note |
| `CALENDAR-SCHEDULER-SPEC.md` | 5-colour Outlook category scheme (Quotes/Trades/Suppliers/Crew/Personal) + event rules |
| `SETUP-ACTIVATION.md` | How to grant Graph Mail.ReadWrite / Calendars.ReadWrite + stand up Zapier real-time + SMS |
| `INBOX-TRIAGE-2026-07-16.md` | Triaged inbox (top ~225 of 972) + 11 ready-to-send drafts + unsubscribe list |

## C. Growth — ads / marketing / sales / advertising
| File | What it is |
|---|---|
| `KLOUD-MEDIA-ADS-ANALYSIS.md` | Competitor teardown (their 23 Meta ads, content model, "Tradie Elevation System" funnel) |
| `META-ADS-PROGRAM-AND-GAPS.md` | Koori's ad state (CPL $46.75 vs <$35, monoculture), what's still to apply, the change-trigger program |
| `META-ADS-BREAKDOWN-AND-EXPANSION.md` | The 2 live ads broken down + expansion matrix to kitchens/granny flats/new builds/etc. |

## D. Team — the hire
| File | What it is |
|---|---|
| `HIRE-RESIDENTIAL-ESTIMATOR.md` | Client-facing Residential Estimator: PD, A-player scorecard, interview questions, comp + $28,200 BRG wage rebate, Seek/HIA ad, Chris Hodder reply |

## E. Live job intel surfaced this session (in chat + triage doc)
- **Thrumster (AHO RFT-2015294):** contract executed, completion 3 Aug; screens critical path; On Time Blinds needs door-width answer; AHO PM OOO till 20 Jul (escalate Tony Todorovski).
- **Green Point (Q1023/Q1036):** deposits $6,933.60 staged for approval; window cancel already replied.
- **Awabakal Medical Centre vinyl (Q10935):** deposit was due; Newcastle Flooring booked 21–22 Jul. Glendale preschool plans in from Donna Smith.
- **Warlga Ngurra (Q1018, 33 Cowper St Wallsend):** Dave/Developing Leaders landscaping quote **$10,670** vs Buildxact allowance turf $3,240 + sandstone $3,360 = **$6,600 → ~$3,100 ex over** (variation; confirm excavation overlap + allowance-vs-fixed).
- **Arcadia Vale (17 Arcadia St):** Bradnams screen install booked 23/6 (order 3675248 / service 3751776).
- **Darkinjung/Ray White (Tabatha):** preferred-contractor onboarding — draft + docs ready.

## The one blocker under everything
The **Graph token on Brad's Mac** — revive it (`launchctl list | grep koori`, run the token/auth
script) to bring the whole fleet (incl. the growth + estimating agents) back to life.
