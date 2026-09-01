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

## Which mailbox — verified 1 Sep 2026, do not rediscover this

There are **two separate Google accounts**, and only one is on the
connector:

- **Datalabs** — `otto@datalabsagency.com`. This is the account the Gmail
  MCP connector is authorised for. Datalabs drafts go through the
  connector's create-draft tool, exactly as the steps above describe.
- **Oddtoe** — `oddtoe@oddtoe.com`. A separate sign-in the connector
  CANNOT reach (its tools have no account switch). It lives in the browser
  at `https://mail.google.com/mail/u/3/` — confirm the account name in the
  tab title before touching anything. Oddtoe drafts are composed there
  with the Chrome browser tools.

**Never create Oddtoe drafts through the connector.** They land in the
Datalabs account signed as Oddtoe, which reads as spoofed mail, and moving
them is manual pain. This was done wrong once; once is enough.

### Composing in the Oddtoe account (browser)

- Click **into each field** — To, then Subject, then the body — and type
  only after the click. Never Tab-chain between fields: a keystroke that
  misses a field becomes a Gmail shortcut (`?` opens the shortcut overlay,
  `c` opens a new compose), and a long paste sprays as a shortcut storm.
- Gmail auto-inserts Otto's real signature. End the body with `Otto`, a
  blank line, and the unsubscribe line, and let the signature carry the
  sign-off. Do not type the full sender block — it doubles the signature.
  The unsubscribe line itself is still required, verbatim, above the
  signature.
- Close the compose with its **X** (top right) — that saves the draft.
  Never press Cmd+Enter, which sends.
- Verify the Drafts count went up before reporting the draft as created.
- The browser gives no usable Gmail draft id. Record the draft on the
  board with a marker id instead — `browser-u3-<date>-<company>` — the
  store only needs a non-empty id to know a draft exists; the loop runs on
  status and dates.

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
