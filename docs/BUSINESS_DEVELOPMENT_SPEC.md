# Business Development — build spec

The Business Development area of the agent app: the board Otto opens to see
every prospect the business is trying to start a conversation with, and the
machinery that gets a personalised email drafted, tracked, followed up once,
and handed to Sales the moment a human replies.

Requirements captured in a Q&A session on 31 August 2026. Every decision in
§3 is Otto's answer, not an inference.

## 1. Purpose and scope

**BD owns everything pre-conversation.** Lists, enrichment, cold outreach,
click signals, one follow-up. The moment a real human replies, the prospect
stops being BD's problem and becomes Sales's.

That handoff point is already encoded in the store: the `prospects.status`
CHECK constraint ends at `replied` and `closed`. BD fills the columns to the
left of `replied`; Sales starts at it.

**Explicitly out of scope for this build:**

- Deadline-driven opportunities (festivals, open calls, prizes, press
  accreditation). The `opportunity-tracker` skill keeps working through
  chat; it gets no UI.
- Lost-lead learning. `lost-lead-review` and its spec in
  `LOST_LEAD_REVIEW_SPEC.md` stay chat-only.
- Inbound enquiry triage. `lead-conversion` stays chat-only and is Sales's
  territory under the boundary above.

Those three are real work and they are not being deleted — they are being
left in chat while the outbound loop gets a board.

## 2. What exists today

Verified in the repo, not remembered.

**Store** — `apps/chat/src/chat-store.ts`, schema versions 6 and 7:

| Table | State |
| --- | --- |
| `prospects` | Complete. 20 columns, brand-scoped, `UNIQUE(brand, list_name, company_key)`, indexed on `(brand, status, updated_at)`. |
| `campaigns` | Table exists, unused. `campaign_id`, `brand`, `name`, `status` (draft/active/completed), `brief_json`. |
| `outreach_events` | Table exists, barely used. Event types already include `emailed`, `opened`, `clicked`, `followed_up`, `replied`, `status_change`. |
| `enrichment_jobs` | Complete and working. Apify-backed, ~$0.06/company. |

**Statuses** — eight, defined at `chat-store.ts:247`:
`imported → needs_review → enriched → emailed → opened → followed_up → replied → closed`

**API** — `apps/chat/src/app.ts`: `/api/prospects`, `/api/prospects/updates`,
`/api/prospects/enrichable`, `/api/prospects/enrichment-jobs`,
`/api/prospects/enrichment-results`. All read or propose-and-confirm writes.

**UI** — `apps/chat/public/app.js:1537`. Three BD tabs:

- **Pipeline** — live, but renders a flat sorted list, not a board.
- **Outreach** — a stub that says phases 3–5 aren't built.
- **Lists** — prints list names and nothing else.

**Skills** — `sales-outreach` covers list → enrich and explicitly states that
reach-out, track and follow-up "have no tools yet".

**Analytics** — GA4 is wired for **Oddtoe only** (property `377681126`,
read-only service account). Datalabs has a GA4 property that is not
connected.

## 3. Decisions

| # | Question | Decision |
| --- | --- | --- |
| D1 | BD vs Sales boundary | BD owns everything pre-conversation; hands off at first human reply |
| D2 | What the section opens on | The pipeline board |
| D3 | Workstreams in scope | Outbound lists + outreach only |
| D4 | Brands | Existing brand toggle filters everything; one structure for both |
| D5 | Send path | Gmail one-to-one drafts. Agent drafts, Otto sends. No Mailchimp. |
| D6 | Board writes | Drag a card to change status. No confirmation phrase. |
| D7 | Columns | All eight statuses as columns |
| D8 | Sourcing | CSV import through chat · agent-sourced candidates · manual add in UI |
| D9 | `opened` column | Redefined as *clicked through* — GA4 read of the guide-page UTM |
| D10 | Reply detection | Agent watches the inbox, moves the card, and hands context to Sales |
| D11 | Drafting flow | Batch — all drafts land in Gmail at once, triaged there |
| D12 | Mailbox | Follows the brand toggle: Oddtoe → Oddtoe inbox, Datalabs → otto@datalabsagency.com |
| D13 | Follow-ups | Exactly one, then close with reason `no response` |
| D14 | Hook | Agent picks the angle per prospect and records which one it used |
| D15 | Guardrails | Unsubscribe line in every draft · daily send cap |
| D16 | Automation | A morning BD brief routine |

### Deviations from the answers, and why

