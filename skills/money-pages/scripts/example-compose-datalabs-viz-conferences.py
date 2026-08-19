#!/usr/bin/env python3
"""Compose the Datalabs 'Data Visualization & Design Conferences 2026 & 2027' PAGE
from design-kit-datalabs-events.html v0 (the Otto-approved v2 design on Datalabs palette).

Rebuild of post 26131 (dated URL /2026/03/25/data-visualization-conferences-2026-2027/)
as an evergreen PAGE per Otto's decision (19 Aug 2026); Redirection 301 at swap time.
All dates/venues verified 19 Aug 2026 (research log in session transcript). Dropped from
the old post: ICDVID (predatory conference-mill listing — verified). Voice: first-person
Otto, Australian spelling. Images: Otto's own conference-art set, he re-art-directs v0.
"""
import re, pathlib, sys, base64, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parents[3]
KIT = (ROOT / 'skills/money-pages/references/design-kit-datalabs-events.html').read_text()
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path('composed-viz-conferences.html')

markers = [
    ('hero',     '<!-- PAT-HERO'),
    ('band',     '<!-- PAT-HEADING-BAND'),
    ('intro',    '<!-- PAT-INTRO'),
    ('picks',    '<!-- PAT-TOP-PICKS'),
    ('month',    '<!-- PAT-MONTH-HEADING'),
    ('eventR',   '<!-- PAT-EVENT-IMG-RIGHT'),
    ('eventL',   '<!-- PAT-EVENT-IMG-LEFT'),
    ('outro',    '<!-- PAT-OUTRO'),
    ('faq',      '<!-- PAT-FAQ'),
    ('footer',   '<!-- FIXED FOOTER BLOCKS (Datalabs'),
]
idx = [(name, KIT.index(m)) for name, m in markers]
blocks = {}
for i, (name, start) in enumerate(idx):
    end = idx[i + 1][1] if i + 1 < len(idx) else len(KIT)
    blocks[name] = KIT[start:end]

def fill(block, mapping):
    for name, val in mapping.items():
        block = re.sub(r'\{\{' + name + r'(:[^}]*)?\}\}', val.replace('\\', r'\\'), block)
    return block

def strip_comments(html):
    return re.sub(r'<!--.*?-->', '', html, flags=re.S)

UTM = 'data-visualization-conferences-guide'
ARVO = '<p class="p1"><span style="font-family: arvo, serif;">'
CANON = 'The <strong>Datalabs Agency</strong> is a Melbourne-based data visualization consultancy founded in 2012 that delivers corporate training workshops (Power BI, Tableau, data storytelling), dashboard design, and BI style guides for clients including Mercedes-Benz, Adidas, and UPS.'

