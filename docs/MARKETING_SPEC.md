# Marketing — build spec

The Marketing area of the agent app: the board Otto opens to see whether the
two businesses are being found, by whom, and through which channel — and the
queues that turn "we are invisible for this question" into a page, a post, or
a campaign.

Requirements captured in a Q&A session on 1 September 2026. Every decision in
§3 is Otto's answer, not an inference.

## 1. Purpose and scope

**Marketing owns demand before a person has a name.** Visibility, audience,
and amplification: GEO/search presence, social following, the email list, and
paid ads. The moment someone identifies themselves — an enquiry, a form fill,
a reply — they stop being Marketing's problem.

The boundary with Business Development is not "who sends email". Both send
email. The line is:

- **Marketing** broadcasts to people who opted in, and publishes to people who
  have not heard of the business yet.
- **BD** writes 1:1 to a named, researched company that never asked.

**Content drafting stays in chat.** This area is not a CMS and does not
replace `seo-article-writer`, `money-pages`, or `geo-playbook`. It shows the
queue and the state, then hands off to chat to actually write. A "Content"
tab was offered in the Q&A and deliberately not taken.

**Explicitly out of scope for this build:**

- A content pipeline tab. This morning's 05:00 draft and any in-flight
  articles surface as a count and a link inside GEO & Search, not their own
  section.
- Publishing to WordPress from the app. The 6am pipeline already writes
  drafts; Otto reviews and publishes in wp-admin. That does not change.
- Anything that posts to a social platform. This area reads follower and
  reach numbers. It never writes.

## 2. What exists today

Verified in the repo, not remembered.

**Skills** — all chat-only today, none has a UI:

| Skill | What it gives Marketing |
| --- | --- |
| `geo-playbook` | The six writing rules; brand separation; canonical brand sentences in `references/brands.md`. Every piece of content depends on it. |
| `money-pages` | `next-best-page.py` ranks live Search Console demand into a page queue with a `do_not_target` cannibalisation guard, and separates title/meta fixes as their own class. `de-ai-check.py` fails machine-sounding drafts. |
| `analytics` | Live GA4 + Search Console reads. **Oddtoe only** — the skill states Datalabs' GA4 property is not wired up. |
| `seo-article-writer` | Draft generation from saved domain research. |
| `paid-domain-research`, `domain-research` | Keyword and competitor evidence behind the queue. |
| `offsite-consensus` | Third-party footprint work — the mentions half of the GEO thesis. |

**Scheduled** — `oddtoe-next-best-page` composes a WordPress draft at 05:00
daily (documented in `money-pages`).

**Store** — `apps/chat/src/chat-store.ts`, schema version 13. Marketing-adjacent
tables that already exist: `seo_snapshots`, `seo_article_jobs`,
`seo_article_versions`, `seo_article_briefs`. There is **nothing** for metric
time series, social followers, ad performance, or email campaigns.

**`campaigns` table** — exists and is unused. `BUSINESS_DEVELOPMENT_SPEC.md`
§4.3 also claims it. See §9 for the collision.

**Strategy** — `GEO_CONTENT_AGENT_SPEC.md` states the business chain this area
must measure:

> Citable page exists → AI assistant retrieves it → assistant recommends the
> business → prospect clicks or searches the brand → lead.

and two findings that shape the metrics below: AI referral traffic converts at
**2–23x** organic, and brand **mentions correlate ~3x more strongly than
backlinks** with AI recommendations.

## 3. Decisions

Otto's answers, 1 September 2026:

1. **One Marketing area with a Datalabs / Oddtoe switcher.** Not two agents,
   not a blended view. Every queue, metric, and draft is brand-scoped;
   nothing is ever summed across the two. Brand order is Datalabs first,
   matching `apps/chat/public/agent.config.js:48` -- the switcher reuses the
   existing runtime `--brand-primary` swap, it is not new machinery.
2. **Four sections:** GEO & search visibility, Social following, Digital ads,
   Email & list.
3. **The top row is the conversion chain**, not a set of loose counters.
4. **Digital ads is a placeholder** until the Meta ad account is reinstated.

### Deviations from the answers, and why

- **"Backlinks Live" is dropped from the metric row.** The Uizard layout had
  it. `GEO_CONTENT_AGENT_SPEC.md` says mentions beat backlinks ~3:1 as a
  predictor of AI recommendation, and nothing in the repo counts either.
  Third-party mentions belong in §5 as a tracked number once a source exists;
  backlinks do not earn a card.
- **Social following did not appear in the offered options** — Otto added it.
  It is built, with the honest caveat in §6 that it is the one section not on
  the conversion chain.

## 4. The four cards — the conversion chain

The top row reads left to right as the chain from §2. Each card is one link.
The point is not the four numbers; it is **finding the link where the chain
breaks.**

