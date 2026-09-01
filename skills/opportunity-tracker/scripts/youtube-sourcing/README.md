# YouTube sourcing pipeline

Built 1 Sep 2026 once Otto added `YOUTUBE_API_KEY` to `.env`. Four stages, run
in order from this directory with the project `.env` sourced.

```bash
python3 yt_search.py      # 1. recent on-topic videos -> candidate channels
python3 yt_channels.py    # 2. subscriber counts + descriptions
python3 yt_score.py       # 3. true last-upload date + fit scoring
python3 build_yt.py       # 4. hand-curated rows -> import-youtube.json
```

Then POST `import-youtube.json` to `/api/media-contacts/import`.

## Why the API and not a scraper

Two Apify actors were tried first and both failed, for reasons worth keeping:

- **Keyword *channel* search returns junk.** It matches channel *names*, not
  content — 13-subscriber channels, a K-pop dance channel, a Hindi sketching
  channel.
- **Video search surfaces a stale canon.** YouTube ranks on all-time
  relevance, so a keyword search returns the historically biggest videos: The
  Creators Project's kinetic-sculpture video is 12 years old, Dezeen's 9–11,
  Insider Art's 6. Of 464 channels found that way, the "fresh" tail was almost
  entirely tiny personal channels and tutorials.

`search.list` takes **`publishedAfter`**, which the API enforces, so the stale
canon never enters the pool. That single parameter is the whole difference.

## Quota

Free tier is 10,000 units/day. A full run costs roughly **2,400**:
`search.list` is 100 units per call (20 queries = 2,000), `channels.list` is
1 unit per call of up to 50 ids (16 calls), and the last-upload check is 1 unit
per channel (~345). Plenty of headroom to widen the queries.

## Two things the API gives that scrapers cannot

**A real `subscriberCount`**, so the runbook's 10k–500k band is enforceable
rather than guessed. And **the full channel description**, which is where
creators publish a business email in plain text — 100 of 777 channels had one.
That is a published address, not a pattern guess. YouTube hides the About-tab
email behind a captcha, so for the rest the contact has to come from the
channel's linked website.

## The last-upload trick

A channel's uploads playlist id is its channel id with `UC` → `UU`. So the
latest upload costs 1 quota unit via `playlistItems.list` with no extra lookup,
which is how the "uploaded in the last 60 days" filter is enforced for real.

## Scoring is a filter, not a verdict

`yt_score.py` keeps territory and vibe on separate axes, per Otto's direction
that the humour is load-bearing. It narrows 777 channels to 314 that pass every
hard filter; the final 26 are picked by hand in `build_yt.py`.

## The structural finding

**YouTube in this field is mostly practitioners, not press.** Unlike podcasts,
which exist to book guests, very few of these channels feature an outside
artist. Only five earned relevance 3 — STIR, MoltenArt, Skill Spectrum, The
Magnificent World of Toys, and W1 Curates. The rest are recorded honestly as
peers, suppliers or long shots rather than dressed up as coverage targets.

Two rows are **cross-stream and should probably move**: W1 Curates is a public
art *commissioner* (Festivals), and Digital Inflatable Sam Yu is a Chinese
inflatable manufacturer (sourcing register — Oddtoe makes building-sized
inflatables).
