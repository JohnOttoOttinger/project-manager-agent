#!/usr/bin/env python3
"""Compose the Marriott APAC Visual Case Study page from the money-pages design kit.

First Visual Case Study build (25 Aug 2026). Content source:
"ODD & DLA Strategy/marriott-apac-case-study.md" — its verification queue is LAW:
no dashboard figures (may be demo data), no GM pull-quote, the "people take action"
line stays a paraphrase. Facts used (73 fields, 5 systems, 4 dashboards, 5 weeks,
2015-2016, Hong Kong workshops, deliverables list) are documented in that file.
Design language: hero + sections + table + GEO Q&A + articles + fixed footers
(design-language.md names: Module: Header Stack, Row: GEO Q&A, Row: Big Statement
territory is covered by the kit's article rows).
"""
import re, base64, urllib.parse, pathlib, json

REPO = pathlib.Path(__file__).resolve().parents[3]
KIT = (REPO / 'skills/money-pages/references/design-kit.html').read_text()
OUT = pathlib.Path('/private/tmp/claude-501/-Users-Ottinger-Claude-Projects-2026-project-manager-agent/1250d283-1a10-4416-b992-be81f96ce7a2/scratchpad/composed-marriott.html')

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

def widen_hero(block):
    # Lessons 7+8: long head noun -> 1/4 + 1/2 + 1/4, offsets changed to match.
    block = block.replace('width="1/3" offset="vc_col-lg-4 vc_col-md-2 vc_col-xs-1"',
                          'width="1/4" offset="vc_col-lg-3 vc_col-md-2 vc_col-xs-1"')
    return block.replace('width="1/3" dfd_column_responsive_enable="dfd-column-responsive-enable" offset="vc_col-lg-4 vc_col-md-8 vc_col-xs-10"',
                         'width="1/2" dfd_column_responsive_enable="dfd-column-responsive-enable" offset="vc_col-lg-6 vc_col-md-8 vc_col-xs-10"')

def widen_inner(block, side, mid):
    # Section/table inner rows carry no offset attr (lesson 7 note) — width alone works.
    block = block.replace('[vc_column_inner width="1/3"][/vc_column_inner]',
                          f'[vc_column_inner width="{side}"][/vc_column_inner]')
    return re.sub(r'\[vc_column_inner width="1/3"\](?=\[dfd_)', f'[vc_column_inner width="{mid}"]', block)

CONTACT = 'https%3A%2F%2Fwww.datalabsagency.com%2Fcontact-us%2F'
LINK = lambda href, label: f'<strong><a class="dfd-custom-link-decorated" href="{href}">{label}</a></strong>'

# ---------- hero ----------
hero = widen_hero(fill(blocks['intro'], {
    'PAGE_SUBTITLE': 'A visual case study&hellip;',
    'PAGE_TITLE': 'Marriott: 73 Metrics, 4 Dashboards',
    'UPDATED_DATE': 'August 2026',
    'HOOK': 'In 2015, Marriott International&rsquo;s Asia-Pacific revenue teams pulled numbers from <strong>five separate enterprise systems</strong> to answer daily pricing questions. Over <strong>five weeks</strong>, I consolidated <strong>73 data fields into four Tableau dashboards</strong> &mdash; one for each person with a decision to make. Here is how the project ran.',
    'SECTION_A_SUBTITLE': 'The project in one paragraph',
    'SECTION_A_HEADING': 'What did the Datalabs Agency build for Marriott?',
    'SECTION_A_INTRO': 'Between 2015 and 2016, the <strong>Datalabs Agency</strong> designed <strong>four production Tableau dashboards</strong> for Marriott International&rsquo;s Asia-Pacific operations, consolidating <strong>73 data fields from five enterprise systems</strong> into screens for General Managers, revenue managers, F&amp;B managers, and sales teams &mdash; alongside a dashboard design style guide and training materials.',
    'CANONICAL_SENTENCE': 'The <strong>Datalabs Agency</strong> is a Melbourne-based data visualization consultancy founded in 2012 that delivers corporate training workshops (Power BI, Tableau, data storytelling), dashboard design, and BI style guides for clients including Mercedes-Benz, Adidas, and UPS.',
    'SECTION_B_SUBTITLE': 'The problem behind the brief',
    'SECTION_B_HEADING': 'Why did Marriott need new dashboards?',
    'SECTION_B_ANSWER': 'The animation above is the finished story. Before it, Marriott&rsquo;s APAC revenue managers were spending <strong>hours every week</strong> manually compiling reports from <strong>73 data fields</strong> spread across those five systems &mdash; MARSHA (reservations), Smith Travel Research (competitive intelligence), PeopleSOFT (financials), Sales Force One (corporate accounts), and GRMRS (revenue management). Basic questions took a compilation exercise to answer.',
    'SECTION_B_CONTEXT': 'The questions themselves were simple ones: how is the property tracking against its competitive set this week, and should we discount rooms for the coming weekend? The data existed &mdash; the delay was in assembling it. APAC analytics leadership set a brief with a higher bar than reporting: they wanted dashboards that <strong>drove action</strong>, screens a manager would open on a Tuesday morning and price a room from. That brief shaped everything that follows on this page, from who was in the discovery workshops to why the final count was <strong>four dashboards</strong>, not one giant one.',
    'PRIMARY_CTA_TEXT': 'Talk dashboards with us',
    'PRIMARY_CTA_URL': CONTACT,
}))

