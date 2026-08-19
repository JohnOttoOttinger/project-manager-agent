# Brand Image Pipeline — project requirements & description

**Status:** SPEC — approved direction (Otto, 19 Aug 2026), not yet built.
**Owner:** Otto (art direction, approvals) · Agent (build, operation).
**Companion project:** Video/animation at scale — separate future project, scoped in §9 only.

## 1. Purpose

Produce website and content images for both brands at scale with generative AI, in each
brand's own visual style, with Otto art-directing once rather than per image. Otto is an
artist with an existing style — the system's job is to reproduce *his* look at volume,
never a generic AI look.

Demand today: guide/money pages need ~17 images each (hero, 4 picks, ~12 entries at
300×300); the Datalabs image estate is 164 images with a large alt-text backlog; every
future money page, guide page and post needs art. Interim practice (totem placeholder on
page 16173) proves the layouts but not the art.

## 2. Brands = two isolated style systems

- **Oddtoe** — plum `#26161f` / sand `#ddccb1` / wine `#210209`, quirky illustration,
  "art of the odd". Voice of the artist Oddtoe.
- **Datalabs** — dark `#2f2e3a` / tan `#c39f76`, clean data-viz-flavoured illustration,
  icons, diagram-adjacent art.
- **Hard rule (geo-playbook banned.md #6):** no brand blending. One style anchor, one
  fine-tune, one output folder per brand. A generation job is always brand-tagged.

## 3. Architecture (three layers)

1. **Style layer** — per brand: a *style anchor* (20–40 of Otto's own best images +
   a locked prompt prefix + negative prompts) and, if the spike justifies it, a **LoRA
   fine-tuned on Flux** (fal.ai or Replicate; ~$5 and ~30 min to train, re-trainable
   when the style evolves). Style anchors live in the repo (or a nominated folder Otto
   provides); training images are Otto's own work only.
2. **Generation layer** — API-driven, swappable model backends:
   - Primary: **Flux (+ brand LoRA)** via fal.ai/Replicate/BFL API — cheap (~1–3¢/img), automatable.
   - **Recraft** — vector/SVG + reusable brand-style ID; first choice for Datalabs icons/diagram art.
   - **Adobe Firefly custom model** — commercially-safe lane (Adobe connector already available).
   - **Midjourney** — exploration/taste only, manual, never automated (no official API);
     winners feed the LoRA training set.
3. **Delivery layer — the pipeline script** (`skills/money-pages/scripts/images.py` or
   its own skill): manifest in → media IDs out.
   - **Manifest** (one row per image): brand · page/slot · subject prompt · size(s) ·
     SEO filename · alt text · caption (optional).
   - Steps: generate (N candidates per slot) → Otto approves via **contact-sheet
     multi-select Q&A** → post-process (crop to slot sizes: 300×300 entries, hero
     widths; WebP compress) → **upload via WP REST** to the right site with SEO
     filename + alt + caption → return media IDs for the page composer.
   - WP REST media upload is already credentialed on both sites (.env Application Passwords;
     browser-like UA required — WAF 403s generic UAs).

## 4. Integration points (existing repo assets)

- **Money-pages composer + template catalog**: image tokens (`{{ENTRY_IMAGE_ID}}`,
  `{{PICKn_IMAGE_ID}}`, `{{HERO_BG_URL}}/{{HERO_BG_ID}}`) get filled with pipeline
  media IDs — a commissioned page arrives with finished art.
- **Analytics/audit skill**: the alt-text and image-SEO audits define the backfill
  worklist (Datalabs 164 images; Yoast/meta passes).
- **Backlog flow**: image jobs attach to page commissions; no separate tracker.

## 5. Approval gates (non-negotiable)

- Otto approves a **contact sheet before any image is uploaded** to a site (multi-select
  Q&A, same mechanism as link-pass plans).
- Nothing self-publishes: images land in the media library; pages using them stay
  drafts per banned.md #4.
- The agent never trains on, or generates from, other artists' work as style input —
  Otto's portfolio only for style anchors/LoRAs.

## 6. Phases

- **Phase 0 — spike (no training):** one agency from page 16173; 3–4 candidate entry
  images per approach (Flux + style-reference images, Recraft style, Firefly); Otto
  judges the contact sheet. Decision: is prompt+reference enough, or train the LoRA?
  *Needs from Otto: a folder of his own work per brand for style references; which
  accounts/budget to use (fal.ai vs Replicate vs existing Adobe).*
- **Phase 1 — style anchors:** curate the per-brand reference sets + locked prompt
  prefixes; train brand LoRA(s) if Phase 0 says so; document in a style-bible file
  per brand.
- **Phase 2 — pipeline script:** manifest → generate → approve → post-process → WP
  upload → media IDs. Includes a dry-run mode and per-job cost print.
- **Phase 3 — composer integration:** guide/money-page composes emit an image manifest
  automatically; approved art flows into the kits' image tokens.
- **Phase 4 — estate backfill:** regenerate/replace weak legacy images and clear the
  alt-text backlog site-by-site, worklist from the audits, Otto approving per batch.

## 7. Costs (order of magnitude, Aug 2026)

LoRA training ~$2–6 per brand per iteration; Flux generations ~1–3¢ each (a 17-image
page with 3 candidates per slot ≈ $1–2); Recraft/Firefly per-image slightly higher.
Local ComfyUI (M-series or rented GPU) = zero marginal cost — revisit only if API spend
becomes material.

## 8. Open questions for Phase 0 kickoff

1. Style reference folders per brand (where do they live — iCloud? repo?).
2. Which paid accounts exist / which to open (fal.ai, Replicate, Recraft; Adobe already connected).
3. Hero-image dimensions worth standardising per template (kit README to record).
4. Does Datalabs want photographic-real imagery anywhere, or all-illustration? (Affects model choice.)

## 9. Companion project (separate, future): video/animation at scale

Otto will open this as its own project; noted here so the image project is built
compatible with it — same style anchors, same brand isolation, same approval gates.
Rough scope to expand later into its own spec:
- **Generation:** image-to-video and text-to-video (Veo, Kling, Runway, Luma; Flux
  stills as first frames — the image pipeline's outputs become video inputs, which is
  why the style layer is shared). Oddtoe's artist-led hybrid workflow (rigging + motion
  design over generated imagery) stays the creative model.
- **Editing automation:** programmatic assembly and cutting — ffmpeg pipelines,
  Remotion (React-defined video, fully code-drivable), Premiere scripting, and the
  Adobe connector's Quick Cut for sizzle/highlight cuts; auto-captioning; batch
  exports per platform (the Adobe social-variations skill already covers resizing).
- **Products:** Oddtoe TV shorts, case-study videos, activation loop content, Datalabs
  explainer/workshop promos; storyboards already covered by the oddtoe-video-storyboard
  skill — the pipeline turns approved storyboards into cut drafts.

---
*Related: `docs/GEO_CONTENT_AGENT_SPEC.md`, `skills/money-pages/references/template-catalog.md`,
`skills/money-pages/references/guide-kits-README.md`.*
