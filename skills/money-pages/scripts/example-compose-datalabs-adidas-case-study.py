#!/usr/bin/env python3
"""Compose the Adidas Visual Case Study page — second build from the Visual Case Study
template (template-catalog.md row, v1 from Marriott 53852, 25 Aug 2026).

Content sources: tier-1 reference (Adidas section) + the client schedule doc
"Client Projects/Adidas/Adidas Case Study Email & Workshops Dates.docx".
RESOLVED 25 Aug 2026: participant count = "about 150" per the client's own email
(~30 VP/SD/D executive track + ~120 junior-to-mid) — the ~210 was cohorts
double-counted across time-zone slots. Dates verified from the same doc
(29 Nov - 13 Dec 2022; weekday names in the doc have typos, so the table uses
dates only). RULES: no client quotes (two were removed from earlier copy — do
not restore), no client contact name, the brief paraphrased not quoted.
Media uploaded 25 Aug: 53879 title, 53882 superlatives, 53885 venn,
53888 dashboard (hotspot), 53891 dataset, 53894 ops diagram.
"""
import re, base64, urllib.parse, pathlib, json, os, urllib.request

REPO = pathlib.Path(__file__).resolve().parents[3]
KIT = (REPO / 'skills/money-pages/references/design-kit.html').read_text()
OUT = pathlib.Path('/private/tmp/claude-501/-Users-Ottinger-Claude-Projects-2026-project-manager-agent/1250d283-1a10-4416-b992-be81f96ce7a2/scratchpad/composed-adidas.html')

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
    block = block.replace('width="1/3" offset="vc_col-lg-4 vc_col-md-2 vc_col-xs-1"',
                          'width="1/4" offset="vc_col-lg-3 vc_col-md-2 vc_col-xs-1"')
    return block.replace('width="1/3" dfd_column_responsive_enable="dfd-column-responsive-enable" offset="vc_col-lg-4 vc_col-md-8 vc_col-xs-10"',
                         'width="1/2" dfd_column_responsive_enable="dfd-column-responsive-enable" offset="vc_col-lg-6 vc_col-md-8 vc_col-xs-10"')

def widen_inner(block, side, mid):
    block = block.replace('[vc_column_inner width="1/3"][/vc_column_inner]',
                          f'[vc_column_inner width="{side}"][/vc_column_inner]')
    return re.sub(r'\[vc_column_inner width="1/3"\](?=\[dfd_)', f'[vc_column_inner width="{mid}"]', block)

CONTACT = 'https%3A%2F%2Fwww.datalabsagency.com%2Fcontact-us%2F'
LINK = lambda href, label: f'<strong><a class="dfd-custom-link-decorated" href="{href}">{label}</a></strong>'

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
BEBAS = "BebasNeueRegular, 'Bebas Neue', sans-serif"
ARVO = "Arvo, serif"

def raw_html(html):
    return '[vc_raw_html]' + base64.b64encode(urllib.parse.quote(html, safe='').encode()).decode() + '[/vc_raw_html]'

def svg_row(subtitle, title, intro, svg):
    return (DARKROW + '[vc_column]' + SP(40)
            + HEAD_ROW(subtitle, title, intro) + SP(30)
            + '[vc_row_inner][vc_column_inner width="1/6"][/vc_column_inner][vc_column_inner width="2/3"]'
            + raw_html(svg)
            + '[/vc_column_inner][vc_column_inner width="1/6"][/vc_column_inner][/vc_row_inner]'
            + SP(40) + '[/vc_column][/vc_row]')

