# DataForSEO sweep — Datalabs service seeds — 24 Aug 2026

Run through the API Playground in Otto's signed-in session (no credentials handled).
Location: **Australia** (2036) · Language: English · Function: `keyword_suggestions`
(plus one `related_keywords`). **Total cost $0.09** across 5 calls.

## Volumes (monthly, Australia)

| Seed | Top term | Vol | CPC | Competition | Suggestions found |
|---|---|---|---|---|---|
| power bi training | training on power bi | **880** | $8.66 | MEDIUM | 508 |
| power bi training | **power bi training** | **720** | $8.59 | MEDIUM | |
| power bi training | microsoft power bi training | 210 | $8.63 | LOW | |
| dashboard design | **dashboard design** | **390** | $5.04 | **LOW** | 660 |
| dashboard design | power bi dashboard design | 140 | $11.82 | **LOW** | |
| infographic report | infographic report | 40 | — | LOW | 42 |
| data visualization style guide | (seed itself) | 10 | — | — | 5 |
| data visualisation training | (seed itself) | 10 | $12.62 | MEDIUM | 1 |

## What this says

**The site is optimised for language nobody searches.** Datalabs' own positioning terms —
"data visualisation training" (10/mo), "data visualization style guide" (10/mo), "infographic
report" (40/mo) — have almost no Australian demand. The terms with real demand are the plain
product names: **Power BI training (720–880/mo)** and **dashboard design (390/mo, LOW competition)**.

**This is the blind spot GSC could never show.** Search Console reports only queries the site
already appears for; across 180 days "power bi training" produced **8 impressions total**, because
Oddtoe/Datalabs effectively does not rank for it at all. The demand was invisible, not absent.

## Actions

1. **NEW PAGE — Power BI training.** `/power-bi-training/` returns **404 (open)**. 720/mo, CPC $8.59.
   Otto already delivers this service; there is no dedicated page for it. Highest-confidence new-page
   candidate found for Datalabs by any method so far. Passes the near-duplicate test: nothing ranks.
2. **FIX — `/dashboard-design/` 301-redirects to a GERMAN post** (`/de/2024/09/15/dashboard-design-pro-tipps/`).
   The highest-volume dashboard term in Australia (390/mo) sends English AU traffic to German content.
   Repoint it at an English dashboard-design page.
3. **fix-existing — power bi dashboard design.** 140/mo LOW competition; `/power-bi-dashboard-design/`
   already exists and ranks pos 8.4 with 0 clicks. CTR/positioning work, not a new page.
4. **Do NOT build** style-guide or infographic-report pages for search reasons — the demand is not there.
   (They may still earn their place as sales collateral; that is a different argument.)

Method note: `keyword_suggestions` returns long-tail terms *containing* the seed and is the right
discovery call. `related_keywords` only reads Google's "searches related to" box and returned a
single term — do not use it for discovery.
