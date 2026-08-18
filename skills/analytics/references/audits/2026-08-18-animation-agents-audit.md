# Animation Agents page — link and freshness audit — 18 Aug 2026

> **Corrected after first pass.** The initial audit read the raw page content and
> counted 10 agencies. Four rows carry `disable_element="yes"` and never render.
> The live page has **6 agencies and 10 agents**. Corrections are at the bottom.

Page 14208 · https://www.oddtoe.com/animation-agents/ · 48,657 chars

**Why this page matters:** it is Oddtoe's biggest traffic asset — **33,161
impressions and 599 clicks** in 180 days, position 18.3, ranking 4.7 for
`animation agent` and 5.5 for `animation agencies`. More clicks than any other
page on the site.

---

## The headline finding

**Not one of the ten agencies is linked.**

All nine outbound links are editorial references — Cartoon Brew, The Hollywood
Reporter, IndieWire, IMDbPro, Oscars, Deadline, Creative Screenwriting, Gotham
Group, Annecy. A guide to animation agents that links to no agent.

Two consequences:

1. **For readers**, the page names people they then have to go and find.
2. **For Otto's outreach plan**, the "you're featured on the page ranking
   top-five for animation agent" opener has nothing to point at. A listing with
   a link is a favour worth acknowledging; a listing without one is harder to
   raise.

---

## Agency status

| Agency | Site | Status |
|---|---|---|
| United Talent Agency (UTA) | unitedtalent.com | live |
| Verve Talent & Literary | vervetla.com | live |
| Summit Talent & Literary | summitalent.org | live |
| Metropolis Talent | metropolistalent.com | live (no `<title>`, JS-rendered) |
| Ritter Talent Agency | ritteragency.com | live |
| Paradigm Talent Agency | paradigmagency.com | live |
| DPN Talent | dpntalent.com | live — **see naming note** |
| **Digital Artists Agency** | d-a-a.com | **DEAD — does not resolve** |
| Natural Talent (Donna Felton) | not found | **needs manual confirm** |
| Annette Van Duran Agency | not found | **needs manual confirm** |

### Naming error

The page says **"Danis, Panero, Nist Talent (DNP)"**. The agency is **DPN** —
the initials are transposed. Their site (dpntalent.com) is live and presents as
a commercial and voice-over agency, which is animation-adjacent through voice
casting rather than animation representation. Worth a sentence of context, or
reconsidering the entry.

---

## Broken and stale links

| Link | Status | Note |
|---|---|---|
| `pro.imdb.com/title/tt9362722/` | **202** | IMDbPro is login-walled; a reader without a subscription hits a wall. Swap for the public IMDb page |
| `aframe.oscars.org/what-to-watch/…` | 200 | redirects to `newsletter.oscars.org` — update to the destination |
| `annecyfestival.com/the-mifa/presentation` | 200 | redirects to `/le-mifa/presentation-mifa` — update |

The other six editorial links resolve cleanly.

---

## Content problems

**The count is wrong.** The intro says:

> "we have a broad array of talent — nine agents from 9 **seperate** agencies"

The page actually lists **10 agencies and 14 named agents**. Also `seperate` is
misspelled, in the intro paragraph of the site's highest-traffic page.

**An unsourced claim.** The intro states:

> "In 2026, UTA agents working in animation signed deals with big studios such as
> Disney, Warner Bros., and Sony Pictures."

No citation. On a page whose whole value is being current and trustworthy, that
line either needs a source or should soften to something defensible.

---

## Agent-level freshness

Only spot-checked, not exhaustive. **Zac Simmons is confirmed still at Paradigm**
and was elevated to partner in its Literary Content division in 2023 — the entry
is accurate and could be strengthened with that detail.

The other 13 agents were not individually verified. Agent moves are the fastest
form of decay on a page like this, and verifying 14 people properly is a separate
pass. Paradigm alone hired two agents in Feb 2026 and parted with three in June
2026, which is the normal churn rate.

---

## Recommended order of work

1. **Link every agency.** Biggest gain for readers, and it is what makes the
   outreach opener land. Nine of ten have a reachable destination.
2. **Fix the count and the typo.** Two minutes, and it is the first paragraph.
3. **Fix DNP → DPN.**
4. **Remove or replace Digital Artists Agency** — its site is gone. Confirm the
   agency still trades before deciding.
5. **Repoint the three stale links.**
6. **Source or soften the UTA deals claim.**
7. **Then** the per-agent verification pass, which is the slow one.

## Note on scope