# ---------- discovery section (variant 1) ----------
sec_discovery = widen_inner(fill(blocks['section1'], {
    'SECTION_C_SUBTITLE': 'Hong Kong, on site, with the users',
    'SECTION_C_HEADING': 'How did the discovery workshops run?',
    'SECTION_C_ANSWER': 'I ran intensive discovery workshops on site in <strong>Hong Kong</strong> with the people who would actually use the system: revenue managers, General Managers, regional analytics teams, and executive leadership. From those sessions, <strong>four distinct decision-making contexts</strong> emerged &mdash; and each one became a dashboard.',
    'SECTION_C_DETAIL': f'The guiding principle: people are the ones who take action, so people come first in dashboard design. Insights come out of data, and they come out of the people working with it. It is the same co-design method I now teach in our {LINK("/?page_id=661", "team training workshops")} &mdash; the workshop is where you learn which numbers a decision actually turns on.',
}), '1/4', '1/2')

# ---------- table: the four dashboards ----------
TH = "style=\"padding: 14px 18px; text-align: left; background-color: #000000 !important; border: none !important; border-bottom: 2px solid #c39f76 !important; font-family: 'Bebas Neue', sans-serif; font-size: 21px; font-weight: normal; letter-spacing: 1px; color: #ffffff !important; white-space: nowrap;\""
def td(bg, bold=False):
    s = f'padding: 12px 18px; text-align: left; background-color: {bg} !important; border: none !important; border-bottom: 1px solid #2f2e3a !important; color: #ffffff !important;'
    if bold: s += ' font-weight: bold;'
    return f'style="{s}"'
rows = [
    ['Hotel', 'General Managers', 'Daily operational calls; position within the competitive set'],
    ['Rooms', 'Revenue managers', 'Pricing and inventory; pace against projection'],
    ['Restaurants &amp; Bars', 'F&amp;B managers', 'Outlet performance; membership and satisfaction tracking'],
    ['Catering', 'Sales teams', 'Group bookings and events'],
]
body = []
for r, cells in enumerate(rows):
    bg = '#111111' if r % 2 == 1 else '#000000'
    body.append('<tr>' + ''.join(
        f'<td {td(bg, bold=(c == 0))}>{cell}</td>' for c, cell in enumerate(cells)) + '</tr>')
table_html = ('<div style="overflow-x: auto;">\n<table style="width: 100%; border-collapse: collapse !important; background-color: #000000 !important; border: none !important;">\n<thead>\n<tr>'
    + ''.join(f'<th scope="col" {TH}>{h}</th>' for h in ['Dashboard', 'Built for', 'Decisions it supports'])
    + '</tr>\n</thead>\n<tbody>\n' + '\n'.join(body) + '\n</tbody>\n</table>\n</div>'
    + '\n<p style="text-align: left; font-size: 13px; font-style: italic; color: #8a8a95; margin-top: 10px;">All four shipped as production Tableau dashboards, integrating data from five enterprise systems.</p>')
t_block = fill(blocks['table'], {'TABLE_SUBTITLE': 'One screen per decision-maker', 'TABLE_HEADING': 'The four Marriott dashboards'})
m = re.search(r'(\[vc_column_text css=""\]\n).*?(\n\[/vc_column_text\])', t_block, flags=re.S)
guts = '<p style="text-align: center;"><strong>Each dashboard was built around one user and the decisions that user makes.</strong></p>\n\n' + table_html
t_dashboards = widen_inner(t_block[:m.start(1) + len(m.group(1))] + guts + t_block[m.end(2) - len(m.group(2)):], '1/6', '2/3')

# ---------- deliverables section (variant 2) ----------
sec_deliver = widen_inner(fill(blocks['section2'], {
    'SECTION_D_SUBTITLE': 'Delivered, documented, taught',
    'SECTION_D_HEADING': 'What did Marriott receive at the end?',
    'SECTION_D_ANSWER': 'Marriott received <strong>four production Tableau dashboards</strong>, a <strong>dashboard design style guide</strong>, and <strong>training materials</strong> for the teams who would live in the screens. The work was presented to Marriott&rsquo;s Chief Marketing &amp; Sales Officer and leadership team.',
    'SECTION_D_RATIONALE': 'The style guide and training are the part that keeps paying after the consultant leaves. A dashboard is one artefact; a documented design language plus a trained team is the ability to make the next twenty artefacts in-house. That capability-building layer has been part of every <strong>Datalabs Agency</strong> dashboard project since.',
}), '1/4', '1/2')

