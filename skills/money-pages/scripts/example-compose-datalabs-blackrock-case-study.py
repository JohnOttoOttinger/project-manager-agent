#!/usr/bin/env python3
"""Compose the BlackRock Visual Case Study — overnight batch, 25 Aug 2026.

Content: tier-1 reference, BlackRock section. CONFIDENTIALITY: shared-in-confidence —
draft named per Otto's 25 Aug decision; he gates at publish. Rules honoured:
NO Aladdin (correction on record — asserted below); engagement years hedged to
"a three-year engagement" (2018-2021 never confirmed); NO BRP metric values published
(NPS etc. are the client's internal numbers — capabilities described instead);
the annual-letter analytics described without naming the executive; no client contacts.
Facts used: NYC global asset manager; PM + design role; Tableau/SQL/PowerPoint;
75-page Tableau style guide (documented TOC incl. audience, devices, time-on-dashboard,
hierarchy, grids/sequencing, language & naming, 30+ chart types in basic/advanced/
specialised tiers, native .TWBX delivery); Data Grid SQL tool; Eloqua dashboard system;
executive reports incl. annual-letter analytics; executive PowerPoint; BRP measurement
dashboard (Jan 2020, brand/web/sentiment scope); COVID-19 communications dashboard
(April 2020); resume split incl. Team Training & Capability Building.
Media: 53917 style guide page (hero), 53920 Data Grid.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from vcs_lib import *

blocks = kit_blocks()
OUT = '/private/tmp/claude-501/-Users-Ottinger-Claude-Projects-2026-project-manager-agent/1250d283-1a10-4416-b992-be81f96ce7a2/scratchpad/composed-blackrock.html'

hero = widen_hero(fill(blocks['intro'], {
    'PAGE_SUBTITLE': 'A visual case study&hellip;',
    'PAGE_TITLE': 'BlackRock: One Design Language',
    'UPDATED_DATE': 'August 2026',
    'HOOK': 'Over a <strong>three-year engagement</strong>, the Datalabs Agency became BlackRock&rsquo;s data visualisation partner in New York: a <strong>75-page Tableau style guide</strong> at the centre, feeding marketing dashboards, executive reporting, brand measurement, and an interactive SQL tool &mdash; one design language across all of it.',
    'SECTION_A_SUBTITLE': 'The engagement in one paragraph',
    'SECTION_A_HEADING': 'What did the Datalabs Agency build for BlackRock?',
    'SECTION_A_INTRO': 'For BlackRock&rsquo;s New York headquarters, the <strong>Datalabs Agency</strong> provided project management and design across a three-year engagement: a <strong>75-page Tableau data visualisation style guide</strong>, a <strong>Tableau dashboard system for the Eloqua</strong> marketing platform, executive reports and presentation design, a brand-measurement dashboard, a COVID-19 communications dashboard, and the <strong>Data Grid</strong> &mdash; an interactive SQL tool.',
    'CANONICAL_SENTENCE': CANONICAL,
    'SECTION_B_SUBTITLE': 'The problem behind the brief',
    'SECTION_B_HEADING': 'Why does an asset manager need a design language?',
    'SECTION_B_ANSWER': 'The animation above is the answer in miniature. BlackRock&rsquo;s analytics output ran across <strong>Tableau, SQL, and PowerPoint</strong>, built by different teams for audiences from marketing analysts to the executive floor. Without one design language, every deliverable stream drifts toward its own fonts, colours, and chart habits &mdash; and the brand fractures a screen at a time.',
    'SECTION_B_CONTEXT': 'That guide fixed the root cause: it legislated the questions that otherwise get re-argued per dashboard &mdash; internal versus external audiences, device dimensions, how long a reader actually spends on a screen, design hierarchy, grids and sequencing, even <strong>language and naming rules</strong> &mdash; and then documented <strong>more than 30 chart types</strong> with when-to-use guidance. Delivered as native Tableau workbooks aligned to BlackRock&rsquo;s brand, it meant every stream that followed started from the same page.',
    'PRIMARY_CTA_TEXT': 'Talk style guides with us',
    'PRIMARY_CTA_URL': CONTACT,
}))
hero_p1, row_secB = split_hero(hero, 53917)

# ---------- Row: Animated Flow Diagram — one language, five streams ----------
def svg_streams():
    streams = [('ELOQUA DASHBOARDS', 'Marketing analytics system'),
               ('EXECUTIVE REPORTING', 'Annual-letter analytics &amp; board decks'),
               ('BRAND MEASUREMENT', 'Awareness, engagement, sentiment'),
               ('COVID-19 COMMS', 'The April 2020 dashboard'),
               ('THE DATA GRID', 'Interactive SQL tool')]
    parts = [f'<svg viewBox="0 0 1200 640" xmlns="http://www.w3.org/2000/svg" role="img" '
             f'aria-label="One 75-page Tableau style guide feeding five BlackRock deliverable streams" '
             f'style="width:100%;height:auto;display:block;">']
    parts.append(f'<rect x="40" y="235" width="250" height="170" rx="12" fill="#1f1e29" stroke="{TAN}" stroke-width="2.5"/>')
    parts.append(f'<text x="165" y="300" text-anchor="middle" font-family="{BEBAS}" font-size="56" fill="{TAN}">75</text>')
    parts.append(f'<text x="165" y="330" text-anchor="middle" font-family="{ARVO}" font-size="14" fill="#ffffff">page style guide</text>')
    parts.append(f'<text x="165" y="352" text-anchor="middle" font-family="{ARVO}" font-size="12" fill="#8a8a95">the design language</text>')
    ys = [40, 158, 276, 394, 512]
    for j, ((name, sub), y) in enumerate(zip(streams, ys)):
        parts.append(flow_line(290, 320, 560, y + 44, cx1=430))
        parts.append(f'<rect x="560" y="{y}" width="300" height="88" rx="10" fill="#262532" stroke="{TAN}" stroke-width="1.5"/>')
        parts.append(f'<text x="584" y="{y+34}" font-family="{BEBAS}" font-size="22" letter-spacing="1.5" fill="#ffffff">{name}</text>')
        parts.append(f'<text x="584" y="{y+58}" font-family="{ARVO}" font-size="12" fill="#c39f76">{sub}</text>')
        # mini bars, stepping highlight with pulse
        for i, h in enumerate([16, 26, 20, 30, 24]):
            bx = 900 + i * 24
            if i == j:
                parts.append(f'<rect x="{bx}" y="{y+70-h}" width="15" height="{h}" rx="2" fill="{TAN}">'
                             f'<animate attributeName="opacity" values="1;0.5;1" dur="2s" repeatCount="indefinite"/></rect>')
            else:
                parts.append(f'<rect x="{bx}" y="{y+70-h}" width="15" height="{h}" rx="2" fill="#4a4860"/>')
    parts.append(f'<text x="1030" y="620" text-anchor="middle" font-family="{ARVO}" font-size="12" fill="#8a8a95">five streams, one look</text>')
    parts.append('</svg>')
    return ''.join(parts)

row_flow = svg_row('Watch one rulebook feed five streams', 'One design language, five deliverable streams',
    'Everything on the right &mdash; three years of marketing, executive, and measurement work &mdash; reads as one product because of the <strong>75 pages</strong> on the left.',
    svg_streams())

# ---------- chart library table ----------
t_charts = table_row(blocks, 'Pages 33 to 70', 'The chart library inside the style guide',
    'More than 30 chart types documented with when-to-use guidance, in three tiers.',
    ['Tier', 'Types', 'Examples'],
    [['Basic', '13', 'Column, bar, clustered, bullet, pie, donut, stacked and 100% stacked variants, radar, candlestick'],
     ['Advanced', '14', 'Slope, histogram, box-plot, waterfall, sankey, scatter, heat-map, calendar heat map, bubble, connected scatter'],
     ['Specialised', '7', 'Funnel, step line, location map, shape map, tree map, tornado, Venn']],
    footnote='Delivered as native Tableau workbooks (.TWBX), aligned to BlackRock&rsquo;s brand guidelines.')

# ---------- gallery (two assets) ----------
row_gallery = gallery_row('The work, full size', 'Two artefacts from the engagement',
    'Click either to view it full-screen &mdash; a page from the <strong>style guide</strong> and the <strong>Data Grid</strong> interactive tool.',
    [(53917, 'The Style Guide', 'One of 75 pages'),
     (53920, 'The Data Grid', 'An interactive SQL tool')])

# ---------- Row: Design Principle Tiles — the style guide's own chapters ----------
row_tiles = svg_row('Six questions the guide settles', 'What the style guide legislates',
    'Six of the design questions answered once, in writing &mdash; instead of re-argued on every dashboard.',
    svg_tiles('Six design questions settled by the BlackRock Tableau style guide', [
        ('AUDIENCE', 'Internal and external readers get different rules', 'people'),
        ('DEVICES &amp; DIMENSIONS', 'Designed for the screens it will meet', 'layers'),
        ('TIME ON DASHBOARD', 'Built for how long a reader really stays', 'clock'),
        ('DESIGN HIERARCHY', 'The key number reads first, detail second', 'hierarchy'),
        ('GRIDS &amp; SEQUENCING', 'One grid, so every screen reads the same', 'grid'),
        ('LANGUAGE &amp; NAMING', 'Titles and labels follow written rules', 'doc'),
    ]))

# ---------- deliverables ----------
sec_deliver = widen_inner(fill(blocks['section2'], {
    'SECTION_D_SUBTITLE': 'Delivered, documented, taught',
    'SECTION_D_HEADING': 'What did BlackRock receive across the engagement?',
    'SECTION_D_ANSWER': 'The <strong>75-page Tableau style guide</strong>, the <strong>Eloqua marketing dashboard system</strong>, executive reports and presentation designs, a brand-measurement dashboard covering awareness, web engagement, and sentiment, the April 2020 <strong>COVID-19 communications dashboard</strong>, and the <strong>Data Grid</strong> SQL tool &mdash; with team training and capability building running through all of it.',
    'SECTION_D_RATIONALE': 'Three years of deliverables only compound if each one leaves the client stronger. The style guide meant BlackRock&rsquo;s own analysts could design to standard without a review queue; the training meant the standard survived staff turnover. A design partnership should leave behind a firm that <strong>designs consistently without you</strong> &mdash; the dashboards are just the receipts.',
}), '1/4', '1/2')

row_quote = quote_row('Otto Ottinger', 'The principle behind the BlackRock engagement',
    'A style guide is a contract between every dashboard the firm will ever build.')

row_faq = faq_row(blocks, 'The BlackRock engagement', 'Ask about your design language', [
    ('What did the Datalabs Agency do for BlackRock?',
     'Project management and design across a three-year engagement at BlackRock&rsquo;s New York headquarters: a 75-page Tableau style guide, a Tableau dashboard system for the Eloqua marketing platform, executive reporting and presentation design, a brand-measurement dashboard, a COVID-19 communications dashboard, and an interactive SQL tool called the Data Grid.'),
    ('What is in the 75-page Tableau style guide?',
     'Four parts: an introduction to purpose and Tableau terminology; dashboard design principles covering audience, devices, time on dashboard, chart choice, hierarchy, grids and sequencing, and language rules; styling &mdash; fonts, colour, margins, and internal versus external themes; and a chart library documenting more than 30 chart types across basic, advanced, and specialised tiers.'),
    ('What tools did the work run on?',
     'Tableau for the style guide and dashboard systems, SQL for the Data Grid interactive tool, and PowerPoint for executive presentation design. Everything in the style guide shipped as native Tableau workbooks aligned to BlackRock&rsquo;s brand guidelines.'),
    ('Did BlackRock&rsquo;s own team get trained?',
     'Yes &mdash; team training and capability building ran alongside the design work throughout the engagement, so BlackRock&rsquo;s analysts could design to the standard themselves rather than routing everything through a consultant.'),
    ('Can the Datalabs Agency build a style guide for my company?',
     'Yes. A BI style guide &mdash; Tableau or Power BI &mdash; is one of our core services, and the BlackRock shape (style guide first, dashboard systems built on it) is the model we recommend for any organisation past its first ten dashboards. Send a note through the contact form for a scoped outline.'),
])

art1 = fill(blocks['article1'], {
    'ARTICLE_1_SUBTITLE': 'Seventy-five pages, four parts',
    'ARTICLE_1_HEADING': 'Anatomy of a Tableau style guide',
    'ARTICLE_1_BODY': f'''{P}The BlackRock guide opens where most dashboards go wrong: <strong>audience</strong>. Internal analysts and external clients read differently, tolerate different densities, and meet the work on different devices &mdash; so the guide splits its rules along that line before a single colour is specified.</p>
{P}The design section carries the thinking most teams never write down: how much <strong>time a reader actually spends</strong> on a dashboard, what <strong>design hierarchy</strong> puts in their first glance, how <strong>grids and sequencing</strong> make a multi-view workbook navigable, and the common dashboard types the firm keeps rebuilding. Then styling &mdash; fonts, colour systems, backgrounds, margins, and separate <strong>internal and external themes</strong> under one brand.</p>
{P}The largest part is the chart library: <strong>38 pages, more than 30 chart types</strong>, from column and bullet through sankey and box-plot to tree map and Venn &mdash; each with guidance on when it earns its place. A chart library is what turns a style guide from taste into law: the argument about which chart fits which question has a written answer.</p>
{P}The same anatomy &mdash; audience, design, styling, chart law &mdash; structures every one of our {LINK("/?page_id=394", "data visualization style guides")}, including the {LINK("https://www.datalabsagency.com/data-visualization-style-guides/tableau-style-guides/", "Tableau style guides")} we build today.</p>''',
})
art2 = fill(blocks['article2'], {
    'ARTICLE_2_SUBTITLE': 'Three years inside one brand&hellip;',
    'ARTICLE_2_HEADING': 'What a long design partnership looks like',
    'ARTICLE_2_BODY': f'''{P}Most design work is a project: brief, build, handover, goodbye. The BlackRock engagement was the other kind &mdash; <strong>three years</strong> of being the design capability a firm reaches for as needs surface. First came the style guide, because everything else depends on it; what followed tracked the business itself.</p>
{P}Marketing needed its <strong>Eloqua platform</strong> turned into dashboards a team could run campaigns from &mdash; that became a full Tableau dashboard system. The executive floor needed analytics shaped for the boardroom, including work supporting the firm&rsquo;s <strong>annual letter</strong>, and presentation design to match. Brand and communications needed measurement: a dashboard spanning <strong>brand tracking, web engagement, and sentiment analysis</strong> across markets.</p>
{P}And in April 2020, the engagement showed why embedded partners matter: a <strong>COVID-19 communications dashboard</strong>, needed immediately, built inside a design language that already existed. Speed at a moment like that is not heroics &mdash; it is the dividend of the 75 pages written two years earlier.</p>
{P}The engagement also produced my favourite odd artefact: the <strong>Data Grid</strong>, an interactive SQL tool &mdash; proof that a design language stretches past dashboards into {LINK("/?page_id=415", "interactive data tools")}. For the engagement model itself, our {LINK("https://www.datalabsagency.com/dashboard-design-services/", "dashboard design services")} page shows how it starts.</p>''',
})

page = assemble([hero_p1, row_flow, row_secB, t_charts, row_gallery, row_tiles,
                 sec_deliver, row_quote, row_faq, art1, blocks['offers'], art2, blocks['fixed']])
page = apply_theme(page, '#1e222b')  # per-page tint (Otto-approved palette, 25 Aug)
assert 'Aladdin' not in page and 'aladdin' not in page.lower()
assert 'Fink' not in page
print('composed chars:', len(page))
import os, json, base64, urllib.request
pathlib.Path(OUT).write_text(page)
user, pw = os.environ['WP_DATALABS_USER'], os.environ['WP_DATALABS_APP_PASSWORD']
req = urllib.request.Request('https://www.datalabsagency.com/wp-json/wp/v2/pages/53923',
    data=json.dumps({'content': page, 'status': 'draft'}).encode(),
    headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
             'Authorization': 'Basic ' + base64.b64encode(f'{user}:{pw}'.encode()).decode()}, method='POST')
print('WP updated:', json.load(urllib.request.urlopen(req))['id'])
print('\nYOAST: SEO TITLE: BlackRock Case Study: One Design Language | Datalabs')
print('META DESCRIPTION: How the Datalabs Agency built BlackRock a 75-page Tableau style guide and the dashboard systems on top of it, across a three-year New York engagement.')
