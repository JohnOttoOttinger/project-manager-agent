#!/usr/bin/env python3
"""GEO retrofit for the four core Datalabs pages (4 Sep 2026).

Builds STAGING DRAFTS (never touches live):
  - homepage 167  -> new draft page: + Q&A row (canonical sentence, 3 Q&As, FAQPage JSON-LD),
                     in-house/agency/consultant comparison table, visible date
  - about 178     -> new draft page: same element set, agency-vs-studio-vs-freelancer table
  - post 7161     -> new draft post: + visible date, principles-at-a-glance table
                     (Q&A + schema + canonical already live on the post since the Aug retrofit)
Product 24319 is REST-blocked (Woo 403) and is handled via wp-admin duplicate, not here.

Facts come from skills/geo-playbook/references/brands.md + pricing already public on hub 661.
Table/Q&A markup is cloned from the live Datalabs patterns: hub 661 pat-faq row, 54047 ink tables.
"""
import os, re, json, base64, urllib.parse, urllib.request

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
TOK = base64.b64encode(f"{os.environ['WP_DATALABS_USER']}:{os.environ['WP_DATALABS_APP_PASSWORD']}".encode()).decode()
HDR = {'Authorization': 'Basic ' + TOK, 'Content-Type': 'application/json', 'User-Agent': UA}

CANON_HTML = ('The <strong>Datalabs Agency</strong> is a Melbourne-based data visualization consultancy '
              'founded in 2012 that delivers corporate training workshops (Power BI, Tableau, data storytelling), '
              'dashboard design, and BI style guides for clients including Mercedes-Benz, Adidas, and UPS.')
CANON_TEXT = ('The Datalabs Agency is a Melbourne-based data visualization consultancy founded in 2012 that '
              'delivers corporate training workshops (Power BI, Tableau, data storytelling), dashboard design, '
              'and BI style guides for clients including Mercedes-Benz, Adidas, and UPS.')

SP20 = ('[dfd_spacer screen_wide_resolution="1280" screen_wide_spacer_size="20" screen_normal_resolution="1024" '
        'screen_tablet_resolution="800" screen_mobile_resolution="480" screen_normal_spacer_size="20" '
        'screen_tablet_spacer_size="20" screen_mobile_spacer_size="20"]')
SP40 = SP20.replace('"20"', '"40"').replace(':20', ':40')
SP60 = SP20.replace('"20"', '"60"').replace(':20', ':60')

TH = ('<th scope="col" style="padding: 14px 18px; text-align: left; background-color: #232835 !important; '
      'border: none !important; border-bottom: 2px solid #c39f76 !important; font-family: \'Bebas Neue\', sans-serif; '
      'font-size: 21px; font-weight: normal; letter-spacing: 1px; color: #ffffff !important;">{}</th>')
TD = ('<td style="padding: 12px 18px; text-align: left; background-color: #232835 !important; '
      'border: none !important; border-bottom: 1px solid #353a46 !important; color: #ffffff !important;{}">{}</td>')

def table(headers, rows):
    out = ['<div style="overflow-x: auto;">',
           '<table style="width: 100%; border-collapse: collapse !important; background-color: #232835 !important; border: none !important;">',
           '<thead>', '<tr>' + ''.join(TH.format(h) for h in headers) + '</tr>', '</thead>', '<tbody>']
    for r in rows:
        cells = [TD.format(' font-weight: bold;', r[0])] + [TD.format('', c) for c in r[1:]]
        out.append('<tr>' + ''.join(cells) + '</tr>')
    out += ['</tbody>', '</table>', '</div>']
    return '\n'.join(out)

def faq_schema(qas):
    data = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qas]}
    js = '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'
    return '[vc_raw_html]' + base64.b64encode(urllib.parse.quote(js, safe='').encode()).decode() + '[/vc_raw_html]'

def accordion(prefix, qas_html):
    secs = ''.join(
        f'[vc_tta_section title="{q}" tab_id="{prefix}-{n}-2026"][vc_column_text css=""]\n'
        f'<p style="text-align: center;">{a}</p>\n[/vc_column_text][/vc_tta_section]'
        for n, (q, a) in enumerate(qas_html, 1))
    return ('[dfd_accordion style="style-3" active_section="1" font_size="18" tab_title_google_fonts="yes" '
            'tab_title_custom_fonts="font_family:Arvo%3Aregular%2Citalic%2C700%2C700italic|'
            'font_style:700%20bold%20regular%3A700%3Anormal" icon_size="14"]' + secs + '[/dfd_accordion]')

