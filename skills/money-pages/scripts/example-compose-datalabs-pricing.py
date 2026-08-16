#!/usr/bin/env python3
"""Compose the workshop pricing page from the money-pages design kit."""
import re, base64, urllib.parse, pathlib, json, os, urllib.request

KIT = pathlib.Path('skills/money-pages/references/design-kit.html').read_text()
OUT = pathlib.Path('/private/tmp/claude-501/-Users-Ottinger-Claude-Projects-2026-project-manager-agent/a78a6ab8-b8af-4f3d-9842-393c8ffff22d/scratchpad/composed-52962.html')

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
    'PAGE_SUBTITLE': 'What a private workshop really costs...',
    'PAGE_TITLE': 'Workshop Pricing',
    'UPDATED_DATE': 'August 2026',
    'HOOK': 'A private data visualisation workshop with Datalabs Agency costs between <strong>$4,600 and $7,500 inc GST</strong>, depending on length and delivery format. Every price includes <strong>up to 12 attendees</strong>, so for a full team the per-person cost is well below public training classes. Full pricing, inclusions, and group-size options are below.',
    'SECTION_A_SUBTITLE': 'The straight answer, up front...',
    'SECTION_A_HEADING': 'How much does a data visualisation workshop cost in Australia?',
    'SECTION_A_INTRO': 'Corporate data visualisation and data storytelling workshops in Australia generally cost <strong>$3,000 to $8,000 per workshop day</strong> for private groups. Datalabs Agency&rsquo;s 2026 prices sit inside that range: <strong>$4,600</strong> for a remote half-day through to <strong>$7,500 inc GST</strong> for a full day on site, including up to 12 attendees.',
    'CANONICAL_SENTENCE': 'Datalabs Agency is a Melbourne-based data visualization consultancy founded in 2012 that delivers corporate training workshops (Power BI, Tableau, data storytelling), dashboard design, and BI style guides for clients including Mercedes-Benz, Adidas, and UPS.',
    'SECTION_B_SUBTITLE': 'Everything your team needs...',
    'SECTION_B_HEADING': 'What is included in every workshop?',
    'SECTION_B_ANSWER': 'Every Datalabs workshop includes the facilitator, a tailored agenda from our ~16 workshop topics, an interactive workbook, <strong>70 dashboard grid templates</strong>, and <strong>18 downloadable dashboard icons</strong>. Workshops are led by our founder, who learned visual storytelling at <strong>National Geographic</strong>, and focus on design thinking rather than software mechanics.',
    'SECTION_B_CONTEXT': 'That tool-agnostic approach means the same workshop works whether your team lives in <strong>Power BI</strong>, <strong>Tableau</strong>, Excel, or PowerPoint. Popular topics include Introduction to Data Visualisation &amp; Storytelling, Designing Great Dashboards, Infographics &amp; Report Design, and Creative Data Presentations with PowerPoint &mdash; see the full list on our <a href="/?page_id=661">training workshops page</a>.',
    'PRIMARY_CTA_TEXT': 'Get a fixed quote',
    'PRIMARY_CTA_URL': CONTACT,
})

# ---------- table builder (styles copied from the kit exemplars) ----------
# Datalabs link style (Otto, 16 Aug 2026): in-content links are
# <strong><a class="dfd-custom-link-decorated" href=...>label</a></strong> -- never inline colours.
# The class is driven by Ronneby Theme Options -> Styling options -> Link options
# (tan #c39f76 base, olive #8a8f6a hover) + the Custom CSS underline block (dotted, size inherit).
TH = "style=\"padding: 14px 18px; text-align: left; background-color: #000000 !important; border: none !important; border-bottom: 2px solid #c39f76 !important; font-family: 'Bebas Neue', sans-serif; font-size: 21px; font-weight: normal; letter-spacing: 1px; color: #ffffff !important; white-space: nowrap;\""
THR = TH.replace('text-align: left', 'text-align: right')
def td(bg, align='left', color='#ffffff', bold=False, nowrap=False):
    s = f'padding: 12px 18px; text-align: {align}; background-color: {bg} !important; border: none !important; border-bottom: 1px solid #2f2e3a !important; color: {color} !important;'
    if bold: s += ' font-weight: bold;'
    if nowrap: s += ' white-space: nowrap;'
    return f'style="{s}"'

