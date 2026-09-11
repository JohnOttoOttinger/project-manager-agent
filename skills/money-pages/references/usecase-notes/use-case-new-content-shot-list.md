# Shot list: Use Case, New Content & Original Series

Content JSON: `money-pages/references/usecase-content-new-content-original-series.json`. Every image slot on the page renders a placeholder today. This table says what should be there instead. Media ids are WordPress attachment ids under `https://www.oddtoe.com/wp-content/uploads/`.

Formats: square crop for the six circles; 640x480 for the three drawings; wide 16:9 for the hero, the six timeline panels and the video.

This is the one use case where the object is a story. Most intended images are frames, drawings and pages from The Oddtoe TV Show and Wire Taps, which already exist in the studio, so this list should be quicker to fill than the others.

| Slot | Intended image | Format | Placeholder used (id) | Note |
|---|---|---|---|---|
| HERO | A wide frame from The Oddtoe TV Show pilot: the newsdesk, anchors mid-bulletin, a meaningless chart on the screen behind them | Wide 16:9 | 16145 baobab sculpture lit deep red by projection | Real Oddtoe work, but the wrong medium for this page. Swap first. |
| DRAW1 (Ideation) | A notebook page of premise notes and a first thumbnail of the cast, pen on paper | 640x480 | 16317 a gag cartoon by Oddtoe | Placeholder is a finished gag by Oddtoe; it suits "where the joke starts" and can stay until a notebook page is shot. |
| DRAW2 (The Bible) | A spread from The Oddtoe TV Show bible: character line-up with names and one line each | 640x480 | 16161 diagram of the Baobab Translator | Placeholder is a diagram of one character's voice becoming pictures; the caption is written to be true of it. |
| DRAW3 (Script & Animatic) | A frame from an animatic with the script line and timecode visible under rough drawings | 640x480 | 16163 the voice bubble turning red, motion design frame | Placeholder is a real Oddtoe motion-design frame; close enough to hold the slot. |
| VIDEO | A looping clip from the Wire Taps pilot animation or The Oddtoe TV Show, ten to twenty seconds, muted | Wide 16:9, mp4 H.264 1280x720 under 2 MB, muted loop, plus poster | Balloon ideation loop `2026/09/oddtoe-balloon-ideation-loop-v2.mp4` with poster `2026/09/oddtoe-balloon-ideation-poster.jpg` | Wrong subject. `VIDEO_ARIA` and the first paragraph of `PANEL_INTRO` describe the balloon clip honestly and must both be rewritten when the clip is replaced. |
| CIRCLE1 (The Series With An Author Attached) | The Oddtoe TV Show title card or the anchors at the desk | Square | 16158 Babbling with Baobabs poster | Placeholder is a real Oddtoe show poster, so it reads as "a show". Swap for the series it names. |
| CIRCLE2 (The Pilot You Can Afford To Lose) | A single frame from a generative-AI test short, rough, with the render still visibly a test | Square | 16265 the shark mascots as a 3D wireframe mesh | Placeholder is a wireframe, which reads as "unfinished on purpose". |
| CIRCLE3 (The Scene Nobody Filmed) | A documentary-style animated frame: a map with a route drawn on, a dated clipping, a timeline | Square | 16152 voice-modulated bubble projected into the baobab's trunk | Placeholder is real Oddtoe projection work, not a documentary frame. Swap when a documentary frame is cleared to show. |
| CIRCLE4 (A Panel A Week) | One weekly gag panel, square, as published | Square | 16317 a gag cartoon by Oddtoe | Placeholder is the real thing. Stays. Same image as DRAW1, so swap DRAW1 first. |
| CIRCLE5 (The Character You Own) | A character sheet: one character in three poses and a turnaround | Square | 16218 animated dog character with a doghouse (Oddtoe animation for NatGeo Kids) | Placeholder is real Oddtoe character work. Can stay if the gif crops square. |
| CIRCLE6 (The Stunt, Shot As An Episode) | A still from a build or a street day framed as an episode thumbnail, with a title strap | Square | 16299 monument-scale head with a banner in a street (concept) | Placeholder is the publicity stunt page's concept image, which is what the circle describes. Stays. |
| STEP1 (The Premise) | Notes on a page: the premise in one line, crossed out and rewritten | Wide 16:9 | 16290 notes on the page before anything is drawn | Placeholder is the right kind of image and is square; the rail letterboxes it. |
| STEP2 (Characters & Bible) | Character sheets pinned above the desk with the bible open beneath them | Wide 16:9 | 16246 panel pattern drawings pinned above a workbench with a maquette | Placeholder shows drawings pinned above a bench; the caption is written to be true of it. |
| STEP3 (Script & Animatic) | An animatic frame with the script visible, or the timeline of the edit with rough drawings in it | Wide 16:9 | 16163 the voice bubble turning red, motion design frame | Same image as DRAW3. Real Oddtoe motion design; can hold the slot. |
| STEP4 (The Pilot) | The pilot playing on the studio monitor with the character drawings beside it | Wide 16:9 | 16153 projection operated live from a laptop | Placeholder is a laptop running projection, not animation. Caption says projection, which is true. |
| STEP5 (The Pitch) | A pitch room: the pilot on the screen at the end of a table, or a channel page with the pilot as the top video | Wide 16:9 | 16142 internally lit baobab on stage | Placeholder is a real Oddtoe show on a stage; caption written to be true of it. |
| STEP6 (What You Keep) | The bible, the character sheets and a drive with the pilot on it, laid out on a table | Wide 16:9 | 16332 a stained-glass window by Oddtoe installed in a building | Placeholder is unrelated Oddtoe work; the caption ("Made once. Still there years later") is true of it and of the idea. Swap when a flat-lay is shot. |
| DIV_IMG1 | A small floating object for the divider. Current: cardboard shipping box with a character on the side | Transparent PNG | 16125 Experiential-Marketing-SampleBox.png | Kept from the exemplar. A bound series bible, cut out, would suit "Written to be Watched". |
| DIV_IMG2 | A small floating object for the divider. Current: black flight case | Transparent PNG | 16253 oddtoe-flight-case-activation-build-v2.png | Kept from the exemplar. A character maquette, cut out, would suit "Drawn to be Owned". |
| PORTFOLIO1 | The Oddtoe TV Show | Module pulls its own image | 12489 The Oddtoe TV Show | Real portfolio item, stays. |
| PORTFOLIO2 | Wire Taps | Module pulls its own image | 12586 Wire Taps | Real portfolio item, stays. |
| PORTFOLIO3 | The weekly gag cartoon | Module pulls its own image | 15269 Gag Cartoonist | Real portfolio item, stays. |

Alt text and captions in the JSON describe the placeholders honestly. When a real image goes in, rewrite the caption for that slot and check the alt text names no client and no event.
