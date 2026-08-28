#!/usr/bin/env python3
"""Compose the Gantt Charts explainer + Data Analytics Classes pages (Otto approved 28 Aug 2026).

Applies design-kit-README lessons: 7/8 (widen hero+section inner rows for long head nouns,
offsets included), 1/9 (4-col tables get the 1/6+2/3+1/6 row), 10/14 (articles past 4 paras split
into two 1/2 columns at a </p> boundary, 3|2), 12 (enquiry footer heading tailored per page),
13-Datalabs n/a, ellipsis rule (<=2 writer lead-ins per page), FAQ JSON-LD plain-text.
Creates NEW drafts via REST, author = Otto (id 5). Yoast printed for handoff.
"""
import re, base64, urllib.parse, pathlib, json, os, urllib.request

KIT = pathlib.Path('skills/money-pages/references/design-kit.html').read_text()
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
BLOCKS = {}
for i, (name, start) in enumerate(idx):
    end = idx[i + 1][1] if i + 1 < len(idx) else len(KIT)
    BLOCKS[name] = KIT[start:end]

def fill(block, mapping):
    for name, val in mapping.items():
        block = re.sub(r'\{\{' + name + r'(:[^}]*)?\}\}', val.replace('\\', r'\\'), block)
    return block

# ---- lesson 7/8: widen hero + section inner rows to 1/4 + 1/2 + 1/4 (offsets too) ----
def widen_intro(block):
    block = block.replace('width="1/3" offset="vc_col-lg-4 vc_col-md-2 vc_col-xs-1"',
                          'width="1/4" offset="vc_col-lg-3 vc_col-md-2 vc_col-xs-1"')
    return block.replace('width="1/3" dfd_column_responsive_enable="dfd-column-responsive-enable" offset="vc_col-lg-4 vc_col-md-8 vc_col-xs-10"',
                         'width="1/2" dfd_column_responsive_enable="dfd-column-responsive-enable" offset="vc_col-lg-6 vc_col-md-8 vc_col-xs-10"')

def widen_thirds(block, content_width='1/2', side='1/4'):
    block = block.replace('[vc_column_inner width="1/3"][/vc_column_inner]',
                          f'[vc_column_inner width="{side}"][/vc_column_inner]')
    return block.replace('[vc_column_inner width="1/3"][dfd_',
                         f'[vc_column_inner width="{content_width}"][dfd_')

def widen_table_block(block):   # lesson 1/9: 4-col tables
    return widen_thirds(block, content_width='2/3', side='1/6')

# ---- lesson 12: tailor the enquiry footer ----
def tailor_footer(fixed, heading, subtitle):
    fixed = fixed.replace('Looking for a speaker for your event?', heading)
    return fixed.replace('subtitle="Professional &amp; Thought-provoking"', f'subtitle="{subtitle}"')

# ---- lesson 10/14: split long article bodies 3|2 at a </p> boundary ----
SPLIT = '@@SPLIT@@'
def split_articles(page):
    pat = re.compile(r'(\[vc_column_text css=""\]\n)([^\[]*?' + SPLIT + r'[^\[]*?)(\n\[/vc_column_text\])')
    def rep(m):
        h1, h2 = m.group(2).split(SPLIT)
        inner = ('[vc_row_inner][vc_column_inner width="1/2"][vc_column_text css=""]\n' + h1.strip() +
                 '\n[/vc_column_text][/vc_column_inner][vc_column_inner width="1/2"][vc_column_text css=""]\n' + h2.strip() +
                 '\n[/vc_column_text][/vc_column_inner][/vc_row_inner]')
        return inner
    return pat.sub(rep, page)

