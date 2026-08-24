# Opportunity register — Oddtoe

Deadline-driven opportunities for the two audiences that do not arrive through
search. One row per opportunity. **A row with no source URL is not a row.**

Status: `researching` → `drafted` → `submitted` → `outcome`

---

## press — festival accreditation and media partnerships

Leverage: the Oddtoe animation conferences guide ranks top-three in Google for
"animation conferences" and "animation conferences 2026". Pitch is in
`media-kit.md`. **Press deadlines are separate from, and earlier than, event
dates — usually 2–3 months out.**

Seeded from Oddtoe's own conferences page (the events Otto already researched).
**Every date below is unverified.** Read the organiser's press page before
acting; do not trust this table as a date source.

| Event | Month (per Oddtoe's guide) | Press deadline | Status | Source |
|---|---|---|---|---|
| Stuttgart ITFS | May 2026 | TO VERIFY | researching | itfs.de |
| Pictoplasma Berlin | May 2026 | TO VERIFY | researching | pictoplasma.com |
| Annecy / MIFA | Jun 2026 | TO VERIFY | researching | annecyfestival.com |
| Pictoplasma NYC | Sep 2026 | TO VERIFY | researching | pictoplasma.com |
| In Motion London | Sep 2026 | TO VERIFY | researching | — find URL |
| Ottawa International Animation Festival | Sep 2026 | TO VERIFY | researching | animationfestival.ca |
| MIPJUNIOR | Oct 2026 | TO VERIFY | researching | mipjunior.com |
| MIPCOM Cannes | 12–15 Oct 2026 (confirmed, Palais des Festivals) | n/a — inbound sales contact | **drafted** | mipcom.com |

**MIPCOM — inbound contact (21 Aug 2026).** Mariel Penilla, Sales Executive, RX
Global — mariel.penilla@rxglobal.com — cold-emailed Otto's Datalabs profile
selling the Visitor Pass (Early Bird EUR 1,550 + VAT until 25 Aug; Premium/
Prestige tiers above). Confirmed details from her email: 12–15 Oct 2026, Palais
des Festivals, Cannes; 2026 programme areas: MIP BrandWorks, MIP Creative Hub,
MIP AI Exchange, MIP Innovation Lab, matchmaking programme. Flip strategy: the
Oddtoe guide already gives MIPCOM its "Best Dealmaking" featured card plus
MIPJUNIOR and MIP AI Exchange links — reply proposes a media/listing partnership
(refreshed dates + 2026 programme coverage) in exchange for a pass, and asks to
be routed to the press/partnerships team if she cannot comp. Draft:
`drafts/2026-08-21-mipcom-reply.md`. She is SALES — her incentive is a sale, so
the draft leaves the door open to a discounted pass as the fallback outcome.

| View Conference Turin | Oct 2026 | TO VERIFY | researching | viewconference.it |
| Manchester Animation Festival | Nov 2026 | TO VERIFY | researching | manchesteranimationfestival.co.uk |
| SIGGRAPH Asia | Dec 2026 | TO VERIFY | researching | siggraph.org |
| Anima Brussels | Feb 2027 | TO VERIFY | researching | animafestival.be |
| Cardiff Animation Festival | Apr 2027 | TO VERIFY | researching | cardiffanimation.com |

**Also worth pitching as a speaker, not only press.** A speaker attends free and
gains a credential that serves the gallery audience too. Otto's angle is scarce:
twenty years of traditional craft plus working generative AI practice. Most
festivals in 2026 want an AI panel and can book either hype or refusal.

---

## media — podcasts, YouTube, journalists, PR agencies

The media outreach stream lives in **`media-contacts.json`** (canonical) with
`scripts/media.py` as the view — no rows are duplicated here, so nothing can
drift. Pipeline design: `media-pipeline.md`. Pitches draw only on
`positioning-source.md` and the approved `artist-bio-statement.md`.

    python3 scripts/media.py          # pipeline state
    python3 scripts/media.py --md     # markdown view of all rows

---

## market — pitch sessions

Where a creator pitches a series to commissioners. Otto **already has a pitch
bible** for the Oddtoe TV series; the gap is the application deadline, not the
material.

| Market | Pitch session | Applications close | Status | Source |
|---|---|---|---|---|
| MIFA Pitches (Annecy) | animation series/shorts | TO VERIFY | researching | annecyfestival.com/mifa |
| Cartoon Forum | European co-production | TO VERIFY | researching | cartoon-media.eu |
| Kidscreen Summit | kids content | TO VERIFY | researching | kidscreensummit.com |

---

## prize — awards and competitions

The most direct attack on the credits gap: a shortlisting is a nameable credit
and nobody has to invite you first. Rivals hold FRAME, Dezeen, LIT, Melbourne
Design Awards, Japan Media Arts, MUSE, and a TEA Master honour. Oddtoe holds
none. See `analytics/references/competitor-register.md`.

| Award | Category fit | Closes | Status | Source |
|---|---|---|---|---|
| *(none logged yet)* | | | | |

---

## opencall — open calls, group shows, artist-run spaces

Otto chose this alongside prizes as the first rung for the gallery audience.
Builds exhibition history line by line, which is the first thing a gallery asks
for.

| Opportunity | Venue / type | Closes | Status | Source |
|---|---|---|---|---|
| *(none logged yet)* | | | | |

---

## register — council and institutional public-art lists

Low glamour, real commissions, and a council credit reads to a museum producer
as "has delivered publicly before". A Blanck Canvas sits on City of Port
Phillip's urban artist directory.

| Body | List | Opens / closes | Status | Source |
|---|---|---|---|---|
| *(none logged yet)* | | | | |

---

## Standing rules

1. **No date without a source.** `TO VERIFY` is an honest state; a guessed date
   that passes silently is the failure this register exists to prevent.
2. **Record outcomes, including rejections.** Five rejections with reasons is
   more useful than five blanks.
3. **Nothing here is submitted by the agent.** Drafts are handed to Otto, who
   sends them.

---

# Evergreen conferences page — draft 16169 (18 Aug 2026)

Draft at slug `animation-conferences`, built by surgery on live page 13839 so
Otto's design and prose survive untouched.

**Removed:** the whole "SEPTEMBER 2024" row — In Motion Rotterdam 2024, an old
Ottawa Sept 25–29 2024 entry, and a duplicate Pictoplasma NYC block (7,467 chars).

**Rolled to verified 2027 dates:** Stuttgart ITFS → 27 Apr–2 May 2027, Annecy →
13–19 Jun 2027, Anima → 19–28 Feb 2027 (was "to be announced"), Pictoplasma
Berlin → "2027 dates to be announced".

**Added:** Cartoon Forum (14–17 Sep 2026, Toulouse) placed first in the September
row, and Cartoon Movie (2–4 Mar 2027, Bordeaux) in a new March 2027 row cloned
from February's.

**Order is now chronological:** Sep 26 · Oct · Nov · Dec · Feb 27 · Mar · Apr ·
Apr–May · Jun.

**Verified in the browser:** 17 conferences, no stale strings, the FAQ module
intact with 4 panels, all nine month headings white at 18.81 contrast.

## Known gap on the draft

Cartoon Forum and Cartoon Movie have **no city illustration**. Every other entry
carries a 512×512 city image (Cardiff 13953, Torino 13951, Stuttgart 13939,
Brussels 13944, Cannes 13950…). There is no Toulouse or Bordeaux image in the
media library. The image column is in place and empty so one can be dropped in.

## Redirection rows to add on publish

| Source | Target | Type |
|---|---|---|
| `/animation-conferences-2026-2027/` | `/animation-conferences/` | 301 |
| `/animation-conferences-2024-2025/` | `/animation-conferences/` | 301 |

The second recovers 4,931 impressions stranded on a stale page.

**Trade-off to accept knowingly:** the old URL ranks 2.6 for "animation
conferences 2026". An evergreen slug gives that up in exchange for a URL that
compounds instead of resetting each cycle. Expect a few unsettled weeks.

## City illustrations added — 18 Aug 2026

Otto supplied Toulouse and Bordeaux illustrations, completing the city-image set.

| File | ID | Used by |
|---|---|---|
| `Toulouse-Cartoon-Forum-Animation-Conference-France.jpg` | 16170 | Cartoon Forum |
| `Bordeaux-Cartoon-Movie-Animation-Conference-France.jpg` | 16171 | Cartoon Movie |

**Naming follows the library's existing pattern** (`Mipcom-Cannes-Animation`,
`Tokyo-Anime-Conferences-Oddtoe-List`): city, then event, then category, then
country. The filename is a ranking signal for image search, and "animation
conference" is the term this page already ranks top-three for.

