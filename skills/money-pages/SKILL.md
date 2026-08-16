# Money Pages

Use this skill when Otto asks for the next money page, a pricing page, a comparison, a case study, or the credits page — or clicks the "Next money page" quick action. These pages answer buying questions AI assistants get asked ("who can train my team", "what does X cost"), which is where a recommendation becomes a lead.

## Workflow

1. **Load the contract.** Read the `geo-playbook` skill: the six rules, `references/brands.md`, `references/banned.md`. The active brand comes from Otto's brand toggle or his message; if ambiguous, ask which brand.
2. **Pick the page.** Take the top unchecked item for that brand from `references/backlog.md`, unless Otto names one.
3. **Interview for facts only.** Ask Otto ONLY for what the brand file marks `TO FILL` or what the page type needs and brands.md lacks (real prices/ranges, nameable clients, project details, outcomes). Rough answers are fine — turn "about 5k a day, less remote" into clean copy. Never invent; if Otto declines a number, use a bracketed range he approves or restructure the page to not need it.
4. **Write per the playbook** using the matching template in `references/page-types.md`. Australian spelling. Include "Updated [Month Year]".
   **Layout:** generate the draft INSIDE the WPBakery design kit (`references/design-kit.html` — Otto's styled patterns with `{{TOKEN}}` slots; token specs and compose rules in `references/design-kit-README.md`). Fill the tokens, repeat/omit patterns per page type, never alter row/column attributes or styling.
5. **Top of the draft body**, include an HTML comment block with the Yoast fields for manual paste:
   `<!-- YOAST SEO TITLE: ... (max ~60 chars) | META DESCRIPTION: ... (max ~155 chars) -->`
6. **Push as a draft.** With shell access, run `scripts/wp-post.sh <datalabs|oddtoe> "<Title>" <html-file>` (requires WP Application Passwords in the repo `.env` — see docs/WORDPRESS_AUTOMATION_CHECKLIST.md). Without shell access, output the complete page + Yoast block for Otto to paste into WordPress himself. NEVER publish — drafts only (banned.md rule 4).
   **Page settings (learned 14 Aug 2026):** design-kit pages depend on three page-level settings the content itself can't provide — `template: page-custom.php` (wp-post.sh sets it via REST; kills the theme title band + boxed width), and two Ronneby meta fields REST can NOT set: **Custom background color `#2f2e3a`** and **header style `2`** (`crum_page_custom_bg_color` / `dfd_headers_header_style` in the page's wp-admin settings). Without the background, `bg_check="row-background-dark"` rows render white text on a white page — invisible. Set them in wp-admin (or via browser automation) right after the draft is created.
7. **Update the backlog.** Mark the item `[~]` with the wp-admin edit link:
   `- [~] Workshop pricing page (datalabs) — [review](https://www.datalabsagency.com/wp-admin/post.php?post=ID&action=edit)`
   When Otto says he has published it, mark it `[x]` and suggest running offsite-consensus for it.

## Authorship: the agent drafts, Otto authors

Public content is attributed to **Otto Ottinger**, never to the content-agent user. AI assistants treat a real, named author (with his existing Person schema and LinkedIn) as a trust signal; an obvious bot byline undermines citation. When creating the draft via REST, set the `author` field to Otto's own user ID on that site if known; otherwise remind Otto in the handoff message to flip the **Author** dropdown to himself in the editor before publishing (one click, in the page's settings panel). Pages rarely display bylines in the current theme, but posts do — this rule applies to both.

## Backlog format (parsed by the app's Content pipeline card — keep exactly)

- `- [ ] Title (datalabs)` — queued
- `- [~] Title (oddtoe) — [review](url)` — draft awaiting Otto's review
- `- [x] Title (datalabs)` — published

## The Otto-designed WPBakery template (and the PUBLISH HOLD)

**⛔ HOLD: no money page goes live until Otto's WPBakery template v1 exists.** Drafts may be created and reviewed, but do not suggest publishing, and remind Otto of the hold if he seems about to publish before the template is ready. (Otto's instruction, Aug 2026.)

The asset pipeline:

