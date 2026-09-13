#!/usr/bin/env python3
"""Compose the Digital Analytics Agency page (slug /analytics-agency/) from the money-pages design kit.

Target cluster (Otto shortlist pick #2, 13 Sep 2026): "analytics agency", 808 impressions / 0 clicks /
avg position 41.6, served by the homepage at position 56.0. Do-not-target guardrail: the EXACT phrases
"analytics agency" and "data analytics agency" are already owned by
/analytics-reporting-agency/data-analysis/ (pos 8.3 / 6.3) -- this page targets the underserved adjacent
terms ("google analytics agency" 141 impr, "digital analytics agency" 66 impr) and links OUT to the
data-analysis page for the excluded exact phrases rather than competing with it.
"""
import re, base64, urllib.parse, pathlib, json

REPO = pathlib.Path(__file__).resolve().parents[3]
KIT = (REPO / 'skills/money-pages/references/design-kit.html').read_text()
OUT = REPO / 'skills/money-pages/references/composed/analytics-agency-2026-09-13.html'

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

# ---------- hero ----------
hero = fill(blocks['intro'], {
    'PAGE_SUBTITLE': 'So you need a&hellip;',
    'PAGE_TITLE': 'Digital Analytics Agency',
    'UPDATED_DATE': 'September 2026',
    'HOOK': 'We are The <strong>Datalabs Agency</strong>, a Melbourne-based analytics agency that turns raw website, product and business data into <strong>dashboards</strong>, executive reports and decisions your team can act on. Since 2012 we have built <strong>BI style guides</strong> and interactive reporting for clients including Mercedes-Benz, Adidas and UPS.',
    'SECTION_A_SUBTITLE': 'The short version',
    'SECTION_A_HEADING': 'What does a digital analytics agency do?',
    'SECTION_A_INTRO': 'A digital analytics agency turns raw numbers from tools like <strong>Google Analytics</strong>, Power BI and Tableau into dashboards, reports and presentations that non-technical stakeholders actually use. We focus on the layer between the data and the decision &mdash; <strong>design</strong>, <strong>storytelling</strong> and <strong>dashboard build</strong> &mdash; not tag installation.',
    'CANONICAL_SENTENCE': 'The <strong>Datalabs Agency</strong> is a Melbourne-based data visualization consultancy founded in 2012 that delivers corporate training workshops (Power BI, Tableau, data storytelling), dashboard design, and BI style guides for clients including Mercedes-Benz, Adidas, and UPS.',
    'SECTION_B_SUBTITLE': 'Two different jobs',
    'SECTION_B_HEADING': 'How is this different to a Google Analytics agency?',
    'SECTION_B_ANSWER': 'A typical Google Analytics agency configures tracking, tags and reports inside GA4. <strong>We start after that step</strong>: once your team already has the numbers, we turn them into dashboards, BI style guides and executive reporting your leadership can actually read and act on.',
    'SECTION_B_CONTEXT': 'A typical &ldquo;Google Analytics agency&rdquo; spends its time inside GA4: tracking plans, event configuration, consent settings, and monthly performance reports. That is valuable work, and it is not ours. We start once your team already has numbers somewhere &mdash; Google Analytics, Power BI, a CRM, a spreadsheet &mdash; and turn them into something people outside the data team will actually open. Whether you run analytics in-house or through a specialist <strong>Google Analytics agency</strong>, we plug in as the design and reporting layer between the raw numbers and the boardroom. If your team needs the earlier stage &mdash; data collected and analysed from the ground up &mdash; our <strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/analytics-reporting-agency/data-analysis/">data analytics and reporting service</a></strong> covers that; this page is about what happens once the numbers already exist.',
    'PRIMARY_CTA_TEXT': 'Get a fixed quote',
    'PRIMARY_CTA_URL': CONTACT,
})
# Lesson 7/8/11 (design-kit-README): head noun is 3 words ("digital analytics agency") --
# widen the hero/section-A/B inner row from 1/3+1/3+1/3 to 1/4+1/2+1/4 (offsets too).
hero = hero.replace(
    '[vc_column_inner el_class="dfd_col-tablet-12" width="1/3" offset="vc_col-lg-4 vc_col-md-2 vc_col-xs-1"][/vc_column_inner][vc_column_inner el_class="dfd_col-tablet-12" width="1/3" dfd_column_responsive_enable="dfd-column-responsive-enable" offset="vc_col-lg-4 vc_col-md-8 vc_col-xs-10"',
    '[vc_column_inner el_class="dfd_col-tablet-12" width="1/4" offset="vc_col-lg-3 vc_col-md-2 vc_col-xs-1"][/vc_column_inner][vc_column_inner el_class="dfd_col-tablet-12" width="1/2" dfd_column_responsive_enable="dfd-column-responsive-enable" offset="vc_col-lg-6 vc_col-md-8 vc_col-xs-10"',
)
hero = hero.replace(
    '[vc_column_inner el_class="dfd_col-tablet-12" width="1/3" offset="vc_col-lg-4 vc_col-md-2 vc_col-xs-1"][/vc_column_inner][/vc_row_inner]',
    '[vc_column_inner el_class="dfd_col-tablet-12" width="1/4" offset="vc_col-lg-3 vc_col-md-2 vc_col-xs-1"][/vc_column_inner][/vc_row_inner]',
)

