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

---

# Fixes applied — 18 Aug 2026

## Alt text (item 2) — done, and the scan over-counted

**Zero real content images now missing alt across the nine trafficked pages.**

But the original figure was wrong, and the reason matters for the Datalabs
numbers too. Of the 33 "missing alt" images the scan reported on Oddtoe, only
**8 were real**. The rest were:

- **`dummy.png`** — Slider Revolution's lazy-load placeholder for decorative
  slide backgrounds. Empty alt is *correct* for those.
- **Gravatar avatars** — base64 inline, not content images.

**The real fixes were two different problems:**

1. **Seven media items had no `alt_text`.** Written from actually looking at each
   image, not from the filename — which mattered: `Topiary-Sculpture-Oddtoe-1`
   turned out to be a marble cherub bust, not topiary.
2. **Two images had `alt=""` hardcoded in page content**, which overrides the
   media library. Setting the library value alone did nothing for those. Found on
   `/about-oddtoe/investment/` only — a site-wide sweep of every published page
   and post turned up no others.

**Also caught my own mistake:** two near-identical logo files exist, `…temp-01.png`
(id 11675) and `…temp-01-1.png` (id 11677). I set alt on 11677; the page uses
11675. Both now set.

### Rules for the next alt pass

- Exclude `dummy.png` and avatars before counting, or the number is inflated
  three-fold.
- **Media library alt is not authoritative.** A hardcoded `alt=""` in content
  wins. Check the page content too.
- Open the image. Filenames on this site are frequently wrong.

## Neucommerce Experiments — trashed and redirected

Otto's call: remove it, no references.

- Page **24001 moved to Trash** (recoverable; slug auto-renamed to
  `neucommerce-experiments__trashed`).
- **301 added in Redirection: `/neucommerce-experiments/` → `/shop/`.** The page
  was a product-and-article showcase, so the shop is the closest match. No
  internal links to it were found on the homepage, about or work pages.
- At the time of writing the old URL still returns 200 from cache
  (`x-cache: HIT`, `age: 395`) — cached before the trash. It will resolve to the
  301 once that short TTL expires.

**Redirection gotcha, again:** do not verify with a `?cachebuster` query string.
Its default "exact match in any order" query handling means the rule will not
match and the URL appears to 404.

## Item 1 — Datalabs pricing page meta description — done

Live on https://www.datalabsagency.com/data-visualisation-workshop-pricing/

    Private data visualisation workshops in Australia cost $4,600-$7,500 inc GST,
    for up to 12 attendees. Full 2026 pricing, inclusions and formats.

144 characters. Leads with the price because that is what the searcher wants and
it pre-qualifies the click. Figures are the page's own: $4,600 remote half-day
through $7,500 inc GST full day on site, up to 12 attendees included.

**A second problem fixed by the same edit.** Yoast had been auto-generating
`og:description` from the raw page content, so anything sharing this page to
LinkedIn or Slack was previewing a string of `[vc_row full_height="yes"
bg_check="row-background-dark"...` shortcodes. It now carries the real
description.

### Writing Yoast fields by automation — the working recipe

Two earlier attempts failed. What actually works, on a WPBakery page in the block
editor:

1. Open the Yoast sidebar (toolbar button), expand **Search appearance**.
2. The meta description is a **Draft.js contenteditable**
   (`#yoast-google-preview-description-modal`), not an input. Setting `.value`
   or `textContent` does nothing — it needs real typed keystrokes.
3. **Clicking Save does nothing.** Yoast's sidebar edit never marks the post
   dirty, so Gutenberg treats Save as a no-op and `isEditedPostDirty()` returns
   false.
4. Force the save instead:

       wp.data.dispatch('core/editor').savePost()

5. **Verify via `yoast_head_json` in the REST response, not the front-end HTML.**
   The page kept serving a stale copy for a minute after the save was already
   committed — checking the HTML first produced a false "it didn't save".

The equivalent classic-editor approach (setting `#yoast_wpseo_metadesc` by
script, then clicking Update) does **not** work; Yoast's store overwrites it on
submit. That was the failure on the Oddtoe conferences page.
