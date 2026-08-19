#!/usr/bin/env python3
"""Compose the Datalabs 'Data Analytics Conferences 2026 & 2027' PAGE from
design-kit-datalabs-events.html v0. Rebuild of post 25928 (dated URL) as an
evergreen PAGE per Otto's decision (19 Aug 2026); Redirection 301 at swap time.

All dates verified 19 Aug 2026. Dropped from the old post: RE-WORK Deep Learning
Summit (defunct), MADS (absorbed into Content Marketing World), VB Transform (2027
unannounced, invite-only format), HIC (niche + 2026 passed), INFORMS Analytics+
(2027 unannounced — outro note). Two hedged entries flagged in copy: Ai4 2027 exact
dates and World Data Summit 2027 dates. Images: original post's city set, reused
by city; Otto re-art-directs v0.
"""
import re, pathlib, sys, base64, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parents[3]
KIT = (ROOT / 'skills/money-pages/references/design-kit-datalabs-events.html').read_text()
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path('composed-analytics-conferences.html')

markers = [
    ('hero', '<!-- PAT-HERO'), ('band', '<!-- PAT-HEADING-BAND'), ('intro', '<!-- PAT-INTRO'),
    ('picks', '<!-- PAT-TOP-PICKS'), ('month', '<!-- PAT-MONTH-HEADING'),
    ('eventR', '<!-- PAT-EVENT-IMG-RIGHT'), ('eventL', '<!-- PAT-EVENT-IMG-LEFT'),
    ('outro', '<!-- PAT-OUTRO'), ('faq', '<!-- PAT-FAQ'), ('footer', '<!-- FIXED FOOTER BLOCKS (Datalabs'),
]
idx = [(name, KIT.index(m)) for name, m in markers]
blocks = {name: KIT[start:(idx[i+1][1] if i+1 < len(idx) else len(KIT))] for i, (name, start) in enumerate(idx)}

def fill(block, mapping):
    for name, val in mapping.items():
        block = re.sub(r'\{\{' + name + r'(:[^}]*)?\}\}', val.replace('\\', r'\\'), block)
    return block

UTM = 'data-analytics-conferences-guide'
ARVO = '<p class="p1"><span style="font-family: arvo, serif;">'
CANON = 'The <strong>Datalabs Agency</strong> is a Melbourne-based data visualization consultancy founded in 2012 that delivers corporate training workshops (Power BI, Tableau, data storytelling), dashboard design, and BI style guides for clients including Mercedes-Benz, Adidas, and UPS.'

