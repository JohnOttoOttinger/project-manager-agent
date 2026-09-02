#!/usr/bin/env python3
"""Compose the Marketing Dashboards money page from the money-pages design kit.

Target: "marketing dashboard" (145 impr, pos 91.1) + "marketing dashboards"
(127 impr, pos 70.2) -- combined per Otto's 2026-09-02 shortlist reply "3",
title kept plural per his follow-up ("Marketing Dashboards (plural) would
be better"). Currently mis-served by the 2016 listicle
/2016/11/25/6-best-marketing-dashboards/ (0% page-1 share, do_not_target: []
per next-best-page.py -- no cannibalisation guardrail on this cluster).
"""
import re, base64, urllib.parse, pathlib, json, os, urllib.request

KIT = pathlib.Path('skills/money-pages/references/design-kit.html').read_text()
OUT = pathlib.Path('/tmp/claude-0/-home-user-project-manager-agent/58476b0a-ffa5-59fc-b176-d31131d01048/scratchpad/composed-marketing-dashboards.html')
FINAL_OUT = pathlib.Path('skills/money-pages/references/composed/marketing-dashboards-2026-09-02.html')

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
CANON = ('The <strong>Datalabs Agency</strong> is a Melbourne-based data visualization consultancy '
         'founded in 2012 that delivers corporate training workshops (Power BI, Tableau, data '
         'storytelling), dashboard design, and BI style guides for clients including Mercedes-Benz, '
         'Adidas, and UPS.')

# ---------- hero ----------
hero = fill(blocks['intro'], {
    'PAGE_SUBTITLE': 'So you need&hellip;',
    'PAGE_TITLE': 'Marketing Dashboards',
    'UPDATED_DATE': 'September 2026',
    'HOOK': 'Marketing teams are asked to prove campaign ROI, but the numbers usually live in five separate logins. We design custom marketing dashboards that put campaign performance, traffic, and spend on one screen, built in <strong>Power BI</strong> or <strong>Tableau</strong> around the metrics your team actually reports on.',
    'SECTION_A_SUBTITLE': 'The straight answer',
    'SECTION_A_HEADING': 'What is a marketing dashboard?',
    'SECTION_A_INTRO': 'Campaign, traffic, and spend data usually live in separate logins &mdash; a marketing dashboard puts them on one screen your team actually opens every week. We design these for you, built around your existing data sources in <strong>Power BI</strong>, <strong>Tableau</strong>, or Excel instead of a generic template.',
    'CANONICAL_SENTENCE': CANON,
    'SECTION_B_SUBTITLE': 'Custom vs off-the-shelf',
    'SECTION_B_HEADING': 'How is a custom dashboard different from a template?',
    'SECTION_B_ANSWER': 'A template ships with someone else&rsquo;s chart choices and default metrics. A <strong>custom marketing dashboard</strong> starts from your campaigns, channels, and reporting cadence, so every chart on the page answers <strong>the question your team actually asks</strong> each week.',
    'SECTION_B_CONTEXT': 'Templates are a reasonable starting point for a small team moving off spreadsheets &mdash; our <strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/product/power-bi-templates/">Power BI templates</a></strong> exist for exactly that. A template cannot know that your team tracks cost per lead by channel, or that leadership only cares about three numbers out of a twelve-tab report. A custom-built dashboard is scoped around your actual KPIs and your actual data sources, built to the metrics your team already reports on. That difference matters most once a team outgrows the basics: more campaigns, more channels, and a report that used to take an afternoon to assemble by hand.',
    'PRIMARY_CTA_TEXT': 'Get a dashboard quote',
    'PRIMARY_CTA_URL': CONTACT,
})

# Lesson 7/8: SECTION_B_HEADING runs 52 chars in the hero's 1/3 middle column at 70px Bebas --
# widen the hero row 1/3+1/3+1/3 -> 1/4+1/2+1/4 (offsets too, since the hero columns carry them).
EMPTY_COL_13 = '[vc_column_inner el_class="dfd_col-tablet-12" width="1/3" offset="vc_col-lg-4 vc_col-md-2 vc_col-xs-1"][/vc_column_inner]'
EMPTY_COL_14 = '[vc_column_inner el_class="dfd_col-tablet-12" width="1/4" offset="vc_col-lg-3 vc_col-md-2 vc_col-xs-1"][/vc_column_inner]'
MID_COL_13_OPEN = '[vc_column_inner el_class="dfd_col-tablet-12" width="1/3" dfd_column_responsive_enable="dfd-column-responsive-enable" offset="vc_col-lg-4 vc_col-md-8 vc_col-xs-10"'
MID_COL_12_OPEN = '[vc_column_inner el_class="dfd_col-tablet-12" width="1/2" dfd_column_responsive_enable="dfd-column-responsive-enable" offset="vc_col-lg-6 vc_col-md-8 vc_col-xs-10"'
assert hero.count(EMPTY_COL_13) == 2 and MID_COL_13_OPEN in hero, 'hero column markup shape changed'
hero = hero.replace(EMPTY_COL_13, EMPTY_COL_14).replace(MID_COL_13_OPEN, MID_COL_12_OPEN)

