# Pricing — Datalabs Agency (single source of truth)

**Scope: Datalabs Agency only.** Oddtoe pricing is a separate exercise (see brands.md). This file is internal reference, not public content — but everything in it must be safe to publish except where marked.

**Updated: 12 August 2026.** Workshop rate card APPROVED by Otto 12 Aug 2026, derived from realized prices in 14 years of Xero invoice history (analysis: `data/private/pricing-analysis-2026-08-12.md` — private, gitignored, never cite publicly).

All future content mentioning any Datalabs price MUST match this file. If a price changes, change it HERE first, then propagate (see Consistency rules at the bottom).

## A. Approved price list (canonical)

### Workshops (private corporate training) — APPROVED 12 Aug 2026

Two-tier model: a **public rate card** (what the website, content, and quotes anchor on) and an **internal floor** (quotes never go below it). The gap between them is spent ONLY via named concessions — never as an unexplained discount.

**Public rate card (AUD, inc GST — the only workshop prices that may appear in public content):**

| Offer | Public price | Includes |
| --- | --- | --- |
| On-site full day | **$7,500** | Up to 12 attendees, materials, Melbourne metro |
| On-site half-day (4 hrs) | **$5,200** | Up to 12 attendees, materials, Melbourne metro |
| Remote full day | **$6,200** | Up to 12 attendees, Zoom/Teams/Webex |
| Remote half-day (4 hrs) | **$4,600** | Up to 12 attendees, Zoom/Teams/Webex |

**Internal floor (NEVER publish; quotes never below):** on-site full day $5,900 · on-site half $4,700 · remote full $5,500 · remote half $4,200.

**Named concessions (the only way a quote moves from list toward the floor; the reason appears on the quote):** multi-workshop series (10–15% off session 2+, matching historical bundle behaviour) · returning client · government/not-for-profit rate · flexible/off-peak scheduling · trimmed scope (no customised materials). Concessions come off session fees only — travel and per-attendee surcharges are never discounted.

**Group-size tiers:**

1. **Up to 12 attendees** — included in the rate card price.
2. **13–20 attendees** — **+$250 per extra attendee per day** (floor $200; a 2022 engagement cleared $250/head). Still far cheaper for the client than public classes at $395–$622/head.
3. **21+ attendees** — do NOT surcharge; **split into cohorts**, each priced as its own session with the series concession on session 2+. Protects workshop quality (interactivity degrades past ~20) and earns more than surcharging.
4. **Enterprise programs** (multiple workshops × locations, e.g. the historical Adidas/Lockheed-scale SOWs): price as (sessions × rate card) + per-head surcharges + travel per location; volume concession capped at 15% and applied to session fees only; anchor the conversation on the program total, not the day rate.

**Other up-factors:** heavy customisation (client data, branded materials) — billed as pre-work at the hourly rate (see Consulting); travel beyond Melbourne metro at cost + travel-day rate.

- Public range for articles/FAQs: **"$3,000 to $8,000 per workshop day for corporate groups"** stays valid — the public rate card sits inside it.

**Rationale (12 Aug 2026, from Xero realized prices):** Public prices = ~75th percentile of what clients actually paid 2023–26 (remote half-days realized $2,300–$5,243, median $3,865 ex-GST; on-site full days $4,968–$5,387 ex-GST), sanity-checked against the $7,500-ex-GST full days held consistently through 2017–19 and the $4,900-ex-GST in-person half-day sold in 2026. Floor = realized 2023–26 medians. $7,500 inc GST positions above Excelerator BI's $6,000 comparable as the design/storytelling specialist; at 12 attendees it is $625/head — at Nexacu's top public rate but private and customised.

### Online courses

| Item | Sale (AUD) | Regular (AUD) |
| --- | --- | --- |
| An Introduction to Data Visualization and Storytelling Course | **$127** | $183 |
| Designing Great Dashboards Course | **$127** | $183 |

Canonical per Otto, 12 Aug 2026. The **$83.00** displayed on the LearnDash course pages is STALE — see Fix actions.

### Consulting

- **Data visualization consulting (Otto, 1-hour blocks, max 4 hours): $250/hour.** Approved 12 Aug 2026.
- **Workshop pre-work/customisation** (data research, incorporating client data/brand into materials): billed hourly. OPEN — Xero shows this leaked out at $75–$122/hr in 2024–25; a $180/hr floor is recommended but Otto has not yet ruled. Until he does, don't publish a pre-work rate; quote per engagement.
- The WooCommerce add-on that handled hourly rates/booking is no longer paid for, so the product cannot take hourly bookings — see Fix actions. Until the product is fixed, content may state the $250/hour rate but must direct people to the contact form, not the product page.

### Digital products (shop prices as published — canonical as-is)

| Product | Tier | Price (AUD) |
| --- | --- | --- |
| Power BI Templates | Standard / Premium / Business | $1,119 / $1,469 / $1,969 |
| Power BI Theme & Style Guide | Standard / Premium / Business | $425 / $1,063 / quoted individually |
| Analyst's Toolkit bundle | — | $978 (shown against $3,396 regular) |

## B. Audit — every price Datalabs published anywhere (as found 12 Aug 2026)