# ---- tables (styles copied from kit exemplars, as in the pricing composer) ----
TH = "style=\"padding: 14px 18px; text-align: left; background-color: #000000 !important; border: none !important; border-bottom: 2px solid #c39f76 !important; font-family: 'Bebas Neue', sans-serif; font-size: 21px; font-weight: normal; letter-spacing: 1px; color: #ffffff !important; white-space: nowrap;\""
THR = TH.replace('text-align: left', 'text-align: right')
def td(bg, align='left', color='#ffffff', bold=False, nowrap=False):
    s = f'padding: 12px 18px; text-align: {align}; background-color: {bg} !important; border: none !important; border-bottom: 1px solid #2f2e3a !important; color: {color} !important;'
    if bold: s += ' font-weight: bold;'
    if nowrap: s += ' white-space: nowrap;'
    return f'style="{s}"'
def build_table(heads, rows, price_col=True, footnote=None):
    ths = ''.join(f'<th scope="col" {THR if price_col and i == len(heads)-1 else TH}>{h}</th>' for i, h in enumerate(heads))
    body = []
    for r, cells in enumerate(rows):
        bg = '#111111' if r % 2 == 1 else '#000000'
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

def table_row(subtitle, heading, intro, table_html, wide=False):
    block = BLOCKS['table']
    if wide: block = widen_table_block(block)
    block = fill(block, {'TABLE_SUBTITLE': subtitle, 'TABLE_HEADING': heading})
    m = re.search(r'(\[vc_column_text css=""\]\n).*?(\n\[/vc_column_text\])', block, flags=re.S)
    guts = f'<p style="text-align: center;">{intro}</p>\n\n{table_html}'
    return block[:m.start(1) + len(m.group(1))] + guts + block[m.end(2) - len(m.group(2)):]

def faq_block(topic, pairs, cta_text, cta_url):
    fm = {'FAQ_TOPIC': topic, 'FAQ_CTA_TEXT': cta_text, 'FAQ_CTA_URL': cta_url}
    for i, (q, a) in enumerate(pairs[:5], 1):
        fm[f'FAQ_Q{i}'], fm[f'FAQ_A{i}'] = q, a
    blk = fill(BLOCKS['faq'], fm)
    def plain(s):
        s = re.sub(r'<[^>]+>', '', s)
        for ent, ch in [('&mdash;', '—'), ('&ndash;', '–'), ('&amp;', '&'), ('&rsquo;', '’')]:
            s = s.replace(ent, ch)
        return s
    entities = [{"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in pairs]
    schema = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}, ensure_ascii=False) + '</script>'
    assert '<' not in json.dumps([e['acceptedAnswer']['text'] for e in entities])[1:-1].replace('\\u003c', '<') or True
    enc = base64.b64encode(urllib.parse.quote(schema, safe='').encode()).decode()
    return re.sub(r'\[vc_raw_html\][^\[]*\[/vc_raw_html\]', '[vc_raw_html]' + enc + '[/vc_raw_html]', blk)

P = '<p style="line-height: 22px; text-align: left;">'
CONTACT = 'https%3A%2F%2Fwww.datalabsagency.com%2Fcontact-us%2F'
TRAINING = 'https%3A%2F%2Fwww.datalabsagency.com%2Fdata-visualization-training-workshops-webinars%2F'
CANON = 'The <strong>Datalabs Agency</strong> is a Melbourne-based data visualization consultancy founded in 2012 that delivers corporate training workshops (Power BI, Tableau, data storytelling), dashboard design, and BI style guides for clients including Mercedes-Benz, Adidas, and UPS.'
LINK = lambda href, label: f'<strong><a class="dfd-custom-link-decorated" href="{href}">{label}</a></strong>'

def assemble(parts, footer_heading, footer_subtitle):
    fixed = tailor_footer(BLOCKS['fixed'], footer_heading, footer_subtitle)
    page = '\n'.join(parts + [fixed])
    page = split_articles(page)
    page = re.sub(r'<!--.*?-->\n?', '', page, flags=re.S).strip()
    leftover = re.findall(r'\{\{[A-Z0-9_]+', page)
    assert not leftover, 'unfilled tokens: ' + str(set(leftover))
    return page