# ---------- comparison table (Google Analytics agency vs The Datalabs Agency) ----------
CTH = "style=\"padding: 8px 14px; text-align: left; background-color: #000000 !important; border: none !important; border-bottom: 2px solid #c39f76 !important; font-family: 'Bebas Neue', sans-serif; font-size: 19px; font-weight: normal; letter-spacing: 1px; color: #ffffff !important;\""
CTHREC = CTH.replace('background-color: #000000 !important', 'background-color: #c39f76 !important').replace('color: #ffffff !important', 'color: #000000 !important')
def ctd(bg, align='left', color='#ffffff', bold=False):
    s = f'padding: 8px 14px; font-size: 15px; text-align: {align}; background-color: {bg} !important; border: none !important; border-bottom: 1px solid #2f2e3a !important; color: {color} !important;'
    if bold: s += ' font-weight: bold;'
    return f'style="{s}"'

rows = [
    ('Main job', 'Configures tracking and tags in GA4', 'Turns existing data into dashboards and reports'),
    ('Typical deliverable', 'Tracking plan, GA4 property setup', 'Power BI or Tableau dashboard, BI style guide'),
    ('Best fit', 'First time setting up analytics', 'Data exists; it needs to be visualised'),
    ('Engagement shape', 'Ongoing tag maintenance', 'Fixed workshop, project, or hourly consulting'),
]
body_rows = []
for i, (crit, ga, dl) in enumerate(rows):
    bg_left, bg_rec = ('#000000', '#c39f76' if False else '#111111')  # recommended col always #111111 per exemplar
    bg = '#000000'
    cells = f'<td {ctd(bg, bold=True)}>{crit}</td><td {ctd(bg)}>{ga}</td><td {ctd("#111111")}>{dl}</td>'
    body_rows.append('<tr>' + cells + '</tr>')
compare_table = (
    '<div style="overflow-x: auto;">\n<table style="width: 100%; border-collapse: collapse !important; background-color: #000000 !important; border: none !important;">\n<thead>\n<tr>'
    + f'<th scope="col" {CTH}>Criterion</th><th scope="col" {CTH}>Google Analytics agency</th><th scope="col" {CTHREC}>The Datalabs Agency</th>'
    + '</tr>\n</thead>\n<tbody>\n' + '\n'.join(body_rows) + '\n</tbody>\n</table>\n</div>'
    + '\n<p style="text-align: left; font-size: 13px; font-style: italic; color: #8a8a95; margin-top: 10px;">Many clients run both &mdash; a Google Analytics agency for tracking, and The <strong>Datalabs Agency</strong> for the dashboards built on top of it.</p>'
)

def table_row(subtitle, heading, intro, table_html):
    block = fill(blocks['table'], {'TABLE_SUBTITLE': subtitle, 'TABLE_HEADING': heading})
    m = re.search(r'(\[vc_column_text css=""\]\n).*?(\n\[/vc_column_text\])', block, flags=re.S)
    guts = f'<p style="text-align: center;"><strong>{intro}</strong></p>\n\n{table_html}'
    return block[:m.start(1) + len(m.group(1))] + guts + block[m.end(2) - len(m.group(2)):]

t_compare = table_row(
    'Same word, different job',
    'Google Analytics agency or Datalabs &mdash; which do you need?',
    'The two are complementary, not competing &mdash; here is where each one starts and stops.',
    compare_table)

