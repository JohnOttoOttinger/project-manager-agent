---
routine: oddtoe-money-page-builder
trigger: trig_016TFL4AeXTT2Ak3AK8mE9Lr
schedule: 0 19 * * * UTC  (5am AEST / 6am AEDT)
---

# Oddtoe money-page builder - 5am

Compose one page as a WordPress **DRAFT**. Never publish - Otto reviews and publishes himself.

Work in the repo checkout. `git pull` first.

## 1. Find out what to build

Read the Gmail thread whose subject starts `Money page candidates - ` (yesterday's date). Match **your own
prefix only**; the other brand's scout uses a different one. Otto's reply is the instruction:

- **a number** - the candidate at that position in yesterday's email
- **"skip"** - stop here. Do not build anything. Do not invent a topic. Send nothing.
- **free text** - that is the page, in his words. It outranks everything.
- **no reply at all** - take the top `queued` item for this brand from
  `python3 skills/money-pages/scripts/suggest.py --list oddtoe`, preferring origin `you`.
  If the top item's status is `blocked`, skip it and say why in the handoff. If nothing is
  queued, stop and report - an empty queue is a real answer.

Then claim it so the 4pm scout stops offering it:

    python3 skills/money-pages/scripts/suggest.py --status <id> drafting

If Otto's reply was free text and no queue item matches, create one first:

    python3 skills/money-pages/scripts/suggest.py oddtoe "<his words>"

## 2. Load the contract before writing

`skills/geo-playbook/SKILL.md` (the rules, including the AI-writing-tells voice guardrail),
`references/brands.md` (canonical sentence, verified facts), `references/banned.md` (overrides
everything), then `skills/money-pages/references/design-kit-README.md` - especially lessons 7-15
- and `references/template-catalog.md` to pick the right template for the page type.

## 3. Compose

Kit: `references/design-kit-oddtoe.html`. Model the script on the closest
`scripts/example-compose-oddtoe-*.py`.

- Article slots are FIRST PERSON ("I take a brief..."). Third person reads as brochure copy.
- **No prices.** Oddtoe pricing is TO FILL in brands.md - delete the pricing table from the kit.
- Honour every `do_not_target` guardrail from the scout email. Those queries are already ranking
  on other pages - mention the topic and link out, never bid for it.
- Sibling keyword forms are ONE page. Do not build two near-duplicates.
- Any statistic needs a real named source you have actually fetched. If you cannot verify it,
  use no statistic. Never invent a client, project, price or number.
- Mark anything needing Otto as `[Otto: ...]` rather than guessing.
- FAQ answers carry markup for the accordion, but the FAQPage JSON-LD must be PLAIN TEXT -
  assert no `<` survives in any `acceptedAnswer.text`.

## 4. Check

    python3 skills/money-pages/scripts/de-ai-check.py <composed.html>

Fix everything it reports and re-run until it passes. Then read the prose in your head - the
linter cannot catch a link sentence that does not parse.

## 5. Push as a draft

    ./skills/money-pages/scripts/wp-post.sh oddtoe "<Page Title>" <composed.html>

Set a flat slug via REST, set `template` to `page-custom.php`, confirm status is `draft`.

## 6. Record it

    python3 skills/money-pages/scripts/suggest.py --status <id> draft

Then append the build record to `references/backlog.md` in the existing format - that file is the
human history and takes the long write-up. `queue.json` is the forward-looking list and stays
short. Commit both, plus the composed HTML.

## 7. Report

Email otto@datalabsagency.com, subject `5am money page: <Page Title>`, with: the title; the
wp-admin review link; the target term with its **verified monthly volume** and where the
incumbent sits; the guardrails honoured; every `[Otto: ...]` gap; the wp-admin page settings REST
cannot set (Custom background `#26161f` + background repeat + header style `6`); and the Yoast title and meta description to paste.

Never publish, never add links to other pages, never touch Search Console - Otto reviews the
draft and asks for those separately.