This audit covers links, agency existence and internal consistency. It does not
verify each agent's current employer, nor whether the roster is the right ten —
both are judgement calls that need Otto's industry read, and the second is where
adding names would come from.

---

# Corrections and completed work — 18 Aug 2026

## Correction 1 — four rows were already disabled

The first pass read raw content and reported 10 agencies. Four rows carry
`disable_element="yes"` and do not render: **Summit Talent, Metropolis Talent,
Natural Talent, Digital Artists Agency.** The live page had **6 agencies and 10
agents**, which is why the intro's "nine agents from 9 agencies" matched nothing.

**Always check `disable_element="yes"` before counting anything on a WPBakery page.**

## Correction 2 — the disabled rows are broken, not merely retired

Otto asked whether the disabled rows held reusable agent names. They do, but the
rows themselves are unusable: each has a correct agency and agent **heading** and
a body of **2024 animation-conference copy**.

| Row | Heading | Body actually contains |
|---|---|---|
| Summit Talent / Sandy Weinberg | correct | Anima Brussels 2024 write-up |
| Metropolis Talent / John Goldsmith | correct | Art Department Berlin 2024 write-up |
| Natural Talent / Donna Felton | correct | Annecy 2024 write-up |

They were duplicated from the conferences page, had headings filled in, and never
had bodies written. Disabling them was the right call at the time.

## Correction 3 — the contamination reached a LIVE entry

Otto spotted it: **Ritter Talent Agency / Teresa "Teri" Ritter** was publishing
the same Berlin conference copy under an agent's name, on the site's
highest-traffic page. A scan of every entry found this was the only live one —
UTA, Verve, Kane-Ritsch, Paradigm, Van Duran and DPN are clean.

## My own error, caught and fixed

I linked **Ritter Talent Agency** to `ritteragency.com`, which redirects to
**acrisure.com/southwest — an insurance company.** The real site is
`rittertalentagency.com`. Corrected.

**Lesson: resolve a guessed domain and read its title before linking it.** A 200
response only proves something answers, not that it is the right something.

## Applied to the live page

1. Agencies linked, UTM-tagged: UTA, Verve, Ritter, Paradigm, DPN. Annette Van
   Duran has no findable site and stays unlinked.
2. `nine agents from 9 seperate agencies` → `ten agents from six separate agencies`
3. `(DNP)` → `(DPN)` — Danis, Panero, Nist
4. Digital Artists Agency row deleted. Its domain `d-a-a.com` is dead and
   `digitalartistz.com` appears to be a different operator on a similar name —
   not linked.
5. Stale links repointed: IMDbPro (login-walled) → public IMDb; Oscars → its
   redirect target; Annecy MIFA → `/le-mifa/presentation-mifa`
6. UTA claim softened from an unsourced "In 2026 … signed deals with Disney,
   Warner Bros. and Sony" to a statement that does not assert a specific year.
7. Ritter body rewritten from verified facts.

**UTM pattern:**

    https://www.unitedtalent.com/?utm_source=oddtoe.com&utm_medium=referral&utm_campaign=animation-agents-guide

## Verified agent facts gathered

| Agent | Agency | Verified |
|---|---|---|
| Zac Simmons | Paradigm | Still there; partner in Literary Content since 2023 |
| Sandy Weinberg | Summit Talent & Literary | Owner; founded 2000; represents animators. Site `summitalent.org` live |
| John Goldsmith | Metropolis Talent | President; animation-specialist agency, Beverly Hills. `metropolistalent.com` live |
| Donna Felton | Natural Talent Inc. | CEO; animation artists and original concepts. **Sources spell it "Felten"** — worth confirming |
| Teri Ritter | Ritter Talent Agency | Owner; founded Aug 2017, Toronto. Film/TV/commercial/voice-over, not animation-lit |

## Open questions for Otto

1. **Re-enable Summit, Metropolis and Natural Talent?** All three are real,
   animation-focused, and two have live sites — a better fit for this page than
   Ritter. Each needs a body written from scratch.
2. **Does Ritter belong here?** Toronto actor and voice-over agency, not an
   animation-talent agency. Kept and written accurately, but it is the odd one out.
3. **Felton or Felten?** Sources disagree with the page.
4. The other agents at UTA, Verve, Van Duran and DPN are still unverified
   individually. That is the slow pass.

---

# Re-enabled with new copy — 18 Aug 2026

Otto's call: bring back Summit, Metropolis and Natural Talent. All three now
render with bodies written from verified facts, replacing the 2024 conference
copy that had been sitting under their headings.

Live page is now **9 agencies, 13 agents**, and the intro count says so.

