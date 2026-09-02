#!/usr/bin/env python3
"""Shared builders for Visual Case Study composes (template-catalog: "Visual Case Study — Datalabs").

Extracted 25 Aug 2026 from the Marriott (53852) and Adidas (53897) composes so per-client
scripts carry content only. Layout idiom, spacing, fonts, and colours are Otto-approved v1 —
change them only via a new template version.
"""
import re, base64, json, os, pathlib, urllib.parse, urllib.request

REPO = pathlib.Path(__file__).resolve().parents[3]
KIT = (REPO / 'skills/money-pages/references/design-kit.html').read_text()
CONTACT = 'https%3A%2F%2Fwww.datalabsagency.com%2Fcontact-us%2F'
BEBAS = "BebasNeueRegular, 'Bebas Neue', sans-serif"
ARVO = "Arvo, serif"
TAN = '#c39f76'
DARKROW = '[vc_row bg_check="row-background-dark" dfd_enable_overlay="" dfd_row_config="full_width_content_paddings"]'
CANONICAL = ('The <strong>Datalabs Agency</strong> is a Melbourne-based data visualization consultancy founded in 2012 '
             'that delivers corporate training workshops (Power BI, Tableau, data storytelling), dashboard design, '
             'and BI style guides for clients including Mercedes-Benz, Adidas, and UPS.')
LINK = lambda href, label: f'<strong><a class="dfd-custom-link-decorated" href="{href}">{label}</a></strong>'
P = '<p style="line-height: 22px; text-align: left;">'

def kit_blocks():
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
    return blocks

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

def raw_html(html):
    return '[vc_raw_html]' + base64.b64encode(urllib.parse.quote(html, safe='').encode()).decode() + '[/vc_raw_html]'

def svg_row(subtitle, title, intro, svg):
    return (DARKROW + '[vc_column]' + SP(40)
            + HEAD_ROW(subtitle, title, intro) + SP(30)
            + '[vc_row_inner][vc_column_inner width="1/6"][/vc_column_inner][vc_column_inner width="2/3"]'
            + raw_html(svg)
            + '[/vc_column_inner][vc_column_inner width="1/6"][/vc_column_inner][/vc_row_inner]'
            + SP(40) + '[/vc_column][/vc_row]')

FLOW_ANIM = '<animate attributeName="stroke-dashoffset" from="0" to="-56" dur="2.6s" repeatCount="indefinite"/>'

def flow_line(x1, y1, x2, y2, cx1=None):
    cx1 = cx1 if cx1 is not None else (x1 + x2) / 2
    return (f'<path d="M {x1} {y1} C {cx1} {y1}, {cx1} {y2}, {x2} {y2}" fill="none" stroke="{TAN}" '
            f'stroke-width="2" stroke-dasharray="6 8" opacity="0.85">{FLOW_ANIM}</path>')

def glyph(kind, cx, cy):
    """Line-icon glyphs for Design Principle Tiles: people, clock, hierarchy, grid, charts, swatches,
    doc, target, layers."""
    t = TAN; g = []
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
    elif kind == 'doc':
        g.append(f'<rect x="{cx-16}" y="{cy-20}" width="32" height="42" rx="3" fill="none" stroke="{t}" stroke-width="2.5"/>')
        for dy in (-8, 0, 8):
            g.append(f'<line x1="{cx-8}" y1="{cy+dy}" x2="{cx+8}" y2="{cy+dy}" stroke="{t}" stroke-width="2"/>')
    elif kind == 'target':
        g.append(f'<circle cx="{cx}" cy="{cy}" r="21" fill="none" stroke="{t}" stroke-width="2.5"/>')
        g.append(f'<circle cx="{cx}" cy="{cy}" r="12" fill="none" stroke="{t}" stroke-width="2" opacity="0.7"/>')
        g.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{t}"/>')
    elif kind == 'layers':
        for i, dy in enumerate((-12, 0, 12)):
            op = 1 - i * 0.3
            g.append(f'<path d="M {cx-24} {cy+dy} L {cx} {cy+dy-10} L {cx+24} {cy+dy} L {cx} {cy+dy+10} Z" fill="none" stroke="{t}" stroke-width="2.5" opacity="{op}"/>')
    else:  # swatches
        g.append(f'<rect x="{cx-30}" y="{cy-14}" width="18" height="34" rx="3" fill="{t}"/>')
        g.append(f'<rect x="{cx-7}" y="{cy-14}" width="18" height="34" rx="3" fill="none" stroke="{t}" stroke-width="2"/>')
        g.append(f'<rect x="{cx+16}" y="{cy-14}" width="18" height="34" rx="3" fill="none" stroke="{t}" stroke-width="2" opacity="0.5"/>')
    return ''.join(g)

