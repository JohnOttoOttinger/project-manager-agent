# Design Language — the shared page/row/module vocabulary (v1, approved by Otto 25 Aug 2026)

**Status: v1 — Otto approved every ⚑ proposed name as-is on 25 Aug 2026 (⚑ marks kept to show
which names were coined in that session vs read from his WP libraries). "Info2" = the Ronneby
`dfd_info_box` module. Unmarked names are Otto's own, read verbatim from the WPBakery
"My Templates" libraries on both sites (25 Aug 2026).**

Both brands use this one vocabulary. A design is named once; each brand renders it with its
own palette/typography (same model as the money/guide kits). This file is the pick-list for
commissioning sentences like:

> "Give me a page that looks like the Otto Ottinger page, but apply the GEO uplift (Q&A).
> Include also the Row that shows a headline and three Info2 modules. Populate with the
> Visual Case Study content for the Adidas workshops."

## Naming convention (Otto's, observed in both libraries)

- **`Page:`** a full page of design. May carry a nickname in parens — e.g.
  *Page: Artist Craft Page w/ Huge Image Opener, Carousel, Text & Q&A (the documentary template)*.
  The nickname alone is a valid call-up.
- **`Row:`** one full-width horizontal layer — e.g. *Row: Client Logo Carousel w/ Headline*.
- **`Module:`** one part inside a row (a Q&A block, a quote card, a header treatment).
- Descriptive " w/ " chains list the row's contents; `&` and abbreviations welcome.

## Otto's existing WP template libraries (verbatim)

### Datalabs (read from page 52964's editor)