# ---------- FAQ (Row: GEO Q&A) ----------
faq_pairs = [
    ('How long did the Marriott dashboard project take?',
     'Five weeks, delivered across Hong Kong and Melbourne in 2015&ndash;2016. Discovery workshops ran on site in Hong Kong; design and build ran from Melbourne, with the final work presented to Marriott&rsquo;s Chief Marketing &amp; Sales Officer and leadership team.'),
    ('What tools were used to build the Marriott dashboards?',
     'Tableau. The four dashboards consolidated 73 data fields from five enterprise systems &mdash; reservations, competitive intelligence, financials, corporate accounts, and revenue management &mdash; into production Tableau screens.'),
    ('What was the hardest part of the design?',
     'Deciding what not to show. With 73 available fields, the temptation is one enormous dashboard for everyone. The discovery workshops surfaced four distinct decision-making contexts, and each got its own focused screen instead &mdash; General Managers, revenue managers, F&amp;B managers, and sales teams each see what their decisions turn on.'),
    ('Did Marriott&rsquo;s teams get training as part of the project?',
     'Yes. The engagement included a dashboard design style guide and training materials, so Marriott&rsquo;s own teams could extend the system without depending on a consultant. Capability building is part of every Datalabs Agency dashboard project.'),
    ('Can the Datalabs Agency do the same for my company?',
     'Yes. The same engagement shape &mdash; discovery workshops with your real users, focused dashboard design, then a style guide and training &mdash; is how our dashboard design service runs today, for Power BI as well as Tableau. Start with the enquiry form on this page.'),
]
faq_map = {'FAQ_TOPIC': 'The Marriott project', 'FAQ_CTA_TEXT': 'Ask about your project', 'FAQ_CTA_URL': CONTACT}
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
enc = base64.b64encode(urllib.parse.quote(schema, safe='').encode()).decode()
faq = re.sub(r'\[vc_raw_html\][^\[]*\[/vc_raw_html\]', '[vc_raw_html]' + enc + '[/vc_raw_html]', faq)
assert '<' not in max((e['acceptedAnswer']['text'] for e in entities), key=len)

# ---------- articles ----------
P = '<p style="line-height: 22px; text-align: left;">'
art1 = fill(blocks['article1'], {
    'ARTICLE_1_SUBTITLE': 'People first, pixels second',
    'ARTICLE_1_HEADING': 'Why the workshops came before the wireframes',
    'ARTICLE_1_BODY': f'''{P}I did not open Tableau in week one. I got on a plane to <strong>Hong Kong</strong> and sat in rooms with the people the dashboards were for &mdash; <strong>revenue managers, General Managers, regional analytics teams</strong>, and the executives they report to. Every hour of those workshops saved days of redesign later.</p>
{P}The workshops did one job: they surfaced how decisions actually get made. A General Manager checks the property&rsquo;s position in its competitive set before the morning stand-up. A revenue manager decides whether to discount a weekend based on pace against projection. Those are <strong>different decisions on different rhythms</strong>, and no single screen serves both well.</p>
{P}That is why the number four matters. Four dashboards was not a design flourish &mdash; it was the number of <strong>distinct decision-making contexts</strong> the workshops uncovered. Each screen answers one person&rsquo;s questions completely, and nobody scrolls past someone else&rsquo;s numbers to find their own.</p>
{P}I run the same discovery method today, in client projects and in our {LINK("/?page_id=661", "data visualisation training workshops")}. If you take one thing from this case study, take the sequence: <strong>workshops, then wireframes</strong>. The data model can wait a fortnight; the people cannot be skipped.</p>''',
})
art2 = fill(blocks['article2'], {
    'ARTICLE_2_SUBTITLE': 'Where the style guides began&hellip;',
    'ARTICLE_2_HEADING': 'What Marriott taught me about design systems',
    'ARTICLE_2_BODY': f'''{P}Consulting with <strong>Marriott Hotels</strong> in Hong Kong in the early days of the BI revolution, I saw the problem that would shape the next decade of my work: dashboards were being created without a design philosophy, without a common design language, and without proper attention to <strong>colour theory, typography, grid systems</strong>, and <strong>user experience design</strong>.</p>
{P}Four dashboards for one region of one hotel group already needed consistency &mdash; shared colour logic, shared chart conventions, shared naming. Scale that to a global company and the need becomes a document. That is why the Marriott engagement shipped with a <strong>dashboard design style guide</strong>, and why the deliverable list included training materials for the teams who would inherit the system.</p>
{P}That insight became a core <strong>Datalabs Agency</strong> service. My {LINK("/?page_id=394", "data visualization style guides")} now operate inside companies such as <strong>Mercedes-Benz</strong> in Germany, <strong>Intel</strong> in San Francisco, and <strong>BlackRock</strong> in New York &mdash; each one doing for a whole organisation what the Marriott guide did for one region.</p>
{P}The through-line from 2015 to now is the same: a dashboard is a product, and products need design systems. If your organisation is accumulating dashboards faster than it is accumulating design decisions, our {LINK("https://www.datalabsagency.com/dashboard-design-services/", "dashboard design services")} page shows how we run that engagement today.</p>''',
})

