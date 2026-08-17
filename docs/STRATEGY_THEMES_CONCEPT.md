# Strategy: Themes — concept note

Captured 17 Aug 2026, in Otto's words, before any design work. The Strategy tab
exists as a `coming-soon` placeholder. **Nothing here is built yet.**

## What Otto described

> "I would like to talk in *Themes* with strategy. As in I might work in other
> areas of the agent (say Marketing) and a possible Strategy theme is for Oddtoe
> to get more leads from my Facebook ad budget. That would then allow me to track
> strategy theme metrics and tasks more closely. It would allow you to optimize
> my time, money, ROI, according to these Themes and then we could break the
> themes down into tactical tasks (check box lists)."

A **theme** is a standing objective with money and attention behind it. His
example: *"more Oddtoe leads from the Facebook ad budget."*

A theme appears to carry:

- an **outcome** — what success is, in his terms
- a **budget** — money, and his time, which is scarcer
- **metrics** — how it is measured, and by what date
- **tactical tasks** — a checkbox list underneath it
- **attribution** — which work, done anywhere in the app, counted toward it

## DECIDED (Otto, 17 Aug 2026)

> "Strategy as a layer. I see the Analytics area being the reporting tab or area."

**Strategy owns intent. Analytics owns measurement.** Strategy defines themes —
outcome, budget, surfaces, tasks — and other agents attach work to them.
Analytics reports what those themes are returning, because it is the only part
of the app that reads real numbers.

This resolves the tension below in favour of option 1. Option 2 is dead.

### What that buys us

**The Analytics watchlist is already a proto-theme.**
`skills/analytics/references/watchlist.json` holds a list of queries and pages to
track. A theme is that, plus a name, an outcome, a budget and tasks. So the
migration is: themes become the source, and the global watchlist becomes derived
from the union of active themes' surfaces. Analytics barely changes — it reports
per theme instead of once globally.

**Attribution should be by declared surface, not manual tagging.**
A theme names the pages, queries and campaigns that belong to it; anything
happening on those counts automatically. A solo operator will not reliably tag
every action, and a tracker that depends on remembering to tag decays within a
fortnight. Manual attachment stays as the fallback for work with no URL — a
pitch, a call, a lost lead.

## The design tension to resolve first — RESOLVED, see above

**Themes are cross-cutting, but the app is organised by agent.**

Otto is explicit that he might do the work *in Marketing* while the theme lives
*in Strategy*. So a theme cannot be a folder inside the Strategy tab — if it were,
it could only ever see work that happened in Strategy, which is the one place the
work will not happen.

That makes Strategy unlike every other tab. The others own a workflow; this one
owns a **lens over the others**. Two ways that could go:

1. **Strategy as a layer.** Themes live in shared state. Any agent can attach its
   output to a theme — a Marketing post, a Money Page, a lost lead, an Analytics
   metric. Strategy is the place you read and steer them. Truer to what he asked
   for; needs a data model the other agents write into, and probably a "which
   theme is this for?" affordance in the other tabs.
2. **Strategy as a reporting tab.** Themes are defined in Strategy, and it pulls
   from what the other agents already record. Cheaper, no changes to other
   agents, but attribution becomes inference rather than fact — and inference is
   exactly what the Analytics work this session was built to stop doing.

Option 1 is what he described. Option 2 is what could ship in a day. Worth putting
that trade-off to him directly rather than picking quietly.

## Questions for the design session

- **What is a theme's lifespan?** A quarter, until hit, or open-ended?
- **How many run at once?** For a solo operator the answer is probably two or
  three; if it's ten, the tool is a to-do list with extra steps.
- **Does a theme own a budget, or reference one?** Investment already deals with
  spending decisions — these two tabs will overlap and the boundary needs stating.
- **Where do tasks live?** There is already a task system (`task-capture`,
  `TASKS.md`). Themes should almost certainly tag existing tasks rather than
  introduce a second, competing list.
- **What counts as ROI here?** Oddtoe has no revenue data in the app. Enquiries
  are now measurable (GA4 `ThankYouOddtoeClicks`, from 17 Aug 2026) and Gravity
  Forms holds the historical record, but enquiry → job → money is manual. Without
  that last link, "ROI" means cost per enquiry, not return. Say so plainly rather
  than presenting a number that looks like profit.
- **Does the Facebook example need ad-platform data?** Nothing in the app reads
  Meta Ads today. That theme specifically would need spend data to mean anything,
  which is another API and another credential.

## What already exists to build on

- **Analytics agent** (`skills/analytics`) reads GA4 + Search Console directly and
  can measure enquiries, rankings, and page performance. Any theme metric that is
  web-shaped is already gettable.
- **Business Development** logs wins and losses with reasons — the closest thing
  to outcome data.
- **`skills/task-capture` and `TASKS.md`** — the existing task substrate.
- **`skills/my-business`** — business memory.

## Standing constraint

Do not let a theme dashboard invent numbers. If a metric is not actually measured,
the theme shows it as unmeasured. The reason this app now has API access at all is
that estimates were being treated as facts.
