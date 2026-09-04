# Datalabs ecommerce tracking — diagnosed 4 Sep 2026, NOT fixed (blocked on admin)

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

## Three separate defects

### 1. `G-ST757S330F` is configured TWICE on every page

Site Kit and the WooCommerce GA plugin each inject their own Google tag — 2 `gtag('config',
'G-ST757S330F')` calls and 3 `gtag.js` script tags per page load. Duplicate tagging inflates
pageviews and makes event delivery unpredictable.

**Fix:** pick one owner of the GA4 tag. Keep the WooCommerce plugin's (it is the one that sends
ecommerce), and turn Site Kit's Analytics snippet off — Site Kit → Settings → Analytics →
disable snippet insertion, keeping the property connection for reporting.

### 2. Dead Universal Analytics tag still on every page

`UA-34087862-1` appears 4 times per page. Universal Analytics stopped processing data in 2023.
Harmless, but it is dead weight and it confuses anyone auditing the tagging. Remove it.

### 3. `add_to_cart` never fires — most likely express checkout

The plugin is present, capable, and correctly fed, so the event is not missing for want of
product data. The likeliest cause is the **express checkout path**: a buyer using the PayPal or
WooPayments express button goes product → payment sheet directly and never touches the cart, so
no add-to-cart interaction exists to capture. That also fits `begin_checkout` being tiny (6) while
`view_item` is 481.

**To confirm:** open a product page in an incognito window with GA4 DebugView running, click the
ordinary **Add to cart** button, and watch whether `add_to_cart` arrives. If it does, the ordinary
path is fine and the gap is entirely express checkout. If it does not, the plugin's event settings
need checking in WooCommerce → Settings → Integration → Google Analytics.

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
