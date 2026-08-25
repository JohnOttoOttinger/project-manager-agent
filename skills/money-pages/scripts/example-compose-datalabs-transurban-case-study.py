#!/usr/bin/env python3
"""Compose the Transurban Visual Case Study — overnight batch, 25 Aug 2026.

Content: transurban-case-study.md (full standalone draft). Verification queue honoured:
NO usage/outcome claims (nothing was measured — capability language only); dates stay
approximate ("mid-2017, roughly three months"); role split stated honestly (Otto
project-managed and led design; a development team built it — team unattributed, so
credited generically); screen data is INDICATIVE and said so on-page; the site is no
longer in service and the page says so plainly (trust signal). No named client contact.
Facts: Transurban Strategy team; Road Usage Cost Calculator at roadusagecalculator.com
(retired); HTML/CSS/JS client-side app; three input modes (Quick / Detailed / CSV);
RUC rate slider; three cost perspectives (fleet / vehicle / km); comparative charts,
trajectory lines, registration donuts, savings highlighted green; data covering 8
states/territories, registration categories (rural/metro/outer-metro/older vehicles),
fuel types and excise, vehicle specs.
Media: 53938 landing (hero), 53941 input methods, 53944 quick mode, 53947 results
(hotspot), 53950 per-car breakdown, 53953 CSV import.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from vcs_lib import *

blocks = kit_blocks()
OUT = '/private/tmp/claude-501/-Users-Ottinger-Claude-Projects-2026-project-manager-agent/1250d283-1a10-4416-b992-be81f96ce7a2/scratchpad/composed-transurban.html'

hero = widen_hero(fill(blocks['intro'], {
    'PAGE_SUBTITLE': 'A visual case study&hellip;',
    'PAGE_TITLE': 'Transurban: The Road Usage Calculator',
    'UPDATED_DATE': 'August 2026',
    'HOOK': 'In mid-2017, Transurban&rsquo;s Strategy team was researching a hard policy question: what happens to road funding as fuel excise fades? Over roughly three months, I project-managed and design-led a <strong>public interactive calculator</strong> that let anyone model current charges against a <strong>distance-based road usage charge</strong> &mdash; for a single car or an entire fleet.',
    'SECTION_A_SUBTITLE': 'The project in one paragraph',
    'SECTION_A_HEADING': 'What did the Datalabs Agency build for Transurban?',
    'SECTION_A_INTRO': 'The <strong>Road Usage Cost Calculator</strong> was a client-side web application &mdash; HTML, CSS, and JavaScript &mdash; launched publicly at roadusagecalculator.com. It modelled current road funding charges against a proposed <strong>Road Usage Charge</strong> across every Australian state and territory, with <strong>three ways in</strong>: a quick mode, a vehicle-by-vehicle detailed mode, and CSV import for whole fleets. Our role: project management and design lead, with a development team building the application.',
    'CANONICAL_SENTENCE': CANONICAL,
    'SECTION_B_SUBTITLE': 'The problem behind the brief',
    'SECTION_B_HEADING': 'Why did a road policy debate need an interactive tool?',
    'SECTION_B_ANSWER': 'The animation above is the tool&rsquo;s logic. The policy problem behind it: Australia funds roads largely through <strong>fuel excise</strong>, and as the fleet shifts to fuel-efficient and electric vehicles, that revenue declines. A <strong>Road Usage Charge</strong> &mdash; paying for distance travelled instead of fuel burned &mdash; affects every vehicle type, state, and registration category differently. Abstract argument was never going to settle it.',
    'SECTION_B_CONTEXT': 'Transurban&rsquo;s Strategy team wanted stakeholders to <strong>model the scenarios themselves</strong>: their own fleet, their own state, their own annual kilometres, against an adjustable per-kilometre rate. An interactive tool turns a policy abstraction into a number on your own household or fleet &mdash; and a debate about a number you can see is a better debate. The calculator shipped with an educational landing page explaining the funding structure, so the context travelled with the tool.',
    'PRIMARY_CTA_TEXT': 'Talk interactive tools with us',
    'PRIMARY_CTA_URL': CONTACT,
}))
hero_p1, row_secB = split_hero(hero, 53938)

# ---------- Row: Animated Flow Diagram — three ways in, three cost lenses out ----------
def svg_calc():
    modes = [('QUICK MODE', 'Fleet parameters and sliders'),
             ('DETAILED MODE', 'Vehicle-by-vehicle entry'),
             ('CSV IMPORT', 'Whole fleets, one upload')]
    lenses = [('TOTAL FLEET', 'The whole-of-fleet annual picture'),
              ('PER VEHICLE', 'What each car pays, both systems'),
              ('PER KILOMETRE', 'The rate the debate turns on')]
    parts = [f'<svg viewBox="0 0 1200 640" xmlns="http://www.w3.org/2000/svg" role="img" '
             f'aria-label="Three input modes feeding the Road Usage Cost Calculator, producing three cost perspectives" '
             f'style="width:100%;height:auto;display:block;">']
    ys = [80, 260, 440]
    for (name, sub), y in zip(modes, ys):
        parts.append(f'<rect x="40" y="{y}" width="280" height="96" rx="10" fill="#262532" stroke="#4a4860" stroke-width="1.5"/>')
        parts.append(f'<text x="64" y="{y+38}" font-family="{BEBAS}" font-size="24" letter-spacing="1.5" fill="#ffffff">{name}</text>')
        parts.append(f'<text x="64" y="{y+64}" font-family="{ARVO}" font-size="13" fill="#8a8a95">{sub}</text>')
        parts.append(flow_line(320, y + 48, 492, 320, cx1=410))
    # calculator hub with slider glyph
    parts.append(f'<circle cx="600" cy="320" r="108" fill="#1f1e29" stroke="{TAN}" stroke-width="2.5"/>')
    parts.append(f'<circle cx="600" cy="320" r="122" fill="none" stroke="{TAN}" stroke-width="1" opacity="0.35" stroke-dasharray="3 7"/>')
    parts.append(f'<text x="600" y="292" text-anchor="middle" font-family="{BEBAS}" font-size="26" letter-spacing="1.5" fill="#ffffff">RUC RATE</text>')
    # animated slider: track + moving knob
    parts.append(f'<line x1="530" y1="322" x2="670" y2="322" stroke="#4a4860" stroke-width="6" stroke-linecap="round"/>')
    parts.append(f'<line x1="530" y1="322" x2="610" y2="322" stroke="{TAN}" stroke-width="6" stroke-linecap="round"/>')
    parts.append(f'<circle cy="322" r="11" fill="{TAN}"><animate attributeName="cx" values="545;655;545" dur="6s" repeatCount="indefinite"/></circle>')
    parts.append(f'<text x="600" y="362" text-anchor="middle" font-family="{ARVO}" font-size="13" fill="#ffffff">cents per kilometre</text>')
    parts.append(f'<text x="600" y="384" text-anchor="middle" font-family="{ARVO}" font-size="11" fill="#8a8a95">adjust it, watch every chart move</text>')
    for j, ((name, sub), y) in enumerate(zip(lenses, ys)):
        parts.append(flow_line(708, 320, 880, y + 48, cx1=790))
        parts.append(f'<rect x="880" y="{y}" width="280" height="96" rx="10" fill="#262532" stroke="{TAN}" stroke-width="1.5"/>')
        parts.append(f'<text x="904" y="{y+38}" font-family="{BEBAS}" font-size="24" letter-spacing="1.5" fill="#ffffff">{name}</text>')
        parts.append(f'<text x="904" y="{y+64}" font-family="{ARVO}" font-size="13" fill="#c39f76">{sub}</text>')
    parts.append('</svg>')
    return ''.join(parts)

row_flow = svg_row('Watch the slider drive it', 'Three ways in, three cost lenses out',
    'Any input mode, one adjustable <strong>per-kilometre rate</strong>, and every scenario lands as fleet, vehicle, and per-km numbers side by side.',
    svg_calc())

# ---------- modes table ----------
t_modes = table_row(blocks, 'Meet users where their data is', 'The three input modes',
    'Each mode served a different user with a different amount of data on hand.',
    ['Mode', 'Built for', 'What you enter'],
    [['Quick', 'Anyone exploring the policy', 'Fleet size, vehicle and fuel type mix, registration costs, average annual kilometres'],
     ['Detailed', 'Analysts and fleet owners', 'Each vehicle&rsquo;s make, model, year, state, fuel type, and annual distance'],
     ['CSV import', 'Large fleet operators', 'A bulk upload against a downloadable template']],
    footnote='All modes fed the same comparison engine: current charges (fuel excise plus registration) against the modelled Road Usage Charge.')

# ---------- gallery ----------
row_gallery = gallery_row('The tool itself, full size', 'Inside the calculator',
    'Click any screen to view it full-size. All figures shown are <strong>indicative modelling data</strong>, not real fleet costs.',
    [(53941, 'Choose Your Way In', 'The three input methods'),
     (53944, 'Quick Mode', 'Sliders for rapid scenarios'),
     (53950, 'Per-Car Breakdown', 'Every vehicle, both systems'),
     (53953, 'CSV Import', 'Whole fleets in one upload')])

# ---------- hotspot on the results view ----------
row_hotspot = hotspot_row('Click the markers', 'Read the results screen',
    'The main results view, annotated &mdash; five markers explain how a scenario reads. Figures are indicative.',
    53947, [
        (8, 40, 'The vehicle rail', 'The fleet being modelled - each vehicle with its state, registration category, and fuel type.'),
        (38, 28, 'The RUC rate slider', 'The heart of the tool: drag the cents-per-kilometre rate and every number on screen recalculates.'),
        (44, 45, 'Current vs RUC', 'Side-by-side bars - fuel excise plus registration today, against the modelled road usage charge. Savings show green.'),
        (42, 72, 'Registration breakdown', 'Donut charts splitting registration by state and category - where the current system is heaviest.'),
        (75, 55, 'The cost trajectory', 'Costs projected across increasing annual distance, so the crossover point is visible at a glance.'),
    ])

# ---------- Row: Design Principle Tiles ----------
row_tiles = svg_row('The rules under the tool', 'The design principles behind the calculator',
    'Six decisions that made a policy instrument feel like a consumer product.',
    svg_tiles('The six design principles behind the Transurban Road Usage Cost Calculator', [
        ('ONE MOVING PART', 'A single rate slider drives every chart', 'target'),
        ('THREE COST LENSES', 'Fleet, per vehicle, and per kilometre', 'layers'),
        ('EIGHT JURISDICTIONS', 'Every state and territory rule encoded', 'grid'),
        ('SAVINGS IN GREEN', 'Cost differences colour-coded instantly', 'swatches'),
        ('CONTEXT FIRST', 'A landing page that explains the policy', 'doc'),
        ('START ROUGH, GO DEEP', 'Quick mode invites, detailed mode proves', 'charts'),
    ]))

# ---------- deliverables ----------
sec_deliver = widen_inner(fill(blocks['section2'], {
    'SECTION_D_SUBTITLE': 'Delivered and shipped public',
    'SECTION_D_HEADING': 'What did Transurban receive at the end?',
    'SECTION_D_ANSWER': 'A fully functional public calculator at roadusagecalculator.com: <strong>real-time comparison</strong> of current charges against a Road Usage Charge, an adjustable per-kilometre rate, three cost perspectives, comparative and trajectory charts, per-vehicle tables, and an educational landing page &mdash; covering <strong>all eight Australian states and territories</strong>.',
    'SECTION_D_RATIONALE': 'The tool has since been retired from service, which this page states plainly &mdash; policy instruments have seasons. What it demonstrated stands: multi-variable cost comparison made <strong>accessible to non-technical stakeholders</strong>, and a funding debate given a shared, checkable model. The hard work was invisible: registration rules across eight jurisdictions and four categories, fuel classifications, and excise rates &mdash; correct in <strong>every combination</strong>.',
}), '1/4', '1/2')

row_quote = quote_row('Otto Ottinger', 'The principle behind the calculator',
    'A policy debate improves the moment the public can poke at the numbers themselves.')

row_faq = faq_row(blocks, 'The Transurban project', 'Ask about your data tool', [
    ('What was the Road Usage Cost Calculator?',
     'A public interactive web tool built for Transurban&rsquo;s Strategy team in mid-2017, letting anyone model current Australian road funding charges &mdash; fuel excise plus registration &mdash; against a proposed distance-based Road Usage Charge, for a single vehicle or a whole fleet. It launched at roadusagecalculator.com and has since been retired.'),
    ('What was the Datalabs Agency&rsquo;s role?',
     'Project management and design lead: stakeholder and requirements management with the Strategy team, the data design sessions that structured the cost calculations, user flows, and testing oversight. A development team built the application itself in HTML, CSS, and JavaScript.'),
    ('What could the calculator model?',
     'Vehicle registration costs across all eight Australian states and territories, four registration categories including rural and metropolitan variations, fuel types and excise rates, and vehicle specifications down to make, model, and year &mdash; compared in real time against an adjustable per-kilometre road usage rate.'),
    ('Why did the data design matter so much?',
     'Because the rules differ by state and registration category, and the calculator had to be right in every combination. Extended data design and cleansing sessions structured those multi-dimensional rules before a single screen was built &mdash; the accuracy of every scenario depended on them.'),
    ('Can the Datalabs Agency build an interactive tool for my organisation?',
     'Yes. Public calculators, explorable models, and interactive data products are a core service alongside dashboards &mdash; the same design discipline, pointed at a wider audience. Send your idea through the contact form and we will reply with an approach and scope.'),
])

art1 = fill(blocks['article1'], {
    'ARTICLE_1_SUBTITLE': 'Invite first, prove later',
    'ARTICLE_1_HEADING': 'Designing a calculator the public can argue with',
    'ARTICLE_1_BODY': f'''{P}A policy tool has two audiences that want opposite things. A curious member of the public wants an answer in <strong>ninety seconds</strong>; a fleet analyst wants to model four hundred vehicles precisely. Serve only the first and the tool is a toy; only the second and nobody opens it.</p>
{P}The calculator&rsquo;s answer was <strong>three doors into one engine</strong>. Quick mode asked for a handful of sliders &mdash; fleet size, vehicle mix, average kilometres &mdash; and produced a defensible first answer fast. Detailed mode let a user specify every vehicle down to <strong>make, model, year, and state</strong>. CSV import took an entire fleet in one upload, against a template the tool itself provided.</p>
{P}The output design carried the argument. Current charges and the modelled <strong>Road Usage Charge sat side by side</strong>, with differences colour-coded and savings in green; a trajectory chart projected both across rising annual distance so the crossover point was visible; and three cost lenses &mdash; <strong>fleet, vehicle, kilometre</strong> &mdash; meant every stakeholder found the number they think in.</p>
{P}Interactivity is our craft in every format &mdash; see the {LINK("/?page_id=415", "interactive data visualizations")} we design &mdash; but a public policy tool is its sharpest use: the audience does not read the analysis, they <strong>drive it</strong>.</p>''',
})
art2 = fill(blocks['article2'], {
    'ARTICLE_2_SUBTITLE': 'Eight jurisdictions, no shortcuts&hellip;',
    'ARTICLE_2_HEADING': 'The data governance under a simple slider',
    'ARTICLE_2_BODY': f'''{P}The calculator looked simple &mdash; that was the point &mdash; but the simplicity sat on a hard data problem. Registration costs differ across <strong>all eight Australian states and territories</strong>, and within them by category: rural, metropolitan, outer metropolitan, older vehicles. Fuel excise varies by fuel classification. Vehicle efficiency varies by make, model, and year.</p>
{P}Getting one combination right is easy; the tool had to be right in <strong>every combination</strong>, because a public calculator that misprices one state&rsquo;s rural utes loses the whole argument. The project&rsquo;s centre of gravity sat behind the interface: the <strong>extended data design sessions</strong> structuring the multi-dimensional cost rules, and the cleansing passes that made the reference data trustworthy.</p>
{P}My role was <strong>project management and design lead</strong>: translating the Strategy team&rsquo;s policy research into functional requirements, running the data design, shaping user flows, and coordinating the development team that built the application across a roughly three-month timeline. Design leadership on a build you do not code yourself is its own discipline &mdash; the spec and the data model are your product.</p>
{P}The tool served its season and has been retired, but the shape is durable: policy question, governed data model, public interface. If your organisation has a debate that needs a shared model, our {LINK("https://www.datalabsagency.com/dashboard-design-services/", "dashboard design services")} page shows how the engagement starts.</p>''',
})

page = assemble([hero_p1, row_flow, row_secB, t_modes, row_gallery, row_hotspot, row_tiles,
                 sec_deliver, row_quote, row_faq, art1, blocks['offers'], art2, blocks['fixed']])
page = apply_theme(page, '#20242e')  # per-page tint (Otto-approved palette, 25 Aug)
print('composed chars:', len(page))
import os, json, base64, urllib.request
pathlib.Path(OUT).write_text(page)
user, pw = os.environ['WP_DATALABS_USER'], os.environ['WP_DATALABS_APP_PASSWORD']
req = urllib.request.Request('https://www.datalabsagency.com/wp-json/wp/v2/pages/53956',
    data=json.dumps({'content': page, 'status': 'draft'}).encode(),
    headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
             'Authorization': 'Basic ' + base64.b64encode(f'{user}:{pw}'.encode()).decode()}, method='POST')
print('WP updated:', json.load(urllib.request.urlopen(req))['id'])
print('\nYOAST: SEO TITLE: Transurban Case Study: A Public Policy Calculator | Datalabs')
print("META DESCRIPTION: How the Datalabs Agency design-led Transurban's Road Usage Cost Calculator - a public interactive tool modelling road funding across every Australian state.")