def build_table(heads, rows, price_col=True, spotlight_row=None, footnote=None):
    ths = ''.join(f'<th scope="col" {THR if price_col and i == len(heads)-1 else TH}>{h}</th>' for i, h in enumerate(heads))
    body = []
    for r, cells in enumerate(rows):
        bg = '#111111' if (spotlight_row == r or (spotlight_row is None and r % 2 == 1)) else '#000000'
        tds = []
        for c, cell in enumerate(cells):
            if price_col and c == len(cells) - 1:
                tds.append(f'<td {td(bg, "right", "#c39f76", bold=True, nowrap=True)}>{cell}</td>')
            elif c == 0:
                tds.append(f'<td {td(bg, bold=True)}>{cell}</td>')
            else:
                tds.append(f'<td {td(bg)}>{cell}</td>')
        body.append('<tr>' + ''.join(tds) + '</tr>')
    fn = f'\n<p style="text-align: left; font-size: 13px; font-style: italic; color: #8a8a95; margin-top: 10px;">{footnote}</p>' if footnote else ''
    return ('<div style="overflow-x: auto;">\n<table style="width: 100%; border-collapse: collapse !important; background-color: #000000 !important; border: none !important;">\n'
            f'<thead>\n<tr>{ths}</tr>\n</thead>\n<tbody>\n' + '\n'.join(body) + '\n</tbody>\n</table>\n</div>' + fn)

def table_row(subtitle, heading, intro, table_html):
    block = fill(blocks['table'], {'TABLE_SUBTITLE': subtitle, 'TABLE_HEADING': heading})
    # replace the exemplar guts of the single vc_column_text with this table's content
    m = re.search(r'(\[vc_column_text css=""\]\n).*?(\n\[/vc_column_text\])', block, flags=re.S)
    guts = f'<p style="text-align: center;"><strong>{intro}</strong></p>\n\n{table_html}'
    return block[:m.start(1) + len(m.group(1))] + guts + block[m.end(2) - len(m.group(2)):]

t_prices = table_row(
    'The current rate card...', 'Datalabs workshop price list (2026)',
    'All prices are in Australian dollars, include GST, and include up to 12 attendees, the interactive workbook, and downloadable templates. Remote workshops run live on Zoom, Microsoft Teams, or Webex; on-site workshops are delivered at your offices.',
    build_table(
        ['Workshop format', 'Length', 'Price (inc GST)'],
        [['On-site workshop, full day', '~7 hours', '$7,500'],
         ['On-site workshop, half-day', '4 hours', '$5,200'],
         ['Remote workshop, full day', '~7 hours, can split over two mornings', '$6,200'],
         ['Remote workshop, half-day', '4 hours, or two 2-hour sessions', '$4,600']]))

t_groups = table_row(
    'Bring the whole team...', 'Group pricing at a glance',
    'Each workshop price includes up to 12 attendees; larger groups are priced like this:',
    build_table(
        ['Group size', 'How it is priced'],
        [['Up to 12 people', 'Included in the workshop price'],
         ['13&ndash;20 people', '+$250 per extra attendee per day'],
         ['21+ people', 'Split into two cohorts, each with its own session'],
         ['Multiple teams, offices, or cities', 'Quoted as a training programme']],
        price_col=False))

# Format comparison — comparison-exemplar treatment: recommended column (private workshop) gets
# tan th + #111 cells; compact padding (approved default for wide tables); tan check / dim dash cells.
CTH = "style=\"padding: 8px 14px; text-align: left; background-color: #000000 !important; border: none !important; border-bottom: 2px solid #c39f76 !important; font-family: 'Bebas Neue', sans-serif; font-size: 19px; font-weight: normal; letter-spacing: 1px; color: #ffffff !important;\""
CTHREC = CTH.replace('background-color: #000000 !important', 'background-color: #c39f76 !important').replace('color: #ffffff !important', 'color: #000000 !important')
def ctd(bg, align='left', color='#ffffff', bold=False):
    s = f'padding: 8px 14px; font-size: 15px; text-align: {align}; background-color: {bg} !important; border: none !important; border-bottom: 1px solid #2f2e3a !important; color: {color} !important;'
    if bold: s += ' font-weight: bold;'
    return f'style="{s}"'