# ---------- table builder (comparison exemplar only -- no marketing-dashboard-specific
# rate card exists, so no pricing exemplar table; see pricing.md and the Dashboard Design
# Services precedent (backlog.md, 25 Aug 2026) for the same honest omission) ----------
CTH = "style=\"padding: 8px 14px; text-align: left; background-color: #000000 !important; border: none !important; border-bottom: 2px solid #c39f76 !important; font-family: 'Bebas Neue', sans-serif; font-size: 19px; font-weight: normal; letter-spacing: 1px; color: #ffffff !important;\""
CTHREC = CTH.replace('background-color: #000000 !important', 'background-color: #c39f76 !important').replace('color: #ffffff !important', 'color: #000000 !important')
def ctd(bg, align='left', color='#ffffff', bold=False):
    s = f'padding: 8px 14px; font-size: 15px; text-align: {align}; background-color: {bg} !important; border: none !important; border-bottom: 1px solid #2f2e3a !important; color: {color} !important;'
    if bold: s += ' font-weight: bold;'
    return f'style="{s}"'
TICK = lambda bg: f'<td {ctd(bg, "center", "#c39f76", bold=True)}>&#10003;</td>'
DASH = lambda bg: f'<td {ctd(bg, "center", "#8a8a95")}>&mdash;</td>'

rows = [
    ('Pricing model', '$1,119&ndash;$1,969 one-off', 'From $4,600 per session', 'Quoted per project'),
    ('Built from your own campaign data', False, False, True),
    ('Who does the building', 'Your team, from a template', 'Your team, after training', 'We build it and hand it over'),
    ('Best for', 'A fast start on standard KPIs', 'Teams who want the skill in-house', 'Marketing teams who want it done for them'),
]
fmt_rows = []
for crit, tpl, wk, custom in rows:
    cells = f'<td {ctd("#000000", bold=True)}>{crit}</td>'
    for val, bg in [(tpl, '#000000'), (wk, '#000000'), (custom, '#111111')]:
        if val is True: cells += TICK(bg)
        elif val is False: cells += DASH(bg)
        else: cells += f'<td {ctd(bg)}>{val}</td>'
    fmt_rows.append('<tr>' + cells + '</tr>')
fmt_table = ('<div style="overflow-x: auto;">\n<table style="width: 100%; border-collapse: collapse !important; background-color: #000000 !important; border: none !important;">\n<thead>\n<tr>'
    + f'<th scope="col" {CTH}>&nbsp;</th><th scope="col" {CTH}>Power BI template</th><th scope="col" {CTH}>Designing Great Dashboards workshop</th><th scope="col" {CTHREC}>Custom marketing dashboard</th>'
    + '</tr>\n</thead>\n<tbody>\n' + '\n'.join(fmt_rows) + '\n</tbody>\n</table>\n</div>'
    + '\n<p style="text-align: left; font-size: 13px; font-style: italic; color: #8a8a95; margin-top: 10px;">Workshop price shown is the remote half-day rate for up to 12 attendees; on-site and full-day rates are on our <strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/data-visualisation-workshop-pricing/">workshop pricing page</a></strong>.</p>')

def table_row(subtitle, heading, intro, table_html):
    block = fill(blocks['table'], {'TABLE_SUBTITLE': subtitle, 'TABLE_HEADING': heading})
    m = re.search(r'(\[vc_column_text css=""\]\n).*?(\n\[/vc_column_text\])', block, flags=re.S)
    guts = f'<p style="text-align: center;"><strong>{intro}</strong></p>\n\n{table_html}'
    return block[:m.start(1) + len(m.group(1))] + guts + block[m.end(2) - len(m.group(2)):]

t_compare = table_row(
    'Compare your options', 'Template, workshop, or custom dashboard &mdash; which fits?',
    'The right option depends on whether you want a dashboard delivered, or the skills to build one yourselves.',
    fmt_table)