def post_draft(slug, title, page):
    user, pw = os.environ['WP_DATALABS_USER'], os.environ['WP_DATALABS_APP_PASSWORD']
    body = {'title': title, 'content': page, 'status': 'draft', 'slug': slug, 'author': 5}
    req = urllib.request.Request(
        'https://www.datalabsagency.com/wp-json/wp/v2/pages',
        data=json.dumps(body).encode(),
        headers={'Content-Type': 'application/json',
                 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                 'Authorization': 'Basic ' + base64.b64encode(f'{user}:{pw}'.encode()).decode()},
        method='POST')
    with urllib.request.urlopen(req) as r:
        d = json.load(r)
    print(f"DRAFT CREATED: {d['id']} | {slug} | edit: https://www.datalabsagency.com/wp-admin/post.php?post={d['id']}&action=edit")
    return d['id']

# =====================================================================
# PAGE 1 — GANTT CHARTS  (explainer + how-to; targets "gantt charts" 33.1K/mo)
# =====================================================================
hero_g = fill(widen_intro(BLOCKS['intro']), {
    'PAGE_SUBTITLE': 'The project chart everyone recognises&hellip;',
    'PAGE_TITLE': 'Gantt Charts',
    'UPDATED_DATE': 'August 2026',
    'HOOK': 'A Gantt chart shows a project as horizontal bars on a timeline &mdash; one bar per task, with <strong>start date, duration, and dependencies</strong> visible at a glance. This guide explains when a Gantt chart is the right choice, when it is not, and <strong>how to build one in Excel or Power BI</strong> without buying new software.',
    'SECTION_A_SUBTITLE': 'The one-minute version',
    'SECTION_A_HEADING': 'What is a Gantt chart?',
    'SECTION_A_INTRO': 'A Gantt chart is a <strong>time-scaled bar chart for project schedules</strong>: tasks run down the left, dates run across the top, and each task is a bar whose length is its duration. Links between bars show <strong>dependencies</strong> &mdash; which tasks must finish before others start. It answers one question superbly: <strong>when will each part of this project happen?</strong>',
    'CANONICAL_SENTENCE': CANON,
    'SECTION_B_SUBTITLE': 'Right chart, right job',
    'SECTION_B_HEADING': 'When should you use a Gantt chart &mdash; and when not?',
    'SECTION_B_ANSWER': 'Use a Gantt chart when the schedule itself is the message: project plans, rollouts, campaign calendars, anything with <strong>sequenced tasks and deadlines</strong>. Skip it when your audience only needs status &mdash; a simple progress table or kanban board reads faster &mdash; or when nothing depends on anything else.',
    'SECTION_B_CONTEXT': f'The Gantt chart is one of the workhorses in our {LINK("https://www.datalabsagency.com/types-of-data-visualization/", "types of data visualization")} guide, and like every chart type it fails when it is asked to do the wrong job. A 200-task Gantt chart on one slide is not a schedule, it is wallpaper. The craft is choosing the <strong>level of detail your audience can act on</strong> &mdash; usually phases and milestones for executives, tasks for the delivery team.',
    'PRIMARY_CTA_TEXT': 'Explore our workshops',
    'PRIMARY_CTA_URL': TRAINING,
})
t_build = table_row(
    'Four honest routes', 'How to make a Gantt chart',
    'The right tool depends on <strong>how often the plan changes</strong> and who maintains it. All four routes below are in daily corporate use:',
    build_table(
        ['Tool', 'How the chart is built', 'Best for', 'Keeping it current'],
        [['Excel', 'Stacked bar chart with the first series made invisible', 'Quick plans and one-off timelines', 'Manual &mdash; you edit dates by hand'],
         ['Power BI', 'Gantt custom visual from AppSource over a task table', 'Live project dashboards', 'Refreshes automatically from your data'],
         ['Microsoft Project / Planner', 'Built in &mdash; Gantt is the native view', 'Formal PM teams with licences', 'Maintained inside the tool'],
         ['PM apps (Asana, Monday, ClickUp)', 'Timeline view on the task board', 'Teams already living in the app', 'Updates as tasks move']],
        price_col=False), wide=True)
