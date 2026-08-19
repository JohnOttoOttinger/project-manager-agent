#!/usr/bin/env python3
"""Compose the Oddtoe 'Biggest Experiential Marketing & Activation Agencies' page
from design-kit-oddtoe-directory.html v1 (companies-only tailoring).

Composes against kit v2 (Otto-approved design, 19 Aug 2026). Entry tokens:
  ORG_SCALE_SENTENCE -> full-sentence scale kicker naming the agency
  ORG_OWNERSHIP      -> ownership ("Family-owned since 1927")
  ORG_HQ             -> HQ ("Dallas, Texas, U.S.A.")
  ENTRY_BODY         -> 60-150 word first-person why-listed copy

All agency facts verified 19 Aug 2026 (official sites + trade press; research log in
the session transcript). Images are Otto-approved interim art rotated from the
existing library — he replaces per agency before publish.
"""
import re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
KIT = (ROOT / 'skills/money-pages/references/design-kit-oddtoe-directory.html').read_text()
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path('composed-experiential-agencies.html')

markers = [
    ('hero',     '<!-- PAT-HERO'),
    ('band',     '<!-- PAT-HEADING-BAND'),
    ('intro',    '<!-- PAT-INTRO'),
    ('picks',    '<!-- PAT-TOP-PICKS'),
    ('featured', '<!-- PAT-ORG-FEATURED'),
    ('standard', '<!-- PAT-ORG-STANDARD '),
    ('standard_left', '<!-- PAT-ORG-STANDARD-IMG-LEFT'),
    ('outro',    '<!-- PAT-OUTRO'),
    ('promo',    '<!-- PAT-CROSS-PROMO'),
    ('announce', '<!-- PAT-ANNOUNCEMENT'),
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

UTM = 'experiential-agencies-guide'
ARVO = '<p class="p1"><span style="font-family: arvo, serif;">'

# Kit v2 (19 Aug 2026) carries the Otto-approved design baked in: dark wine rows,
# icon/name/ownership/HQ header stack, scale-sentence kicker, 60% band, gap 20.

HERO = {
    'HERO_KICKER': 'Your guide to the biggest experiential marketing agencies in the world',
    'HERO_TITLE': 'EXPERIENTIAL AGENCIES',
    'HERO_RANGE': '2026',
    'HERO_BG_URL': 'https://www.oddtoe.com/wp-content/uploads/2018/02/Oddtoe-Experiential-Artist-Cover.jpg',
    'HERO_BG_ID': '11129',
}
BAND = {
    'BAND_SUBTITLE': 'The agencies behind the world&rsquo;s biggest brand experiences',
    'BAND_TITLE_LINE1': 'Who are the Biggest Experiential Marketing',
    'BAND_TITLE_LINE2': '&amp; Brand Activation Agencies in the World?',
}
INTRO = {
    'INTRO_COL1': f'''
{ARVO}Planning a <strong>brand activation</strong> and wondering who the big players are? Benchmarking your own agency? Or hunting for a job in <strong>experiential marketing</strong>? Here is my guide to the <strong>biggest experiential marketing and activation agencies in the world</strong> &mdash; who owns them, how big they really are, and the work they are known for.</span></p>
{ARVO}And what a year to write it. The industry has been <strong>reshaped since late 2025</strong>: the <strong>Omnicom&ndash;IPG merger</strong> closed in November 2025 and immediately rearranged who owns whom.</span></p>
''',
    'INTRO_COL2': f'''
{ARVO}<strong>Jack Morton</strong> &mdash; an experiential name since 1939 &mdash; exited Omnicom in January 2026 and merged with <strong>Impact XM</strong> under private-equity backing. <strong>INVNT</strong> was acquired by Nth Degree in April 2026. Private equity is consolidating the sector fast, so any list written in 2024 is already wrong.</span></p>
{ARVO}The scale at the top is remarkable: the biggest player runs <strong>90+ locations</strong> and produces thousands of expositions a year, while <strong>Seoul&rsquo;s Cheil Worldwide</strong> puts 8,000-plus people behind experiential and retail work across 46 countries.</span></p>
''',
    'INTRO_COL3': f'''
{ARVO}Where do I fit in this picture? <strong>Oddtoe</strong> is an experiential design and generative-AI animation studio based in Melbourne, creating projection, installation, and animated work for events, venues, and galleries. Agencies of the size below don&rsquo;t need a rival &mdash; they need <strong>specialist studios</strong> for <a href="https://www.oddtoe.com/experiential-marketing/">experiential</a> content: projection, installation, and <strong>AI animation</strong>. That is the vantage point this list is written from.</span></p>
{ARVO}So here are <strong>my picks for the biggest experiential marketing &amp; activation agencies in the world</strong>. &raquo;</span></p>
''',
}
PICKS = {
    'PICKS_HEADING': 'Who are the Biggest Experiential Agencies in the World?',
    'PICKS_SUBTITLE': 'My Top 4',
    'PICK1_IMAGE_ID': '16174', 'PICK1_LABEL': 'Biggest Overall', 'PICK1_NAME': 'Freeman', 'PICK1_DETAIL': 'Dallas, U.S.A.',
    'PICK2_IMAGE_ID': '16175', 'PICK2_LABEL': 'Biggest Pure Specialist', 'PICK2_NAME': 'Jack Morton', 'PICK2_DETAIL': 'New York, U.S.A.',
    'PICK3_IMAGE_ID': '16187', 'PICK3_LABEL': 'Best for Tech Launches', 'PICK3_NAME': 'George P. Johnson', 'PICK3_DETAIL': 'Auburn Hills, U.S.A.',
    'PICK4_IMAGE_ID': '16179', 'PICK4_LABEL': 'Best Culture-Led', 'PICK4_NAME': 'Amplify', 'PICK4_DETAIL': 'London, England',
}

FEATURED = {
    'ORG_NAME': 'Freeman', 'ORG_URL': 'https://www.freeman.com', 'UTM_CAMPAIGN': UTM,
    'ENTRY_IMAGE_ID': '16174',
    'ORG_SCALE_SENTENCE': 'Freeman has 7,000+ people across 90+ locations.',
    'ORG_OWNERSHIP': 'Family-owned since 1927',
    'ORG_HQ': 'Dallas, Texas, U.S.A.',
    'ENTRY_BODY': '''If &ldquo;biggest&rdquo; is the question, Freeman is the answer. Advertising Age has recognised it as the <strong>world&rsquo;s largest brand experience company</strong>: more than <strong>7,000 people</strong> across <strong>90+ locations</strong>, producing over <strong>4,300 expositions a year</strong> plus thousands of other events. It has stayed <strong>family-owned since 1927</strong>, which in a year of private-equity consolidation makes it the industry&rsquo;s stable centre of gravity. Freeman is the infrastructure under America&rsquo;s biggest trade shows &mdash; think <strong>HIMSS</strong>, the giant global health conference &mdash; and in 2023 it bought award-magnet agency <strong>Sparks</strong> (below), adding a creative edge to all that muscle. If your brand experience needs a small city built by Tuesday, this is who builds it.''',
}

STANDARD = [
    {
        'ORG_NAME': 'Jack Morton', 'ORG_URL': 'https://www.jackmorton.com',
        'ENTRY_IMAGE_ID': '16175',
        'ORG_SCALE_SENTENCE': 'Jack Morton fields 1,000+ people across 20 offices.',
        'ORG_OWNERSHIP': 'Independent, private-equity backed',
        'ORG_HQ': 'New York, U.S.A.',
        'ENTRY_BODY': '''The biggest <strong>pure experiential specialist</strong> on this list &mdash; and the biggest story of 2026. Jack Morton has been making brand experiences since <strong>1939</strong> (it produced the <strong>Athens 2004 Olympic opening ceremony</strong>, the first outside producer in Olympic history). After the Omnicom&ndash;IPG merger closed, Omnicom let it go; in early 2026 it merged with <strong>Impact XM</strong> under The Riverside Company, creating a <strong>20-office, 1,000-plus-person</strong> network that is once again independent of the holding companies. Recent work includes <strong>Amazon at CES 2026</strong>. And a note for Australian readers: the office list includes <strong>Sydney and Melbourne</strong> &mdash; the biggest specialist in the world has people in my home town.''',
    },
    {
        'ORG_NAME': 'George P. Johnson (GPJ)', 'ORG_URL': 'https://www.gpj.com',
        'ENTRY_IMAGE_ID': '16187',
        'ORG_SCALE_SENTENCE': 'George P. Johnson runs 30 offices on six continents.',
        'ORG_OWNERSHIP': 'Employee-owned (Project Worldwide)',
        'ORG_HQ': 'Auburn Hills, Michigan, U.S.A.',
        'ENTRY_BODY': '''GPJ started in <strong>1914 as a Detroit flag maker</strong> and grew into the definitive <strong>tech-launch and B2B flagship-event agency</strong>: <strong>AMD&rsquo;s CES keynote</strong>, and long-standing programmes for <strong>IBM, Cisco, Salesforce and Mercedes-Benz</strong>. It runs <strong>30 offices on six continents</strong> &mdash; Sydney included &mdash; and sits inside <strong>Project Worldwide</strong>, an <strong>employee-owned</strong> agency network, so the century-old shop dodged the 2025&ndash;26 holding-company shake-up entirely. If you are launching enterprise technology and the room has to be full of the right ten thousand people, GPJ has probably already built that room somewhere on Earth this month.''',
    },
    {
        'ORG_NAME': 'Momentum Worldwide', 'ORG_URL': 'https://www.momentumww.com',
        'ENTRY_IMAGE_ID': '16177',
        'ORG_SCALE_SENTENCE': 'Momentum Worldwide is Experiential Agency of the Year three years running.',
        'ORG_OWNERSHIP': 'Part of Omnicom',
        'ORG_HQ': 'New York, U.S.A.',
        'ENTRY_BODY': '''The strongest awards case in the business: Campaign US named Momentum <strong>Experiential Agency of the Year in 2024, 2025 and 2026</strong> &mdash; a three-peat, the third confirmed in March 2026. Formerly IPG&rsquo;s experiential flagship, it now carries that flag inside <strong>Omnicom</strong> after the merger. The work runs from big consumer culture plays like the <strong>Sprite x Wakanda</strong> activation to a dedicated B2B practice it calls <strong>&ldquo;Business2Human&rdquo;</strong>, out of offices from New York and London to Tokyo and <strong>Sydney</strong>. If you want holding-company reach with the trophy shelf to match, this is the pick.''',
    },
    {
        'ORG_NAME': 'Sparks', 'ORG_URL': 'https://wearesparks.com',
        'ENTRY_IMAGE_ID': '16178',
        'ORG_SCALE_SENTENCE': 'Sparks (est. 1919) is Adweek&rsquo;s 2024 Experiential Agency of the Year.',
        'ORG_OWNERSHIP': 'A Freeman Company',
        'ORG_HQ': 'Philadelphia, Pennsylvania, U.S.A.',
        'ENTRY_BODY': '''Sparks is what happens when a century-old Philadelphia shop (est. <strong>1919</strong>) becomes the creative tip of the world&rsquo;s largest brand experience company &mdash; <strong>Freeman acquired it in August 2023</strong>, and the client roster barely blinked. Adweek named it <strong>2024 Experiential Agency of the Year</strong>, and the 2026 slate shows why: <strong>Salesforce Beach at Cannes Lions</strong>, <strong>Google Cloud Next</strong>, and work on <strong>Netflix House</strong>. Around 750 people joined Freeman with the acquisition. For premium tech-brand environments &mdash; the kind where the espresso bar is on-message &mdash; Sparks is the name that keeps coming up.''',
    },
    {
        'ORG_NAME': 'Imagination', 'ORG_URL': 'https://imagination.com',
        'ENTRY_IMAGE_ID': '16184',
        'ORG_SCALE_SENTENCE': 'Imagination runs 13 studios worldwide.',
        'ORG_OWNERSHIP': 'Independent since 1968',
        'ORG_HQ': 'London, England',
        'ENTRY_BODY': '''London&rsquo;s grand independent. Imagination has been designing experiences since <strong>1968</strong> &mdash; before &ldquo;experiential marketing&rdquo; had a name &mdash; and still answers to nobody but itself, with <strong>13 studios worldwide</strong> including Los Angeles. It is known for decades of <strong>global experience programmes for Ford</strong>, plus work for <strong>Major League Baseball and Jaguar Land Rover</strong>. In a sector now dominated by holding companies and private equity, a 57-year-old independent with this footprint is a genuine rarity &mdash; and for brands that want experience design with a capital-D design culture, it remains the benchmark European choice.''',
    },
    {
        'ORG_NAME': 'Amplify', 'ORG_URL': 'https://www.weareamplify.com',
        'ENTRY_IMAGE_ID': '16179',
        'ORG_SCALE_SENTENCE': 'Amplify is Campaign&rsquo;s Brand Experience Agency of the Decade.',
        'ORG_OWNERSHIP': 'Part of Common Interest',
        'ORG_HQ': 'London, England',
        'ENTRY_BODY': '''Campaign didn&rsquo;t just give Amplify agency of the year &mdash; it named it <strong>Brand Experience Agency of the Decade</strong>. Founded in London in 2008 by Jonathan Emmins, it now runs offices in <strong>Paris, Los Angeles, New York and Sydney</strong>, and in April 2025 sold a majority stake to Anthony Freedman&rsquo;s <strong>Common Interest</strong> group. The work is culture-first: <strong>Nike Air Max Day</strong>, Netflix&rsquo;s <strong>La Casa de Papel</strong> campaign, Samsung&rsquo;s <strong>&ldquo;Space to Dream&rdquo;</strong>. It is also <strong>B Corp certified</strong>. If the brief says &ldquo;make us matter in popular culture&rdquo; rather than &ldquo;fill a convention centre&rdquo;, this is my pick.''',
    },
    {
        'ORG_NAME': 'Cheil Worldwide', 'ORG_URL': 'https://www.cheil.com',
        'ENTRY_IMAGE_ID': '16185',
        'ORG_SCALE_SENTENCE': 'Cheil Worldwide has 8,000+ people in 55 offices across 46 countries.',
        'ORG_OWNERSHIP': 'Samsung Group affiliate',
        'ORG_HQ': 'Seoul, South Korea',
        'ENTRY_BODY': '''The giant of the East. Seoul-based Cheil puts <strong>8,000-plus people in 55 offices across 46 countries</strong>, and much of that machine exists to build <strong>Samsung&rsquo;s retail, launch and experiential presence</strong> around the planet &mdash; every flagship store and product-launch experience feeding one of the most demanding brand programmes anywhere. Cheil is publicly listed, ranks among the world&rsquo;s largest agency networks, and its retail and experiential practice has been one of its growth engines through 2024&ndash;25. On raw experiential headcount and geographic reach, only Freeman keeps it company on this list.''',
    },
    {
        'ORG_NAME': 'Opus Agency', 'ORG_URL': 'https://www.opusagency.com',
        'ENTRY_IMAGE_ID': '16186',
        'ORG_SCALE_SENTENCE': 'Opus Agency fields 450+ people from hubs on three continents.',
        'ORG_OWNERSHIP': 'The Opus Group',
        'ORG_HQ': 'Beaverton, Oregon, U.S.A.',
        'ENTRY_BODY': '''If you have been to a big cloud-software event, you have probably walked through Opus&rsquo;s work: the <strong>Salesforce World Tour</strong> multi-city series, the <strong>AWS Summit ASEAN</strong> events in Singapore, Bangkok and Jakarta, and <strong>NetApp INSIGHT</strong> in Las Vegas. Founded in 1993 and headquartered near Portland, Oregon, the agency runs <strong>450-plus people</strong> with hubs in EMEA and APAC, inside The Opus Group under private-equity owner Growth Catalyst Partners. It has been buying its way across the Pacific too, acquiring APAC event shop <strong>The Company We Keep</strong>. The specialty: repeatable, global, tech-flagship event programmes at serious scale.''',
    },
    {
        'ORG_NAME': 'NVE Experience Agency', 'ORG_URL': 'https://experiencenve.com',
        'ENTRY_IMAGE_ID': '16181',
        'ORG_SCALE_SENTENCE': 'NVE produces 150+ events a year with 200+ people.',
        'ORG_OWNERSHIP': 'Independent, founder-owned',
        'ORG_HQ': 'Los Angeles, California, U.S.A.',
        'ENTRY_BODY': '''The Hollywood one. Brett Hyman founded NVE in <strong>2005</strong>, took no outside investment, and built a <strong>200-plus-person</strong> agency producing <strong>more than 150 events a year</strong> from Los Angeles, New York and London. Its roots are entertainment-industry premieres and culturally-tuned launches, and the client work spans <strong>Amazon, Apple, PlayStation and Hennessy</strong>. Event Marketer put it on the <strong>2025 It List</strong> of the top event agencies. Among giants owned by holding companies and private equity, NVE is proof a founder-owned independent can still sit at the big table &mdash; the trade-off is focus: cultural moments, not convention centres.''',
    },
    {
        'ORG_NAME': 'INVNT', 'ORG_URL': 'https://www.invnt.com',
        'ENTRY_IMAGE_ID': '16182',
        'ORG_SCALE_SENTENCE': 'INVNT has 11 offices across four continents.',
        'ORG_OWNERSHIP': 'Part of Nth Degree',
        'ORG_HQ': 'New York, U.S.A.',
        'ENTRY_BODY': '''The live-brand-storytelling agency &mdash; and 2026&rsquo;s other big consolidation story. In <strong>April 2026</strong> INVNT was acquired by <strong>Nth Degree</strong>, the Shamrock Capital-backed events group, with co-founder <strong>Kristina McCoobery</strong> leading the combined events agency and the INVNT name staying on the corporate-events work. It brings <strong>11 offices across North America, Europe, the Middle East and Asia-Pacific</strong>, and &mdash; relevant from where I sit &mdash; one of the stronger <strong>Australian and APAC footprints</strong> of any agency on this list. Watch this one: the private-equity consolidation it is part of is redrawing the sector&rsquo;s whole map.''',
    },
    {
        'ORG_NAME': 'DRPG', 'ORG_URL': 'https://www.drpgroup.com',
        'ENTRY_IMAGE_ID': '16183',
        'ORG_SCALE_SENTENCE': 'DRPG has 300+ people and has been founder-led since 1980.',
        'ORG_OWNERSHIP': 'Independent',
        'ORG_HQ': 'Worcestershire, England',
        'ENTRY_BODY': '''The quiet achiever. Dale Parmenter started DRPG as a <strong>one-man operation in 1980</strong> and still runs it today &mdash; now <strong>300-plus people</strong> across the UK plus offices in the U.S. and Germany, delivering integrated events, film and communications for <strong>Tesco, BT, GSK and Nationwide</strong>. It is <strong>B Corp certified</strong> and has a particular strength the flashier shops overlook: <strong>large-scale employee experiences</strong> &mdash; the town halls, launches and internal events where big organisations actually talk to their own people. Forty-six years founder-led, no holding company, no private equity. There&rsquo;s something to respect in that.''',
    },
]

OUTRO = {
    'OUTRO_HEADING': 'What Other Experiential Agencies Are Worth Mentioning?',
    'OUTRO_BODY': '''This sector is consolidating so fast that some famous names now live inside other companies &mdash; Impact XM is part of Jack Morton, Giant Spoon sits inside Wpromote, and sports-experiential powerhouse Octagon works within Omnicom. Am I missing an agency you rate? <a href="/?page_id=176">Contact me</a> and make the case &mdash; I&rsquo;ll keep this list current through 2026 and 2027.

And if you are planning an activation of your own &mdash; whatever its size &mdash; start with my guide to <a href="https://www.oddtoe.com/brand-activation-ideas/">brand activation ideas</a>, or see how <a href="https://www.oddtoe.com/experiential-marketing/">experiential marketing</a> works when a specialist studio builds the projection, installation and animated content. Animators looking for representation should head to my list of the <a href="https://www.oddtoe.com/animation-agents/">best animation agents</a>.''',
}

page = (
    # PAT-PAGE-LINK-CSS is prepended AFTER the draft exists (needs the page id).
    fill(blocks['hero'], HERO)
    + fill(blocks['band'], BAND)
    + fill(blocks['intro'], INTRO)
    + fill(blocks['picks'], PICKS)
    + fill(blocks['featured'], {**FEATURED, 'UTM_CAMPAIGN': UTM})
    # Alternation rule (Otto, 19 Aug 2026): featured is image-left, then entries alternate
    # image-right / image-left strictly down the page.
    + ''.join(fill(blocks['standard_left' if i % 2 else 'standard'], {**d, 'UTM_CAMPAIGN': UTM})
              for i, d in enumerate(STANDARD))
    + fill(blocks['outro'], OUTRO)
    + blocks['promo']
    + blocks['announce']
)
page = strip_comments(page)


# collapse inter-row whitespace — stray text between rows becomes EMPTY FILLER ROWS
# on the first WPBakery save (16 of them appeared on 16173, 19 Aug 2026)
page = re.sub(r'\]\s+\[', '][', page.replace('\r\n', '\n'))
leftover = sorted(set(re.findall(r'\{\{([A-Z0-9_]+)(?::[^}]*)?\}\}', page)))
if leftover:
    sys.exit(f'ABORT — unfilled tokens: {leftover}')
OUT.write_text(page)
print(f'wrote {OUT} ({len(page)} chars)')