# Lesson 1/9: 4 columns overflow the kit's default 1/3 table row -- widen to 1/6+2/3+1/6.
t_compare = t_compare.replace(
    '[vc_column_inner width="1/3"][/vc_column_inner][vc_column_inner width="1/3"][dfd_heading enable_delimiter="" style="style_02" heading_margin="margin-bottom:20px;" subtitle="{{TABLE_SUBTITLE}}"'.replace('{{TABLE_SUBTITLE}}', 'Compare your options'),
    '[vc_column_inner width="1/6"][/vc_column_inner][vc_column_inner width="2/3"][dfd_heading enable_delimiter="" style="style_02" heading_margin="margin-bottom:20px;" subtitle="Compare your options"'
).replace(
    '[/vc_column_text][dfd_spacer screen_wide_resolution="1280" screen_wide_spacer_size="20" screen_normal_resolution="1024" screen_tablet_resolution="800" screen_mobile_resolution="480" screen_normal_spacer_size="20" screen_tablet_spacer_size="20" screen_mobile_spacer_size="20"][/vc_column_inner][vc_column_inner width="1/3"][/vc_column_inner][/vc_row_inner][/vc_column][vc_column][dfd_spacer',
    '[/vc_column_text][dfd_spacer screen_wide_resolution="1280" screen_wide_spacer_size="20" screen_normal_resolution="1024" screen_tablet_resolution="800" screen_mobile_resolution="480" screen_normal_spacer_size="20" screen_tablet_spacer_size="20" screen_mobile_spacer_size="20"][/vc_column_inner][vc_column_inner width="1/6"][/vc_column_inner][/vc_row_inner][/vc_column][vc_column][dfd_spacer',
    1
)

# ---------- sections ----------
def widen_section_row(block, label):
    # Lesson 7: no offset attr on these inner columns, so a plain width swap is enough
    # (matches the table row's behaviour in lesson 1). SECTION_C/D headings run 37/50 chars.
    n = block.count('[vc_column_inner width="1/3"]')
    assert n == 3, f'{label}: expected 3 x 1/3 inner columns, found {n}'
    parts = block.split('[vc_column_inner width="1/3"]')
    return '[vc_column_inner width="1/4"]'.join(parts[:2]) + '[vc_column_inner width="1/2"]' + '[vc_column_inner width="1/4"]'.join(parts[2:])

sec_c = fill(blocks['section1'], {
    'SECTION_C_SUBTITLE': 'Built around your channels',
    'SECTION_C_HEADING': 'What goes into a marketing dashboard?',
    'SECTION_C_ANSWER': 'Campaign performance, website traffic, spend against budget, and channel comparison usually sit side by side on a <strong>marketing dashboard</strong>. We choose the chart types and layout around <strong>the decisions your team makes each week</strong>, instead of a fixed set of default widgets.',
    'SECTION_C_DETAIL': 'This follows the same process behind our wider <strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/dashboard-design-services/">dashboard design service</a></strong>: sketch the layout before styling it, then build in whichever tool your data already lives in.',
})
sec_c = widen_section_row(sec_c, 'section1')

sec_d = fill(blocks['section2'], {
    'SECTION_D_SUBTITLE': 'Marketing has its own KPIs',
    'SECTION_D_HEADING': 'How is this different from a general BI dashboard?',
    'SECTION_D_ANSWER': 'Marketing gets <strong>its own dashboard</strong> because its metrics change weekly: campaign, traffic, and spend numbers your team actually reports on. A general BI dashboard usually mixes finance, operations, and sales metrics that <strong>only a few people ever open</strong>.',
    'SECTION_D_RATIONALE': 'Scoping a dashboard to one function is <strong>a design decision</strong>. A dashboard trying to serve marketing, finance, and operations at once tends to serve none of them well &mdash; too many metrics compete for the same screen, and nobody can find the one number they actually track that week. Building a <strong>marketing-specific view</strong> means every chart on the page answers a question a marketer actually asks.',
})
sec_d = widen_section_row(sec_d, 'section2')

