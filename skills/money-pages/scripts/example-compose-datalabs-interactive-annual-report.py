#!/usr/bin/env python3
"""Compose the Interactive Annual Report money page from the Datalabs design kit."""
import re, base64, urllib.parse, pathlib, json

KIT = pathlib.Path('skills/money-pages/references/design-kit.html').read_text()
OUT = pathlib.Path('skills/money-pages/references/composed/interactive-annual-report-2026-08-25.html')

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

# ---------- widen helpers (design-kit-README lessons 7/8/11: head noun 3+ words -> 1/4+1/2+1/4) ----------
def widen_hero(block):
    block = block.replace(
        'width="1/3" offset="vc_col-lg-4 vc_col-md-2 vc_col-xs-1"',
        'width="1/4" offset="vc_col-lg-3 vc_col-md-2 vc_col-xs-1"')
    block = block.replace(
        'width="1/3" dfd_column_responsive_enable="dfd-column-responsive-enable" offset="vc_col-lg-4 vc_col-md-8 vc_col-xs-10"',
        'width="1/2" dfd_column_responsive_enable="dfd-column-responsive-enable" offset="vc_col-lg-6 vc_col-md-8 vc_col-xs-10"')
    return block

def widen_thirds(block):
    counts = [0]
    order = {1: 'width="1/4"', 2: 'width="1/2"', 3: 'width="1/4"'}
    def repl(m):
        counts[0] += 1
        return order.get(counts[0], m.group(0))
    return re.sub(r'width="1/3"', repl, block)

# ---------- hero ----------
hero_block = widen_hero(blocks['intro'])
hero = fill(hero_block, {
    'PAGE_SUBTITLE': 'Turn your PDF into an&hellip;',
    'PAGE_TITLE': 'Interactive Annual Report',
    'UPDATED_DATE': 'August 2026',
    'HOOK': 'An <strong>interactive annual report</strong> turns your static PDF into a scrollable, on-brand web experience that stakeholders actually explore instead of downloading once and forgetting. Our team at <strong>The Datalabs Agency</strong> designs and builds these reports from the ground up &mdash; no annual-report software subscription to buy, no plug-in to install, just a page on your own site you can update every year.',
    'SECTION_A_SUBTITLE': 'A clear definition first',
    'SECTION_A_HEADING': 'What is an interactive annual report?',
    'SECTION_A_INTRO': 'An <strong>interactive annual report</strong> is a <strong>scrollable web page or microsite</strong> that presents a company&rsquo;s yearly results, highlights, and data instead of, or alongside, a printed or PDF report. Readers click and scroll through sections instead of downloading a file, and every chart, photo, and figure can be swapped out the following year without a new print run.',
    'CANONICAL_SENTENCE': 'The Datalabs Agency is a Melbourne-based data visualization consultancy founded in 2012 that delivers corporate training workshops (Power BI, Tableau, data storytelling), dashboard design, and BI style guides for clients including Mercedes-Benz, Adidas, and UPS.',
    'SECTION_B_SUBTITLE': 'No new platform to learn',
    'SECTION_B_HEADING': 'Do you need special software for an interactive annual report?',
    'SECTION_B_ANSWER': 'No. This lives as a normal page on your existing website. There is no separate <strong>annual-report software</strong> to buy, install, or renew a licence for &mdash; <strong>The Datalabs Agency</strong> designs and builds the page directly, so there is nothing new for your investor relations or communications team to learn.',
    'SECTION_B_CONTEXT': 'Searches for &ldquo;annual report software&rdquo; usually mean one of two things: a flipbook tool that turns a PDF into a page-turning animation, or a dedicated microsite platform with its own subscription and login. Both add an ongoing licence fee and a separate system for your team to manage alongside your main website. Our approach at <strong>The Datalabs Agency</strong> is different: we design the report as pages that live on your own domain, built with the same <strong>data visualization</strong> and <strong>dashboard design</strong> skills we use for corporate clients. That means one website to maintain, one login your communications team already has, and no annual software renewal beyond your normal hosting costs.',
    'PRIMARY_CTA_TEXT': 'Discuss your report',
    'PRIMARY_CTA_URL': CONTACT,
})

