# Podcast sourcing pipeline

Built 1 Sep 2026 for the first Oddtoe Business Development press dataset.
Four stages, run in order, from this directory. **No API key and no cost** —
the whole pipeline runs on the free iTunes Search API plus each show's own
RSS feed.

```bash
python3 search_podcasts.py > candidates.json   # 1. find shows by keyword
python3 fetch_feeds.py                         # 2. read each RSS feed
python3 score.py                               # 3. pre-score into a shortlist
python3 build_rows.py                          # 4. emit import rows
```

Then POST the result to the running app:

```bash
curl -X POST http://localhost:3000/api/media-contacts/import -H "Content-Type: application/json" --data @import-podcasts.json
```

## Why it works

`releaseDate` on an iTunes podcast result is the **most recent episode date**,
so the runbook's "still publishing in the last 90 days" filter is free and
needs no extra request. Roughly two thirds of shows found fail it — the
first run saw 1,076 live shows out of 1,441 seen.

Podcast RSS feeds carry `<itunes:owner><itunes:email>`, a **published**
contact address. 798 of 1,058 readable feeds had one. This is the reason the
stream never has to guess an email pattern.

## The two honesty rules, enforced in `build_rows.py`

1. **A platform relay is not a contact.** Addresses at `anchor.fm`,
   `*.acast.com`, `*.libsyn.com` and friends, and anything starting `no-reply`,
   are dropped to empty with the reason recorded — the same treatment a
   catch-all domain gets in the sales-outreach enrichment path. Three of the
   first 33 rows were dropped this way.
2. **`person` is only filled where the feed names a human.** Organisation-
   authored feeds (ABC, BBC, a gallery) keep `person` empty rather than
   inventing a host.

A third caveat is recorded in every row's notes rather than enforced: the
`itunes:owner` address is the feed owner, which is **not** necessarily a
booking address. Treat it as a real published address, not a verified pitch
contact.

## Scoring is a filter, not a verdict

`score.py` keeps three axes separate on purpose — `territory` (does it cover
what Oddtoe makes), `vibe` (playful / funny / curious) and `bookable` (does it
interview anyone). Otto's direction, 1 Sep 2026: the humour is load-bearing,
not a garnish, so a show scoring high on territory and zero on vibe is a
*worse* fit than the reverse. Keyword scoring only narrows 1,076 shows to a
readable ~100; the final pick and every `why_fit` is written by hand.

## Known gap

`search_podcasts.py` can hit HTTP 429 on the free endpoint near the end of a
long run. The first pass lost 5 of 60 term/country pairs that way. `widen.py`
(kept in the session scratchpad, not here) shows the retry-and-merge pattern:
sleep 3–5s between retries and merge on `collectionId`.
