# Framework: finding the keywords behind your next page

For use *before* you type a free-text page request. It turns "what should I build?" into a
handful of specific terms with real numbers behind them, so `suggest.py` gets a page idea that
already knows what it is targeting.

Four screens, in order. A term has to survive all four.

---

## Screen 1 — Does anyone search for it? (volume)

**A term with no volume is not a page, whatever it says about the brand.** The 24 Aug sweep is
the proof: Datalabs' own positioning language — "data visualisation training" (10/mo),
"data visualization style guide" (10/mo) — has essentially no Australian demand, while the plain
product names do. The site was optimised for language nobody types.

Source: a DataForSEO sweep in your signed-in API Playground at `app.dataforseo.com`.
Location **Australia (2036)**, language English. No credential is ever handled — the Playground
runs the calls in your session. Budget roughly $0.15 a sweep.

Two calls do almost all the work:

| Call | Endpoint | What it answers |
|---|---|---|
| `keyword_suggestions` | `/dataforseo-labs` | every long-tail term *containing* a seed you give it — use for expanding a service you already sell |
| `ranked_keywords` | `/dataforseo-labs` | every term a **rival domain** ranks for — use for stealing |

Do **not** use `related_keywords` for discovery; it only reads Google's "searches related to" box
and returned a single term.

---

## Screen 2 — Does anyone own it? (winnability)

This is the highest-yield screen, and the one that found the best page in the backlog.

Pull a rival's `ranked_keywords` and sort by **high volume, weak position**. A rival ranking at
position 40+ on a big term is not defending it — they have a thin page that happens to exist.
That is an open goal.

Worked example, 28 Aug: Nexacu ranks **position 53** for `gantt charts`, **33,100/mo**. They also
sit at 45 and 48 on the two `data analytics courses` forms, both 2,400/mo. Three pages' worth of
demand, none of it defended.

The mirror case matters too: Nexacu at **position 2** for `power bi training` is a *strong*
incumbent, and that is still worth having, because it proves the demand is real and the buyer
intent is commercial. A strong incumbent costs effort, not the idea.

**Who to pull, per brand:**

| Brand | Rival | Why |
|---|---|---|
| Datalabs | `nexacu.com.au` | AU Power BI/Excel training house, publishes prices, our pricing anchor |
| Oddtoe | `eness.com` | the #1 register rival — direct overlap on projection, installation, council and museum buyers |

The Oddtoe result from that pull is itself a strategy finding: ENESS's whole search footprint is
**named-project fame** — `bunjil` 3,600/mo, `airship orchestra`, `iwagumi air scape` — and exactly
one category term (`interactive installation art`, 40/mo, position 22). **The category shelf is
empty. No rival owns it.** Two consequences: category pages are cheap to win, and naming Oddtoe's
own works memorably turns them into searchable entities. See
`skills/analytics/references/competitor-register.md` for who else belongs on this list — it is
deliberately a list of who you lose pitches to, not who Ahrefs thinks looks similar.

---

## Screen 3 — Is it about what we actually do? (relevance)

The screen that stops the machine embarrassing itself. `communication skills course` is 1,000/mo
with Nexacu at position 41 — it passes screens 1 and 2 comfortably, and it is a page you would
never build. `how to create a drop down list in excel` is 6,600/mo and is Excel data entry, not
data visualisation.

Ask it plainly: **if someone arrives here from Google, is there anything on this page we could
sell them?** If the honest answer is no, it fails, whatever the volume.

Terms that fail this screen stay in `keyword-universe.json` with an `exclude` reason rather than
being deleted, so a later sweep does not rediscover and re-propose them.

---

## Screen 4 — Do we already cover it? (gap)

Three different answers, and only one of them is a new page:

- **Slug 404s and nothing of ours ranks** → a real gap. Build it.
- **We already have a page for this** → retrofit that page. Building a rival splits your own
  ranking. `kinetic sculpture` (480/mo) is this case: `/artist-designer/kinetic-sculptor/` exists,
  so it goes in the universe with `served_by` set, and the scout offers it as a retrofit.
- **We rank top-10 already and earn no clicks** → a title and meta problem, not a missing page.

`next-content.py` runs this screen automatically with a live HEAD check, and uses Search Console
for the `do_not_target` list — queries our other pages already rank top-10 for, which a new page
must not bid against.

---

## Google Trends — the tie-breaker, not the input

Trends gives **direction**, not volume, and has no official API. Use it manually at
trends.google.com, Australia, 5-year window, when you want to separate a rising term from a dying
one, or pick between two terms that score alike. It is a sanity check on a candidate that already
passed the four screens — never the reason a candidate exists.

Worth a Trends check: any term whose volume looks surprisingly large for how little competition it
has, and any AI-adjacent term, where a flat AdWords volume can hide a steep climb.
`generative ai artist` has **no AdWords volume at all** and is still in the universe as a
pre-volume term — that is exactly the case Trends can adjudicate.

---

## Turning the result into a page request

Once a term survives all four:

    python3 skills/money-pages/scripts/suggest.py datalabs "gantt chart explainer, target 'gantt charts'" \
        --term "gantt charts" --volume 33100 --slug /gantt-charts/

Then add the term to `references/keyword-universe.json` with its volume, competition, and
`incumbent` position, so the scout can reason about it too, and write the sweep up in
`skills/analytics/references/dataforseo/` so the numbers have a provenance.

**Never invent a volume.** A page you want with no verified figure is completely legitimate — it
goes in the queue as an Otto-origin idea, marked volume-unvalidated, and outranks the algorithm
anyway. Making up a number is the only thing that breaks the system.