HERO = {
    'HERO_KICKER': 'Your guide to the best data visualization and design conferences in the world',
    'HERO_TITLE': 'DATA VIZ CONFERENCES',
    'HERO_RANGE': '2026 &amp; 2027',
    'UPDATED_DATE': 'August 2026',
    'HERO_BG_URL': 'https://www.datalabsagency.com/wp-content/uploads/2026/08/design-conferences-visualization-japan-dark.jpg',
    'HERO_BG_ID': '53677',
}
BAND = {
    'BAND_SUBTITLE': 'Where the world&rsquo;s chart-makers, designers and dashboard people meet',
    'BAND_TITLE_LINE1': 'What are the Best Data Visualization',
    'BAND_TITLE_LINE2': '&amp; Design Conferences in 2026 &amp; 2027?',
}
INTRO = {
    'INTRO_COL1': f'''
{ARVO}Planning your conference calendar for the year ahead? Here is my verified guide to the <strong>best data visualization and design conferences in 2026 and 2027</strong> &mdash; exact dates, cities, and who each event is really for. Every date on this page has been checked against the conference&rsquo;s own site this month.</span></p>
''',
    'INTRO_COL2': f'''
{ARVO}The calendar splits into two camps. The <strong>research conferences</strong> &mdash; IEEE VIS, EuroVis, PacificVis &mdash; are where the field&rsquo;s new ideas surface first. The <strong>practitioner events</strong> &mdash; Tableau Conference, Outlier &mdash; are where working analysts and designers trade techniques. I&rsquo;ll tell you which is which, because they are very different rooms.</span></p>
''',
    'INTRO_COL3': f'''
{ARVO}{CANON} That is the seat this list is written from &mdash; and if a conference is not in the budget this year, an <a href="https://www.datalabsagency.com/data-visualization-training/">in-house training workshop</a> is how many of our clients close the same skills gap.</span></p>
''',
}
INTRO['INTRO_LEADOUT'] = 'Here are <strong>my picks for the data visualization conferences of 2026 and 2027</strong>. &raquo;'
PICKS = {
    'PICKS_HEADING': 'What are the Best Data Viz Conferences in the World?',
    'PICKS_SUBTITLE': 'My Top 4',
    'PICK1_IMAGE_ID': '37536', 'PICK1_LABEL': 'Best Overall', 'PICK1_NAME': 'IEEE VIS 2026', 'PICK1_DETAIL': 'Boston, U.S.A.',
    'PICK2_IMAGE_ID': '37515', 'PICK2_LABEL': 'Best in Asia-Pacific', 'PICK2_NAME': 'IEEE PacificVis 2027', 'PICK2_DETAIL': 'Busan, South Korea',
    'PICK3_IMAGE_ID': '37038', 'PICK3_LABEL': 'Best in Australia', 'PICK3_NAME': 'Gartner D&amp;A Summit', 'PICK3_DETAIL': 'Sydney, Australia',
    'PICK4_IMAGE_ID': '37545', 'PICK4_LABEL': 'Best Community Feel', 'PICK4_NAME': 'Outlier 2027', 'PICK4_DETAIL': 'Data Visualization Society',
}