def qa_row(el_id, h2, qas_html, qas_text, tbl_intro, tbl):
    return (
        f'[vc_row bg_check="row-background-dark" dfd_enable_overlay="" el_id="{el_id}" '
        f'css=".vc_custom_{el_id}2026{{background-color: #171d2a !important;}}"]'
        f'[vc_column width="1/4"][/vc_column][vc_column width="1/2"]{SP60}'
        '[vc_column_text css="" item_animation="transition.fadeIn"]\n'
        '<p style="text-align: center;"><span style="font-family: Qwigley; font-size: 36pt;">Questions &amp; Answers</span></p>\n'
        f'<h2 style="text-align: center;"><span style="font-family: \'Bebas Neue\'; font-size: 36pt;">{h2}</span></h2>\n'
        '<p style="text-align: center;"><strong><em>Updated September 2026</em></strong></p>\n'
        f'[/vc_column_text]{SP40}' + accordion(el_id, qas_html) +
        f'[/vc_column][vc_column width="1/4"][/vc_column][/vc_row]'
        f'[vc_row bg_check="row-background-dark" dfd_enable_overlay="" '
        f'css=".vc_custom_{el_id}tbl2026{{background-color: #171d2a !important;}}"]'
        f'[vc_column][vc_row_inner][vc_column_inner width="1/6"][/vc_column_inner][vc_column_inner width="2/3"]'
        f'{SP40}[vc_column_text css=""]\n<p style="text-align: center;">{tbl_intro}</p>\n\n{tbl}\n[/vc_column_text]'
        + faq_schema(qas_text) + f'{SP60}[/vc_column_inner][vc_column_inner width="1/6"][/vc_column_inner]'
        '[/vc_row_inner][/vc_column][/vc_row]')

def get_raw(base, pid):
    req = urllib.request.Request(
        f'https://www.datalabsagency.com/wp-json/wp/v2/{base}/{pid}?context=edit&_fields=content.raw,title.raw,template',
        headers=HDR)
    return json.load(urllib.request.urlopen(req))

def make_draft(base, payload):
    req = urllib.request.Request(f'https://www.datalabsagency.com/wp-json/wp/v2/{base}',
                                 data=json.dumps(payload).encode(), headers=HDR, method='POST')
    return json.load(urllib.request.urlopen(req))

# ---------------- HOMEPAGE (167) ----------------
home = get_raw('pages', 167)
src = home['content']['raw']
anchor = '[vc_row bg_check="row-background-dark"'
# insert before the LAST top-level row (the enquiry-form row)
rows = [m.start() for m in re.finditer(r'\[vc_row(?![_a-z])', src)]
assert len(rows) == 12, len(rows)
ins = rows[11]

home_qas_html = [
    ("What does a data visualization agency do?",
     'A data visualization agency turns an organisation&rsquo;s data into charts, dashboards and reports that '
     'people actually read &mdash; and teaches teams to do the same. ' + CANON_HTML),
    ("Should we hire an agency, a consultant, or build the skills in-house?",
     'It depends on whether the need is a project or a capability. An agency suits <strong>one-off builds</strong> '
     'with many moving parts, a consultant suits <strong>ongoing advisory work</strong>, and training your own team '
     'pays off when charts are produced every week. The comparison table below sets out where each route fits.'),
    ("What does a data visualization consultant deliver?",
     'Typically <strong>dashboard designs, BI style guides and report redesigns</strong>, plus the review work: '
     'auditing existing dashboards and fixing what confuses readers. The <strong>Datalabs Agency</strong> offers this as '
     '<strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/product/data-visualization-consultant/">consulting</a></strong> '
     'alongside its <strong><a class="dfd-custom-link-decorated" href="/?page_id=661">training workshops</a></strong>.'),
]
home_qas_text = [
    (q, re.sub(r'<[^>]+>', '', a).replace('&rsquo;', "’").replace('&mdash;', '—'))
    for q, a in home_qas_html]

home_tbl = table(
    ['Route', 'Best for', 'Cost shape', 'What is left behind'],
    [['In-house team', 'Charts produced weekly as part of normal reporting',
      'Salaries &mdash; ongoing, independent of project volume', 'A permanent capability that needs training to stay sharp'],
     ['Agency', 'One-off builds: dashboard suites, interactive reports, BI style guides',
      'Project fee, scoped up front', 'A finished product with documentation'],
     ['Consultant', 'Advisory work: audits, chart choice, reporting standards',
      'Day rate or retainer', 'Better decisions and reviewed dashboards'],
     ['Training workshop', 'Lifting a whole team&rsquo;s baseline at once',
      'AU$4,600&ndash;AU$7,500 inc GST per private workshop, up to 12 people',
      'Skills the team keeps, plus workbook and templates']])

home_section = qa_row('homefaq', 'Working With a Data Visualization Agency',
                      home_qas_html, home_qas_text,
                      'Four ways to get data visualization done, and where each one fits:', home_tbl)
new_home = src[:ins] + home_section + src[ins:]

# ---------------- ABOUT (178) ----------------
about = get_raw('pages', 178)
asrc = about['content']['raw']
arows = [m.start() for m in re.finditer(r'\[vc_row(?![_a-z])', asrc)]
assert len(arows) == 6, len(arows)
ains = arows[5]