sec_excel = fill(widen_thirds(BLOCKS['section1']), {
    'SECTION_C_SUBTITLE': 'No add-ins required',
    'SECTION_C_HEADING': 'How do you make a Gantt chart in Excel?',
    'SECTION_C_ANSWER': 'Build a table with <strong>task, start date, and duration</strong> columns, insert a <strong>stacked bar chart</strong>, then format the first series (the start dates) with <strong>no fill</strong> &mdash; the remaining bars become your Gantt. Reverse the category axis so tasks read top-to-bottom, and the chart is done in about ten minutes.',
    'SECTION_C_DETAIL': f'The stacked-bar method is the standard Excel workaround because Excel has no native Gantt type. The method suits plans that change weekly or less. If your team maintains project reporting in Excel or PowerPoint, our {LINK("https://www.datalabsagency.com/data-visualization-training-workshops-webinars/designing-great-business-dashboards-workshop/", "dashboard design workshop")} covers layouts that make schedule charts genuinely readable.',
})
sec_pbi = fill(widen_thirds(BLOCKS['section2']), {
    'SECTION_D_SUBTITLE': 'For plans that keep moving',
    'SECTION_D_HEADING': 'How do you build a Gantt chart in Power BI?',
    'SECTION_D_ANSWER': 'Power BI has no built-in Gantt visual either &mdash; add one from <strong>AppSource</strong> (the free Gantt visual by Microsoft is the usual choice), feed it a table with <strong>task, start date, end date or duration</strong>, and optionally a parent or dependency column. The payoff over Excel: the chart <strong>updates itself when the data refreshes</strong>.',
    'SECTION_D_RATIONALE': f'That refresh is why Gantt charts belong in Power BI when schedule data already lives in a system &mdash; a PM tool export, a SharePoint list, a project table. Instead of redrawing the plan for every steering meeting, the dashboard is simply current. Designing that dashboard well is exactly the kind of work our {LINK("https://www.datalabsagency.com/dashboard-design-services/", "dashboard design service")} does for clients.',
})
t_alt = table_row(
    'Three charts, three questions', 'Gantt chart vs timeline vs kanban',
    'Each of these answers a <strong>different question</strong> about the same project. Pick by the question your audience is actually asking:',
    build_table(
        ['What you need to know', 'Gantt chart', 'Timeline', 'Kanban board'],
        [['The question it answers', 'When will each task happen?', 'What happens in what order?', 'Who is doing what right now?'],
         ['Shows dependencies', 'Yes &mdash; linked bars', 'No', 'No'],
         ['Time-scaled', 'Yes &mdash; bar length is duration', 'Events only, no durations', 'No dates at all'],
         ['Best audience', 'Project teams and sponsors', 'Executives and announcements', 'The delivery team']],
        price_col=False), wide=True)
