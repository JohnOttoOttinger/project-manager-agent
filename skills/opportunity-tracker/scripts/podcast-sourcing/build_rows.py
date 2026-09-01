"""Stage 4: turn the shortlist into import rows.

Two honesty rules enforced in code, both learned from the enrichment run:
  * a platform relay or no-reply address is NOT a contact - it is dropped to
    empty and the reason recorded, exactly as a catch-all domain would be.
  * `person` is only filled where the feed names a human. Organisation-authored
    feeds keep person empty rather than inventing a host.
"""
import json, re

RELAY = re.compile(r"@(anchor\.fm|.*\.acast\.com|.*\.libsyn\.com|"
                   r".*\.buzzsprout\.com|.*\.spreaker\.com)$", re.I)
NOREPLY = re.compile(r"^(no-?reply|donotreply|podcasts?\d)", re.I)
GENERIC = re.compile(r"^(info|hello|contact|admin|podcast|support|programming|"
                     r"abcpodcasts)[@+]", re.I)

# hand-written judgement: (feed show name, person-or-blank, role, hook,
#                          relevance, why_fit, evidence episode url)
PICKS = [
("The Installation Art Podcast","Anastasia Parmson","Host; installation artist","public-art-oddity","3",
 "The single closest fit in the whole pool: a podcast entirely about installation art, hosted by a practising installation artist, running long interviews with artists about making and siting public work. Recent episodes cover public art commissioning and what a public art curator actually does.",
 "https://orchid-bat-732353.hostingersite.com/blog/michael-johansson-047"),
("Creating New Spaces: Interviews with artists redefining spaces through technology","Robin Petterd","Host; media artist","melbourne-local","3",
 "Australian, and squarely on Oddtoe's territory - media art in public space. Has run episodes on public art permanence and decay, and on Craig Walsh using projection to turn trees into temporary public monuments, which is the closest published parallel to Oddtoe's projection and garden work.",
 "https://podcasters.spotify.com/pod/show/creatingnewspaces/episodes/How-Craig-Walsh-uses-projection"),
("Sculpture Vulture","Lucy Branch","Host; sculptural conservator and author","public-art-oddity","3",
 "Interviews sculptors whose work stands in public space, on practice and career rather than art theory. Recent episodes include the public sculpture of Canary Wharf and a sculptor working the 1% public art scheme in New Zealand.",
 "https://podcasters.spotify.com/pod/show/sculpturevulture733/episodes/The-Public-Sculpture-of-Canary-Wharf"),
("The Experience Designers","Steve Usher","Host","public-art-oddity","3",
 "Experience and immersive design, interviewing the people who build large public experiences - Secret Cinema's creative director, and an architect who worked on the Sphere. Directly adjacent to the experiential half of Oddtoe's practice.",
 "https://www.theexperiencedesigners.com/episodes/paul-nicholls-from-architecture-to-the-sphere"),
("Experience Imagination: A Themed Entertainment Podcast","","Falcon's Creative Group studio podcast","public-art-oddity","3",
 "Themed entertainment and location-based experience. Episode 091 is specifically about one independent artist delivering large location-based impact on a shoestring budget, which is the exact shape of a one-person studio pitching against big builds.",
 "https://falconscreativegroup.libsyn.com/091-shoestring-budget-big-lbe-impact"),
("Voices of VR","Kent Bye","Host","public-art-oddity","3",
 "Nearly 1,800 episodes of oral history with immersive artists and experiential designers, including curatorial overviews of Venice Immersive. Deep, serious, and a standing venue for artists explaining a practice.",
 "http://voicesofvr.com/1787-blending-the-elements-of-experiential-design"),
("Matters of Experience","","Lorem Ipsum Corp studio podcast","public-art-oddity","3",
 "Experience design for museums and expos - pavilions, immersive futures, and making museums smaller and more accessible. The commissioner-side conversation Oddtoe wants to be visible in.",
 "https://rss.com/podcasts/matters-of-experience/2821041"),
("The Visual Cast","Alon Hammer","Host","hybrid-craftsman","3",
 "Interviews visual artists working in projection, immersive and generative visuals, each guest presenting a set or a workflow deep-dive. Format suits showing a hybrid AI-plus-craft pipeline rather than just describing it.",
 "https://podcasters.spotify.com/pod/show/thevisualcast/episodes/VC--EP83-The-Void-Andrew-Hunter"),
("The Bancroft Brothers Animation Podcast","","Hosted by Tom and Tony Bancroft","hybrid-craftsman","3",
 "Three hundred episodes of working animators interviewing working animators about the craft and the business, explicitly including the future of animation. The natural venue for the hybrid-craftsman argument - twenty years of traditional craft plus generative AI in production.",
 "https://bancroftbros.libsyn.com/our-300th-episode-looking-back-and-looking-forward"),
("ACCA Podcast","","Australian Centre for Contemporary Art","melbourne-local","2",
 "Melbourne's flagship contemporary art space. Institution-run channel of panels and artist/curator walkthroughs rather than a guest booking slot, so treat as a relationship and exhibition target, not a pitch for an interview.",
 "https://soundcloud.com/acca_melbourne/artist-and-curator-walkthrough"),
("Toon-In Talk","Whitney Grace","Host; writer and pop culture historian","hybrid-craftsman","2",
 "Weekly animation interviews, and the host specialises in animation, comics and puppetry - three of Oddtoe's own strands. Recent guests include Kathy Mullen and Michael Frith of Muppet fame.",
 "https://podcasters.spotify.com/pod/show/toonintalk/episodes/Episode-60"),
("Fantasy/Animation","","Academic animation podcast","hybrid-craftsman","2",
 "Scholarly animation podcast that has covered immersive experience and the Sphere in Las Vegas. Adjacent rather than exact - the register is academic, so the pitch would be the argument about AI and craft, not the studio.",
 "https://fananimresearch.podbean.com/e/immersive-experiences-and-the-sphere-las-vegas"),
("Le MoDCast","","Apéros Motion Design collective","hybrid-craftsman","2",
 "French-language motion design podcast that has run a special on AI and intellectual property and an episode on an art toy designer. On-topic twice over, but conducted in French - only worth pitching if Otto is comfortable with that.",
 "https://shows.acast.com/modcast/episodes/hors-serie-intelligence-artificielle-ia-propriete-intellectuelle"),
("Outsiding","","Hosted by Adam Frost and Caitlin Moran","public-art-oddity","2",
 "Gardens as joy rather than horticulture, hosted by a garden designer and a comedy writer, booking comedians like Ed Byrne and Phil Wang. The tone is the closest match in the pool to Oddtoe's own - playful, funny, public. Books celebrities rather than designers, so the angle would be the oddity of topiary and sensory gardens, not a practice interview.",
 "https://podcasts.apple.com/gb/podcast/outsiding/id6782845808"),
("The James & Joe Garden Show","","Hosted by James Alexander-Sinclair and Joe Swift","public-art-oddity","2",
 "Two garden designers being deliberately silly - 'Hanging Baskets: A Party in a Basket or a Crime Against Gardening?', 'What RHS Judges REALLY Eat'. Humour plus real design credibility, which is the combination Oddtoe's garden work needs.",
 "https://podcasters.spotify.com/pod/show/the-james--joe-garden-sho/episodes/Hanging-Baskets"),
("Gardeners' Question Time","","BBC Radio 4","public-art-oddity","2",
 "BBC Radio 4's long-running gardening panel, and it has run a topiary segment. Prestigious and hard to book; the feed address is BBC podcast support, not an editorial or booking contact, so a real pitch needs the programme's own contact route.",
 "http://www.bbc.co.uk/programmes/b006qp2f"),
("Gardening Show","","3CR Community Radio Melbourne","melbourne-local","2",
 "Melbourne community radio, 477 episodes, weekly panel of local horticulturists and designers. Genuinely reachable local media for the sensory garden and topiary side of the practice.",
 "https://www.3cr.org.au/gardening"),
("The Gardener Ben Podcast","","Hosted by Gardener Ben","public-art-oddity","2",
 "Independent UK gardening podcast that interviews garden designers as well as growers - a recent episode covers a garden design practice. Small and bookable.",
 "https://podcasters.spotify.com/pod/show/gardener-ben/episodes/S4E7-Dakic-garden-design"),
("Jo's Art History Podcast","Jo McLaughlin","Host; art historian","public-art-oddity","2",
 "Art history deliberately made fun and accessible, with a stated mission against art-world elitism. That editorial line is friendly to an artist whose whole argument is that public space should be quirkier.",
 "https://podcasters.spotify.com/pod/show/jos-art-history-podcast/episodes/Born-to-Episode-Two-Mike-Kelly"),
("Exhibitionistas: Notes on Contemporary Art and Life","Joana P. R. Neves","Host; art curator and writer","public-art-oddity","2",
 "Award-winning contemporary art podcast hosted by a curator, describing itself as an 'art wonderment' show. Curator-hosted matters: this is a contact who commissions and selects, not only broadcasts.",
 "https://exhibitionistaspodcast.com/"),
("The Conversation Art Podcast","Michael Shaw","Host","public-art-oddity","2",
 "Long-running Los Angeles contemporary art podcast with artists, dealers and curators. Relevant to the LA positioning in Oddtoe's own brief.",
 "https://theconversationartpodcast.libsyn.com/episode-388-lauren-oneill-butler"),
("New Media Gallery Podcast","","Jack Straw Cultural Center, Seattle","hybrid-craftsman","2",
 "Interviews with resident artists in a new media gallery programme. Institutional, US-based, and a residency route as much as a press one.",
 "https://www.jackstraw.org/podcasts/new-media-gallery/"),
("The Sculptor's Funeral","Jason Arkles","Host; sculptor","public-art-oddity","2",
 "The only podcast dedicated to working figurative sculptors, with real tech talk about making. Caveat: it is explicitly in the Western European figurative tradition, which is a long way from Oddtoe's register - fit is the fabrication conversation, not the aesthetics.",
 "https://thesculptorsfuneral.libsyn.com/episode-97-drawing-in-space"),
("The love that loves you back","","First Floor Gallery Harare","public-art-oddity","2",
 "Gallery-run conversation podcast that has covered public sculpture and run an episode on AI and outsourcing humanity - both of Oddtoe's arguments in one feed.",
 "https://podcasters.spotify.com/pod/show/first-floor-gallery-harar/episodes/Abdollah-Nafisi-Public-Sculpture"),
("Drawing Funny","Lin Workman","Host; Mid-South Cartoonists Association","public-art-oddity","2",
 "A cartoonists' association podcast about the comic industry. Speaks directly to Otto's own background in political cartooning and gag panels, and the humour is the point rather than a footnote.",
 "http://www.drawingfunny.com/"),
("The Shop Stool Podcast","","Robin Lewis Makes","public-art-oddity","2",
 "Makers and fabricators talking shop across 156 episodes. Relevant to the prop design, fabrication and kinetic sculpture side of the practice rather than the screen side.",
 "https://www.robinlewismakes.com/shopstoolpodcast/"),
("Arts Underground","Katy Ganaway","Host","public-art-oddity","2",
 "Public radio arts show explicitly about 'beautiful oddities', running a recurring comedy strand alongside artist interviews including a paper sculptor. Small and regional (north Alabama), but the editorial taste is unusually aligned.",
 "https://wlrh.org/episode/arts-underground-taylor-mclendon/"),
("Art · The Creative Process: Artists, Curators, Museum Directors Talk Art, Life & Creativity","","The Creative Process network","public-art-oddity","2",
 "Interviews artists, curators and museum directors, including an episode on transforming public art and spaces with Lincoln Center's Shanta Thake. Note this network runs several parallel feeds (AI, technology) from the same interviews - pitch the network once, not each feed.",
 "https://www.creativeprocess.info/art/"),
("Gardening Australia Junior Podcast","","ABC Australia","melbourne-local","1",
 "ABC children's gardening podcast. Long shot as a press target - the audience is children, not commissioners - but the sensory garden work is genuinely a fit for a kids' format, and the ABC relationship has value beyond this show.",
 "https://www.abc.net.au/kidslisten/programs/gardening-australia-junior/"),
("The Week in Art","","The Art Newspaper","public-art-oddity","1",
 "The Art Newspaper's weekly show. Prestigious and worth knowing, but it covers major institutional stories and is not a realistic guest slot for an artist with one public commission. Record as a coverage target, not a pitch.",
 "https://www.theartnewspaper.com/the-week-in-art"),
("grow, cook, eat, arrange with Sarah Raven & friends","Sarah Raven","Host; gardener, writer and cook","public-art-oddity","1",
 "Very large UK gardening podcast, but plant- and growing-focused rather than design-focused. Long shot, and the feed publishes no contact address.",
 "https://www.sarahraven.com/podcast"),
("Muddy Boots","","Hosted by Keith and Elisabeth","public-art-oddity","1",
 "Australian gardening podcast, 257 episodes. General growing content rather than design; local, so cheap to try, but no published contact address in the feed.",
 "https://www.muddyboots.net.au"),
("Header/Footer Gallery Presents","","New Media Caucus","hybrid-craftsman","1",
 "New Media Caucus academic podcast on exhibitions and museums as laboratories. Scholarly register and the feed address is an explicit no-reply, so any approach has to go through the organisation.",
 "https://newmediacaucus.org"),
]