# (month_label or None, side R/L alternating handled below, event dict)
EVENTS = [
    ('SEPTEMBER 2026', {
        'EVENT_NAME': 'CDAO Melbourne 2026', 'EVENT_URL': 'https://cdao-mel.coriniumintelligence.com/',
        'ENTRY_IMAGE_ID': '26153',
        'EVENT_KICKER': 'CDAO Melbourne brings 500+ senior data leaders to my home town on 1&ndash;2 September.',
        'EVENT_DATES': '1&ndash;2 September 2026', 'EVENT_LOCATION': 'Melbourne, Australia',
        'EVENT_BODY': '''If you are in Australia and reading this in time: Corinium&rsquo;s <strong>Chief Data &amp; Analytics Officer</strong> conference lands in Melbourne with <strong>70+ speakers and 500+ senior data and AI leaders</strong> from finance, government, healthcare, retail and energy. It leans executive &mdash; strategy and agentic-AI case studies rather than chart craft &mdash; but it is the most substantial dated data event on Australian soil this year, and it is co-located with Data &amp; AI Architecture and Enterprise AI events on day two. If your interest is presentation-layer skills rather than leadership networking, see the honest note in the FAQ below about the Australian scene.''',
    }),
    (None, {
        'EVENT_NAME': 'DATA ANALYTICS 2026', 'EVENT_URL': 'https://www.iaria.org/conferences2026/DATAANALYTICS26.html',
        'ENTRY_IMAGE_ID': '37521',
        'EVENT_KICKER': 'DATA ANALYTICS 2026 runs in Barcelona from 27 September to 1 October, onsite or virtual.',
        'EVENT_DATES': '27 September &ndash; 1 October 2026', 'EVENT_LOCATION': 'Barcelona, Spain (hybrid)',
        'EVENT_BODY': '''The <strong>Fifteenth International Conference on Data Analytics</strong> is the <strong>academic option</strong> on this list &mdash; an IARIA conference covering machine learning, big-data analytics and BI, co-located with seven sibling conferences as part of the <strong>NexTech 2026 congress</strong>. Fair warning from me: IARIA events are volume academic conferences, not industry showcases &mdash; you go to read papers and meet researchers, not to see keynote theatrics. The hybrid option (attend virtually) makes it a low-cost way to sample the research end of the field from Australia.''',
    }),
    ('NOVEMBER 2026', {
        'EVENT_NAME': 'IEEE VIS 2026', 'EVENT_URL': 'https://ieeevis.org/year/2026/welcome/',
        'ENTRY_IMAGE_ID': '37536',
        'EVENT_KICKER': 'IEEE VIS is the premier visualization conference on Earth &mdash; Boston, 9&ndash;13 November.',
        'EVENT_DATES': '9&ndash;13 November 2026', 'EVENT_LOCATION': 'Boston, U.S.A. (+ satellites in Paris &amp; Tianjin)',
        'EVENT_BODY': '''My <strong>best-overall pick</strong>. <strong>IEEE VIS</strong> is where the field&rsquo;s future arrives first &mdash; the premier forum for visualization and visual analytics research, run this year from Boston&rsquo;s Back Bay with <strong>satellite venues in Paris and Tianjin</strong> for those who cannot cross an ocean. Registration is already open; the keynote is NASA&rsquo;s <strong>Kimberly Arcand</strong>, who visualises deep-space data. Practitioners should look at <strong>CLUSTER, the practitioners&rsquo; summit</strong>, and the VIS Arts Program &mdash; the two corners of VIS built for people who make charts for a living rather than write papers about them.''',
    }),
    ('APRIL 2027', {
        'EVENT_NAME': 'IEEE PacificVis 2027', 'EVENT_URL': 'https://pacificvis2027.github.io/',
        'ENTRY_IMAGE_ID': '37515',
        'EVENT_KICKER': 'IEEE PacificVis turns 20 in Busan, South Korea, 19&ndash;22 April 2027.',
        'EVENT_DATES': '19&ndash;22 April 2027', 'EVENT_LOCATION': 'Busan, South Korea',
        'EVENT_BODY': '''The <strong>20th-anniversary edition</strong> of the <strong>IEEE Pacific Visualization Conference</strong> &mdash; the research conference built to grow visualization in the <strong>Asia-Pacific</strong>. For Australian readers this is the practical one: Busan is a nine-hour flight, not a twenty-hour one, and the programme carries the same IEEE rigour as its Boston sibling at a fraction of the travel cost. If you have ever wanted to see where the region&rsquo;s visualization research is heading &mdash; and it is heading somewhere fast &mdash; the anniversary year is the year to go.''',
    }),
    ('JUNE 2027', {
        'EVENT_NAME': 'Gartner Data &amp; Analytics Summit', 'EVENT_URL': 'https://www.gartner.com/en/conferences/apac/data-analytics-australia',
        'ENTRY_IMAGE_ID': '37038',
        'EVENT_KICKER': 'Gartner&rsquo;s Sydney summit is announced for 7&ndash;8 June 2027 at ICC Sydney.',
        'EVENT_DATES': 'Announced for 7&ndash;8 June 2027', 'EVENT_LOCATION': 'ICC Sydney, Australia',
        'EVENT_BODY': '''My <strong>best-in-Australia pick</strong> for 2027. <strong>Gartner&rsquo;s APAC Data &amp; Analytics Summit</strong> returns to the <strong>International Convention Centre Sydney</strong>, aimed at data and analytics leaders &mdash; strategy, governance, AI and the BI tooling landscape. It is a suits-and-lanyards event rather than a designers&rsquo; gathering, but it is where Australian data teams&rsquo; budgets and roadmaps get set, and the tooling floor is the best place in the country to compare BI platforms side by side in one afternoon. Dates are as announced at the time of writing &mdash; check Gartner&rsquo;s page before booking.''',
    }),
    ('2027 &mdash; DATES COMING', {
        'EVENT_NAME': 'Tableau Conference 2027 (TC27)', 'EVENT_URL': 'https://www.salesforce.com/tableau-conference/',
        'ENTRY_IMAGE_ID': '37548',
        'EVENT_KICKER': 'Tableau Conference is the biggest event in the Tableau world &mdash; TC27 is not yet dated.',
        'EVENT_DATES': 'TC27 &mdash; dates to be announced', 'EVENT_LOCATION': 'U.S.A. (TC26 was San Diego)',
        'EVENT_BODY': '''The one my <a href="https://www.datalabsagency.com/tableau-dashboard-design-training/">Tableau training</a> clients always ask about. TC26 came and went in San Diego this May, so the next edition is <strong>TC27</strong> &mdash; Salesforce has a sign-up list open but no dates or city yet. When it lands, expect what TC always delivers: the largest gathering in the Tableau ecosystem, from first-dashboard beginners to the product team itself, heavy on hands-on sessions and famously heavy on community. Join the waitlist and watch this page &mdash; I&rsquo;ll update it the day dates appear.''',
    }),
    (None, {
        'EVENT_NAME': 'EuroVis 2027', 'EVENT_URL': 'https://eurovis27.github.io/web/',
        'ENTRY_IMAGE_ID': '37530',
        'EVENT_KICKER': 'EuroVis 2027 moves to Stuttgart, Germany &mdash; dates still to be announced.',
        'EVENT_DATES': '2027 &mdash; dates to be announced', 'EVENT_LOCATION': 'Stuttgart, Germany',
        'EVENT_BODY': '''Europe&rsquo;s premier visualization research conference changes address: after Nottingham in 2026, the <strong>29th EuroVis</strong> will be hosted by the Visualization Research Center (VISUS) at the <strong>University of Stuttgart</strong>. The Eurographics/IEEE VGTC pedigree makes this the continent&rsquo;s answer to IEEE VIS &mdash; smaller, more walkable, and with a strong tradition of state-of-the-art reports that are genuinely readable by practitioners. If Europe 2027 is on your travel map, pencil it in and watch the official site for dates.''',
    }),
    (None, {
        'EVENT_NAME': 'Outlier 2027', 'EVENT_URL': 'https://www.datavisualizationsociety.org/outlier',
        'ENTRY_IMAGE_ID': '37545',
        'EVENT_KICKER': 'Outlier is the Data Visualization Society&rsquo;s own conference &mdash; 2027 planning is underway.',
        'EVENT_DATES': '2027 &mdash; planning underway', 'EVENT_LOCATION': 'Format to be announced (2026 was virtual)',
        'EVENT_BODY': '''My <strong>best-community pick</strong>. <strong>Outlier</strong> is the conference the <strong>Data Visualization Society</strong> runs for itself &mdash; artists, journalists, BI developers and academics in one (often virtual) room, talking data design, storytelling and ethics. The 2026 edition ran online in June; organisers have said planning for 2027 is underway but nothing is dated yet. Two things make it special: the talks end up free on the DVS YouTube channel, and it is the rare conference where a hobbyist and a New York Times graphics editor genuinely mix.''',
    }),
    (None, {
        'EVENT_NAME': 'Information+ 2027', 'EVENT_URL': 'https://informationplusconference.com/',
        'ENTRY_IMAGE_ID': '51994',
        'EVENT_KICKER': 'Information+ is the design-research crowd&rsquo;s biennial gathering &mdash; a 2027 edition would fit the cadence.',
        'EVENT_DATES': 'Biennial &mdash; 2027 edition not yet confirmed', 'EVENT_LOCATION': 'Location to be announced (2025 was Boston)',
        'EVENT_BODY': '''<strong>Information+</strong> is the most design-minded event on this list: a biennial, interdisciplinary conference where <strong>information designers, educators and researchers</strong> meet in one place &mdash; less algorithms, more typography, colour and communication. The last edition ran in Boston in late 2025, and the two-year rhythm points to 2027, though the organisers have confirmed nothing yet. I include it because readers of this page who care about the <em>design</em> half of data visualization will find their people here more than anywhere else on the calendar.''',
    }),
]
OUTRO = {
    'OUTRO_HEADING': 'What Other Data Viz Conferences Are Worth Watching?',
    'OUTRO_BODY': '''A few honest notes from the verification pass behind this update. Some once-loved events are dormant: <strong>Tapestry</strong> has not run since the late 2010s, and Malofiej &mdash; the infographics world&rsquo;s Pulitzers &mdash; has been paused since 2021. Eyeo Festival has third-party listings claiming a 2026 revival that its own site does not confirm, so it stays off this list until it does. And one listing from the previous version of this page has been removed entirely after it turned out to be a conference-mill advertisement rather than a real event &mdash; a reminder of why every date here is checked at the source.

Know a conference I have missed &mdash; especially an Australian one? <a href="https://www.datalabsagency.com/contact/">Contact me</a> and I&rsquo;ll verify it and add it. Planning your data year? See the sibling guide to <a href="https://www.datalabsagency.com/data-analytics-conferences/">data analytics conferences</a>, or bring the conference to your team with a <a href="https://www.datalabsagency.com/data-visualisation-workshop-pricing/">data visualization workshop</a>.''',
}
FAQS = [
    ('When are the big data visualization conferences in 2026 and 2027?',
     'The verified anchors are IEEE VIS in Boston (9&ndash;13 November 2026), IEEE PacificVis in Busan (19&ndash;22 April 2027) and Gartner&rsquo;s Sydney summit (announced for 7&ndash;8 June 2027). Tableau Conference, EuroVis and Outlier will all run 2027 editions that are not yet dated.'),
    ('Is there a data visualization conference in Australia?',
     'There is no dedicated data-visualization-craft conference in Australia right now. The local calendar runs on analytics leadership events &mdash; CDAO Melbourne (1&ndash;2 September 2026) and Gartner&rsquo;s Data &amp; Analytics Summit in Sydney &mdash; plus meetups. Many Australian teams close the gap with in-house training instead.'),
    ('What is the difference between a research and a practitioner conference?',
     'Research conferences like IEEE VIS, EuroVis and PacificVis are built around peer-reviewed papers &mdash; you see the field&rsquo;s future two years early. Practitioner events like Tableau Conference and Outlier are built around talks and workshops on doing the work today. Choose by which room you want to be in.'),
    ('Are data visualization conferences worth attending virtually?',
     'Often, yes &mdash; more than in most fields. Outlier runs virtual-first, IEEE VIS 2026 has satellite venues in Paris and Tianjin, and DATA ANALYTICS 2026 in Barcelona offers full virtual participation. The talks translate to a screen well; the hallway conversations do not, so go in person when the goal is meeting people.'),
]