# ---------- table helpers (kit comparison exemplar styling, copied exactly) ----------
TH = "style=\"padding: 14px 18px; text-align: left; background-color: #000000 !important; border: none !important; border-bottom: 2px solid #c39f76 !important; font-family: 'Bebas Neue', sans-serif; font-size: 21px; font-weight: normal; letter-spacing: 1px; color: #ffffff !important; white-space: nowrap;\""
TH_REC = TH.replace('background-color: #000000 !important', 'background-color: #c39f76 !important').replace('color: #ffffff !important', 'color: #000000 !important')
def td(bg, align='left', color='#ffffff', bold=False):
    s = f'padding: 12px 18px; text-align: {align}; background-color: {bg} !important; border: none !important; border-bottom: 1px solid #2f2e3a !important; color: {color} !important;'
    if bold: s += ' font-weight: bold;'
    return f'style="{s}"'

def comparison_table(option_headers, rows, recommended_idx, footnote=None):
    ths = f'<th scope="col" {TH}>Criterion</th>'
    for i, h in enumerate(option_headers):
        ths += f'<th scope="col" {TH_REC if i == recommended_idx else TH}>{h}</th>'
    body = []
    for crit, cells in rows:
        row = f'<td {td("#000000", bold=True)}>{crit}</td>'
        for i, val in enumerate(cells):
            bg = '#111111' if i == recommended_idx else '#000000'
            if val is True:
                row += f'<td {td(bg, "center", "#c39f76", bold=True)}>&#10003;</td>'
            elif val is None:
                row += f'<td {td(bg, "center", "#8a8a95")}>&mdash;</td>'
            else:
                row += f'<td {td(bg)}>{val}</td>'
        body.append('<tr>' + row + '</tr>')
    fn = f'\n<p style="text-align: left; font-size: 13px; font-style: italic; color: #8a8a95; margin-top: 10px;">{footnote}</p>' if footnote else ''
    return ('<div style="overflow-x: auto;">\n<table style="width: 100%; border-collapse: collapse !important; background-color: #000000 !important; border: none !important;">\n'
            f'<thead>\n<tr>{ths}</tr>\n</thead>\n<tbody>\n' + '\n'.join(body) + '\n</tbody>\n</table>\n</div>' + fn)

def table_row(subtitle, heading, intro, table_html):
    block = fill(blocks['table'], {'TABLE_SUBTITLE': subtitle, 'TABLE_HEADING': heading})
    m = re.search(r'(\[vc_column_text css=""\]\n).*?(\n\[/vc_column_text\])', block, flags=re.S)
    guts = f'<p style="text-align: center;">{intro}</p>\n\n{table_html}'
    return block[:m.start(1) + len(m.group(1))] + guts + block[m.end(2) - len(m.group(2)):]

t_static = table_row(
    'Side by side', 'Static PDF or interactive annual report &mdash; what actually changes?',
    'Here is how a printed or PDF annual report compares with an interactive, web-based version:',
    comparison_table(
        ['Static PDF report', 'Interactive annual report'],
        [('Format', ['Single downloadable file', 'Pages on your own website']),
         ('Updating after publish', ['New file, new distribution round', 'Edited any time']),
         ('Resizes for mobile screens', [None, True]),
         ('Interactive charts', [None, True]),
         ('Direct link to one section', [None, True]),
         ('Ongoing cost model', ['Print and distribution each year', 'One design cost, hosted on your site'])],
        recommended_idx=1,
        footnote='Both formats can exist together &mdash; many organisations keep a downloadable PDF for compliance filing alongside the interactive version for everyone else.'))

t_software = table_row(
    'The other option', 'Annual report software or a custom-built report &mdash; which fits?',
    'If you are weighing a dedicated annual-report platform against a custom page, here is what differs:',
    comparison_table(
        ['Annual report software', 'Custom build (Datalabs)'],
        [('Ongoing cost', ['Subscription or per-report licence fee', 'One-off design cost, hosted on your own site']),
         ('Design', ['Template-based, shared with other users', 'Built to your brand, nothing else looks the same']),
         ('Where it lives', ["Vendor's platform, separate login", 'Your own domain, alongside your main site']),
         ('Data visualisation', ['Basic charts built into the template', 'Full dashboard-design expertise applied to your data']),
         ('Who maintains it', ["Vendor's support team", 'The Datalabs Agency, then your own team'])],
        recommended_idx=1,
        footnote='Annual-report software pricing is set by each vendor and varies by report length and user count &mdash; confirm current rates directly with the provider before comparing.'))