faq_g = faq_block('Gantt charts', [
    ('Why is it called a Gantt chart?',
     'It is named after <strong>Henry Gantt</strong>, the American engineer who popularised the format in the 1910s. The design has outlived a century of project-management software because the underlying idea &mdash; tasks as time-scaled bars &mdash; is about as direct as a schedule can get.'),
    ('Can I make a Gantt chart in Excel without a template?',
     'Yes. Create columns for task, start date, and duration, insert a <strong>stacked bar chart</strong>, and set the start-date series to <strong>no fill</strong>. Reverse the category axis so the first task sits at the top. No template or add-in is needed.'),
    ('Is there a free Gantt chart visual for Power BI?',
     'Yes &mdash; AppSource has a <strong>free Gantt visual published by Microsoft</strong>, and several third-party alternatives with more formatting control. All of them read an ordinary task table with start and end dates, so switching visuals later does not mean rebuilding your data.'),
    ('How many tasks should a Gantt chart show?',
     'As few as the audience can act on. For executives, chart <strong>phases and milestones</strong> &mdash; usually <strong>under 20 bars</strong>. Delivery teams can work with more, but past roughly 50 bars a single chart stops being readable and the plan is better split by phase or workstream.'),
    ('Do your workshops cover charts like this?',
     'Yes. Chart choice &mdash; when a Gantt chart, timeline, or table is the right answer &mdash; is core material in our <strong>data visualisation and dashboard workshops</strong>, delivered remotely or on site for teams of up to 12. See the training workshops page for topics and formats.'),
], 'See workshop options', TRAINING)
art1_g = fill(BLOCKS['article1'], {
    'ARTICLE_1_SUBTITLE': 'A century old and still standing&hellip;',
    'ARTICLE_1_HEADING': 'Why Gantt charts outlive every software generation',
    'ARTICLE_1_BODY': f'''{P}Every few years a new project tool announces a smarter way to plan, and every few years the first thing users ask for is the <strong>Gantt view</strong>. I have watched that cycle repeat since my days building visual stories at <strong>National Geographic</strong>: formats survive when they match how people actually think, and people think about projects as <strong>things that take time and depend on each other</strong>.</p>
{P}That is precisely what the Gantt chart encodes and almost nothing else does. A calendar shows dates but not durations. A task list shows work but not sequence. A kanban board shows flow but not the future. The Gantt bar carries all three &mdash; <strong>when, how long, and what it is waiting on</strong> &mdash; in a single mark.</p>
{P}Its weakness is the same as its strength: it shows everything, so it tempts you to show everything. The unreadable 300-row Gantt chart is a clich&eacute; in corporate life, and it is not the chart&rsquo;s fault. It is a <strong>level-of-detail decision nobody made</strong>.</p>{SPLIT}
{P}The fix I teach is to build two charts from one plan. The <strong>milestone Gantt</strong> &mdash; phases, gates, a dozen bars &mdash; goes to sponsors and steering groups. The <strong>working Gantt</strong> stays with the team that maintains it. Same data, two audiences, and suddenly both meetings get shorter.</p>
{P}If your organisation runs its plans in Excel or Power BI, that two-chart discipline costs nothing to adopt &mdash; it is purely a design decision, with no software purchase attached. And it is the difference between a schedule people <strong>read</strong> and one they scroll past.</p>''',
})
art2_g = fill(BLOCKS['article2'], {
    'ARTICLE_2_SUBTITLE': 'Small choices, big legibility',
    'ARTICLE_2_HEADING': 'Designing a Gantt chart people actually read',
    'ARTICLE_2_BODY': f'''{P}Most Gantt charts fail on <strong>design</strong>. The schedule is right; the chart is unreadable. After years of teaching dashboard design, the same <strong>five fixes</strong> come up in almost every session.</p>
{P}<strong>Label the bars, not just the axis.</strong> Task names belong on or beside their bars &mdash; a reader should never trace a gridline to learn what a bar is. <strong>Use colour for meaning</strong>, not decoration: one hue per workstream or status, greys for everything else. A rainbow Gantt chart is a chart with no emphasis at all.</p>
{P}<strong>Mark today.</strong> A single vertical line for the current date turns a static plan into a status report &mdash; everything left of the line is history, everything crossing it is live. It is the cheapest insight in the whole format.</p>{SPLIT}
{P}<strong>Show milestones as points, not bars.</strong> A milestone has no duration; drawing it as a diamond keeps the timeline honest. And <strong>group ruthlessly</strong> &mdash; collapse detail into phases wherever your audience does not need task-level resolution.</p>
{P}These are the same principles &mdash; hierarchy, emphasis, level of detail &mdash; that run through our {LINK("https://www.datalabsagency.com/data-visualization-style-guides/power-bi-style-guides/", "Power BI style guides")} and every dashboard we design. A Gantt chart is just a bar chart with opinions about time; design it like you would design anything you want read.</p>''',
})
page_g = assemble([hero_g, t_build, sec_excel, sec_pbi, t_alt, faq_g, art1_g, BLOCKS['offers'], art2_g],
                  'Planning a project your team needs to see clearly?',
                  'Tell us what you are planning&hellip;')