**Model (Otto's call, Aug 2026): Otto designs a PATTERN KIT, the agent composes pages from it.** Not a fixed page skeleton — page types differ too much (a comparison page is five tables; a case study is mostly narrative). Otto designs what each building block looks like; the agent assembles blocks per page type.

1. **Basis:** a master page with one of each building block as raw `[vc_row]` markup was delivered Aug 2026 (now titled "MONEY PAGE DESIGN KIT — MASTER (never publish)", Datalabs page 52964): intro row, question-section rows, table row, article rows, FAQ row, plus fixed footer blocks. Otto styles each row in WPBakery — he is designing the *patterns* (what a table/CTA/section looks like), not one page. Styling rules that must survive: real `<h2>/<h3>` tags, real `<table>` HTML, all text as text, ONE `h1` per page (the hero title). **Heading tags are load-bearing for typography (14 Aug 2026): Ronneby styles Qwigley subtitles and Bebas titles BY TAG (`div` kills the fonts). Agreed final tag map: hero = h1 with the page's only Qwigley h2 subtitle; all other subtitles h3; cross-promo titles h2. Qwigley subtitle text is always sentence case (capital first letter only), per the Oddtoe design system.** **FAQ (updated 14 Aug 2026, supersedes the earlier flat-FAQ rule):** the styled `dfd_accordion` block with 4–8 Q&As plus a `[vc_raw_html]` FAQPage JSON-LD block (Ronneby renders accordion content server-side, so the text stays crawlable; the JSON-LD gives AI assistants the structured copy).
2. **Snapshot into the kit:** DONE for v1 (14 Aug 2026) — `references/design-kit.html`, tokenized with `{{TOKEN}}` slots and pattern labels; specs in `references/design-kit-README.md`. When Otto restyles the dummy, re-fetch its RAW content (authenticated GET, `context=edit`), re-apply the tokens, and overwrite the kit.
3. **Compose per page type:** every draft is assembled by repeating, re-ordering, and omitting kit patterns to fit the page structure in `references/page-types.md` — e.g. a comparison page reuses the table pattern five times. Content goes into the blocks; Otto's row/column styling attributes are NEVER altered. Drafts arrive in wp-admin already in his look-and-feel, and Otto retains full liberty to further art-direct any individual page in WPBakery afterwards (the agent must not overwrite his per-page styling on later edits — re-fetch raw content before any update).
4. **Kit updates:** when Otto restyles the dummy (or adds new patterns to it), re-snapshot → the next drafts pick the changes up. New pattern ideas (e.g. a highlight band, a testimonial row) get added to the dummy first, then re-snapshotted.
5. **Retrofit + lifting the hold:** the workshop pricing page (draft 52962) gets recomposed from the kit before Otto reviews it; once he publishes it, the hold is lifted and the normal flow resumes (publish → link pass).

## Page type, URLs, and ownership (agreed with Otto, Aug 2026)

- **Money pages are WordPress PAGES, never posts** (no dated URLs; freshness = the visible "Updated [Month Year]" line). Think pieces and timely articles are posts — those are Otto's, not the agent's. Case-by-case exceptions only if Otto says so.
- **Flat slugs** (e.g. `/data-visualisation-workshop-pricing/`) — no provenance folder, no "/geo/" section. Agent-drafted pages must be first-class site citizens; provenance is tracked internally, never in the URL.
- **Edit fence: the agent may only edit pages/posts listed in `references/backlog.md` or `references/links-ledger.md` (and there only the recorded edits).** Everything else on both sites is READ-ONLY. Otto's think pieces and custom pages are never touched without his explicit per-edit approval.
- After publish, record the page ID + URL on the backlog line — the backlog is the ownership ledger.

## Retrospective link pass (after each money page publishes)

An orphan page gets crawled (Yoast sitemap) but not weighted; internal links do the ranking and citation work. So after Otto publishes a money page:

1. Run discovery (read-only): `python3 scripts/link-pass.py plan <brand> --target <page-id> --keywords <topic words>` — ranks existing published pages/posts as link sources and shows candidate sentences.
2. The agent drafts an **edit plan** (max 5 edits): exact search/replace pairs adding one contextual link each, descriptive anchor text, into the top 2–4 relevant sources. Present it to Otto with before/after text.
3. **Otto approves the specific plan** (this edits HIS pages — the fence requires it), then `"approved": true` goes into the plan JSON and `scripts/link-pass.py apply <brand> --plan <file>` applies it. Exact-match only: if a page changed since planning, the edit is skipped, never guessed. **Plan-first is Otto's standing default (14 Aug 2026): even a casual "put the links in" or "let's link" is NOT blanket approval — always show the exact before/after edits and wait for his yes on that plan. Preferred mechanism (16 Aug 2026): present the plan as a multi-select question in the Q&A interface (one option per edit, exact wording in the description) so Otto can approve all or a subset in one step.**
4. Applied links are recorded in `references/links-ledger.md` (append-only). If Otto removes a link, mark it "(removed by Otto)" — never re-add.
5. Standing targets beyond in-body links (Otto handles in wp-admin): the footer "Pricing & Guides" block, and optionally one submenu entry for genuinely commercial pages (e.g. Workshop Pricing under Data Training).

**Link-pass field notes (learned 14 Aug 2026, first run):**
- **Verify the anchor RENDERS before planning it.** WPBakery keeps rows with `disable_element="yes"` in raw content — the discovery script sees them but they never render (the homepage 167 has whole legacy sections like this). Check the sentence exists in the live page's DOM/HTML, not just the raw.
- **WP rewrites hrefs on save** (pretty URL → `/?page_id=N`), and it renders them back pretty. The apply script compares href-agnostically for idempotency (fixed same day; a literal compare caused duplicate sentences).
- **Style new in-content links inline**: `<a style="color: #c39f76;" href=...>` (Oddtoe: `#ddccb1`). The theme's link colour is context-dependent and plain links can render white-on-dark (invisible).
- **After the pass, request indexing for the EDITED source pages too** (Google Search Console URL inspection; Bing picks up via sitemap lastmod) — the new page was submitted at publish, but Google finds the internal links faster when the changed sources are resubmitted.
- WAF note: REST calls (GET and POST) need a browser-like User-Agent — generic client UAs get 403s.

## Guardrails

Everything in geo-playbook `banned.md` applies. One page = one brand. After the site publishes, remind Otto the Cloudflare cache holds HTML ~4 hours — verify with a cache-buster URL, or purge.
