# Guide kits — events & directory (token reference & workflows)

Two WPBakery pattern kits snapshotted 19 Aug 2026 from Otto's two proven Oddtoe guide pages.
They complement the money-page kits (`design-kit.html` / `design-kit-oddtoe.html`); the catalog of
all kits is `template-catalog.md`. All money-kit ground rules apply unless overridden here: strip
HTML comments before sending to WordPress, never alter row/column/styling attributes, content goes
only where tokens are, drafts only, author = Otto.

- **Events guide**: `design-kit-oddtoe-events.html` — from `/animation-conferences/` (page 16169).
  A chronological list of events (time + place). Dark theme: rows `#0f111b`, chino zigzags.
- **Directory guide**: `design-kit-oddtoe-directory.html` — **v2, the Otto-approved design (19 Aug
  2026)**, proven on the experiential-agencies page (16173). A ranked list of companies or people.
  Dark theme: rows deep wine `#210209` with `row-background-dark`, white zigzags. v1 (the raw salmon
  snapshot of `/animation-agents/` page 14208) is in git history; the raw master is in `masters/`.

Raw untokenized masters (for diffing and re-snapshotting) live in `masters/` — byte-faithful,
keeping WordPress's CRLF line endings; the kits are LF-normalized like the money kits (WordPress
accepts either). When Otto restyles a
live master page, re-fetch its raw content (`context=edit`, browser-like UA) and rebuild the kit
the same way.

## Differences from the money-page kits (important)

- **These pages predate the money-page conventions.** They use `ultimate_spacer` (not merged
  `dfd_spacer`) and their own row backgrounds. Do NOT "fix" them to money-kit rules — the kits are
  faithful snapshots of pages Otto approved as they stand.
- **Two-H1 flag:** on both masters the hero title is an `<h1>` AND the heading band renders
  `tag:h1` — two H1s per page. For NEW pages, keep the hero H1 and set the band's
  `title_font_options` tag to `h2` (Bebas renders identically). This is the one sanctioned
  attribute change. Already baked into directory v2 (hero title is the h1); still applies when
  composing from the events kit.
- **Hero background** is set in the row's `css` attribute: `url({{HERO_BG_URL}}?id={{HERO_BG_ID}})`
  — both values come from a media-library image (upload first, then fill both).
- **External links carry UTM tags**: `?utm_source=oddtoe.com&utm_medium=referral&utm_campaign={{UTM_CAMPAIGN}}`
  — one campaign slug per page (e.g. `animation-conferences-guide`). Keep `target="_blank" rel="noopener"`.

## Alternating layout rule (Otto, 19 Aug 2026 — BOTH kits)

Entries must alternate image side down the page — the layout shift is deliberate visual interest,
not an accident of the masters. **Events:** chain PAT-EVENT-IMG-LEFT / PAT-EVENT-IMG-RIGHT strictly
alternately, continuing the alternation ACROSS month bands (the last event of one band and the
first of the next must differ). **Directory:** PAT-ORG-FEATURED opens image-left; then alternate
PAT-ORG-STANDARD (image-right) and PAT-ORG-STANDARD-IMG-LEFT (image-left, derived variant with the
same tokens) — so entry #2 is image-right, #3 image-left, and so on. Never let two consecutive
entries put the image on the same side.

## Hero v2.1 + the empty-filler-row trap (19 Aug 2026)

**Hero proportions (Otto's re-proportioning on 16173, baked into both v2-design kits):** the hero
is compact — a `dfd_spacer` 200/200/160/120 above the title block and another below it (replacing
the old 1000px-tall block), and the hero row carries `bg_check="row-background-dark"`.

**Compose rule — no stray text between rows:** any whitespace/newlines left between `]` and `[`
in pushed content becomes EMPTY FILLER ROWS on the page's first WPBakery save (16 appeared on
16173). Compose scripts must collapse `]\s+[` → `][` before pushing (all three example scripts
now do). WPBakery saves also wpautop-wrap shortcode lines in `<p>`/`<br />` — harmless noise, but
it means byte-diffing live content against a compose after Otto has saved requires normalising.

