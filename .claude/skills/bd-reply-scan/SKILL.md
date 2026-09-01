---
name: bd-reply-scan
description: Close the BD outbound loop — scan the inbox for replies to outreach, record sends and clicks, draft the one follow-up when it comes due, auto-close silent prospects, and read out the morning BD brief. Use when Otto asks who replied, what needs chasing, to run the reply scan, or for the morning BD brief.
---

# BD reply scan, follow-up and brief

Outreach without this skill is a one-way street: drafts go out and the board
never learns what happened. This is the return path.

**You read the inbox and write to the board. You never send an email, and you
never mark something replied that you did not actually see.**

The local app must be running (`./start.command`, http://localhost:3000). If
it is not reachable, stop and say so — never report a scan you could not run.

## Say which mailbox first

The Gmail connector reads the single account it is authorised for. Before
scanning, say which mailbox that is. If it is not the brand's own address —
Oddtoe is `oddtoe@oddtoe.com`, Datalabs `otto@datalabsagency.com` — say so
before reporting anything, because replies to the other brand will not be in
what you just read, and "no replies" would be a false all-clear.

## 1. Who is waiting

    GET /api/prospects/awaiting-reply?brand=oddtoe

Returns `awaiting` (each with company, contact, status, `draftedAt`,
`sentAt`, `followUpDue`) and `addresses`, the flat list of email addresses to
match against. If it is empty, nothing has been drafted yet — say that
plainly rather than reporting a clean scan.

## 2. Scan the mailbox

Search the inbox for messages from `addresses`, from the earliest `draftedAt`
in the set onwards.

**Match on the sender's email address, never on a display name.** Two people
share a name; nobody shares an address. A message from a colleague at the
same company is not that prospect replying — it is a new contact, and it goes
in `detail` for Otto to read, not into a `replied` signal.

### What is not a reply

Getting this wrong is worse than missing a reply, because it stops the
follow-up and tells Otto someone is interested when they are not:

- **Out-of-office and holiday auto-responders.** Not a reply. Leave the
  prospect awaiting and let the follow-up date do its work.
- **Delivery failures and bounces.** Not a reply. Record a suppression
  instead (below) so the address is never used again.
- **Unsubscribe or "stop emailing me".** Not a reply in the sense that
  matters — record the suppression *and* the reply, because Otto should see
  it, and the suppression is what makes the opt-out real.
- **Automated ticket acknowledgements** from a support desk address.

When you are unsure whether something is a human answer, do not record it.
Report it to Otto and let him decide. An unrecorded reply costs one follow-up
email; a wrongly recorded one silently kills a live prospect.

## 3. Record what you found

    POST /api/prospects/signals
    { "brand": "...", "signals": [
        { "prospectId": "...", "kind": "replied|sent|clicked",
          "occurredAt": "<ISO timestamp from the message>",
          "detail": "<who answered and the gist, one line>" }
    ] }

- `replied` — a human answered. **This is the handoff to Sales.** The card
  moves to Replied, the follow-up date is cleared, and BD is done with it.
  The response returns `handedToSales`; read those names out.
- `sent` — the draft actually left the mailbox, found in Sent. Until this
  lands, a card sitting in Emailed only means a draft exists.
- `clicked` — the guide link was followed.

Every signal is safe to send twice. A repeat comes back `already` and changes
nothing, so an overlapping scan window is fine and re-running after an error
is fine.

## 4. The follow-up

    GET /api/prospects/follow-up-due?brand=oddtoe

Returns `due` — prospects past their follow-up date who have not answered,
with `daysOverdue` and the original `hook` — plus `settings` for the sender
block and unsubscribe line.

**One follow-up per prospect, ever.** The store enforces it; do not ask twice.

For each one:

1. Compose a short nudge. Shorter than the first email — three or four
   sentences. Refer to the original angle in `hook`, do not restate the whole
   pitch, and do not add a new offer. No guilt, no "just bumping this", no
   "following up on my previous email" as the opening line.
2. It must still carry the `unsubscribeLine` verbatim and the sender name, on
   the same rules as the first email.
3. Validate it the same way the first draft was validated:

       POST /api/outreach/validate-drafts

4. Create the Gmail draft with the connector. Keep the draft id.
5. Record it:

       POST /api/prospects/follow-ups
       { "brand": "...", "drafts": [{ "prospectId", "draftId" }] }

   Outcomes come back per prospect: `recorded`, `already` (chased once
   before), `replied` (they answered while you were composing), `suppressed`,
   `not_due`, `not_found`. Read any non-`recorded` outcome out; never retry
   one.

If Gmail succeeded and the record call failed, say so plainly — the drafts
exist and the board is wrong, and Otto must not send until it is fixed.

## 5. Close the silent ones

    POST /api/outreach/auto-close
    { "brand": "...", "days": 14 }

Closes prospects that were followed up and still said nothing after `days`.
The outbound loop ends at one follow-up; without this the board fills with
cards that will never move. Report how many closed and their names — a close
is a real decision, not housekeeping, and Otto may want one of them back.

## 6. The morning brief

    GET /api/outreach/brief?brand=oddtoe

Returns six counts, the follow-ups due, and the replies waiting to be worked.
Read it in this order, because it is the order the work should be done in:

1. **Replies waiting** — a human answered and nobody has responded. Always
   first. Name them.
2. **Follow-ups due** — with days overdue.
3. **Drafted, not sent** — drafts sitting in the mailbox unsent. This is
   usually the real bottleneck, and it is Otto's to clear, not yours.
4. **Ready to draft** — enriched prospects with nobody written to yet.
5. **Stale for close** — what the next auto-close would take.

Keep it to a few lines. A brief that has to be read twice is not a brief.
If every count is zero, say the board is quiet in one sentence.

## Someone asks to be left alone, or the address bounces

    POST /api/suppressions
    { "brand": "...", "email": "...", "reason": "unsubscribed|bounced|asked|manual",
      "detail": "..." }

Do it the moment you see it in the inbox. A bounce recorded only in a note is
not a suppression, and the next import would write to that address again.

## What you must never do

- Never send an email, and never say one was sent. Otto sends every one.
- Never record a reply you did not read in the mailbox. Not from a hunch, not
  from an earlier session's summary, not because a follow-up "probably" got
  an answer.
- Never quote the contents of a reply into a public artefact or a draft to a
  different company.
- Never work around a refusal from the store. `already`, `suppressed` and
  `not_due` are answers, not obstacles.
