# Datalabs ecommerce tracking — FIXED 4 Sep 2026

Follows on from `ga4-key-events-datalabs.md`. The enquiry conversions are now counted; the shop
still is not.

## What GA4 receives today (180 days)

    view_item_list 15,238 → view_item 481 → add_to_cart 0 → begin_checkout 6 → purchase 0
                                            remove_from_cart 2

**`add_to_cart` is provably broken.** You cannot begin checkout, and you certainly cannot remove
from cart, without adding to cart first. Six checkout starts and two removals against zero adds
is not a low conversion rate, it is a missing event.

**`purchase` is undetermined.** Zero purchases is what you would see if the tracking were broken
*and* also what you would see if nobody completed an order. The two cannot be separated without
the WooCommerce order count — see "The one number that decides it" below.

## What is actually installed (read from the live product page)

- **Google Analytics for WooCommerce** — `woocommerce-google-analytics-integration`, loading
  `assets/js/build/main.js`. It registers all the right event names, and **its data layer is
  correctly populated**: product 24182 "Power BI Templates", category Digital Products, price
  109800 minor units (AU$1,098), currency AUD. The plugin has everything it needs.
- **Site Kit**, which also injects a Google tag.
- **WooCommerce Payments**, **PayPal (PPCP / smart buttons)** and **Stripe** — the product page
  carries a "Secure express checkout frame" beside the ordinary Add to cart button.

## ROOT CAUSE — the ecommerce plugin is pointed at a property that died in 2023

Read straight off the live product page, by script id:

| Script block | Configures |
|---|---|
| `woocommerce-google-analytics-integration-gtag-js-after` | **`UA-34087862-1`** |
| `google_gtagjs-js-after` (Site Kit) | `G-ST757S330F` |
| `GA Google Analytics` plugin (m0n.co/ga), inline | `UA-34087862-1` |

**The plugin that generates every ecommerce event is configured with the dead Universal Analytics
property, not the GA4 one.** Universal Analytics stopped processing data in July 2023.

**Verified 4 Sep 2026: the UA property no longer exists.** The Google Analytics account
*Data Arts Master Account* (34087862) contains exactly two properties — Datalabs GA4
(265583155) and Oddtoe - GA4 (377681126). There is no Universal Analytics property to select,
so `UA-34087862-1` is not merely stale, it is an address with nothing behind it. Every ecommerce
event the plugin sends to it is discarded.

There is therefore **nothing to delete on the Google side**. The only UA left anywhere is the tag
on the website.

Its events reach GA4 today only by accident: Site Kit separately configures `G-ST757S330F` on the
same page, and `gtag()` broadcasts an event to *every* configured destination. That is why
`view_item` and `view_item_list` show up at all — they are riding on Site Kit's config, not on
the plugin's own.

### This invalidates the earlier recommendation

An earlier version of this file said to fix the duplicate tagging by turning off Site Kit's
snippet and keeping the WooCommerce plugin's. **Doing that first would have killed ecommerce
tracking completely**, because Site Kit's config is currently the only thing pointing at GA4.
Order matters, and it is the reverse of what it looked like.

## APPLIED 4 Sep 2026 (Otto granted admin; changes made in wp-admin)

| Step | Result |
|---|---|
| Repoint WooCommerce plugin to `G-ST757S330F` | **DONE**, verified server-side on home, product and post |
| Deactivate + delete `GA Google Analytics` (m0n.co/ga) | **DONE** — "was successfully deleted" |
| `UA-34087862-1` on the site | **0 references**, site-wide |
| legacy `analytics.js` library | **gone** |
| Site Kit snippet | **left ON, deliberately** — see below |

The plugin's Event Tracking checkboxes were already all ticked — Purchase Transactions, Add to
Cart, Remove from Cart, Product Impressions, Product Clicks, Product Detail Views. Nothing was
disabled. The events were configured to fire the whole time and were being sent to a property
that no longer exists.

### Why Site Kit's snippet was NOT turned off