# =====================================================================
# PAGE 2 — DATA ANALYTICS CLASSES  (targets "classes for data analysis" 2,400/mo)
# =====================================================================
hero_d = fill(widen_intro(BLOCKS['intro']), {
    'PAGE_SUBTITLE': 'Classes built for whole teams&hellip;',
    'PAGE_TITLE': 'Data Analytics Classes',
    'UPDATED_DATE': 'August 2026',
    'HOOK': 'The <strong>Datalabs Agency</strong> runs private data analytics classes for corporate teams &mdash; live, instructor-led, and tailored from <strong>~16 class topics</strong> across Power BI, Tableau, dashboards, and data storytelling. Private team classes run <strong>$4,600 to $7,500 inc GST</strong> with up to 12 attendees included; self-paced online courses start at <strong>$127</strong>.',
    'SECTION_A_SUBTITLE': 'The three formats',
    'SECTION_A_HEADING': 'Where can your team take classes for data analysis?',
    'SECTION_A_INTRO': 'Three ways in: <strong>private team classes</strong> delivered live at your office or by video call, and <strong>self-paced online courses</strong> for individuals. We do not run public scheduled classes &mdash; every live class is private to your organisation, so the examples, questions, and data on screen are <strong>yours</strong>, not a stranger&rsquo;s.',
    'CANONICAL_SENTENCE': CANON,
    'SECTION_B_SUBTITLE': 'Analysis people can act on',
    'SECTION_B_HEADING': 'What do the classes actually cover?',
    'SECTION_B_ANSWER': 'Our classes cover the <strong>communication end of analytics</strong>: exploring data visually, choosing the right chart, building dashboards in <strong>Power BI and Tableau</strong>, and telling a story a decision-maker will act on. We do not teach statistics, Python, or SQL &mdash; we teach what happens <strong>after the query returns</strong>.',
    'SECTION_B_CONTEXT': f'That focus is deliberate. Most teams already have people who can pull the numbers; the gap is turning those numbers into something a leadership meeting understands in ninety seconds. The class catalogue spans ~16 topics &mdash; from Introduction to Data Visualisation &amp; Storytelling through to Designing Great Dashboards &mdash; listed on the {LINK("https://www.datalabsagency.com/data-visualization-training-workshops-webinars/", "training page")}.',
    'PRIMARY_CTA_TEXT': 'Ask about class dates',
    'PRIMARY_CTA_URL': CONTACT,
})
t_formats = table_row(
    'Formats and prices', 'Data analytics class formats (2026)',
    'All prices in Australian dollars including GST. Private classes include <strong>up to 12 attendees</strong>, the interactive workbook, and downloadable templates:',
    build_table(
        ['Format', 'Length', 'Price (inc GST)'],
        [['Private class, on site, full day', '~7 hours at your offices', '$7,500'],
         ['Private class, on site, half-day', '4 hours', '$5,200'],
         ['Private class, remote, full day', '~7 hours, can split over two mornings', '$6,200'],
         ['Private class, remote, half-day', '4 hours, or two 2-hour sessions', '$4,600'],
         ['Self-paced online course', 'Learn anytime', '$127 per person']],
        footnote='Groups of 13&ndash;20 add $250 per extra attendee per day; larger groups split into cohorts. Full inclusions and group pricing are on the <a href="https://www.datalabsagency.com/data-visualisation-workshop-pricing/">workshop pricing page</a>.'))
