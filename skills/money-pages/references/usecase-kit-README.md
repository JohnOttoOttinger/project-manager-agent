# Use Case kit — token reference & workflow

**Kit:** `design-kit-oddtoe-usecase.html` — v1, snapshot of the live, Otto-art-directed page
**16272** `/use-cases/publicity-stunts/` taken 11 Sep 2026 (raw master in `masters/`).
**Fill it with:** `scripts/compose-usecase.py <content.json>`. **Re-snapshot it with:**
`scripts/snapshot-usecase-kit.py <master-raw.txt>` whenever Otto restyles the live page.

A Use Case page takes **one kind of brief** and follows it from the first drawing to the day
itself. One page per audience row on the homepage "See yourself as?" module. Parent is the hub
**16296** `/use-cases/`; slug is the brief, not the object (`publicity-stunts`, not `carried-heads`).

## Otto's decisions that shape the kit (11 Sep 2026)

1. **Fixed spine, modules swap content only.** All 19 rows, in the live order, row and column
   attributes untouched. Six modules carry the page-specific story: six-idea circles, six-step
   timeline, five package boxes, six spec figures, the comparison table, and the FAQ.
2. **Template first.** The kit exists before the next page is commissioned. Nothing composes
   until Otto has seen it.
3. **One page per homepage row.** Art Director / Marketing → Product Launch; Events management →
   Festival or Precinct Activation; Real estate / architecture → Lobby or Development Launch;
   Entertainment producer / publisher → New Content; Gallery / museum → Museum Late Opening
   (the sleepover installation is one of its six ideas, not its own page). Pending Otto's
   review of the sector mapping note before any is built.
4. **The buyer's lens (confirmed 11 Sep).** Every use case starts from the buyer's year and the
   jobs they would hire Oddtoe for; the six ideas are those jobs. Sectors are only names in
   "Who commissions". The five audiences are worked through in
   `Oddtoe New Growth Pages 2026/use-case-sector-mapping-2026-09-11.md`.
5. **Raw HTML stays raw** for the timeline, the circles and the video (Otto keeps them for the
   interactivity). Drawings and package boxes are native so he can edit text in the builder.

## The 19 rows

| # | Anchor | Row | Tokens |
|---|---|---|---|
| 1 | `hero` | Canvas image hero, the page's one H1 | `HERO_IMAGE_ID`, `HERO_KICKER`, `HERO_TITLE`, `TINT` |
| 2 | — | Homepage opener: 200px Bebas giant title over 48px kicker, h2 + Qwigley kicker, Updated line, two 1/4 columns | `GIANT_TITLE`, `GIANT_KICKER`, `INTRO_TITLE`, `INTRO_KICKER`, `UPDATED`, `INTRO_COL1..2` |
| 3 | `drawings` | Three drawings from the sketchbook (640x480 rounded, step label, h3, body) | `DRAWINGS_TITLE/KICKER/INTRO`, `DRAWn_IMAGE_ID`, `DRAWn_STEP`, `DRAWn_TITLE`, `DRAWn_BODY` (n=1–3) |
| 4 | `who-briefs-gap-top` | 70px gap | — |
| 5 | `who-briefs` | Looping mp4 left (2/3), dark panel right (1/3): heading, intro, three icon items, outro | `VIDEO_MP4_URL`, `VIDEO_POSTER_URL`, `VIDEO_ARIA`, `PANEL_TITLE/KICKER/INTRO/OUTRO`, `PANEL_ITEMn_ICON/TITLE/TEXT` (n=1–3) |
| 6 | `who-briefs-gap-bottom` | 70px gap | — |
| 7 | `mechanics` | Six-idea scatter circles (`.pm`) | `CIRCLES_KICKER/TITLE/SUB/FOOT`, `CIRCLES_IMG_BASE`, `CIRCLEn_TITLE/IMG/BODY` (n=1–6) |
| 8 | `who` | Who commissions work like this, two 1/4 columns | `WHO_TITLE/KICKER/COL1/COL2` |
| 9 | `the-day` | Six-step timeline rail (`.uc`), one panel at a time, image right | `TIMELINE_TITLE/KICKER/ARIA`, `STEPn_WHEN/LABEL/TITLE/BODY/CRAFT/IMG_URL/CAPTION` (n=1–6), `ID_SLUG` |
| 10 | `words` | Why Oddtoe likes this brief — the bit that is not a service | `WHY_TITLE/KICKER/COL1/COL2` |
| 11 | `carried-and-travelled` | Giant heading pair with a floating object either side | `DIV_RIGHT_TITLE/KICKER`, `DIV_LEFT_TITLE/KICKER`, `DIV_IMG1_URL/ALT`, `DIV_IMG2_URL/ALT` |
| 12 | `what-you-get` | Deliverables, two 1/4 columns (COL1 = bold summary + bullets) | `WYG_TITLE/KICKER/COL1/COL2` |
| 13 | `package` | Five cardboard-box columns | `PKG_TITLE/KICKER`, `PKGn_IMAGE_ID/KICKER/TITLE/BODY` (n=1–5) |
| 14 | `spec` | Six-column spec strip on the canvas | `SPECn_FIGURE` (Qwigley, on top), `SPECn_LABEL` (Bebas, beneath) (n=1–6), `TINT` |
| 15 | `cartoonist` | The authorship credential, two 1/4 columns | `CRED_TITLE/KICKER/COL1/COL2` |
| 16 | `compare` | Otto's styled table: three options across, five rows down | `CMP_TITLE/KICKER/INTRO`, `CMP_COLn_HEAD` (n=1–3), `CMP_ROWr_LABEL`, `CMP_ROWr_Cn` (r=1–5) |
| 17 | — | FAQ accordion + FAQPage JSON-LD + Contact button | `FAQ_KICKER`, `FAQ_TOPIC`, `FAQ[]` (list of `{q, a}`), `FAQ_TAB_STAMP`, `ID_SLUG` |
| 18 | `more` | Portfolio trio + contact circle | `MORE_KICKER`, `MORE_TITLE`, `PORTFOLIOn_ID` (n=1–3) |
| 19 | `form` | Gravity form (id=1) under an h2 + kicker | `FORM_TITLE`, `FORM_KICKER` |

