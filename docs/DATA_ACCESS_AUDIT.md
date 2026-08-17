# What the agent can actually see

Audited 17 Aug 2026 by testing, not by assuming. Re-test before trusting this —
access changes and credentials get revoked.

## First, a distinction worth making

Otto's list mixed two different things:

- **Data sources** make the agent smarter about the business. They answer
  "what happened, what's working, what's it worth."
- **Production tools** let the agent make things. They don't tell it anything.

Adobe, Midjourney and Runway are production tools. Connecting them is about
output, not intelligence. Xero, Stripe, Mailchimp and Gravity Forms are data.

## And what "automatic" honestly means

The agent does not hold a standing copy of the business in its head. Between
sessions it remembers only what is written to this repo or the memory files.
"Automatic" means **it can fetch the answer on demand without Otto doing
anything** — not that the data is always loaded.

Three tiers:

| Tier | Meaning |
|---|---|
| **Automatic** | Stored credential, agent queries whenever it needs to |
| **Assisted** | Needs Otto's logged-in browser; agent can drive it while he's present |
| **Manual** | No API path; Otto exports or pastes |

---

## Live today

| Source | Tier | What it gives | Verified |
|---|---|---|---|
| **GA4 (Oddtoe)** | Automatic | Users, sessions, pages, events, enquiries | 17 Aug — numbers matched the UI exactly |
| **Search Console** | Automatic | Queries, clicks, impressions, positions, index status | 17 Aug — live query + URL inspection |
| **WordPress ×2** | Automatic | Pages, posts, media, categories; publish and edit | Used all session |
| **Apify** | Automatic | Scraping and enrichment actors | 3 workflows call it; credential bound |
| **DataForSEO** | Automatic | Keyword and domain research | Wired into `paid-domain-research` |
| **Gmail** | Assisted | Otto's inbox — searched for the Baobab invoice this session | Used 17 Aug |

### Known WordPress limits

- `my-product` (portfolio) has **no REST endpoint** — browser only
- **Yoast fields are not REST-writable**; only `_acf_changed` and `footnotes` exposed
- Menu editing needs `edit_theme_options`; the content agent is an Editor
- XML-RPC returns 403

---

## Cheap to add, high value

### 1. Gravity Forms REST — the cheapest unlock

**Not enabled.** `/wp-json/` exposes 28 namespaces, none of them `gf`. Turning it
on (Forms → Settings → REST API) makes the **144 entries** programmatically
readable instead of scraped from the admin table.

Directly enables the Business Development CRM: auto-classify each enquiry on
arrival, surface only the real briefs, draft the stock replies. Also gives the
historical enquiry record that GA4 cannot, because the key event only started
collecting today.

### 2. Xero — the single most valuable thing on the list

This is the one that changes what the agent can say. Right now the app can
measure enquiries and nothing beyond them. Xero closes **enquiry → job → money**,
which is exactly what blocked the Themes ROI discussion: without it, a theme can
report cost per enquiry but never return.

Gives invoices, payments, revenue by client, expenses, P&L. Feeds Investment and
Bookkeeping, which are both currently active tabs with no financial data behind
them.

Setup is heavier than Google's: OAuth2 with user consent and refreshing tokens,
not a service-account key. Roughly an hour, once.

### 3. Mailchimp — easy, once the Oddtoe account exists

Plain API key. Campaigns, opens, clicks, list growth, unsubscribes. Pairs with
GA4 to answer "did that campaign produce enquiries or just opens." Worth wiring
as soon as the Oddtoe audience is created.

### 4. Stripe — easy if it carries real volume

Restricted read-only key, straightforward. Payments, customers, revenue. Overlaps
Xero; if invoicing runs through Xero, Stripe is confirmation rather than new
information. Worth asking which one actually holds the truth.

---

## Production tools, not data

| Tool | Reality |
|---|---|
| **Adobe** (Premiere, After Effects, Illustrator) | Desktop apps. Project files are not a data source. An Adobe MCP exists for Express/Firefly work but needs authorising, and it makes things rather than reporting them |
| **Midjourney** | No official API — Discord-driven. Not cleanly automatable |
| **Runway** | Has a generation API. Useful for content workflows later; tells the agent nothing about the business |

Worth revisiting when the goal is *producing* content at volume. Not now, when
the goal is knowing what is working.

---

## Recommended order

1. **Gravity Forms REST** — minutes of work, unlocks the CRM and the enquiry history
2. **Xero** — the only path to revenue, and the missing half of every ROI question
3. **Mailchimp** — when the Oddtoe account exists
4. **Stripe** — if it holds truth Xero doesn't
5. Everything else on demand

## Standing rule

Every credential goes in `.env` (gitignored) or a file outside the repo,
referenced by path. Read-only scopes wherever the API offers them. The agent has
no business holding write access to money.

---

## Update — Gravity Forms REST enabled (17 Aug 2026)

**Done.** `gf/v2` namespace now registered and returning data.

- Enabled at Forms → Settings → REST API
- The existing WordPress app password does **not** work: `otto-content-agent` is
  an Editor with no `gravityforms_*` capabilities, so it gets `rest_forbidden`.
  Rather than widen that account's role, a scoped key was created instead.
- **Read-only** GF v2 API key, description "Analytics agent - read entries",
  bound to the Oddtoe user. Stored in `.env` as `GF_ODDTOE_CONSUMER_KEY` /
  `GF_ODDTOE_CONSUMER_SECRET`. It cannot write, delete or modify anything.

### What it returns

| | |
|---|---|
| Form 1 "Oddtoe Core Form" | **144 entries** |
| Form 3 "Oddtoe Comic Inquiry" | 0 entries |
| Date range | 2023-06-01 → 2026-08-15 |
| Per entry | `date_created`, `ip`, field values, `form_id`, `id` |

**Dates were not visible in the admin table** — this is genuinely new. Enquiry
volume by month shows a clear ramp: 1 in March 2026, then 6, 9, **13**, 12 —
June and July are the busiest months on record, roughly triple the winter rate.
That trend was invisible before today.

Endpoint shape:

    GET /wp-json/gf/v2/forms
    GET /wp-json/gf/v2/forms/1/entries?paging[page_size]=200

Basic auth with the consumer key and secret.
