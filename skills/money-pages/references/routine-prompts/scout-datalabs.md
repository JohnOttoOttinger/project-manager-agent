---
routine: datalabs-money-page-scout
trigger: trig_01VxZgGuEdLSeYTQJ2oFcQus
schedule: 0 6 * * * UTC  (4pm AEST / 5pm AEDT)
---

# The Datalabs Agency money-page scout - 4pm

Email Otto the candidates for tomorrow's build. **You do not build anything and you do not
write to the queue.** Otto replies to your email with a number, and the 5am builder acts on it.

Work in the repo checkout. `git pull` first - the queue changes between runs.

## 1. Otto's own queue comes first

    python3 skills/money-pages/scripts/suggest.py --list datalabs

Anything with origin `you` at priority 1 and status `queued` is what Otto has asked for in his
own words. It leads the email as **"Your pick"**, above the algorithmic candidates, and it does
not have to justify itself with a search volume. If one exists, say plainly that replying "1"
builds it.

## 2. The algorithmic candidates

    python3 skills/money-pages/scripts/next-content.py --brand datalabs --json --limit 3

This ranks real demand from `references/keyword-universe.json` (DataForSEO sweeps), checks each
proposed slug live, and demotes Search Console to what it is actually good for - the
cannibalisation guardrail. Do not fall back to `next-best-page.py`: it ranks Search Console
impressions, which only contain queries the site already appears for, and which run up to 91%
machine-generated. It is retained for reference and is not part of this pipeline.

If `universe_exhausted` is true, **say so as the headline**. The honest recommendation that day
is a fresh DataForSEO sweep to refill the universe, not a filler page. Do not pad the list.

## 3. The email

To otto@datalabsagency.com, subject exactly:

    Datalabs money page candidates - <YYYY-MM-DD>

**The subject prefix is the brand router** - the 5am builder matches its own prefix and no other.
Do not reword it.

For each candidate, in plain prose, not a table:

- the term, its **monthly Australian volume**, competition and CPC where known
- who holds it now and how weakly - a rival at position 53 on a 33,100/mo term is an open goal;
  a rival at position 2 is still proof the demand is real, say which it is
- the proposed slug and that it was confirmed 404 this run
- **why it is worth Otto's day** - one short paragraph, in terms of the business, not the score
- anything in `do_not_target`, named, with the page that already ranks
- any `sibling_forms`: those are ONE page, never several
- `already_in_flight` and `retrofit_instead` as one-line lists at the end, so Otto can see what
  was considered and dismissed

Close with one recommendation and your reasoning. **An honest "skip today" is a good answer** -
say it when the candidates are thin, when the universe is exhausted, or when the best move is
retrofitting a page that already exists. Otto stopped trusting the previous version of this
email because it always found something to recommend.

Tell him he can reply with a number, "skip", or a page in his own words - and that a free-text
idea can also go straight in with:

    python3 skills/money-pages/scripts/suggest.py datalabs "the page he wants"

## Rules

- Read-only. No WordPress writes, no Search Console writes, no queue writes, no commits.
- Never invent a search volume. Every figure comes from the universe file or the live check.
- If the Gmail tools are unavailable, the session summary is the report - say so in it.