pool = {s["show"]: s for s in json.load(open("unique.json"))["shows"]}
rows, report = [], []
for show, person, role, hook, relevance, why, evidence in PICKS:
    s = pool[show]
    raw = s.get("email", "")
    if not raw:
        email, grade = "", "none - feed publishes no address"
    elif NOREPLY.match(raw) or RELAY.search(raw):
        email, grade = "", f"dropped - platform relay/no-reply ({raw})"
    elif GENERIC.match(raw):
        email, grade = raw, "generic org address"
    else:
        email, grade = raw, "direct"
    rows.append({
        "outlet": show[:200],
        "sourceId": f"itunes-2026-09-01",
        "segment": "podcast",
        "person": person,
        "role": role,
        "url": s.get("itunes_url", "") or s.get("website", ""),
        "email": email,
        "contactPage": s.get("website", ""),
        "linkedin": "",
        "hook": hook,
        "whyFit": why,
        "evidenceUrl": evidence,
        "relevance": relevance,
        "notes": (f"Sourced 2026-09-01 via iTunes Search API; last episode "
                  f"{s['last_episode'][:10]}; {s.get('episode_count')} episodes. "
                  f"Email {grade}, read from the RSS feed's itunes:owner field - "
                  f"not verified as a booking address."),
    })
    report.append((relevance, show[:52], email or "-", grade))

json.dump({"brand": "oddtoe", "rows": rows}, open("import-podcasts.json", "w"), indent=2)
report.sort(key=lambda r: (-int(r[0]), r[1]))
print(f"{len(rows)} rows built\n")
print(f"{'rel':>3}  {'show':54} {'email':38} grade")
for rel, show, email, grade in report:
    print(f"{rel:>3}  {show:54} {email[:36]:38} {grade[:34]}")
n_direct = sum(1 for r in rows if r["email"])
print(f"\n{n_direct}/{len(rows)} carry a usable address; "
      f"{len(rows)-n_direct} need a contact page visit")