# ---------- sections (variant 1: answer + detail with internal link) ----------
sec1_block = widen_thirds(blocks['section1'])
sec_convert = fill(sec1_block, {
    'SECTION_C_SUBTITLE': 'From existing PDF to web',
    'SECTION_C_HEADING': 'Can you convert our existing PDF annual report?',
    'SECTION_C_ANSWER': 'Yes. We take the content, data, and design of your current PDF or print annual report and rebuild it as a <strong>scrollable web experience</strong>, keeping your existing <strong>brand guidelines</strong>, colour palette, and typography so the interactive version still looks like your report instead of a generic template.',
    'SECTION_C_DETAIL': 'This sits alongside your other reporting assets &mdash; see examples of the format in our <strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/digital-annual-reports-microsites/">digital annual reports and microsites</a></strong> portfolio, where past interactive and microsite reports are gathered in one place.',
})
sec_accessible = fill(widen_thirds(blocks['section1']), {
    'SECTION_C_SUBTITLE': 'Everyone can read it',
    'SECTION_C_HEADING': 'Is an interactive annual report accessible on mobile and to screen readers?',
    'SECTION_C_ANSWER': 'Yes. Every interactive annual report we build <strong>resizes automatically</strong> for phones and tablets, and we structure headings, alt text, and reading order so <strong>screen readers</strong> can follow the same content sighted readers see. Nothing depends on a plug-in your reader has to install first.',
    'SECTION_C_DETAIL': 'That discipline comes from the same design process we teach in our <strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/data-visualization-training-workshops-webinars/infographics-report-design-workshop/">infographics and report design workshop</a></strong> &mdash; layout, colour, and hierarchy principles applied to every interactive report we build.',
})

# ---------- section (variant 2: answer + rationale) ----------
sec_cost = fill(widen_thirds(blocks['section2']), {
    'SECTION_D_SUBTITLE': 'What moves the number',
    'SECTION_D_HEADING': 'What determines the cost of an interactive annual report?',
    'SECTION_D_ANSWER': 'Cost depends on how many sections the report needs, how much of your existing PDF content and data can be reused, and how much custom illustration or interactive charting you want. Design work is billed at our published <strong>data visualisation consulting rate of $250 per hour</strong>, quoted as a fixed project total once we know your report&rsquo;s scope.',
    'SECTION_D_RATIONALE': 'We price this way because no two annual reports start from the same place &mdash; a report with clean data and a recent PDF to rebuild from takes far less time than one built from scratch with fresh data visualisation and custom illustration throughout. An hourly rate quoted as a <strong>fixed total</strong> means you see the real number before committing, instead of a flat package price that overcharges the simple projects or undercharges the complex ones. [Otto: confirm a typical total-hours range or starting project price for an interactive annual report so we can add a ballpark figure here.]',
})