# ---------- sections ----------
sec_deliver = fill(blocks['section1'], {
    'SECTION_C_SUBTITLE': 'What you actually get',
    'SECTION_C_HEADING': 'What do you actually get from an engagement?',
    'SECTION_C_ANSWER': 'Most engagements produce a working <strong>Power BI</strong> or <strong>Tableau dashboard</strong>, a <strong>BI style guide</strong> your team can reuse on future builds, and a short handover session so staff can maintain it without calling us back.',
    'SECTION_C_DETAIL': 'For a dashboard-only engagement we also run a dedicated <strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/dashboard-design-services/">dashboard design service</a></strong>, and teams standardised on Microsoft&rsquo;s platform can go straight to our <strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/power-bi-dashboard-design/">Power BI dashboard design page</a></strong>.',
})
sec_who = fill(blocks['section1'], {
    'SECTION_C_SUBTITLE': 'Who this is for',
    'SECTION_C_HEADING': 'Who is this actually built for?',
    'SECTION_C_ANSWER': 'We work best with marketing, finance and operations teams that already collect data in <strong>Google Analytics</strong>, Power BI or a CRM but have no in-house designer to turn it into something a board or client can read.',
    'SECTION_C_DETAIL': 'Teams earlier in that journey &mdash; with no analytics or reporting set up yet &mdash; are better served by our <strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/analytics-reporting-agency/data-analysis/">data analysis and reporting service</a></strong>, which builds the numbers this page assumes you already have.',
})
sec_pricing = fill(blocks['section2'], {
    'SECTION_D_SUBTITLE': 'How pricing works',
    'SECTION_D_HEADING': 'What does an analytics engagement cost?',
    'SECTION_D_ANSWER': 'Scoped consulting work is <strong>$250 per hour inc GST</strong>, billed in one-hour blocks with a four-hour maximum, which suits a single dashboard fix or style-guide review. Larger dashboard builds and training programmes are quoted per engagement.',
    'SECTION_D_RATIONALE': 'Hourly pricing works for a tightly scoped fix; a full <strong>dashboard design</strong> engagement or a multi-session training programme has too many moving parts for an hourly rate to price fairly, so those are quoted once we understand the brief. See our <strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/data-visualisation-workshop-pricing/">workshop pricing page</a></strong> for the rate card behind our training days.',
})

# ---------- FAQ ----------
faq_pairs = [
    ('How much does it cost to hire a digital analytics agency?',
     'Scoped consulting work is $250 per hour inc GST, billed in one-hour blocks with a four-hour maximum, which suits a single dashboard fix or style-guide review. Larger dashboard builds and training programmes are quoted per engagement, and the public range for a full workshop day is $3,000 to $8,000 inc GST.'),
    ('Do you set up Google Analytics, or is that a different service?',
     'Setting up tracking and tags inside Google Analytics is a different job to ours. We work with the data once it already exists, turning it into dashboards and reports; if you need the analytics set up first, our <a href="https://www.datalabsagency.com/analytics-reporting-agency/data-analysis/">data analysis and reporting service</a> covers that earlier stage.'),
    ('Can you work alongside our existing analytics team?',
     'Yes. We commonly work alongside an in-house analyst or a Google Analytics agency, picking up once the numbers exist and turning them into dashboards, style guides and reports the rest of the business can use.'),
    ('Do you work with companies outside Australia?',
     'Yes. On-site workshops and dashboard projects have run in the United States, Germany, Saudi Arabia, Hong Kong and Singapore, and remote engagements run live over Zoom, Microsoft Teams or Webex from anywhere.'),
    ('What tools do you design dashboards in?',
     'Most commonly Power BI and Tableau, though the design approach is tool-agnostic and works equally well in Excel or PowerPoint. We recommend the platform that fits the tools your team already uses, rather than pushing a preferred one.'),
]
faq_map = {'FAQ_TOPIC': 'Analytics agency FAQ', 'FAQ_CTA_TEXT': 'Ask us a question', 'FAQ_CTA_URL': CONTACT}
for i, (q, a) in enumerate(faq_pairs, 1):
    faq_map[f'FAQ_Q{i}'] = q
    faq_map[f'FAQ_A{i}'] = a
faq = fill(blocks['faq'], faq_map)

def plain(s):
    s = re.sub(r'<[^>]+>', '', s)
    for ent, ch in [('&mdash;', '—'), ('&ndash;', '–'), ('&amp;', '&'), ('&rsquo;', '’'), ('&ldquo;', '“'), ('&rdquo;', '”'), ('&times;', 'x')]:
        s = s.replace(ent, ch)
    return s
entities = [{"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in faq_pairs]
schema = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}, ensure_ascii=False) + '</script>'
assert '<' not in json.dumps([e['acceptedAnswer']['text'] for e in entities]), 'HTML leaked into FAQPage JSON-LD'
enc = base64.b64encode(urllib.parse.quote(schema, safe='').encode()).decode()
faq = re.sub(r'\[vc_raw_html\][^\[]*\[/vc_raw_html\]', '[vc_raw_html]' + enc + '[/vc_raw_html]', faq)