def svg_tiles(aria, tiles):
    """Design Principle Tiles: list of (TITLE, caption, glyph_kind), 6 tiles in 3x2."""
    parts = [f'<svg viewBox="0 0 1200 560" xmlns="http://www.w3.org/2000/svg" role="img" '
             f'aria-label="{aria}" style="width:100%;height:auto;display:block;">']
    for i, (title, sub, kind) in enumerate(tiles):
        x = 40 + (i % 3) * 390
        y = 40 + (i // 3) * 260
        parts.append(f'<rect x="{x}" y="{y}" width="330" height="220" rx="12" fill="#262532" stroke="#4a4860" stroke-width="1.5"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="330" height="4" rx="2" fill="{TAN}"/>')
        parts.append(glyph(kind, x + 165, y + 62))
        parts.append(f'<text x="{x+165}" y="{y+136}" text-anchor="middle" font-family="{BEBAS}" font-size="26" letter-spacing="2" fill="#ffffff">{title}</text>')
        parts.append(f'<text x="{x+165}" y="{y+166}" text-anchor="middle" font-family="{ARVO}" font-size="14" fill="#8a8a95">{sub}</text>')
    parts.append('</svg>')
    return ''.join(parts)

def gal_cell(image_id, title, sub):
    return ('[vc_column_inner width="1/2"]'
            f'[dfd_heading enable_delimiter="" style="style_02" heading_margin="margin-bottom:10px;" subtitle="{sub}" '
            'title_font_options="tag:h3|font_size:34|line_height:34" subtitle_font_options="tag:h4|font_size:26|line_height:26"]\n'
            f'<p style="text-align: center;">{title}</p>\n[/dfd_heading]' + SP(10)
            + f'[vc_single_image image="{image_id}" img_size="large" alignment="center" style="vc_box_rounded" onclick="link_image"]'
            + SP(40, 30) + '[/vc_column_inner]')

def gallery_row(subtitle, title, intro, cells):
    """cells: list of (image_id, cell_title, cell_sub); laid out 2-up per inner row."""
    inner = ''
    for i in range(0, len(cells), 2):
        inner += '[vc_row_inner]' + ''.join(gal_cell(*c) for c in cells[i:i+2]) + '[/vc_row_inner]'
    return (DARKROW + '[vc_column]' + SP(40) + HEAD_ROW(subtitle, title, intro) + SP(30)
            + inner + SP(20) + '[/vc_column][/vc_row]')

def hotspot_row(subtitle, title, intro, image_id, hotspots):
    """hotspots: list of (x_pct, y_pct, Title, Message) — plain text, no HTML entities in Message."""
    hs_data = urllib.parse.quote(json.dumps([
        {"index": i + 1, "x": x, "y": y, "Title": t, "Message": msg}
        for i, (x, y, t, msg) in enumerate(hotspots)]), safe='')
    return (DARKROW + '[vc_column]' + SP(40) + HEAD_ROW(subtitle, title, intro) + SP(30)
        + '[vc_row_inner][vc_column_inner width="1/6"][/vc_column_inner][vc_column_inner width="2/3"]'
        + ('[dfd_hotspot module_animation="transition.fadeIn" marker_background="#c39f76" tooltip_position="dfd-button-tooltip-right" '
           f'tooltip_width="300" image="{image_id}" box_shadow="box_shadow_enable:enable|shadow_horizontal:0|shadow_vertical:15|shadow_blur:50|'
           'shadow_spread:0|box_shadow_color:rgba(0%2C0%2C0%2C0.15)" title_font_options="font_size:18|color:%23333333|line_height:32|letter_spacing:0" '
           'content_font_options="font_size:14|color:%23202c2d|line_height:18" title_google_fonts="yes" '
           'title_custom_fonts="font_family:Arvo%3Aregular%2Citalic%2C700%2C700italic" '
           f'hotspot_data="{hs_data}"]')
        + '[/vc_column_inner][vc_column_inner width="1/6"][/vc_column_inner][/vc_row_inner]'
        + SP(40) + '[/vc_column][/vc_row]')

def quote_row(author, subtitle, description, image_id=24350):
    return ('[vc_row bg_check="row-background-dark" dfd_enable_overlay=""][vc_column width="1/4"][/vc_column]'
        '[vc_column width="1/2"]' + SP(40)
        + f'[new_testimonials main_style="style-1" main_layout="layout-1" image="{image_id}" author="{author}" '
          f'subtitle="{subtitle}" title_font_options="tag:h4" subtitle_font_options="tag:div|color:%23ffffff" '
          f'description="{description}" content_font_options="line_height:22" thumb_radius="20" thumb_color="rgba(81,86,52,0.46)"]'
        + SP(40) + '[/vc_column][vc_column width="1/4"][/vc_column][/vc_row]')

TH = ("style=\"padding: 14px 18px; text-align: left; background-color: #000000 !important; border: none !important; "
      "border-bottom: 2px solid #c39f76 !important; font-family: 'Bebas Neue', sans-serif; font-size: 21px; "
      "font-weight: normal; letter-spacing: 1px; color: #ffffff !important; white-space: nowrap;\"")

def _td(bg, bold=False, nowrap=False):
    s = (f'padding: 12px 18px; text-align: left; background-color: {bg} !important; border: none !important; '
         f'border-bottom: 1px solid #2f2e3a !important; color: #ffffff !important;')
    if bold: s += ' font-weight: bold;'
    if nowrap: s += ' white-space: nowrap;'
    return f'style="{s}"'

def table_row(blocks, subtitle, title, intro, heads, rows, footnote=None, first_col_nowrap=True):
    body = []
    for r, cells in enumerate(rows):
        bg = '#111111' if r % 2 == 1 else '#000000'
        body.append('<tr>' + ''.join(
            f'<td {_td(bg, bold=(c == 0), nowrap=(c == 0 and first_col_nowrap))}>{cell}</td>'
            for c, cell in enumerate(cells)) + '</tr>')
    html = ('<div style="overflow-x: auto;">\n<table style="width: 100%; border-collapse: collapse !important; '
            'background-color: #000000 !important; border: none !important;">\n<thead>\n<tr>'
            + ''.join(f'<th scope="col" {TH}>{h}</th>' for h in heads)
            + '</tr>\n</thead>\n<tbody>\n' + '\n'.join(body) + '\n</tbody>\n</table>\n</div>')
    if footnote:
        html += f'\n<p style="text-align: left; font-size: 13px; font-style: italic; color: #8a8a95; margin-top: 10px;">{footnote}</p>'
    block = fill(blocks['table'], {'TABLE_SUBTITLE': subtitle, 'TABLE_HEADING': title})
    m = re.search(r'(\[vc_column_text css=""\]\n).*?(\n\[/vc_column_text\])', block, flags=re.S)
    guts = f'<p style="text-align: center;"><strong>{intro}</strong></p>\n\n{html}'
    return widen_inner(block[:m.start(1) + len(m.group(1))] + guts + block[m.end(2) - len(m.group(2)):], '1/6', '2/3')

def plain(s):
    s = re.sub(r'<[^>]+>', '', s)
    for ent, ch in [('&mdash;', '—'), ('&ndash;', '–'), ('&amp;', '&'), ('&rsquo;', '’'), ('&lsquo;', '‘'), ('&ldquo;', '“'), ('&rdquo;', '”'), ('&hellip;', '…'), ('&times;', 'x')]:
        s = s.replace(ent, ch)
    return s

def faq_row(blocks, topic, cta_text, faq_pairs):
    faq_map = {'FAQ_TOPIC': topic, 'FAQ_CTA_TEXT': cta_text, 'FAQ_CTA_URL': CONTACT}
    for i, (q, a) in enumerate(faq_pairs, 1):
        faq_map[f'FAQ_Q{i}'] = q
        faq_map[f'FAQ_A{i}'] = a
    faq = fill(blocks['faq'], faq_map)
    entities = [{"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in faq_pairs]
    assert not any('<' in e['acceptedAnswer']['text'] for e in entities)
    schema = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}, ensure_ascii=False) + '</script>'
    enc = base64.b64encode(urllib.parse.quote(schema, safe='').encode()).decode()
    return re.sub(r'\[vc_raw_html\][^\[]*\[/vc_raw_html\]', '[vc_raw_html]' + enc + '[/vc_raw_html]', faq)

def split_hero(hero, hero_image_id):
    """Return (hero_p1, row_secB): hero ends after Section A; Section B + CTA get their own row."""
    hero = hero.replace('[vc_single_image image="52827" img_size="large" alignment="center" css=""]',
                        f'[vc_single_image image="{hero_image_id}" img_size="large" alignment="center" style="vc_box_rounded" onclick="link_image" css=""]')
    i = hero.index('[dfd_spacer screen_wide_resolution="1280" screen_wide_spacer_size="80"')
    btn_close = 'hover_border="border-style:none;|border-radius:5px;"]'
    j = hero.index(btn_close, i) + len(btn_close)
    secB_inner = hero[hero.index('[dfd_heading', i):j]
    hero_p1 = (hero[:i]
        + '[/vc_column_inner][vc_column_inner el_class="dfd_col-tablet-12" width="1/4" offset="vc_col-lg-3 vc_col-md-2 vc_col-xs-1"][/vc_column_inner][/vc_row_inner]'
        + SP(40) + '[/vc_column][/vc_row]')
    row_secB = (DARKROW + '[vc_column]' + SP(20)
        + '[vc_row_inner][vc_column_inner width="1/4"][/vc_column_inner][vc_column_inner width="1/2"]'
        + secB_inner
        + '[/vc_column_inner][vc_column_inner width="1/4"][/vc_column_inner][/vc_row_inner]'
        + SP(40) + '[/vc_column][/vc_row]')
    return hero_p1, row_secB

def assemble(rows):
    page = '\n'.join(rows)
    page = re.sub(r'<!--.*?-->\n?', '', page, flags=re.S)
    page = re.sub(r'\]\s+\[', '][', page)
    page = page.strip()
    leftover = re.findall(r'\{\{[A-Z0-9_]+', page)
    assert not leftover, 'unfilled tokens: ' + str(set(leftover))
    assert page.count('&hellip;') >= 2 and '...' not in page
    return page

def create_draft(title, slug, page, out_path):
    pathlib.Path(out_path).write_text(page)
    user, pw = os.environ['WP_DATALABS_USER'], os.environ['WP_DATALABS_APP_PASSWORD']
    author = os.environ.get('WP_DATALABS_AUTHOR_ID')
    body = {'title': title, 'content': page, 'status': 'draft',
            'slug': slug, 'parent': 19482, 'template': 'page-custom.php'}
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
    print('WP draft created:', d['id'], '| slug:', d['slug'], '| parent:', d['parent'])
    print('Review:', f"https://www.datalabsagency.com/wp-admin/post.php?post={d['id']}&action=edit")
    return d['id']

def upload_media(plan, folder):
    """plan: list of (filename, alt, title) with files in folder. Returns {filename: media_id}."""
    site = 'https://www.datalabsagency.com'
    auth = 'Basic ' + base64.b64encode(f"{os.environ['WP_DATALABS_USER']}:{os.environ['WP_DATALABS_APP_PASSWORD']}".encode()).decode()
    UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    out = {}
    for fn, alt, title in plan:
        data = open(os.path.join(folder, fn), 'rb').read()
        req = urllib.request.Request(site + '/wp-json/wp/v2/media', data=data, method='POST', headers={
            'Content-Type': 'image/jpeg' if fn.endswith(('.jpg', '.jpeg')) else 'image/png',
            'Content-Disposition': f'attachment; filename="{fn}"', 'Authorization': auth, 'User-Agent': UA})
        with urllib.request.urlopen(req) as r:
            d = json.load(r)
        mid = d['id']
        req2 = urllib.request.Request(site + f'/wp-json/wp/v2/media/{mid}',
            data=json.dumps({'alt_text': alt, 'title': title}).encode(), method='POST',
            headers={'Content-Type': 'application/json', 'Authorization': auth, 'User-Agent': UA})
        urllib.request.urlopen(req2).read()
        out[fn] = mid
        print('uploaded:', fn, '->', mid)
    return out


# ---------- per-page tinted-dark themes (Otto's style, 25 Aug 2026) ----------
# One near-black tint per page, set at Page Options > Background color in wp-admin.
# apply_theme() re-derives the SVG panel/hub/stroke shades and the hero overlay from
# the page tint, and strips row-level background-color css attrs so the page ground
# is one clean colour (Otto's call: variation comes from SVG panels + black tables).

def _hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def _rgb_to_hex(r, g, b):
    return '#%02x%02x%02x' % (max(0, min(255, round(r))), max(0, min(255, round(g))), max(0, min(255, round(b))))

def shade(h, f):
    r, g, b = _hex_to_rgb(h)
    return _rgb_to_hex(r * f, g * f, b * f)

def lighten(h, f):
    r, g, b = _hex_to_rgb(h)
    return _rgb_to_hex(r + (255 - r) * f, g + (255 - g) * f, b + (255 - b) * f)

def apply_theme(page, bg):
    """Retint a composed page to a new page-background hex (e.g. '#1a2230')."""
    panel = shade(bg, 0.82)    # SVG cards, a shade darker than the page
    hub = shade(bg, 0.64)      # SVG hub circles, darker still
    stroke = lighten(bg, 0.13) # neutral card strokes
    dim = lighten(bg, 0.06)    # dim bars
    for old, new in [('#262532', panel), ('#1f1e29', hub), ('#4a4860', stroke), ('#3a384c', dim),
                     ('#2f2e3a', bg), ('#2F2E3A', bg.upper())]:
        page = page.replace(old, new)
    # strip row-level pure-background css attrs (uncompiled vc_custom classes; would fight the tint after an editor save)
    page = re.sub(r'\s*css="\.vc_custom_\d+\{background-color: #[0-9a-fA-F]{3,6} !important;\}"', '', page)
    return page