The original plan said to remove it as a duplicate. On inspection that is wrong: Site Kit is
Google's own plugin and is the natural owner of site-wide pageview tracking, while the WooCommerce
plugin exists to send ecommerce events and should not be the only tag on the site.

### The third tag — pre-existing, left alone

The homepage carries THREE `gtag('config','G-ST757S330F')` calls:

    woocommerce-google-analytics-integration-gtag-js-after   (WooCommerce plugin, correct)
    google_gtagjs-js-after                                   (Site Kit, correct)
    jquery-migrate-js-after                                  (a hand-injected Google tag snippet)

The third predates this work — it already configured GA4 before today. It is **not** from WPCode
(its 6 snippets are Yoast/schema/Mailchimp/comments, no gtag). Source not yet identified; likely a
theme option or a header-script field.

**It is not causing measurable harm.** Page views to sessions runs 38,560 / 32,004 = **1.20**.
Triple-counting would show roughly 3.0. Worth removing as housekeeping, not urgent.

### Still unverified: does `add_to_cart` now fire?

Could not be tested from Otto's browser — it blocks analytics (zero `collect` requests, the
plugin's `main.js` blocked from loading client-side while present server-side). A real add-to-cart
was performed and the cart did populate, so the click path works. **Check GA4 in 24-48 hours**
for `add_to_cart` against real traffic.

## The original fix plan, for reference

1. **Point the WooCommerce plugin at GA4.** WooCommerce → Settings → Integration → Google
   Analytics (or the plugin's own settings screen). Replace `UA-34087862-1` with
   **`G-ST757S330F`**. Nothing else should change until this is done and verified.
2. **Verify in GA4 DebugView** that `view_item` still arrives, then that `add_to_cart` arrives
   when the ordinary Add to cart button is clicked in an incognito window.
3. **Only then, remove the duplicate tag.** Site Kit → Settings → Analytics → stop it inserting
   its own snippet, keeping the property connection for reporting. Re-check DebugView afterwards.
4. **Delete the `GA Google Analytics` plugin** (m0n.co/ga). It exists solely to inject the dead UA
   property and does nothing else. Nothing on the site needs it.
5. **Re-test `add_to_cart` via express checkout.** If it still never fires when a buyer uses the
   PayPal / WooPayments express button, that path genuinely bypasses the cart and the honest
   answer is that express-checkout buyers cannot produce an add-to-cart event — in which case
   `begin_checkout` and `purchase` are the events that matter for them.

## The one number that decides it — ANSWERED

**One.** WooCommerce holds 216 orders all-time (188 completed), but by date the recent list reads:
Apr 12 2026 (Failed), Apr 2 2026 (Processing, $450), **Mar 19 2026 (Completed, $45)**, then Feb 9,
then Nov 2025. Inside the 180-day window there is exactly **one completed order**.

So `purchase: 0` in GA4 was very nearly correct on its own terms. The repoint was still right —
events were going nowhere — but purchase tracking was never going to be a meaningful signal at
this volume. **The shop is close to dormant, and that is a commercial finding, not a tracking one.**

Original framing below.

**How many WooCommerce orders completed in the last 180 days?**

- If the answer is **0**, then `purchase: 0` is correct, nothing is broken about purchase
  tracking, and the real problem is commercial, not technical — 481 product views and no sales.
- If the answer is **more than 0**, purchase tracking is broken and every sale is invisible to
  GA4, which also means the money-page ranking can never see which pages produce revenue.

## Why this could not be fixed from here

Both available routes are Editor-level and neither can reach WooCommerce or plugin settings:

- The `.env` API user is `otto-content-agent (do not delete)`, role **editor**, no
  `manage_options`. `GET /wp-json/wc/v3/orders` returns **403 woocommerce_rest_cannot_view**.
- The Chrome session is signed in as the same user. `wp-admin/admin.php?page=wc-orders` returns
  **"You need a higher level of permission."**

Fixing any of the three defects means changing plugin settings, which needs an administrator.
Otto either does it himself or grants admin to the agent user — the latter is a real decision,
not a formality, since it would give automation the ability to change a live commercial site.