Anchors are row attributes and stay as they are on every page, including `cartoonist` and
`carried-and-travelled` — they are ids, not copy.

## Content JSON

`usecase-content-publicity-stunts.json` is the worked example: every token of the live page, in
place. Copy it, rename it `usecase-content-<url-slug>.json`, and rewrite the values. Extra keys
the compose script reads: `URL_SLUG` (output filename), `YOAST_TITLE`, `YOAST_DESC` (printed for
the handoff, never in the body). Keys that do not change between pages: `FAQ_TAB_STAMP`,
`TINT` (unless Otto picks a tint per page — he has, on every page so far), `CIRCLES_IMG_BASE`.

### Writing rules per slot

- **Headings** are written in sentence case; Bebas uppercases them. Qwigley kickers are sentence
  case and follow the ellipsis rule in `design-kit-README.md` (`...` only when something below
  finishes the thought). Keep `»` and `«` in the divider titles.
- **`INTRO_COL1`** carries the canonical Oddtoe sentence (bold company name, `brands.md` wording)
  and names the page as a use case in its second sentence. Then **`UPDATED`** is its own centred
  line, never folded into a paragraph.
- **Body columns** (`*_COL1/COL2`) are `<span style="font-family: Arvo;">` paragraphs separated by
  blank lines, exactly as the JSON shows. **Balance every pair** before handover (Lesson 11c:
  measure on the preview, both columns within one line). Bold is for keyphrases, never sentences.
- **Circles**: six always. Titles in Title Case (the module renders them as given). Bodies are
  one cheeky paragraph each with one `<strong>` phrase; generic targets, cheap-to-big spread.
  `CIRCLEn_IMG` is a filename under `CIRCLES_IMG_BASE`; images are square crops uploaded with alt
  text. The scatter geometry (`size/left/top`) is the kit's and does not change.
- **Timeline**: six steps always — the problem, design, build, the day, the pickup, the return.
  `STEPn_BODY` is double-quoted JS: no raw `"` (use `&quot;`), apostrophes as `&rsquo;`.
  `STEPn_CRAFT` is single-quoted JS and may carry an `<a href="…">`: no `'` inside it.
- **Package**: five boxes always — Ideation, Visualisation, Feasibility, Fabrication, Project
  Management stay as the titles; kicker and body change to the brief. Box images are the
  shared cardboard-box icon set (16125/16126/16127 + 16319/16320).
- **Spec strip**: `FIGURE` is the number or single word (Five, One, 6–8, Freight), `LABEL` the
  phrase that wraps to two lines. Never a price. Nothing unverified — figures come from the page
  copy or from Otto.
- **Comparison table**: three options a buyer already weighs, five factual rows. Cells are short
  and plain. Column 3 is the built object; make its cells true, not triumphant.
- **FAQ**: 6–8 questions, target phrase in at least three of them, answers with keyphrase bold
  (none over 60 characters). The JSON-LD is generated from the same list as plain text, so the
  visible answer and the schema always match. Pricing question always answers "does not publish
  prices" and links `/prop-fabrication-services/`.
- **Video**: self-hosted mp4 (1280x720 H.264, under 2 MB, looped and muted) with a poster.
  `VIDEO_ARIA` describes the clip in one sentence. No page embeds YouTube.
- **Portfolio trio**: `my-product` items only — the module cannot show a page.

## Page settings and the steps after compose

1. Compose: `python3 scripts/compose-usecase.py references/usecase-content-<slug>.json`.
   The script verifies no token or comment survives and prints the Yoast lines.
2. Draft to WordPress via the money-pages workflow: parent **16296**, template `page-custom.php`,
   author Otto, status draft. Then in wp-admin (REST cannot): Custom background = `TINT`,
   header style **13**, Yoast title and description from the printout.
3. `de-ai-check.py` clean; column pairs measured; hero and circle images carry alt text that
   names no client and no event.
4. **Hub card** on 16296: `scripts/example-compose-oddtoe-usecases-hub.py` `card(image, title,
   subtitle, body, url)` — one card per use case, the in-the-works card becomes the link.
5. **Homepage row** on 15922: relink the matching "See yourself as?" row to the new page (the
   rows are `vc_tta_section`s in the `dfd_accordion`; write the permalink by hand).
6. Link pass and GSC indexing request after publish, per SKILL.md.

## Verification

`compose-usecase.py <json> --verify <master>` decodes the raw blocks on both sides and diffs row
by row. On 11 Sep 2026 the stunts JSON reproduces master 16272 identically in all 19 rows. Run it
after every re-snapshot; if it fails, the kit and the master have drifted.
