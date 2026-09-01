"""Curated YouTube rows. Every channel below passed the hard filters
(5k-1M subs, uploaded within 60 days, on-territory) and was then read by hand.

The structural finding recorded in the notes: YouTube in this field is mostly
PRACTITIONERS, not press. Channels that would actually feature an outside
artist are rare, so relevance 3 is reserved for them and peers are marked as
what they are rather than dressed up as coverage targets.
"""
import json

# title -> (person, role, hook, relevance, why_fit)
J = {
"STIR": ("", "STIRworld — global media house and curatorial agency",
 "public-art-oddity", "3",
 "THE STRONGEST PRESS TARGET IN THE POOL. STIR describes itself as a global media house and curatorial agency covering architecture, design and new-media arts, and STIRworld.com is its content arm. Its recent video is literally about a public artwork becoming a community playground. This is an outlet that commissions writing about exactly Oddtoe's territory, not a maker channel."),
"MoltenArt": ("", "Art documentary channel", "melbourne-local", "3",
 "AUSTRALIAN and on-territory. Covers installation and public art as documentary - recent video on Yayoi Kusama's legacy - and surfaced repeatedly across separate searches for land art, kinetic sculpture and playful public art. An Australian channel that profiles installation artists is a rare and useful thing."),
"Skill Spectrum": ("", "Documentary channel profiling makers", "public-art-oddity", "3",
 "Explicitly a channel about 'skillful and talented people... art-work, skills and wonderful people'. Its whole format is profiling a maker, which is the shape of a feature on Oddtoe. Publishes a contact address."),
"The Magnificent World of Toys and Creative Arts": ("", "Toy and creative-arts documentary channel",
 "public-art-oddity", "3",
 "Describes itself as documenting and archiving toy collectors and the creative arts, and runs long interview episodes with makers and collectors. Directly relevant to the art-toy and character-design strand."),
"W1 Curates": ("", "Public art platform, Oxford Street London", "public-art-oddity", "3",
 "NOT PRESS - A COMMISSIONER, recorded here because it surfaced in the press sweep. W1 Curates is a public art platform on London's Oxford Street showing art, fashion and music work on its facade. Treat this as an opportunity to submit to, and consider moving it to the Festivals stream."),
"Gardening With Alan Titchmarsh": ("Alan Titchmarsh", "Broadcaster and gardener", "public-art-oddity", "2",
 "The best-known gardening broadcaster in the UK, sixty years in the field, active daily. Relevant to the topiary and sensory-garden strand rather than the studio - a long shot for coverage, but the garden work is genuinely unusual enough to interest a mainstream gardening audience."),
"Lucinda Dilworth": ("Lucinda Dilworth", "Digital artist — projection mapping, immersive spaces",
 "hybrid-craftsman", "2",
 "Small but exactly on-territory: a working projection-mapping and immersive-visuals artist documenting process. Peer rather than press, and the most likely of these to swap notes on technique."),
"Curious Refuge": ("", "AI storytelling channel and course", "hybrid-craftsman", "2",
 "Calls itself the first online home for AI storytellers, 273k subscribers. The natural audience for the hybrid-craftsman argument - a working animator with twenty years of traditional craft using generative tools in production. Note it sells courses, so any approach should be editorial, not promotional."),
"Dan Kieft": ("Dan Kieft", "AI tools commentator, Netherlands", "hybrid-craftsman", "2",
 "288k subscribers covering AI production tools, with a published business address. Reaches the audience arguing about AI in animation; the pitch is the practitioner's counterweight to the hype."),
"Pierrick Picaut": ("Pierrick Picaut", "Blender Foundation certified trainer; former art director and rigger",
 "hybrid-craftsman", "2",
 "187k subscribers, France. A serious animation-craft channel run by a former art director and rigger - the rigging half of Oddtoe's hybrid pipeline is exactly his subject."),
"VanOaksProps": ("Derek", "Prop maker", "public-art-oddity", "2",
 "114k subscribers of prop building and fabrication. Peer with a real audience; relevant to the prop design and fabrication strand rather than to coverage of public art."),
"Brick In The Yard Molding & Casting": ("", "Moulding and casting production", "public-art-oddity", "2",
 "345k subscribers on moulding, casting, foam carving and sprayed resin hard-coating - the actual techniques behind fabricated public sculpture. Peer and technique source."),
"Dave Fogler at the Cinodrome": ("Dave Fogler", "Former Industrial Light & Magic visual effects artist",
 "hybrid-craftsman", "2",
 "Design-build-film from a former ILM VFX artist. Small (17k) but a credible practitioner whose format - building things and filming the process - matches how Oddtoe's work is best shown."),
"Creative Geekery": ("Matt", "Maker and prop builder", "public-art-oddity", "2",
 "Prop building and practical effects including projection tricks. Moderate fit; a maker audience rather than an art audience."),
"Swazzle Productions": ("", "Custom puppet builders", "public-art-oddity", "2",
 "A professional puppet-building company that has built for notable television projects, posting workshop process. Speaks to Otto's puppetry background; a peer and possible collaborator rather than press."),
"svv art": ("Sarah", "Illustrator and sculptor", "public-art-oddity", "2",
 "156k subscribers, UK, an illustrator and sculptor documenting sculpture builds with a published business address. Peer with genuine reach in the art-toy and sculpture space."),
"So-Hee Woo": ("So-Hee Woo", "Artist and toymaker, brand GoodBadorElse", "public-art-oddity", "2",
 "Small channel from a working artist and toymaker making art toys and props. Close peer for the art-toy strand."),
"Ten Hundred": ("Peter Robinson", "Artist and muralist", "public-art-oddity", "2",
 "868k subscribers. A muralist who runs collaborative art challenges featuring other artists - one of the few large channels here with a format that actually brings in an outside artist."),
"Interactive solution Expert": ("", "KLEADER — high-tech art installation supplier, Hong Kong",
 "public-art-oddity", "1",
 "NOT PRESS - A SUPPLIER. Makes interactive and holographic installation hardware. Recorded because it is a live lead for the sourcing or agencies stream rather than for coverage."),
"Digital Inflatable Inflable Sam Yu": ("Sam Yu", "Inflatable manufacturer, China", "public-art-oddity", "1",
 "NOT PRESS - A SOURCING LEAD. A Chinese inflatable manufacturer of 26 years posting custom advertising inflatables. Oddtoe makes building-sized inflatables and the sourcing skill already covers Guangzhou; this belongs in that register, not in media."),
"Akasha Mead": ("Akasha Mead", "Australian artist", "melbourne-local", "1",
 "Australian artist with a small channel and a published contact address. Long shot for coverage; recorded as a local peer."),
"JollyJunk": ("", "Stop-motion channel", "hybrid-craftsman", "1",
 "Stop-motion enthusiast channel that also covers industry news about who is commissioning animation. Small, but the animation-industry angle is adjacent."),
"BlakeMakes": ("Blake", "Art toy maker", "public-art-oddity", "1",
 "Art-toy and resin-printing channel with a published partnership address. Long shot - the format is product-led rather than artist-led."),
"‘til i make it": ("", "Maker channel", "public-art-oddity", "1",
 "General maker channel with a published business address. Long shot, recorded for completeness in the art-toy segment."),
"Mythical Makers Workshop": ("", "Fantasy craft and cosplay props", "public-art-oddity", "1",
 "Husband-and-wife craft-build channel. Adjacent to prop fabrication; long shot for coverage."),
"Jon Laymon Studios": ("Jon Laymon", "Creature and prop studio", "public-art-oddity", "1",
 "Prop and creature build studio with a published business address. Peer, long shot."),
}

