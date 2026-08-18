# Person/Organization schema for Oddtoe — APPLIED to the two bio pages 18 Aug 2026

Applied by `skills/money-pages/scripts/faq-bio-pages.py` alongside the GEO
Q&A rows; JSON-LD verified parsing on both live pages. Two notes from apply
time: (1) datalabsagency.com's Yoast already emitted a Person node with
`@id: #otto` — our block reuses that @id so the graph merges rather than
duplicating; (2) the oddtoe.com **homepage** placement is still pending —
only the two bio pages were in the approved scope.

Prepared 18 Aug 2026. Nothing below is applied to the site yet — WordPress
edits are plan-first. Verified state: the homepage carries only Yoast defaults
(`Organization`, `WebSite`, `WebPage`); nothing anywhere declares Oddtoe an
artist to machines.

## The shape — two Person entities, one per brand (decided 18 Aug 2026)

Otto's call: **"Otto Ottinger" belongs to the Datalabs side.** Two Person
nodes, each anchored to its own about page. **Update 18 Aug 2026: Otto is
happy for the two to be linked in the schemas** — so each node's `sameAs`
carries the other's anchor page, and the shared LinkedIn appears on both:

| Entity | `name` | Anchor page | Brand |
|---|---|---|---|
| Person 1 | Oddtoe | https://www.oddtoe.com/about-oddtoe/ | Oddtoe |
| Person 2 | Otto Ottinger | https://www.datalabsagency.com/otto-ottinger/ | Datalabs |

This matches the entity-separation strategy: the personas stay distinct for
machines even though a human reading `/about-oddtoe/` can see the pseudonym
history. Consequences to accept knowingly:

- Names stay per-brand: `name: "Oddtoe"` on oddtoe.com, `name: "Otto
  Ottinger"` on datalabsagency.com. No legal name on the Oddtoe node.
- Machine linking is via `sameAs` cross-references (each node lists the
  other's anchor URL) plus the shared LinkedIn profile on both nodes —
  machines can reconcile the two identities; page copy still keeps each
  brand's register (the naming rule is about visible text, not markup).

## The JSON-LD block

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Person",
      "@id": "https://www.oddtoe.com/#/schema/person/oddtoe",
      "name": "Oddtoe",
      "mainEntityOfPage": "https://www.oddtoe.com/about-oddtoe/",
      "url": "https://www.oddtoe.com/about-oddtoe/",
      "jobTitle": "Artist and animator",
      "description": "Melbourne artist and animator working across generative AI animation, experiential design and public art.",
      "hasOccupation": [
        { "@type": "Occupation", "name": "Animator" },
        { "@type": "Occupation", "name": "Visual artist" }
      ],
      "workLocation": { "@type": "Place", "name": "Melbourne, Australia" },
      "knowsAbout": [
        "generative AI animation",
        "documentary and factual animation",
        "character design",
        "prop design and fabrication",
        "kinetic and public sculpture",
        "installation art",
        "projection art",
        "topiary and sensory garden design",
        "robotics design",
        "political cartooning",
        "puppetry",
        "comedy writing"
      ],
      "sameAs": [
        "https://www.instagram.com/oddtoe_artist/",
        "https://www.youtube.com/@OddtoeAndDatalabs",
        "https://twitter.com/Oddtoe",
        "https://www.facebook.com/OddtoeArtist/",
        "https://www.linkedin.com/in/ottinger/",
        "https://www.datalabsagency.com/otto-ottinger/"
      ],
      "subjectOf": [
        "https://www.oddtoe.com/animation-conferences/",
        "https://www.oddtoe.com/animation-agents/"
      ],
      "worksFor": { "@id": "https://www.oddtoe.com/#organization" }
    },
    {
      "@type": "Organization",
      "@id": "https://www.oddtoe.com/#organization",
      "name": "Oddtoe",
      "url": "https://www.oddtoe.com/",
      "founder": { "@id": "https://www.oddtoe.com/#/schema/person/oddtoe" }
    }
  ]
}
</script>
```

### Person 2 — Otto Ottinger, for datalabsagency.com

Facts below verified against the live `/otto-ottinger/` page, 18 Aug 2026:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Person",
      "@id": "https://www.datalabsagency.com/#/schema/person/otto-ottinger",
      "name": "Otto Ottinger",
      "alternateName": "John \"Otto\" Ottinger",
      "url": "https://www.datalabsagency.com/otto-ottinger/",
      "mainEntityOfPage": "https://www.datalabsagency.com/otto-ottinger/",
      "jobTitle": "Founder & Managing Director, Datalabs Agency",
      "description": "Data visualizer specializing in the visual design of complex data systems, working at the intersection of UX design, visual analytics and storytelling. Started his career as an editor and interactive designer at National Geographic in Washington, DC.",
      "hasOccupation": [
        { "@type": "Occupation", "name": "Data visualization designer" },
        { "@type": "Occupation", "name": "Keynote speaker and trainer" }
      ],
      "workLocation": { "@type": "Place", "name": "Melbourne, Australia" },
      "knowsAbout": [
        "data visualization",
        "dashboard design",
        "information design",
        "visual analytics",
        "UX design",
        "data storytelling"
      ],
      "sameAs": [
        "https://www.linkedin.com/in/ottinger/",
        "https://www.oddtoe.com/about-oddtoe/"
      ],
      "worksFor": { "@id": "https://www.datalabsagency.com/#organization" }
    },
    {
      "@type": "Organization",
      "@id": "https://www.datalabsagency.com/#organization",
      "name": "Datalabs Agency",
      "url": "https://www.datalabsagency.com/",
      "sameAs": [
        "https://www.linkedin.com/company/datalabs-agency",
        "https://twitter.com/DatalabsAgency",
        "https://www.facebook.com/datalabsagency/",
        "https://www.instagram.com/datalabsagency/",
        "https://www.pinterest.com.au/datalabs/",
        "https://www.youtube.com/channel/UCiF-JlTyywll7YkB630PrdA"
      ],
      "founder": { "@id": "https://www.datalabsagency.com/#/schema/person/otto-ottinger" }
    }
  ]
}
</script>
```