# ---------- Row: Animated Flow Diagram (SVG) — four continents -> 7 workshops -> two tracks ----------
def svg_flow():
    sources = [('SHANGHAI', 'APAC &amp; GCA cohort'), ('HERZOGENAURACH', 'PELT + EMEA cohorts'),
               ('PORTLAND', 'Americas cohort'), ('LISBON', 'Portugal+ cohort')]
    tracks = [('EXECUTIVE TRACK', 'Around 30 VPs, Senior Directors &amp; Directors'),
              ('ANALYST TRACK', 'Around 120 junior and mid-level staff')]
    parts = [f'<svg viewBox="0 0 1200 640" xmlns="http://www.w3.org/2000/svg" role="img" '
             f'aria-label="Four Adidas cohorts across four continents, trained in seven workshops over three weeks, in an executive track and an analyst track" '
             f'style="width:100%;height:auto;display:block;">']
    ys = [70, 205, 340, 475]
    for (name, sub), y in zip(sources, ys):
        parts.append(f'<rect x="40" y="{y}" width="270" height="80" rx="10" fill="#262532" stroke="#4a4860" stroke-width="1.5"/>')
        parts.append(f'<text x="62" y="{y+35}" font-family="{BEBAS}" font-size="22" letter-spacing="1.5" fill="#ffffff">{name}</text>')
        parts.append(f'<text x="62" y="{y+59}" font-family="{ARVO}" font-size="13" fill="#8a8a95">{sub}</text>')
        parts.append(f'<path d="M 310 {y+40} C 420 {y+40}, 440 320, 492 320" fill="none" stroke="#c39f76" '
                     f'stroke-width="2" stroke-dasharray="6 8" opacity="0.85">'
                     f'<animate attributeName="stroke-dashoffset" from="0" to="-56" dur="2.6s" repeatCount="indefinite"/></path>')
    parts.append('<circle cx="600" cy="320" r="104" fill="#1f1e29" stroke="#c39f76" stroke-width="2.5"/>')
    parts.append('<circle cx="600" cy="320" r="118" fill="none" stroke="#c39f76" stroke-width="1" opacity="0.35" stroke-dasharray="3 7"/>')
    parts.append(f'<text x="600" y="322" text-anchor="middle" font-family="{BEBAS}" font-size="96" fill="#c39f76">7</text>')
    parts.append(f'<text x="600" y="356" text-anchor="middle" font-family="{ARVO}" font-size="15" fill="#ffffff">workshops in three weeks</text>')
    parts.append(f'<text x="600" y="378" text-anchor="middle" font-family="{ARVO}" font-size="12" fill="#8a8a95">delivered live from Melbourne</text>')
    yd = [110, 380]
    for j, ((name, sub), y) in enumerate(zip(tracks, yd)):
        parts.append(f'<path d="M 708 320 C 780 320, 800 {y+75}, 888 {y+75}" fill="none" stroke="#c39f76" '
                     f'stroke-width="2" stroke-dasharray="6 8" opacity="0.85">'
                     f'<animate attributeName="stroke-dashoffset" from="0" to="-56" dur="2.6s" repeatCount="indefinite"/></path>')
        parts.append(f'<rect x="888" y="{y}" width="272" height="150" rx="10" fill="#262532" stroke="#c39f76" stroke-width="1.5"/>')
        parts.append(f'<text x="912" y="{y+38}" font-family="{BEBAS}" font-size="26" letter-spacing="1.5" fill="#ffffff">{name}</text>')
        # subtitle wraps onto two Arvo lines
        s1, s2 = sub.split(', ', 1) if ', ' in sub else (sub, '')
        parts.append(f'<text x="912" y="{y+62}" font-family="{ARVO}" font-size="13" fill="#c39f76">{s1}{"," if s2 else ""}</text>')
        if s2:
            parts.append(f'<text x="912" y="{y+81}" font-family="{ARVO}" font-size="13" fill="#c39f76">{s2}</text>')
        # mini bars — stepping highlight (card 1 -> bar 1, card 2 -> bar 2) with pulse
        for i, h in enumerate([18, 30, 24, 36, 28]):
            if i == j:
                parts.append(f'<rect x="{912+i*26}" y="{y+128-h}" width="16" height="{h}" rx="2" fill="#c39f76">'
                             f'<animate attributeName="opacity" values="1;0.5;1" dur="2s" repeatCount="indefinite"/></rect>')
            else:
                parts.append(f'<rect x="{912+i*26}" y="{y+128-h}" width="16" height="{h}" rx="2" fill="#4a4860"/>')
    parts.append('</svg>')
    return ''.join(parts)