# ---------- FAQ ----------
faq_pairs = [
    ('What is a marketing dashboard?',
     'Think of a marketing dashboard as one screen for the campaign performance, website traffic, and spend data that usually sits in separate platforms and logins. Instead of rebuilding a report every month, your team opens a dashboard that already reflects your <strong>Power BI</strong>, <strong>Tableau</strong>, or Excel data, however you already track it.'),
    ('What platforms do you build marketing dashboards in?',
     'Your dashboard goes wherever your data already lives, most commonly <strong>Power BI</strong>, <strong>Tableau</strong>, or Excel. The goal is a dashboard your team keeps using, built around your existing reporting tools.'),
    ('How much does a custom marketing dashboard cost?',
     'There is no single marketing-dashboard rate card &mdash; every build is scoped to your data sources and KPIs and quoted as a fixed project cost once we understand the brief. The closest published reference points are our <strong>$250 per hour</strong> data visualisation consulting rate and the <strong>$3,000 to $8,000 per workshop day</strong> range for a facilitated build session; ask for a quote for your specific dashboard.'),
    ('Do you offer a workshop instead of a custom build?',
     'Yes. If you want the skill in-house, our <strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/data-visualization-training-workshops-webinars/designing-great-business-dashboards-workshop/">Designing Great Dashboards</a></strong> workshop teaches the same design principles as a live team session, starting at <strong>$4,600</strong> for a remote half-day.'),
    ('Can you build the dashboard around our existing campaign data?',
     'Yes. We connect the dashboard to your existing data sources and reporting tools instead of asking you to change how your team already tracks campaigns. That is the difference between a template and a dashboard built for your channels specifically.'),
]
faq_map = {'FAQ_TOPIC': 'Marketing dashboards', 'FAQ_CTA_TEXT': 'Get a dashboard quote', 'FAQ_CTA_URL': CONTACT}
for i, (q, a) in enumerate(faq_pairs, 1):
    faq_map[f'FAQ_Q{i}'] = q
    faq_map[f'FAQ_A{i}'] = a
faq = fill(blocks['faq'], faq_map)

def plain(s):
    s = re.sub(r'<[^>]+>', '', s)
    for ent, ch in [('&mdash;', '—'), ('&ndash;', '–'), ('&amp;', '&'), ('&rsquo;', '’'), ('&times;', 'x')]:
        s = s.replace(ent, ch)
    return s
entities = [{"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in faq_pairs]
schema = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}, ensure_ascii=False) + '</script>'
assert '<' not in json.dumps([e['acceptedAnswer']['text'] for e in entities]).replace('\\u003c', '<')[2:-2] or True  # sanity placeholder
for e in entities:
    assert '<' not in e['name'] and '<' not in e['acceptedAnswer']['text'], 'markup leaked into FAQPage JSON-LD'
enc = base64.b64encode(urllib.parse.quote(schema, safe='').encode()).decode()
faq = re.sub(r'\[vc_raw_html\][^\[]*\[/vc_raw_html\]', '[vc_raw_html]' + enc + '[/vc_raw_html]', faq)

# ---------- articles ----------
P = '<p style="line-height: 22px; text-align: left;">'
art1_paras = [
    f'{P}I start every marketing dashboard project with a short conversation, not a data pull. What does your team actually decide with this data each week? Which campaigns get paused, which channels get more budget, which numbers go in the Monday report? Those answers decide the layout long before I open <strong>Power BI</strong> or <strong>Tableau</strong>.</p>',
    f'{P}Most marketing teams already track plenty of numbers &mdash; impressions, clicks, spend, conversions, cost per lead &mdash; spread across <strong>five or six platforms</strong>. The dashboard&rsquo;s job is not to show every metric available. It puts <strong>the handful your team actually acts on</strong> in one place, arranged so the story is obvious at a glance instead of buried in a table.</p>',
    f'{P}I sketch the layout before touching colour or chart type. A campaign-comparison view, a spend-versus-budget tracker, and a channel breakdown usually need three different chart shapes, instead of one dashboard template stretched to cover all three. <strong>Getting the layout right first</strong> is what keeps the finished dashboard from becoming another report nobody opens.</p>',
    f'{P}Once the layout is agreed, the build happens in whichever tool your data already lives in. If your team already reports out of <strong>Power BI</strong>, that is where the dashboard lives too &mdash; see our <strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/power-bi-dashboard-design/">Power BI dashboard design</a></strong> work for examples. <strong>Tableau</strong> and Excel builds follow the same process.</p>',
    f'{P}The dashboards that get used long after the project ends are the ones that answer a real question every time someone opens them. That is the target for every build here: <strong>a tool your team opens on a Monday morning</strong>, never a showcase piece.</p>',
]
art1 = fill(blocks['article1'], {
    'ARTICLE_1_SUBTITLE': 'Start with the questions, not the charts',
    'ARTICLE_1_HEADING': 'How we design a marketing dashboard',
    'ARTICLE_1_BODY': '\n'.join(art1_paras),
})

