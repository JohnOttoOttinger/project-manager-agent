# The Datalabs "traffic collapse" is bots leaving. Organic is up. (4 Sep 2026)

GA4 Home shows sessions −43.9%, active users −47.7%, event count −49.3% over 90 days. Month by
month it looks worse still: **15,734 sessions in Feb 2026 down to 3,469 in Aug — a 78% fall**,
declining every single month.

**It is not a loss of business, and it is not a tracking break.** Split by channel it inverts:

| Month | Direct | Organic Search |
|---|---:|---:|
| Feb 2026 | 14,616 | 916 |
| Aug 2026 | 1,801 | **1,369** |

Direct fell 88%. **Organic search rose 49%**, and August was its best month of the year.

## How we know the Direct traffic was not human

| Feb 2026 channel | Sessions | Engaged | Avg duration |
|---|---:|---:|---:|
| Direct | 14,616 | 8.0% | **5.7 seconds** |
| Organic Search | 916 | 77.6% | 119.3 seconds |

No human cohort averages 5.7 seconds across fourteen thousand sessions. By August the Direct
channel is down to 1,801 at 12.4% engagement, and Organic Search sessions have got *longer* —
206 seconds, up from 119.

Oddtoe is the control: over the same window it runs 974 → 681 → 829 → 664 → 866 → 1,150 sessions,
flat-to-up, on the same service account and the same measurement setup. The anomaly is specific to
the Datalabs property, which rules out a platform or credentials problem.

## A new channel worth watching

**AI Assistant: 74 sessions in Aug 2026, 60.8% engaged, 121s average.** That is ChatGPT,
Perplexity and friends sending real readers, and it behaves like the organic cohort rather than
the junk. It is the first direct measurement of the GEO work paying off, and it did not exist as
a channel earlier in the year.

## What this changes

**Raw GA4 `sessions` is not a business metric on this property** — the same lesson as
[[data-hygiene-rule]] for Search Console impressions, one metric over. Anything that ranked pages
by sessions was partly ranking bots: the Datalabs homepage showed 12,457 sessions over 180 days
and **328 engaged sessions from human channels**. A 97% overstatement.

`candidate-table.py` was fixed the same day to count engaged sessions from human channels only
(Organic Search, AI Assistant, Referral, Organic Social, Paid Search — Direct excluded).

Report the trend as **organic up 49%**, not sessions down 78%. Both are true; only one is about
the business.