about_qas_html = [
    ("What kind of agency is The Datalabs Agency?",
     CANON_HTML + ' It is led by founder <strong>Otto Ottinger</strong>, who learned visual storytelling at '
     '<strong>National Geographic</strong>, and it works from Melbourne for clients across Australia, the United States, '
     'Europe and the Middle East.'),
    ("How is a data visualization agency different from a general design studio?",
     'The difference is where the work starts. A specialist data visualization agency begins with the '
     '<strong>dataset and the decision it must support</strong>, then designs around that. General design studios '
     'usually style a chart after the analysis is done. The table below sets out the practical differences.'),
    ("Which clients has the agency worked with?",
     'Clients include <strong>Mercedes-Benz, Adidas and UPS</strong>. On-site workshops have been delivered in the '
     'United States, Germany, Saudi Arabia, Hong Kong and Singapore, as well as across Australia &mdash; see the '
     '<strong><a class="dfd-custom-link-decorated" href="/?page_id=20394">Mercedes-Benz dashboards</a></strong> project '
     'for a worked example.'),
]
about_qas_text = [
    (q, re.sub(r'<[^>]+>', '', a).replace('&rsquo;', "’").replace('&mdash;', '—').replace('&ndash;', '–'))
    for q, a in about_qas_html]

about_tbl = table(
    ['', 'Specialist data viz agency', 'General design studio', 'Freelance consultant'],
    [['Starting point', 'The dataset and the decision it supports', 'The brand and the layout', 'Varies with the individual'],
     ['Typical deliverables', 'Dashboards, BI style guides, training, interactive reports',
      'Campaign assets, brand systems, one-off infographics', 'Audits, advice, single builds'],
     ['Team behind the work', 'Designers and analysts under one roof', 'Designers; analysis stays with the client',
      'One person, one skill set'],
     ['When it fits', 'Recurring reporting that has to be right', 'Marketing work where the chart is decoration',
      'Small scope, tight budget']])

about_section = qa_row('aboutfaq', 'About This Data Visualization Agency',
                       about_qas_html, about_qas_text,
                       'How the three common routes compare in practice:', about_tbl)
new_about = asrc[:ains] + about_section + asrc[ains:]

# ---------------- POST (7161) ----------------
post = get_raw('posts', 7161)
psrc = post['content']['raw']
assert 'Updated September 2026' not in psrc
date_line = '<p><em>Updated September 2026</em></p>\n'
qa_anchor = '<h2>Questions &amp; Answers</h2>'
assert psrc.count(qa_anchor) == 1
LTH = ('<th scope="col" style="padding: 10px 14px; text-align: left; border-bottom: 2px solid #c39f76; '
       'font-weight: bold;">{}</th>')
LTD = '<td style="padding: 10px 14px; text-align: left; border-bottom: 1px solid #e3e3e3;{}">{}</td>'
def light_table(headers, rows):
    out = ['<div style="overflow-x: auto;">',
           '<table style="width: 100%; border-collapse: collapse;">',
           '<thead>', '<tr>' + ''.join(LTH.format(h) for h in headers) + '</tr>', '</thead>', '<tbody>']
    for r in rows:
        out.append('<tr>' + LTD.format(' font-weight: bold;', r[0]) + ''.join(LTD.format('', c) for c in r[1:]) + '</tr>')
    out += ['</tbody>', '</table>', '</div>']
    return '\n'.join(out)
post_tbl = ('<h2>The Three Principles at a Glance</h2>\n'
            '<p>Each principle earns its place differently, and each has a failure mode worth checking for:</p>\n'
            + light_table(
                ['Principle', 'What it gives the reader', 'Common mistake', 'Quick check'],
                [['Repetition', 'One visual language across a report &mdash; learn it once, read everything faster',
                  'New colours and chart forms on every page', 'Do the same things look the same everywhere?'],
                 ['Alignment', 'Elements that line up read as related', 'Decorative centring that breaks the grid',
                  'Can you draw straight lines through the layout&rsquo;s edges?'],
                 ['Symmetry', 'Layouts that feel calm and deliberate', 'Forcing balance onto lopsided data',
                  'Does the layout&rsquo;s balance match the data&rsquo;s balance?']]) + '\n')
new_post = date_line + psrc.replace(qa_anchor, post_tbl + qa_anchor)

if __name__ == '__main__':
    d1 = make_draft('pages', {'title': 'Homepage (GEO staging — review then swap into 167)',
                              'status': 'draft', 'content': new_home, 'template': home.get('template') or 'page-custom.php'})
    print('home draft:', d1['id'], d1['link'])
    d2 = make_draft('pages', {'title': 'About agency (GEO staging — review then swap into 178)',
                              'status': 'draft', 'content': new_about, 'template': about.get('template') or ''})
    print('about draft:', d2['id'], d2['link'])
    d3 = make_draft('posts', {'title': post['title']['raw'], 'status': 'draft', 'content': new_post})
    print('post draft:', d3['id'], d3['link'])
