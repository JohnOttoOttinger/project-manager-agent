# Oddtoe WooCommerce store — audit

17 Aug 2026. Everything below is from the live site, the WooCommerce admin, GA4
and Search Console.

## Verdict

**The store has never traded.** It is four affiliate links to Redbubble, a
partly broken shop index, one test order from 2021, and a full ecommerce stack
loading on every page of the site to support none of it.

## What is actually there

Four products, all created 2020–2021, nothing since:

| ID | Product | Created |
|---|---|---|
| 11733 | Kim Jong-un Clock | 2021-08-14 |
| 11730 | Sweaty Cabbage Time Clock | 2021-08-14 |
| 11669 | Attracting the Opposite Sex | 2021-03-16 |
| 11526 | Sumo & Cherub Throw Pillow | 2020-07-28 |

All are WooCommerce **external** products — they don't sell anything on
oddtoe.com. Each page says a version of:

> "Additional products with this illustration await you on Oddtoe's Redbubble
> store. Buy This Clock »"

So the store is a shopfront pointing at Redbubble. Prices are all `0.00`, which
is expected for external products but means every listing shows no price.

## What's broken

- **The `/shop/` index lists one of the four products.** Three are published and
  reachable directly but absent from the shop page.
- **`/shop/visualize-workshop/` returns 404** and still received 2 views in the
  last 90 days — a dead product page people are somehow still reaching.
- **`//checkout/`** (double slash) received 2 views. Malformed URL in circulation.
- **One order, ever**: #11667, 15 March 2021, placed by Otto himself via Stripe.
  Still sitting in **Processing** five and a half years later.

## What the numbers say

**GA4, last 90 days** — the entire store:

| Page | Views |
|---|---|
| /cart/ | 10 |
| /shop/attracting-the-opposite-sex/ | 3 |
| /shop/sumo-cherub-throw-pillow/ | 2 |
| /shop/visualize-workshop/ (404) | 2 |
| //checkout/ (malformed) | 2 |
| /shop/ | 1 |

Twenty views in three months. Ten of them reached a cart on a store with nothing
purchasable in it.

**Search Console, 16 months**: no product query earns impressions. The store is
invisible in search.

**GA4 key events**: `purchase` exists as a key event and reports *"No stream data
detected"* — it has never once fired.

## The hidden cost

WooCommerce is fully installed and active. It registers eleven REST namespaces
(`wc/v3`, `wc/store`, `wc-admin`, `wc-analytics`, and more), and ships cart,
checkout and my-account pages plus its scripts and styles across the site. The
homepage already carries 38 script tags and 28 stylesheets, and part of that is
an ecommerce engine supporting four affiliate links and zero revenue.

This is worth weighing against the earlier finding that Core Web Vitals report
"No data" — there isn't enough traffic to measure speed, but the weight is real.

## Three honest options

1. **Retire it.** Delete the four products, deactivate WooCommerce, redirect
   `/shop/*` to the portfolio. Removes the cart, checkout, my-account and
   `purchase` noise, and lightens every page on the site. The Redbubble links can
   live as ordinary links on a portfolio page.
2. **Point at Redbubble properly.** Keep it as a shopfront but fix it — all four
   products on the index, working outbound links, no cart or checkout.
3. **Make it a real store.** Only worth it if there is something to sell that
   isn't print-on-demand. Nothing in the current data suggests demand: no search
   interest, no traffic, no orders in five years.

Option 1 is the honest default. Nothing measured here argues for keeping a
checkout that has processed one self-placed test order since 2021.

## API access notes

- `wc/store/v1` is **public** — products readable with no auth. Used for this audit.
- `wp/v2/product` works with the existing WordPress app password.
- `wc/v3` (orders, customers, reports) returns **403** for `otto-content-agent`;
  it needs a WooCommerce consumer key/secret, or a user with `manage_woocommerce`.
  Not created — there is no order data worth reading.
