# Measurement health — what the numbers can and cannot carry

The single page to read before quoting any figure from either brand. Updated 4 Sep 2026.

## The rule

**Rank and report on clicks and engaged sessions from human channels. Never on impressions,
never on raw sessions.** Both brands carry heavy machine traffic, in two different metrics, and
both have at some point been used to justify a decision they could not support.

| Metric | Status | Why |
|---|---|---|
| GSC impressions | **Do not use** | Up to 91% machine-generated on some pages (Oddtoe homepage). Query enumeration, almost entirely offshore. |
| GSC clicks | **Trust**, AU-filtered | Only a person clicks. Filter to Australia; the AU filter alone dropped the Oddtoe prop page from 78% machine-shaped to 5%. |
| GA4 `sessions` | **Do not use** | Contaminated by the Direct channel on both properties — see below. |
| GA4 engaged sessions, human channels | **Trust** | Organic Search, AI Assistant, Referral, Organic Social, Paid Search. Direct excluded. |
| GA4 key events | **Trust from 4 Sep 2026** | Before that date Datalabs recorded none at all, because its key event's rule was circular. Not retroactive. |
| WooCommerce ecommerce events | **Do not use** | The plugin is pointed at a property that died in 2023. See `ga4-ecommerce-datalabs.md`. |

## The Direct-channel contamination, both brands (180 days)

| | Sessions | Engaged | Avg duration |
|---|---:|---:|---:|
| Datalabs Direct, Feb 2026 | 14,616 | 8.0% | **5.7 s** |
| Datalabs Organic, Feb 2026 | 916 | 77.6% | 119.3 s |
| Oddtoe Direct, 180d | 2,920 | 12.7% | 32.3 s |
| Oddtoe Organic, 180d | 1,909 | 54.0% | 124.2 s |

Datalabs' Direct traffic has since decayed to 1,801/month, which reads on GA4 Home as a 78%
collapse and is nothing of the kind — organic rose 916 → 1,369 over the same window. Oddtoe has
the same disease at a tenth the scale.

**Real human traffic, most recent full month:** Datalabs ~1,369 organic; Oddtoe ~1,909 organic
per 180 days. Those are the numbers to plan against.

## AI Assistant — the channel that matters most from here

Growing on both brands, and behaving like humans, not bots:

| Month | Datalabs | Oddtoe |
|---|---:|---:|
| Jun 2026 | 43 | 7 |
| Jul 2026 | 63 | 4 |
| Aug 2026 | **74** | **30** |

Engagement 55–61%, average duration around two minutes — the same shape as organic search. This
is the GEO work becoming measurable for the first time.

### What the assistants actually cite (Datalabs, 180d, by landing page)

    26  /2026/03/29/9-incredible-examples-of-interactive-data-visualization/
    25  /2026/05/11/data-visualization-websites/
    24  /2026/03/26/data-analytics-conferences-2026-2027/
    22  /
    18  /case-studies/
    16  /animated-data-videos/

**Almost all of it is reference and listicle content, not service pages.** The pages earning AI
citation are the ones that answer "show me examples of X", and they are largely disconnected from
the pages that sell anything. That is a strategy finding, not a tracking one: the GEO play is
reference content that links into the money pages, and the internal linking from these specific
posts is worth auditing first.

## Open measurement defects

1. **Ecommerce events go to a dead property.** `ga4-ecommerce-datalabs.md`. Needs admin.
2. **`G-ST757S330F` is configured twice per page**, by Site Kit and the WooCommerce plugin. Fix
   only after the repoint above, or ecommerce tracking stops entirely.
3. **Dead `UA-34087862-1` tagged 4x per page**, including by a plugin that exists only to inject
   it. Needs admin.
4. **Whether any WooCommerce order completed in 180 days is still unknown** — the number that
   decides whether `purchase: 0` is a bug or an empty till. Needs admin.
5. **Oddtoe has one key event** (`ThankYouOddtoeClicks`, 5 in 180d). Worth the same treatment
   Datalabs just had.
