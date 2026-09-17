# Datalabs GA4 conversions — diagnosed and fixed 4 Sep 2026

**Property 265583155. 32,304 sessions in 180 days, 0 key events.** Anything that claims to rank
pages by business result is really ranking sessions until this is fixed.

## What is actually happening on the site

Conversions ARE occurring. GA4 just isn't told which pageviews mean one:

| Completion page | Views 180d | Sessions | By month (Mar→Aug) |
|---|---:|---:|---|
| `/thank-you/` | 26 | 25 | 6, 4, 8, 7, 3, 4 |
| `/thank-you-download-free-dashboard/` | 5 | 5 | — |
| `/thank-you-download/` | 1 | 1 | — |

`/thank-you/` is reached almost entirely from `/contact-us/`, and it fires every single month.
That is a live enquiry path — roughly **one enquiry every 6 days**, none of it counted.

## The funnel as GA4 currently records it

    32,304 sessions → 176 contact-us → 1,229 cart → 6 begin_checkout → 0 purchase

`purchase`, `add_to_cart`, `form_start`, `form_submit` and `generate_lead` do not fire at all.
`view_item` (481) and `begin_checkout` (6) do. So WooCommerce tagging is **half-wired**: the
browsing events reach GA4 and the money events do not. 1,229 cart views producing 6 checkout
starts is not a real conversion rate, it is missing instrumentation.

## Fix 1 — count the enquiries (3 minutes, do this first)

GA4 cannot mark a pageview as a conversion directly. Create a custom event from it, then mark
that as key. This is the same pattern Oddtoe already uses (`ThankYouOddtoeClicks`).

1. GA4 → **Admin** → **Events** (under Data display) → **Create event** → **Create**
2. Custom event name: `enquiry_submitted`
3. Matching conditions:
   - `event_name` **equals** `page_view`
   - `page_location` **contains** `/thank-you/`
4. Leave "Copy parameters from the source event" ticked → **Create**
5. Admin → **Key events** → **New key event** → name it `enquiry_submitted` exactly → save

**Not retroactive.** GA4 counts from creation onward; the 26 historical completions stay
uncounted. The sooner it exists the sooner the ranking has something real to stand on.

## Fix 2 — count the lead-magnet downloads (separate event)

Same steps, custom event `guide_downloaded`, condition `page_location` **contains**
`/thank-you-download`. Keep it separate from `enquiry_submitted` — a downloaded PDF and a person
asking for a quote are not the same conversion and should never share a number.

## Fix 3 — the ecommerce hole (bigger job)

`add_to_cart` and `purchase` are missing. Check whether the WooCommerce → GA4 integration
(GA4 plugin / GTM container) has ecommerce events enabled and the data stream's Enhanced
Measurement is on. Until then the course and template sales are invisible, and `begin_checkout`
at 6 against 1,229 cart views should be treated as broken rather than as a real drop-off.

## DONE 4 Sep 2026 (in the GA4 UI, on Otto's explicit go-ahead)

The original setup was **already broken in a way the numbers could not show**. A key event named
`FormFilloutThankYou` existed and was starred, but its custom-event rule was circular:

    event_name equals FormFilloutThankYou  AND  page_location contains thank-you

It triggered on an event of its own name — which nothing ever emitted — so it could only ever
create itself. That is why 180 days produced zero conversions despite the thank-you page being
visited every month. Marking something as a key event was never the missing piece.

Two custom events now exist and both are key events:

| Custom event | Conditions | Feeds |
|---|---|---|
| `FormFilloutThankYou` | `event_name equals page_view` + `page_location contains /thank-you/` | the pre-existing key event, which now receives data |
| `guide_downloaded` | `event_name equals page_view` + `page_location contains /thank-you-download` | new key event |

Reusing the name `FormFilloutThankYou` was deliberate: the key event of that name already
existed, so populating it needed no second key-event definition and no naming drift.

The trailing slash matters. `/thank-you/` does **not** match `/thank-you-download/`, so the
enquiry count stays clean of lead-magnet downloads — they are counted separately, because a
downloaded PDF and someone asking for a quote are not the same conversion.

`purchase` is listed as an event but is **not** starred as a key event, and does not fire anyway
(see Fix 3).

### The old circular rule — DELETED 4 Sep 2026 on Otto's instruction

It had to go: the new rule emits `FormFilloutThankYou` on a page whose URL contains `thank-you`,
which is exactly what the old rule matched on, so it would have created a second event from the
first. GA4 warns against a created event matching its own conditions; the risk was a doubled
count or a loop.

Deleting the custom-event rule does **not** remove the key event of the same name — verified
after deletion, both key events remain starred. Only two custom-event rules now exist, and both
are correct.

**Sanity check in a few days** (`Reports → Engagement → Events`): `FormFilloutThankYou` should
track the `/thank-you/` pageview count roughly 1:1. Materially more than that would mean
something else is still emitting it.

## Why this could not be done from the repo automatically

Two independent blockers, both verified 4 Sep 2026:

- The service account holds **read-only** scopes (`analytics.readonly`, `webmasters.readonly`).
  Creating a key event needs `analytics.edit` plus an Editor role on the property.
- The **GA4 Admin API is not enabled** on GCP project 151799608371 — every
  `analyticsadmin.googleapis.com` call returns 403.

Neither should be changed casually: granting an automation write access to analytics config is a
bigger decision than the 3 minutes the UI takes.