chans = {c["title"]: c for c in json.load(open("scored.json"))}
rows, missing = [], []
for title, (person, role, hook, rel, why) in J.items():
    c = chans.get(title)
    if not c:
        missing.append(title); continue
    handle = c.get("handle") or ""
    url = f"https://www.youtube.com/{handle}" if handle.startswith("@") else f"https://www.youtube.com/channel/{c['channel_id']}"
    email = c["emails_in_description"][0] if c["emails_in_description"] else ""
    rows.append({
        "outlet": title[:200], "sourceId": "youtube-api-2026-09-01", "segment": "youtube",
        "person": person, "role": role, "url": url, "email": email,
        "contactPage": url + "/about", "linkedin": "",
        "hook": hook, "whyFit": why,
        "evidenceUrl": f"https://www.youtube.com/watch?v={[v['video_id'] for v in json.load(open('search.json'))['videos'] if v['channel_id']==c['channel_id'] and v['video_id']][0]}" if any(v['channel_id']==c['channel_id'] and v['video_id'] for v in json.load(open('search.json'))['videos']) else url,
        "relevance": rel,
        "notes": (f"Sourced 1 Sep 2026 via the YouTube Data API. {c['subscribers']:,} subscribers; "
                  f"last upload {c['days_since_upload']} days ago"
                  f"{'; country ' + c['country'] if c['country'] else ''}. "
                  f"Passed the runbook filters (subscriber band + active in 60 days). "
                  f"{'Email read from the channel description — a published business address, not a guess.' if email else 'No email in the channel description; YouTube hides the About-tab address behind a captcha, so the contact needs the channel’s linked website.'}"),
    })
if missing:
    raise SystemExit(f"not found in scored pool: {missing}")
json.dump({"brand":"oddtoe","rows":rows}, open("import-youtube.json","w"), indent=2)
from collections import Counter
print(f"{len(rows)} YouTube rows built")
print("relevance:", dict(Counter(r['relevance'] for r in rows)))
print("with email:", sum(1 for r in rows if r['email']), "/", len(rows))