HERO = {
    'HERO_KICKER': 'Your guide to the best data analytics and data science conferences in the world',
    'HERO_TITLE': 'DATA ANALYTICS CONFERENCES',
    'HERO_RANGE': '2026 &amp; 2027',
    'UPDATED_DATE': 'August 2026',
    'HERO_BG_URL': 'https://www.datalabsagency.com/wp-content/uploads/2026/08/london-data-analytics-imagery-dark.jpg',
    'HERO_BG_ID': '53680',
}
BAND = {
    'BAND_SUBTITLE': 'Where the world&rsquo;s data teams learn, hire and compare notes',
    'BAND_TITLE_LINE1': 'What are the Best Data Analytics',
    'BAND_TITLE_LINE2': '&amp; Data Science Conferences in 2026 &amp; 2027?',
}
INTRO = {
    'INTRO_COL1': f'''
{ARVO}This is my verified calendar of the <strong>best data analytics and data science conferences for 2026 and 2027</strong> &mdash; every date on this page was checked against the conference&rsquo;s own site this month, and the graveyard of events that quietly died since last year has been cleared out (details at the bottom).</span></p>
''',
    'INTRO_COL2': f'''
{ARVO}The spread is wider than ever: <strong>mega technical summits</strong> (Databricks, Snowflake), <strong>hands-on training conferences</strong> (ODSC), <strong>executive strategy events</strong> (Gartner, ANA), a free community <strong>unconference in 27 cities</strong> (MeasureCamp) &mdash; and the AI wave running through all of them. I&rsquo;ve marked who each event is actually for, so you spend the travel budget on the right room.</span></p>
''',
    'INTRO_COL3': f'''
{ARVO}{CANON} Conferences are where data teams sharpen the craft &mdash; and when the budget doesn&rsquo;t stretch to Las Vegas, an <a href="https://www.datalabsagency.com/data-visualization-training/">in-house workshop</a> brings the sharpening to your office instead.</span></p>
''',
}
INTRO['INTRO_LEADOUT'] = 'Here are <strong>my picks for the data analytics conferences of 2026 and 2027</strong>. &raquo;'
PICKS = {
    'PICKS_HEADING': 'What are the Biggest Data Analytics Conferences in the World?',
    'PICKS_SUBTITLE': 'My Top 4',
    'PICK1_IMAGE_ID': '37032', 'PICK1_LABEL': 'Biggest Technical Event', 'PICK1_NAME': 'Databricks Data + AI', 'PICK1_DETAIL': 'San Francisco, U.S.A.',
    'PICK2_IMAGE_ID': '37029', 'PICK2_LABEL': 'Best in Europe', 'PICK2_NAME': 'Big Data LDN', 'PICK2_DETAIL': 'London, England',
    'PICK3_IMAGE_ID': '37002', 'PICK3_LABEL': 'Best Hands-On Training', 'PICK3_NAME': 'ODSC AI', 'PICK3_DETAIL': 'San Francisco &amp; Boston',
    'PICK4_IMAGE_ID': '37038', 'PICK4_LABEL': 'Best Value', 'PICK4_NAME': 'MeasureCamp', 'PICK4_DETAIL': '27 cities worldwide',
}

E = lambda name, url, img, kick, dates, loc, body: {
    'EVENT_NAME': name, 'EVENT_URL': url, 'ENTRY_IMAGE_ID': img, 'EVENT_KICKER': kick,
    'EVENT_DATES': dates, 'EVENT_LOCATION': loc, 'EVENT_BODY': body}