# ---------- v2 VISUAL ROWS (25 Aug 2026, Otto: "Build v2 — show the numbers as-is") ----------
# Poached modules per design-language.md: Row: Info2 Grid (dfd_info_box, style-guides idiom),
# gallery of vc_single_image w/ lightbox, Row: Big Statement + image (Otto page R7 shape),
# Module: Hotspot (workshop page 687), Module: Avatar Quote (new_testimonials, Otto page R13).
# Media uploaded 25 Aug: 53854 title slide, 53857 system map, 53860 hotel, 53863 rooms,
# 53866 group&catering, 53869 restaurants&bars (2000px, alt text set).

def SP(n, m=None):
    m = m if m is not None else n
    return (f'[dfd_spacer screen_wide_resolution="1280" screen_wide_spacer_size="{n}" '
            f'screen_normal_resolution="1024" screen_tablet_resolution="800" screen_mobile_resolution="480" '
            f'screen_normal_spacer_size="{n}" screen_tablet_spacer_size="{m}" screen_mobile_spacer_size="{m}"]')

def HEAD_ROW(subtitle, title, intro=None):
    txt = f'[vc_column_text css=""]\n<p style="text-align: center;">{intro}</p>\n[/vc_column_text]' if intro else ''
    return ('[vc_row_inner][vc_column_inner width="1/4"][/vc_column_inner][vc_column_inner width="1/2"]'
            f'[dfd_heading enable_delimiter="" style="style_02" heading_margin="margin-bottom:20px;" subtitle="{subtitle}" '
            'title_font_options="tag:h2|font_size:70|line_height:64" subtitle_font_options="tag:h3|font_size:38|line_height:32"]\n'
            f'<p style="text-align: center;">{title}</p>\n[/dfd_heading]' + SP(20) + txt +
            '[/vc_column_inner][vc_column_inner width="1/4"][/vc_column_inner][/vc_row_inner]')

DARKROW = '[vc_row bg_check="row-background-dark" dfd_enable_overlay="" dfd_row_config="full_width_content_paddings"]'

# --- Row: Info2 Grid — the five enterprise systems ---
def info2(icon, title, body):
    return (f'[dfd_info_box module_animation="transition.slideLeftIn" icon="{icon}" line_hide="yes" style="style-01" '
            f'layout="layout-06" title="{title}" icon_size="45" icon_color="#c39f76" icon_hover="#ddccb1" icon_bg_size="45" '
            'title_font_options="tag:h3" subtitle_font_options="tag:div" font_options="tag:div"]'
            f'{body}[/dfd_info_box]')
SYSTEMS = [
    ('dfd-icon-doc_check2 dfd_icon_set-icon-doc_check2', 'MARSHA', 'Reservations — the booking engine every rooms number starts from.'),
    ('dfd-icon-target3 dfd_icon_set-icon-target3', 'Smith Travel Research', 'Competitive intelligence — how the property tracks against its comp set.'),
    ('dfd-icon-bar_graph_1 dfd_icon_set-icon-bar_graph_1', 'PeopleSOFT', 'Financials — budgets, actuals, and everything the GM answers for.'),
    ('dfd-icon-users dfd_icon_set-icon-users', 'Sales Force One', 'Corporate accounts — the top clients driving group revenue.'),
    ('dfd-icon-graph_growth dfd_icon_set-icon-graph_growth', 'GRMRS', 'Revenue management — pace, pricing, and inventory decisions.'),
]
CELL = '[vc_column_inner el_class="dfd_col-tablet-6" width="1/3" offset="vc_col-lg-4 vc_col-md-4 vc_col-xs-12"]{box}' + SP(40) + '[/vc_column_inner]'
row_info2 = (DARKROW + '[vc_column]' + SP(40)
    + HEAD_ROW('Where the 73 metrics lived', 'Five systems, one question at a time',
               'Before the dashboards, answering one revenue question meant visiting up to <strong>five separate systems</strong>.')
    + SP(30)
    + '[vc_row_inner]' + ''.join(CELL.format(box=info2(*s)) for s in SYSTEMS[:3]) + '[/vc_row_inner]'
    + '[vc_row_inner][vc_column_inner width="1/6"][/vc_column_inner]'
    + ''.join(CELL.replace('width="1/3" offset="vc_col-lg-4 vc_col-md-4 vc_col-xs-12"', 'width="1/3" offset="vc_col-lg-4 vc_col-md-4 vc_col-xs-12"').format(box=info2(*s)) for s in SYSTEMS[3:])
    + '[vc_column_inner width="1/6"][/vc_column_inner][/vc_row_inner]'
    + SP(20) + '[/vc_column][/vc_row]')

# --- Row: dashboard gallery (2x2, lightbox) ---
def gal_cell(image_id, title, user):
    return ('[vc_column_inner width="1/2"]'
            f'[dfd_heading enable_delimiter="" style="style_02" heading_margin="margin-bottom:10px;" subtitle="{user}" '
            'title_font_options="tag:h3|font_size:34|line_height:34" subtitle_font_options="tag:h4|font_size:26|line_height:26"]\n'
            f'<p style="text-align: center;">{title}</p>\n[/dfd_heading]' + SP(10)
            + f'[vc_single_image image="{image_id}" img_size="large" alignment="center" style="vc_box_rounded" onclick="link_image"]'
            + SP(40, 30) + '[/vc_column_inner]')