| Agency | Agent | Site |
|---|---|---|
| Summit Talent & Literary | Sandy Weinberg, Owner | **none** — see below |
| Metropolis Talent | John Goldsmith, President | **metropolistalent.info** |
| Natural Talent | Donna Felton, Chief Executive | **none** |

## Domain check — a second near-miss

Having already linked an insurance company by trusting a 200, I resolved every
candidate and read what it served. Just as well:

| Domain | Reality |
|---|---|
| `summitalent.org` | **parked lander** — redirects to `/lander`. Not a site |
| `summittalentagency.com` | dead |
| `metropolistalent.com` | **parked lander** — same pattern |
| `metropolistalent.info` | **the real site** — John Goldsmith, 9201 Wilshire Blvd Suite 104, matching the corporate record |
| `metropolis-talent.com` | dead, despite being their email domain |
| `naturaltalentinc.com` | dead |
| `natural-talent.com` | a coaching and training company, unrelated |

**This corrects the first pass**, which listed `summitalent.org` and
`metropolistalent.com` as live. Both are parked. Only Metropolis got a link.

**Rule: a 200 means something answered. Read the title and the body before
linking, every time.**

## What the new copy says, and what it is built on

Only verified facts. Where an agency has no site, the copy says so plainly rather
than leaving a reader hunting.

- **Sandy Weinberg** — founded Summit in 2000 for cross-platform clients; roster
  spans TV writers, screenwriters, animation artists, producers, authors and
  directors across film, TV, web series and 4D theme-park work; Beverly Hills;
  no working website.
- **John Goldsmith** — President; animation is the whole business, not a
  division; positions at the intersection of animation and technology; offers
  career coaching and CGI/technology development alongside contract work; has
  written on the agent's role for Animation World Network.
- **Donna Felton** — Chief Executive; licensed agency that both places animation
  artists and helps them pitch their own original concepts; long counted among
  the LA animation specialists; no public website.

## Still open

- **Felton or Felten?** Two LinkedIn profiles spell it **Felten**; the page says
  Felton. Left as-is — changing a person's name on a guess is worse than leaving
  it. Otto to confirm.
- **Does Ritter belong on this list?** Toronto actor and voice-over agency, not
  an animation-talent agency. Accurate now, but the odd one out.
- Individual agents at UTA, Verve, Van Duran and DPN remain unverified.

---

# Final pass — 18 Aug 2026

Otto's calls: Felten spelling confirmed, Ritter dropped.

| Change | |
|---|---|
| `Donna Felton` → `Donna Felten` | Otto confirmed; two LinkedIn profiles agreed |
| Ritter Talent Agency row | **removed** — Toronto actor/voice agency, not animation-talent |
| Count | now `twelve agents from nine separate agencies` |
| `Julie Kane-Ritch` → `Kane-Ritsch` | misspelling inside the Gotham body |
| Gotham Group | **linked** — gotham-group.com verified as "Home \| The Gotham Group" |
| Link palette | scoped CSS, near-black on the peach background |

## Correction 4 — Gotham Group is a roster entry

I twice treated Gotham Group as editorial because my heading regex expected
`<h2>` and Gotham's title sits as bare text inside a `[dfd_heading]` shortcode
with no `<h2>` wrapper and no trailing newline. It is a full roster entry with
its own agent, **Julie Kane-Ritsch, Talent Manager and Head of Animation**.

That is why the count went 6 → 8 → 9 agencies across three passes.

**Lesson: on this theme a heading can live as bare text inside `[dfd_heading]`.
Count from the rendered page, not from an HTML-tag regex over the raw content.**

## Link palette on `#edb39f`

Every row on the page uses one background, `#edb39f`. Measured:

| Colour | Ratio | AA |
|---|---|---|
| tan `#c39f76` (theme default) | **1.35** | fail |
| **near-black `#0d0d0d`** | **10.69** | pass |
| plum `#26161f` | 9.49 | pass |
| **wine `#5c2b3f`** (hover) | **6.17** | pass |
| olive `#8a8f6a` | 1.86 | fail |
| sand `#ddccb1` | 1.16 | fail |

Applied as `.page-id-14208 .vc_row:not(.dfd-background-dark)` covering body text,
`h2` and `h3` links. Verified live: **16 links on the peach background, 0 failing
AA**, all at 10.69.

This is the second Oddtoe page where the theme's tan accent fails on a light
background. The pattern is now established: **on any light-background Oddtoe row,
tan/sand/olive all fail — use near-black with a wine hover.**

## Final state of the page

Nine agencies, twelve named agents, six UTM-tagged agency links.

