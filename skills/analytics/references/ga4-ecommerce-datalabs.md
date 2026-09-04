# Datalabs ecommerce tracking — root cause found 4 Sep 2026, NOT fixed (blocked on admin)

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

Its events reach GA4 today only by accident: Site Kit separately configures `G-ST757S330F` on the
same page, and `gtag()` broadcasts an event to *every* configured destination. That is why
`view_item` and `view_item_list` show up at all — they are riding on Site Kit's config, not on
the plugin's own.

### This invalidates the earlier recommendation

An earlier version of this file said to fix the duplicate tagging by turning off Site Kit's
snippet and keeping the WooCommerce plugin's. **Doing that first would have killed ecommerce
tracking completely**, because Site Kit's config is currently the only thing pointing at GA4.
Order matters, and it is the reverse of what it looked like.

## The fixes, in the order they must happen

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

## The one number that decides it

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