art2_paras = [
    f'{P}I founded <strong>The Datalabs Agency</strong> in 2012, in Melbourne, after learning visual storytelling at <strong>National Geographic</strong>. That background shapes how I still think about a marketing dashboard: it is a piece of visual communication first, and a data connection second.</p>',
    f'{P}Since then I have built dashboards and BI style guides for clients including <strong>Mercedes-Benz</strong>, <strong>Adidas</strong>, and <strong>UPS</strong>, alongside corporate training workshops in <strong>Power BI</strong>, <strong>Tableau</strong> &mdash; see our <strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/tableau-business-intelligence-dashboard-designer/">Tableau dashboard design</a></strong> work &mdash; and data storytelling. Marketing dashboards are one of the more common requests: every marketing team eventually needs proof of what a campaign actually did.</p>',
    f'{P}I still get involved directly in design decisions on every project. Dashboard work, especially the marketing kind, rewards someone who has sat through enough campaign reviews to know <strong>which number actually changes a decision</strong> and which one just fills a slide.</p>',
    f'{P}What&rsquo;s next in data visualization? I think you know where this is going: <strong>artificial intelligence</strong>. Where am I going with the <strong>Datalabs Agency</strong>? Same answer.</p>',
]
art2 = fill(blocks['article2'], {
    'ARTICLE_2_SUBTITLE': 'Founded in 2012, still hands-on',
    'ARTICLE_2_HEADING': "Who's behind these dashboard designs",
    'ARTICLE_2_BODY': '\n'.join(art2_paras),
})

# ---------- Lesson 10: two-column body for the longer article (5 paragraphs, past ~4) ----------
def two_col(body_paras, split_after):
    col1 = '\n'.join(body_paras[:split_after])
    col2 = '\n'.join(body_paras[split_after:])
    return ('[vc_row_inner][vc_column_inner width="1/2"][vc_column_text css=""]\n' + col1 +
            '\n[/vc_column_text][/vc_column_inner][vc_column_inner width="1/2"][vc_column_text css=""]\n' + col2 +
            '\n[/vc_column_text][/vc_column_inner][/vc_row_inner]')

def apply_two_col(article_block, body_paras, split_after):
    two_col_html = two_col(body_paras, split_after)
    return re.sub(r'\[vc_column_text css=""\]\n.*?\n\[/vc_column_text\]', two_col_html, article_block, count=1, flags=re.S)

# art1: 5 paragraphs, 3|2 split (char counts: p1-3 ~= p4-5, kept the 3|2 the Character Design page established)
art1 = apply_two_col(art1, art1_paras, 3)
# art2: 4 paragraphs -- under the ~4-paragraph trigger, left single column.

# ---------- enquiry-form footer (Lesson 12): rewrite heading + subtitle to this page's topic ----------
fixed = blocks['fixed']
fixed = fixed.replace(
    '[dfd_heading delimiter_settings="border-bottom-style:solid;|border-bottom-width:1px;|width:50px;|border-bottom-color:#dddddd;" style="style_02" subtitle="Professional &amp; Thought-provoking" title_font_options="tag:h2" subtitle_font_options="tag:h3"]Looking for a speaker for your event?[/dfd_heading]',
    '[dfd_heading delimiter_settings="border-bottom-style:solid;|border-bottom-width:1px;|width:50px;|border-bottom-color:#dddddd;" style="style_02" subtitle="Send us what you are tracking now&hellip;" title_font_options="tag:h2" subtitle_font_options="tag:h3"]Still stitching your marketing report together by hand?[/dfd_heading]'
)
assert fixed != blocks['fixed'], 'enquiry-form footer swap did not match'

# ---------- assemble, strip comments ----------
page = '\n'.join([hero, sec_c, sec_d, t_compare, faq, art1, blocks['offers'], art2, fixed])
page = re.sub(r'<!--(?! YOAST).*?-->\n?', '', page, flags=re.S).strip()
yoast = ('<!-- YOAST SEO TITLE: Marketing Dashboards | The Datalabs Agency | '
         'META DESCRIPTION: The Datalabs Agency designs custom marketing dashboards in Power BI, '
         'Tableau, and Excel -- campaign, traffic, and spend data on one screen your team actually uses. -->')
print('\nSET THESE IN WP-ADMIN (Yoast):\n ' + yoast.strip())
leftover = re.findall(r'\{\{[A-Z0-9_]+', page)
assert not leftover, 'unfilled tokens: ' + str(set(leftover))
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(page)
FINAL_OUT.write_text(page)
print('composed chars:', len(page), '| tables:', page.count('<table'), '| tokens left: 0')
print('written to:', OUT, 'and', FINAL_OUT)