# ---------- FAQ ----------
faq_pairs = [
    ('What is an interactive annual report?',
     'An interactive annual report is a scrollable web page or microsite that presents a company’s yearly results and highlights instead of a printed or PDF document. Readers explore it in a browser, and it can be updated at any time, without a reprint.'),
    ('Do I need annual report software to publish one?',
     'No. The report is built as pages on your own website instead of a separate platform with its own subscription or login. We design and build it directly, so there is no extra software for your team to manage.'),
    ('Can you turn our existing PDF annual report into an interactive one?',
     'Yes. We rebuild the content, data, and design of your current PDF or print annual report as a web experience, keeping your existing brand colours and typography so the interactive version still reads as your report.'),
    ('How much does an interactive annual report cost?',
     'Design work is billed at our published data visualisation consulting rate of $250 per hour, quoted as a fixed project total once we know your report’s scope and how much existing content can be reused. Contact us for a quote based on your report.'),
    ('How long does an interactive annual report project take?',
     'Timelines depend on how many sections the report needs and how much of your existing content and data visualisation work can be reused. Contact us with your report’s scope and we will give you a project timeline before you commit to anything.'),
    ('Will it work on mobile devices?',
     'Yes. Every interactive annual report we build resizes automatically for phones and tablets, and headings and alt text are structured so screen readers can follow the same content as sighted readers, with nothing to install first.'),
]
faq_map = {'FAQ_TOPIC': 'Interactive annual reports', 'FAQ_CTA_TEXT': 'Discuss your report', 'FAQ_CTA_URL': CONTACT}
for i, (q, a) in enumerate(faq_pairs, 1):
    faq_map[f'FAQ_Q{i}'] = q
    faq_map[f'FAQ_A{i}'] = a
faq = fill(blocks['faq'], faq_map)
q6, a6 = faq_pairs[5]
sec6 = f'[vc_tta_section title="{q6}" tab_id="1787644800001-mobile-6q"][vc_column_text css=""]\n<p style="text-align: center;">{a6}</p>\n[/vc_column_text][/vc_tta_section]'
faq = faq.replace('[/dfd_accordion]', sec6 + '[/dfd_accordion]')

def plain(s):
    s = re.sub(r'<[^>]+>', '', s)
    for ent, ch in [('&mdash;', '—'), ('&ndash;', '–'), ('&amp;', '&'), ('&rsquo;', '’'), ('&ldquo;', '“'), ('&rdquo;', '”')]:
        s = s.replace(ent, ch)
    return s
entities = [{"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in faq_pairs]
schema = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}, ensure_ascii=False) + '</script>'
assert '<' not in json.dumps([e['acceptedAnswer']['text'] for e in entities]) or True  # sanity placeholder
for e in entities:
    assert '<' not in e['acceptedAnswer']['text'], e
enc = base64.b64encode(urllib.parse.quote(schema, safe='').encode()).decode()
faq = re.sub(r'\[vc_raw_html\][^\[]*\[/vc_raw_html\]', '[vc_raw_html]' + enc + '[/vc_raw_html]', faq)

# ---------- articles (first-person Otto voice, two-column split past ~4 paragraphs) ----------
P = '<p style="line-height: 22px; text-align: left;">'

def two_col(paragraphs, split):
    left = '\n'.join(paragraphs[:split])
    right = '\n'.join(paragraphs[split:])
    return ('[vc_row_inner][vc_column_inner width="1/2"][vc_column_text css=""]\n' + left + '\n[/vc_column_text][/vc_column_inner]'
            '[vc_column_inner width="1/2"][vc_column_text css=""]\n' + right + '\n[/vc_column_text][/vc_column_inner][/vc_row_inner]')

def insert_body(block, token_name, html):
    pattern = r'\[vc_column_text css=""\]\n\{\{' + token_name + r'(:[^}]*)?\}\}\n\[/vc_column_text\]'
    return re.sub(pattern, html.replace('\\', r'\\'), block, count=1)

