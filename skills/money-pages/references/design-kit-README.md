# Design Kit v1 — token reference & workflows

**Source of truth for layout:** `design-kit.html` — tokenized snapshot of Otto's WPBakery/Ronneby dummy page
("MONEY PAGE DESIGN KIT — MASTER (never publish)", page 52964 on datalabsagency.com), taken 14 Aug 2026.
When Otto restyles the dummy, re-snapshot per SKILL.md and re-apply the tokens.

**Rules baked into the kit** (do not undo, final per Otto 14 Aug 2026):
- **Tags carry the typography in Ronneby** — h1–h6 in `dfd_heading` get Bebas (titles) / Qwigley
  (subtitles); `div` kills the fonts. Never retag to div.
- **Exactly one H1 per page**: the hero title. Cross-promo titles are `h2` (renders Bebas identically);
  the hero subtitle is the page's ONLY Qwigley `h2`; every other subtitle is `h3` (also Qwigley).
- **Casing**: Qwigley subtitle text is SENTENCE CASE — capital first letter, lowercase after (per the
  Oddtoe design system's script-accent rule). Never write subtitle content in all caps; the caps in the
  dummy page are just the uppercase token names. Bebas uppercases titles on its own, so title/heading
  token content is also written in sentence case.
- The FAQ topic line is a real `<h2>` (inline-styled span keeps its look). Body copy is NOT wrapped in
  blanket `<strong>` — bold is reserved for keyphrases and numbers per the geo-playbook.

## Token replacement

Tokens look like `{{NAME}}` or `{{NAME: inline spec}}`. Replace with regex `\{\{NAME(:[^}]*)?\}\}`.
Tokens inside shortcode **attributes** are always bare (no inline spec) — their specs live here.
Never alter row/column/styling attributes; content goes only where tokens are.

| Token | Where | Spec |
|---|---|---|
| `{{PAGE_TITLE}}` | hero H1 | Primary keyword phrase, 2–5 words |
| `{{PAGE_SUBTITLE}}` | hero, above H1 (div) | 3–6 word lead-in |
| `{{UPDATED_DATE}}` | hero | Month Year, e.g. "August 2026" — only bump with a real content update |
| `{{HOOK}}` | hero | 40–60 words, page promise, core number/claim in first sentence, 2–3 `<strong>` keyphrases |
| `{{SECTION_A_HEADING}}` / `{{SECTION_A_SUBTITLE}}` | hero section A | H2 phrased as the page's core question (include keyword) / short lead-in |
| `{{SECTION_A_INTRO}}` | hero section A | 40–60 words, direct answer, real numbers, price range in first sentence |
| `{{CANONICAL_SENTENCE}}` | hero section A | Brand canonical sentence from `geo-playbook/references/brands.md` VERBATIM |
| `{{SECTION_B_HEADING}}` / `{{SECTION_B_SUBTITLE}}` | hero section B | Second most important buying question |
| `{{SECTION_B_ANSWER}}` / `{{SECTION_B_CONTEXT}}` | hero section B | 40–60 word standalone answer / 75–300 words support |
| `{{PRIMARY_CTA_TEXT}}` / `{{PRIMARY_CTA_URL}}` | hero button | 2–4 word action / **URL-encoded** target (`https%3A%2F%2F...`) |
| `{{FAQ_TOPIC}}` | FAQ h2 | Keyword topic of the Q&A block |
| `{{FAQ_Q1..5}}` / `{{FAQ_A1..5}}` | accordion + JSON-LD | Question in natural search language / 2–3 sentence standalone plain-text answer |
| `{{FAQ_CTA_TEXT}}` / `{{FAQ_CTA_URL}}` | FAQ button | As primary CTA; URL-encoded |
| `{{SECTION_C_*}}` | section variant 1 | HEADING, SUBTITLE, ANSWER (inclusions), DETAIL (has internal link) |
| `{{SECTION_D_*}}` | section variant 2 | HEADING, SUBTITLE, ANSWER (the rule), RATIONALE (why — quotable) |
| `{{ARTICLE_1_HEADING/SUBTITLE/BODY}}` | article slot 1 | 300–700 words, multiple `<p style="line-height: 22px; text-align: left;">`, first-person Otto voice, E-E-A-T, 1–2 internal links |
| `{{ARTICLE_2_HEADING/SUBTITLE/BODY}}` | article slot 2 | Same shape; may go deeper/more technical |
| `{{TABLE_HEADING/SUBTITLE/INTRO}}` | table row | Section head / lead-in / one-sentence table explainer |
| *(table)* | table row | No token — the kit contains TWO fully styled exemplar `<table>`s to copy exactly (the `!important` flags are mandatory — Ronneby's table CSS overrides plain inline styles). Keep `scope="col"`; `overflow-x` wrapper stays (horizontal scroll on mobile, never stacked rows). Oddtoe: accent `#c39f76` → `#ddccb1` |

**Table defaults (Otto approved, 14 Aug 2026):**
- **Pricing exemplar** (first table): black cells, Bebas `th` with tan underline, zebra `#111111` rows, bold row labels, right-aligned bold tan price in the LAST column.
- **Comparison exemplar** (second table): criterion column + 2–3 option columns; the RECOMMENDED option gets a tan `th` (black text) and `#111111` cells — no zebra, no badges. Checkmark cells: tan `✓` / dim `—` (`#8a8a95`), centered; never a red cross.
- **Footnote**: small italic dimmed line inside the table block, right under the table (GST, travel, minimums).
- **Compact variant** (8+ rows): padding `8px 14px`, `font-size: 15px`, same palette.
- **Prices**: `$4,500 AUD` on first mention then `$4,500`; ranges use an en dash (`$3,000–$5,000`); `From $X` only where a floor is honest.

## Composing a page (repeat/omit patterns per page-types.md)

- Patterns are the top-level `[vc_row]` blocks, labelled with HTML comments and `el_id="pat-*"`.
- **Strip all HTML comments** before sending content to WordPress (WPBakery can mangle stray text between rows).
- Repeatable: section variants, table row, article rows. One per page: intro (only H1), FAQ.
- FAQ: 4–8 Q&As. To add Q6+, duplicate a `vc_tta_section` with a NEW unique `tab_id` and add `FAQ_Q6/FAQ_A6` to the JSON-LD too.
- Everything below the "FIXED FOOTER BLOCKS" comment ships as-is (Otto, 14 Aug 2026).

## FAQ JSON-LD (the `[vc_raw_html]` block)

`vc_raw_html` content is `base64_encode(rawurlencode(html))` — URL-ENCODE FIRST, then base64 (WPBakery
decodes `rawurldecode(base64_decode(x))`; the reverse order renders mojibake `��` on the page). The kit
ships it pre-encoded with bare `{{FAQ_Qn}}/{{FAQ_An}}` tokens inside; `faq-schema-decoded.html` is the
readable copy. Per page:
1. Start from `faq-schema-decoded.html`; fill the tokens with the SAME text as the accordion (plain text, no HTML).
2. Adjust the number of Question entries to match the accordion.
3. Re-encode: `python3 -c "import base64,urllib.parse,sys;print(base64.b64encode(urllib.parse.quote(sys.stdin.read().strip(),safe='').encode()).decode())" < filled.html`
4. Replace the `[vc_raw_html]...[/vc_raw_html]` payload.

## Site-specific swaps (Datalabs → Oddtoe)

The kit is the Datalabs instance. For Oddtoe, swap (all are Datalabs media/form IDs):
- Hero row background `dfd_bg_image_new="25838"`; hero image `52827`
- Offers row: both `info_banner` cards (images 39363/39429, links, titles) → Oddtoe equivalents
- Fixed footer: parallax banner (layer_image 35828, heading text + subtitle), cross-promo images (52527),
  Otto photo 24350, client logo carousel IDs, `gravityform id="1"`
- An `oddtoe` variant of this kit should be snapshotted from an Oddtoe-styled dummy page when one exists.

## Publishing

Per SKILL.md: drafts only (never publish), author = Otto, Yoast comment block at top of draft body,
`scripts/wp-post.sh <site> "<Title>" <file>` with Application Passwords in `.env` — or hand Otto the
composed markup to paste into a new page's Text tab if credentials aren't set up.