TICK = lambda bg: f'<td {ctd(bg, "center", "#c39f76", bold=True)}>&#10003;</td>'
DASH = lambda bg: f'<td {ctd(bg, "center", "#8a8a95")}>&mdash;</td>'
fmt_rows = []
for crit, course, pub, priv in [
    ('Pricing model', '$127 per person', 'Per seat, per day', 'Per session &mdash; up to 12 people included'),
    ('Content', 'Fixed curriculum', 'Fixed curriculum', 'Tailored from ~16 workshop topics'),
    ('Uses your own data', None, None, True),
    ('Scheduling', 'Anytime, self-paced', 'Provider&rsquo;s dates', 'Your dates'),
    ('Best for', 'Individuals starting out', 'One or two people', 'Whole teams'),
]:
    cells = f'<td {ctd("#000000", bold=True)}>{crit}</td>'
    for val, bg in [(course, '#000000'), (pub, '#000000'), (priv, '#111111')]:
        if val is True: cells += TICK(bg)
        elif val is None: cells += DASH(bg)
        else: cells += f'<td {ctd(bg)}>{val}</td>'
    fmt_rows.append('<tr>' + cells + '</tr>')
fmt_table = ('<div style="overflow-x: auto;">\n<table style="width: 100%; border-collapse: collapse !important; background-color: #000000 !important; border: none !important;">\n<thead>\n<tr>'
    + f'<th scope="col" {CTH}>&nbsp;</th><th scope="col" {CTH}>Self-paced course</th><th scope="col" {CTH}>Public class</th><th scope="col" {CTHREC}>Private team workshop</th>'
    + '</tr>\n</thead>\n<tbody>\n' + '\n'.join(fmt_rows) + '\n</tbody>\n</table>\n</div>'
    + '\n<p style="text-align: left; font-size: 13px; font-style: italic; color: #8a8a95; margin-top: 10px;">Our self-paced courses &mdash; An Introduction to Data Visualization and Storytelling, and Designing Great Dashboards &mdash; are $127 each in the <strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/shop/">Datalabs shop</a></strong>.</p>')
t_compare = table_row(
    'Three ways to learn...', 'Private workshop or public course &mdash; which should you book?',
    'The right format depends on how many people need the skills and how tailored the content must be. Here is how the three options differ:',
    fmt_table)

# ---------- sections ----------
sec_c = fill(blocks['section1'], {
    'SECTION_C_SUBTITLE': 'From four people to forty...',
    'SECTION_C_HEADING': 'How does group size change the price?',
    'SECTION_C_ANSWER': 'Each workshop price includes <strong>up to 12 attendees</strong>. For groups of 13 to 20, add <strong>$250 per additional attendee per day</strong>, which covers their materials and keeps the session hands-on. Beyond 20 attendees we split the group into two cohorts rather than diluting the workshop.',
    'SECTION_C_DETAIL': 'Workshops teach best at 20 people or fewer &mdash; past that point, exercises and individual feedback suffer. Splitting a larger group into cohorts costs more than surcharging would, but both groups get the workshop that earns the feedback. Multi-team or multi-city rollouts are quoted as a single <a href="/?page_id=661">data visualisation training programme</a>.',
})
sec_global = fill(blocks['section1'], {
    'SECTION_C_SUBTITLE': 'Melbourne based, globally delivered...',
    'SECTION_C_HEADING': 'Can you deliver a workshop in our city?',
    'SECTION_C_ANSWER': 'Yes. Datalabs workshops are delivered <strong>worldwide</strong> from our Melbourne base. On-site sessions have run in the <strong>United States</strong>, <strong>Germany</strong> (several cities), <strong>Saudi Arabia</strong>, <strong>Hong Kong</strong>, and <strong>Singapore</strong>, as well as across Australia. Travel is quoted up front with the workshop price, so international delivery arrives as one fixed, itemised quote.',
    'SECTION_C_DETAIL': 'Remote delivery crosses borders even more easily: workshops run live on Zoom, Microsoft Teams, or Webex, and a full day can split into <strong>two mornings</strong> to suit your time zone. For in-person delivery the session fee is the same rate card shown on this page plus travel &mdash; no international premium hidden in the price. If your team is spread across offices or countries, ask for a <a href="https://www.datalabsagency.com/contact-us/">programme quote</a>.',
})
sec_d = fill(blocks['section2'], {
    'SECTION_D_SUBTITLE': 'Levers you control...',
    'SECTION_D_HEADING': 'What moves the price up or down?',
    'SECTION_D_ANSWER': 'Prices rise with extra attendees beyond 12, travel beyond Melbourne, and deep customisation &mdash; building exercises around your own datasets, dashboards, or brand guidelines, which is quoted as preparation work. Prices come down for <strong>multi-workshop series</strong> bookings and for choosing <strong>remote delivery</strong> over on-site.',
    'SECTION_D_RATIONALE': 'If you are planning a series &mdash; the same workshop for several teams, or a progression across skill levels &mdash; ask for a programme quote. Series bookings attract a discount on subsequent sessions, and multi-city or multi-office rollouts are quoted as a single training programme rather than one-off workshops.',
})

