# Design Kit v1 — token reference & workflows

## Two kits, one token set

- **Datalabs**: `design-kit.html` — v1, Otto-styled, snapshot of Datalabs page 52964. Accent `#c39f76`.
- **Oddtoe**: `design-kit-oddtoe.html` — **v1 (re-snapshot 14 Aug 2026, Otto-styled)** from Oddtoe master
  page 16132. Accent warm sand `#ddccb1`; page + rows plum `#26161f`. Required page settings for every
  composed Oddtoe page: template `page-custom.php`, `crum_page_custom_bg_color=#26161f`, bg repeat,
  `dfd_headers_header_style=6`. Offers row = info_banner cards (swap per page); footer = delimiter +
  project-enquiry Gravity form (id=1). Oddtoe pricing facts are still TO FILL (see brands.md) — no
  Oddtoe page may quote a price until Otto provides ranges.
  Tokens are identical across both kits; everything below applies to both unless an accent/ID is named.

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

## The ellipsis rule — Qwigley lead-ins only (Otto, 24 Aug 2026)

A Qwigley lead-in either **stands on its own** or it **doesn't**. The ellipsis marks the ones that don't.

**Use `&hellip;` when something below finishes the thought.** Two shapes qualify:

1. **It runs into the Bebas headline.** The lead-in is a grammatical fragment the title completes.
   `So you want an&hellip;` → **ANIMATION AGENCY** · `Interested in seeing more&hellip;` → **INSTALLATION WORK?**
2. **It hands over to the content.** The lead-in names a thing the section is about to deliver.
   `What to send&hellip;` · `More from the Oddtoe studio&hellip;` · `Two workshops that Otto facilitates&hellip;`

**No ellipsis when the lead-in is already complete** — it closes its own thought and nothing is pending:

| Lead-in | Why no ellipsis |
|---|---|
| `Which one is your brief?` | a question; the `?` already closes it |
| `Why one team beats twelve` | a claim, complete as written |
| `Two words, two different jobs` | a label, complete as written |
| `The short version` | a label for what follows, not a promise of it |

The test: read the lead-in aloud and stop. If it sounds finished, no ellipsis. If it sounds like you were
interrupted, that is the ellipsis.

**Constraints**
- **Two per page maximum, counting only lead-ins you write.** It is a spice; if every lead-in trails,
  none of them read as trailing. The kit's two fixed trailing lead-ins — the cross-promo delimiter
  (`More from the Oddtoe studio&hellip;`) and the enquiry-form subtitle (`Tell us what you are
  imagining&hellip;`) — are furniture that ships on every money page and sit outside the count — it is far down the page
  and separated from the heading stack, so it does not compete with a hero or article lead-in.
- **Never on a Bebas headline or an H1** — titles do not trail, only lead-ins do.
- **Never alongside a question mark.** Pick one.
- **Character: `&hellip;`, never three full stops.** Three dots can break across a line and render with
  uneven spacing; the entity is one glyph with correct kerning. (Legacy pages still carry `...` — convert
  on next edit, do not sweep the site for it.)
- No space before; one space after only if text continues on the same line.
- Sentence case as always — the ellipsis does not change the casing rule.

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

