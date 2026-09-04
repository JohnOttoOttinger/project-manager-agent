# Datalabs GA4 records no conversions — what to fix (4 Sep 2026)

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

## Why this could not be done from the repo

Two independent blockers, both verified 4 Sep 2026:

- The service account holds **read-only** scopes (`analytics.readonly`, `webmasters.readonly`).
  Creating a key event needs `analytics.edit` plus an Editor role on the property.
- The **GA4 Admin API is not enabled** on GCP project 151799608371 — every
  `analyticsadmin.googleapis.com` call returns 403.

Neither should be changed casually: granting an automation write access to analytics config is a
bigger decision than the 3 minutes the UI takes.