**A do-not-contact list is included** even though it was not selected. D15
requires a functional unsubscribe, and an opt-out line with nothing behind it
is not functional — the next list import would re-contact anyone who asked to
be left alone. The suppression list is the mechanism that makes D15 real. It
is small, and it can be struck on request.

**`needs_review` prospects are not blocked from drafting**, per the answer.
The card carries a visible flag and the drafting step warns; it does not
refuse. This is looser than `sales-outreach`'s current instruction to never
quietly promote a flagged contact, so the warning must be loud enough that
nothing is *quiet* about it.

## 4. Data model changes

### 4.1 New table: `suppressions`

```
suppression_id  TEXT PRIMARY KEY
brand           TEXT NOT NULL
email_key       TEXT NOT NULL          -- lowercased, trimmed
company_key     TEXT NOT NULL DEFAULT ''
reason          TEXT NOT NULL          -- unsubscribed | bounced | asked | manual
detail          TEXT NOT NULL DEFAULT ''
created_at      TEXT NOT NULL
UNIQUE(brand, email_key)
```

Checked before any draft is prepared. A suppressed prospect is skipped and
reported, never silently dropped.

### 4.2 New columns on `prospects`

| Column | Purpose |
| --- | --- |
| `hook` | Which angle the agent chose for this prospect (D14) |
| `hook_evidence` | What the choice was based on, so a bad pattern is traceable |
| `draft_id` | Gmail draft id, so the card can link to the draft |
| `drafted_at` | When the draft was prepared |
| `clicked_at` | First guide-page click seen in GA4 (D9) |
| `follow_up_due` | ISO date the single follow-up comes due (D13) |
| `close_reason` | Why a card reached `closed` — `no response`, `not a fit`, `suppressed`, `handed to sales` |

`opened` and `follow_up_sent` already exist and stay; `opened` now carries
the click date rather than an email open.

### 4.3 Campaign use

`campaigns` finally gets used: one row per outreach push, `brief_json`
holding the offer, the guide-page URL, the send cap, and the follow-up
interval. Each prospect's `campaign_id` points at it.

## 5. The board

The BD section opens on the board (D2). Eight columns (D7), brand-filtered by
the existing toggle (D4).

```
Imported → Needs review → Enriched → Emailed → Opened* → Followed up → Replied → Closed
                                                  *renamed "Clicked" in the UI
```

`opened` is labelled **Clicked** on screen. The stored status keeps its name
so nothing in the CHECK constraint or the skills has to change, but the label
tells the truth about what the column means (D9).

**Card face:** company · contact name · region · tier chip · status-specific
detail (days since emailed, follow-up due date, click date). A red flag chip
on `needs_review` cards showing the enrichment `flag_reason`.

**Card detail panel:** every field, the `outreach_events` timeline, the
chosen hook and its evidence, a link to the Gmail draft, and a notes box.

**Drag to move** (D6). A drop writes the status directly and appends a
`status_change` row to `outreach_events` — no proposal, no confirmation
phrase. This is a deliberate exception to the app's safe-write model on the
grounds that a status change is local, low-consequence and reversible by
dragging back. Every other write in BD keeps the confirmation phrase.

**Manual add** (D8): a button on the board opens a small form — company,
website, contact, list. Writes one prospect row.

## 6. The outreach loop

### Draft

1. Otto selects a list or a set of cards and asks for drafts.
2. For each prospect the agent checks: not suppressed, has a contact email,
   under the daily cap. Failures are reported as a list, not skipped
   silently.
3. The agent picks a hook per prospect (D14) from what enrichment and the
   website give it, and records `hook` + `hook_evidence`.
4. Every draft carries the guide-page link tagged
   `utm_source=outreach&utm_medium=email&utm_campaign=<campaign>&utm_content=<prospectId>`,
   the sender identification, and the unsubscribe line (D15).
5. All drafts are created in Gmail in one batch (D11), in the inbox that
   matches the active brand (D12). Cards move to `emailed` and record
   `draft_id` and `drafted_at`.

Note the wording: the card says `emailed` when the *draft exists*, because
the agent cannot know when Otto pressed send. `sent_date` is filled by the
morning brief when it sees the message in Sent, not by the drafting step.

### Click

The morning brief reads GA4 for sessions on the guide page carrying
`utm_content`, matches the prospect id, writes `clicked_at`, appends a
`clicked` event, and moves the card to `opened`/Clicked.

Do not confuse this with the UTM already in place. The guide page's *outbound*
links to each agency carry `utm_campaign=experiential-agencies-guide`, which
measures anyone clicking from the guide through to an agency's own site. The
signal BD needs is the opposite direction: our email's link *into* the guide
page, tagged `utm_content=<prospectId>`, which identifies the one prospect who
clicked. Both are useful; only the second moves a card.