# ---------- Row: Design Principle Tiles (SVG) — the six curriculum principles ----------
def svg_concepts():
    tiles = [
        ('A POINT OF VIEW', 'Data supports a recommendation, never a dump', 'charts'),
        ('ANSWER FIRST', 'Open with the number that matters most', 'hierarchy'),
        ('TWO TRACKS, ONE METHOD', 'Executive and analyst depth, same language', 'people'),
        ('REAL ADIDAS DATA', 'Exercises built on procurement scenarios', 'grid'),
        ('BUILT FOR TIME ZONES', 'Seven sessions, live from Melbourne', 'clock'),
        ('A SHARED LANGUAGE', 'One way to communicate data upward', 'swatches'),
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
             f'aria-label="The six curriculum principles behind the Adidas data storytelling workshops" '
             f'style="width:100%;height:auto;display:block;">']
    for i, (title, sub, kind) in enumerate(tiles):
        x = 40 + (i % 3) * 390
        y = 40 + (i // 3) * 260
        parts.append(f'<rect x="{x}" y="{y}" width="330" height="220" rx="12" fill="#262532" stroke="#4a4860" stroke-width="1.5"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="330" height="4" rx="2" fill="#c39f76"/>')
        parts.append(glyph(kind, x + 165, y + 62))
        parts.append(f'<text x="{x+165}" y="{y+136}" text-anchor="middle" font-family="{BEBAS}" font-size="26" letter-spacing="2" fill="#ffffff">{title}</text>')
        parts.append(f'<text x="{x+165}" y="{y+166}" text-anchor="middle" font-family="{ARVO}" font-size="14" fill="#8a8a95">{sub}</text>')
    parts.append('</svg>')
    return ''.join(parts)

# ---------- hero ----------
hero = widen_hero(fill(blocks['intro'], {
    'PAGE_SUBTITLE': 'A visual case study&hellip;',
    'PAGE_TITLE': 'Adidas: 7 Workshops, 4 Continents',
    'UPDATED_DATE': 'August 2026',
    'HOOK': 'In late 2022, Adidas Global Procurement asked the Datalabs Agency to train <strong>about 150 people</strong> in data storytelling. The answer became <strong>seven live workshops across four continents in three weeks</strong> &mdash; an executive track and an analyst track, taught on Adidas&rsquo;s own procurement scenarios, all delivered from Melbourne.',
    'SECTION_A_SUBTITLE': 'The program in one paragraph',
    'SECTION_A_HEADING': 'What did the Datalabs Agency deliver for Adidas?',
    'SECTION_A_INTRO': 'In 2022, the <strong>Datalabs Agency</strong> designed and facilitated a custom data storytelling curriculum for <strong>Adidas Global Procurement</strong>: seven three-hour workshops for cohorts in Shanghai, Herzogenaurach, Portland, and Lisbon &mdash; <strong>around 150 participants</strong> across an executive track and an analyst track &mdash; plus training materials and <strong>custom procurement datasets</strong> built from real Adidas business scenarios.',
    'CANONICAL_SENTENCE': 'The <strong>Datalabs Agency</strong> is a Melbourne-based data visualization consultancy founded in 2012 that delivers corporate training workshops (Power BI, Tableau, data storytelling), dashboard design, and BI style guides for clients including Mercedes-Benz, Adidas, and UPS.',
    'SECTION_B_SUBTITLE': 'The problem behind the brief',
    'SECTION_B_HEADING': 'Why did Adidas bring in a data storytelling trainer?',
    'SECTION_B_ANSWER': 'The animation above is the delivery map. The brief behind it: Adidas&rsquo;s procurement teams had no shortage of analysis, but stakeholder presentations were arriving as <strong>data dumps</strong> &mdash; dozens of metrics and no message. Leadership wanted presentations that <strong>open with the number that matters</strong> and use data to support a recommendation.',
    'SECTION_B_CONTEXT': 'That reframing &mdash; from data reporters to <strong>strategic advisors</strong> who use data to support a point of view &mdash; set the shape of the whole program. Executives and analysts were given separate tracks with the same methodology, so a VP and a junior buyer came away speaking the same language at the depth their role needs. And because generic training examples slide off a specialist audience, every exercise was built from <strong>procurement-specific scenarios and datasets</strong>, not stock charts.',
    'PRIMARY_CTA_TEXT': 'Book a workshop like this',
    'PRIMARY_CTA_URL': CONTACT,
}))

# ---------- tailoring section (variant 1) ----------
sec_tailor = widen_inner(fill(blocks['section1'], {
    'SECTION_C_SUBTITLE': 'Custom, not off the shelf',
    'SECTION_C_HEADING': 'How was the program tailored to Adidas?',
    'SECTION_C_ANSWER': 'Everything was rebuilt around procurement: a <strong>custom curriculum</strong>, dummy datasets modelled on <strong>real Adidas supplier scenarios</strong> (invoices, discounts, factory locations, ratings), and exercises like the superlatives game shown below &mdash; run in <strong>three-hour interactive sessions</strong> sized for hands-on work.',
    'SECTION_C_DETAIL': f'Two tracks carried the same methodology at different depths: an executive session for VPs, Senior Directors, and Directors, and analyst sessions for junior and mid-level staff. It is the same tailoring approach behind all of our {LINK("/?page_id=661", "data visualisation training workshops")} &mdash; the content changes to fit the team, the method does not.',
}), '1/4', '1/2')

# ---------- table: the seven workshops (dates verified from the schedule doc) ----------
TH = "style=\"padding: 14px 18px; text-align: left; background-color: #000000 !important; border: none !important; border-bottom: 2px solid #c39f76 !important; font-family: 'Bebas Neue', sans-serif; font-size: 21px; font-weight: normal; letter-spacing: 1px; color: #ffffff !important; white-space: nowrap;\""
def td(bg, bold=False, nowrap=False):
    s = f'padding: 12px 18px; text-align: left; background-color: {bg} !important; border: none !important; border-bottom: 1px solid #2f2e3a !important; color: #ffffff !important;'
    if bold: s += ' font-weight: bold;'
    if nowrap: s += ' white-space: nowrap;'
    return f'style="{s}"'
sched = [
    ['29 Nov 2022', 'APAC &amp; GCA analysts', 'Shanghai'],
    ['30 Nov 2022', 'Executive session (PELT)', 'Herzogenaurach'],
    ['5 Dec 2022', 'Americas analysts', 'Portland'],
    ['6 Dec 2022', 'EMEA analysts', 'Herzogenaurach'],
    ['8 Dec 2022', 'Executive session (PELT)', 'Herzogenaurach'],
    ['12 Dec 2022', 'Portugal+ mixed group', 'Lisbon'],
    ['13 Dec 2022', 'EMEA analysts', 'Herzogenaurach'],
]
body = []
for r, cells in enumerate(sched):
    bg = '#111111' if r % 2 == 1 else '#000000'
    body.append('<tr>' + ''.join(
        f'<td {td(bg, bold=(c == 0), nowrap=(c == 0))}>{cell}</td>' for c, cell in enumerate(cells)) + '</tr>')
table_html = ('<div style="overflow-x: auto;">\n<table style="width: 100%; border-collapse: collapse !important; background-color: #000000 !important; border: none !important;">\n<thead>\n<tr>'
    + ''.join(f'<th scope="col" {TH}>{h}</th>' for h in ['Date', 'Cohort', 'Primary city'])
    + '</tr>\n</thead>\n<tbody>\n' + '\n'.join(body) + '\n</tbody>\n</table>\n</div>'
    + '\n<p style="text-align: left; font-size: 13px; font-style: italic; color: #8a8a95; margin-top: 10px;">All seven sessions ran live from Melbourne in a three-hour interactive format, across start times spanning 2 AM to 12 PM Australian time.</p>')
t_block = fill(blocks['table'], {'TABLE_SUBTITLE': 'Three weeks, door to door', 'TABLE_HEADING': 'The seven Adidas workshops'})
m = re.search(r'(\[vc_column_text css=""\]\n).*?(\n\[/vc_column_text\])', t_block, flags=re.S)
guts = '<p style="text-align: center;"><strong>The delivery schedule, from the project&rsquo;s own planning documents.</strong></p>\n\n' + table_html
t_schedule = widen_inner(t_block[:m.start(1) + len(m.group(1))] + guts + t_block[m.end(2) - len(m.group(2)):], '1/6', '2/3')

# ---------- gallery (2x2, lightbox) ----------
def gal_cell(image_id, title, sub):
    return ('[vc_column_inner width="1/2"]'
            f'[dfd_heading enable_delimiter="" style="style_02" heading_margin="margin-bottom:10px;" subtitle="{sub}" '
            'title_font_options="tag:h3|font_size:34|line_height:34" subtitle_font_options="tag:h4|font_size:26|line_height:26"]\n'
            f'<p style="text-align: center;">{title}</p>\n[/dfd_heading]' + SP(10)
            + f'[vc_single_image image="{image_id}" img_size="large" alignment="center" style="vc_box_rounded" onclick="link_image"]'
            + SP(40, 30) + '[/vc_column_inner]')
row_gallery = (DARKROW + '[vc_column]' + SP(40)
    + HEAD_ROW('The teaching assets, full size', 'Inside the workshop materials',
               'Click any asset to view it full-screen &mdash; these are the <strong>actual workshop materials</strong> built for Adidas.')
    + SP(30)
    + '[vc_row_inner]' + gal_cell(53882, 'The Superlatives Exercise', 'Suppliers become characters') + gal_cell(53885, 'The Superlative Venn', 'One supplier, three stories') + '[/vc_row_inner]'
    + '[vc_row_inner]' + gal_cell(53891, 'The Custom Dataset', 'Real scenarios, dummy numbers') + gal_cell(53894, 'Where Procurement Sits', 'The go-to-market context') + '[/vc_row_inner]'
    + SP(20) + '[/vc_column][/vc_row]')

# ---------- hotspot: the teaching dashboard ----------
hotspots = [
    (8, 32, 'The KPI rail', 'Month-to-date quality KPIs - 114 suppliers, $11.20M ordered, a 3.0% vendor rejection rate - the health check before any drill-down.'),
    (48, 6, 'Filters', 'Project, category, supplier and time filters, so one dashboard serves every buyer question.'),
    (55, 30, 'Return cost analysis', 'Return costs and rejection rates for the top five suppliers, side by side - the chart that starts the conversation.'),
    (55, 62, 'Supplier quality rating', 'Ordered value, availability, defect rate and a single quality score per supplier - a ranking the room can argue with.'),
    (30, 90, 'Project analysis', 'Spend under management and project-level drill-down sitting beneath the summary view.'),
]
hs_data = urllib.parse.quote(json.dumps([
    {"index": i + 1, "x": x, "y": y, "Title": t, "Message": msg} for i, (x, y, t, msg) in enumerate(hotspots)
]), safe='')
row_hotspot = (DARKROW + '[vc_column]' + SP(40)
    + HEAD_ROW('Click the markers', 'Read the teaching dashboard',
               'Workshop cohorts practised dashboard critique on this <strong>procurement quality dashboard</strong>, built on dummy supplier data. Five markers explain how it reads.')
    + SP(30)
    + '[vc_row_inner][vc_column_inner width="1/6"][/vc_column_inner][vc_column_inner width="2/3"]'
    + ('[dfd_hotspot module_animation="transition.fadeIn" marker_background="#c39f76" tooltip_position="dfd-button-tooltip-right" '
       'tooltip_width="300" image="53888" box_shadow="box_shadow_enable:enable|shadow_horizontal:0|shadow_vertical:15|shadow_blur:50|'
       'shadow_spread:0|box_shadow_color:rgba(0%2C0%2C0%2C0.15)" title_font_options="font_size:18|color:%23333333|line_height:32|letter_spacing:0" '
       'content_font_options="font_size:14|color:%23202c2d|line_height:18" title_google_fonts="yes" '
       'title_custom_fonts="font_family:Arvo%3Aregular%2Citalic%2C700%2C700italic" '
       f'hotspot_data="{hs_data}"]')
    + '[/vc_column_inner][vc_column_inner width="1/6"][/vc_column_inner][/vc_row_inner]'
    + SP(40) + '[/vc_column][/vc_row]')

# ---------- deliverables section (variant 2) ----------
sec_deliver = widen_inner(fill(blocks['section2'], {
    'SECTION_D_SUBTITLE': 'Delivered, documented, taught',
    'SECTION_D_HEADING': 'What did Adidas receive at the end?',
    'SECTION_D_ANSWER': 'Adidas received a <strong>custom data storytelling curriculum</strong>, seven delivered workshops, the <strong>training materials and custom datasets</strong> behind them, and around 150 staff &mdash; from VPs to junior buyers &mdash; trained in the same method.',
    'SECTION_D_RATIONALE': 'The lasting deliverable is the reframing: procurement teams positioned as <strong>strategic advisors</strong> who use data to support a point of view, with a <strong>shared language</strong> for how data is communicated internally and upward. Training the executive layer alongside the analysts is what makes that language stick &mdash; both sides of the conversation learned it in the same three weeks.',
}), '1/4', '1/2')

# ---------- Avatar Quote ----------
row_quote = ('[vc_row bg_check="row-background-dark" dfd_enable_overlay=""][vc_column width="1/4"][/vc_column]'
    '[vc_column width="1/2"]' + SP(40)
    + '[new_testimonials main_style="style-1" main_layout="layout-1" image="24350" author="Otto Ottinger" '
      'subtitle="The principle behind the Adidas curriculum" title_font_options="tag:h4" '
      'subtitle_font_options="tag:div|color:%23ffffff" '
      'description="Procurement teams should be strategic advisors who use data to support a point of view &mdash; not data reporters." '
      'content_font_options="line_height:22" thumb_radius="20" thumb_color="rgba(81,86,52,0.46)"]'
    + SP(40) + '[/vc_column][vc_column width="1/4"][/vc_column][/vc_row]')

# ---------- FAQ (Row: GEO Q&A) ----------
faq_pairs = [
    ('How many people did the Datalabs Agency train at Adidas?',
     'Around 150 people across seven workshops: an executive session for roughly 30 VPs, Senior Directors, and Directors, and analyst sessions for roughly 120 junior and mid-level procurement staff across APAC, EMEA, and the Americas.'),
    ('How were seven workshops delivered across four continents in three weeks?',
     'All sessions ran live and virtually from Melbourne between 29 November and 13 December 2022, in a three-hour interactive format. Start times spanned 2 AM to 12 PM Australian time so each cohort &mdash; Shanghai, Herzogenaurach, Portland, and Lisbon &mdash; trained in its own working day.'),
    ('What made the training Adidas-specific?',
     'Every exercise was built from real Adidas procurement scenarios: custom dummy datasets covering supplier invoices, discounts, factory locations, and ratings, plus teaching devices like the superlatives exercise that turn supplier data into stories. No generic stock examples.'),
    ('Did executives and analysts attend the same sessions?',
     'No &mdash; they had separate tracks with the same methodology. Executives got level-appropriate depth in their own sessions, and analysts got hands-on time in theirs, so both sides of the reporting conversation came away speaking the same language.'),
    ('Can the Datalabs Agency run this program for my company?',
     'Yes. A custom curriculum, cohort scheduling across time zones, and exercises built from your own data is the standard shape of our corporate training. Send your team size and rough timing through the contact form and we will reply with a program outline and a fixed quote.'),
]
faq_map = {'FAQ_TOPIC': 'The Adidas program', 'FAQ_CTA_TEXT': 'Ask about your team', 'FAQ_CTA_URL': CONTACT}
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
    'ARTICLE_1_SUBTITLE': 'Give every supplier a character',
    'ARTICLE_1_HEADING': 'Why the superlatives exercise works',
    'ARTICLE_1_BODY': f'''{P}A procurement spreadsheet has no story in it &mdash; until you ask a yearbook question. Which supplier is <strong>most profitable</strong>? Which is <strong>least reliable</strong>? Who is the <strong>largest discounter</strong>, the <strong>closest in location</strong>, the <strong>worst rated</strong>? The moment a team answers, the rows stop being rows. They become characters.</p>
{P}That is the superlatives exercise, and it was the engine of the Adidas workshops. Each cohort worked through <strong>real procurement scenarios</strong> &mdash; supplier invoices, discounts, factory locations, quality ratings &mdash; and had to award the superlatives before drawing a single chart. Finding the message first is the whole discipline; the chart is just how you say it out loud.</p>
{P}The Venn version turns up the tension. When one supplier is simultaneously <strong>most profitable</strong>, <strong>smallest by volume</strong>, and <strong>best quality</strong>, that intersection is not a data point &mdash; it is an argument about where the next contract should go. A junior buyer who can spot that intersection and lead with it has stopped reporting and started advising.</p>
{P}I use the same device in our {LINK("/?page_id=687", "Introduction to Data Visualization workshop")}, on whatever data a team brings. The superlatives change; the effect &mdash; a room suddenly arguing about their own numbers &mdash; never does.</p>''',
})
art2 = fill(blocks['article2'], {
    'ARTICLE_2_SUBTITLE': 'Seven sessions, one body clock&hellip;',
    'ARTICLE_2_HEADING': 'Designing training for a global team',
    'ARTICLE_2_BODY': f'''{P}The Adidas brief had a constraint most training providers quietly fail: the audience lived in <strong>Shanghai, Herzogenaurach, Portland, and Lisbon</strong>, and the program had to land in three weeks. Flying a facilitator to four continents was never on the table. Delivering from <strong>Melbourne</strong>, live, was &mdash; if the schedule bent around the cohorts instead of the trainer.</p>
{P}So it bent. Sessions started anywhere from <strong>2 AM to 12 PM</strong> my time, each placed inside the cohort&rsquo;s own working morning or afternoon. A <strong>three-hour interactive format</strong> kept every session hands-on &mdash; long enough for exercises on real scenarios, short enough to hold a screen-bound room.</p>
{P}The other design decision was splitting the audience into an <strong>executive track</strong> and an <strong>analyst track</strong>. The methodology was identical; the altitude was not. Executives worked on what to demand from a data story; analysts worked on how to build one. Training both layers in the same fortnight is why the shared language held after the program ended.</p>
{P}Remote, time-zone-shaped delivery is now a standard option in our {LINK("/?page_id=661", "training workshops")} &mdash; and the format is priced on our {LINK("https://www.datalabsagency.com/data-visualisation-workshop-pricing/", "workshop pricing page")}, where a remote full day can split across two mornings for exactly this reason.</p>''',
})