# ---------- FAQ ----------
faq_pairs = [
    ('Is GST included in the prices?',
     'Yes. All prices on this page are in Australian dollars and include GST. If you need an itemised quote for procurement &mdash; inclusions, attendee numbers, preparation hours, and travel listed separately &mdash; we provide one before you commit to anything.'),
    ('Do you run workshops outside Melbourne?',
     'Yes. Remote workshops run anywhere via Zoom, Microsoft Teams, or Webex, and on-site workshops are delivered worldwide &mdash; recent sessions have run in Sydney, Canberra, Hong Kong, and Germany. On-site delivery outside Melbourne adds travel costs, quoted up front with the workshop price.'),
    ('What if we have 30 attendees?',
     'We split the group into two cohorts and run two sessions &mdash; for example, morning and afternoon of the same day. Each cohort gets the full interactive workshop, and the second session is priced as part of a series rather than as two separate bookings.'),
    ('Is there a cheaper option for small teams or individuals?',
     'Yes. Our self-paced online courses &mdash; An Introduction to Data Visualization and Storytelling, and Designing Great Dashboards &mdash; are $127 each in the <a href="https://www.datalabsagency.com/shop/">Datalabs shop</a>, and include the same design frameworks the live workshops teach.'),
    ('How do we book a workshop?',
     'Send us your team size, preferred format, and rough timing through the contact form on this site, and we will reply with availability and a fixed quote. There is no phone tag and no obligation &mdash; you will know the exact price before you decide.'),
    ('Do you offer government or not-for-profit rates?',
     'Yes &mdash; government and not-for-profit rates are available; mention your organisation when you enquire. Every quote is itemised for procurement, with inclusions, attendee numbers, preparation hours, and travel listed separately, and remote delivery works well for distributed teams. Recent government-sector sessions have run in Canberra.'),
]
faq_map = {'FAQ_TOPIC': 'Workshop pricing', 'FAQ_CTA_TEXT': 'Ask for availability', 'FAQ_CTA_URL': CONTACT}
for i, (q, a) in enumerate(faq_pairs, 1):
    faq_map[f'FAQ_Q{i}'] = q
    faq_map[f'FAQ_A{i}'] = a
faq = fill(blocks['faq'], faq_map)
# kit accordion ships 5 sections; append Q6 as a new section with a unique tab_id
q6, a6 = faq_pairs[5]
sec6 = f'[vc_tta_section title="{q6}" tab_id="1786585600001-gov-rates-6q"][vc_column_text css=""]\n<p style="text-align: center;">{a6}</p>\n[/vc_column_text][/vc_tta_section]'
faq = faq.replace('[/dfd_accordion]', sec6 + '[/dfd_accordion]')

def plain(s):
    s = re.sub(r'<[^>]+>', '', s)
    for ent, ch in [('&mdash;', '—'), ('&ndash;', '–'), ('&amp;', '&'), ('&rsquo;', '’'), ('&times;', 'x')]:
        s = s.replace(ent, ch)
    return s
entities = [{"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in faq_pairs]
schema = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}, ensure_ascii=False) + '</script>'
enc = base64.b64encode(urllib.parse.quote(schema, safe='').encode()).decode()
faq = re.sub(r'\[vc_raw_html\][^\[]*\[/vc_raw_html\]', '[vc_raw_html]' + enc + '[/vc_raw_html]', faq)