UTA · Verve · Gotham Group · Summit · Metropolis · Natural Talent · Paradigm ·
Annette Van Duran · DPN

## Still open

- Individual agents at UTA, Verve, Van Duran and DPN are unverified. Agent moves
  are the fastest decay here; Paradigm alone had five changes in 2026.
- Annette Van Duran has no findable website and stays unlinked.

---

# Agent-by-agent verification — 18 Aug 2026

Every named agent checked against trade press, agency sites and LinkedIn.

| Agent | Agency on page | Verdict |
|---|---|---|
| **Anna Berthold** | UTA | **STALE — left UTA May 2024.** Now EVP Animation and Kids & Family at Stampede Ventures |
| Jason Burns | UTA | **Current.** Partner, co-head of Motion Picture Literary. Variety interviewed him ahead of Annecy, June 2026 |
| Andrew Cannava | UTA | **Current.** Partner/Agent |
| Bryan Besser | Verve | **Current.** Co-founding partner, 13 years |
| David Boxerbaum | Verve | **Current.** Partner since 2017 (ex-Paradigm, ex-APA) |
| Julie Kane-Ritsch | Gotham Group | **Current.** Head of animation |
| Sandy Weinberg | Summit | **Current.** Owner since 2000 |
| John Goldsmith | Metropolis | **Current.** President |
| Donna Felten | Natural Talent | **Current.** CEO |
| Zac Simmons | Paradigm | **Current.** Partner, Literary Content, since 2023 |
| **Annette van Duren** | own agency | **Current** — but the page spelled it "Van Duran". Real spelling **van Duren** |
| Natanya Rose | DPN | **Current.** Senior EVP, Animation/Interactive. Ex-ICM |

**Eleven of twelve current.** One two-year-stale entry, and it was the headline
one.

## The Berthold problem

She was not just listed — she was the page's **"Best Agent"** in the awards
banner and her entry claimed she was "leading UTA's animation division". She
founded that division in 2017 and left in May 2024.

Fixed by telling the truth rather than deleting her. The entry now credits her
for building UTA Animation and states she moved to Stampede Ventures, with the
point that matters to a reader pitching animated family content: **she is now on
the buying side**, which may be more useful than an agent.

The "Best Agent" banner moved to **Jason Burns** — verified UTA Partner,
co-head of MP Lit, and the agency's current animation voice in the trade press.
That is an editorial call and is easy to revert.

## Two more name errors, same class as Felten

- **Annette Van Duran → Annette van Duren.** Her agency site
  (`annettevandurenagency.net`, verified live) uses van Duren. Now corrected and
  linked.
- The page had already had **Felton → Felten** and **Kane-Ritch → Kane-Ritsch**.

**Three misspelled names on one page.** Worth a proofread pass on any page that
lists real people — a misspelled name is the fastest way to lose a reader who
knows the industry, and these are the exact people Otto wants to approach.

## Stale dates cleared

- `"I'll look to update the 2024 animation agents' list throughout the year and
  into 2025."` → `"I'll keep this list current through 2026 and into 2027."`
- An internal link to the retired `/animation-conferences-2023-2024/` now points
  at `/animation-conferences/`.

## Final state

Nine agencies, twelve agents, **seven UTM-tagged agency links**. Live at
https://www.oddtoe.com/animation-agents/

**Note on process:** this page was already published, so every edit in this audit
went straight to the live site. There was no draft stage, unlike the conferences
rebuild.

---

# Search Console — 18 Aug 2026

Both refreshed pages submitted for re-crawl.

| URL | Status before | Action |
|---|---|---|
| https://www.oddtoe.com/animation-conferences/ | **already indexed** | Indexing requested — priority crawl queue |
| https://www.oddtoe.com/animation-agents/ | already indexed | Indexing requested — priority crawl queue |

**The new conferences URL was already on Google within hours of publishing.** No
waiting, no discovery problem — almost certainly because the 301 came from a URL
Google already trusted. Worth remembering for the next migration: a redirect
from an established URL is a faster path to indexing than a fresh sitemap entry.

## GSC automation notes

- The direct deep link `search-console/inspect?...&id=<encoded URL>` **404s**.
  It only works with Google's internal opaque id.
- Working route: open the property, click the inspection box **by coordinate**
  (a `ref`-based click typed into the box but the value was discarded on Enter),
  type the URL, verify the input's value by script, then press Return.
- Verifying the field before submitting is what makes this reliable. The earlier
  note that "GSC rejects long URLs via automation" was really this: the value
  silently failed to stick.