# ---------- hero split: Section A stays in the hero; Section B + CTA follow the flow animation ----------
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

# hero image: the Adidas workshop title slide
hero_p1 = hero_p1.replace('[vc_single_image image="52827" img_size="large" alignment="center" css=""]',
                          '[vc_single_image image="53879" img_size="large" alignment="center" style="vc_box_rounded" onclick="link_image" css=""]')
assert 'image="53879"' in hero_p1

row_svg_flow = svg_row('Watch the program come together', 'Four continents, seven workshops, two tracks',
    'Every cohort on the left trained inside its own working day; every participant landed in one of <strong>two tracks</strong> on the right.',
    svg_flow())
row_svg_concepts = svg_row('The rules under every session', 'The principles behind the curriculum',
    'Six principles shaped all seven sessions &mdash; and the <strong>training materials</strong> built on them stayed with Adidas.',
    svg_concepts())

# ---------- assemble ----------
page = '\n'.join([hero_p1, row_svg_flow, row_secB, sec_tailor, t_schedule, row_gallery, row_hotspot,
                  row_svg_concepts, sec_deliver, row_quote, faq, art1, blocks['offers'], art2, blocks['fixed']])
page = re.sub(r'<!--.*?-->\n?', '', page, flags=re.S)
page = re.sub(r'\]\s+\[', '][', page)
page = page.strip()
leftover = re.findall(r'\{\{[A-Z0-9_]+', page)
assert not leftover, 'unfilled tokens: ' + str(set(leftover))
assert page.count('&hellip;') >= 2 and '...' not in page
OUT.write_text(page)
print('composed chars:', len(page), '| tables:', page.count('<table'), '| images:', page.count('vc_single_image'),
      '| hotspots:', page.count('dfd_hotspot'), '| svgs:', page.count('<svg'))

