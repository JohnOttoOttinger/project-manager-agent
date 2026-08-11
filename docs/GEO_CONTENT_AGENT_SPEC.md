# GEO Content Agent — Build Spec

**For:** AI Solopreneur session, 12 Aug 2026
**Owner:** Otto Ottinger — Datalabs Agency (datalabsagency.com) + Oddtoe (oddtoe.com)
**Feed this file to Claude and say:** "Build the three skills in this spec, starting with Skill 1."

---

## 1. Where we are and what this agent is for

**Done (Aug 2026 foundation work):** clean LocalBusiness/Person schema on both sites, entity fixes, robots.txt/llms.txt hygiene, cache incident fixed + daily canonical monitor, Bing Webmaster verified with sitemaps, Google Business Profile + Bing Places listings for both businesses.

**The gap:** the foundation makes the businesses *findable* to AI assistants (Claude, ChatGPT, Perplexity, Google AI). It gives them almost nothing to *cite*. AI assistants recommend businesses whose pages directly answer buying questions and whose names appear across third-party sources. Neither site has those pages; neither brand has that off-site footprint.

**The business chain this agent drives:**

> Citable page exists → AI assistant retrieves it (Claude→Brave, ChatGPT→Bing, Google AI→Google index) → assistant recommends/links the business → prospect clicks or searches the brand → lead.

Known numbers (2025–26 research): AI referral traffic is small (~0.1–1% of visits) but converts at **2–23x** the rate of organic search visitors; brand **mentions correlate ~3x more strongly** than backlinks with AI recommendations; "best X" answers are drawn almost entirely from **third-party listicles**, not from the brands' own sites.

**Goal, stated plainly:**
- **Datalabs:** be the answer when someone asks an AI "who can train my team in Power BI / data storytelling" or "who should design our dashboards" — selling workshops, consulting, and templates.
- **Oddtoe:** be the answer for "experiential/projection studio Melbourne" and "AI animation studio" — selling installations and commissions.

---

## 2. What to build — three skills

All three follow the existing repo pattern: `skills/<id>/skill.yaml` + `SKILL.md` (+ optional `references/`, `scripts/`), enabled via `skills/enabled.txt`.

Skill 3 (the playbook) is a dependency of Skills 1 and 2 — **build it first in the session**, it's the smallest.

---

### Skill 3 (build first): `geo-playbook` — the shared style contract

**What it is:** not a workflow — a reference skill both content skills MUST load before writing anything. This is how "bake the playbook into the agent" becomes real: the rules live in one versioned file, not in Otto's head or scattered prompts.

**Files:**
```
skills/geo-playbook/
  skill.yaml
  SKILL.md              # the rules below + how to apply them
  references/
    brands.md           # canonical brand facts (see below)
    banned.md           # things never to write/leak
```

**Rules to encode in SKILL.md (non-negotiable for every page/post generated):**
1. **Answer-first:** every section opens with a direct 40–60 word answer under a question-shaped H2/H3 ("How much does a Power BI training workshop cost?"). AI retrieval is passage-level — each section must survive being lifted out alone.
2. **Self-contained sections** of 75–300 words; no "as mentioned above" dependencies.
3. **Named, attributed statistics** ("a 2025 Semrush study of 150k AI citations found…") — never vague "studies show".
4. **Comparison tables** wherever two options are being weighed (AI answers love extracting tables).
5. **Visible dates** ("Updated August 2026") with real content updates behind them.
6. **One canonical definitional sentence per brand**, reused verbatim everywhere (site, GBP, LinkedIn, listicle pitches) so retrieval systems converge on one entity description.

**references/brands.md must contain:**
- Datalabs canonical sentence: *"Datalabs Agency is a Melbourne-based data visualization consultancy founded in 2012 that delivers corporate training workshops (Power BI, Tableau, data storytelling), dashboard design, and BI style guides for clients including Mercedes-Benz, Adidas, and UPS."* (adjust wording once, then freeze)
- Oddtoe canonical sentence: *"Oddtoe is an experiential design and generative-AI animation studio based in Melbourne, creating projection, installation, and animated work for events and venues."* (adjust once, freeze)
- Real client/credit lists per brand, service lists, founder bio line (Otto Ottinger, ex-National Geographic), site URLs, sameAs URLs.
- Entity rule: **Datalabs and Oddtoe are separate businesses.** Never blend them in one page; shared ownership may be mentioned in bios only.

