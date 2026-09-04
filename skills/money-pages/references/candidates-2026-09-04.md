<!-- Regenerate: python3 skills/money-pages/scripts/candidate-table.py --limit 10 --per-brand 5 -->

# Next-page candidates — every source, 180d, Australia only

Sweep captured 2026-08-28. GSC/GA4 to 2026-09-01. AU clicks are machine-filtered; impressions are not bankable, clicks are.

| # | term | brand | AU vol/mo | comp | CPC | incumbent | our AU clicks | our impr | our pos | nearest page | GA4 sess | GA4 events | slug | score | already queued |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | data analytics courses | datalabs | 2,400 | MEDIUM | - | nexacu.com.au #45 | 0 | 194 | 38.7 | / | 12457 | 0 | 404 | 2.87 | Data Analytics Classes |
| 2 | classes for data analysis | datalabs | 2,400 | MEDIUM | - | nexacu.com.au #48 | 0 | 194 | 38.7 | / | 12457 | 0 | 404 | 2.87 | Data Analytics Classes |
| 3 | gantt charts | datalabs | 33,100 | ? | - | nexacu.com.au #53 | 0 | 12 | 12.2 | /2024/06/24/15-most-common-types-of-data-visualization/ | 478 | 0 | 404 | 2.11 | Gantt chart explainer |
| 4 | power bi course | datalabs | 1,600 | ? | - | nexacu.com.au #3 | 0 | 46 | 38.7 | /product/introduction-data-visualization-course/ | 130 | 0 | 404 | 1.91 | Power BI training |
| 5 | microsoft power bi training | datalabs | 210 | LOW | $8.63 | - | 0 | 0 | - | - | - | - | 404 | 1.86 | Power BI training |
| 6 | experiential agency | oddtoe | 50 | ? | - | - | 0 | 185 | 35.6 | /animation-agents/ | 1007 | 0 | 404 | 1.16 | - |
| 7 | interactive installation art | oddtoe | 40 | ? | - | eness.com #22 | 0 | 0 | - | - | - | - | 404 | 1.16 | - |
| 8 | interactive installation | oddtoe | 30 | ? | - | - | 0 | 2 | 7.5 | /artist-designer/installation-artist/ | 23 | 0 | 404 | 1.0 | - |
| 9 | immersive experience melbourne | oddtoe | 320 | HIGH | - | - | 0 | 0 | - | - | - | - | 404 | 0.9 | - |
| 10 | projection mapping melbourne | oddtoe | 20 | ? | - | - | 0 | 0 | - | - | - | - | 404 | 0.88 | How much does projection mapping cost? |


## What the GA4 columns can and cannot tell you (checked 4 Sep 2026)

`GA4 events` is key events — conversions. It reads 0 on every row, and that is not a rounding
problem with these particular pages:

| Brand | Sessions 180d | Engaged | Key events 180d |
|---|---:|---:|---:|
| Datalabs | 32,279 | 8,236 | **0** |
| Oddtoe | 5,050 | 1,490 | **5** (`ThankYouOddtoeClicks`) |

**Datalabs has no key events configured at all.** `begin_checkout` fired 6 times and `click`
2,437 times in the window, but nothing is marked as a conversion, so GA4 cannot report one.
Until that is fixed, any ranking claiming to sort pages by business result is really sorting by
sessions. The Gravity Forms entries are the more truthful conversion record for enquiries — see
the parked `gravity-forms-attribution` work.
