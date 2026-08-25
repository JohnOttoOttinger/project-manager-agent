#!/usr/bin/env python3
"""Compose the Gumtree/eBay Visual Case Study — overnight batch, 25 Aug 2026.

Content: gumtree-ebay-case-study.md (full standalone draft). Resolutions applied:
ENTITY = Datalabs (Otto's ruling 25 Aug — "eBay was a Datalabs project & client");
NO sponsor name ("the Director of Analytics" only); the multi-million-dollar claim is
STRUCK (never sourced); outcome language stays designed-to-enable, never measured;
tool recommendations NOT named (never captured in session); the engagement fee is NOT
published (Otto can add — it is documented at $20,530.55 AUD ex GST if he wants it).
Facts: Gumtree Australia (eBay Group, contracting via Marktplaats B.V. — entity not
named on page, "the eBay Group" suffices); 2 May - 30 June 2017, 8 weeks; remote from
Melbourne with secure access to eBay consoles and the data warehouse under eBay's
Data Protection Requirements Addendum and ISO 27001-aligned controls; four audit
lenses (technical / business / data / tool evaluation); strategy deliverables
(multi-year roadmap, governance frameworks, implementation guidelines, training and
capability recommendations); final presentation to the Director of Analytics.
Media: 53958 three-things (hero), 53961/53964 session agendas, 53967 relational map.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from vcs_lib import *

blocks = kit_blocks()
OUT = '/private/tmp/claude-501/-Users-Ottinger-Claude-Projects-2026-project-manager-agent/1250d283-1a10-4416-b992-be81f96ce7a2/scratchpad/composed-gumtree.html'

hero = widen_hero(fill(blocks['intro'], {
    'PAGE_SUBTITLE': 'A visual case study&hellip;',
    'PAGE_TITLE': 'Gumtree &amp; eBay: A Visual BI Strategy',
    'UPDATED_DATE': 'August 2026',
    'HOOK': 'In mid-2017, Gumtree Australia &mdash; part of the eBay Group &mdash; had deep data and no strategy connecting it to decisions. Over an <strong>eight-week engagement</strong>, Datalabs audited the analytics landscape across <strong>four lenses</strong> and delivered a visual BI strategy: a multi-year roadmap, governance frameworks, and a capability pathway.',
    'SECTION_A_SUBTITLE': 'The engagement in one paragraph',
    'SECTION_A_HEADING': 'What did the Datalabs Agency deliver for Gumtree?',
    'SECTION_A_INTRO': 'From 2 May to 30 June 2017, the <strong>Datalabs Agency</strong> ran an independent <strong>visual business intelligence strategy</strong> engagement for Gumtree Australia: a discovery audit across the existing Google Analytics and <strong>eBay data warehouse</strong> landscape, then a strategy package &mdash; a multi-year roadmap, <strong>governance frameworks and best-practice standards</strong>, implementation guidelines, and training recommendations &mdash; presented to the Director of Analytics and leadership.',
    'CANONICAL_SENTENCE': CANONICAL,
    'SECTION_B_SUBTITLE': 'The problem behind the brief',
    'SECTION_B_HEADING': 'Why did a data-rich business need a BI strategy?',
    'SECTION_B_ANSWER': 'The animation above is the engagement&rsquo;s shape. The problem behind it: Gumtree had <strong>no shortage of data</strong> &mdash; Google Analytics and the eBay data warehouse gave deep visibility into behaviour, audience, revenue, and user actions. What was missing was the connective layer: no coherent approach to <strong>visual analytics</strong>, complex data never reaching decision-makers in usable form, and no basis for choosing BI tools.',
    'SECTION_B_CONTEXT': 'The Director of Analytics wanted something specific: an <strong>independent expert assessment</strong> &mdash; someone outside the organisation, with nothing to sell, who could evaluate the landscape objectively and produce a roadmap the business could act on. That independence shaped the whole engagement: pure strategy, no build, and recommendations judged on <strong>fit-for-purpose criteria</strong> rather than a vendor relationship.',
    'PRIMARY_CTA_TEXT': 'Ask for an independent audit',
    'PRIMARY_CTA_URL': CONTACT,
}))
hero_p1, row_secB = split_hero(hero, 53958)

# ---------- Row: Animated Flow Diagram — four lenses in, four outputs out ----------
def svg_strategy():
    lenses = [('TECHNICAL', 'Data infrastructure across GA and the warehouse'),
              ('BUSINESS', 'How decisions were actually being made'),
              ('DATA', 'Quality, accessibility, integration points'),
              ('TOOLS', 'The BI landscape, judged on fit')]
    outputs = [('THE ROADMAP', 'Multi-year visual analytics maturity'),
               ('GOVERNANCE', 'Frameworks and best-practice standards'),
               ('ARCHITECTURE', 'Technical recommendations and guidelines'),
               ('CAPABILITY', 'Training and skills pathway')]
    parts = [f'<svg viewBox="0 0 1200 640" xmlns="http://www.w3.org/2000/svg" role="img" '
             f'aria-label="Four audit lenses feeding the Gumtree visual BI strategy, producing a roadmap, governance, architecture, and capability outputs" '
             f'style="width:100%;height:auto;display:block;">']
    ys = [56, 200, 344, 488]
    for (name, sub), y in zip(lenses, ys):
        parts.append(f'<rect x="40" y="{y}" width="290" height="96" rx="10" fill="#262532" stroke="#4a4860" stroke-width="1.5"/>')
        parts.append(f'<text x="64" y="{y+38}" font-family="{BEBAS}" font-size="24" letter-spacing="1.5" fill="#ffffff">{name}</text>')
        parts.append(f'<text x="64" y="{y+64}" font-family="{ARVO}" font-size="12" fill="#8a8a95">{sub}</text>')
        parts.append(flow_line(330, y + 48, 494, 320, cx1=420))
    parts.append(f'<circle cx="600" cy="320" r="106" fill="#1f1e29" stroke="{TAN}" stroke-width="2.5"/>')
    parts.append(f'<circle cx="600" cy="320" r="120" fill="none" stroke="{TAN}" stroke-width="1" opacity="0.35" stroke-dasharray="3 7"/>')
    parts.append(f'<text x="600" y="308" text-anchor="middle" font-family="{BEBAS}" font-size="30" letter-spacing="1.5" fill="{TAN}">8 WEEKS</text>')
    parts.append(f'<text x="600" y="338" text-anchor="middle" font-family="{ARVO}" font-size="14" fill="#ffffff">of independent audit</text>')
    parts.append(f'<text x="600" y="360" text-anchor="middle" font-family="{ARVO}" font-size="12" fill="#8a8a95">nothing to sell, everything to check</text>')
    for j, ((name, sub), y) in enumerate(zip(outputs, ys)):
        parts.append(flow_line(706, 320, 870, y + 48, cx1=790))
        parts.append(f'<rect x="870" y="{y}" width="290" height="96" rx="10" fill="#262532" stroke="{TAN}" stroke-width="1.5"/>')
        parts.append(f'<text x="894" y="{y+38}" font-family="{BEBAS}" font-size="24" letter-spacing="1.5" fill="#ffffff">{name}</text>')
        parts.append(f'<text x="894" y="{y+64}" font-family="{ARVO}" font-size="12" fill="#c39f76">{sub}</text>')
    parts.append('</svg>')
    return ''.join(parts)

row_flow = svg_row('Watch the audit become a strategy', 'Four lenses in, four outputs out',
    'Eight weeks between them: an audit across <strong>four lenses</strong> on the left, and the strategy package it produced on the right.',
    svg_strategy())

# ---------- audit lens table ----------
t_lenses = table_row(blocks, 'What an audit inspects', 'The four audit lenses',
    'Each lens asked a different question of the same analytics landscape.',
    ['Lens', 'What was assessed'],
    [['Technical analysis', 'The existing data infrastructure across Google Analytics consoles and eBay data warehouse systems'],
     ['Business analysis', 'Stakeholder needs, current reporting capability, and how decisions were actually being made'],
     ['Data analysis', 'Data quality, accessibility, and integration points across platforms'],
     ['Tool evaluation', 'The BI tool landscape, assessed against fit-for-purpose criteria']],
    footnote='Delivered primarily remotely from Melbourne, under secure access to eBay consoles and databases.')

# ---------- gallery ----------
row_gallery = gallery_row('The working documents, full size', 'From the strategy sessions',
    'Click any document to view it full-screen &mdash; the session materials and the proposed <strong>dashboard relational map</strong>.',
    [(53967, 'The Relational Map', 'The proposed dashboard system'),
     (53958, 'Three Things', 'The strategy presentation opener'),
     (53961, 'Session One', 'The first working session agenda'),
     (53964, 'Session Two', 'The second working session agenda')])

# ---------- Row: Design Principle Tiles ----------
row_tiles = svg_row('Why this engagement is different', 'The shape of an independent strategy',
    'Six things that defined the engagement &mdash; and define every strategy audit we run.',
    svg_tiles('Six defining characteristics of the Gumtree eBay visual BI strategy engagement', [
        ('PURE STRATEGY', 'The deliverable was thinking, no build', 'doc'),
        ('INDEPENDENT ADVISOR', 'Objectivity on a major tool decision', 'target'),
        ('ENTERPRISE SECURITY', 'ISO 27001-aligned controls throughout', 'grid'),
        ('REMOTE, SECURE ACCESS', 'Melbourne to the eBay warehouse, governed', 'layers'),
        ('GOVERNANCE FIRST', 'Frameworks before dashboards', 'hierarchy'),
        ('CAPABILITY PATHWAY', 'A plan the in-house team executes', 'people'),
    ]))

# ---------- deliverables ----------
sec_deliver = widen_inner(fill(blocks['section2'], {
    'SECTION_D_SUBTITLE': 'Delivered and presented',
    'SECTION_D_HEADING': 'What did Gumtree receive at the end?',
    'SECTION_D_ANSWER': 'A comprehensive <strong>strategy audit report</strong>, the visual BI strategy presentation with a <strong>multi-year roadmap</strong>, technical architecture recommendations, and implementation guidelines with next steps &mdash; translated into accessible visual form and presented to the <strong>Director of Analytics</strong> and leadership team.',
    'SECTION_D_RATIONALE': 'The strategy was written to be enabling rather than binding: tool selection criteria instead of a vendor pick made for them, governance frameworks the team could grow into, and a capability pathway so the roadmap had owners inside the business. An independent assessment earns its fee by leaving the client <strong>able to decide</strong>, and equipped to execute.',
}), '1/4', '1/2')

row_quote = quote_row('Otto Ottinger', 'The principle behind the engagement',
    'An independent audit is worth commissioning precisely because the auditor has nothing to sell.')

row_faq = faq_row(blocks, 'The Gumtree engagement', 'Ask about a strategy audit', [
    ('What did the Datalabs Agency do for Gumtree and eBay?',
     'An <strong>eight-week independent visual BI strategy engagement</strong> for Gumtree Australia, part of the eBay Group, from May to June 2017: a discovery audit across technical, business, data, and tool-evaluation lenses, followed by a strategy package &mdash; <strong>multi-year roadmap</strong>, governance frameworks, architecture recommendations, and implementation guidelines &mdash; presented to the Director of Analytics.'),
    ('Why did the client want an external consultant?',
     '<strong>Independence</strong>. Gumtree&rsquo;s analytics leadership wanted an expert from outside the organisation who could evaluate the data landscape objectively and assess BI tools on <strong>fit-for-purpose criteria</strong> &mdash; an assessment with no build contract or software sale attached to the answer.'),
    ('How was the work delivered securely?',
     'Primarily remotely from Melbourne, using <strong>secure remote access</strong> to eBay consoles and databases under eBay&rsquo;s Data Protection Requirements Addendum and <strong>ISO 27001-aligned controls</strong> &mdash; the security standard a global technology company expects of its consultants.'),
    ('Did the engagement include any dashboard builds?',
     'No, deliberately. This was <strong>pure strategy</strong>: audit, roadmap, and recommendations. The value was an objective read of the landscape and a plan the in-house team could execute &mdash; including the <strong>governance and capability groundwork</strong> that makes later builds succeed.'),
    ('Can the Datalabs Agency audit our BI landscape?',
     'Yes. A strategy audit &mdash; <strong>four lenses</strong>, a roadmap, governance frameworks, and <strong>tool selection criteria</strong> &mdash; is how we recommend starting when reporting has grown faster than strategy. Send a note through the contact form and we will reply with a scoped outline.'),
])

art1 = fill(blocks['article1'], {
    'ARTICLE_1_SUBTITLE': 'Four questions, one landscape',
    'ARTICLE_1_HEADING': 'What a visual BI audit actually inspects',
    'ARTICLE_1_BODY': f'''{P}An analytics audit fails when it only looks at technology. Gumtree&rsquo;s landscape got four separate examinations, because the four ways a BI capability breaks are different. The <strong>technical lens</strong> walked the infrastructure &mdash; Google Analytics consoles, the <strong>eBay data warehouse</strong>, and the joins between them.</p>
{P}The <strong>business lens</strong> asked the awkward question: how are decisions actually made here, and what reporting do they really run on? The gap between official dashboards and the spreadsheets people trust is where most strategies are won. The <strong>data lens</strong> then tested quality, accessibility, and integration &mdash; whether the raw material could support the ambitions.</p>
{P}The <strong>tool evaluation</strong> came last, on purpose. Assessing the BI market against <strong>fit-for-purpose criteria</strong> only makes sense once you know the infrastructure, the decisions, and the data health the tool must serve. Choosing the platform first and discovering the requirements afterwards is the standard failure mode of BI procurement.</p>
{P}Those four lenses became the audit report, and the report became the strategy. It is the same sequence behind our {LINK("https://www.datalabsagency.com/dashboard-design-services/", "dashboard design services")} engagements today &mdash; understand before recommending, recommend before building.</p>''',
})
art2 = fill(blocks['article2'], {
    'ARTICLE_2_SUBTITLE': 'Inside the security perimeter&hellip;',
    'ARTICLE_2_HEADING': 'Consulting to enterprise security standards',
    'ARTICLE_2_BODY': f'''{P}Working for an eBay Group company means working inside an eBay-grade perimeter. The engagement ran under a formal <strong>Data Protection Requirements Addendum</strong> and <strong>ISO 27001-aligned controls</strong>, with secure remote access from Melbourne into eBay consoles and databases &mdash; every session governed, every access accountable.</p>
{P}That framework is a constraint, and it is also a credential. A consultancy that can operate under a global technology company&rsquo;s security regime &mdash; full service agreements, governed data access, remote delivery &mdash; has demonstrated something no case study paragraph can: that it can be <strong>trusted inside the walls</strong>.</p>
{P}The remote model mattered too. In 2017, delivering an enterprise strategy engagement <strong>primarily from Melbourne</strong> into an Australian subsidiary of a US giant was still unusual; it has since become our default shape for interstate and international work. Secure access plus disciplined working sessions beat airfares &mdash; then and now.</p>
{P}And the deliverable respected the trust: strategy the client owns outright, with training and capability recommendations so the {LINK("/?page_id=661", "skills to execute it")} could be built in-house. When the engagement ended, everything of value stayed behind.</p>''',
})

page = assemble([hero_p1, row_flow, row_secB, t_lenses, row_gallery, row_tiles,
                 sec_deliver, row_quote, row_faq, art1, blocks['offers'], art2, blocks['fixed']])
page = apply_theme(page, '#1c241b')  # per-page tint (Otto-approved palette, 25 Aug)
assert 'Marktplaats' not in page and 'million' not in page.lower() and '20,530' not in page
print('composed chars:', len(page))
import os, json, base64, urllib.request
pathlib.Path(OUT).write_text(page)
user, pw = os.environ['WP_DATALABS_USER'], os.environ['WP_DATALABS_APP_PASSWORD']
req = urllib.request.Request('https://www.datalabsagency.com/wp-json/wp/v2/pages/53970',
    data=json.dumps({'content': page, 'status': 'draft'}).encode(),
    headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
             'Authorization': 'Basic ' + base64.b64encode(f'{user}:{pw}'.encode()).decode()}, method='POST')
print('WP updated:', json.load(urllib.request.urlopen(req))['id'])
print('\nYOAST: SEO TITLE: Gumtree & eBay Case Study: Visual BI Strategy | Datalabs')
print('META DESCRIPTION: How the Datalabs Agency audited Gumtree Australia\\u2019s analytics landscape for the eBay Group and delivered a visual BI strategy - roadmap, governance, and tools.')
