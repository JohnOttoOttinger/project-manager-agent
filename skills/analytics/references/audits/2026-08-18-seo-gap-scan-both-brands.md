# SEO / GEO gap scan — both brands — 18 Aug 2026

**506 URLs fetched and parsed** from the content sitemaps (posts, pages,
my-product, product). Taxonomy, author, quiz and certificate archives excluded.
Checked for: meta description, image alt text, figure captions, and structured
data.

Oddtoe is ranked by **real Search Console traffic**. Datalabs is not — see the
access note at the end.

---

## The numbers

| | Oddtoe | Datalabs |
|---|---|---|
| Pages scanned | 55 | 447 |
| **Missing meta description** | **7 (13%)** | **107 (24%)** |
| Content images | 817 | 7,668 |
| **Images with no alt text** | **33 (4%)** | **716 (9%)** |
| Pages with ≥1 un-alted image | 21 (38%) | 197 (44%) |
| `<figure>` blocks / no caption | 32 / 6 | 238 / **148** |
| Pages carrying `FAQPage` schema | **13** | **3** |

Oddtoe is in materially better shape on every measure — the work of the last few
days shows.

---

## Highest-value fixes, Oddtoe (ranked by 180-day impressions)

22 trafficked pages have a gap, sitting behind **111,570 impressions**.

| Impressions | Page | Gap |
|---|---|---|
| 80,543 | /artist-designer/prop-designer-maker/ | 1 image no alt |
| 7,433 | /studio/generative-ai-animator/ | 1 image no alt |
| 5,640 | / (homepage) | 1 image no alt |
| 5,002 | /about-oddtoe/ | 2 images no alt |
| 4,580 | /experiential-design-techniques-examples/ | **no meta description** + 1 image |
| 2,001 | /about-oddtoe/investment/ | 4 images no alt |
| 1,449 | /artist-designer/roboticist/ | 1 image no alt |
| 848 | /artist-designer/ | 3 images no alt |
| 347 | /shop/ | **no meta description** |

Oddtoe's alt-text problem is shallow — usually one image per page, 4% overall.
A short pass clears it.

---

## Highest-value fix overall: the Datalabs pricing page

**`/data-visualisation-workshop-pricing/` has no meta description and no
og:description.** Verified directly, not inferred.

This is the money page published on 14 August, link-passed, and submitted for
indexing. Google is writing its own snippet for the page Otto most wants to
convert on. `/neucommerce-experiments/` (1,871 words) is in the same state.

---

## Datalabs: the translations are the problem

| Language | Type | Pages | No description | Images | No alt |
|---|---|---|---|---|---|
| **Arabic** | page | 107 | **39** | 1,665 | 148 |
| **German** | page | 102 | **36** | 1,596 | 146 |
| English | page | 92 | 21 | 1,645 | 76 |
| English | blog post | 64 | 3 | 1,145 | 112 |

**75 of the 107 missing descriptions are on German and Arabic pages.** The
translation workflow carried the body copy across but not the Yoast fields —
those pages go to market with no snippet at all, in languages where Otto has
least ability to spot it.

The English blog archive is the opposite: descriptions are almost all present
(3 missing of 64), but the alt text is not.

---

## The GEO gap is bigger than the SEO one

**Datalabs has FAQPage schema on 3 pages. Oddtoe has 13.**

Oddtoe got there this week. Datalabs has had none of that work, and it is the
brand with the higher-value transaction — corporate training workshops against
art commissions. Every "how much does data visualisation training cost", "what
is data storytelling" style question is one Datalabs could be answering in an
AI result and currently is not.

**148 of 238 `<figure>` blocks on Datalabs have no caption.** Captions are read
by both search and AI extraction, and they are among the most-read text on a
page.

---

## Recommended order

1. **Datalabs pricing page meta description.** One field, on the page most
   likely to convert. Also `/neucommerce-experiments/`.
2. **Oddtoe alt text**, top 9 trafficked pages. About 15 images total.
3. **Datalabs German and Arabic descriptions** — 75 pages. Bulk work, but they
   are currently invisible in two markets.
4. **Datalabs FAQ modules**, using the pattern proven on Oddtoe this week.
   Highest GEO return of anything here.
5. Datalabs figure captions — 148 of them.

---

## Access note

The `analytics-reader` service account can read **only** `https://www.oddtoe.com/`
in Search Console. Datalabs cannot be ranked by traffic, which is why its
priorities above are inferred from page type and word count rather than measured.

**Fix:** add `analytics-reader@oddtoe-analytics.iam.gserviceaccount.com` as a
user on the Datalabs property at
https://search.google.com/search-console/users?resource_id=https%3A%2F%2Fwww.datalabsagency.com%2F

That is a one-minute change and it would let this scan rank Datalabs the same
way — which matters, because Datalabs has four times the gaps and no measurement
behind any of them.

## Method

`skills/analytics/references/audits/` — scan script fetched each URL, parsed the
`<head>` for title/description/canonical/robots, counted `<img>` tags pointing at
`/wp-content/uploads/` (theme chrome excluded), counted `<figure>` blocks without
`<figcaption>`, and collected `@type` values from JSON-LD. Findings on the three
highest-value pages were re-verified by direct fetch.