row_gallery = (DARKROW + '[vc_column]' + SP(40)
    + HEAD_ROW('The design work, full size', 'Every dashboard, up close',
               'Click any design to view it full-screen &mdash; these are the <strong>production design files</strong>, indicative figures included.')
    + SP(30)
    + '[vc_row_inner]' + gal_cell(53860, 'Hotel', 'For General Managers') + gal_cell(53863, 'Rooms', 'For revenue managers') + '[/vc_row_inner]'
    + '[vc_row_inner]' + gal_cell(53869, 'Restaurants &amp; Bars', 'For F&amp;B managers') + gal_cell(53866, 'Group &amp; Catering', 'For sales teams') + '[/vc_row_inner]'
    + SP(20) + '[/vc_column][/vc_row]')

# --- Row: Hotspot — read the Hotel Dashboard (attrs poached from Datalabs page 687) ---
import urllib.parse as _u
hotspots = [
    (55, 16, 'Financials / Forecast', 'A three-year rolling forecast (2015-2017), so a GM sees what is expected, not just what happened.'),
    (52, 44, 'Revenue at a glance', 'Rooms $200 REVPAR against budget and last year; catering $2.0M; restaurants and bars $2.0M - each with its top segments.'),
    (47, 70, 'Loyalty split', 'Member vs non-member revenue (62% / 38%) shows how much the loyalty programme actually drives.'),
    (63, 66, 'Market share indices', 'RPI 128, MPI 116, ARI 109 - performance indexed against the competitive set, with rankings auto-calculated (#1, #2, #4 of 7).'),
    (81, 62, 'Channel mix', 'Distribution across six booking channels, so a discounting decision sees the whole mix it lands in.'),
]
hs_data = _u.quote(__import__('json').dumps([
    {"index": i + 1, "x": x, "y": y, "Title": t, "Message": m} for i, (x, y, t, m) in enumerate(hotspots)
]), safe='')
row_hotspot = (DARKROW + '[vc_column]' + SP(40)
    + HEAD_ROW('Click the markers', 'Read the Hotel Dashboard like a GM',
               'Five markers explain what each region of the screen does for the <strong>person who opens it every morning</strong>.')
    + SP(30)
    + '[vc_row_inner][vc_column_inner width="1/6"][/vc_column_inner][vc_column_inner width="2/3"]'
    + ('[dfd_hotspot module_animation="transition.fadeIn" marker_background="#c39f76" tooltip_position="dfd-button-tooltip-right" '
       'tooltip_width="300" image="53860" box_shadow="box_shadow_enable:enable|shadow_horizontal:0|shadow_vertical:15|shadow_blur:50|'
       'shadow_spread:0|box_shadow_color:rgba(0%2C0%2C0%2C0.15)" title_font_options="font_size:18|color:%23333333|line_height:32|letter_spacing:0" '
       'content_font_options="font_size:14|color:%23202c2d|line_height:18" title_google_fonts="yes" '
       'title_custom_fonts="font_family:Arvo%3Aregular%2Citalic%2C700%2C700italic" '
       f'hotspot_data="{hs_data}"]')
    + '[/vc_column_inner][vc_column_inner width="1/6"][/vc_column_inner][/vc_row_inner]'
    + SP(40) + '[/vc_column][/vc_row]')

# --- Row: Big Statement + system map (Otto page R7 shape) ---
row_map = ('[vc_row bg_check="row-background-dark" css=".vc_custom_1691550358421{background-color: #2f2e3a !important;}"]'
    '[vc_column width="1/6"][/vc_column][vc_column width="4/6"]' + SP(40)
    + '[dfd_heading enable_delimiter="" style="style_02" heading_margin="margin-bottom:20px;" subtitle="How it all connects" '
      'title_font_options="tag:h2|font_size:70|line_height:64" subtitle_font_options="tag:h3|font_size:38|line_height:32"]\n'
      '<p style="text-align: center;">One dashboard system, six tiers deep</p>\n[/dfd_heading]' + SP(20)
    + '[vc_column_text css=""]\n'
      '<p style="line-height: 22px; text-align: left;">The four screens are not four separate projects &mdash; they are one system. '
      'This relational map from the project&rsquo;s dashboard design style guide from the project&rsquo;s dashboard design style guide shows how the executive summary rolls down through '
      '<strong>continent, area, market, and hotel</strong> to the four operational dashboards, supporting a <strong>six-tier '
      'organisational hierarchy</strong> with drill-down and filtering at every level.</p>\n[/vc_column_text]' + SP(20)
    + '[vc_single_image image="53857" img_size="full" alignment="center" style="vc_box_rounded" onclick="link_image"]'
    + SP(40) + '[/vc_column][vc_column width="1/6"][/vc_column][/vc_row]')