EVENTS = [
('SEPTEMBER 2026', E('Disney Data &amp; Analytics Conference', 'https://disneydataconference.com/', '36915',
    'DDAC packs 2,500+ analytics people into Disney World, 14&ndash;16 September.',
    '14&ndash;16 September 2026', 'Orlando, U.S.A.',
    '''Do not let the Mickey ears fool you: <strong>DDAC</strong> draws <strong>2,500+ executives, managers and analysts from 250+ organisations</strong> for genuinely serious content on revenue management, pricing, forecasting and decision science. This year&rsquo;s confirmed keynotes include mathematician <strong>Matt Parker</strong> and machine-learning author <strong>Eric Siegel</strong>, alongside Disney and Coca-Cola practitioners. Registration is open, and it sells out &mdash; the venue is Disney&rsquo;s Coronado Springs Resort, which does no harm to the case for bringing the family.''')),
(None, E('dbt Summit 2026', 'https://www.getdbt.com/dbt-summit', '37023',
    'dbt Summit &mdash; the conference formerly known as Coalesce &mdash; hits Las Vegas 15&ndash;18 September.',
    '15&ndash;18 September 2026', 'Las Vegas, U.S.A. (hybrid)',
    '''New name, same tribe: <strong>Coalesce has rebranded as dbt Summit</strong> for 2026 as dbt broadens from analytics engineering into the AI-data mainstream. This is the home conference of the <strong>analytics engineering</strong> movement &mdash; the people who decide how your metrics get defined and shipped &mdash; live at The Cosmopolitan with a virtual option. If your team touches a modern data stack, someone from it should be in this room (or on this stream).''')),
(None, E('Gartner Data &amp; Analytics Summit Mumbai', 'https://www.gartner.com/en/conferences/apac/data-analytics-india', '26153',
    'Gartner&rsquo;s Mumbai summit runs 21&ndash;22 September &mdash; the last Gartner D&amp;A stop of 2026.',
    '21&ndash;22 September 2026', 'Mumbai, India',
    '''The final 2026 stop on <strong>Gartner&rsquo;s Data &amp; Analytics circuit</strong>, at the Grand Hyatt Mumbai. Gartner summits are <strong>strategy events for data leaders</strong> &mdash; analyst one-on-ones, governance and AI-roadmap content rather than hands-on technique. The 2027 series is already announced: <strong>Orlando (8&ndash;10 March)</strong>, <strong>London (10&ndash;12 May)</strong> and <strong>Sydney (7&ndash;8 June)</strong> &mdash; the Orlando edition gets its own entry below, and Australian readers will find Sydney covered in my <a href="https://www.datalabsagency.com/data-visualization-conferences/">data visualization conferences guide</a>.''')),
(None, E('Big Data LDN', 'https://www.bigdataldn.com/', '37029',
    'Big Data LDN fills Olympia London on 23&ndash;24 September &mdash; the UK&rsquo;s flagship data show.',
    '23&ndash;24 September 2026', 'London, England',
    '''My <strong>best-in-Europe pick</strong>. <strong>Big Data LDN</strong> takes over both the Grand and National halls at <strong>Olympia London</strong> &mdash; the UK&rsquo;s largest data, analytics and AI gathering, mixing a huge expo floor with a dense free conference programme. It is the rare big show where registration has historically cost nothing, which makes it the best value-per-airfare on the European calendar. If you can only do one European event in 2026, this is the one I&rsquo;d book.''')),
(None, E('DATA ANALYTICS 2026', 'https://www.iaria.org/conferences2026/DATAANALYTICS26.html', '37005',
    'DATA ANALYTICS 2026 runs in Barcelona from 27 September to 1 October, onsite or virtual.',
    '27 September &ndash; 1 October 2026', 'Barcelona, Spain (hybrid)',
    '''The academic option: the <strong>fifteenth IARIA conference</strong> on data analytics methodology, co-located with seven sibling conferences as the <strong>NexTech 2026 congress</strong>. Expect peer-reviewed papers and technical rigour rather than keynote theatre &mdash; you go to read the research and meet the researchers. The <strong>virtual participation option</strong> makes it the cheapest way on this list to sample the field&rsquo;s academic frontier from your desk.''')),
('OCTOBER 2026', E('Ai Everything Global', 'https://aieverythingglobal.com/home', '37053',
    'Ai Everything Global lands at ADNEC Abu Dhabi on 6&ndash;7 October.',
    '6&ndash;7 October 2026', 'Abu Dhabi, U.A.E.',
    '''The Gulf&rsquo;s government-backed AI mega-show has <strong>moved from Dubai to Abu Dhabi</strong>, rebranded as <strong>Ai Everything Global</strong> under organiser KAOUN. This is a <strong>deal-making event</strong> &mdash; investors, ministries, startups and enterprise buyers at national-strategy scale &mdash; rather than a practitioner conference. Go to understand where sovereign AI money is flowing (and there is a lot of it flowing through the UAE); bring business cards, not notebooks.''')),
(None, E('AI &amp; Big Data Expo Europe', 'https://www.ai-expo.net/global/', '37005',
    'AI &amp; Big Data Expo Europe returns to RAI Amsterdam on 19&ndash;20 October.',
    '19&ndash;20 October 2026', 'Amsterdam, Netherlands',
    '''<strong>AI &amp; Big Data Expo Europe</strong> is the European stop of the TechEx circuit at <strong>RAI Amsterdam</strong>, co-located with IoT, cyber-security and digital-transformation expos &mdash; one badge, five shows. It is vendor-heavy by design, which is exactly its use: comparing platforms and integrators side by side in an afternoon. The circuit&rsquo;s <strong>Global edition moves to Olympia London on 3&ndash;4 February 2027</strong>, and North America follows in San Jose on 16&ndash;17 June 2027.''')),
(None, E('ODSC AI West 2026', 'https://odsc.ai/west/', '37032',
    'ODSC AI West runs 27&ndash;29 October in the San Francisco Bay Area &mdash; the hands-on one.',
    '27&ndash;29 October 2026', 'Burlingame / San Francisco, U.S.A.',
    '''My <strong>best-for-training pick</strong>. ODSC (now rebranded <strong>ODSC AI</strong>) is built around workshops rather than keynotes &mdash; hands-on sessions on RAG pipelines, LLM orchestration and agentic AI that working data scientists can take back to their desks on Monday. West 2026 runs at the Hyatt Regency SF Airport in Burlingame; its sibling <strong>ODSC AI East returns to Boston in May 2027</strong>. If your goal is skills rather than networking, spend your money here.''')),
('NOVEMBER 2026', E('Machine Learning Week Europe', 'https://machinelearningweek.eu/', '37530',
    'Machine Learning Week Europe runs in Munich, 16&ndash;18 November.',
    '16&ndash;18 November 2026', 'Munich, Germany',
    '''&ldquo;Technical depth, practical lessons, no sales pitches&rdquo; is the promise <strong>Machine Learning Week Europe</strong> makes, and the format backs it up: a dedicated <strong>masterclass day</strong> (16 November) followed by two days of case studies with extended Q&amp;A. This is the European event for <strong>ML practitioners who ship models</strong> rather than talk about them &mdash; smaller and more focused than the expo circuit, and priced accordingly.''')),
(None, E('Big Data Conference Europe', 'https://bigdataconference.eu/', '52000',
    'Big Data Conference Europe runs in Vilnius, 24&ndash;27 November &mdash; onsite or online.',
    '24&ndash;27 November 2026', 'Vilnius, Lithuania (hybrid)',
    '''<strong>Big Data Conference Europe</strong> is four days in Vilnius at human scale: an onsite <strong>workshop day</strong> (24 November) then three hybrid conference days on big data, ML and AI at Forum Cinemas Vingis. No vendor-summit gloss, sensible Baltic pricing, and the <strong>online option</strong> covers the talks if the flight doesn&rsquo;t make sense from your part of the world. A good European bookend to the year for engineers and analysts.''')),
('FEBRUARY 2027', E('World AI Cannes Festival', 'https://waicf.com/', '37056',
    'WAICF brings applied AI to the Cannes Palais on 10&ndash;11 February 2027.',
    '10&ndash;11 February 2027', 'Cannes, France',
    '''Europe&rsquo;s glossiest AI event survives its change of ownership &mdash; now backed by Informa &mdash; and returns to the <strong>Palais des Festivals</strong>, trimmed to a sharper two days. <strong>WAICF</strong> is enterprise-AI showcase territory: big-brand case studies, strategy content and Riviera networking. It is not where you learn to build; it is where you take a stakeholder who needs to <em>believe</em>. February on the C&ocirc;te d&rsquo;Azur is, I am told, a hardship.''')),
(None, E('MIT Sloan Sports Analytics Conference', 'https://www.sloansportsconference.com/', '37146',
    'SSAC27 &mdash; the definitive sports analytics conference &mdash; runs in Boston, 25&ndash;26 February 2027.',
    '25&ndash;26 February 2027', 'Boston, U.S.A.',
    '''The conference <em>Moneyball</em> built. <strong>SSAC</strong> is where team executives, data scientists and media meet on how analytics and machine learning are changing sport &mdash; and its ideas leak into every other industry a season later. The 2027 edition is confirmed for Boston&rsquo;s Menino Convention Center. Even if you never touch sports data, the talks are a masterclass in <strong>making analytics persuasive to decision-makers</strong>, which is most of our job.''')),
('MARCH 2027', E('Gartner Data &amp; Analytics Summit Orlando', 'https://www.gartner.com/en/conferences/na/data-analytics-us', '36915',
    'Gartner&rsquo;s flagship D&amp;A summit runs in Orlando, 8&ndash;10 March 2027.',
    '8&ndash;10 March 2027', 'Orlando, U.S.A.',
    '''The biggest edition of <strong>Gartner&rsquo;s circuit</strong> and the annual weather-vane for <strong>data and analytics leadership</strong>: what CDAOs will be asked to do about AI, governance and data products this year, delivered with Gartner&rsquo;s research machine behind it. Analyst one-on-ones are the quiet superpower &mdash; book them the day registration opens. London follows on 10&ndash;12 May and Sydney on 7&ndash;8 June 2027.''')),
('APRIL 2027', E('ANA Masters of Data Conference', 'https://www.ana.net/conference/show/id/DATA-APR27', '36455',
    'ANA&rsquo;s Masters of Data returns to San Diego, 26&ndash;28 April 2027.',
    '26&ndash;28 April 2027', 'San Diego, U.S.A.',
    '''The marketing-analytics room: senior marketing and data executives on <strong>measurement, customer analytics and data accountability</strong>, run by the Association of National Advertisers at the Omni San Diego. With the former MADS conference now absorbed into Content Marketing World (see the note at the bottom of this page), <strong>ANA Masters of Data</strong> is the standalone event for the marketing end of the data spectrum.''')),
('MAY 2027', E('Data Summit 2027', 'https://www.dbta.com/DataSummit/', '37002',
    'DBTA&rsquo;s Data Summit runs in Boston, 12&ndash;13 May 2027.',
    '12&ndash;13 May 2027', 'Boston, U.S.A.',
    '''<strong>Data Summit</strong> is a compact, well-run two days from Database Trends and Applications at the Hyatt Regency Boston &mdash; data management, analytics and AI for practitioners at every level, without mega-summit sprawl. The early-bird pricing runs to 9 April 2027. Pair it with <strong>ODSC AI East</strong>, which brings its workshop-heavy programme back to Boston the same month &mdash; one flight, two very different conferences.''')),
(None, E('World Data Summit', 'https://worlddatasummit.com/', '36900',
    'World Data Summit&rsquo;s European edition is announced for Amsterdam, 20&ndash;21 May 2027.',
    'Announced for 20&ndash;21 May 2027', 'Amsterdam, Netherlands',
    '''<strong>World Data Summit</strong> is a mid-size European summit that goes deeper and quieter than the expo circuit: <strong>data strategy, data literacy, customer analytics and AI ethics</strong>, with a strong workshop tradition and a hybrid history. It now runs European and APAC editions; the Amsterdam dates are as announced at the time of writing &mdash; confirm on the official site before you book flights.''')),
(None, E('The Data Science Conference', 'https://www.thedatascienceconference.com/', '36915',
    'The Data Science Conference runs sponsor-free in Chicago, 27&ndash;28 May 2027.',
    '27&ndash;28 May 2027', 'Chicago, U.S.A.',
    '''<strong>The Data Science Conference</strong> is the contrarian of the calendar: <strong>no sponsors, no vendors, no recruiters</strong> &mdash; a rule it has kept since 2015. What is left when you remove the sales floor is two days of practitioners talking honestly at the University of Chicago&rsquo;s Gleacher Center, with a loyalty discount for returning attendees that tells you how many people come back. The purist&rsquo;s pick.''')),
('JUNE 2027', E('Snowflake Summit 2027', 'https://www.snowflake.com/en/summit/', '37032',
    'Snowflake Summit takes over Moscone Center on 7&ndash;10 June 2027.',
    '7&ndash;10 June 2027', 'San Francisco, U.S.A.',
    '''The warehouse-side counterweight to Databricks: <strong>Snowflake&rsquo;s summit</strong> has grown into one of the largest data events anywhere, filling Moscone with hundreds of sessions across the data-cloud ecosystem. If your stack lives on Snowflake &mdash; or you are deciding between the two platform giants &mdash; the fortnight of June 2027 in San Francisco settles it: Snowflake first, <strong>Databricks two weeks later in the same building</strong>.''')),
(None, E('Big Data &amp; Analytics Summit Canada', 'https://www.bigdatasummitcanada.com/', '37020',
    'Canada&rsquo;s big data summit marks its 12th year in Toronto, 8&ndash;9 June 2027.',
    '8&ndash;9 June 2027', 'Toronto, Canada (hybrid)',
    '''<strong>Big Data &amp; Analytics Summit Canada</strong> is the country&rsquo;s cross-industry data gathering, now in its twelfth year &mdash; real estate to manufacturing under one Toronto roof, with a <strong>hybrid option</strong> for remote attendance. It is deliberately broad rather than deep, which makes it a good first conference for analysts early in their careers, and interest registration for 2027 is already open.''')),
(None, E('Databricks Data + AI Summit 2027', 'https://www.databricks.com/dataaisummit', '37032',
    'Databricks&rsquo; Data + AI Summit fills three Moscone halls, 21&ndash;24 June 2027.',
    '21&ndash;24 June 2027', 'San Francisco, U.S.A. (hybrid)',
    '''My <strong>biggest-technical-event pick</strong>. The <strong>Data + AI Summit</strong> has outgrown everything around it &mdash; the 2027 edition is confirmed across <strong>Moscone North, West and South</strong>, with a virtual pass covering the keynotes and hundreds of sessions for those not making the trip. Lakehouse, governance, streaming, and whatever the AI platform war looks like by mid-2027: the sharpest technical programme in the industry, at overwhelming scale.''')),
('AUGUST 2027 &amp; YEAR-ROUND', E('Ai4 2027', 'https://ai4.io/', '37023',
    'Ai4 returns to the Venetian, Las Vegas in August 2027 &mdash; registration is already open.',
    'August 2027 (dates to be confirmed)', 'Las Vegas, U.S.A.',
    '''<strong>Ai4</strong> is one of North America&rsquo;s largest AI industry events, with a Vegas-appropriate sense of scale and past keynotes as big as <strong>Geoffrey Hinton</strong>. The 2026 edition wrapped in early August; 2027 registration is live at the Venetian, though exact dates were not confirmed at the time of writing &mdash; treat &ldquo;August 2027&rdquo; as the booking window and check the site before locking travel.''')),
(None, E('MeasureCamp', 'https://www.measurecamp.org/', '37038',
    'MeasureCamp runs free, community-built unconferences in 27 cities &mdash; including Australia.',
    'Rolling calendar, year-round', '27 cities worldwide',
    '''My <strong>best-value pick</strong>, at a price of zero. <strong>MeasureCamp</strong> is the digital-analytics community&rsquo;s <strong>free one-day unconference</strong>: no pre-booked speakers, an open session board, and anyone in the room can teach. Founded in 2012, it now runs in <strong>27 cities</strong> across Europe, North America, Asia, the Middle East &mdash; and Australia, which makes it the most accessible entry on this whole page for local readers. Watch the site for your city&rsquo;s date.''')),
]

