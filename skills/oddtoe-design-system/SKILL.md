# Oddtoe Design System

Use this skill whenever designing, theming, or generating visual content for the Oddtoe brand (oddtoe.com — experiential design / generative AI animation studio, Melbourne). Tokens below were extracted from the live site's CSS on 11 Aug 2026. If the site is redesigned, re-extract and update this file.

## Colour palette

| Token | Hex | Usage on oddtoe.com |
|---|---|---|
| Olive (primary accent) | `#8a8f6a` | Button fills, accent backgrounds |
| Deep olive | `#4e5041` | Button hover states |
| Warm sand | `#ddccb1` | Small accent text on dark backgrounds |
| Studio black | `#262b2a` | Dark section backgrounds (green-tinged near-black) |
| Near-black | `#2d2d2d` / `#252f31` | Dark rows, footer |
| Charcoal | `#414141` | Secondary dark fills |
| Soft grey | `#dddddd` | Delimiters, borders on dark |
| Mid grey | `#bcbcbc` | Icon delimiters |
| White | `#ffffff` | Text on dark, light backgrounds |

No bright blues, purples, or saturated reds — the brand is earthy, warm, and theatrical (dark room + warm light, like a projection space).

## Fonts

| Role | Font | Notes |
|---|---|---|
| Display / headings | **Bebas Neue** | Uppercase condensed display; the brand's loudest signature |
| Body text | **Arvo** | Slab serif; warm, sturdy reading text |
| Script accents | **Qwigley** | Handwritten script; use sparingly for subtitles/flourishes only |

All three are Google Fonts. Never substitute a geometric sans for headings — Bebas Neue is the identity.

## Usage rules

1. Dark-first: Oddtoe's home aesthetic is warm-lit content on studio black (`#262b2a`), like work glowing in a dark room.
2. Olive `#8a8f6a` is the action colour (buttons, active states); deep olive `#4e5041` on hover.
3. Warm sand `#ddccb1` for small labels/accents on dark — never for large text blocks.
4. Qwigley is a garnish: one script flourish per view, maximum.
5. Bebas Neue headings are uppercase with generous letter-spacing (0–1px) and tight line-height.
6. Entity separation: never mix Datalabs' palette (its pale olive `#ededb1` band yellow, tan `#c39f76`) into Oddtoe designs, even though both brands share the olive/Bebas DNA. Datalabs' own system lives in `Claude-Projects-2026/datalabs-pages/design-system/`.

## Related

- Brand voice/facts: `skills/geo-playbook/references/brands.md` (once built — see docs/GEO_CONTENT_AGENT_SPEC.md)
- Chat app brand toggle colours: `apps/chat/public/agent.config.js` (`brands` array)