| Where | What it says | Status |
| --- | --- | --- |
| Shop `/product/power-bi-templates/` | $1,119 / $1,469 / $1,969 (Standard/Premium/Business), on sale from $1,402 base | Canonical |
| Shop `/product/power-bi-theme-json-style-guide/` | $425 / $1,063, Business quoted; on sale from $638 base | Canonical |
| Shop `/product/introduction-data-visualization-course/` | $127 sale / $183 regular | Canonical |
| Shop `/product/dashboard-training-designing-great-dashboards-course/` | $127 sale / $183 regular | Canonical |
| Shop `/product/analysts-toolkit/` | $978 sale / $3,396 regular | Canonical (but see Fix actions on the regular price) |
| Shop `/product/data-visualization-consultant/` | No price; store API returns $0/"Free" | BROKEN — rate is $250/hr, add-on lapsed |
| LearnDash `/courses/introduction-to-data-visualization/` | $83.00 | STALE |
| LearnDash `/courses/designing-great-dashboards/` | $83.00 | STALE |
| Article 27 Jan 2026 "Data Storytelling Workshop Providers…" FAQ | "Costs generally range from $3,000 to $8,000 per workshop day for corporate groups" | Canonical public range |
| Workshop pages (e.g. Designing Great Business Dashboards) | "It depends… by the number of attendees or on a per workshop basis, whichever is cheaper. Contact us for an estimate." Also "between 5 and 20 attendees per workshop" | Kept, but see Fix actions re group size |
| All other pages/articles checked (training hub, style-guide pages, 2024 training article, etc.) | No prices published | — |

## C. Competitor benchmarks (published prices only; all verified 12 Aug 2026)

| Provider | Offer | Price (AUD) | Source |
| --- | --- | --- | --- |
| Excelerator BI (Melbourne) | 1-day private Power BI workshop, face-to-face, max 10 people | $6,000 inc GST ($4,000 instruction + $2,000 on-site delivery) | exceleratorbi.com.au/product/1-day-mel/ |
| Nexacu | Public 1-day classes, per person | $395 (Beginner) – $622 (top courses) | nexacu.com.au/microsoft-power-bi-training-courses/ |
| Lumify Work | Power BI Fundamentals, 2 days, per person | $1,677.50 inc GST (~$839/day) | lumifywork.com/en-au/courses/power-bi-fundamentals/ |
| StoryIQ (AU) | Data Storytelling for Business, 2 half-days, per person | $649 (disc. from $699) | storyiq.com/au/ |
| StoryIQ (AU) | Data Storytelling for Leaders, half-day, per person | $385 (disc. from $415) | storyiq.com/au/ |
| ANZSOG | Data & Storytelling for Policy, 2 × 3-hr online sessions, per person | $2,050 inc GST | anzsog.edu.au/learning-and-development/courses/data-and-storytelling/ |

Do not add benchmarks without a live source URL and verification date. Never estimate a competitor's unpublished price. (IAPA's data storytelling workshop page was unreachable on 12 Aug 2026 — no price recorded.)

## D. Inconsistencies found & fix actions (WordPress edits — Otto or a future authorised session)

1. **Course price conflict ($83 vs $127/$183).** LearnDash course pages show $83; Woo products show $127/$183. Canonical is $127/$183. Fix: update or hide the LearnDash price display so only the Woo price appears.
2. **Consultant product broken.** Purchasable at $0/"Free", no rate shown, and the hourly-booking add-on has lapsed. Fix: convert the product page to an enquiry (contact form) stating $250/hour in 1-hour blocks (max 4), or re-instate booking. It must not remain buyable at $0.
3. **Permanent-sale framing.** Every product is "on sale"; the Analyst's Toolkit shows 71% off a $3,396 regular price that exceeds the sum of its components' regular prices. Fix: either set honest regular prices or drop the sale framing — permanent fake discounts are a credibility risk with both customers and AI assistants citing the shop.
4. **Group-size mismatch.** Workshop pages say "between 5 and 20 attendees"; the approved rate card includes up to 12, with 13–20 as a per-head surcharge and 21+ split into cohorts. Fix: when workshop/pricing pages are next edited, describe group size consistently with section A ("includes up to 12 attendees; larger groups accommodated").

## E. Consistency rules (binding on all future content)

1. **This file wins.** Any price in any Datalabs draft must match section A. If Otto quotes a different number in conversation, update this file first, then write the content.
2. **Change propagation order:** (1) this file → (2) the 27 Jan 2026 article FAQ if the $3k–$8k range changes → (3) shop/LearnDash pages → (4) any other page listing prices (per section B). All WordPress changes land as drafts per banned.md rule 4.
3. **Public content may quote the PUBLIC rate card and/or the $3,000–$8,000/day range — NEVER the internal floor, concession percentages, or the Xero analysis.** The floor and concession rules exist for quoting, not publishing. AI assistants will repeat whatever price the site publishes, so published numbers must always be the public rate card verbatim.
4. **Published prices only** in benchmarks — source URL + verification date required; re-verify before reusing a benchmark older than ~6 months.
5. **GST:** all workshop/consulting figures are inc GST. Say "inc GST" whenever a workshop or consulting price appears in public content.
6. **No blending:** this file is Datalabs-only. Oddtoe pricing gets its own file when Otto provides projection/installation ranges.
7. All banned.md rules apply (no home address, no personal mobile, no invented figures).
