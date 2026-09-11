# Shot list: Use Case, Festival & Precinct Activations

Content JSON: `money-pages/references/usecase-content-festival-activation.json`. Every image slot on the page renders a placeholder today. This table says what should be there instead. Media ids are WordPress attachment ids under `https://www.oddtoe.com/wp-content/uploads/`.

The worked example on the page is a walk-in inflatable entrance for a city festival, so most intended shots are of that one object: drawn, built, installed, photographed by the crowd, and packed for next year.

Formats: square crop for the six circles; 640x480 for the three drawings; wide 16:9 for the hero, the six timeline panels and the video.

| Slot | Intended image | Format | Placeholder used (id) | Note |
|---|---|---|---|---|
| HERO | The walk-in inflatable entrance at the top of a festival queue, late afternoon, people walking through the doorway, stage in the background | Wide 16:9 | 16197 blue horned inflatable monster with a walk-in doorway at a festival | Placeholder is the right subject in the wrong colours; it can hold the slot. No festival named in alt text. |
| DRAW1 (Ideation) | First pencil sketch of the entrance drawn on the site plan, the queue drawn as arrows, a figure for scale | 640x480 | 16194 3D render showing panel seams of two inflatable forms | Placeholder is a render, not a sketch. Swap when a real ideation drawing exists. |
| DRAW2 (Panel Drawings) | The entrance form modelled in 3D and cut into its panel pattern, seams numbered | 640x480 | 16202 3D render of an inflatable dome's panel pattern | Right kind of drawing; subject is a dome, not the entrance. Can stay until the real pattern exists. |
| DRAW3 (Site & Crowd) | A plan and section of the entrance on site: doorway width against the queue, blower position, power run, anchor points | 640x480 | 16254 walk-through archway woven from eucalypt branches | Placeholder is a built archway, not a drawing. Swap first when a site drawing exists. |
| VIDEO | A looping clip: the crowd walking through the entrance by day, cutting to the same character projected on the venue after dark | Wide 16:9, mp4 H.264 1280x720 under 2 MB, muted loop, plus poster | Balloon ideation loop `2026/09/oddtoe-balloon-ideation-loop-v2.mp4` with poster `2026/09/oddtoe-balloon-ideation-poster.jpg` | Wrong subject. `VIDEO_ARIA` describes the balloon clip honestly and must be rewritten when the clip is replaced. |
| CIRCLE1 (The Entrance) | The walk-in entrance from the queue, people mid-step through the doorway | Square | 16197 blue horned inflatable monster with a walk-in doorway at a festival | Same image as the hero; a different crop of the same shoot would do. |
| CIRCLE2 (The Photo Spot) | One large object in the middle of a festival site with a short queue of people waiting to stand in front of it | Square | 16198 giant orange inflatable octopus on a street festival | Right subject; can stay if the crop works. |
| CIRCLE3 (The Venue After Dark) | Projection on a venue facade or inside a hall during an evening session, crowd with phones up | Square | 16195 large illuminated inflatable sphere glowing in a dark hall | Placeholder is a lit object, not projection. 16145 (baobab under projection) is the closer stand-in if a square crop works. |
| CIRCLE4 (The Parade Piece) | A carried or pulled piece in a street parade, volunteers under it, crowd either side | Square | 16256 oversized caricature heads carried at street level | Right kind of picture; can stay. |
| CIRCLE5 (The Seasonal Takeover) | A Christmas or summer installation in a laneway or on a rooftop bar, diners or shoppers around it | Square | 16192 giant inflatable acorn character | Placeholder is a character on its own, no precinct around it. Swap first. |
| CIRCLE6 (The Festival Mascot) | The festival mascot in costume on site, with the same character visible on a poster or banner behind it | Square | 16267 shaggy costume mascot on a workbench | Placeholder shows a costume in the workshop, not on site. |
| STEP1 (The Brief) | A festival site on load-in day before anything is up: fencing, an empty stage, trucks | Wide 16:9 | 16290 notes on the page before anything is drawn | Placeholder is square; the rail letterboxes it. |
| STEP2 (Design) | The entrance drawn at scale on the festival site plan, then the same form as a 3D panel pattern | Wide 16:9 | 16202 3D render of an inflatable dome's panel pattern | Same image as DRAW2; replace both when the entrance drawings exist. |
| STEP3 (Fabrication) | The entrance being sewn on a specialist maker's floor, panels laid out | Wide 16:9 | 16333 maker stitching fabric panels onto a head form | Placeholder is a maker at work, so the caption is true of both. Subject is a head, not an inflatable. |
| STEP4 (Install day) | Install day outdoors: the entrance half inflated, site crew on the anchor points, blower and power lead visible | Wide 16:9 | 16201 white inflatable walk-in dome on a timber floor indoors | Placeholder is an inflatable installed indoors; caption written to be true of it. |
| STEP5 (The Run) | Two frames if possible: the queue in front of the entrance by day, and the same character projected on the venue after dark | Wide 16:9 | 16145 baobab sculpture lit deep red by projection | Real Oddtoe projection work; caption describes it honestly. |
| STEP6 (The Return) | The deflated entrance packed into its case in a storage shed, label on the lid, next to the blower | Wide 16:9 | 16253 black flight case | Placeholder is a cut-out object on a plain ground, also used as DIV_IMG2. Swap first. |
| DIV_IMG1 | A small floating object for the divider. Current: cardboard shipping box with a character on the side | Transparent PNG | 16125 Experiential-Marketing-SampleBox.png | Kept from the exemplar. A blower unit, cut out, would suit "Designed to be Installed". |
| DIV_IMG2 | A small floating object for the divider. Current: black flight case | Transparent PNG | 16253 oddtoe-flight-case-activation-build-v2.png | Kept from the exemplar. A sandbag anchor or a folded inflatable in its bag, cut out, would suit "Built to Come Down Again". |
| PORTFOLIO1 | A built sculpture with live projection at a festival | Module pulls its own image | 16154 Babbling with Baobabs | Real portfolio item, stays. |
| PORTFOLIO2 | Outdoor installed work for a precinct | Module pulls its own image | 14808 Topiary Design | Real portfolio item, stays. |
| PORTFOLIO3 | Built sculpture | Module pulls its own image | 14669 3D Sculpture | Real portfolio item, stays. |

Alt text and captions in the JSON describe the placeholders honestly. When a real image goes in, rewrite the caption for that slot and check the alt text names no client, no venue, and no festival.