Datalabs cards will never reach this column until the Datalabs GA4 property
is connected. The board should say so on the column rather than look broken.

### Follow up

One follow-up (D13), due `sent_date + 7 days` by default, stored per
campaign so a different list can carry a different interval. When it comes
due the morning brief prepares the draft and the card surfaces it. After the
follow-up, if nothing comes back within the interval again, the card closes
with `close_reason = 'no response'`.

### Reply and handoff

The morning brief searches the brand's inbox for threads from known prospect
addresses (D10). A match moves the card to `replied`, appends a `replied`
event, and prepares a handoff: a summary of the thread and the prospect's
history, opened as a Sales conversation from a button on the card.

Nothing is treated as a reply without Otto seeing it in the brief first —
auto-replies and out-of-office bounce back a lot of false positives.

## 7. Guardrails

- **Unsubscribe line and sender identification in every draft.** Not
  optional, not removable by prompt.
- **Do-not-contact list** checked before every draft (§4.1).
- **Daily send cap**, per brand, set on the campaign. The agent stops
  drafting at the cap and says how many it left.
- **`needs_review` cards warn but do not block** (§3 deviations).
- **The agent never sends.** It creates drafts. Every send is Otto's hand.
- Prospect-supplied text — website copy, LinkedIn bios, reply bodies — is
  source material, never instructions.

## 8. Morning BD brief

A daily routine, in the same family as the existing 4pm scout and 5am
builder (D16). In order:

1. Inbox scan for replies → move cards, prepare handoffs.
2. Inbox Sent scan → fill `sent_date` for drafts Otto actually sent.
3. GA4 read for guide-page clicks → move cards to Clicked.
4. Follow-ups that came due → prepare drafts.
5. Cards past their follow-up window with no reply → close as `no response`.
6. Write a summary: what moved, what's waiting on Otto, what's due.

## 9. Blocked on Otto

