#!/usr/bin/env python3
"""Compose the Intel Visual Case Study — overnight batch, 25 Aug 2026.

Content: tier-1 reference, Intel section. CONFIDENTIALITY: shared-in-confidence client —
draft named per Otto's 25 Aug decision; he gates at publish. Rules honoured: NO dollar
figures (phase totals do not reconcile, and client pricing stays private by default);
NO client contact names. Facts used are documented: IPG division, Oct 2020 - Apr 2021,
Power BI, three phases (training + 78-page "Business Class" style guide + templates +
checklist; retrofit of 3 interfaces / 27 modules; 10 dashboard designs / 90 modules +
navigation system), 9-module standard architecture, 15+ analysts trained, annotated
flat designs with functional notes for Intel's in-house Power BI developers, dashboards:
Bug Escapes Summary & Profile (By Project / IP Family / IP Supplier views), IP Scan
Overview, Ops Review Summary, Test Chips Review. Style guide contents (accessibility
checklist, iconic memory, colorways, mobile design, Pre-Flight Check) are all from the
documented 78-page structure.
INTERACTIVE EXPERIMENT #2: the design system assembling itself — 10 dashboard cards,
each building up its 9 modules cell by cell, staggered, to a 90-module total.
No client images exist for this project — the page is deliberately SVG-led.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from vcs_lib import *

blocks = kit_blocks()
OUT = '/private/tmp/claude-501/-Users-Ottinger-Claude-Projects-2026-project-manager-agent/1250d283-1a10-4416-b992-be81f96ce7a2/scratchpad/composed-intel.html'

hero = widen_hero(fill(blocks['intro'], {
    'PAGE_SUBTITLE': 'A visual case study&hellip;',
    'PAGE_TITLE': 'Intel: 90 Modules, One Design System',
    'UPDATED_DATE': 'August 2026',
    'HOOK': 'Between October 2020 and April 2021, the Datalabs Agency built Intel&rsquo;s IPG division a complete <strong>Power BI design system</strong>: a <strong>78-page style guide</strong>, then <strong>13 dashboard designs totalling 117 modules</strong> &mdash; every screen assembled from the same nine-module architecture, and handed to Intel&rsquo;s own developers to build.',
    'SECTION_A_SUBTITLE': 'The engagement in one paragraph',
    'SECTION_A_HEADING': 'What did the Datalabs Agency build for Intel?',
    'SECTION_A_INTRO': 'Across three phases, the <strong>Datalabs Agency</strong> delivered Intel&rsquo;s Integrated Products Group a <strong>&ldquo;Business Class&rdquo; Power BI style guide</strong> (78 pages), workshop training for <strong>15+ analysts</strong>, standard report templates and a design checklist, a retrofit of three existing interfaces (27 modules), and ten new dashboard designs (90 modules) including the <strong>Bug Escapes</strong> suite &mdash; plus the navigation system connecting them.',
    'CANONICAL_SENTENCE': CANONICAL,
    'SECTION_B_SUBTITLE': 'The problem behind the brief',
    'SECTION_B_HEADING': 'Why did Intel need a dashboard design system?',
    'SECTION_B_ANSWER': 'The animation above is the point: dashboards at scale are a <strong>manufacturing problem</strong>. IPG&rsquo;s engineering data &mdash; bug escapes, IP scans, ops reviews, test chips &mdash; needed more than a dozen dashboards, built by different hands over months. Without a design system, every new screen becomes a new argument about fonts, colours, and layout.',
    'SECTION_B_CONTEXT': 'The engagement was sequenced to prevent exactly that. <strong>Phase one built the law</strong>: the style guide, templates, and a checklist, taught to the analyst team in workshops. Phase two proved it on existing screens, retrofitting three interfaces. Only then did phase three scale to ten new dashboards &mdash; each assembled from the same <strong>nine-module architecture</strong>, so Intel&rsquo;s in-house Power BI developers could build from annotated designs without a designer looking over their shoulder.',
    'PRIMARY_CTA_TEXT': 'Talk design systems with us',
    'PRIMARY_CTA_URL': CONTACT,
}))
hero_p1, row_secB = split_hero(hero, None)
# no client imagery exists for this engagement — drop the hero image slot entirely
hero_p1 = hero_p1.replace('[vc_single_image image="None" img_size="large" alignment="center" style="vc_box_rounded" onclick="link_image" css=""]', '')

# ---------- INTERACTIVE: the design system assembling itself ----------
def svg_assembly():
    labels = ['BUG ESCAPES SUMMARY', 'BUG ESCAPES PROFILE', 'IP SCAN OVERVIEW', 'OPS REVIEW SUMMARY', 'TEST CHIPS REVIEW',
              'DASHBOARD 6', 'DASHBOARD 7', 'DASHBOARD 8', 'DASHBOARD 9', 'DASHBOARD 10']
    parts = [f'<svg viewBox="0 0 1200 700" xmlns="http://www.w3.org/2000/svg" role="img" '
             f'aria-label="Ten Intel dashboard designs assembling from the same nine-module architecture, ninety modules in total" '
             f'style="width:100%;height:auto;display:block;">']
    # style guide source node
    parts.append(f'<rect x="40" y="270" width="240" height="160" rx="12" fill="#1f1e29" stroke="{TAN}" stroke-width="2.5"/>')
    parts.append(f'<text x="160" y="330" text-anchor="middle" font-family="{BEBAS}" font-size="52" fill="{TAN}">78</text>')
    parts.append(f'<text x="160" y="358" text-anchor="middle" font-family="{ARVO}" font-size="14" fill="#ffffff">page style guide</text>')
    parts.append(f'<text x="160" y="380" text-anchor="middle" font-family="{ARVO}" font-size="12" fill="#8a8a95">one set of rules, taught first</text>')
    # 10 dashboard cards in 2 rows of 5, each with a 3x3 module grid that lights up staggered
    total = 0
    for i, label in enumerate(labels):
        col, row_i = i % 5, i // 5
        x = 340 + col * 172
        y = 80 + row_i * 300
        parts.append(flow_line(280, 350, x, y + 105, cx1=310))
        parts.append(f'<rect x="{x}" y="{y}" width="150" height="210" rx="9" fill="#262532" stroke="#4a4860" stroke-width="1.5"/>')
        # title bar
        fs = 13 if len(label) > 14 else 15
        parts.append(f'<text x="{x+75}" y="{y+26}" text-anchor="middle" font-family="{BEBAS}" font-size="{fs}" letter-spacing="1" fill="#ffffff">{label}</text>')
        # 3x3 module cells, staggered build
        for m in range(9):
            total += 1
            mx = x + 14 + (m % 3) * 42
            my = y + 44 + (m // 3) * 44
            delay = round(0.06 * total, 2)
            fillc = TAN if m == 0 else '#3a384c'
            parts.append(f'<rect x="{mx}" y="{my}" width="36" height="38" rx="4" fill="{fillc}" opacity="0">'
                         f'<animate attributeName="opacity" from="0" to="{1 if m==0 else 0.9}" dur="0.5s" begin="{delay}s" fill="freeze"/></rect>')
        parts.append(f'<text x="{x+75}" y="{y+198}" text-anchor="middle" font-family="{ARVO}" font-size="10" fill="#8a8a95">9 modules, same grid</text>')
    # counter band
    parts.append(f'<rect x="340" y="640" width="810" height="46" rx="9" fill="#262532" stroke="{TAN}" stroke-width="1.5" stroke-dasharray="5 6"/>')
    parts.append(f'<text x="745" y="670" text-anchor="middle" font-family="{BEBAS}" font-size="20" letter-spacing="2" fill="{TAN}">90 MODULES ACROSS 10 DASHBOARDS &#8212; EVERY ONE ON THE SAME GRID</text>')
    parts.append('</svg>')
    return ''.join(parts)

row_flow = svg_row('Watch the system assemble', 'Ninety modules, one grid',
    'Phase three in one picture: ten dashboards built from the <strong>same nine-module architecture</strong>, so every screen reads like a sibling of the last.',
    svg_assembly())

# ---------- phases table ----------
t_phases = table_row(blocks, 'Law first, then scale', 'The three-phase engagement',
    'The engagement structure, October 2020 to April 2021.',
    ['Phase', 'Window', 'Scope'],
    [['Phase 1 &mdash; the rules', 'To the November launch', 'Workshop training; the 78-page &ldquo;Business Class&rdquo; style guide; standard templates; a design checklist'],
     ['Phase 2 &mdash; the proof', 'Late Nov &ndash; mid Dec 2020', 'Retrofit of three existing interfaces &mdash; 27 modules brought onto the new system'],
     ['Phase 3 &mdash; the scale', 'Mid Jan &ndash; end Mar 2021', 'Ten new dashboard designs (90 modules), the Bug Escapes suite, and the navigation system connecting it all']],
    footnote='Designs were delivered as annotated flat designs with functional notes, built by Intel&rsquo;s in-house Power BI development team through iterative revision rounds.')

# ---------- dashboards table ----------
t_dash = table_row(blocks, 'The screens themselves', 'The dashboards designed for IPG',
    'Each dashboard was designed for one engineering question.',
    ['Dashboard', 'What it answers'],
    [['Bug Escapes Summary', 'High-level bug trends: which IP families and projects need attention'],
     ['Bug Escapes Profile', 'Detailed analysis in three views &mdash; By Project, By IP Family, By IP Supplier &mdash; with pre-silicon vs post-silicon comparison'],
     ['IP Scan Overview', 'Scan status across the IP portfolio'],
     ['Ops Review Summary', 'The operations review, standardised'],
     ['Test Chips Review', 'Test chip programs at a glance']],
    footnote='All screens filterable by customer, sub-organisation, project, IP supplier, and IP family.')

# ---------- Row: Design Principle Tiles — straight from the 78 pages ----------
row_tiles = svg_row('Six of the 78 pages', 'What a &ldquo;Business Class&rdquo; style guide teaches',
    'Six rules from the style guide&rsquo;s own contents &mdash; the document Intel&rsquo;s analysts now design by.',
    svg_tiles('Six design rules from the Intel Business Class Power BI style guide', [
        ('THE 9-MODULE GRID', 'Every dashboard assembles from one grid', 'grid'),
        ('ICONIC MEMORY', 'Design for the half-second first glance', 'target'),
        ('ACCESSIBILITY', 'A checklist, not an afterthought', 'doc'),
        ('COLORWAYS', 'Chart palettes built as a system', 'swatches'),
        ('MOBILE DESIGN', 'Screens that survive a phone', 'layers'),
        ('PRE-FLIGHT CHECK', 'A quality gate before anything ships', 'clock'),
    ]))

# ---------- deliverables ----------
sec_deliver = widen_inner(fill(blocks['section2'], {
    'SECTION_D_SUBTITLE': 'Delivered, documented, taught',
    'SECTION_D_HEADING': 'What did Intel receive at the end?',
    'SECTION_D_ANSWER': 'Intel received the <strong>78-page style guide</strong>, standard report templates and a design checklist, <strong>13 dashboard designs</strong> (three retrofits plus ten new screens, 117 modules in all), a navigation system, and <strong>15+ analysts trained</strong> through workshops &mdash; everything needed to keep designing without a consultant.',
    'SECTION_D_RATIONALE': 'The handover model is the quiet win: every screen shipped as an <strong>annotated flat design with functional notes</strong>, built by Intel&rsquo;s own Power BI developers through iterative revision rounds. The design intelligence lives in the style guide and the team, which means the system keeps growing after the engagement ends &mdash; the same capability-building model behind every <strong>Datalabs Agency</strong> design system since.',
}), '1/4', '1/2')

row_quote = quote_row('Otto Ottinger', 'The principle behind the Intel system',
    'Design the system before the screens &mdash; when the style guide is right, the tenth dashboard almost designs itself.')

row_faq = faq_row(blocks, 'The Intel engagement', 'Ask about your design system', [
    ('What did the Datalabs Agency deliver for Intel?',
     'A three-phase Power BI design engagement for Intel&rsquo;s IPG division, October 2020 to April 2021: a 78-page style guide with templates and a design checklist, workshop training for 15+ analysts, a retrofit of three existing interfaces, and ten new dashboard designs including the Bug Escapes suite, plus the navigation system connecting them.'),
    ('What is in the &ldquo;Business Class&rdquo; Power BI style guide?',
     '78 pages covering dashboard design (audience, iconic memory, chart selection, hierarchy, grids, accessibility with a checklist, mobile design), styling (fonts, chart palettes, colorways, layout examples), more than 20 chart types with alternatives, and a Pre-Flight Check quality gate.'),
    ('How were the dashboard designs delivered?',
     'As annotated flat designs with functional notes, standardised on a nine-module architecture. Intel&rsquo;s in-house Power BI development team built each screen from the annotations through iterative revision rounds &mdash; a designer-to-developer handover model rather than an agency build.'),
    ('Did Intel&rsquo;s own team get trained?',
     'Yes. More than fifteen analysts went through the phase-one workshops, and the style guide, templates, and checklist were built to be theirs &mdash; the system was designed so Intel could keep extending it internally.'),
    ('Can the Datalabs Agency build a Power BI design system for my company?',
     'Yes. The Intel shape &mdash; style guide first, retrofit second, scale third &mdash; is our standard design-system engagement, and it works in Tableau as well as Power BI. Send a note through the contact form and we will reply with a phased outline.'),
])

art1 = fill(blocks['article1'], {
    'ARTICLE_1_SUBTITLE': 'The rulebook is the product',
    'ARTICLE_1_HEADING': 'What 78 pages of design law actually buys',
    'ARTICLE_1_BODY': f'''{P}A style guide sounds like decoration until you watch a dashboard portfolio grow without one. Screen five contradicts screen two; every new build relitigates the colour palette; the mobile view is nobody&rsquo;s job. The <strong>Business Class guide</strong> we built for Intel exists to end those arguments before they start.</p>
{P}Its spine is practical: how to choose charts, how <strong>iconic memory</strong> shapes the first half-second of reading, how <strong>design hierarchy</strong> decides what gets seen, how grids and sequencing make a screen scannable. Then the system layer: fonts, <strong>chart colorways</strong> built as reusable palettes, layout templates, an <strong>accessibility checklist</strong>, and mobile rules &mdash; ending in a <strong>Pre-Flight Check</strong> that every screen passes before it ships.</p>
{P}The economics are the argument. Ten dashboards designed one-off cost <strong>ten design projects</strong>. Ten dashboards on a nine-module grid with a style guide cost <strong>one design project and nine assemblies</strong> &mdash; and they read as one product, which is what an executive flipping between screens actually notices.</p>
{P}This is the same discipline behind our {LINK("/?page_id=394", "data visualization style guides")} for other clients &mdash; each one a rulebook first and a portfolio second.</p>''',
})
art2 = fill(blocks['article2'], {
    'ARTICLE_2_SUBTITLE': 'Designs that survive the handover&hellip;',
    'ARTICLE_2_HEADING': 'Designing for someone else&rsquo;s developers',
    'ARTICLE_2_BODY': f'''{P}The Intel engagement had a constraint that shaped everything: I would not be building the dashboards. Intel&rsquo;s own <strong>in-house Power BI team</strong> would. A design that only works with its designer standing next to it is a failed design, so every screen shipped as an <strong>annotated flat design</strong> &mdash; the layout plus functional notes covering states, filters, and interactions.</p>
{P}The <strong>nine-module architecture</strong> made the handover honest. When every dashboard is nine modules on one grid, a developer who has built one screen has practised for all of them, and a reviewer can spot a deviation at a glance. Standardisation is not a creative constraint; it is what lets a system scale past its designer.</p>
{P}The sequencing did the rest. Teaching the <strong>15+ analysts</strong> first meant the people closest to the data understood the rules before the screens arrived. Retrofitting three live interfaces second meant the system proved itself on real workloads before anyone bet ten new dashboards on it. By phase three, iteration rounds were about refinement, and the <strong>Bug Escapes suite</strong> &mdash; summary, profile, three analysis views &mdash; landed on schedule.</p>
{P}If your BI backlog is growing faster than your design capacity, the Intel shape is the fix: rules, proof, then scale. Our {LINK("https://www.datalabsagency.com/dashboard-design-services/", "dashboard design services")} page shows how the engagement runs, and the {LINK("/?page_id=379", "Power BI dashboard design")} page covers the platform specifics.</p>''',
})

page = assemble([hero_p1, row_flow, row_secB, t_phases, row_tiles, t_dash,
                 sec_deliver, row_quote, row_faq, art1, blocks['offers'], art2, blocks['fixed']])
page = apply_theme(page, '#16222e')  # per-page tint (Otto-approved palette, 25 Aug)
print('composed chars:', len(page))
import os, json, base64, urllib.request
pathlib.Path(OUT).write_text(page)
user, pw = os.environ['WP_DATALABS_USER'], os.environ['WP_DATALABS_APP_PASSWORD']
req = urllib.request.Request('https://www.datalabsagency.com/wp-json/wp/v2/pages/53915',
    data=json.dumps({'content': page, 'status': 'draft'}).encode(),
    headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
             'Authorization': 'Basic ' + base64.b64encode(f'{user}:{pw}'.encode()).decode()}, method='POST')
print('WP updated:', json.load(urllib.request.urlopen(req))['id'])
print('\nYOAST: SEO TITLE: Intel Case Study: A Power BI Design System | Datalabs')
print('META DESCRIPTION: How the Datalabs Agency built Intel IPG a Power BI design system - a 78-page style guide, 13 dashboard designs on one nine-module grid, and a trained team.')