Both carry alt text, title and caption. Converted from PNG to JPEG at quality 82
before upload — the originals were 1.9 MB and 1.4 MB, which is a real page-speed
cost on a page that already ranks. They landed at 504 KB and 308 KB at the same
1024×1024, and WordPress serves the 300×300 crop the layout asks for.

**For the next city image:** convert to JPEG before uploading, name it
`City-Event-Animation-Conference-Country.jpg`, and set alt text describing the
illustration and the festival it belongs to.

---

# PUBLISHED — /animation-conferences/ — 18 Aug 2026

Page 16169 live at https://www.oddtoe.com/animation-conferences/
Old page 13839 set to **draft** (recoverable) so its URL frees up for the redirect.

## Final fixes before publish

| Issue | Cause | Fix |
|---|---|---|
| MIPJUNIOR image had square corners | its shortcode alone carried `link_object`/`enable_link`/`image_ext_link_url`; linking the image makes the theme skip the `dfd-single-image-module` wrapper, and the radius lives on that wrapper | link attributes removed |
| Missing delimiter, Cartoon Forum → Pictoplasma | new insert had none | added |
| Delimiter spacing 20px vs 40px elsewhere | house pattern is **1 spacer before, 2 after**; the insert had 1 after | second spacer added |
| SIGGRAPH Asia had no image | no Kuala Lumpur illustration existed | Otto supplied one; uploaded as 16172 |
| 3 dead outbound links | two `adobe.com/max/2025` pages gone, one Manchester 404 | Adobe ones unlinked (text kept), Manchester repointed to its homepage |

