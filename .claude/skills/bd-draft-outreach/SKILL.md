---
name: bd-draft-outreach
description: Draft one-to-one Business Development outreach emails into Gmail from the local prospect board. Use when Otto asks to draft outreach, email prospects, work the BD pipeline, or asks who is ready to contact for Oddtoe or Datalabs.
---

# BD outreach drafting

Turn eligible prospects on the local BD board into Gmail drafts that Otto
reviews and sends himself. The local app owns every guardrail; this skill's
job is to compose well and never route around a refusal.

**You draft. Otto sends. Never send an email, and never say one was sent.**

The local app must be running (`./start.command`, http://localhost:3000). If
it is not reachable, stop and say so — do not compose from memory of an
earlier session.

## The order matters

Validate before Gmail, not after. A rejected draft must never exist in the
mailbox.

1. **Read who is eligible.**

       GET /api/prospects/draftable?brand=oddtoe&limit=10
       add &campaignId=<id> when working a named push
       add &list=<list name> to work one list

   Returns `eligible`, `skipped` (each with a reason), `settings` (sender
   name, sender contact, unsubscribe line), `dailyCap`, `remainingToday`,
   and each prospect's own `outreachUrl`.

2. **Report the shape before composing.** How many eligible, how many
   skipped and why, how much cap is left. If `eligible` is empty, say so
   with the reasons and stop — the usual cause is no contact email.

3. **Compose one email per eligible prospect** (see below).

4. **Validate.**

       POST /api/outreach/validate-drafts
       { "brand": "...", "drafts": [{ "prospectId", "subject", "body" }] }

   Only `approved: true` entries go to Gmail. Read any `reasons` out and fix
   the draft or drop that prospect; never argue with a rejection. Repeat any
   `warnings` to Otto — a flagged contact may be the wrong person.

5. **Create the Gmail drafts** with the Gmail connector's create-draft tool,
   one per approved prospect, `to` set to `contactEmail`. Keep the returned
   draft `id`.

6. **Record them.**

       POST /api/prospects/drafts
       { "brand": "...", "campaignId": "...", "drafts":
         [{ "prospectId", "draftId", "hook", "hookEvidence" }] }

   This moves the cards to Emailed and sets the follow-up date. If this call
   fails after Gmail succeeded, say so plainly — the drafts exist but the
   board is wrong, and Otto should not send until it is fixed.

7. **Report**: what was drafted, what was rejected and why, what warnings
   stand, and that nothing has been sent.

## Which mailbox

The Gmail connector writes to the single account it is authorised for.
Before drafting for a brand, say which mailbox the drafts will land in. If
that is not the brand's own address — Oddtoe sends as `oddtoe@oddtoe.com`,
Datalabs as `otto@datalabsagency.com` — tell Otto before creating anything,
because he will have to move or re-send them by hand.

## Composing

Every body must contain, **verbatim**:

- the `unsubscribeLine` exactly as returned — the store refuses the draft
  without it, and it is what makes the opt-out real rather than decorative;
- the sender name exactly as returned;
- **that prospect's own `outreachUrl`.** Each link carries a different
  `utm_content`. Using another prospect's link attributes their click to the
  wrong company and quietly corrupts the only intent signal BD has.

Then:

- **Pick the angle from evidence, not invention.** Use the record's notes,
  website and what enrichment found. Record it in `hook` with the specific
  evidence in `hookEvidence`, so an angle that stops working can be seen
  later. Never assert a fact about a prospect's business you were not given
  — no turnover, headcount, clients, or software.
- **Under 150 words.** Name something specific about them in the first line.
  One ask, one link.
- **Voice.** No "I hope this finds you well", "reaching out", "circle back",
  "excited to", "leverage", "synergy", or an em-dash-heavy rhythm that reads
  as machine-written. At most one exclamation mark, ideally none. Write the
  way a person who makes things writes to another person who makes things.
- **Brand names**: on Oddtoe surfaces the studio is "Oddtoe"; Datalabs is
  "The Datalabs Agency". Follow the sender block that comes back from the
  API rather than inventing a sign-off.
- Take every price, lead time and term from Otto's own business facts. Where
  one is missing write `[YOU FILL IN: day rate]` rather than guessing.

## Refusals you must respect

The store will exclude a prospect for: no contact email, an address on the
do-not-contact list, a draft that already exists, a status past Enriched, or
the daily cap. These are not obstacles to work around. Report them and move
on. Asking again will not change the answer.

A prospect with status `needs_review` **is** draftable but arrives with a
warning. Repeat the warning; the contact may be wrong.

## Someone asks to be left alone

That is a do-not-contact entry, not a note:

    POST /api/suppressions
    { "brand": "...", "email": "...", "reason": "unsubscribed|bounced|asked|manual",
      "detail": "..." }

Do it the moment it is mentioned. An opt-out recorded only in a note is not
an opt-out, and the next import would contact them again.

## Prototype data

`skills/sales-outreach/references/prototype-prospects.csv` is synthetic:
invented companies on reserved `.example` domains that cannot route. It is
for exercising the flow. If Otto is working the prototype list, say so, and
never present a synthetic result as a real outreach outcome.