## Page-level settings (wp-admin, per new page)

Template `page-custom.php` (wp-post.sh sets it). Then in wp-admin set the Ronneby Page Settings
(REST cannot): custom background colour = the page's row colour (`#0f111b` events / **`#210209`**
directory v2), background repeat on, header style 6. Without it, white lines show between rows.

## Directory kit v2 — the approved entry design (Otto, 19 Aug 2026)

Each entry row (`gap="20"` for a wider image/text gutter) is:
1. **Header stack, centred, full row width:** medal icon (hand markup `<i class="dfd-icon-medal_star
   dfd_icon_set-icon-medal_star">`, icon above the name) → org name, Bebas 96px, UTM-tagged link →
   `{{ORG_OWNERSHIP}}` Arvo 16px italic → `{{ORG_HQ}}` Arvo 13px uppercase, 2px letter-spacing.
2. **Content band at 60% of the row, centred:** empty `1/6` columns each side; image `1/4` (300×300
   art keeps full size); text `5/12` (~480px prose). Image side alternates per the alternation rule.
3. **The body text opens with `{{ORG_SCALE_SENTENCE}}`** — a bold Arvo 18px kicker, left-aligned,
   phrased as a full sentence that NAMES the org ("INVNT has 11 offices across four continents.").
   Repeating the name ties the kicker to the header stack (Otto's rationale).
4. Zigzag closes the row, full width.

For a PEOPLE directory (animation-agents style), the same slots serve: ORG_OWNERSHIP → the person's
role, ORG_HQ → their city, ORG_SCALE_SENTENCE → a sentence naming the person.

The v1 PAT-PAGE-LINK-CSS block (page-scoped link CSS for the light salmon palette) is GONE from v2
— dark rows use the theme's own light-on-dark links. `masters/directory-link-css-decoded.css` stays
for reference if a light-palette variant is ever wanted (see git history for the v1 kit).

## Token table (shared patterns)

| Token | Where | Spec |
|---|---|---|
| `{{HERO_KICKER}}` | hero, Qwigley 36pt | "Your guide to …" line, sentence case |
| `{{HERO_TITLE}}` | hero, Bebas 100pt | 2–3 word page title (the page's only H1) |
| `{{HERO_RANGE}}` | hero, Bebas 44pt | year or range, e.g. "2026 &amp; Beyond" |
| `{{HERO_BG_URL}}` / `{{HERO_BG_ID}}` | hero row css attr | full-bleed bg image URL + media id |
| `{{BAND_TITLE}}` (events) / `{{BAND_TITLE_LINE1/2}}` (directory) | heading band | the page's core question; directory splits it over two centred lines |
| `{{BAND_SUBTITLE}}` | heading band attr | Qwigley lead-in, sentence case |
| `{{INTRO_COL1..2}}` (events) / `{{INTRO_COL1..3}}` (directory) | intro columns | welcome copy split across columns; answer-first, keyword-bearing, links to the sibling guide page; ends "here are my picks … »". Directory columns keep the `<p class="p1"><span style="font-family: arvo, serif;">` wrapper of the master |
| `{{PICKS_HEADING}}` / `{{PICKS_SUBTITLE}}` | top-picks row | H2 question / "My Top 4" style tag |
| `{{PICKn_IMAGE_ID}}` `{{PICKn_LABEL}}` `{{PICKn_NAME}}` `{{PICKn_DETAIL}}` (n=1–4) | info_banner strip | media id / superlative ("Best Agency") / who or what / place or affiliation |
| `{{OUTRO_HEADING}}` / `{{OUTRO_BODY}}` | outro row | "What other X are worth mentioning?" + invite to contact (`/?page_id=176`) and a link to the sibling guide |
| `{{UTM_CAMPAIGN}}` | every external link | one slug per page, e.g. `brand-activation-events-guide` |

## Events-only tokens

| Token | Spec |
|---|---|
| `{{MONTH_LABEL}}` | e.g. "SEPTEMBER 2026" (caps in content is fine here — master style) |
| `{{EVENT_NAME}}` / `{{EVENT_URL}}` | h3 linked title; official site URL (kit appends UTM) |
| `{{EVENT_DATES}}` | e.g. "September 14th to the 17th, 2026" |
| `{{EVENT_LOCATION}}` / `{{EVENT_MODE}}` | "City, Country" / "onsite", "onsite and virtual", "virtual" |
| `{{EVENT_IMAGE_ID}}` | 300×300 media id, `dfd-image-scale`, radius 10 |
| `{{EVENT_BODY}}` | 60–150 words, first-person Oddtoe voice, why attend + who it's for; 0–2 internal links |
| `{{FAQ_TOPIC}}`, `{{FAQ_Qn}}/{{FAQ_An}}`, `{{FAQ_TAB_ID_n}}`, `{{FAQ_JSONLD_B64}}` | FAQ row: 4–8 Q&As (duplicate `vc_tta_section` for more, unique tab_ids like `faqslug-n-2026`); JSON-LD payload encoded urlencode-then-base64 exactly as the money kit (README §FAQ JSON-LD) |

**Composing a month band:** repeat the whole PAT-MONTH-BAND row per month. Inside it, chain event
entries alternating PAT-EVENT-IMG-LEFT / PAT-EVENT-IMG-RIGHT with PAT-EVENT-DELIMITER between
each pair; the band's trailing zigzag stays once at the end. One to five events per band.

## Directory-only tokens

| Token | Spec |
|---|---|
| `{{ORG_NAME}}` / `{{ORG_URL}}` | Bebas 96px centred heading; official site (kit appends UTM) |
| `{{ORG_SCALE_SENTENCE}}` | body kicker: full sentence naming the org, one defensible scale fact |
| `{{ORG_OWNERSHIP}}` / `{{ORG_HQ}}` | header stack: ownership line (italic) / "City, Country" (uppercase) |
| `{{ENTRY_BODY}}` | 60–150 words, first-person, why they made the list; verify entries are current — this page type goes stale (see 18 Aug 2026 audit) |
| `{{ENTRY_IMAGE_ID}}` | 300×300 media id (renders full size in the 1/4 column) |

**Composing entries:** PAT-ORG-FEATURED once (rank #1), then PAT-ORG-STANDARD per remaining
organisation, ranked order. Multiple people in one org = extra column pairs before the zigzag
column (copy the image/text column pair, swap widths to alternate sides).

## Events pages: carry the v2 design language (Otto, 19 Aug 2026 — note only, no retrofit)

Otto approved the directory v2 design as THE template look. The live Oddtoe conferences page stays
as it is, but the NEXT events-guide compose (first up: the Datalabs conference guides) should adapt
the same language, subject to Otto's art direction on v0: pinched **60% content band** with empty
side columns and `gap="20"`; a **centred header stack** per event (icon above → event name large →
meta lines in styled Arvo: dates italic, city uppercase letter-spaced); the **scale/hook line as a
bold Arvo kicker opening the body text, phrased as a full sentence naming the event**; dark rows
with `row-background-dark`; one H1. Once Otto approves the first such page, snapshot it as that
brand's events kit per the catalog loop.

## Body-copy rules for entries (Otto, 19 Aug 2026)

- **Bold the FIRST mention of the event/org name in each entry body** (not repeats) — a scanning
  anchor and entity signal; the name is already huge in the header, so once is enough.
- **Datalabs brand name**: "The **Datalabs Agency**", always bold; casual "**Datalabs**" (bold)
  sparingly. See geo-playbook brands.md.
- **"Updated [Month Year]"** renders as the money-kit hero treatment — centred bold italic line
  under the hero range ({{UPDATED_DATE}} token) — never as an inline sentence in the intro.
- **The intro lead-out** ("Here are my picks…") is its own centred line below the intro columns
  ({{INTRO_LEADOUT}}), never the tail of the third column.

## Verification rule (from the 18 Aug audits — applies to BOTH page types)

Every entry is a factual claim that decays: events move cities and dates; agents change agencies;
sites die. Before composing, verify every event/person/org against its official source (dates,
venue, spelling, live URL). Never carry entries forward from a previous year's page unverified.