# ---------- articles ----------
P = '<p style="line-height: 22px; text-align: left;">'
art1 = fill(blocks['article1'], {
    'ARTICLE_1_SUBTITLE': 'The economics of a good workshop...',
    'ARTICLE_1_HEADING': 'Why we price per session, not per seat',
    'ARTICLE_1_BODY': f'''{P}Public training classes price <strong>per seat</strong>. Private workshops price <strong>per session</strong>. That single difference decides which one makes sense for your team, and it is why this page quotes session prices rather than per-person rates.</p>
{P}A public one-day class in Australia charges <strong>$395 to $622 per person</strong>. Send twelve people and you have spent roughly the price of a private full day &mdash; except the curriculum was generic, the examples were someone else&rsquo;s data, and the date was fixed by the provider. A private session flips all three: the agenda is tailored from our ~16 workshop topics, the exercises can use your own dashboards and reports, and the workshop runs when your team can actually attend.</p>
{P}Per-session pricing also sets an honest ceiling on quality. Workshops teach best at <strong>20 people or fewer</strong>; past that, the exercises and individual feedback that justify a live workshop stop working. That is why groups beyond 20 split into cohorts rather than paying a surcharge &mdash; and why the second cohort is priced as part of a series, not a separate booking.</p>
{P}I learned visual storytelling at <strong>National Geographic</strong>, and I have run these sessions for corporate teams for more than a decade. The best sessions are never the biggest ones &mdash; they are the ones where every attendee has built something with their own data by the afternoon. The pricing model exists to protect exactly that.</p>''',
})
art2 = fill(blocks['article2'], {
    'ARTICLE_2_SUBTITLE': 'From National Geographic to now...',
    'ARTICLE_2_HEADING': 'Who teaches these workshops?',
    'ARTICLE_2_BODY': f'''{P}I started visualizing data at the <strong>National Geographic Society</strong> back in the early 2000s. A lot has changed since then. I took what I learned there &mdash; <strong>visual storytelling</strong> and <strong>infographic design</strong> &mdash; and applied it to my new world and new company Down Under.</p>
{P}I was one of the first to bring infographics to <strong>Australia</strong>. The problem was it was too early. No one at that time understood the power of that type of visual data and storytelling. Believe it or not, &ldquo;What is an infographic?&rdquo; was a typical question.</p>
{P}I was at the first <strong>Tableau</strong> roadshow in <strong>Melbourne, Australia</strong>. The speaker asked the audience of a thousand or so attendees, &ldquo;Who here is currently using our product?&rdquo; Roughly <em>one in ten</em> hands went up. Since then, <strong>Microsoft Power BI</strong> has overtaken Tableau, both in client interest and in functionality. I now design and teach in both &mdash; see our <a href="/?page_id=367">dashboard design page</a>.</p>
{P}In the early days of the BI revolution, consulting with <strong>Marriott Hotels</strong> in <strong>Hong Kong</strong>, I saw a need for <a href="/?page_id=394">data visualization style guides</a>. Too many dashboards are created without a design philosophy, without a common design language, and without proper attention to <strong>color theory, typography, grid systems,</strong> and <strong>user experience (UX) design</strong>. My data visualization style guides now operate inside companies such as <strong>Mercedes-Benz</strong> in Germany, <strong>Intel</strong> in San Francisco, <strong>BlackRock</strong> in New York, and <strong>Telstra</strong> in Australia.</p>
{P}What&rsquo;s next in data visualization? I think you know where this is going: <strong>artificial intelligence</strong>. Where am I going with the <strong>Datalabs Agency</strong>? Same answer.</p>''',
})

# ---------- assemble, strip comments ----------
page = '\n'.join([hero, t_prices, sec_c, t_groups, sec_d, t_compare, sec_global, faq, art1, blocks['offers'], art2, blocks['fixed']])
page = re.sub(r'<!--(?! YOAST).*?-->\n?', '', page, flags=re.S).strip()
yoast = '<!-- YOAST SEO TITLE: Data Visualisation Workshop Pricing 2026 — Datalabs Agency | META DESCRIPTION: Datalabs Agency workshop pricing for 2026: remote half-days $4,600, on-site full days $7,500 inc GST for up to 12 people. Compare Australian training costs. -->\n'
page = yoast + page

leftover = re.findall(r'\{\{[A-Z0-9_]+', page)
assert not leftover, 'unfilled tokens: ' + str(set(leftover))
OUT.write_text(page)
print('composed chars:', len(page), '| tables:', page.count('<table'), '| tokens left: 0')

# ---------- update WP draft 52962 ----------
user, pw = os.environ['WP_DATALABS_USER'], os.environ['WP_DATALABS_APP_PASSWORD']
author = os.environ.get('WP_DATALABS_AUTHOR_ID')
body = {'content': page, 'status': 'draft', 'slug': 'data-visualisation-workshop-pricing'}
if author: body['author'] = int(author)
req = urllib.request.Request(
    'https://www.datalabsagency.com/wp-json/wp/v2/pages/52962',
    data=json.dumps(body).encode(),
    headers={'Content-Type': 'application/json',
             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
             'Authorization': 'Basic ' + base64.b64encode(f'{user}:{pw}'.encode()).decode()},
    method='POST')
with urllib.request.urlopen(req) as r:
    d = json.load(r)
print('WP updated:', d['id'], '| status:', d['status'], '| slug:', d['slug'], '| author:', d['author'], '| modified:', d['modified'])