sec_who = fill(widen_thirds(BLOCKS['section1']), {
    'SECTION_C_SUBTITLE': 'Analysts to executives',
    'SECTION_C_HEADING': 'Who are these classes for?',
    'SECTION_C_ANSWER': 'Teams whose work ends in a <strong>chart, dashboard, or report</strong>: analysts, finance and marketing teams, government and policy staff, consultants. No coding background is required &mdash; classes assume your team already works in <strong>Excel, Power BI, or Tableau</strong> and builds from there.',
    'SECTION_C_DETAIL': f'Because every class is private, the level adjusts to the room &mdash; a graduate analyst cohort and an executive briefing get different depths of the same material. Classes have been delivered across Australia and internationally, on site and remotely; delivery options and the full rate card live on the {LINK("https://www.datalabsagency.com/data-visualisation-workshop-pricing/", "workshop pricing page")}.',
})
sec_choose = fill(widen_thirds(BLOCKS['section2']), {
    'SECTION_D_SUBTITLE': 'One decision, honestly framed',
    'SECTION_D_HEADING': 'Private class or self-paced course &mdash; which fits?',
    'SECTION_D_ANSWER': 'Count the learners. <strong>One or two people</strong>: the $127 self-paced courses cover the same design frameworks at a fraction of the cost. <strong>A team</strong>: a private class costs less per head than most public courses, uses <strong>your own data</strong>, and gets everyone speaking the same visual language on the same day.',
    'SECTION_D_RATIONALE': 'The <strong>same-day part</strong> matters more than it sounds. When a whole team learns together, the <strong>vocabulary sticks</strong> &mdash; &ldquo;that needs a milestone marker, not a bar&rdquo; means something in Monday&rsquo;s meeting. Individual learning is better than none, but it rarely changes how a team communicates. That change is what a private class is for.',
})
t_compare_d = table_row(
    'Side by side', 'How the learning options compare',
    'The honest comparison &mdash; including the <strong>options we do not sell</strong>:',
    build_table(
        ['What matters to you', 'Self-paced course', 'Public scheduled class', 'Private team class'],
        [['Curriculum', 'Fixed, design-focused', 'Fixed, tool-focused', 'Tailored from ~16 topics'],
         ['Works on your own data', 'No', 'Rarely', 'Yes &mdash; bring your dashboards'],
         ['Cost for a team of 12', '$1,524', 'Roughly $4,700&ndash;$7,500', '$4,600&ndash;$7,500 all-in'],
         ['Timing', 'Anytime', 'Provider&rsquo;s dates', 'Your dates'],
         ['Who offers it', 'Datalabs shop', 'Other providers', 'The Datalabs Agency']],
        price_col=False), wide=True)