art1_paras = [
    f'{P}I have spent more than a decade designing how organisations present their own data, and a PDF is one of the worst formats for it. A PDF is built to be printed, not read on a screen &mdash; it fights you on a phone, it cannot be updated once it is out, and every chart inside it is a flat image no one can explore further. An <strong>interactive annual report</strong> fixes all three problems by being what it actually is: a web page.</p>',
    f'{P}I started thinking about visual storytelling at the <strong>National Geographic Society</strong>, where the whole point was making a reader stop and look closer at something they would otherwise skim past. An annual report faces the same problem &mdash; most readers open it once, skim the summary, and never touch the detailed numbers. A scrollable, well-designed web version invites the kind of closer look a stapled PDF never gets.</p>',
    f'{P}The brief is usually the same: take a year&rsquo;s worth of results, decide which numbers deserve a chart and which deserve a sentence, and build a structure a stakeholder can navigate in under a minute. That is <strong>dashboard design</strong> work wearing an annual-report hat &mdash; the same principles behind our <strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/power-bi-dashboard-design/">dashboard design</a></strong> projects apply directly to laying out a year&rsquo;s highlights.</p>',
    f'{P}What changes most for clients is what happens after launch. A printed report is finished the day it goes to the printer; a <strong>web-based</strong> one keeps working. We can <strong>swap a stat</strong>, add a late-breaking result, or fix a typo without reprinting a single page or reissuing a file to a distribution list. That flexibility alone is usually what convinces a communications team to make the switch.</p>',
    f'{P}None of this replaces a <strong>compliance filing</strong> &mdash; if your organisation is required to lodge a PDF, keep doing that. What it replaces is <strong>the version most people actually read</strong>: the one your website links to, the one you email to stakeholders, the one that still looks current the day before next year&rsquo;s report goes live.</p>',
]
art1 = fill(blocks['article1'], {
    'ARTICLE_1_SUBTITLE': 'The case for going interactive&hellip;',
    'ARTICLE_1_HEADING': 'Why I design annual reports as pages, not PDFs',
})
art1 = insert_body(art1, 'ARTICLE_1_BODY', two_col(art1_paras, 3))

art2_paras = [
    f'{P}Every interactive annual report I build starts the same way: an audit of what you already have. That means the current PDF or print report, the underlying data behind each chart, your <strong>brand guidelines</strong>, and any photography or illustration you already own. Most of that content is reusable &mdash; the job is restructuring it for a screen instead of a page.</p>',
    f'{P}From there I map the report into sections a reader can jump between: a highlights summary, a letter from leadership, the year&rsquo;s results broken into a handful of charts, and whatever else your organisation reports on. Each section is built to <strong>stand on its own</strong>, because most readers will land on one section from a link or a search instead of starting at page one.</p>',
    f'{P}Charts get rebuilt as fully interactive visualisations instead of embedded images wherever the data supports it, which is where the same <strong>data visualization</strong> discipline behind our corporate <strong>dashboard design</strong> work carries over directly &mdash; choosing the chart type that shows the number honestly, not the one that looks most dramatic.</p>',
    f'{P}Once the structure and charts are in place, the report gets built on your own site instead of a separate platform, so your team keeps one login, one hosting bill, and one place to make next year&rsquo;s update. If you want to see what the finished format looks like, browse our <strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/digital-annual-reports-microsites/">digital annual reports and microsites</a></strong> examples before we start scoping your version.</p>',
    f'{P}The whole point of building it this way is that <strong>year two costs less work than year one</strong>. Once the structure exists, refreshing it each year is largely a <strong>content update</strong>: new numbers, a new highlights section, maybe a new chart &mdash; not a full rebuild from a blank page.</p>',
]
art2 = fill(blocks['article2'], {
    'ARTICLE_2_SUBTITLE': 'The build, step by step',
    'ARTICLE_2_HEADING': 'What actually goes into an interactive annual report',
})
art2 = insert_body(art2, 'ARTICLE_2_BODY', two_col(art2_paras, 3))

# ---------- assemble, strip comments ----------
page = '\n'.join([hero, t_static, sec_convert, sec_cost, t_software, sec_accessible, faq, art1, blocks['offers'], art2, blocks['fixed']])
page = re.sub(r'<!--(?! YOAST).*?-->\n?', '', page, flags=re.S).strip()

leftover = re.findall(r'\{\{[A-Z0-9_]+', page)
assert not leftover, 'unfilled tokens: ' + str(set(leftover))

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(page)

yoast_title = 'Interactive Annual Report Design – The Datalabs Agency'
yoast_meta = 'Turn your PDF annual report into an interactive web report designed by The Datalabs Agency — no annual-report software or licence required.'
print('YOAST SEO TITLE (%d chars): %s' % (len(yoast_title), yoast_title))
print('META DESCRIPTION (%d chars): %s' % (len(yoast_meta), yoast_meta))
print('composed chars:', len(page), '| tables:', page.count('<table'), '| tokens left: 0')
print('internal links:', page.count('dfd-custom-link-decorated'))
print('ellipsis count (&hellip;, excluding fixed furniture):', page.count('&hellip;'))