page_faq = blocks['faq']
page_faq = fill(page_faq, {'FAQ_TOPIC': 'Data Viz Conferences'})
for i, (q, a) in enumerate(FAQS, 1):
    page_faq = fill(page_faq, {f'FAQ_Q{i}': q, f'FAQ_A{i}': a, f'FAQ_TAB_ID_{i}': f'faqvizconf-{i}-2026'})
jsonld = ('<script type="application/ld+json">{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ['
    + ', '.join('{"@type": "Question", "name": "%s", "acceptedAnswer": {"@type": "Answer", "text": "%s"}}' %
        (re.sub(r'<[^>]+>', '', q).replace('&ndash;', '–').replace('&amp;', '&').replace('&rsquo;', '’').replace('"', '\\"'),
         re.sub(r'<[^>]+>', '', a).replace('&ndash;', '–').replace('&amp;', '&').replace('&rsquo;', '’').replace('"', '\\"'))
        for q, a in FAQS) + ']}</script>')
b64 = base64.b64encode(urllib.parse.quote(jsonld, safe='').encode()).decode()
page_faq = fill(page_faq, {'FAQ_JSONLD_B64': b64})

body_parts = [fill(blocks['hero'], HERO), fill(blocks['band'], BAND), fill(blocks['intro'], INTRO), fill(blocks['picks'], PICKS)]
side = 0  # first entry image-left per the alternation rule (featured opens image-left)
for month, ev in EVENTS:
    if month:
        body_parts.append(fill(blocks['month'], {'MONTH_LABEL': month}))
    blk = blocks['eventL'] if side % 2 == 0 else blocks['eventR']
    body_parts.append(fill(blk, {**ev, 'UTM_CAMPAIGN': UTM}))
    side += 1
body_parts += [fill(blocks['outro'], OUTRO), page_faq, blocks['footer']]
page = strip_comments(''.join(body_parts))
# collapse inter-row whitespace — stray text between rows becomes EMPTY FILLER ROWS
# on the first WPBakery save (16 of them appeared on 16173, 19 Aug 2026)
page = re.sub(r'\]\s+\[', '][', page.replace('\r\n', '\n'))
leftover = sorted(set(re.findall(r'\{\{([A-Z0-9_]+)(?::[^}]*)?\}\}', page)))
if leftover:
    sys.exit(f'ABORT — unfilled tokens: {leftover}')
OUT.write_text(page)
print(f'wrote {OUT} ({len(page)} chars)')