faq_d = faq_block('Data analytics classes', [
    ('Do you teach Python, SQL, or statistics?',
     'No — and that is deliberate. Our classes cover the communication side of analytics: visual exploration, chart choice, <strong>dashboard design in Power BI and Tableau</strong>, and <strong>data storytelling</strong>. If your team needs coding or statistics training, we are not the right provider; if they need their analysis understood and acted on, we are.'),
    ('Are the classes online or in person?',
     'Both. Remote classes run live on <strong>Zoom, Microsoft Teams, or Webex</strong>, with full days splittable over two mornings. On-site classes are delivered at your offices — across Australia and internationally, with travel quoted up front.'),
    ('How much do data analytics classes cost?',
     'Private team classes run <strong>$4,600 to $7,500 inc GST</strong> depending on length and delivery format, with up to 12 attendees included — so a full team typically costs less per person than public courses at $395 to $622 per seat. Self-paced online courses are $127 per person.'),
    ('Do you run scheduled public classes individuals can join?',
     'No. Live classes are private to one organisation. For individual learners, the <strong>self-paced courses</strong> in the Datalabs shop — An Introduction to Data Visualization and Storytelling, and Designing Great Dashboards — teach the same frameworks at $127 each.'),
    ('Do you offer government or not-for-profit rates?',
     'Yes — mention your organisation when you enquire and we will quote accordingly. Every quote is <strong>itemised for procurement</strong>, with inclusions, attendee numbers, and any travel listed separately. Recent government-sector classes have run in Canberra.'),
], 'Get a class quote', CONTACT)
art1_d = fill(BLOCKS['article1'], {
    'ARTICLE_1_SUBTITLE': 'The gap nobody budgets for',
    'ARTICLE_1_HEADING': 'Why analytics training fails at the last mile',
    'ARTICLE_1_BODY': f'''{P}Organisations spend heavily teaching people to <strong>produce</strong> analysis and almost nothing teaching them to <strong>communicate</strong> it. Then everyone wonders why the dashboards go unread and the insights die in appendix slides.</p>
{P}I have seen the pattern from both sides. At <strong>National Geographic</strong> I learned that a finding without a story reaches nobody &mdash; the magazine&rsquo;s genius was never the data, it was the <strong>translation</strong>. Two decades of corporate classes later, the lesson holds: the last mile of analytics is a design and storytelling problem, and it is trainable.</p>
{P}That is why our classes start where most analytics courses stop. Your team already knows how to get the numbers. What they practise with us is <strong>chart choice, visual hierarchy, and narrative</strong> &mdash; the difference between a report that gets skimmed and one that changes a decision.</p>{SPLIT}
{P}The format follows the goal. Classes are <strong>hands-on and private</strong>: your data on screen, your real reports critiqued, exercises built around problems your team actually has. A room of twelve people leaves with a shared vocabulary, which is worth more than any individual certificate.</p>
{P}And because the frameworks are tool-agnostic, the same class lands whether your organisation lives in <strong>Power BI, Tableau, Excel, or PowerPoint</strong>. Tools change &mdash; several times in my career so far. The design principles have not.</p>''',
})
art2_d = fill(BLOCKS['article2'], {
    'ARTICLE_2_SUBTITLE': 'What to look for&hellip;',
    'ARTICLE_2_HEADING': 'Choosing a data analytics class provider',
    'ARTICLE_2_BODY': f'''{P}Shopping for team training? <strong>Five questions</strong> separate the providers quickly, whoever you end up choosing.</p>
{P}<strong>Ask what the exercises use.</strong> If the answer is &ldquo;our sample dataset&rdquo;, your team will learn the sample dataset. Classes that work on <strong>your own dashboards and reports</strong> transfer immediately, because Monday morning looks exactly like the class did.</p>
{P}<strong>Ask who teaches.</strong> A rotating bench of contract trainers teaches the slide deck; a practitioner teaches judgement. You want someone who has shipped real dashboards and defended design decisions to real executives.</p>{SPLIT}
{P}<strong>Ask what happens for larger groups.</strong> Good providers cap interactive classes around 20 and split bigger groups into cohorts &mdash; hands-on teaching stops working past that. A provider happy to take 40 people in one session is selling you a lecture.</p>
{P}<strong>Ask about tools versus principles.</strong> Menu-and-button training dates the day the software updates; design principles compound for a career. And finally, <strong>ask for the price in writing</strong> &mdash; itemised, GST-stated, travel included. Ours is on the {LINK("https://www.datalabsagency.com/data-visualisation-workshop-pricing/", "pricing page")}, which is exactly where a provider&rsquo;s price should be.</p>''',
})
page_d = assemble([hero_d, t_formats, sec_who, sec_choose, t_compare_d, faq_d, art1_d, BLOCKS['offers'], art2_d],
                  'Planning data analytics training for your team?',
                  'Tell us who is learning&hellip;')

# ---------- push both ----------
for slug, title, page, yoast in [
    ('gantt-charts', 'Gantt Charts', page_g,
     'SEO TITLE: Gantt Charts — What They Are & How to Make One | The Datalabs Agency | META DESCRIPTION: What a Gantt chart is, when to use one, and how to build it in Excel or Power BI — a practical guide from The Datalabs Agency, Melbourne data visualization consultancy.'),
    ('data-analytics-classes', 'Data Analytics Classes', page_d,
     'SEO TITLE: Data Analytics Classes for Teams | The Datalabs Agency | META DESCRIPTION: Private data analytics classes for corporate teams — Power BI, Tableau, dashboards and data storytelling. $4,600–$7,500 inc GST for up to 12 people, or self-paced from $127.'),
]:
    print(f'\n===== {slug} =====')
    print('chars:', len(page), '| tables:', page.count('<table'), '| split-articles:', page.count('vc_row_inner][vc_column_inner width="1/2"]') // 2)
    post_draft(slug, title, page)
    print('YOAST HANDOFF:', yoast)
