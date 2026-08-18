# Media contact-sourcing pipeline — runbook

Built 18 Aug 2026 from `media-outreach-brief.md`. The stream's canonical data
is `media-contacts.json`; view it with `scripts/media.py`. Status flow:
`sourced → qualified → drafted → sent → outcome`, same as opportunities.

**Standing constraints.** No invented facts — every pitch draws only on
`positioning-source.md` and the approved `artist-bio-statement.md`. Audience
numbers only from a fresh analytics-skill read. Small and targeted, never a
spray list. The agent drafts; **Otto sends everything**. PR agencies are
flagged, never pitched (they cost money).

## Stage 1 — Source (per segment, evidence-first)

A contact enters the JSON as `sourced` only with a `why_fit` and, ideally, an
`evidence_url` — the episode or article that proves the fit. An outlet name
alone is a lead, not a contact.

- **Journalists** — start from the article, not the masthead. The seed rows
  are the eight outlets on ENESS's press list; the sourcing pass finds the
  actual piece each outlet ran on ENESS/Cave Urban/comparable studios and
  records the **byline**. That byline is the contact; the article is the
  evidence. Search: `site:dezeen.com ENESS`, outlet search pages, or the
  Apify `rag-web-browser` actor for pages that block plain fetches.
- **Podcasts** — Apple Podcasts / Spotify search and the free Podcast Index
  API (podcastindex.org) for terms: animation podcast, AI art, motion design,
  generative art. Qualify on: still publishing (episode in last 90 days) and
  has run at least one episode on AI-in-animation or a working-animator
  interview — record that episode as evidence. Host name + show site go in
  the record.
- **YouTube** — channels covering animation tooling and AI art. Filters:
  subscriber count (roughly 10k–500k — big enough to matter, small enough to
  book an unknown guest) and cadence (upload in last 60 days). Evidence: the
  video closest to the hybrid-pipeline angle. Apify YouTube scraper actors
  can pull channel stats in bulk if the list grows.
- **PR agencies** — record only, status stays `sourced` with a note; Otto
  decides if any conversation happens.

## Stage 2 — Enrich

Reuse the sales-outreach machinery — do not rebuild. The app's enrichment
(`start_enrichment`, live with the Apify credential bound) takes rows with a
LinkedIn company URL and no email, at ~$0.06 per row. For media contacts the
usual find is simpler: podcast/show sites publish booking emails, outlets
publish tips/contact pages. Order of preference:

1. Contact/booking page on the show or outlet site (record `contact_page`).
2. Published byline email or outlet tips address (record `email`).
3. LinkedIn URL (record `linkedin`) → app enrichment if an email is needed.

Set `verified` to the date the detail was read on a live page. Never guess an
email pattern.

## Stage 3 — Qualify

Score `relevance` 1–3 against the angle: a working animator with twenty years
of traditional craft using generative AI in production, while the public
argument is loud and fact-free. 3 = has covered exactly this territory;
2 = adjacent (general animation/design coverage); 1 = long shot. A show that
has never touched animation or AI art is a wasted pitch — drop it, don't
score it. Qualification also assigns the `hook` (see JSON `hooks` map).
Only `relevance ≥ 2` advances to drafting.

## Stage 4 — Pitch (drafts only, per segment)

All drafts derive from the media-kit template and `artist-bio-statement.md`.
**The statement was approved 18 Aug 2026 — the drafting gate is open.** The
short/long bios are reviewed drafts; confirm with Otto at first external use.

- **Podcasts / YouTube** — guest one-liner + 3 talking points + the short
  bio. Lead with the angle, not the traffic.
- **Journalists** — a story, not a guest: the hook that matches their
  evidence article, why now, and what's visual about it. Under 200 words.
- Voice guardrails apply (geo-playbook): no AI-writing tells, nothing poetic.

Draft text is stored on the record (`notes` or a per-pitch file if long) and
handed to Otto with deep links. Status → `drafted`; Otto sending it →
`sent`; reply/silence after follow-up window → `outcome` (record rejections
too — the pattern matters).

## Stage 5 — Track

`media.py` is the daily view. Rules the script enforces by loudness:

- A row past `sourced` with `verified: null` is flagged — details must be
  checked against a live page before anyone acts on them.
- One follow-up nudge per quiet contact, same as sales-outreach policy.
- Australian Spam Act checklist applies to any bulk-ish sending — raise it
  when drafting starts.

## Rule of thumb

If a media fact is about to be typed anywhere other than
`media-contacts.json` — a register row, a kit page, a pitch list — stop and
put it in the JSON first. Everything else is a generated view.