| # | Card | Source | Period |
| --- | --- | --- | --- |
| 1 | Citable pages live | Count of published money pages / articles for the brand | Total, with net new this month |
| 2 | Search clicks | Search Console | 28 days vs prior 28 |
| 3 | AI referral sessions | GA4, referrer host in `chatgpt.com`, `perplexity.ai`, `claude.ai`, `copilot.microsoft.com`, `gemini.google.com` | 28 days vs prior 28 |
| 4 | Enquiries | GA4 goal + inbound mail | 28 days vs prior 28 |

**The break indicator.** Each card carries its change against the previous
period. The first card whose growth lags the card to its left is highlighted —
that is the constriction. Pages up 40% and clicks flat means the pages are not
being retrieved. Clicks up and AI referrals flat means the content is not
being cited. Referrals up and enquiries flat means the landing pages do not
convert. One glance, one answer to "what do I work on".

**Datalabs renders "Not connected", not zero.** Cards 2–4 have no data source
for Datalabs until its GA4 property is wired up. A zero reads as "we got no
clicks" and is a lie. The card states the gap and links to the fix.

## 5. GEO & search visibility

The section that does the most work, because it is the one with real data
behind it today.

**Page opportunity queue** — persisted output of `next-best-page.py`. Per
candidate: the query cluster, impressions, current position, the serving page
that is wrong for it, and the computed `do_not_target` list. Sorted by the
pattern that produced `/animation-agency/` — real demand, already appearing,
ranking badly, converting at nothing.

**Title/meta fix lane** — a *separate* queue, not folded into the one above.
These are queries already ranking top-10 with no clicks; they need a headline
rewrite, and proposing a new page over one is self-cannibalisation. The first
run surfaced `prop making companies australia`: 15,015 impressions, position
6.4, 0.01% CTR. That is the cheapest win on the board and it should be
visible as such.

**Today's draft** — the 05:00 WordPress draft, with its `de-ai-check` result
(pass / fail) and a link to review in wp-admin. One line, not a tab.