# ---------- create the draft ----------
user, pw = os.environ['WP_DATALABS_USER'], os.environ['WP_DATALABS_APP_PASSWORD']
author = os.environ.get('WP_DATALABS_AUTHOR_ID')
body = {'title': 'Adidas: 7 Workshops, 4 Continents', 'content': page, 'status': 'draft',
        'slug': 'adidas-data-storytelling-workshops', 'parent': 19482, 'template': 'page-custom.php'}
if author: body['author'] = int(author)
req = urllib.request.Request(
    'https://www.datalabsagency.com/wp-json/wp/v2/pages',
    data=json.dumps(body).encode(),
    headers={'Content-Type': 'application/json',
             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
             'Authorization': 'Basic ' + base64.b64encode(f'{user}:{pw}'.encode()).decode()},
    method='POST')
with urllib.request.urlopen(req) as r:
    d = json.load(r)
print('WP draft created:', d['id'], '| status:', d['status'], '| slug:', d['slug'], '| parent:', d['parent'])
print('Review:', f"https://www.datalabsagency.com/wp-admin/post.php?post={d['id']}&action=edit")
print('\nYOAST (set in wp-admin): SEO TITLE: Adidas Case Study: Data Storytelling Workshops | Datalabs')
print('META DESCRIPTION: How the Datalabs Agency trained 150+ Adidas procurement staff in data storytelling - seven live workshops across four continents in three weeks.')
