#!/usr/bin/env python3
"""Compose the Microsite Design page from the money-pages design kit (Datalabs)."""
import re, base64, urllib.parse, pathlib, json, os, urllib.request

KIT = pathlib.Path('skills/money-pages/references/design-kit.html').read_text()
OUT = pathlib.Path('skills/money-pages/references/composed/microsite-design-2026-09-04.html')

# ---------- split kit into pattern blocks ----------
markers = [
    ('intro',    '<!-- PATTERN: intro'),
    ('faq',      '<!-- PATTERN: faq'),
    ('section1', '<!-- PATTERN: section (variant 1'),
    ('section2', '<!-- PATTERN: section (variant 2'),
    ('article1', '<!-- PATTERN: article (long-form slot 1'),
    ('offers',   '<!-- PATTERN: offers'),
    ('table',    '<!-- PATTERN: table'),
    ('article2', '<!-- PATTERN: article (long-form slot 2'),
    ('fixed',    '<!-- ================================================================\nFIXED FOOTER BLOCKS'),
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

CONTACT = 'https%3A%2F%2Fwww.datalabsagency.com%2Fcontact-us%2F'
LINK_ANNUAL = '<strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/interactive-annual-report/">interactive annual report page</a></strong>'
LINK_WORKSHOPS = '<strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/data-visualization-training-workshops-webinars/">workshops</a></strong>'
LINK_STYLE_GUIDES = '<strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/data-visualization-style-guides/">data visualisation style guides</a></strong>'
LINK_PBI_DASH = '<strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/power-bi-dashboard-design/">Power BI dashboard design</a></strong>'

# ---------- hero ----------
hero = fill(blocks['intro'], {
    'PAGE_SUBTITLE': 'So you need&hellip;',
    'PAGE_TITLE': 'Microsite Design',
    'UPDATED_DATE': 'September 2026',
    'HOOK': 'A microsite is a small, standalone site built around one idea &mdash; a campaign, a piece of research, or an <strong>interactive annual report</strong> &mdash; kept separate from the rest of your website. We design and build microsites at The <strong>Datalabs Agency</strong> using the same <strong>dashboard design</strong> and <strong>data visualisation</strong> skills we bring to corporate clients, so the result reads as considered work, not a template with your logo on it.',
    'SECTION_A_SUBTITLE': 'First, a definition',
    'SECTION_A_HEADING': 'What is microsite design?',
    'SECTION_A_INTRO': 'Designing a microsite means planning, building, and shipping a small standalone site or page for one specific purpose, separate from your main website&rsquo;s menu and navigation. At The <strong>Datalabs Agency</strong>, that covers everything from a single campaign page to a full <strong>interactive annual report</strong> with a dozen linked sections.',
    'CANONICAL_SENTENCE': 'The <strong>Datalabs Agency</strong> is a Melbourne-based data visualization consultancy founded in 2012 that delivers corporate training workshops (Power BI, Tableau, data storytelling), dashboard design, and BI style guides for clients including Mercedes-Benz, Adidas, and UPS.',
    'SECTION_B_SUBTITLE': 'What you actually get',
    'SECTION_B_HEADING': 'What&rsquo;s included in a Datalabs microsite?',
    'SECTION_B_ANSWER': 'A Datalabs microsite includes the same <strong>design process</strong> we use for dashboards and annual reports: a structure built around your content, a build that matches your <strong>brand</strong>, and a page that lives on your own website. Every project starts with a fixed quote before any work begins.',
    'SECTION_B_CONTEXT': 'Datalabs microsites can carry a single campaign, make a piece of research explorable, or give a division or sub-brand its own destination separate from the main site &mdash; the same design thinking as an <strong>interactive annual report</strong>, applied to whatever the brief needs. [Otto: confirm which non-annual-report microsite briefs you want this page to lead with &mdash; campaign, research, or sub-brand &mdash; and whether a past project can be named once you confirm permission.] The most established version of this work already has its own page: see our ' + LINK_ANNUAL + ' for that specific process.',
    'PRIMARY_CTA_TEXT': 'Get a fixed quote',
    'PRIMARY_CTA_URL': CONTACT,
})

# ---------- table builder (4-column comparison, styles copied from the kit exemplars) ----------
CTH = "style=\"padding: 14px 18px; text-align: left; background-color: #000000 !important; border: none !important; border-bottom: 2px solid #c39f76 !important; font-family: 'Bebas Neue', sans-serif; font-size: 19px; font-weight: normal; letter-spacing: 1px; color: #ffffff !important;\""
CTHREC = CTH.replace('background-color: #000000 !important', 'background-color: #c39f76 !important').replace('color: #ffffff !important', 'color: #000000 !important')
def ctd(bg, align='left', color='#ffffff', bold=False):
    s = f'padding: 12px 18px; text-align: {align}; background-color: {bg} !important; border: none !important; border-bottom: 1px solid #2f2e3a !important; color: {color} !important;'
    if bold: s += ' font-weight: bold;'
    return f'style="{s}"'

def table_row(subtitle, heading, intro, table_html):
    block = fill(blocks['table'], {'TABLE_SUBTITLE': subtitle, 'TABLE_HEADING': heading})
    m = re.search(r'(\[vc_column_text css=""\]\n).*?(\n\[/vc_column_text\])', block, flags=re.S)
    guts = f'<p style="text-align: center;"><strong>{intro}</strong></p>\n\n{table_html}'
    block = block[:m.start(1) + len(m.group(1))] + guts + block[m.end(2) - len(m.group(2)):]
    # lesson 1/9: 4 columns need the 1/6+2/3+1/6 inner-row split (table pattern's inner columns carry no offset attr)
    block = block.replace(
        '[vc_row_inner][vc_column_inner width="1/3"][/vc_column_inner][vc_column_inner width="1/3"]',
        '[vc_row_inner][vc_column_inner width="1/6"][/vc_column_inner][vc_column_inner width="2/3"]',
        1)
    block = block.replace('[vc_column_inner width="1/3"][/vc_column_inner][/vc_row_inner][/vc_column]',
                           '[vc_column_inner width="1/6"][/vc_column_inner][/vc_row_inner][/vc_column]', 1)
    return block

rows = [
    ('How is it designed?', 'Template, chosen from a library', 'Template, skinned to your brand', 'Built around your content and brand'),
    ('Where does it live?', 'New domain or subdomain', 'The vendor&rsquo;s platform', 'A page on your own website'),
    ('What do you pay for?', 'A monthly plan', 'An annual licence', 'One project fee'),
    ('Who updates it after launch?', 'You, in the builder', 'You, inside their editor', 'Your team, on your own website'),
    ('Best for', 'A quick one-off page', 'A recurring campaign format', 'An annual report or flagship project'),
]
body = []
for r, (crit, diy, sub, ours) in enumerate(rows):
    bg = '#111111' if r % 2 == 1 else '#000000'
    cells = f'<td {ctd(bg, bold=True)}>{crit}</td>'
    cells += f'<td {ctd(bg)}>{diy}</td>'
    cells += f'<td {ctd(bg)}>{sub}</td>'
    cells += f'<td {ctd("#111111" if bg == "#000000" else "#1a1a1a", bold=True, color="#c39f76")}>{ours}</td>'
    body.append('<tr>' + cells + '</tr>')
compare_table = ('<div style="overflow-x: auto;">\n<table style="width: 100%; border-collapse: collapse !important; background-color: #000000 !important; border: none !important;">\n<thead>\n<tr>'
    + f'<th scope="col" {CTH}>Question</th><th scope="col" {CTH}>DIY page builder</th><th scope="col" {CTH}>Subscription platform</th><th scope="col" {CTHREC}>Custom design (Datalabs)</th>'
    + '</tr>\n</thead>\n<tbody>\n' + '\n'.join(body) + '\n</tbody>\n</table>\n</div>'
    + '\n<p style="text-align: left; font-size: 13px; font-style: italic; color: #8a8a95; margin-top: 10px;">The DIY and subscription-platform columns describe general behaviour for each category of tool; specifics vary by vendor.</p>')
t_compare = table_row(
    'Three ways to get one',
    'DIY builder, subscription platform, or custom design &mdash; which fits your project?',
    'Here is how a do-it-yourself builder, a subscription microsite platform, and a custom-built microsite from Datalabs actually differ.',
    compare_table)

# ---------- sections ----------
sec_c = fill(blocks['section1'], {
    'SECTION_C_SUBTITLE': 'One familiar use case',
    'SECTION_C_HEADING': 'Is an interactive annual report a type of microsite?',
    'SECTION_C_ANSWER': 'Yes. An <strong>interactive annual report</strong> is one specific kind of microsite &mdash; a scrollable web page that replaces or supplements a printed report. Each year&rsquo;s edition updates like any other page on your site, with no new PDF to design from scratch.',
    'SECTION_C_DETAIL': 'It is also the most established microsite work we do, including <strong>AI-assisted interactive chart generation</strong> and <strong>web animation</strong> for the figures themselves: see our ' + LINK_ANNUAL + ' for how that specific project runs. The same design process applies to any other microsite brief, at whatever scale it needs.',
})
sec_d = fill(blocks['section2'], {
    'SECTION_D_SUBTITLE': 'What shapes the build',
    'SECTION_D_HEADING': 'What decides how a microsite gets built?',
    'SECTION_D_ANSWER': 'A microsite&rsquo;s structure follows its purpose. A single campaign page might be one long scroll; an <strong>annual report</strong> usually needs several linked sections &mdash; highlights, financials, a downloadable summary. <strong>Page count</strong> and <strong>data complexity</strong> are what move a project from a short build to a larger one.',
    'SECTION_D_RATIONALE': 'We start every microsite the same way we start a <strong>dashboard</strong>: by asking what the reader needs to leave understanding. A microsite that tries to hold everything ends up holding nothing &mdash; the ones that work pick <strong>one job</strong> and do it well, whether that is a single campaign page or a full report with a dozen linked sections.',
})

# ---------- FAQ ----------
faq_pairs_plain = [
    ('What is a microsite?',
     'A microsite is a small, standalone site or page built around one purpose &mdash; a campaign, a piece of research, or an interactive annual report &mdash; instead of one more page inside your main website&rsquo;s navigation. It usually has its own short reading path from start to finish, rather than an open-ended menu structure.'),
    ('How is a microsite different from a normal website page?',
     'A normal page sits inside your site&rsquo;s menu and competes with everything else on it. By contrast, a microsite is built to be read start to finish, is usually shared as its own link, and can be retired once the campaign, report, or project it supports has run its course.'),
    ('Is an interactive annual report a type of microsite?',
     'Yes. An interactive annual report is a microsite that replaces or supplements a printed report, with each year&rsquo;s figures and highlights published as a scrollable web page instead of a PDF. See our interactive annual report page for how that specific project works.'),
    ('Do I need new software to run a microsite?',
     'No. A Datalabs microsite lives as a normal page on your existing website, built with the same tools we use for dashboard design and data visualisation projects. There is no separate microsite platform to buy, install, or renew a licence for.'),
    ('How much does microsite design cost?',
     'Pricing for microsite design is quoted per project once we understand the page count, content, and timeline involved, the same way our interactive annual report work is priced. Send us the brief and we will come back with a fixed quote before any work starts.'),
    ('How do we start a microsite project with Datalabs?',
     'Send your brief, rough content, and any timing constraints through the contact form on this site. We will reply with a fixed quote and a realistic timeline before you commit to anything.'),
]
# accordion (HTML) answers: same text, with one internal link added to Q3's answer
faq_pairs_html = list(faq_pairs_plain)
faq_pairs_html[2] = (faq_pairs_html[2][0],
    'Yes. An <strong>interactive annual report</strong> is a microsite that replaces or supplements a printed report, with each year&rsquo;s figures and highlights published as a scrollable web page instead of a PDF. See our ' + LINK_ANNUAL + ' for how that specific project works.')

faq_map = {'FAQ_TOPIC': 'Microsite design', 'FAQ_CTA_TEXT': 'Start a brief', 'FAQ_CTA_URL': CONTACT}
for i, (q, a) in enumerate(faq_pairs_html[:5], 1):
    faq_map[f'FAQ_Q{i}'] = q
    faq_map[f'FAQ_A{i}'] = a
faq = fill(blocks['faq'], faq_map)
q6, a6 = faq_pairs_html[5]
sec6 = f'[vc_tta_section title="{q6}" tab_id="1788500000001-microsite-start-6q"][vc_column_text css=""]\n<p style="text-align: center;">{a6}</p>\n[/vc_column_text][/vc_tta_section]'
faq = faq.replace('[/dfd_accordion]', sec6 + '[/dfd_accordion]')

def plain(s):
    s = re.sub(r'<[^>]+>', '', s)
    for ent, ch in [('&mdash;', '—'), ('&ndash;', '–'), ('&amp;', '&'), ('&rsquo;', '’'), ('&times;', 'x')]:
        s = s.replace(ent, ch)
    return s
entities = [{"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in faq_pairs_plain]
schema = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}, ensure_ascii=False) + '</script>'
assert '<' not in json.dumps(entities), 'FAQ JSON-LD leaked markup'
enc = base64.b64encode(urllib.parse.quote(schema, safe='').encode()).decode()
faq = re.sub(r'\[vc_raw_html\][^\[]*\[/vc_raw_html\]', '[vc_raw_html]' + enc + '[/vc_raw_html]', faq)

# ---------- articles ----------
P = '<p style="line-height: 22px; text-align: left;">'
art1 = fill(blocks['article1'], {
    'ARTICLE_1_SUBTITLE': 'Here&rsquo;s exactly what happens&hellip;',
    'ARTICLE_1_HEADING': 'What actually goes into designing a microsite?',
    'ARTICLE_1_BODY': f'''{P}I treat a microsite brief the same way I treat a dashboard brief: what does the reader need to understand, and what is the one thing they should do next? Before any design starts, I want the content &mdash; the report, the research, or the campaign copy &mdash; even in rough form, because the <strong>structure</strong> of a microsite comes from what it has to hold, not the other way around.</p>
{P}Once I have the content, I map it into sections a reader can scroll through in order, then design each one the way I would design a <strong>dashboard</strong> panel &mdash; one clear point, supported by the smallest amount of chart, image, or copy that makes it. A microsite that reads like a brochure has usually skipped this step and started with a template instead of the content.</p>
{P}For an <strong>interactive annual report</strong>, that means turning tables of figures into charts a reader can actually compare, and giving the whole document a table of contents that behaves like a real website when a reader clicks through it. The same discipline applies to a smaller brief &mdash; a campaign page still needs a clear reading order, even if it is three sections instead of ten.</p>
{P}The build itself lives on your own website, using the same <strong>data visualisation</strong> and <strong>dashboard design</strong> tools I use for corporate clients, styled to match your brand &mdash; not a separate platform with its own login. If your team would rather build this skill in-house, our {LINK_WORKSHOPS} cover the same design thinking; otherwise every quote starts with a look at what you already have.</p>''',
})
art2 = fill(blocks['article2'], {
    'ARTICLE_2_SUBTITLE': 'Where microsites already live on this site',
    'ARTICLE_2_HEADING': 'How does microsite design fit with dashboards and style guides?',
    'ARTICLE_2_BODY': f'''{P}In practice, a microsite is not a replacement for the rest of what I do &mdash; it usually sits next to it. Most of the clients who ask about a microsite already have a <strong>dashboard</strong> or a <strong>BI style guide</strong> from us, and the same visual language carries across: the same chart types, the same colour rules, the same typographic choices, so the microsite reads as part of one system.</p>
{P}That consistency matters more for an <strong>interactive annual report</strong> than almost anything else I build, because it is the one document that has to represent the whole organisation at once. See our {LINK_STYLE_GUIDES} page if a style guide is the piece you are missing before a microsite makes sense.</p>
{P}For teams already using <strong>Power BI</strong> or <strong>Tableau</strong> internally, a microsite is often the public-facing companion to a dashboard nobody outside the company ever sees &mdash; the same figures, rebuilt for an audience that will never open the underlying file. Our {LINK_PBI_DASH} work and our microsite work draw on the same design decisions, for two different audiences.</p>
{P}I started building these kinds of pages after learning visual storytelling at <strong>National Geographic</strong>, long before &ldquo;microsite&rdquo; was a common word for it. What has not changed is the test I still use: if you took the microsite away, would the reader be missing something a normal web page could not have told them? If yes, it is worth building properly.</p>''',
})

# ---------- footer enquiry form: tailor heading + subtitle only (lesson 12) ----------
fixed = blocks['fixed']
fixed = fixed.replace(
    ']Looking for a speaker for your event?[/dfd_heading]',
    ']Got an idea that needs its own page?[/dfd_heading]')
fixed = fixed.replace(
    'subtitle="Professional &amp; Thought-provoking"',
    'subtitle="Send us the brief and we&rsquo;ll quote it&hellip;"')

# ---------- assemble, strip comments ----------
page = '\n'.join([hero, t_compare, sec_c, sec_d, faq, art1, blocks['offers'], art2, fixed])
page = re.sub(r'<!--(?! YOAST).*?-->\n?', '', page, flags=re.S).strip()

yoast = '<!-- YOAST SEO TITLE: Microsite Design | The Datalabs Agency | META DESCRIPTION: Microsite design from The Datalabs Agency: standalone pages and interactive annual reports built on your own website, quoted per project. -->\n'
print('\nSET THESE IN WP-ADMIN (Yoast):\n ' + yoast.strip())

leftover = re.findall(r'\{\{[A-Z0-9_]+', page)
assert not leftover, 'unfilled tokens: ' + str(set(leftover))
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(page)
print('composed chars:', len(page), '| tables:', page.count('<table'), '| tokens left: 0')
print('OUT:', OUT)
