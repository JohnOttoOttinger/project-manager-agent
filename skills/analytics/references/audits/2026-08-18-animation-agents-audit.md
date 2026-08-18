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