# --- Module: Avatar Quote (new_testimonials, Otto page idiom; Otto photo 24350 from the kit footer) ---
row_quote = ('[vc_row bg_check="row-background-dark" dfd_enable_overlay=""][vc_column width="1/4"][/vc_column]'
    '[vc_column width="1/2"]' + SP(40)
    + '[new_testimonials main_style="style-1" main_layout="layout-1" image="24350" author="Otto Ottinger" '
      'subtitle="The design principle behind the Marriott project" title_font_options="tag:h4" '
      'subtitle_font_options="tag:div|color:%23ffffff" '
      'description="People are the only ones who take action &mdash; so people, not data, have to be the priority in dashboard design." '
      'content_font_options="line_height:22" thumb_radius="20" thumb_color="rgba(81,86,52,0.46)"]'
    + SP(40) + '[/vc_column][vc_column width="1/4"][/vc_column][/vc_row]')


# ---------- v2.1 CONCEPT-ROW OPTIONS (25 Aug 2026, Otto: two visual-heavy alternatives to the Info2 row) ----------
# Both are inline SVGs in the brand palette (plum ground, tan #c39f76 accents, Bebas/Arvo),
# delivered via vc_raw_html (base64(rawurlencode())). SMIL dash animation on the flow lines.

BEBAS = "BebasNeueRegular, 'Bebas Neue', sans-serif"
ARVO = "Arvo, serif"

def svg_flow():
    # Option A: five systems converging into 73 fields, fanning out to four screens
    systems = [('MARSHA', 'Reservations'), ('SMITH TRAVEL RESEARCH', 'Competitive intelligence'),
               ('PEOPLESOFT', 'Financials'), ('SALES FORCE ONE', 'Corporate accounts'),
               ('GRMRS', 'Revenue management')]
    dashes = [('HOTEL', 'General Managers'), ('ROOMS', 'Revenue managers'),
              ('RESTAURANTS &amp; BARS', 'F&amp;B managers'), ('GROUP &amp; CATERING', 'Sales teams')]
    parts = [f'<svg viewBox="0 0 1200 640" xmlns="http://www.w3.org/2000/svg" role="img" '
             f'aria-label="Five Marriott enterprise systems consolidated into 73 data fields, delivered as four dashboards" '
             f'style="width:100%;height:auto;display:block;">']
    # left system nodes
    ys = [40, 152, 264, 376, 488]
    for (name, sub), y in zip(systems, ys):
        parts.append(f'<rect x="40" y="{y}" width="270" height="80" rx="10" fill="#262532" stroke="#4a4860" stroke-width="1.5"/>')
        parts.append(f'<text x="62" y="{y+35}" font-family="{BEBAS}" font-size="22" letter-spacing="1.5" fill="#ffffff">{name}</text>')
        parts.append(f'<text x="62" y="{y+59}" font-family="{ARVO}" font-size="13" fill="#8a8a95">{sub}</text>')
        # converging flow line
        parts.append(f'<path d="M 310 {y+40} C 420 {y+40}, 440 320, 492 320" fill="none" stroke="#c39f76" '
                     f'stroke-width="2" stroke-dasharray="6 8" opacity="0.85">'
                     f'<animate attributeName="stroke-dashoffset" from="0" to="-56" dur="2.6s" repeatCount="indefinite"/></path>')
    # centre hub
    parts.append('<circle cx="600" cy="320" r="104" fill="#1f1e29" stroke="#c39f76" stroke-width="2.5"/>')
    parts.append('<circle cx="600" cy="320" r="118" fill="none" stroke="#c39f76" stroke-width="1" opacity="0.35" stroke-dasharray="3 7"/>')
    parts.append(f'<text x="600" y="316" text-anchor="middle" font-family="{BEBAS}" font-size="84" fill="#c39f76">73</text>')
    parts.append(f'<text x="600" y="352" text-anchor="middle" font-family="{ARVO}" font-size="15" fill="#ffffff">data fields</text>')
    parts.append(f'<text x="600" y="374" text-anchor="middle" font-family="{ARVO}" font-size="12" fill="#8a8a95">one governed model</text>')
    # right dashboard cards
    yd = [44, 190, 336, 482]
    for (name, sub), y in zip(dashes, yd):
        parts.append(f'<path d="M 708 320 C 780 320, 800 {y+57}, 888 {y+57}" fill="none" stroke="#c39f76" '
                     f'stroke-width="2" stroke-dasharray="6 8" opacity="0.85">'
                     f'<animate attributeName="stroke-dashoffset" from="0" to="-56" dur="2.6s" repeatCount="indefinite"/></path>')
        parts.append(f'<rect x="888" y="{y}" width="272" height="114" rx="10" fill="#262532" stroke="#c39f76" stroke-width="1.5"/>')
        parts.append(f'<text x="912" y="{y+34}" font-family="{BEBAS}" font-size="24" letter-spacing="1.5" fill="#ffffff">{name}</text>')
        parts.append(f'<text x="912" y="{y+56}" font-family="{ARVO}" font-size="13" fill="#c39f76">{sub}</text>')
        # tiny wireframe bars — the highlight steps one bar to the right per card
        # (card 1 highlights bar 1, card 2 bar 2, ...), with a soft pulse on the highlighted bar
        j = yd.index(y)
        for i, h in enumerate([18, 30, 24, 36, 28]):
            if i == j:
                parts.append(f'<rect x="{912+i*26}" y="{y+96-h}" width="16" height="{h}" rx="2" fill="#c39f76">'
                             f'<animate attributeName="opacity" values="1;0.5;1" dur="2s" repeatCount="indefinite"/></rect>')
            else:
                parts.append(f'<rect x="{912+i*26}" y="{y+96-h}" width="16" height="{h}" rx="2" fill="#4a4860"/>')
    parts.append('</svg>')
    return ''.join(parts)

