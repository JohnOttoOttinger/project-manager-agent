# Media outreach brief — Oddtoe as artist, and who should be talking about him

Prepared 18 Aug 2026 as the starting package for a dedicated session. Four
deliverables in scope: **artist bio**, **artist statement**, **artist/studio
schema**, and an **automated contact-sourcing pipeline** for podcasts,
YouTubers, journalists and PR agencies.

## Source material — read these first, in this order

| File | What it holds |
|---|---|
| `references/positioning-source.md` | The single source of truth: verified facts, credits, and the honest gaps (artist statement and CV are both `TO FILL` — deliverables 1 and 2 close two rows of that table) |
| `references/media-kit.md` | The press-facing asset: search positions (top-3 for "animation conferences"), traffic with honesty caveats, the offer, and a working pitch template |
| `references/opportunities.md` | The deadline register — `press` stream is the nearest neighbour to this work |
| `skills/analytics/references/competitor-register.md` | The five rivals and the finding that the shortlist gap is a credits problem |
| `skills/analytics/references/ahrefs/2026-08-17-content-gap.md` | What rivals publish that Oddtoe doesn't: ENESS's press list (FRAME, Dezeen, Wallpaper, WIRED, ArchDaily, The Age, SMH, "50+ others") is the model of what media attention looks like in this field |
| Memory: `oddtoe-target-audiences` | Audiences 4 (entertainment/publishing) and 5 (gallery/museum) are who media attention ultimately serves |
| Memory: `oddtoe-naming-rule` | "Oddtoe" on all artistic surfaces; "Otto Ottinger" only for legal/operator contexts |
| Memory: `otto-working-style` | Voice guardrails (no AI-writing tells), plan-first approvals, deep links when handing tasks over, report progress continuously |

## Live-site state (verified 18 Aug 2026)

- **Bio material exists but is scattered**: `/about-oddtoe/` (first-person,
  informal, "since 1996 … under the pseudonym Oddtoe"), plus city pages
  (`/about-oddtoe/melbourne-australia/`, `/berlin/`, `/los-angeles/`) and
  13 role pages under `/artist-designer/` and `/studio/`. There is **no single
  canonical bio** and no artist statement anywhere.
- **Schema gap confirmed**: homepage carries only Yoast defaults
  (`Organization`, `WebSite`, `WebPage`…). **No `Person`**, no artist typing,
  no `sameAs` beyond the social row, no `knowsAbout`. Nothing anywhere declares
  Oddtoe an artist to machines. Recommended shape: `Person` (Oddtoe, with
  `alternateName` John "Otto" Ottinger) linked to `Organization` via `founder`,
  with `jobTitle`/`hasOccupation` (visual artist, animator), `knowsAbout` the
  craft list, and `sameAs` to socials + the two ranking guides. Delivery route:
  Yoast's Person/Organization settings first (cleanest), `[vc_raw_html]`
  JSON-LD blocks where Yoast can't express it — the FAQ rollout scripts in
  `skills/money-pages/scripts/` already do exactly this pattern.
- The **llms.txt advantage** (Oddtoe serves it, all five rivals 404) extends
  naturally: a bio + statement page becomes citable by LLMs, which is GEO for
  "who is Oddtoe".

## The angle that earns attention

From the media kit and content gap, the one story no rival can tell: **a
working animator with 20 years of traditional craft (National Geographic
credits, political cartooning, puppetry) who uses generative AI in production
rather than theorising about it** — while the industry argument about AI in
animation is loud and largely fact-free. Podcasts and YouTubers in animation
currently book either AI-hype guests or anti-AI traditionalists; a craftsman in
the middle with a hybrid pipeline (AI imagery + rigging + traditional motion
design) is rare booking material. Secondary hooks: the top-3 conferences guide
(useful to any host's audience), topiary/robotics/sensory-garden oddness for
general-interest formats, Melbourne public-art scene for local press.

## Contact-sourcing pipeline — the build target

Goal: a repeatable `media` stream alongside the existing streams, feeding the
same register. Sketch to refine in session:

1. **Source** — per segment, enumerable lists exist: podcast directories
   (Apple/Spotify search, podcast index APIs) for animation/AI-art/design
   shows; YouTube channels covering animation tooling and AI art (subscriber
   and cadence filters); journalists via the outlets rivals already appear in
   (FRAME, Dezeen, Wallpaper, WIRED, ArchDaily, Designboom, The Age, SMH) —
   who bylined those pieces; PR agencies last (they cost money — flag, don't
   pitch).
2. **Enrich** — the solopreneur app's sales-outreach enrichment is **already
   built and live with the Apify credential bound** (Phases 1+2, PRs #9/#10).
   Reuse that machinery: contact page / email / LinkedIn per name.
3. **Qualify** — relevance scoring against the angle above; a show that has
   never covered animation or AI art is a wasted pitch. Record *why* each
   contact fits (the episode/article that proves it).
4. **Pitch** — per-segment templates derived from the media-kit template
   (podcasts want a guest one-liner + talking points; journalists want a story,
   not a guest). All drafts from `positioning-source.md` facts only. Otto
   sends; the agent never contacts anyone directly.
5. **Track** — rows in the register with status flow
   `sourced → qualified → drafted → sent → outcome`, same as opportunities.

Constraints that stand: no invented facts (the credits are thin — one 2019
public commission — and the media kit's honesty rules apply to every pitch);
audience numbers only from a fresh analytics-skill read; volume is small and
targeted, not a spray list.

## One source of structured data — the architecture decision to carry in

A problem already lived through this week, worth solving properly in this
session rather than repeating: **the same facts exist in three places, typed by
hand three times.** Festival dates were hand-typed into `opportunities.md`
after already existing on the animation-conferences WordPress page, and would
be hand-typed again at the next page update. Same facts, three places, drifting
apart immediately.

The fix is direction-of-flow: **one canonical structured file → everything else
generated.**

| Task | Shape |
|---|---|
| Canonical data file | One JSON per domain (conferences/festivals already half-exists as `references/opportunities.json`; media contacts get their own). Every record: name, dates, deadlines, URLs, contact, status, source-verified date |
| Page generation | The WordPress conferences page composes *from* the JSON via the existing composer-script pattern (`skills/money-pages/scripts/example-compose-*.py`) — a date changes once, the page regenerates |
| Tracker feed | `opportunities.md` rows and `due.py` deadlines read from the same JSON — no re-typing, no drift |
| Media pipeline | The contact-sourcing pipeline (above) writes into this structure from day one — sourced contacts are records, pitches and outcomes are fields on the record, and any future "media" page or kit refresh generates from it |
| Media kit refresh | Traffic numbers pulled by the analytics skill into the kit at send time, never quoted from memory — same principle, live source over copied fact |

Rule of thumb for the session: **if a fact is about to be typed a second time,
stop and move it into the JSON first.**

## Suggested kickoff prompt for the new chat

> Read `skills/opportunity-tracker/references/media-outreach-brief.md` and the
> files it lists. Then: (1) draft the Oddtoe artist bio (short + long) and
> artist statement for my approval; (2) propose the Person/Organization schema
> and where it goes; (3) design the media contact-sourcing pipeline and build
> the `media` stream on the one-source-of-structured-data architecture in the
> brief. Work in that order — the bio and statement are inputs to
> every pitch the pipeline will send.
