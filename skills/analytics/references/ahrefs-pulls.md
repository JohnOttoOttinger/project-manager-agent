# Ahrefs assisted pulls

Otto is on **Ahrefs Webmaster Tools (free)**. No API, no CSV export, no alert
emails — all three are paid. What the free tier *does* give is full in-browser
access to reports that Search Console cannot replicate at all: competitor
keywords, competitor traffic, and the real texture of a backlink profile.

So Ahrefs is an **assisted** source: Otto opens the tab, the agent reads the
screen, and **the agent writes what it read into `references/ahrefs/` as a dated
snapshot**. That last step is the whole point — it turns a one-off glance into a
series that can be compared month over month, which is most of what an API would
have bought.

## The standing rule

Never read an Ahrefs report and only answer in chat. **Always** write a snapshot
to `references/ahrefs/YYYY-MM-DD-<report>.md` at the same time. A read that isn't
recorded is a read that has to be repeated.

## What to pull, and when

| Report | Cadence | Why |
|---|---|---|
| **Organic competitors** | Monthly | Who shares Oddtoe's search space, and whether that's shifting toward buyers or away |
| **Backlinks** | Monthly | New links, and whether the spam volume is still climbing |
| **Content gap** | Quarterly, or before planning a page | Terms competitors rank for that Oddtoe doesn't — the single best input to a content decision |
| **Site Audit** | Quarterly, or after a big change | Technical crawl; catches what GSC reports slowly |
| **Keywords Explorer** | Ad hoc | Volume and difficulty for a specific term being considered. GSC only shows terms Oddtoe *already* ranks for, so this is the only way to size something new |

Monthly is deliberate. Backlink and competitor data moves slowly, and a cadence
Otto can actually keep beats an ambitious one he abandons.

## Working URLs (verified 17 Aug 2026)

Oddtoe's Ahrefs `projectId` is **1549831**. The `target` needs a trailing slash,
URL-encoded as `%2F` — without it every report 404s. That cost twenty minutes to
work out; don't rediscover it.

    Organic competitors
    https://app.ahrefs.com/site-explorer/organic-competitors?mode=subdomains&projectId=1549831&target=oddtoe.com%2F

    Backlinks
    https://app.ahrefs.com/site-explorer/backlinks?mode=subdomains&projectId=1549831&target=oddtoe.com%2F

    Alerts
    https://app.ahrefs.com/alerts

    Plan and limits
    https://app.ahrefs.com/account/limits-and-usage

**Known 404s on this plan:** `referring-domains`. Use **Backlinks** instead — it
carries the same information with more detail, grouped by linking page.

**Content gap** has no stable URL; it needs competitor targets selected in the
form. Reach it from the Site Explorer sidebar under Competitive analysis.

## How to ask Otto

He runs dozens of Chrome tabs and has asked, explicitly, for **deep links rather
than breadcrumb directions** whenever a step needs his clicks. Give him the URL,
say which report, and say what will be done with it. One request per pull, not a
checklist of five.

## Reading the screen

The Ahrefs app returns nothing to DOM queries — `javascript_tool` comes back
empty every time. **Screenshots are the only way to read it.** The app also
renders small; zoom into a region rather than squinting at a full-page capture.

Tables paginate at 100 rows. For a first pass the top page sorted sensibly
(traffic descending for competitors, first-seen descending for backlinks) is
almost always enough to answer the question.

## What Ahrefs is genuinely for here

Not Oddtoe's own performance — GA4 and Search Console cover that automatically
and in more detail. Ahrefs earns its place on three questions those two cannot
answer at all:

1. **Who else ranks for this, and how strong are they?**
2. **What are they ranking for that we aren't?**
3. **Is a term worth chasing** — volume and difficulty for something Oddtoe
   doesn't yet rank for, which GSC is structurally blind to.

Frame every pull against one of those. A pull that just restates GSC data is
wasted effort and wasted goodwill.
