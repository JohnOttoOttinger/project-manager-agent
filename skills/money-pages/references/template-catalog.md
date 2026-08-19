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
