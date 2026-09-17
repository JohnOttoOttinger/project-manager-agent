"""Commissioner watchlist -> opportunities rows, kind='scouting'.

These are NOT live calls. They are the organisations that commission Oddtoe's
kind of work, each with a URL that was machine-checked on 1 Sep 2026 and a
next_action saying when to look. Deadlines stay empty on purpose: a watchlist
entry that carries a date nobody read is the exact failure this stream exists
to prevent.
"""
import json

# name -> (relevance, next_action, verified_date_or_blank)
J = {
"Sculpture by the Sea": (
 "TOP-TIER FIT AND THE BIGGEST MONEY ON THE LIST. Site-responsive outdoor sculpture on a coastal walk - kinetic and public sculpture is a listed Oddtoe craft. Awards include the Aqualand Sculpture Award of $70,000 (acquisitive) and three Helen Lempriere Scholarships for Australian artists ($35k senior, $30k mid-career, $25k emerging). Australian-eligible, no invitation needed - exactly the 'first rung' route the positioning brief argues for.",
 "2026 submissions CLOSED 11:59pm AEST 19 Apr 2026; the exhibition runs 16 Oct - 2 Nov 2026 along the Bondi-Tamarama walk. Two actions: (1) VISIT the Oct-Nov 2026 show as scouting - see what gets selected; (2) diarise FEBRUARY 2027 to catch the Bondi 2027 call opening. Cottesloe (Perth) runs on its own cycle, check separately.",
 "2026-09-01"),
"Swell Sculpture Festival": (
 "STRONG FIT. Beachfront outdoor sculpture festival at Currumbin, Gold Coast; large-scale site-responsive work, generally September. Smaller and more approachable than Sculpture by the Sea, which makes it a realistic first outdoor credit.",
 "Check the artists/EOI page for the next call - cycle TO VERIFY.", ""),
"Sculpture at Scenic World": (
 "GOOD FIT and unusual siting - sculpture installed through Jamison Valley rainforest on a boardwalk, so works must survive weather and read in a natural setting. Suits fabrication plus the environmental/garden sensibility.",
 "Find the artist entry page and record the annual call dates - cycle TO VERIFY.", ""),
"McClelland Sculpture Survey & Award": (
 "STRONG FIT AND LOCAL - Langwarrin, on Melbourne's edge, one of Australia's most significant sculpture awards, set in a sculpture park. A Victorian institution Oddtoe can reach by car.",
 "Survey is periodic rather than annual - confirm whether the next Survey is announced and how artists are considered (some editions are invitation/nomination based, which would change the approach). TO VERIFY.", ""),
"Woollahra Small Sculpture Prize": (
 "MODERATE FIT. Small-scale sculpture prize, annual, Sydney. Small format is a different discipline to the building-sized work, but it is a low-cost credit and prizes build the CV the positioning brief says is the real gap.",
 "Council site blocks automated checks - open it by hand and record the annual entry window.", ""),
"Lorne Sculpture Biennale": (
 "STRONG FIT, VICTORIAN, AND THE TIMING IS LIVE. Site-responsive outdoor sculpture along the Lorne foreshore; the 2025 edition showed sixteen new site-responsive works. Coastal, environmental and public - directly onto Oddtoe's outdoor practice.",
 "BIENNIAL, held in March. The 2025 edition ran 1-30 Mar 2025, so the next is MARCH 2027 - which means the artist call should open around MID-2026, i.e. NOW. Check lornesculpture.com/latest-news early. Domain did not answer an automated probe on 1 Sep 2026; open it manually.",
 "2026-09-01"),
"Montalto Sculpture Prize": (
 "GOOD FIT, VICTORIAN. Annual sculpture prize sited across a vineyard and gardens on the Mornington Peninsula - an outdoor, landscape-sited commission an hour from Melbourne.",
 "Confirm the annual entry window on the sculpture page. TO VERIFY.", ""),
"Yorkshire Sculpture Park": (
 "ASPIRATIONAL. Major international sculpture park. Realistically a scouting and relationship target rather than an open-call route, but its opportunities page is worth watching.",
 "Watch the opportunities page; treat as long-term.", ""),
"Amsterdam Light Festival": (
 "TOP-TIER FIT AND IMMINENT. Large-scale light artworks sited along Amsterdam's canals, seen by very large audiences. The festival states plainly that BOTH light-art professionals AND newcomers can submit an idea, and explicitly encourages creatives from varied backgrounds - so the thin exhibition CV is not disqualifying. Selected works receive technical and financial support.",
 "ACT THIS MONTH. The Edition 15 (2026-27) call has closed, and the festival says the Edition 16 (2027-28) open call opens in EARLY SEPTEMBER and that all information is published on amsterdamlightfestival.com/en/open-call first. Watch that page now. Portfolio contact: artists@amsterdamlightfestival.com.",
 "2026-09-01"),
"Lumiere (Artichoke)": (
 "STRONG FIT. Artichoke produces Lumiere Durham and large-scale public art events in the UK - projection, light and spectacle in public space, which is Oddtoe's territory. Artichoke has historically run open calls (Brilliant / Lumiere BRILLIANT).",
 "Watch artichoke.uk.com opportunities. Cycle TO VERIFY.", ""),
"Fête des Lumières Lyon": (
 "STRONG FIT. One of the world's largest light festivals; runs an artist call for projects sited across the city.",
 "Find the 'appel a projets' page and record its annual window - typically well ahead of the December festival. TO VERIFY.", ""),
"Signal Festival Prague": (
 "STRONG FIT. Light and digital art festival with a track record of commissioning new work from international artists.",
 "Watch signalfestival.com for the open call. Cycle TO VERIFY.", ""),
"i Light Singapore": (
 "STRONG FIT. Sustainable light art festival run by the Urban Redevelopment Authority; runs an international open call and pays production. Singapore is on the list of markets already in play for the agencies stream.",
 "Watch ilightsingapore.gov.sg for the artist open call. Cycle TO VERIFY.", ""),
"GLOW Eindhoven": (
 "GOOD FIT. Annual light art route through Eindhoven, November, strong design-city context.",
 "Watch gloweindhoven.nl for artist submissions. Cycle TO VERIFY.", ""),
"Luminale Frankfurt": (
 "GOOD FIT but confirm it is running. Biennial light art and urban design festival held alongside the Light + Building trade fair.",
 "The 2024 edition was CANCELLED and the following edition is listed as 2026 TBA. Confirm the festival is actually proceeding before investing time. Domain did not answer an automated probe; try luminale-frankfurt.de/en/m/die-luminale/.",
 "2026-09-01"),
"Bella Skyway Festival": (
 "MODERATE FIT. Light festival in Torun, Poland, with projection and installation work.",
 "Watch bellaskyway.pl/en for an open call. Cycle TO VERIFY.", ""),
"LUX Helsinki": (
 "GOOD FIT. City-run winter light festival, January, commissions light installations across Helsinki.",
 "Watch luxhelsinki.fi/en for the artist call. Cycle TO VERIFY.", ""),
"Winter Lights Canary Wharf": (
 "GOOD FIT and commercially interesting - a corporate estate commissioning interactive light art annually, which is closer to the paid-commission end than a festival prize.",
 "Find who curates it (the estate uses producers) and approach through that route rather than waiting for a public call.", ""),
"Melbourne International Flower & Garden Show": (
 "DISTINCTIVE FIT - THE CLEAREST USE OF THE GARDEN SIDE. Australia's largest horticultural event, held at the Royal Exhibition Building and Carlton Gardens each March, with juried Show Garden and Boutique Garden categories. Topiary and sensory garden design is a listed Oddtoe craft and almost nobody in the experiential field competes here. A local, buildable, award-bearing credit.",
 "Find the designer/exhibitor application window - applications typically open the winter before the March show, so CHECK NOW for 2027. TO VERIFY.", ""),
"RHS Chelsea Flower Show": (
 "ASPIRATIONAL BUT THE RIGHT AMBITION. The most prestigious garden show in the world; RHS commissions and juries show gardens. A Chelsea garden would be a career-changing credit for the garden strand.",
 "Understand the RHS garden proposal process and lead times (multi-year, and normally requires a named sponsor). Long-term - but read the process now so the option stays open.", ""),
"RHS Hampton Court Palace Garden Festival": (
 "BETTER FIRST RHS TARGET THAN CHELSEA. Larger, more experimental, and more open to conceptual and installation-led gardens than Chelsea.",
 "Read the RHS show-garden application process and deadlines. TO VERIFY.", ""),
"Singapore Garden Festival": (
 "STRONG AND UNDER-CONTESTED FIT. NParks' international garden festival invites designers to create fantasy and landscape gardens - conceptual, spectacle-driven horticulture, which is precisely where topiary plus fabrication plus a sense of humour would stand out.",
 "Find the designer invitation/application route on nparks.gov.sg/sgf. Cycle TO VERIFY.", ""),
"International Garden Festival (Jardins de Metis)": (
 "EXCELLENT CONCEPTUAL FIT. Quebec's annual International Garden Festival runs a genuine international open call for CONTEMPORARY conceptual gardens - installation art that happens to be a garden. This is the single best match on the list for the sensory-garden and topiary strand combined with the playful register.",
 "Find the annual competition call at jardinsdemetis.com - historically opens in the northern autumn for the following summer. CHECK NOW. TO VERIFY.", ""),
"Domaine de Chaumont-sur-Loire International Garden Festival": (
 "EXCELLENT CONCEPTUAL FIT, same family as Metis. A long-running international festival that commissions experimental conceptual gardens on an annual theme, with a public call.",
 "Find the annual 'concours' / call for projects and its deadline. TO VERIFY.", ""),
"Floriade Canberra": (
 "MODERATE FIT. Australia's largest flower festival; commissions installations and public programming alongside the horticulture.",
 "Identify who commissions art and installation for Floriade - likely a direct approach rather than an open call.", ""),
"Ars Electronica": (
 "STRONG FIT FOR THE AI-ANIMATION STRAND. The Prix Ars Electronica is the most established award in digital and computer-generated art, with categories covering AI and computer animation. Also the field's central gathering.",
 "Prix categories and deadlines are published at ars.electronica.art/prix - the deadline usually falls in the northern spring. Record the exact date. TO VERIFY.", ""),
"Sonar+D": (
 "MODERATE FIT. The creative-technology strand of Sonar Barcelona; showcases interactive and AV installation work.",
 "Watch for the Sonar+D projects call. Note sonar.es issues a 308 redirect - use the site's own navigation.", ""),
"MUTEK": (
 "GOOD FIT. Digital creativity and electronic arts festival with editions in Montreal and several other cities; programs AV performance and immersive installation.",
 "Watch mutek.org for artist submissions across editions. Cycle TO VERIFY.", ""),
"ISEA (International Symposium on Electronic Art)": (
 "GOOD FIT for the credentialled/academic route. Rotating international symposium with an annual open call for artworks and papers - a recognised line on a CV.",
 "Identify the host city and open call for the next edition at isea-international.org. TO VERIFY.", ""),
"FILE Sao Paulo": (
 "MODERATE FIT. Long-running electronic language art festival with an annual open call across animation, installation and interactive work - historically accessible to unrepresented artists.",
 "Watch file.org.br for the annual call. TO VERIFY.", ""),
"Currents New Media": (
 "MODERATE FIT. Santa Fe new-media festival with an annual open call covering installation, projection and generative work; known for being open to newcomers.",
 "Watch currentsnewmedia.org for the annual call. TO VERIFY.", ""),
"Athens Digital Arts Festival": (
 "MODERATE FIT. Annual open call across digital art categories including animation and installation; low barrier, international.",
 "Watch adaf.gr for the annual open call. TO VERIFY.", ""),
"ANAT (Australian Network for Art and Technology)": (
 "STRONG FIT AND AUSTRALIAN. The national body for art and technology; runs residencies, labs and funded programs, and its opportunities page aggregates Australian art-tech calls. Membership is cheap and it is the natural professional home for this practice.",
 "Watch anat.org.au/opportunities - a live, machine-checked opportunities page. Consider joining.", "2026-09-01"),
"Dark Mofo": (
 "STRONG FIT ON REGISTER. Mona's winter festival, Hobart - large-scale public spectacle with a taste for the odd and the confronting. The playfulness and public-spectacle instinct fit; it has run public art commissions and open calls.",
 "Watch darkmofo.net.au for commissions and open calls; also a scouting trip.", ""),
"City of Melbourne — public art": (
 "HIGHEST-VALUE LOCAL RELATIONSHIP. Otto's own council, and the commissioner behind Now or Never and the Signal space where Babbling with Baobabs was delivered in 2019 - the studio's one public credit. That prior relationship is the strongest door on this list.",
 "Watch the arts and culture pages for public art EOIs, Signal programs and Now or Never artist calls. Given the 2019 credit, a direct approach to the public art team is also warranted.", "2026-09-01"),
"Creative Victoria": (
 "STATE FUNDING BODY - the layer above the councils. Runs the Creative Projects Fund and other programs an individual artist can apply to.",
 "Site blocks automated checks; open creative.vic.gov.au/funding-opportunities by hand and record the current rounds and their dates.", ""),
"City of Yarra — public art": (
 "GOOD LOCAL FIT. Inner-Melbourne council with an active public art program; also the council behind the Gertrude Street Projection Festival already on the board.",
 "Site blocks automated checks - open it by hand and find the public art EOI register.", ""),
"City of Port Phillip — public art": (
 "GOOD LOCAL FIT. St Kilda and surrounds; active public art and festival program with regular commissions.",
 "Find the public art EOI or artist register. TO VERIFY.", ""),
"Merri-bek City Council — public art": (
 "GOOD LOCAL FIT. Formerly Moreland; a strong arts program and regular public art commissions in Melbourne's north.",
 "Find the public art EOI or artist register. TO VERIFY.", ""),
"Darebin City Council — arts": (
 "GOOD LOCAL FIT. Active arts and public art program in Melbourne's north.",
 "Site blocks automated checks - open it by hand and find the arts grants and public art pages.", ""),
"Maribyrnong City Council — public art": (
 "GOOD LOCAL FIT, and next door to Brimbank whose residency cycle is already on the board. Melbourne's inner west runs the same shape of scheme.",
 "Site blocks automated checks - open it by hand and find the public art program.", ""),
"Wyndham City Council — public art": (
 "GOOD LOCAL FIT. Fast-growing outer-west council with real public art budgets attached to new development.",
 "Find the public art EOI or artist register on the arts and culture pages. TO VERIFY.", ""),
"ACMI": (
 "STRONG INSTITUTIONAL FIT. Australia's museum of screen culture, in Fed Square - the natural institutional home for generative AI animation, and it commissions and exhibits moving-image work.",
 "Watch the work-with-us and commissioning pages; also a relationship target given the animation strand.", ""),
"Federation Square": (
 "GOOD FIT. Melbourne's central civic space, programs large-scale public work and facade projection - Jess Johnson's XYZZY REDUX ran on the Hamer Hall facade nearby during Now or Never 2026.",
 "Find who programs the public space and the big screen; likely a direct approach rather than an open call.", ""),
"Regional Arts Victoria": (
 "MODERATE FIT. Supports and tours work into regional Victoria; a route to commissions outside metropolitan Melbourne and to touring an existing work.",
 "Watch rav.net.au for programs and commissions. TO VERIFY.", ""),
}