## UTM tracking

40 outbound links to festival domains now carry:

    ?utm_source=oddtoe.com&utm_medium=referral&utm_campaign=animation-conferences-guide

Applied only to the 14 festival/market domains — internal Oddtoe and Datalabs
links are asserted clean. This is what makes the press-accreditation pitch
provable: the festival can see the referrals in their own analytics.

## Redirects — chain flattening still outstanding

Otto already had a chain from previous cycles. Current state, all verified 301:

| Source | Hops to /animation-conferences/ | Lifetime hits |
|---|---|---|
| /animation-conferences-2026-2027/ | 1 (direct) | new |
| /animation-conferences-2024-2025/ | 2 | 861 |
| /animation-conferences-2023-2024/ | 3 | 2,750 |

**Worth flattening.** In Tools → Redirection, edit the two older rules to target
`/animation-conferences/` directly. Google follows chains but equity decays, and
the 2023-2024 URL still takes real traffic.

**Redirection gotcha:** rules default to "Exact match in any order" on query
parameters, so a URL with `?anything` does **not** match and returns 404. Test
redirects without cache-buster query strings or you will misdiagnose them.

Redirection's REST API rejects application-password auth (`rest_forbidden`) — it
needs its own admin nonce. Redirect work has to go through the admin UI.

## Yoast — needs Otto's hands

Setting `#yoast_wpseo_title` / `#yoast_wpseo_metadesc` by script does not stick;
Yoast's React store overwrites the hidden inputs on submit. Type into the Yoast
panel directly at
https://www.oddtoe.com/wp-admin/post.php?post=16169&action=edit

    SEO title:  Animation Conferences 2026 & 2027 — The World's Best
    Meta desc:  The best animation conferences and festivals worldwide, month by
                month: dates, venues and what each is really for. Annecy, Ottawa,
                Cartoon Forum and more.

Until then the page has no meta description and Google writes its own snippet.

## Indexing status

- Sitemap: new URL present, retired URL gone. Canonical correct.
- `llms.txt` serves 200, so AI crawlers have a path in.
- Google has **not** seen it yet — published minutes ago. The 301 from the old
  URL is the strongest signal and needs no action.
