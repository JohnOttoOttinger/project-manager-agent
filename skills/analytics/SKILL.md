---
name: analytics
description: Read Oddtoe's GA4 and Search Console data and answer what actually moved. Use when the user asks how a page is performing, whether published work paid off, what search terms are worth chasing, how many enquiries came in, whether something got indexed, or wants the weekly numbers.
---

# Analytics

Answer from the numbers, not from opinion. Every figure in this skill comes from
a live read of GA4 or Search Console — never from memory, never estimated, and
never from what a previous session said was true.

Scope is **Oddtoe only**. Datalabs has its own GA4 property that is not wired up;
if asked about Datalabs, say so rather than reporting Oddtoe's numbers.

## Before anything else

Run the command. Do not answer analytics questions from the conversation history
or from the ledger — both go stale, and the whole reason this skill exists is
that we were guessing.

    cd skills/analytics
    python3 scripts/report.py <command>

Add `--json` to any command for structured output. Everything is read-only;
no command writes to Google.

## The commands

| Command | Answers |
|---|---|
| `digest [--days 28]` | The weekly picture: totals, enquiries, what moved, new queries, impressions earning no clicks |
| `watch [--days 28]` | Only what crossed an alert threshold. Silent when nothing did |
| `verify <url> [--days 28]` | Did a published page get indexed, crawled, viewed, ranked |
| `queries [--contains X] [--days 90]` | Search terms, optionally filtered |
| `pages [--days 28]` | Most-viewed pages |
| `enquiries [--days 28]` | Conversions plus the landing pages that produced the sessions |
| `snapshot` | Record today's numbers so future digests can show deltas |

## Reading the output honestly

**`enquiries` counts views of the thank-you page.** The GA4 key event
`ThankYouOddtoeClicks` fires on any `page_view` where the URL contains
`thank-you-oddtoe`. Gravity Forms redirects there after a successful submit, so
in practice it means an enquiry — but a bookmark or a stray crawl would also
count. It was created 17 Aug 2026 and **is not retroactive**: zero for earlier
windows means "not measured", not "nobody enquired". The real record of older
enquiries is Gravity Forms → Entries.

**Impressions at deep positions are cheap.** A term sitting at position 30 with
2,000 impressions is not 2,000 near-misses; almost nobody scrolls that far. Rank
matters more than volume. Say so rather than presenting a big number as a big
opportunity.

**A zero-click term is only an opportunity if the searcher could buy.** Oddtoe's
best-ranking pages attract animators looking for representation, not
commissioners. High impressions from the wrong audience are not a win — check
what the query implies about who is typing it before recommending work.

**Snapshots are the only source of deltas.** `digest` compares against the most
recent file in `references/snapshots/`. With no earlier snapshot it reports
current numbers and says so. Run `snapshot` at the end of a digest to set the
next baseline.

## Alert thresholds

Set in `scripts/report.py`, tuned to be quiet:

- a watched term moving **5+ positions** in either direction
- a **new query** arriving with **100+ impressions**
- a watched page whose index verdict is not `PASS`

Everything else waits for the digest. If alerts start firing constantly the
thresholds are wrong — raise them rather than training the user to ignore them.

## The watchlist

`references/watchlist.json` — terms and pages to alert on. Edit it directly when
a new money page ships or a term stops mattering. Adding a page here means
`watch` will check its index status every run.

## After publishing a page

Run `verify <url>` at roughly 7, 14 and 30 days. Before about a week, "not
indexed" usually means "not yet", not "something is wrong" — do not raise it as
a problem that early. Record the outcome in
`skills/money-pages/references/links-ledger.md` so the content work has a
measured result rather than an assumption.

## Answering a question

1. Pick the narrowest command that covers it.
2. Quote real figures. Never round a number into vagueness, and never carry a
   figure across from an earlier answer without re-reading it.
3. Give the interpretation, then the number that supports it — the user wants to
   know what to do, not to be handed a table.
4. If the data does not answer the question, say what is missing and what would
   need to change to measure it.

## Setup this depends on

Read from the repo `.env` (gitignored):

    GOOGLE_APPLICATION_CREDENTIALS  ~/.config/oddtoe/ga-service-account.json
    GA4_ODDTOE_PROPERTY_ID          377681126
    GSC_ODDTOE_SITE_URL             https://www.oddtoe.com/

The service account `analytics-reader@oddtoe-analytics.iam.gserviceaccount.com`
holds Viewer in GA4 and Full in Search Console. It cannot change anything in
either product. A `403` almost always means that access was removed — the error
message says where to restore it.

**The key file must never enter the repo or a chat message.** It lives outside
the tree at mode 600. Reference it by path only.

## Known constraint

Otto's Chrome blocks Google Analytics — on a test load, requests to
`googletagmanager.com` were dropped while Facebook's pixel loaded. He cannot QA
his own analytics in that browser, and Realtime will look empty to him even when
collection is fine. This skill is unaffected: it reads server-side. If he reports
"Realtime shows nothing", that is expected, not a bug.