rows, missing = [], []
for e in json.load(open("resolved.json")):
    name = e["n"]
    if name not in J:
        missing.append(name); continue
    relevance, action, verified = J[name]
    status_note = {
        "200": "URL machine-checked 200 OK on 1 Sep 2026.",
        "HTTP 403": "URL returns 403 to automated checks (site firewall) - the link is very likely fine, confirm once by hand.",
        "HTTP 308": "URL issues a 308 redirect - use the site's own navigation.",
        "UNREACHABLE": "URL did NOT answer an automated probe on 1 Sep 2026 - verify by hand before trusting it.",
    }.get(e["url_status"], e["url_status"])
    rows.append({
        "name": name, "sourceId": "commissioner-watchlist-2026-09-01",
        "organiser": e["o"], "kind": "scouting", "city": e["c"], "country": e["k"],
        "url": e["url"], "submissionDeadline": "", "pressDeadline": "",
        "relevance": relevance, "nextAction": action, "verified": verified,
        "notes": f"WATCHLIST — {e['g']}. Not a live call: this is a commissioner to check on a "
                 f"schedule. {status_note} {e['url_note'] if e['url_note'] and e['url_status']!='200' else ''}".strip(),
    })

if missing:
    raise SystemExit(f"no judgement written for: {missing}")
json.dump({"brand": "oddtoe", "rows": rows}, open("import-watchlist.json", "w"), indent=2)
print(f"{len(rows)} watchlist rows built")
from collections import Counter
for g, n in Counter(r["notes"].split("— ")[1].split(".")[0] for r in rows).most_common():
    print(f"  {n:>2}  {g}")