**Table defaults (Otto approved, 14 Aug 2026; cell-content rule added 16 Aug 2026):**
- **Cells are factual, never poetic (Otto's general rule):** every cell carries a concrete, comparable
  fact in plain words a buyer immediately understands ("Weeks to months", "Changes from shot to shot") —
  no metaphors, wordplay, or clever fragments ("Rarely survives one" ✗). Criteria labels should be
  tangible questions a buyer would ask. Poetry belongs in prose, not tables. Also avoid unexplained
  jargon anywhere ("campaign loops" ✗ → "social video").
- **Pricing exemplar** (first table): black cells, Bebas `th` with tan underline, zebra `#111111` rows, bold row labels, right-aligned bold tan price in the LAST column.
- **Comparison exemplar** (second table): criterion column + 2–3 option columns; the RECOMMENDED option gets a tan `th` (black text) and `#111111` cells — no zebra, no badges. Checkmark cells: tan `✓` / dim `—` (`#8a8a95`), centered; never a red cross.
- **Footnote**: small italic dimmed line inside the table block, right under the table (GST, travel, minimums).
- **Compact variant** (8+ rows): padding `8px 14px`, `font-size: 15px`, same palette.
- **Prices**: `$4,500 AUD` on first mention then `$4,500`; ranges use an en dash (`$3,000–$5,000`); `From $X` only where a floor is honest.

## Lessons from the Animation Agency build (24 Aug 2026) — read before composing

Six things that cost a review round each. All were caught by Otto, none by the QA script at the time.

**1. The table row is a `1/3` column. Four columns overflow it.**
`pat-table` puts its content in the middle of a `1/3 + 1/3 + 1/3` inner row. The kit's own exemplars are
three columns wide and fit. A four-column comparison table does NOT — Ronneby's `overflow-x` wrapper does
its job and you get a horizontal scrollbar on desktop.
**Rule: 3 columns → leave the row alone. 4+ columns → widen that inner row to `1/6 + 2/3 + 1/6`** (the split
the Installation Artist page uses). Scope the change to the table row only; other rows keep their `1/3`s.
*(Not changed in the master — the `1/3` is Otto's art direction and is right for 3 columns. Ask before
making `2/3` the default.)*

**2. Oddtoe pages must DELETE the pricing exemplar.** `brands.md` has Oddtoe pricing as `TO FILL`, so no
Oddtoe page may quote a number. The kit ships two tables; drop the first, keep the comparison, and replace
the price footnote with a "quoted per project" line. Datalabs pages keep both.

**3. Bolding the FAQ leaks markup into the FAQPage JSON-LD.** The accordion and the schema are filled from
the SAME token. House style requires keyphrase bolding in answers; schema requires plain text. **Strip tags
on the way into the JSON-LD** — a `plain()` helper on the token value, applied only in the `vc_raw_html`
re-encode. Verify by decoding the payload and asserting no `<` in any `acceptedAnswer.text`.

**4. Article slots are FIRST PERSON and nothing enforces it.** The token table says "first-person Otto
voice" and it is easy to miss — the first Animation Agency draft was entirely third person ("Oddtoe takes a
brief... the client gets one contact") and read as brochure copy. Write "I take a brief... you get one
contact". Brand statements stay "Oddtoe"; judgement statements are "I".

**5. Nothing checks bold density.** The first pass had 17 of 27 paragraphs with zero emphasis, and 11 of the
13 `<strong>` spans were links (which are `<strong>`-wrapped by convention and inflate the count without
doing any scanning work). **Count keyphrase bolds separately from link bolds**, and target 2–5 per paragraph.

**6. Read every link sentence aloud before applying.** An exact-match keyword anchor placed straight after a
verb reads as a caption, not prose: *"Hiring rather than pitching? See animation agency."* is not a sentence.
Give the link a noun to attach to — "the animation agency **page**", "works as an **animation agency**" — or
rebuild the clause. Exact-match, render-verified and live-verified all passed on that sentence; only reading
it caught it.

## Lessons from the Character Design Services build (24 Aug 2026, page 16208)

Four more, all caught by Otto in draft review.

**7. `width=` alone does NOT widen a column that carries an `offset=` attr.** The hero and section inner
columns ship with `offset="vc_col-lg-4 vc_col-md-…"` — the lg class **overrides** `width` at desktop sizes,
so changing `width="1/3"`→`"1/2"` renders no change. **Change the `vc_col-lg-N` in `offset` to match**
(1/2→lg-6, 2/3→lg-8, 1/4→lg-3, 1/6→lg-2). The kit's table row has no offset attr, which is why lesson 1's
width-only fix worked there.

**8. Long heading tokens wrap 4–5 lines in `1/3` columns.** "What does a character design service actually
do?" is far longer than the animation-agency equivalents. When the page's head noun is long (3+ words),
widen the hero and section inner rows from `1/3+1/3+1/3` to `1/4+1/2+1/4` (offsets too, per lesson 7).

**9. A 3-column table can still overflow — check, don't count columns.** Lesson 1's "3 columns → leave
alone" failed here: three columns with sentence-length cells scrollbarred anyway. Widen to `1/6+2/3+1/6`
whenever the rendered table overflows, regardless of column count.

**10. Long article bodies get Otto's TWO-COLUMN treatment, and the "More from…" delimiter needs its
Qwigley attrs.** (a) An article body in the `4/6` slot renders as one ~800px-wide block — too wide to read.
Otto's rule: past ~4 paragraphs, split the body at a `</p>` boundary into `[vc_row_inner]` with two `1/2`
columns of `vc_column_text`. (b) Compose the "More from the Oddtoe studio&hellip;" delimiter EXACTLY as the
kit ships it — `custom_fonts="font_family:Qwigley…" use_google_fonts="show" title_font_options=…` and
`&hellip;` not `...` — and keep the spacer under it at 20px (not 50) so the cards sit close.

## Lessons from the Dashboard Design Services review (25 Aug 2026, page 53840)

**11. The overnight builder composes from the KIT, not from this file — lessons do not apply themselves.**
53840 shipped with `1/3+1/3+1/3` intro and section rows, single-column 5-paragraph articles, and a plain
`...` delimiter: lessons 7, 8 and 10 all missed, on a page whose main heading ("What does a dashboard
design service actually do?") is the near-twin of the one lesson 8 was written for. **Run this checklist
against every composed draft before pushing it**, whether a human or the 05:00 task assembled it:
head noun 3+ words → widen hero/section inner rows to `1/4+1/2+1/4` (offsets too, lesson 7);
article body past ~4 paragraphs → two `1/2` columns (lesson 10a); table renders wider than its column →
`1/6+2/3+1/6` (lesson 9); every `...` → `&hellip;`.

**12. Zero ellipses is under-applying the rule, not playing it safe.** The cap is two per page; 53840
had none. The hero is the natural home for shape 1 — a fragment the Bebas H1 completes
(`So you need&hellip;` → DASHBOARD DESIGN SERVICES). Spend the second one on an article lead-in that
genuinely hands over (`Stage by stage&hellip;`), and leave the complete labels alone.

**13. The Datalabs cross-promo delimiter is Qwigley (Otto, 25 Aug 2026).** `Two workshops that Otto
facilitates&hellip;` now carries the same attrs as the Oddtoe one —
`custom_fonts="font_family:Qwigley%3Aregular|font_style:400%20regular%3A400%3Anormal"
module_animation="transition.expandIn" use_google_fonts="show" title_font_options="font_size:30|line_height:38"`.
`design-kit.html` is updated, and the three legacy `...` footer subtitles in it converted to `&hellip;`.
**25 Aug 2026: the kit itself now carries the 20px spacer under the cross-promo delimiter** (was 50 — lesson 10b existed but the kit still shipped the old value; Otto flagged the gap again on the case-study batch).
**⚠ Master page 52964 still ships the plain version** — re-snapshotting the master before Otto restyles
that delimiter in WPBakery will regress both changes.

**14. A two-column split will not balance, and that is fine.** 53840's articles split 3|2 into columns of
650px/347px and 606px/369px; the alternative 2|3 splits were no better. Keep the 3|2 the Character Design
page established — the ragged bottom sits on the right, which is what a reader expects.

## Composing a page (repeat/omit patterns per page-types.md)

- Patterns are the top-level `[vc_row]` blocks, labelled with HTML comments and `el_id="pat-*"`.
- **Strip all HTML comments** before sending content to WordPress (WPBakery can mangle stray text between rows).
- **Spacers stay merged (Otto's rule, 16 Aug 2026):** consecutive `dfd_spacer` elements are collapsed into
  ONE spacer with per-breakpoint sizes summed (pixel-identical render, cleaner markup). `scripts/merge-spacers.py`
  does this safely (aborts unless spacing totals and all non-spacer content are preserved) — run it after any
  master re-snapshot, and never compose pages with back-to-back spacers.
- After Otto re-saves a master in WPBakery, wpautop may inject stray `</p>` fragments right after `[vc_column_text]` tags in the snapshot — when composing, replace a block's FULL inner content (regex across `.*?` to `[/vc_column_text]`), never anchor on exact whitespace.
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


## Lesson 11 — balance the two-column body by RENDERED HEIGHT, not character count (Otto, 26 Aug 2026)

Otto's rule for the lesson-10 two-column treatment: **both columns should come out roughly the same
depth.** It is an aesthetic requirement, not a nicety — a 63/37 split looks like a mistake.

Splitting the body at the midpoint by character count is NOT enough. On the Interactive Annual Report
page (54005) a 49/51 character split still rendered 435 vs 496 px, because:

- the column with **3 paragraphs carries an extra paragraph margin** the 2-paragraph column does not;
- **bold runs and links wrap wider** than plain text, so equal characters ≠ equal lines.

**Method that works — measure, then tune the copy:**

1. Split at a `</p>` boundary so reading order still runs col1 top-to-bottom, then col2.
2. Push, then measure the real thing in the browser:
   `document.querySelectorAll('.wpb_text_column')` → `getBoundingClientRect().height` for each half.
3. Convert the gap to characters: at the kit's column width roughly **1px of height ≈ 1 character
   moved across** (moving x chars grows one side and shrinks the other, so the gap closes ~1.04x).
4. Do not cut mid-sentence — the halves are separate `vc_column_text` blocks. Instead **lengthen a
   sentence on the short side and trim one on the tall side** by that many characters.
5. Re-measure. Target **under ~5% / under one line** of difference.

Result on 54005: 435/496 and 391/452 px → **479/474 (1%)** and **413/430 (4%)**.

Mobile is unaffected — the columns stack, so this only governs desktop.


## Lesson 12 — the footer enquiry form is NOT fixed furniture: tailor its heading and CTA (Otto, 26 Aug 2026)

The "FIXED FOOTER BLOCKS" note says everything below it ships as-is. **One exception: the enquiry-form
row's heading and subtitle.** They must be rewritten to the page's topic on every page.

Shipping them untouched is a real defect, not a cosmetic one. The Datalabs kit's stock copy is a
**speaker-booking** ask — `Looking for a speaker for your event?` / `Professional & Thought-provoking`
— so the Interactive Annual Report page (54005) spent its entire final CTA inviting speaking gigs from
readers who had just been convinced to rebuild their annual report. The page argued one thing and asked
for another.

**What to change (and only this):**

- the `dfd_heading` **title text** — a question naming the specific job the page just described;
- the `subtitle` **attribute** — the Qwigley lead-in that hands over to the form.

Leave the row, spacers, `dfd_heading` attributes, column widths and `[gravityform id="1"]` exactly as
they are. Same form, same styling — new words.

**How to write the pair**

| Slot | Shape | Example (54005) |
|---|---|---|
| Heading (h2, Bebas) | A question that states the reader's current problem in their words, not the service name | `Still publishing your annual report as a PDF?` |
| Subtitle (h3, Qwigley) | Sentence case, the concrete first step, ends in `&hellip;` because it hands over to the form | `Send us the one you already have&hellip;` |

The enquiry-form subtitle is kit furniture and stays **outside** the two-ellipsis-per-page count (see
the ellipsis rule above), so it may trail even when a hero or article lead-in already does.

**Never promise a service `brands.md` does not list.** The first version of the 54005 CTA left AI out,
because at the time the Datalabs service list did not include it and the page body made no AI claim —
inventing an offer is banned.md rule 3. Otto then confirmed (26 Aug 2026) that **AI-assisted annual
reports are real**, it was added to `brands.md`, and only then did the CTA become:

> **Turn last year's PDF into an AI-assisted report** / *Send us the one you already have&hellip;*

That is the sequence to repeat: **confirm → record in `brands.md` → then write the claim.** Otto's
direction is to infuse AI across every product and service, so this list will grow — but AI may only be
attached to a *specific* service once that service is named as real in `brands.md`. The general brand
positioning line ("The Data Design Firm for AI & Visualization") may always be echoed.

---

## Lesson 13 — every Oddtoe money page gets its own near-black (26 Aug 2026)

The kit ships plum `#26161f`, and after four pages Otto's verdict on the result was blunt:
"I'm bored of the dark purple repetition." Visual Case Studies had already solved this for
Datalabs (`vcs_lib.apply_theme`), so Oddtoe money pages now do the same.

Run `scripts/oddtoe_theme.py:retint(content, 'teal')` on the composed body **before** pushing,
then set `crum_page_custom_bg_color` to the same hex in wp-admin Page Options — that field is
Ronneby post meta and is not exposed over REST, so it is always a manual step. Palette,
assignment table, and the full list of tint anchor points live in `design-language.md`.

Two things worth knowing before you touch it:

- **Row backgrounds get stripped, not recoloured.** The three `pat-article-1`,
  `pat-article-2`, and `related-workshops` rows carry a `css=".vc_custom_N{background-color:
  …}"` attr identical to the page ground. Deleting it leaves the ground as the single source
  of truth, so the next tint change is one wp-admin field instead of a re-compose.
- **The kit's scroll-down delimiter was lavender.** `delim_line_color="#8224E31C"` /
  `icon_color="#EEE6F6"` / `icon_hover_color="#D4C9E0"` were leftovers from the v0 seed that
  survived the v1 snapshot — faint enough on plum that nobody caught them, and part of why
  the pages read so purple. The kit is fixed; `retint()` also repairs pages composed before
  the fix.

**Check the draft's Page Options before assuming a tint problem is a tint problem.** Page
16210 was still on `#ffffff` with header style `0` when this ran — the builder had pushed the
draft but the wp-admin settings pass had never happened, which is a different bug wearing the
same clothes.