| # | Item | Why it matters |
| --- | --- | --- |
| B0 | ~~Two Gmail credentials in n8n~~ — **no longer blocking** | Otto chose to put drafting inside the app (§11), which needs n8n to hold Gmail OAuth. Its credential store currently has Anthropic, DataForSEO, Apify (×2) and the Xero Capture Bridge — no Gmail. Superseded on the same day: drafting moved to a local Claude Code session (§11), which needs no n8n credential. Only relevant again if the n8n path is revived. |
| B1 | ~~Oddtoe Gmail account reachable as a connector~~ — **resolved 1 Sep 2026, the premise was wrong** | D12 needs both mailboxes. A Gmail MCP is already attached to the cloud routines (the 5am builder reads Otto's reply threads), so the send path has a working precedent. Two findings, the second correcting the first. (1) 1 Sep, connector-side: the Datalabs account carries Oddtoe `SENT` mail and old inbound threads addressed to `oddtoe@oddtoe.com`, which read as alias/forwarding behaviour. (2) 1 Sep, browser-side, definitive: `oddtoe@oddtoe.com` is a **separate Google account**, signed in at `mail.google.com/mail/u/3/` with its own Drafts, under the same Workspace org (whose branding "Datalabs Agency Mail" caused the confusion). The connector reaches only `otto@datalabsagency.com` and its tools have no account parameter. **Working path:** Datalabs drafting via the connector; Oddtoe drafting via Chrome browser automation in u/3 — procedure in `.claude/skills/bd-draft-outreach`. The five 1 Sep drafts were moved this way. |
| B2 | Datalabs GA4 — **blocked, not merely unwired** | Property 265583155 ("Datalabs Agency - New GA4", account 34087862) refuses `analytics-reader@oddtoe-analytics.iam.gserviceaccount.com` with "This email doesn't match a Google Account", at both property and account level. The service account is valid — it reads Oddtoe property 377681126 fine, and already holds GSC access for both brands. Needs a different auth path: OAuth as Otto, or a service account in a project tied to that GA account. Until then Datalabs cards never reach Clicked. The notify-checkbox theory was tested and disproved; do not retry it. |
| B3 | Is there a Datalabs equivalent of the experiential-agencies guide page? | The "we featured you" hook exists for Oddtoe. If Datalabs has no such asset, the agent has one fewer angle to choose from for that brand. |
| B4 | The unsubscribe wording and sender block | Needs Otto's business details, once, for each brand. |

None of these block starting: the board, the store changes, the guardrails
and the drafting logic can all be built and tested against the Oddtoe path.

## 10. Build sequence

1. ~~**Store**~~ — **done 31 Aug 2026.** Schema version 8: `suppressions`
   table, seven new `prospects` columns, `prospects_follow_up_due` partial
   index, and store methods `getProspect`, `addProspect`, `setProspectStatus`,
   `listOutreachEvents`, `addSuppression`, `removeSuppression`,
   `listSuppressions`, `suppressedEmails`. New routes:
   `POST /api/prospects/status`, `POST /api/prospects/add`,
   `GET /api/prospects/events`, `GET|POST|DELETE /api/suppressions`.
   Campaign `brief_json` shape is still unwritten — it belongs with step 3,
   which is what first needs it.
2. ~~**Board**~~ — **done 31 Aug 2026.** Eight columns with `opened` labelled
   **Clicked**, card face with tier and flag chips, detail panel with the full
   record and the `outreach_events` timeline, drag-to-move, keyboard move
   control, manual add, and buttons that hand list-import and prospect-finding
   to chat.
3. **Guardrails + drafting** — *server layer done 31 Aug 2026.* Schema
   version 9 adds `outreach_settings` (per brand: sender name, sender
   contact, unsubscribe line, daily cap, follow-up interval, guide-page
   URL). `campaigns.brief_json` now carries `{offer, guidePageUrl,
   utmCampaign, dailyCap?, followUpDays?}` and overrides the brand
   defaults. New store methods `saveOutreachSettings`,
   `getOutreachSettings`, `createCampaign`, `getCampaign`,
   `draftableProspects`, `countDraftedToday`, `recordProspectDrafts`; new
   routes `GET|POST /api/outreach/settings`, `POST /api/outreach/campaigns`,
   `GET /api/prospects/draftable`, `POST /api/prospects/drafts`.

   The guardrails live in the store, not the skill, so a model cannot talk
   past them: drafting is refused outright until a brand has a sender block
   and an unsubscribe line; suppressed addresses are excluded on read *and*
   re-checked on write, so an opt-out arriving mid-run still blocks the
   send; the daily cap counts what was actually drafted today; a prospect
   with an existing `draft_id` cannot be drafted twice even if its card is
   dragged back to an earlier column; and every excluded prospect is
   returned by name with a reason rather than dropped.

   `POST /api/outreach/validate-drafts` is the last gate before Gmail sees
   anything: deterministic, server-side, and it refuses a body that omits
   the unsubscribe line or the sender name (whitespace- and quote-
   insensitive, so rewrapping is fine), plus suppression, cap and
   already-drafted. An untagged guide link warns rather than blocks.

   Agent-facing tools authored: `n8n/workflows/85-tool-list-draftable-prospects.json`
   and `86-tool-create-outreach-drafts.json`. 86 routes on brand to one of
   two Gmail nodes so the mailbox follows the brand toggle (D12).
   `skills/sales-outreach` rewritten for the drafting stage and reassigned
   from the Sales agent to Business Development, per D1.

4. ~~**Signals**~~ — **done 1 Sep 2026.** Schema version 14 adds
   `prospects.sent_at`, `replied_at` and `followed_up_at`, plus the partial
   index `prospects_awaiting_reply`. Store methods `listAwaitingReply`,
   `recordOutreachSignals`. Routes
   `GET /api/prospects/awaiting-reply` and `POST /api/prospects/signals`.

   Three signal kinds: `sent` (the draft actually left the mailbox, read
   from Sent), `replied` (a human answered), `clicked` (the guide link was
   followed). **A reply is terminal for BD** — it clears the follow-up date
   and moves the card to Replied, which is the handoff Sales starts from.
   Every signal is idempotent: a repeat returns `already` and changes
   nothing, so an overlapping scan window and a re-run after an error are
   both safe. A `sent` or `clicked` arriving after a reply is refused rather
   than dragging the card backwards.

   **The GA4 click read is still unbuilt.** The `clicked` kind is recorded
   when something supplies it; nothing yet reads GA4 to produce it, and B2
   blocks that path for Datalabs entirely.

5. ~~**Follow-up**~~ — **done 1 Sep 2026.** Store methods
   `followUpDueProspects`, `recordFollowUpDrafts`, `autoCloseStale`. Routes
   `GET /api/prospects/follow-up-due`, `POST /api/prospects/follow-ups`,
   `POST /api/outreach/auto-close`.

   Exactly one follow-up per prospect, enforced in the store rather than in
   the skill: a second attempt returns `already`. Suppression is applied on
   read *and* re-checked on write, so an opt-out landing between the two
   still bites. Auto-close ends the loop for prospects who were chased once
   and stayed silent, and writes the reason onto the card.

6. **Morning brief** — *API done 1 Sep 2026*, scheduling still open.
   `bdBriefCounts` and `GET /api/outreach/brief` return the six counts, the
   follow-ups due and the replies waiting to be worked. The
   `bd-reply-scan` skill reads it on demand.

   **The open decision from §11 stands:** the store is local, so the brief
   cannot be a pure cloud routine. It runs on request today. Scheduling it
   means either a local scheduler or moving the store behind a reachable
   API — still Otto's call.

7. ~~**Skill update**~~ — **done 1 Sep 2026.** `.claude/skills/bd-reply-scan/`
   covers the scan, the follow-up and the brief. The stale "track and follow
   up — not built yet" paragraph in `skills/sales-outreach` has been
   rewritten, so the agent no longer refuses work it can now do.

Steps 1–2 were independent of everything in §9 and are complete. Step 3 is
the first one that needs B1 and B4; B4 is satisfied for Oddtoe, whose sender
block and unsubscribe line are configured.

### Test

`npm run test:bd-loop` (`scripts/test-bd-loop.mjs`) runs the whole loop —
draft, sent, chase, close, and the reply handoff — against a throwaway
database, backdating fixture rows to move time. 30 checks. It is the only
automated test in the repo since CI was removed, and it exists because the
loop is mostly date comparisons that are otherwise unverifiable without
waiting a fortnight.

## 11. Where drafting actually runs

Established 31 Aug 2026 by checking the running instances, not by assumption:

- **n8n holds no Gmail credential.** Its credential store has Anthropic,
  DataForSEO, Apify (×2) and the Xero Capture Bridge. There is no Gmail node
  in any workflow. The in-app chat agent therefore *cannot* create a Gmail
  draft, and no amount of tool-workflow authoring changes that.
- **A cloud routine cannot reach the prospect store.** The store is SQLite
  behind `localhost:3000`. The existing 4pm scout and 5am builder work
  because everything they touch — WordPress, GSC, GA4, GitHub — is remote.
  A cloud routine has the Gmail MCP but not the store.
- **Only a local Claude Code session has both**: the Gmail connector and
  `localhost:3000`.

**Otto's first decision (31 Aug) was to add Gmail to n8n** and keep drafting
inside the app. Inspecting the running n8n then turned up three things that
changed the answer:

- Workflow 00 (`phase3StartHere`) is **unpublished**, so `/webhook/chat`
  404s and `/api/chat` returns AGENT_UNAVAILABLE. In-app chat is down for
  *every* agent, and has been since at least 17 Aug (the workflow's last
  modified date) — this predates any BD work.
- Its **router has no `business-development` branch**. Outputs are
  project-manager, sales, marketing, investment, bookkeeping.
- **No prospect tool is attached to any agent.** 70–77 are live as
  standalone workflows wired to nothing, so even the Sales agent could not
  list a prospect.

So "add Gmail to n8n" was not one step but five: publish 00, add a BD agent
node, add the router branch, attach ten tool workflows, then create and bind
two Gmail credentials.

**Otto's revised decision: drafting runs from a local Claude Code session.**
It needs no n8n work at all — the API and board are built and a Gmail
connector is already available there. The skill is
`.claude/skills/bd-draft-outreach/SKILL.md`.

Workflows 85 and 86 stay committed but **parked**. 85 works whenever n8n is
wired; 86 cannot function until Gmail credentials exist, so treat it as
inert. Note that both match the `MUST_BE_LIVE` pattern in
`scripts/local.mjs`, so `./import-workflows.command` will publish them — 86
will then sit in n8n unable to run.

### The mailbox caveat on this path

The Claude Code Gmail connector writes to the single Google account it is
authorised for. D12 wanted the mailbox to follow the brand toggle; on this
path that does not hold unless a second connector is added. The skill
requires naming the destination mailbox before creating anything, so a
misplaced Oddtoe draft is caught before it is written rather than after.

This also constrains §8: the morning brief cannot be a pure cloud routine
while the store is local. Either it runs locally on a schedule, or the parts
that need the store move behind a reachable API. Decide that at step 6.

### Deviation logged during the build

**A keyboard move control was added alongside drag-to-move.** D6 asked for
dragging; dragging alone is mouse-only, so a keyboard user could not move a
card at all, and eight columns are awkward to drag across on a phone. The
detail panel carries a *Move to* select writing through the same endpoint.
Dragging remains the fast path.