**references/banned.md:**
- Home address (2a Ogrady St) — never in any output. Suburb level only: "Brunswick, VIC" / "Melbourne".
- Personal mobile +61 458 858 825 — never in any output.
- Invented clients, invented statistics, invented reviews or testimonials.
- Publishing directly — everything lands as a WordPress **draft** for Otto's review (see §4).

**Business payoff:** consistency is the mechanism. AI systems build entity confidence from repetition across sources; one frozen definitional sentence repeated across 30 artifacts does more than 30 cleverly varied ones.

---

### Skill 1: `money-pages` — citable commercial pages

**What it does:** takes a page brief + real facts from Otto, produces a complete, playbook-compliant page, and pushes it to the right WordPress site **as a draft** for review.

**Files:**
```
skills/money-pages/
  skill.yaml
  SKILL.md              # workflow: brief → interview → draft → WP push
  references/
    page-types.md       # the four templates below
    backlog.md          # the prioritized page list below
  scripts/
    wp-post.sh          # curl wrapper: create/update draft via WP REST API
```

**Workflow the SKILL.md should enforce:**
1. Load `geo-playbook` rules + brand facts.
2. Ask Otto ONLY for facts the agent can't know (real prices/ranges, real client names it may use, real project details). Never invent these; if Otto won't give a number, use a bracketed range he approves.
3. Write the page per playbook (question-headed sections, answer-first openers, table, dated).
4. Push to the correct site as a **draft** via WP REST API; reply with the wp-admin edit link.
5. Output the Yoast SEO title + meta description as a copy-paste block at the top of the draft (manual paste into Yoast is acceptable at first; automate later only if worth it).

**Page-type templates (references/page-types.md):**
- **Pricing page** — "How much does X cost?" sections per service tier, factors that move price, a table, FAQ.
- **Comparison page** — honest X-vs-Y with a table and a "which should you choose" answer (fine to recommend competitors' tools; the page's job is to be THE cited comparison).
- **Case study** — client/venue, problem, what was built, named outcome, one quotable stat, images with alt text.
- **Credits page** (Oddtoe) — a crawlable text list: project, venue/event, city, year, medium. No design flourish needed; its whole job is machine-readable evidence Oddtoe exists and works.

**Page backlog (references/backlog.md) — priority order:**

*Datalabs (goal: workshop + consulting leads, template sales):*
1. Training workshop pricing ("How much does a corporate Power BI / data-viz workshop cost in Australia?")
2. "Power BI vs Tableau training: which should your team learn?" comparison
3. "How much does dashboard design cost?" consulting pricing
4. 2 case studies (pick clients Datalabs may name publicly — Mercedes-Benz, Adidas, UPS, Rabobank as permitted)
5. "Best data visualization training providers" — honest roundup Datalabs appears in

*Oddtoe (goal: commissions/bookings):*
1. Credits page (all projects, venues, events, years — crawlable text)
2. 2–3 case studies of the strongest installations
3. "How much does projection mapping / an experiential installation cost?" pricing guide
4. "What is generative AI animation?" definitional page owning the term + Oddtoe's take

**Business payoff:** these are the pages AI assistants cite for commercial-intent questions — the queries where a recommendation becomes a lead. Datalabs currently loses "who should train us / what does it cost" answers to competitors with pricing pages; Oddtoe is nearly invisible because its portfolio has no crawlable text evidence. Each published page is a permanent asset that answers a buying question 24/7 across every AI surface at once.

---

### Skill 2: `offsite-consensus` — mentions everywhere Otto can't be bothered to write

**What it does:** generates ready-to-send drafts for the off-site surfaces that actually feed AI retrieval. **Drafts only — Otto sends/publishes everything himself.** The agent never posts, emails, or submits on its own.

**Files:**
```
skills/offsite-consensus/
  skill.yaml
  SKILL.md
  references/
    targets.md          # living list of listicles/directories/subreddits found
    outreach-log.md     # what was sent where, when, result
```

