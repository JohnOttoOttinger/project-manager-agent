---
name: opportunity-tracker
description: Track and act on deadline-driven opportunities for Oddtoe — festival press accreditation, animation market pitch sessions, open calls, prizes, council public-art registers and gallery submissions. Use when the user asks what is due, wants to log an opportunity, wants a submission or press-accreditation pitch drafted, or asks how to reach commissioners, curators, agents or festivals.
---

# Opportunity Tracker

For the two Oddtoe audiences that **do not arrive through search**: entertainment
producers and publishers, and galleries and museums. See
`oddtoe-target-audiences` in memory for what Otto wants from each.

Money pages serve people already searching for a supplier. A commissioning
editor, a curator and a festival press office are reached by submitting to a
deadline. Missing one costs a year, so the deadline is the thing this skill
protects.

## The register

`references/opportunities.md` — one row per opportunity, grouped by stream.
Every row carries a **closing date** and a **source URL**, because a date
nobody can check is a date nobody should act on.

| Stream | What it is |
|---|---|
| `press` | Festival press accreditation and media partnerships |
| `market` | Pitch sessions at animation markets |
| `prize` | Awards and competitions — a shortlisting is a nameable credit |
| `opencall` | Open calls, group shows, artist-run spaces |
| `register` | Council and institutional public-art registers and EOI lists |

Status runs `researching → drafted → submitted → outcome`. Record the outcome
even when it is a rejection; the pattern matters more than any single result.

## Before adding anything

**Never write a deadline you have not read on the organiser's own page.**
Conference and festival dates move, and press deadlines are usually separate
from and earlier than the event. If a date cannot be verified, the row says
`TO VERIFY` and names the page to check. A confident wrong date is worse than
a blank.

## What is due

    cd skills/opportunity-tracker
    python3 scripts/due.py            # next 90 days
    python3 scripts/due.py --days 30
    python3 scripts/due.py --all

Run it at the start of any Business Development conversation. Anything inside
30 days that is still `researching` needs raising unprompted.

## Drafting a submission

Most open calls, prizes and accreditation forms want the same five things in
different shapes: an artist statement, a CV, work samples, a project
description, and a budget. Draft from `references/positioning-source.md` so the
facts stay identical across submissions, then reshape to the form's word limit.

Rules that matter more here than elsewhere:

- **Never invent a credit, a date, an exhibition or a client.** A padded CV is
  found out, and in this world it ends the relationship permanently.
- Oddtoe's exhibition history is genuinely thin — one strong 2019 credit. Write
  around it honestly rather than dressing it up. Curators read a lot of these.
- On Oddtoe surfaces the name is **Oddtoe**, not Otto Ottinger, except where a
  form asks for the legal entity. See `oddtoe-naming-rule` in memory.
- Otto's voice guardrails apply — no aphoristic closers, no balanced
  antitheses, nothing poetic in a factual field.

## The press-accreditation play

Oddtoe's animation conferences guide ranks in Google's **top three** for
"animation conferences" and "animation conferences 2026". That is a real media
asset, and festivals accredit outlets on reach and coverage.

The trade: press accreditation in exchange for a post-event piece and a listing
kept current year-round. Numbers to quote are in `references/media-kit.md`,
refreshed from the analytics skill — never from memory.

Press deadlines typically close **two to three months** before the event and are
easy to miss because they are not the event date.

## The agent play

The animation agents page ranks around position 5 for `animation agent`. The
Gravity Forms record shows it attracts animators *seeking* agents rather than
agents seeking talent — the inverse of what it was built for. The traffic is
still leverage: agents listed on that page can be approached with an opener
almost nobody has, that they are featured on the page ranking top-five for their
own category.

That outreach reuses the `sales-outreach` skill's machinery pointed at a
different list. Do not rebuild it here.

## What this skill does not do

- It cannot send email or submit a form. Draft, hand over, and say so plainly.
- It does not track client work or lost bids — that is `lost-lead-review`.
- It does not do search or content work — that is `money-pages` and `analytics`.