**AI answer checks** — the actual goal. For a defined set of buying questions
per brand ("who can train my team in Power BI", "experiential projection
studio Melbourne"), record whether an assistant names the brand. This is the
only metric that measures the thing `GEO_CONTENT_AGENT_SPEC.md` is trying to
achieve. Needs the question set defined (§10) and a periodic check; weekly is
enough.

**Third-party mentions** — count of citable off-site appearances, fed by
`offsite-consensus`. Blocked on a source (§10).

## 6. Social following

Otto asked for follower numbers on YouTube, X, Facebook/Instagram, and
LinkedIn.

**Stated plainly: this is the weakest section in the area.** A follower count
sits on no link of the conversion chain and moves too slowly to act on. It is
built because Otto asked for it, with two design choices that make it less
vanity than it would otherwise be:

- **Weekly snapshots, not live.** Followers move slowly; polling daily is
  noise and burns API quota. One row per brand/platform/week.
- **Show the 12-week trajectory, not the number.** "+184 over 12 weeks" is a
  fact you can act on. "3,412 followers" is not.

Feasibility per platform, honestly graded:

| Platform | Route | Status |
| --- | --- | --- |
| YouTube | Data API v3, `channels.list` → `statistics.subscriberCount` | **Straightforward.** Free key; `docs/YOUTUBE_SIGNALS.md` already walks through getting one. |
| Facebook Page / Instagram | Graph API, Page followers + IG `follower_count` | **Likely fine.** Needs a Meta app and a Page token. Page insights are a different permission from ads, so the disabled ad account should not block it — but it is the same Business Manager, so verify before relying on it. |
| LinkedIn | Organization `followerCount` | **Gated.** Needs an approved Marketing Developer Platform app. Approval is not guaranteed and is not quick. |
| X | `users` lookup → `public_metrics.followers_count` | **Costs money.** The free tier does not include user lookup reads. Confirm current pricing before committing to it. |

Recommendation: build YouTube and Meta, leave LinkedIn and X as manually
entered numbers with a "last updated" date until the access question is
settled. A hand-typed number with an honest date beats an empty panel.

## 7. Digital ads — placeholder

Per decision 4, this section is a stub. It states:

- what it will show when live (spend, cost per lead, ROAS against WooCommerce
  orders, creative performance);
- that it is blocked on the Meta ad account (`752951848135271`) being
  reinstated;
- the link to the reinstatement step.

**No data model, no API work, no draft tooling in this build.** If the account
comes back, §11 phase 4 picks it up.

## 8. Email & list

Mailchimp, under the guardrail already established by the agency-list work:
**the agent drafts, a human sends.** Nothing in this section changes that.

- Campaigns: draft / scheduled / sent, with open and click rates for sent.
- List health: size, net change, unsubscribe rate.
- **Where subscribers came from.** The one number here that touches the
  conversion chain — if a money page is producing signups, that is the page
  working, and it belongs next to the page in §5.

## 9. Data model changes

Three new tables, all brand-scoped like everything else in the store.

### 9.1 `marketing_metrics`

One generic time series rather than a table per source. `brand`,
`metric_key`, `period_start`, `period_end`, `value`, `source`, `captured_at`.
Unique on `(brand, metric_key, period_start)`. Every card in §4 and every
trend line in §5 and §8 reads from here.

### 9.2 `social_snapshots`

`brand`, `platform`, `followers`, `captured_at`, `entry_method`
(`api` / `manual`). The `entry_method` column is what lets LinkedIn and X be
hand-entered without pretending they are live.

### 9.3 `page_opportunities`

Persisted output of `next-best-page.py`: `brand`, `cluster`, `impressions`,
`position`, `serving_page`, `do_not_target_json`, `class`
(`new_page` / `title_fix`), `computed_at`. The UI must not shell out to Python
on every render.

### 9.4 The `campaigns` collision

`campaigns` exists, is unused, and is claimed by both this spec and
`BUSINESS_DEVELOPMENT_SPEC.md` §4.3. Marketing campaigns (broadcast, list) and
BD campaigns (outbound, named prospects) are different shapes.

**Resolve before either build touches it.** Cheapest fix: add a `kind` column
(`marketing` / `outreach`) and let both use it. Alternative: Marketing gets
`marketing_campaigns` and leaves `campaigns` to BD. This is a decision, not
something to discover mid-build.

## 10. Blocked on Otto

| Item | Why it matters | Effort |
| --- | --- | --- |
| Connect Datalabs GA4 | Three of the four cards are dead for Datalabs without it | Small |
| YouTube Data API key | Unblocks the one social platform that is easy | ~10 min, free, `docs/YOUTUBE_SIGNALS.md` |
| Define the buying-question set per brand | §5 AI answer checks cannot run without it | One sitting |
| Pick a mentions source | Ahrefs is available in the session but unauthorised | Decision + auth |
| Meta ad account reinstatement | Unblocks §7 entirely | Out of our hands |
| Decide whether X is worth paying for | Otherwise X stays manual | Decision |
| Resolve the `campaigns` collision (§9.4) | Blocks both this and the BD build | Decision |

## 11. Build sequence

1. **Store + chain.** The three tables in §9, the four cards in §4 with the
   break indicator, and the brand switcher. Oddtoe has live data; Datalabs
   shows "Not connected" honestly.
2. **GEO & search.** Persist `next-best-page.py` output, render both queues,
   surface the 05:00 draft and its `de-ai-check` result.
3. **Social + email.** YouTube and Meta on a weekly snapshot; LinkedIn and X
   manual. Mailchimp read, draft-only.
4. **Ads.** Stub only. Revisit if and when the account is reinstated.

AI answer checks (§5) can land any time after phase 1 — they depend on the
question set, not on the other phases.

## 12. Phase 1 trim — what is deliberately not being built

Decided 1 September 2026, when Otto asked what in phase 1 is development-heavy
and not yet needed. Two sections come out. Both were in the Q&A answers, so
this is a sequencing call, not a reversal.

### Deferred: Social following

**Four integrations for a number that sits on no link of the chain.** YouTube
needs a Data API key, Meta needs an app plus a Page token, LinkedIn needs an
approved Marketing Developer Platform app that may not be granted, and X needs
a paid tier. That is the highest integration cost in the whole spec for the
lowest decision value — a follower count never tells you what to do next.

**Interim:** the `social_snapshots` table (§9.2) still gets created, with
`entry_method` defaulting to `manual`. Numbers typed in once a month with an
honest date give the trajectory without a single API call. If the trajectory
turns out to be worth watching, automate YouTube first — it is the only one
that is both free and ungated.

### Deferred: AI answer checks

**No clean API exists for the question being asked.** "Does Google's AI
Overview name Oddtoe" cannot be read from an endpoint, and automating the
assistant checks means driving four separate surfaces on a schedule and
parsing prose for a brand name. That is real engineering for a number that
moves monthly at best.

**Interim:** run the check by hand. Five questions across four assistants is
about twenty minutes once a month, recorded straight into `marketing_metrics`.
The manual version produces the identical number, and doing it by hand first
is how you learn what the automated check would need to look for.

### What stays in phase 1

The chain (§4), both GEO queues (§5), and the ads stub (§7). The chain is the
spine and the queues are the only part with live data behind them today.

### Revised sequence

1. Store + chain + brand switcher.
2. GEO: persist `next-best-page.py` output, both queues, the 05:00 draft.
3. Ads stub. Email & list.
4. Social, manual entry only.
5. Automate anything above that has earned it.
