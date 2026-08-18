---
name: sourcing
description: Secure and run a vetted supplier network for Oddtoe's physical products — art toys, giant inflatables, bags and soft goods, props, plush, packaging — sourced from the Pearl River Delta. Use when the user asks about suppliers, factories, MOQs, samples, quotes, compliance certs, the China trip, or wants a supplier contacted, compared, or moved along the vetting pipeline.
---

# Sourcing

Oddtoe makes characterful physical things — blind-box art toys, building-sized
inflatables, the Havas ham-bag — and the factories that make them are almost
all inside the Shenzhen–Dongguan–Guangzhou triangle. This skill is the single
source of truth for who those factories are, how far each one has been vetted,
and what happens next.

The full seed context (regional map, capability table, vision, trip notes) is
in `references/sourcing-brief.md`. Read it before proposing new suppliers.

## The register

`references/suppliers.md` — one row per factory, grouped by category
(bags, art toys, inflatables, and whatever comes next). Machine-readable copy
in `references/suppliers.csv`. Every row carries a **status** and a
**next action**, because a supplier list without a next action is a brochure.

Status runs:

`candidate → contacted → certs-received → quoted → sampled → vetted`

…and a supplier can drop to `rejected` at any step (record why — the pattern
of rejections teaches what to screen for earlier).

## The ham-bag gate (vetting standard)

**No supplier passes `certs-received` without documents in writing:**

- Current **social-audit cert** — BSCI or Sedex/SMETA, in date.
- Safety certs for the product class: **EN71 / ASTM F963 / CPSIA** for toys,
  **CE + fire-retardant PVC** for event inflatables.

Compliance claims on a factory's own website are marketing until the PDF is in
Otto's inbox. The register never says "BSCI" on website say-so alone — it says
`claimed, unverified` until the cert is sighted.

## Capability → where to source

| Want to make | Go to |
|---|---|
| 3D-printed masters, prototypes, interactive/LED | Shenzhen (Bao'an; Huaqiangbei) |
| Injection-moulded plastic, art toys, figures | Dongguan |
| Bags, leather goods, giant inflatables | Guangzhou |
| Lighting | Zhongshan (Guzhen) |
| Furniture / large builds | Foshan (Shunde) |
| Toy-moulding at scale | Chenghai / Shantou |

A new product idea starts here: name the capability, pick the town, then look
for two or three candidate factories so there is always a comparison quote.

## Contacting suppliers

First-contact emails ask for exactly three things: the social-audit cert
(current, as PDF), the relevant safety certs, and an indicative quote at
Oddtoe's realistic quantity — not the factory's preferred MOQ. Drafts are
prepared for Otto to send from his own address; the agent does not email
factories directly. Record every contact date in the register.

## Trip planning

Sample-visit trips anchor on a live project (the ham-bag sample anchors the
~mid-September 2026 trip). Fold suppliers into half-days by city — Shenzhen
base, Dongguan ~1 h east, Guangzhou ~1 h north. Practicalities (visa-free
30 days, Alipay/WeChat Pay, VPN needed) are in the brief.

## Before adding anything

Verify a factory exists beyond its own website — a Made-in-China/Alibaba
storefront with transaction history, a checkable address, or a named contact
who answers. A confident row about a ghost factory is worse than a blank.