Filled 18 Aug 2026: personal LinkedIn (https://www.linkedin.com/in/ottinger/,
supplied by Otto) on the Person; the six company profiles (read from the
datalabsagency.com header) on the Organization.

**Shared LinkedIn (resolved 18 Aug 2026):** Otto approved machine-linking
the two personas, so https://www.linkedin.com/in/ottinger/ sits in both
Person nodes' `sameAs`, alongside cross-references to each other's anchor
pages. Follow-up task Otto has queued: surfacing Oddtoe better ON that
profile (featured section, experience entry).

**Site bug spotted while reading the header:** datalabsagency.com links to
`linkedin.com/company/2709205/admin/` — the admin URL, broken for visitors.
Swap to https://www.linkedin.com/company/datalabs-agency in the theme's
social row.

Notes on the Oddtoe draft:

- The Oddtoe `Organization` node re-declares Yoast's `@id` (`#organization`)
  so `founder` attaches to the existing graph node. **Verify Yoast's actual
  `@id` in each site's homepage source before applying** — match what's there.
- `sameAs` carries identity profiles only (the four verified Oddtoe socials);
  the two ranking guides sit in `subjectOf`. Confirm the guide URLs — the
  conferences page moved to `/animation-conferences/` on 18 Aug.
- No legal name anywhere on the Oddtoe node, per the two-entity decision.

## Where it goes, in order

1. **Oddtoe Person → `/about-oddtoe/`** (page-level `[vc_raw_html]` block,
   same base64 pattern as the FAQ rollout scripts) — the bio page is the
   anchor the `@id` and `mainEntityOfPage` point at.
2. **Oddtoe Person → oddtoe.com homepage** — same block, highest-authority URL.
3. **Otto Ottinger Person → `/otto-ottinger/` on datalabsagency.com** — same
   delivery pattern; both sites' REST creds are already verified.
4. Once the approved bio text lands on `/about-oddtoe/`, the visible copy and
   the markup agree — LLM-citable, extending the llms.txt advantage to
   "who is Oddtoe".

## What I need from Otto

- ~~Two-entity design~~ — confirmed 18 Aug 2026.
- ~~Datalabs `sameAs` URLs~~ — supplied 18 Aug 2026 (personal LinkedIn +
  header profiles).
- **Remaining: approve the two blocks and the three placements** (Oddtoe →
  /about-oddtoe/ + homepage; Otto Ottinger → /otto-ottinger/); they then go
  in via the vc_raw_html pattern and get verified with Google's Rich Results
  test.