# ---------- articles (first person plural -- "we/our", never Oddtoe's singular "I") ----------
P = '<p style="line-height: 22px; text-align: left;">'
art1 = fill(blocks['article1'], {
    'ARTICLE_1_SUBTITLE': 'What changes once you&rsquo;re on board&hellip;',
    'ARTICLE_1_HEADING': 'Why we treat analytics as a design problem',
    'ARTICLE_1_BODY': f'''{P}Most companies do not have an analytics problem. They have a <strong>communication</strong> problem: the data is already sitting in Google Analytics, Power BI, or a CRM that nobody outside the analytics team opens. We have watched that pattern for more than a decade, across workshops and dashboard projects for <strong>Mercedes-Benz</strong>, <strong>Adidas</strong>, and <strong>UPS</strong>, and it rarely changes with more dashboards &mdash; it changes with better ones.</p>
{P}A dashboard full of charts is not automatically useful. <strong>Design</strong> decides whether a stakeholder reads it in ten seconds or ignores it for a week: which number leads, what gets a colour, what gets left off entirely. That is the layer we work in &mdash; one level up from the analytics platform itself, whichever one your team already uses.</p>
{P}We are tool-agnostic on purpose. The same design thinking works whether your team lives in <strong>Power BI</strong>, <strong>Tableau</strong>, Excel, or PowerPoint, because the hard part was never the software &mdash; it is deciding what the dashboard is actually for. A <strong>BI style guide</strong> exists to answer that once, so every dashboard your team builds afterwards follows the same rules automatically.</p>
{P}That approach is why our workshops cover <strong>data storytelling</strong> and <strong>infographic design</strong> alongside tool-specific sessions &mdash; see the full list on our <strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/data-visualization-training-workshops-webinars/">training workshops page</a></strong>. A team that understands the design principles gets more out of every dashboard we hand over, long after the engagement ends.</p>''',
})
art2 = fill(blocks['article2'], {
    'ARTICLE_2_SUBTITLE': 'Where we sit in your team',
    'ARTICLE_2_HEADING': 'Where we fit around your existing team',
    'ARTICLE_2_BODY': f'''{P}We are based in <strong>Melbourne</strong>, and most of our clients are not. On-site workshops and dashboard projects have taken us to the <strong>United States</strong>, <strong>Germany</strong>, <strong>Saudi Arabia</strong>, <strong>Hong Kong</strong>, and <strong>Singapore</strong>, alongside cities across Australia. Analytics and reporting work does not need a shared office &mdash; it needs a shared file and a video call.</p>
{P}Remote engagements run live over <strong>Zoom</strong>, Microsoft Teams, or Webex, and a full workshop day can split across <strong>two mornings</strong> to suit time zones on the other side of the world. Dashboard and reporting projects work the same way: we review your data, share drafts, and iterate on calls rather than requiring anyone to travel.</p>
{P}We are usually the second team in the room, not the first. Most clients already have someone collecting the data &mdash; an analyst, a marketing lead, an agency handling <strong>Google Analytics</strong> &mdash; and bring us in once that data needs to go somewhere the rest of the business can use it: a board pack, a client report, a shared dashboard.</p>
{P}If that describes where you are, the fastest way in is a short call about what you already have and what you need it to become. Rates for scoped consulting work start at <strong>$250 per hour</strong> (one-hour blocks, four-hour maximum, inc GST); larger builds and training programmes are quoted once we understand the brief &mdash; see our <strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/data-visualisation-workshop-pricing/">workshop pricing page</a></strong> for the full rate card.</p>''',
})

# ---------- fixed footer: rewrite enquiry-form heading/subtitle to this page's topic (Lesson 12) ----------
fixed = blocks['fixed'].replace(
    'subtitle="Professional &amp; Thought-provoking" title_font_options="tag:h2" subtitle_font_options="tag:h3"]Looking for a speaker for your event?[/dfd_heading]',
    'subtitle="Tell us what you&rsquo;re tracking&hellip;" title_font_options="tag:h2" subtitle_font_options="tag:h3"]Sitting on data with nowhere for it to go?[/dfd_heading]',
)
assert fixed != blocks['fixed'], 'enquiry-form heading/subtitle replacement did not match — kit text may have changed'

# ---------- assemble, strip comments ----------
page = '\n'.join([hero, t_compare, sec_deliver, sec_who, sec_pricing, faq, art1, blocks['offers'], art2, fixed])
page = re.sub(r'<!--(?! YOAST).*?-->\n?', '', page, flags=re.S).strip()

leftover = re.findall(r'\{\{[A-Z0-9_]+', page)
assert not leftover, 'unfilled tokens: ' + str(set(leftover))

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(page)

yoast = ('YOAST SEO TITLE: Digital Analytics Agency | Datalabs Agency (56 chars) | '
         'META DESCRIPTION: The Datalabs Agency turns your Google Analytics, Power BI and Tableau data into dashboards and reports your board will read. Melbourne-based since 2012. (154 chars)')
print('\nSET THESE IN WP-ADMIN (Yoast):\n ' + yoast)
print('composed chars:', len(page), '| tables:', page.count('<table'), '| tokens left: 0')
