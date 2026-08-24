# Template catalog — the page-template suite

The list of WPBakery kits Otto can call upon when commissioning a page, and the agent composes
from. One row per template. When Otto commissions a page ("new events page for X", "directory of
Y", "pricing page for Z"), pick the template here, follow its kit + README, and run the money-pages
workflow (interview → compose → draft → backlog).

| Template | Call it for | Brand | Kit file | Specs | Source master | Status |
|---|---|---|---|---|---|---|
| **Money page — Datalabs** | Pricing, comparison, case study — pages that answer a buying question | Datalabs | `design-kit.html` | `design-kit-README.md`, `page-types.md` | Datalabs page 52964 (master dummy, never publish) | v1, proven (workshop pricing page) |
| **Money page — Oddtoe** | Same page types, Oddtoe styling (plum `#26161f`, sand `#ddccb1`) | Oddtoe | `design-kit-oddtoe.html` | `design-kit-README.md`, `page-types.md` | Oddtoe page 16132 (master dummy, never publish) | v1, proven (brand-activation-ideas, AI-animation pages) |
| **Events guide** | A chronological list of events — time + place + why attend (conferences, festivals, fairs) | Oddtoe | `design-kit-oddtoe-events.html` | `guide-kits-README.md` | Live page 16169 `/animation-conferences/` (snapshot 19 Aug 2026 in `masters/`) | v1, snapshot of Otto-approved live page |
| **Directory guide** | A ranked list of companies or people — who they are + why listed (agencies, studios, vendors) | Oddtoe | `design-kit-oddtoe-directory.html` | `guide-kits-README.md` | v1: page 14208 `/animation-agents/`; **v2 design approved by Otto 19 Aug 2026 on page 16173** (kit reproduces it byte-for-byte) | **v2 — THE approved template design** (wine `#210209`, header stack, 60% band, scale-sentence kicker) |
| Events guide — Datalabs | Chronological event lists on the approved v2 design, Datalabs palette | Datalabs | `design-kit-datalabs-events.html` | `guide-kits-README.md` (v2 design + events notes) | Assembled 19 Aug 2026 from directory-kit v2 + events-kit month/FAQ patterns + Datalabs money-kit footer | **v0 SEED** — first composes: pages 53654 + 53656 (drafts); Otto art-directs, then snapshot as v1 |
| **Artist &amp; Designer discipline page** | One craft Oddtoe practises — the `/artist-designer/` siblings (installation artist, kinetic sculptor, inflatable artist...) | Oddtoe | *(no kit yet — compose from `scripts/example-compose-oddtoe-installation-artist.py`)* | This row + `page-types.md` | Live page 11178 `/artist-designer/installation-artist/`, itself built on Documentary Animator (15400) | **v0 SEED** — 14-row shape, proven live; snapshot as v1 once Otto art-directs the bubble-FAQ change |
| Directory guide — Datalabs | (not built) | Datalabs | — | — | — | Same approach |

## Shared building blocks (usable across kits)

- **FAQ block** (accordion + FAQPage JSON-LD): money kits carry the `vc_tta`/`dfd_accordion` +
  raw_html pair; the events kit has its own instance. A directory page needing FAQs borrows the
  events kit's PAT-FAQ (swap the row background colour).
- **Cross-promo + announcement footers**: each kit ships its own fixed instance — always used as-is.
- **Tables**: only the money kits carry Otto's styled table exemplars; copy from there if a guide
  page ever needs one (cells factual, never poetic).

## Rules that apply to every template

1. Kits are snapshots of Otto-styled masters — content goes into `{{TOKEN}}` slots only; row/column
   attributes are never altered (single sanctioned exception: the guide kits' band `tag:h1` → `h2`,
   see guide-kits-README.md).
2. Strip all HTML comments before sending to WordPress.
3. Drafts only, author = Otto, Yoast fields in the handoff message (never in the body).
4. One page = one brand; geo-playbook rules and `banned.md` apply everywhere.
5. When Otto restyles a master, re-snapshot the kit (raw fetch, `context=edit`, browser UA) and
   bump the kit's header date. Raw snapshots live in `masters/`.

## Adding a new template to the suite

When Otto commissions a page shape that no kit covers: compose v0 from the nearest kit, let Otto
art-direct it in WPBakery, then snapshot the approved page into a new tokenized kit + README
section and add its row here. That is exactly how the events and directory kits were born.

## Artist & Designer discipline page — the 14-row shape

Reference implementation: `scripts/example-compose-oddtoe-installation-artist.py` (live, page 11178).
Second build: `scripts/example-compose-oddtoe-inflatable-artist.py` (Aug 2026), which introduces the
bubble-FAQ change below.

Row order: **1** hero (full-bleed dark, `dfd_bg_style="canvas"`, h1 + Qwigley h2 subtitle) · **2** intro
(h2/h3 heading, two `1/4` text columns inside `1/4` gutters) · **3** section head · **4** `dfd_carousel`
(~15 images, 250×250, radius 10) · **5–6** `qsection()` pairs · **7** comparison table · **8** who
commissions · **9** process · **10** in Oddtoe's words · **11** FAQ · **12** `rev_slider` band ·
**13** portfolio trio · **14** gravityform contact.

### Change v0 → v1: the bubble-FAQ row (Otto's request, Aug 2026)

Row 11 previously ran the accordion alone at `1/4 + 1/2 + 1/4`. It now takes the **homepage 15922
row #2 treatment**: a `width="1/2"` left column of five circular bubbles beside the accordion in the
right half.

- Left column carries `offset="vc_hidden-xs"` — **bubbles are hidden on phones**, accordion goes full
  width. That is the homepage's own behaviour; keep it.
- **Column split is `1/3` bubbles + `2/3` accordion — NOT the homepage's `1/2 + 1/2`.** The homepage row
  gets away with an even split because its five persona answers are one line each. A real FAQ runs 40–60
  words per answer, so at `1/2` the accordion towers over the bubbles and leaves dead space beneath them.
  Widening the accordion shortens it and narrowing the bubble column raises its height: both ends close
  the gap. (Corrected on the Inflatable Artist build, Otto's note, 21 Aug 2026.)
- Bubble geometry: a **2 – 1 – 2 scatter** down the column, not the homepage's 3-over-2, with `sp(70,60,45,30)`
  between inner rows so the stack tracks the accordion's height. Row A = `1/2` 80×80 right · `1/2` 140×140
  left; row B = `1/1` 115×115 centre; row C = `1/2` 120×120 right · `1/2` 160×160 left. Animations alternate
  `transition.expandIn` / `transition.shrinkIn`.
- **Stagger comes from `alignment` only — never copy the homepage's `css=".vc_custom_1778728115865{padding-right:50px}"`.**
  Those `vc_custom_*` classes are generated per-page and stored in that page's own WPBakery CSS; pasted onto a
  different page the class exists in the markup but the rule does not, so the padding silently does nothing.
- All bubbles use `style="vc_box_border_circle_2"`.
- The accordion gains `icon_size="18"`, `icon_color="#000000"`, `active_two_px_border="on"` and one
  `i_icon_fontawesome` (FontAwesome **5** names) per `vc_tta_section`.
- **The FAQPage JSON-LD stays.** Only the visual treatment is borrowed from the homepage; the content
  model remains FAQ, not the homepage's persona routing. The schema is the GEO payload — do not drop it
  for a page built to be cited.

### Bold is for keyphrases, never whole sentences

`design-kit-README.md` line 27: *"Body copy is NOT wrapped in blanket `<strong>` — bold is reserved for
keyphrases and numbers per the geo-playbook."* The money kit's own token specs say the same — "real
numbers and keyphrases in strong tags" — and `{{CANONICAL_SENTENCE}}` renders in a **plain `<p>`, unbolded**.

So: bold 2–3 keyphrases or a number inside the answer-first sentence, not the sentence itself. Bold
paragraph *labels* in a stepped list ("**1. Brief and site.**") are fine — those are scanning aids, not
body copy.

**Live page 11178 (Installation Artist) breaks this in six places**, including the canonical sentence, and
that is where the Inflatable Artist build inherited it from. Treat 11178 as a reference for *structure
only*, not for copy treatment. Retrofit both this and the timestamp when Otto next opens that page.

### "Updated [Month Year]" — its own centred line, never an intro sentence

Same markup everywhere; the row it sits in differs by template.

    [vc_column_text css=""]
    <p style="text-align: center;"><strong><em>Updated August 2026</em></strong></p>
    [/vc_column_text]
    [dfd_spacer ... 30 / 30 / 20 / 20 ...]

Centred, bold italic, no trailing full stop, always alone on its line.

- **Money kits / guide kits:** hero row, under the h1 (`guide-kits-README.md` line 148).
- **Artist & Designer discipline pages:** NOT the hero — the hero here is a tall full-bleed image with
  the h1 floating on it, and a centred date line has nothing to sit against. It goes in the **intro row
  (row 2), directly under the first `h2` and its delimiter**, above the two intro columns, followed by a
  30px spacer. (Otto's call, 21 Aug 2026, on the Inflatable Artist build.)

**Never as an inline sentence at the tail of an intro paragraph.** Live page 11178 (Installation Artist)
still carries it inline — `...an audience can walk around. <em>Updated August 2026.</em>` — predating this
rule and the reason the first Inflatable Artist build inherited the mistake. Retrofit it when Otto next
opens that page; do not edit 11178 for this alone without his say-so (edit fence).

### Slug convention

Person-noun under the hub: `/artist-designer/<craft>-artist/`. Prefer **artist** over **designer** where
both exist — "designer" SERPs are dominated by manufacturers, "artist" returns named practitioners, and
these pages exist to make Oddtoe the named practitioner. Cover the "designer" phrasing in body copy and
Yoast instead.