def svg_concepts():
    # Option B: the six design concepts applied on the project (from the dashboard design style guide method)
    tiles = [
        ('AUDIENCE FIRST', 'Who opens the screen decides what is on it', 'people'),
        ('TIME ON DASHBOARD', 'Designed for the 30-second morning read', 'clock'),
        ('DESIGN HIERARCHY', 'The key number reads first, detail second', 'hierarchy'),
        ('GRIDS &amp; SEQUENCING', 'One grid, so every screen reads the same', 'grid'),
        ('CHART SELECTION', 'The chart fits the question asked of it', 'charts'),
        ('ONE DESIGN LANGUAGE', 'Colour, type and icon rules in a style guide', 'swatches'),
    ]
    def glyph(kind, cx, cy):
        t = '#c39f76'; g = []
        if kind == 'people':
            g.append(f'<circle cx="{cx-16}" cy="{cy-10}" r="11" fill="none" stroke="{t}" stroke-width="2.5"/>')
            g.append(f'<path d="M {cx-34} {cy+26} C {cx-34} {cy+6}, {cx+2} {cy+6}, {cx+2} {cy+26}" fill="none" stroke="{t}" stroke-width="2.5" stroke-linecap="round"/>')
            g.append(f'<circle cx="{cx+18}" cy="{cy-6}" r="8" fill="none" stroke="{t}" stroke-width="2.5" opacity="0.6"/>')
            g.append(f'<path d="M {cx+5} {cy+26} C {cx+5} {cy+11}, {cx+31} {cy+11}, {cx+31} {cy+26}" fill="none" stroke="{t}" stroke-width="2.5" stroke-linecap="round" opacity="0.6"/>')
        elif kind == 'clock':
            g.append(f'<circle cx="{cx}" cy="{cy+2}" r="22" fill="none" stroke="{t}" stroke-width="2.5"/>')
            g.append(f'<path d="M {cx} {cy-10} L {cx} {cy+2} L {cx+13} {cy+9}" fill="none" stroke="{t}" stroke-width="2.5" stroke-linecap="round"/>')
        elif kind == 'hierarchy':
            g.append(f'<rect x="{cx-26}" y="{cy-18}" width="52" height="18" rx="3" fill="{t}"/>')
            g.append(f'<rect x="{cx-26}" y="{cy+6}" width="24" height="12" rx="3" fill="none" stroke="{t}" stroke-width="2"/>')
            g.append(f'<rect x="{cx+2}" y="{cy+6}" width="24" height="12" rx="3" fill="none" stroke="{t}" stroke-width="2"/>')
        elif kind == 'grid':
            for dx in (-27, -8, 11):
                for dy in (-18, 1):
                    g.append(f'<rect x="{cx+dx}" y="{cy+dy}" width="15" height="15" rx="2" fill="none" stroke="{t}" stroke-width="2"/>')
        elif kind == 'charts':
            g.append(f'<rect x="{cx-30}" y="{cy-2}" width="9" height="22" rx="2" fill="{t}"/>')
            g.append(f'<rect x="{cx-17}" y="{cy-14}" width="9" height="34" rx="2" fill="none" stroke="{t}" stroke-width="2"/>')
            g.append(f'<path d="M {cx+2} {cy+12} L {cx+12} {cy-4} L {cx+22} {cy+4} L {cx+32} {cy-14}" fill="none" stroke="{t}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>')
        else:  # swatches
            g.append(f'<rect x="{cx-30}" y="{cy-14}" width="18" height="34" rx="3" fill="{t}"/>')
            g.append(f'<rect x="{cx-7}" y="{cy-14}" width="18" height="34" rx="3" fill="none" stroke="{t}" stroke-width="2"/>')
            g.append(f'<rect x="{cx+16}" y="{cy-14}" width="18" height="34" rx="3" fill="none" stroke="{t}" stroke-width="2" opacity="0.5"/>')
        return ''.join(g)
    parts = [f'<svg viewBox="0 0 1200 560" xmlns="http://www.w3.org/2000/svg" role="img" '
             f'aria-label="The six dashboard design concepts applied on the Marriott project" '
             f'style="width:100%;height:auto;display:block;">']
    for i, (title, sub, kind) in enumerate(tiles):
        x = 40 + (i % 3) * 390
        y = 40 + (i // 3) * 260
        parts.append(f'<rect x="{x}" y="{y}" width="330" height="220" rx="12" fill="#262532" stroke="#4a4860" stroke-width="1.5"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="330" height="4" rx="2" fill="#c39f76"/>')
        parts.append(glyph(kind, x + 165, y + 62))
        parts.append(f'<text x="{x+165}" y="{y+136}" text-anchor="middle" font-family="{BEBAS}" font-size="27" letter-spacing="2" fill="#ffffff">{title}</text>')
        parts.append(f'<text x="{x+165}" y="{y+166}" text-anchor="middle" font-family="{ARVO}" font-size="14" fill="#8a8a95">{sub}</text>')
    parts.append('</svg>')
    return ''.join(parts)

def raw_html(html):
    return '[vc_raw_html]' + base64.b64encode(urllib.parse.quote(html, safe='').encode()).decode() + '[/vc_raw_html]'

def svg_row(subtitle, title, intro, svg):
    return (DARKROW + '[vc_column]' + SP(40)
            + HEAD_ROW(subtitle, title, intro) + SP(30)
            + '[vc_row_inner][vc_column_inner width="1/6"][/vc_column_inner][vc_column_inner width="2/3"]'
            + raw_html(svg)
            + '[/vc_column_inner][vc_column_inner width="1/6"][/vc_column_inner][/vc_row_inner]'
            + SP(40) + '[/vc_column][/vc_row]')

row_svg_flow = svg_row('Watch the data find its screen', 'From five systems to four screens',
    'Every metric a manager needs starts in one of <strong>five systems</strong> on the left and ends on one of <strong>four screens</strong> on the right.',
    svg_flow())
row_svg_concepts = svg_row('The rules under every screen', 'The design concepts behind the screens',
    'Six principles from the project&rsquo;s <strong>dashboard design style guide</strong> shaped every screen &mdash; and the guide itself became a deliverable.',
    svg_concepts())

# hero image: swap the kit placeholder for the Marriott project title slide, with lightbox
hero = hero.replace('[vc_single_image image="52827" img_size="large" alignment="center" css=""]',
                    '[vc_single_image image="53854" img_size="large" alignment="center" style="vc_box_rounded" onclick="link_image" css=""]')
assert 'image="53854"' in hero


# ---------- v2.2: hero split (Otto, 25 Aug) — the flow animation moves up to sit right after
# Section A; Section B + CTA move into their own row below it, copy handing off from the animation.
_i = hero.index('[dfd_spacer screen_wide_resolution="1280" screen_wide_spacer_size="80"')
_btn_close = 'hover_border="border-style:none;|border-radius:5px;"]'
_j = hero.index(_btn_close, _i) + len(_btn_close)
_secB_inner = hero[hero.index('[dfd_heading', _i):_j]
hero_p1 = (hero[:_i]
    + '[/vc_column_inner][vc_column_inner el_class="dfd_col-tablet-12" width="1/4" offset="vc_col-lg-3 vc_col-md-2 vc_col-xs-1"][/vc_column_inner][/vc_row_inner]'
    + SP(40) + '[/vc_column][/vc_row]')
row_secB = (DARKROW + '[vc_column]' + SP(20)
    + '[vc_row_inner][vc_column_inner width="1/4"][/vc_column_inner][vc_column_inner width="1/2"]'
    + _secB_inner
    + '[/vc_column_inner][vc_column_inner width="1/4"][/vc_column_inner][/vc_row_inner]'
    + SP(40) + '[/vc_column][/vc_row]')

# ---------- assemble (v2) ----------
page = '\n'.join([hero_p1, row_svg_flow, row_secB, sec_discovery, t_dashboards, row_gallery, row_hotspot, row_map,
                   row_svg_concepts, sec_deliver, row_quote, faq, art1, blocks['offers'], art2, blocks['fixed']])
page = re.sub(r'<!--.*?-->\n?', '', page, flags=re.S)
page = re.sub(r'\]\s+\[', '][', page)  # stray newlines between rows become empty filler rows on first WPBakery save
page = page.strip()
leftover = re.findall(r'\{\{[A-Z0-9_]+', page)
assert not leftover, 'unfilled tokens: ' + str(set(leftover))
OUT.write_text(page)
print('composed v2 chars:', len(page), '| tables:', page.count('<table'), '| images:', page.count('vc_single_image'),
      '| info boxes:', page.count('dfd_info_box'), '| hotspots:', page.count('dfd_hotspot'))

# ---------- push update to draft 53852 ----------
import os, urllib.request
user, pw = os.environ['WP_DATALABS_USER'], os.environ['WP_DATALABS_APP_PASSWORD']
body = {'content': page, 'status': 'draft'}
req = urllib.request.Request(
    'https://www.datalabsagency.com/wp-json/wp/v2/pages/53852',
    data=json.dumps(body).encode(),
    headers={'Content-Type': 'application/json',
             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
             'Authorization': 'Basic ' + base64.b64encode(f'{user}:{pw}'.encode()).decode()},
    method='POST')
with urllib.request.urlopen(req) as r:
    d = json.load(r)
print('WP updated:', d['id'], '| status:', d['status'], '| slug:', d['slug'], '| modified:', d['modified'])
