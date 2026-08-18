# Datalabs missing meta descriptions — 18 Aug 2026

Baseline: the 448-URL live scan (`scan_datalabs.json`, 18 Aug). **108 URLs have no
meta description** — 26 EN, 41 DE, 41 AR. An earlier count of "448 missing" was
mine reading the wrong key (`description` instead of `desc`); the scan was correct.

## Search Console access — resolved

The service account could not read Datalabs because the only property was
`sc-domain:datalabsagency.com`, verified by someone else's DNS record. Otto is a
delegated full user there, not an owner, so he cannot grant access on it.

Fix taken 18 Aug: verified `https://www.datalabsagency.com/` (URL-prefix) as a
separate property. It **auto-verified from an HTML file already on the server** —
no DNS change needed. `analytics-reader@oddtoe-analytics.iam.gserviceaccount.com`
added at Full. Confirmed readable via the API.

**Caveat:** this property only holds data for 18 Apr – 3 Jun 2025 (47 days), then
nothing. Fresh data starts accruing from verification day. The continuous history
lives on the domain property, which the API still cannot reach. If that history
matters, Otto should add his own DNS TXT record for `datalabsagency.com` — that
makes him a *co-owner* of the existing domain property (multiple owners are
allowed) and the service account can then be added there too.

`gsc_query()` and `gsc_inspect()` in `ga_client.py` now take an optional `site=`
argument; they defaulted to Oddtoe and were hard-wired to one property.

## The write channel is the bottleneck

Yoast's fields are **not writable over REST** — verified on page 35565, whose
`meta` exposes only `_acf_changed` and `footnotes`. Yoast's bulk editor is also
gone: `admin.php?page=wpseo_tools&tool=bulk-editor` redirects to the tools index
on Yoast 27.3.

That leaves the per-page browser recipe (SKILL.md rule 5) at roughly three
actions per page — about 320 actions for 108 pages. **Decision pending with Otto:**
add a small WPCode snippet registering the two Yoast meta keys for REST, which
turns the whole job into one scripted pass and can be deleted afterwards.

## Not descriptions — these should leave the index

Writing a description for these would help nothing; they are not answers to any
search. Recommend `noindex,follow`.

| URL | Why |
|---|---|
| `/shop-2/cart/` `/shop-2/checkout/` `/shop-2/my-account/` `/my-account/` | Transactional, user-specific. Currently indexable with no robots meta. |
| `/organizer-dashboard/` `/venue-dashboard/` | Logged-in dashboards |
| `/submit-organizer-form/` `/submit-venue-form/` | Form endpoints |
| `/footer/` | A theme part rendering as a page |
| `/our-work/52511/` | Bare attachment/portfolio ID, 29 words |
| `/refund_returns/` | Terms of sale; standard to noindex |
| `/event-organizers/` `/event-venues/` | **Broken** — both render the raw shortcode `[event_organizers]` / `[event_venues]` unprocessed. Fix or trash, don't describe. |

`/neucommerce-experiments/` is already slated for Trash + redirect (Otto, 18 Aug).

`/2016/11/09/data-visualization-conferences-2017/` needs no description — it
already canonicalises to the 2026–2027 post. A 301 would be firmer than a
canonical hint, and would collapse a decade of links onto the live page.

`/department-of-treasury-finance-tasmania/` is a **client materials page**
(workshop packs and workbooks for a 2023 engagement), not marketing. Recommend
noindex rather than a description.

`/data-arts-factory-at-jacks-magazine/` is stale — it advertises spaces "opening
in February 2021". Describe it only if the offer still stands.

## EN descriptions to write (9)

Yoast target is roughly 120–156 characters. Counts shown.

| Page | Description | Chars |
|---|---|---|
| `/2026/01/27/data-storytelling-workshop-providers-what-to-look-for-when-hiring/` | How to choose a data storytelling workshop provider: what to ask, what good looks like, and the questions that separate real trainers from slide decks. | 150 |
| `/2026/03/25/data-visualization-conferences-2026-2027/` | The best data visualization and design conferences in 2026 and 2027 — dates, cities, and what each is actually good for. Updated through the year. | 145 |
| `/data-visualization-training-workshops-webinars/tableau-dashboard-design-workshop/` | A hands-on Tableau dashboard design workshop covering eight advanced techniques — so your team builds dashboards that drive decisions, not just report. | 150 |
| `/analysts-toolkit/` | The Analyst's Toolkit: courses, templates and visual guides that help analysts find sharper insights and tell better stories with data. | 133 |
| `/product/analysts-toolkit/` | Buy the Analyst's Toolkit — a bundle of courses, templates and visual guides for analysts who want stronger design and data storytelling skills. | 142 |
| `/designing-explainable-decisions-with-ai/` | A hands-on workshop for government and corporate teams: turn AI-assisted decisions into clear, human-friendly explanations backed by real governance. | 148 |
| `/data-ai-training-workshops/` | Data and AI training workshops from Datalabs — data storytelling, creative PowerPoint presentations, and designing explainable AI decisions. | 138 |
| `/our-work/` | Portfolio of Datalabs data visualization work: dashboards, infographic reports, interactive maps and animated data videos, built for clients worldwide. | 150 |
| `/data-arts-factory-at-jacks-magazine/` | The Data Arts Factory: ten creative studio and industrial spaces on the Maribyrnong River in Melbourne, for designers, makers and data professionals. | 148 |

The page and product versions of the Analyst's Toolkit are deliberately different
— identical descriptions on two indexed URLs is the problem being solved, not a
shortcut.

## DE / AR (82)

Same pages, translated. These are written in German and Arabic, not translated
mechanically from the English above — a meta description is ad copy and reads as
machine output otherwise. Blocked on the same write-channel decision.

Note the DE and AR sets contain their own junk that should be noindexed rather
than described, mirroring the English list: `/de/fusszeile/`, `/de/mein-konto/`,
`/de/shop/wagen/`, `/de/shop/kasse/`, `/ar/تذييل/`, `/ar/حسابي/` and the rest of
the cart/checkout/dashboard family, plus template leftovers like
`/de/vorlage-fuer-die-finanzseite-platzhalter-bitte-nicht-veroeffentlichen/`
("template, placeholder, please do not publish") which is live and indexable at
1,477 words.