OUTRO = {
    'OUTRO_HEADING': 'What Happened to the Other Analytics Conferences?',
    'OUTRO_BODY': '''Part of keeping this page honest is reporting the departures. Since the last update: <strong>RE-WORK&rsquo;s Deep Learning Summit</strong> is gone &mdash; the organiser has pivoted to executive CDAO and vertical AI events. <strong>Marketing Analytics &amp; Data Science (MADS)</strong> no longer exists as a standalone conference; it survives as a track inside Content Marketing World (Denver, 5&ndash;7 October 2026). <strong>VB Transform</strong> has become a small invite-curated affair, and <strong>INFORMS Analytics+</strong> has not yet announced a 2027 edition &mdash; its October 2027 Annual Meeting is the announced fallback for the operations-research crowd.

Know a conference that deserves a slot &mdash; especially an Australian one? <a href="https://www.datalabsagency.com/contact/">Contact me</a> and I&rsquo;ll verify it and add it. Chart people should see the sibling guide to <a href="https://www.datalabsagency.com/data-visualization-conferences/">data visualization conferences</a> &mdash; and if the travel budget is spent, a <a href="https://www.datalabsagency.com/data-visualisation-workshop-pricing/">data visualization workshop</a> brings the conference to your team instead.''',
}
FAQS = [
    ('What are the biggest data analytics conferences in 2026 and 2027?',
     'The mega technical events are Databricks Data + AI Summit (21&ndash;24 June 2027, San Francisco) and Snowflake Summit (7&ndash;10 June 2027, San Francisco), with Gartner&rsquo;s Data &amp; Analytics Summit series (Orlando, London, Sydney, Mumbai) the biggest on the strategy side and Big Data LDN (23&ndash;24 September 2026) the largest in Europe.'),
    ('Which data conferences can I attend free or cheaply?',
     'MeasureCamp is completely free &mdash; a community unconference running in 27 cities worldwide, including Australia. Big Data LDN has historically been free to attend, and several events on this page (Databricks, dbt Summit, Big Data Conference Europe, DATA ANALYTICS 2026) offer virtual passes far cheaper than travelling.'),
    ('Which conference is best for hands-on data science training?',
     'ODSC AI &mdash; West in the San Francisco Bay Area (27&ndash;29 October 2026) and East in Boston (May 2027). Its programme is built around workshops on RAG, LLM orchestration and agentic AI rather than keynotes. Machine Learning Week Europe in Munich (16&ndash;18 November 2026) is the strongest European equivalent.'),
    ('Are there data analytics conferences in Australia?',
     'The anchors are Gartner&rsquo;s Data &amp; Analytics Summit in Sydney (announced for 7&ndash;8 June 2027), CDAO Melbourne (1&ndash;2 September 2026), and free MeasureCamp unconferences. There is no Australian mega-summit yet &mdash; many local teams use in-house training to cover the gap between events.'),
]

