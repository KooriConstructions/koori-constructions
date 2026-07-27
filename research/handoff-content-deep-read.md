# Handoff: Deep-Read the Source Content (Podcasts, Books, Articles, Posts)
**For a fresh session to pick up — 27 July 2026**

## The ask
Brad wants a full close-read/analysis of every source turned up in the two research briefs below — not just search-snippet summaries, but actually going through podcast transcripts, the book, long-form articles, and social content, then breaking down what's said.

## Why this session couldn't do it
Confirmed by direct test (not just agent reports): **WebFetch returns HTTP 403 on every live site tried** in this environment (news publishers and small company sites alike) — this matches what all 10 research agents hit independently across this whole project. **The Wayback Machine workaround is also disabled** in this environment ("Claude Code is unable to fetch from web.archive.org"). On top of the blocking:
- **Podcasts are audio** — no transcription tool was available in this session's toolkit. Unless a host publishes a written transcript, there's nothing to fetch even if blocking weren't an issue.
- **Justin Gehde's book** is commercial copyrighted content — full-text reproduction/analysis needs a legitimately obtained copy (Audible/Kindle/print), not a web fetch.
- **Instagram/LinkedIn posts** are largely login-gated/JS-rendered and were not reliably retrievable either.

**What the next session should try that this one couldn't:** a different fetch tool/proxy configuration (if WebFetch is blocked there too, try an MCP-provided fetch tool if one is connected — the tool description for WebFetch itself says to prefer an MCP fetch tool when available, since it "may have fewer restrictions"); actually purchasing/opening Gehde's book via Audible/Kindle if Brad has or gets access; checking whether YouTube's auto-caption track is reachable (would need a dedicated transcript extraction approach, not a generic page fetch); and checking podcast platforms directly (Spotify and some Apple Podcasts episodes now auto-generate transcripts in-app — worth checking if those are exposed via a URL this session couldn't reach).

## Prior work already done — two documents in this repo
1. **`research/builder-to-developer-playbook.md`** — the master brief: strategy answer (PPOR-as-development-site), the ladder, Graya deep-dive, Rich List founders, tradie-to-developer stories, modern vertically-integrated cohort, the "gatekept" small-developer playbook, and NSW Hunter/Central Coast/Lake Macquarie planning rules.
2. **`research/top10-wealth-lists-and-hiring-milestones.md`** — round 2: definitive top-10 wealthiest developers and top-10 wealthiest builders (by founder wealth), hiring-milestone research (when did each founder make key hires), and a deep content sweep identifying the best individual pieces of content per founder.

Both were built from search-result synthesis (WebSearch), not full page reads — so there's real headroom for a deeper pass if the fetch/transcript problem can be solved.

## Priority source list for the deep read

### Highest priority — podcasts/video (need transcripts)
- **Rob Gray, "$1 Billion Dollar Property Developer Blueprint" — Everything Property podcast, ep. 111.** buzzsprout.com/2146744/episodes/17152866
- **"Graya: How Two Brothers Are Quietly Dominating Australian Property" — Bothsides Podcast, ep. 147.** podcasts.apple.com/ca/podcast/ep-147-graya-how-two-brothers-are-quietly-dominating/id1585830750?i=1000768441472 — also on YouTube.
- **The Urban Developer × STAC Capital, "From Blueprint to Build: GRAYA's Growth Story" — 3-part video series.** theurbandeveloper.com/articles/from-blueprint-to-build-graya-s-growth-story-with-stac-capital (this is the single most tactically useful piece identified across all research — covers actual debt/finance structuring)
- **"EP39: A Chat with Rob Gray from Graya" — BuildHer Collective podcast.** buildhercollective.com.au/podcast/ep39-a-chat-with-rob-gray-from-graya-building-a-budget-with-your-builder/
- **Duayne Pearce's "Level Up" podcast** — youtube.com/@LiveLifeBuild — any recent episodes on cashflow, PAC process, business systems. Start with whatever's most recent/highest-viewed.
- **"272 – Mastering the Art of Property Development ft. Tim Willing" — The Perth Property Show.** theperthpropertyshow.podbean.com/e/272-expert-developer-interview-ft-tim-willing/ / youtube.com/watch?v=q8Ps08vpeG4
- **"3 Pathways to Property Development" — Rob Flux on The Property Couch, ep. 570.** thepropertycouch.com.au/ep570-3-pathways-property-development-rob-flux/
- Justin Gehde's **Property Developer Podcast** (propertydeveloperpodcast.com) — 250+ episodes; prioritise any where Gehde discusses his own first deal (20-townhouse project).

### The book
- **Justin Gehde, *Become a Million Dollar Property Developer: An Insider's Guide to Wealth, Fulfilment and Glory*** (2023). Available Audible/Kindle/print. His own first deal — 20 townhouses, $1M+ profit — is the spine of the book. This is the single most relatable case study identified across both rounds of research given Brad's scale.

### Long-form written profiles (should be directly fetchable if the blocking issue is solved)
- graya.com.au/our-story
- theurbandeveloper.com/articles/good-design-has-to-pass-the-barbecue-test-graya
- theurbandeveloper.com/articles/development-a-team-sport-graya-stac-capital
- eco-outdoor.com/en-us/outdoor-design/two-brothers-making-big-impact-property-industry
- satterley.com.au/about/company-story/
- perrongroup.com.au/history
- propertycouncil.com.au/news/ross-robertson-looks-back-on-40-years-with-perron-group
- ariaproperty.com.au/our-story/
- mosaicproperty.com.au/who-we-are/leadership-team/
- fortis.com.au/my-path-to-pallas-house/
- villawoodproperties.com.au/our-story/how-we-started/
- bgc.com.au/our-history/
- hutchinsonbuilders.com.au/history
- thirdigroup.com.au/about/ and primeresi.com/we-are-definitely-in-acquisition-mode-at-the-moment-in-conversation-with-third-is-ron-dadd-luke-berry/

### Social content
- Instagram: instagram.com/graya, instagram.com/rob.graya, instagram.com/willingperth — design-led post captions/content strategy is itself part of what Brad asked to understand (how they use social media as a sales funnel).
- LinkedIn: au.linkedin.com/in/grayatm, au.linkedin.com/in/andrew-gray-graya, Justin Gehde's book-launch post (linkedin.com/posts/justin-gehde-5723068).

## What "analyse and break down" should mean once the content is accessible
Not just re-summarise — extract:
1. Specific dollar figures, dates, and deal structures mentioned (not paraphrases)
2. Direct quotes on financing mechanics (how they actually got each deal funded)
3. Direct quotes on mistakes/regrets
4. Anything said about hiring/staffing decisions and timing (the gap identified in round 2 — most public sources don't cover this, so any direct mention in these specific pieces is high-value)
5. Cross-check against claims already made in the two existing briefs — confirm, correct, or add nuance rather than duplicating

## Full raw source list from all ten research agents (for completeness/backup)
The two existing documents' own "Sources" sections contain the full per-topic URL lists gathered in this project (Graya, Rich List founders, tradie-to-developer stories, modern cohort, financing/legal playbook, NSW planning rules, top-10 wealth lists, hiring milestones, content sweep). Pull from those directly rather than re-searching from scratch — the discovery work is done; what's missing is the close-read.