| Name | Notes |
|---|---|
| Page: Otto Ottinger Template | The founder-page shape — see anatomy below |
| Page: Analysts Toolkit, 50% of the Way | Work-in-progress save |
| Page: Beautiful Grid Option w/Video & Form | |
| Row: Client Logo Carousel | Also exists on Oddtoe (w/ Headline variant) |
| Row: Twin Screamouts with Transparent 3d Products | The 5/6+1/6 double CTA pair ("Buy Creative Design Assets »" / "« Book a Workshop") |
| Row: What Our Clients Say w/ Logos & Testimonials | Dark bg testimonial carousel |
| Button: Opens Into a Form | |
| Client Portal: Workshop Slides & Workbook Download | |
| New DLA One / Two / Seven / Twenty-One / Twenty-Five / Twenty-eight | **DFD stock templates** (Ronneby maker's portfolio downloads) — see "DFD stock" policy below |
| SAVE: Datalabs Homepage (9 June 2026) | Backup save |
| CBRE Portfolio (delete after porting) | Marked for deletion |

### Oddtoe (read from page 16132's editor)

| Name | Notes |
|---|---|
| Page: Artist Craft Page w/ Huge Image Opener, Carousel, Text & Q&A **(the documentary template)** | = the 14-row Artist & Designer shape in template-catalog.md |
| Page: Artist Craft Page 2 w/ Huge Opener, Lots of Text, Compare Slider, & Q&A **(the sensory garden template)** | |
| Page: City Template w/ Text, Three Infoboxes Q&A, & Three Promo Rows **(the Melbourne template)** | |
| Blog: Template A - Lots of Modules | |
| Blog: Template B w/ Video & Two Images | |
| Row: Biggest Headline w/ Opening Header & Text | |
| Row: Client Logo Carousel w/ Headline | |
| Row: Five Bubble Images & Half-page Q&A | The homepage-15922 row #2 treatment (also the bubble-FAQ source) |
| Row: Four Tiny Infobox Promoters w/ Headline | |
| Row: Headline w/ Three Columns of Icons or Images | |
| Row: Headline w/ Two Column Text | |
| Row: Nine Spinning Images w/ Text Explainers on Back **(the gag cartoonist gallery)** | |
| Row: Parallax Image Chapter Divider | |
| Row: Q&A Interactive Quuestionairre | |

## DFD stock templates — the "New DLA n" saves (policy agreed 25 Aug 2026)

The six `New DLA …` saves are unmodified DFD/Ronneby portfolio templates — **not yet in either
brand's design style**. They stay in the vocabulary as a **separate category**, never called up
directly for a live page:

1. **Category, not brand.** In this registry they are `DFD:` stock. (WPBakery's library is a flat
   list, so the name prefix *is* the category — same trick as Otto's `Page:`/`Row:` prefixes.
   Renaming the saves themselves to `DFD: One` etc. is Otto's optional wp-admin cleanup.)
2. **Restyle on first use.** When a DFD stock design earns a slot on a real page, it gets
   rebuilt in brand style (fonts → Qwigley/Bebas stack, colours → brand deltas, spacing →
   dfd_spacer hygiene) on a draft, Otto art-directs, and the approved result is saved as a NEW
   named template (`Row:`/`Module:` + brand). The stock save stays untouched as the reference.
3. Restyling is proven mechanics — fonts and colours are shortcode attributes, exactly what the
   money/guide kits already retokenize. The one unknown per template is *which* modules it uses;
   that's discovered the first time it's pulled onto a draft page.

## ⚑ Proposed names for recurring un-named designs (from the 25 Aug scan of 30 pages)

Found by structural scan of every main-nav page on both sites + the recent money pages.
Each appears on 3+ pages. **All names below are proposals — approve, rename, or strike.**

| ⚑ Proposed name | What it is | Where it lives today |
|---|---|---|
| **Module: Header Stack** | The signature heading treatment: Qwigley script kicker + condensed BEBAS headline + short dash delimiter | Every page, both brands; guide kits call it the "header stack" |
| **Row: Clients of Note** | "Otto Ottinger's Clients of Note" — heading + 7 framed client single-images + logo carousel | Otto Ottinger R3, both money pages, style-guides R8 |
| **Row: Products Shelf** | Header Stack + WooCommerce `[products]` grid ("Level Up In Data Viz!", "Buy Templates, Courses...") | Datalabs: home, all Data Design pages, workshops |
| **Row: Contact Footer** | Dark band, Header Stack + Gravity Form ("Interested in working with Oddtoe?", "Looking for a speaker...") | Last row of nearly every page, both brands |
| **Row: GEO Q&A** | 1/4+1/2+1/4 accordion + FAQPage JSON-LD — "the GEO uplift" | Money kits, Otto Ottinger R14, all Oddtoe craft pages |
| **Row: Animated Text Band** | Full-width `dfd_animated_text` marquee on a flat colour | Datalabs service pages; Oddtoe artist-designer, gen-AI pages |
| **Row: Info2 Grid** | Header Stack + grid of 5–8 `dfd_info_box` modules (icon + title + text) | Home R5/R9, style-guides R9, workshop pages, map/power-bi pages |
| **Module: Info2** | One `dfd_info_box` (icon/number + heading + body) | Inside the grids above; "three Info2 modules" = 3-up row of these |
| **Row: Masonry Client Wall** | 35-logo `dfd_masonry_container` wall ("A Data Visualization Consultancy Serving All Industries") | Datalabs home R3 |
| **Row: Blog Trio** | Header Stack + 3 latest-post cards (`dfd_blog`) | Datalabs home R10 |
| **Row: Keynote Deck Stack** | Repeating title-card image + venue caption list ("Workshops at Company Retreats") | Otto Ottinger R5–R8 |
| **Module: Avatar Quote** | Centred pull-quote + circular avatar + name/caption (the ChatGPT & Gretzky quote) | Otto Ottinger R13; infographic pages |
| **Row: Big Statement** | 1/6+4/6+1/6 centred prose band on dark ("Why we price per session...", "Public, Guest, or Keynote Speaker") | Money pages, Otto Ottinger, Oddtoe home R12/R15 |
| **Row: Hero Slider** | Full-bleed Revolution Slider opener | Oddtoe home, gen-AI pages, investment |
| **Row: Portfolio Trio** | 3 `dfd_portfolio_module` cards | Oddtoe craft pages R13, portfolio, original-stories |
| **Page: Data Design Service** | The recurring Datalabs service-page shape: dark h1 band → intro → logo carousel → examples → Info2 Grid → Animated Text Band → What Our Clients Say → Products Shelf → Contact Footer | interactive-data-viz, power-bi, maps, infographic-reports, etc. |

## Registered 25 Aug 2026 (Otto-approved, from the Marriott build)

| Name | What it is | Reference implementation |
|---|---|---|
| **Page: Visual Case Study** | Client case study with visual assets: split hero (Section A) → Animated Flow Diagram → problem section + CTA → discovery → dashboard/asset table → 2×2 lightbox gallery → Hotspot deep-dive → Big Statement + image → Design Principle Tiles → deliverables → Avatar Quote → GEO Q&A → articles → fixed footers | Marriott draft 53852; compose from `scripts/example-compose-datalabs-marriott-case-study.py`; raw master `masters/datalabs-visual-case-study-53852-v1-2026-08-25.txt`; catalog row in template-catalog.md |
| **Row: Animated Flow Diagram (SVG)** | Inline brand-palette SVG in a `vc_raw_html` block (1/6+2/3+1/6): source nodes → central hub → outcome cards, animated dashed tan flow lines (SMIL), per-card stepping bar highlight w/ pulse | Marriott 53852 ("From five systems to four screens"); generator `svg_flow()` in the Marriott compose script — regenerate per project, never hand-edit the base64 |
| **Row: Design Principle Tiles (SVG)** | Inline SVG grid of 3×2 principle tiles: tan top-rule, custom line-icon glyph, Bebas title, one-line Arvo caption | Marriott 53852 ("The design concepts behind the screens"); generator `svg_concepts()` in the same script — glyph library: people, clock, hierarchy, grid, charts, swatches |
| **Module: Hotspot** (poach recipe confirmed) | `dfd_hotspot` image + markers + tooltips; `hotspot_data` = URL-encoded JSON `[{index,x,y,Title,Message}]`, x/y percentages; tan `marker_background` | Marriott 53852; original exemplar Datalabs 687 |
| **Module: Avatar Quote** (poach recipe confirmed) | `new_testimonials main_style="style-1" main_layout="layout-1"` — photo, author, subtitle, quote | Marriott 53852; original exemplar Otto Ottinger page 35734 |

## Anatomy: Page: Otto Ottinger Template (page 35734, all rows on plum #2f2e3a)

R1 hero (Header Stack h1, 4-col) · R2 photo carousel · R3 **Clients of Note** · R4–R6 keynote
section (Header Stacks + **Keynote Deck Stack**) · R7 **Big Statement** + image · R9–R11 data-viz
section + carousel · R12–R13 **Big Statement** + inventions image + **Avatar Quote** ·
R14 speaker form + **GEO Q&A** + Gravity Form.

## Brand deltas (unchanged from the kit system)

- **Datalabs:** plum `#2f2e3a` / near-blacks `#252525`/`#000` / light `#e9e9e9`; tan accent.
- **Oddtoe:** sand `#ddccb1`, olive `#8a9f6a`-family accents. The money kit ships plum
  `#26161f`, but **every money page gets its own near-black** (Otto, 26 Aug 2026: bored of
  the plum repetition) — the same per-page tinting the Visual Case Studies use. Palette and
  rule below; craft pages already did this by hand (`#332D26`, `#322E34`, `#262B2A`).
- Typography identical stack (Qwigley / Bebas-style condensed / body serif-sans per theme).

## Source snapshots

Raw `context=edit` bodies of all 30 scanned pages: session scratchpad `dla-scan/` +
`odd-scan/` (25 Aug 2026). Re-fetch any page the same way when a named row's markup is
needed for composing; long-lived exemplars get promoted into kits per template-catalog.md.


## Oddtoe money-page tints (approved 26 Aug 2026)

`scripts/oddtoe_theme.py` holds the palette and does the retint. A money page carries the
tint in **five** places — the first is wp-admin only, so the script cannot finish the job
alone:

| # | Where | Set by |
|---|---|---|
| 1 | Page Options `crum_page_custom_bg_color` (+ `repeat`, header style 6) | wp-admin, by hand |
| 2 | Hero row `dfd_overlay_color` | `retint()` |
| 3 | Three row `css=".vc_custom_N{background-color:…}"` attrs | `retint()` — **stripped**, not recoloured |
| 4 | 28 table `border-bottom: 1px solid …` hairlines → `lighten(bg, .13)` | `retint()` |
| 5 | Scroll-down delimiter line + icon (v0-seed lavender) → tint + sand/olive | `retint()` |

Row backgrounds are stripped rather than recoloured so the page ground stays the single
source of truth — a later tint change is then one wp-admin field, not a re-compose.

| Name | Hex | Assigned to |
|---|---|---|
| plum | `#26161f` | kit default; retire from new builds |
| teal | `#142322` | AI Animation Studios (16210) |
| ink | `#171d2a` | — |
| forest | `#16211a` | — |
| graphite | `#1c1c1f` | — |
| umber | `#241b16` | — |
| slate | `#1a1e26` | — |
| nearblack | `#101418` | — |

**Rule:** never give the same tint to two pages in one cluster — the point is that a visitor
moving between Oddtoe service pages sees a different ground each time.