page_faq = fill(blocks['faq'], {'FAQ_TOPIC': 'Data Analytics Conferences'})
for i, (q, a) in enumerate(FAQS, 1):
    page_faq = fill(page_faq, {f'FAQ_Q{i}': q, f'FAQ_A{i}': a, f'FAQ_TAB_ID_{i}': f'faqanconf-{i}-2026'})
clean = lambda t: re.sub(r'<[^>]+>', '', t).replace('&ndash;', '–').replace('&amp;', '&').replace('&rsquo;', '’').replace('&ldquo;', '“').replace('&rdquo;', '”').replace('"', '\\"')
jsonld = ('<script type="application/ld+json">{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ['
    + ', '.join('{"@type": "Question", "name": "%s", "acceptedAnswer": {"@type": "Answer", "text": "%s"}}' % (clean(q), clean(a)) for q, a in FAQS)
    + ']}</script>')
page_faq = fill(page_faq, {'FAQ_JSONLD_B64': base64.b64encode(urllib.parse.quote(jsonld, safe='').encode()).decode()})

parts = [fill(blocks['hero'], HERO), fill(blocks['band'], BAND), fill(blocks['intro'], INTRO), fill(blocks['picks'], PICKS)]
side = 0
for month, ev in EVENTS:
    if month:
        parts.append(fill(blocks['month'], {'MONTH_LABEL': month}))
    parts.append(fill(blocks['eventL'] if side % 2 == 0 else blocks['eventR'], {**ev, 'UTM_CAMPAIGN': UTM}))
    side += 1
parts += [fill(blocks['outro'], OUTRO), page_faq, blocks['footer']]
page = re.sub(r'<!--.*?-->', '', ''.join(parts), flags=re.S)
# collapse inter-row whitespace — stray text between rows becomes EMPTY FILLER ROWS
# on the first WPBakery save (16 of them appeared on 16173, 19 Aug 2026)
page = re.sub(r'\]\s+\[', '][', page.replace('\r\n', '\n'))
leftover = sorted(set(re.findall(r'\{\{([A-Z0-9_]+)(?::[^}]*)?\}\}', page)))
if leftover:
    sys.exit(f'ABORT — unfilled tokens: {leftover}')
OUT.write_text(page)
print(f'wrote {OUT} ({len(page)} chars, {len(EVENTS)} events)')