**Draft types it produces (all playbook-compliant, all using the canonical brand sentences):**
1. **Listicle pitches** — find "best data visualization agencies / best Power BI training / best experiential studios Melbourne" articles (WebSearch + Apify for scraping the SERPs), draft a short pitch email per target asking for inclusion, with the canonical sentence + 2 proof points ready to paste. Log targets in `targets.md`.
2. **Review requests** — short personal emails to past clients asking for a Clutch (Datalabs) or Google (both) review, referencing the actual project. Clutch reviews are heavily retrieved for "best agency" queries.
3. **LinkedIn posts** — repurpose each new money page into 2–3 posts (LinkedIn IS retrievable by AI assistants; Instagram/TikTok are NOT — don't spend agent effort there).
4. **YouTube descriptions + transcript cleanups** — the @OddtoeAndDatalabs channel's spoken content is retrievable only if transcripts/descriptions carry the key terms and brand sentences.
5. **Reddit/forum answers** — genuinely useful answers to relevant questions (r/PowerBI, r/dataisbeautiful, r/vfx, event-industry forums) where a Datalabs/Oddtoe mention is honest and non-spammy. Reddit is a top retrieval surface for ChatGPT and Google AI.

**Cadence:** when a money page publishes → immediately generate its LinkedIn posts + check for listicle targets it strengthens. Monthly → one review-request batch, one listicle-pitch batch.

**Business payoff:** this is the ~3x lever. When a prospect asks an AI "who are the best data-viz training providers in Australia?", the answer is assembled from third-party consensus — listicles, review sites, Reddit threads — not from datalabsagency.com. Every mention is a vote. Solo-operator reality: the writing is 80% of the friction, so the agent does the writing; Otto just approves and hits send.

---

## 3. Optional Skill 4 (later): `geo-measurement`

Monthly check: Bing Webmaster **AI Performance (Beta)** report (ChatGPT/Copilot retrievals), GSC queries containing brand names, referral traffic from chatgpt.com / perplexity.ai / claude.ai in analytics, and a spot-check asking each assistant the 5 money questions to see who gets recommended. Output: one short scorecard note. Skip building this until Skills 1–2 have produced ~5 pages — before that there's nothing to measure.

---

## 4. Infrastructure & repos actually needed

Honest answer: **you barely need external repos — the skills ARE the build.** What you need is WordPress write access and the tools already connected.

| Need | Solution | Notes |
|---|---|---|
| Create WP drafts programmatically | **WordPress REST API + Application Passwords** (built into WP core) | wp-admin → Users → Profile → Application Passwords, one per site. Store in `.env` (repo already has `.env.example`). `scripts/wp-post.sh` = ~20 lines of curl. Posts land as `status=draft`. |
| WordPress MCP alternative | Automattic's `wordpress-mcp` plugin (github.com/Automattic/wordpress-mcp) | Optional nicety — evaluate in session only if REST feels clunky. REST + curl is fewer moving parts. |
| SERP/listicle research | **Apify MCP** (already connected) + WebSearch | For finding listicle targets and scraping what competitors' cited pages look like. |
| Publishing verification | curl with cache-buster (pattern already in `oddtoe-canonical-monitor` scheduled task) | Remember: Cloudflare caches HTML ~4h; after Otto publishes a draft, purge or wait before verifying live. |
| Browser fallback | claude-in-chrome MCP (already set up) | Only for things REST can't do (Yoast fields, menus). |
| Repo template for skill structure | none needed — copy the existing `lead-conversion` / `domain-research` skill layout | Keep `skill.yaml` fields identical: id, name, version, description. |

**Caution for the session:** WP Engine + Cloudflare cache both sites' HTML. Any "is it live?" check must use a cache-buster query string, and Oddtoe still runs Yoast 24.5 (older REST surface) — publish as drafts and let Otto hit Publish in wp-admin; don't burn session time automating one-click publishing.

---

## 5. Guardrails (bake into every SKILL.md)

1. **Draft, never publish.** Human review is the quality gate and the safety gate.
2. **No invented facts.** Prices, clients, outcomes, quotes come from Otto or existing site content only.
3. **Privacy:** no home address beyond suburb, no personal mobile, ever.
4. **Entity separation:** one page = one brand.
5. **Outreach is drafted, not sent.** Otto owns the send button on every email/post/submission.
6. **Log everything** (`outreach-log.md`, `backlog.md`) so a solo operator can stop for 3 weeks and resume without archaeology.

---

## 6. Definition of done for tomorrow's session

Realistic scope for one long session:
1. ✅ `geo-playbook` skill complete (rules + brands.md + banned.md).
2. ✅ `money-pages` skill complete with `wp-post.sh` tested against **one** site (Datalabs) — proven by one real draft (suggested: the workshop pricing page) visible in wp-admin.
3. ✅ `offsite-consensus` skill scaffolded (SKILL.md + empty targets/log files); first LinkedIn drafts generated from the pricing page.
4. Stretch: second WP site (Oddtoe) wired; Oddtoe credits-page interview done.

If the session produces one live-ready pricing page and the playbook skill, that already beats 90% of what most people ship — everything after is repetition of a working loop.
