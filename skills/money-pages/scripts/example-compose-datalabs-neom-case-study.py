#!/usr/bin/env python3
"""Compose the NEOM Visual Case Study — overnight batch, 25 Aug 2026.

Content: tier-1 reference, NEOM section. NDA: final dashboard designs and certain
details are under NDA — the page CARRIES THE CONFIDENTIALITY NOTE in copy, and the
three design images (53927/53930/53933) ride in the DRAFT for Otto's gate call:
⚠ HE MUST CONFIRM THEY ARE PUBLISHABLE before this page goes live. The banned
"120+ clients trained globally" claim is not used. Facts: NEOM Education District,
Saudi Arabia; Aug-Dec 2023 engagement, 7 weeks of delivery; three phases (training:
four workshops over two days on-site Dec 2023, 12 education staff, custom workbooks,
real NEOM data; co-design: requirements, personas, wireframing, IA, use cases;
data audit & implementation planning: sources, metric definitions, recommendations,
tech evaluation and roadmap); three-tier dashboard framework Leadership/School/Student;
initial design scope (enrolment, facility utilisation, attendance, intake projections,
applied-status tracking); audit scope; strategic deliverables incl. governance
guidelines and documented design decisions.
Interactive: the three-tier drill-down (Leadership -> School -> Student) animated.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from vcs_lib import *

blocks = kit_blocks()
OUT = '/private/tmp/claude-501/-Users-Ottinger-Claude-Projects-2026-project-manager-agent/1250d283-1a10-4416-b992-be81f96ce7a2/scratchpad/composed-neom.html'

hero = widen_hero(fill(blocks['intro'], {
    'PAGE_SUBTITLE': 'A visual case study&hellip;',
    'PAGE_TITLE': 'NEOM: Data Skills for a New City',
    'UPDATED_DATE': 'August 2026',
    'HOOK': 'In late 2023, the education district of <strong>NEOM</strong> &mdash; Saudi Arabia&rsquo;s new-city megaproject &mdash; needed its schools to run on data. The answer was <strong>four on-site workshops</strong>, a co-designed dashboard framework, and a <strong>full data audit</strong> &mdash; skills first, screens second.',
    'SECTION_A_SUBTITLE': 'The engagement in one paragraph',
    'SECTION_A_HEADING': 'What did the Datalabs Agency deliver for NEOM?',
    'SECTION_A_INTRO': 'Across August to December 2023, the <strong>Datalabs Agency</strong> ran a three-phase engagement for NEOM&rsquo;s Education District: <strong>four training workshops delivered on site</strong> over two days for 12 education staff, <strong>co-design sessions</strong> that produced a three-tier dashboard framework, and a <strong>data audit with implementation planning</strong> &mdash; metric definitions, governance guidelines, technology recommendations, and a roadmap. <em>Some project details and final dashboard designs remain confidential under NDA.</em>',
    'CANONICAL_SENTENCE': CANONICAL,
    'SECTION_B_SUBTITLE': 'The problem behind the brief',
    'SECTION_B_HEADING': 'Why does a brand-new school system need a data audit?',
    'SECTION_B_ANSWER': 'The animation above is the framework the co-design produced. The brief behind it: a school system being built from scratch has <strong>no legacy reports to lean on</strong> &mdash; and no legacy habits to unlearn. NEOM&rsquo;s education leadership wanted the data foundations designed deliberately: what to measure, who sees it, and at what altitude.',
    'SECTION_B_CONTEXT': 'That is a rarer and better starting point than it sounds. Most dashboard projects begin by untangling years of accumulated reporting; this one began with <strong>real questions and clean intent</strong> &mdash; enrolment and demographics, attendance patterns, facility utilisation, future intake projections. The engagement was sequenced so the people came first: train the team, co-design the framework with them, and only then audit the data sources and plan the build. Skills before screens is the whole philosophy, and a new city is the purest place to apply it.',
    'PRIMARY_CTA_TEXT': 'Plan your data foundations',
    'PRIMARY_CTA_URL': CONTACT,
}))
hero_p1, row_secB = split_hero(hero, 53927)

# ---------- Row: Animated Flow Diagram — the three-tier drill-down ----------
def svg_tiers():
    tiers = [
        ('LEADERSHIP DASHBOARD', 'District-level executive overview', 130),
        ('SCHOOL DASHBOARD', 'Individual school performance and operations', 300),
        ('STUDENT DASHBOARD', 'Student-level tracking and intervention support', 470),
    ]
    scopes = [
        ('Enrolment', 40), ('Attendance', 262), ('Facility utilisation', 484),
        ('Intake projections', 706), ('Applied status', 928),
    ]
    parts = [f'<svg viewBox="0 0 1200 640" xmlns="http://www.w3.org/2000/svg" role="img" '
             f'aria-label="The three-tier NEOM education dashboard framework: leadership, school, and student dashboards, fed by five measurement areas" '
             f'style="width:100%;height:auto;display:block;">']
    # measurement chips along the top
    for label, x in scopes:
        w = 200
        parts.append(f'<rect x="{x}" y="40" width="{w}" height="44" rx="22" fill="#262532" stroke="#4a4860" stroke-width="1.5"/>')
        parts.append(f'<text x="{x+w/2}" y="68" text-anchor="middle" font-family="{ARVO}" font-size="14" fill="#ffffff">{label}</text>')
        parts.append(flow_line(x + w / 2, 84, 600, 130, cx1=x + w / 2))
    # three tiers, widening as they drill down, staggered reveal
    widths = [420, 620, 820]
    for i, ((name, sub, y), w) in enumerate(zip(tiers, widths)):
        x = 600 - w / 2
        delay = round(0.5 + i * 0.7, 2)
        parts.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.7s" begin="{delay}s" fill="freeze"/>'
                     f'<rect x="{x}" y="{y}" width="{w}" height="110" rx="12" fill="#262532" stroke="{TAN}" stroke-width="{2.5 - i * 0.5}"/>'
                     f'<text x="600" y="{y+44}" text-anchor="middle" font-family="{BEBAS}" font-size="30" letter-spacing="2" fill="#ffffff">{name}</text>'
                     f'<text x="600" y="{y+74}" text-anchor="middle" font-family="{ARVO}" font-size="14" fill="#c39f76">{sub}</text></g>')
        if i < 2:
            parts.append(f'<path d="M 600 {y+110} L 600 {y+170}" fill="none" stroke="{TAN}" stroke-width="2" stroke-dasharray="6 8" opacity="0.85">{FLOW_ANIM}</path>')
            parts.append(f'<path d="M 592 {y+158} L 600 {y+168} L 608 {y+158}" fill="none" stroke="{TAN}" stroke-width="2"/>')
    parts.append(f'<text x="600" y="620" text-anchor="middle" font-family="{ARVO}" font-size="12" fill="#8a8a95">one measurement model, three altitudes &mdash; drill from district to a single student</text>')
    parts.append('</svg>')
    return ''.join(parts)

row_flow = svg_row('Watch the framework unfold', 'From district to a single student',
    'The co-design sessions produced a <strong>three-tier framework</strong>: one measurement model read at three altitudes, from the district overview down to individual intervention support.',
    svg_tiers())

# ---------- phases table ----------
t_phases = table_row(blocks, 'People, framework, foundations', 'The three-phase engagement',
    'The engagement structure, August to December 2023.',
    ['Phase', 'What happened'],
    [['1 &mdash; Training', 'Four workshops over two days, delivered on site in December 2023 &mdash; 12 education staff, hands-on exercises on real NEOM data, custom workbooks'],
     ['2 &mdash; Co-design', 'Dashboard planning with education leadership: requirements across user personas, wireframing, information architecture, use cases'],
     ['3 &mdash; Data audit &amp; planning', 'Assessment of data sources and structures, metric definition and documentation, technology evaluation, and an implementation roadmap']],
    footnote='Strategic deliverables included governance guidelines, skills recommendations, and documented design decisions with rationale.')

# ---------- gallery ----------
row_gallery = gallery_row('The design work, full size', 'From the drawing board',
    'Click either to view it full-screen. <em>Confidential details are limited to what the engagement record supports; final designs remain under NDA.</em>',
    [(53930, 'Dashboard Concepts', 'Early design exploration'),
     (53933, 'Enrolment Reporting', 'The report design layer')])

# ---------- Row: Design Principle Tiles — the six engagement components ----------
row_tiles = svg_row('Six moving parts', 'What the engagement was made of',
    'Four workshops and two consulting streams &mdash; each one a component NEOM keeps.',
    svg_tiles('The six components of the NEOM education engagement', [
        ('DATA VIZ &amp; STORYTELLING', 'Workshop 1: principles, audience, chart choice', 'charts'),
        ('INFOGRAPHICS &amp; REPORTS', 'Workshop 2: layout, colour, typography', 'doc'),
        ('CREATIVE PRESENTATIONS', 'Workshop 3: data slides beyond bullet points', 'layers'),
        ('STORYTELLING WITH DATA', 'Workshop 4: narrative arcs for executives', 'people'),
        ('CO-DESIGN SESSIONS', 'The dashboard framework, built together', 'target'),
        ('DATA AUDIT &amp; ROADMAP', 'Sources, metrics, governance, technology', 'grid'),
    ]))

# ---------- deliverables ----------
sec_deliver = widen_inner(fill(blocks['section2'], {
    'SECTION_D_SUBTITLE': 'Delivered, documented, taught',
    'SECTION_D_HEADING': 'What did NEOM receive at the end?',
    'SECTION_D_ANSWER': 'NEOM received <strong>12 trained education staff</strong> with custom workbooks, the <strong>three-tier dashboard framework</strong> with wireframes and use cases, a documented <strong>data audit</strong> spanning enrolment, academic performance, attendance, and resourcing, plus governance guidelines, technology recommendations, and a written implementation roadmap.',
    'SECTION_D_RATIONALE': 'For a system that is still being built, the roadmap matters more than any single screen. Every design decision shipped <strong>with its rationale documented</strong>, so the people who inherit the build &mdash; years from now, in a city that did not exist when the work was done &mdash; can see why each choice was made. That is what data foundations mean: decisions that outlive their meeting.',
}), '1/4', '1/2')

row_quote = quote_row('Otto Ottinger', 'The principle behind the NEOM engagement',
    'Build the skills before the dashboards &mdash; a data-literate team is the real infrastructure.')

row_faq = faq_row(blocks, 'The NEOM engagement', 'Ask about your data foundations', [
    ('What did the Datalabs Agency do for NEOM?',
     'A three-phase engagement for NEOM&rsquo;s Education District across August to December 2023: four on-site training workshops for 12 education staff, co-design sessions that produced a three-tier dashboard framework, and a data audit with implementation planning &mdash; metric definitions, governance guidelines, and a technology roadmap.'),
    ('What is the three-tier dashboard framework?',
     'One measurement model read at three altitudes: a Leadership Dashboard for the district-level executive view, a School Dashboard for individual school performance and operations, and a Student Dashboard for student-level tracking and intervention support. Initial designs covered enrolment, facility utilisation, attendance, intake projections, and applied-status tracking.'),
    ('What did the workshops cover?',
     'Four sessions over two days, on site: Introduction to Data Visualisation and Storytelling, Infographics and Report Design, Creative Data Presentations with PowerPoint, and Storytelling with Data. Each combined live instruction, hands-on exercises on real NEOM education data, group critique, and a custom workbook.'),
    ('Is the project confidential?',
     'Partly. The final dashboard designs and certain project details are under NDA, so this page describes the engagement structure and publicly shareable material only.'),
    ('Can the Datalabs Agency set up data foundations for our organisation?',
     'Yes. The NEOM shape &mdash; train the team, co-design the framework, audit the data, write the roadmap &mdash; works for any organisation building its reporting from a low base. Send a note through the contact form and we will reply with a phased outline.'),
])

art1 = fill(blocks['article1'], {
    'ARTICLE_1_SUBTITLE': 'Co-design earns its keep',
    'ARTICLE_1_HEADING': 'Why the framework was designed with NEOM, together',
    'ARTICLE_1_BODY': f'''{P}I could have designed a school-district dashboard framework from Melbourne and shipped it. It would have been wrong in a dozen quiet ways &mdash; because a <strong>new school system in a new city</strong> does not run like the systems the templates were learned from. Co-design exists for exactly this situation.</p>
{P}The sessions worked through <strong>user personas</strong> before screens: what a district leader needs on a Monday morning, what a school principal acts on weekly, what student-level intervention actually requires. Wireframes and <strong>information architecture</strong> came out of those conversations, not ahead of them, and every use case was NEOM&rsquo;s own.</p>
{P}The result was the <strong>three-tier framework</strong> &mdash; Leadership, School, Student &mdash; with a scope that started honest: enrolment (matriculated and non-matriculated), <strong>facility utilisation</strong> measured as available against occupied seats, attendance across grade levels, and future intake projections. No vanity metrics, because the people in the room would be the ones living with them.</p>
{P}Co-design is the same method behind our {LINK("/?page_id=661", "training workshops")} and every dashboard engagement we run: the client&rsquo;s knowledge is a design input, and the workshop is how you collect it.</p>''',
})
art2 = fill(blocks['article2'], {
    'ARTICLE_2_SUBTITLE': 'Foundations before furniture&hellip;',
    'ARTICLE_2_HEADING': 'Auditing data for a city that is still arriving',
    'ARTICLE_2_BODY': f'''{P}Phase three was the least glamorous and the most valuable: a <strong>data audit</strong> for a school system whose data was still taking shape. We assessed the sources and structures behind <strong>enrolment and demographics</strong>, academic performance, attendance patterns, behavioural incident tracking, <strong>teacher-student ratios</strong>, and resource allocation &mdash; and wrote down, metric by metric, what each one means and where it comes from.</p>
{P}Metric definition sounds bureaucratic until two reports disagree. When &ldquo;attendance&rdquo; is documented once &mdash; numerator, denominator, exclusions &mdash; the Leadership Dashboard and the Student Dashboard can never quietly diverge. That documentation, plus <strong>data governance guidelines</strong>, is what lets a growing organisation add reporting without re-arguing its arithmetic.</p>
{P}The engagement closed with a written <strong>implementation plan</strong>: technology evaluation and recommendations, a skills assessment with development recommendations for the team, and a roadmap for automated reporting. Deliberately, it is a plan NEOM&rsquo;s own people can execute &mdash; the workshops in phase one existed so the roadmap in phase three would have owners.</p>
{P}If your organisation is earlier in its data life than its ambitions, that sequence &mdash; skills, framework, audit, roadmap &mdash; is the one to copy. Our {LINK("https://www.datalabsagency.com/dashboard-design-services/", "dashboard design services")} page shows how we scope it.</p>''',
})

page = assemble([hero_p1, row_flow, row_secB, t_phases, row_gallery, row_tiles,
                 sec_deliver, row_quote, row_faq, art1, blocks['offers'], art2, blocks['fixed']])
page = apply_theme(page, '#16262a')  # per-page tint (Otto-approved palette, 25 Aug)
assert '120+' not in page
print('composed chars:', len(page))
import os, json, base64, urllib.request
pathlib.Path(OUT).write_text(page)
user, pw = os.environ['WP_DATALABS_USER'], os.environ['WP_DATALABS_APP_PASSWORD']
req = urllib.request.Request('https://www.datalabsagency.com/wp-json/wp/v2/pages/53936',
    data=json.dumps({'content': page, 'status': 'draft'}).encode(),
    headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
             'Authorization': 'Basic ' + base64.b64encode(f'{user}:{pw}'.encode()).decode()}, method='POST')
print('WP updated:', json.load(urllib.request.urlopen(req))['id'])
print('\nYOAST: SEO TITLE: NEOM Case Study: Education Data Foundations | Datalabs')
print("META DESCRIPTION: How the Datalabs Agency gave NEOM's education district its data foundations - on-site workshops, a co-designed three-tier dashboard framework, and a data audit.")
