#!/usr/bin/env python3
"""Compose the Data Visualisation Outsourcing money page from the money-pages design kit.

Target: "data visualisation outsourcing" (72 impr, pos 54.1) + "outsourcing data
visualisation" (72 impr, pos 65.9) -- part of a 1,386-impression cluster mis-served
by the homepage (pos 46.1). Picked via Otto's shortlist reply "1" on the
2026-09-08 "Datalabs money page candidates" email.

Guardrail (from that email, confirmed by next-best-page.py's do_not_target list):
"data visualisation consultancy" (333 impr, pos 7.5) and "data visualisation
consultant" (129 impr, pos 11.1) are already owned by
/product/data-visualization-consultant/ on page 1 -- this page never targets
those exact phrases as a heading; it links OUT to that product page instead.
The page's own angle is the outsourcing DECISION (in-house vs freelancer vs
agency partner), not the consultancy service itself.
"""
import re, base64, urllib.parse, pathlib, json, os, urllib.request

KIT = pathlib.Path('skills/money-pages/references/design-kit.html').read_text()
SCRATCH_OUT = pathlib.Path('/tmp/claude-0/-home-user-project-manager-agent/d273dec6-6806-58f3-85f8-1d076c23404d/scratchpad/composed-data-visualisation-outsourcing.html')
FINAL_OUT = pathlib.Path('skills/money-pages/references/composed/data-visualisation-outsourcing-2026-09-08.html')

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
LINK_CONSULTANT = '<strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/product/data-visualization-consultant/">data visualisation consulting</a></strong>'
LINK_DASHBOARD_SERVICE = '<strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/dashboard-design-services/">dashboard design service</a></strong>'
LINK_WORKSHOPS = '<strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/data-visualization-training-workshops-webinars/">training workshops</a></strong>'
LINK_STYLE_GUIDES = '<strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/data-visualization-style-guides/">data visualisation style guides</a></strong>'
LINK_WORKSHOP_PRICING = '<strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/data-visualisation-workshop-pricing/">workshop pricing</a></strong>'
LINK_CASE_STUDIES = '<strong><a class="dfd-custom-link-decorated" href="https://www.datalabsagency.com/case-studies/">case studies</a></strong>'

# ---------- hero ----------
hero = fill(blocks['intro'], {
    'PAGE_SUBTITLE': "So you&rsquo;re weighing up&hellip;",
    'PAGE_TITLE': 'Data Visualisation Outsourcing',
    'UPDATED_DATE': 'September 2026',
    'HOOK': 'Deciding whether to outsource data visualisation work means choosing between three real paths &mdash; an <strong>in-house hire</strong>, a <strong>freelancer</strong>, and a specialist <strong>agency partner</strong> &mdash; and each one trades cost, control, and quality differently. This page compares all three plainly, including when hiring The <strong>Datalabs Agency</strong> is not the right answer.',
    'SECTION_A_SUBTITLE': 'The short answer, first',
    'SECTION_A_HEADING': 'Should you outsource data visualisation work, or keep it in-house?',
    'SECTION_A_INTRO': 'Outsourcing makes sense when you need dashboard or data-visualisation work at a <strong>level of polish</strong> your team cannot deliver alone, without carrying a <strong>full-time salary</strong> for it. Keeping it in-house makes sense when the work is constant enough to fill a real role. Most teams sit somewhere in between, which is why the comparison below exists.',
    'CANONICAL_SENTENCE': CANON,
    'SECTION_B_SUBTITLE': 'What a specialist agency adds',
    'SECTION_B_HEADING': "What does The Datalabs Agency do that a freelancer or in-house hire can&rsquo;t?",
    'SECTION_B_ANSWER': 'Twelve years of refining <strong>one design process</strong> is what The <strong>Datalabs Agency</strong> brings to this decision, alongside a design language that stays consistent across every deliverable and a team that does not disappear once one project ends. A single freelancer offers none of that consistency by default, and an in-house hire takes months to reach the same standard.',
    'SECTION_B_CONTEXT': 'If you already know you want ongoing help instead of a one-off comparison, our ' + LINK_CONSULTANT + ' runs in fixed one-hour blocks, billed at <strong>$250 per hour inc GST</strong> (up to four hours), so you bring us in for exactly the hours a project needs instead of a permanent seat. For a defined dashboard build with a fixed scope, our ' + LINK_DASHBOARD_SERVICE + ' usually fits better than an open-ended consulting arrangement. And if the real answer for your team is building the skill in-house, our ' + LINK_WORKSHOPS + ' exist for exactly that &mdash; sending your own people home able to do the work themselves, instead of staying dependent on an outside partner at all.',
    'PRIMARY_CTA_TEXT': 'Get an outsourcing quote',
    'PRIMARY_CTA_URL': CONTACT,
})

# Lesson 7/8: page head noun is 3 words ("Data Visualisation Outsourcing") -- widen the
# hero row 1/3+1/3+1/3 -> 1/4+1/2+1/4 (offsets too, since the hero columns carry them).
EMPTY_COL_13 = '[vc_column_inner el_class="dfd_col-tablet-12" width="1/3" offset="vc_col-lg-4 vc_col-md-2 vc_col-xs-1"][/vc_column_inner]'
EMPTY_COL_14 = '[vc_column_inner el_class="dfd_col-tablet-12" width="1/4" offset="vc_col-lg-3 vc_col-md-2 vc_col-xs-1"][/vc_column_inner]'
MID_COL_13_OPEN = '[vc_column_inner el_class="dfd_col-tablet-12" width="1/3" dfd_column_responsive_enable="dfd-column-responsive-enable" offset="vc_col-lg-4 vc_col-md-8 vc_col-xs-10"'
MID_COL_12_OPEN = '[vc_column_inner el_class="dfd_col-tablet-12" width="1/2" dfd_column_responsive_enable="dfd-column-responsive-enable" offset="vc_col-lg-6 vc_col-md-8 vc_col-xs-10"'
assert hero.count(EMPTY_COL_13) == 2 and MID_COL_13_OPEN in hero, 'hero column markup shape changed'
hero = hero.replace(EMPTY_COL_13, EMPTY_COL_14).replace(MID_COL_13_OPEN, MID_COL_12_OPEN)

# ---------- table: in-house vs freelancer vs Datalabs (comparison exemplar only --
# no outsourcing-specific rate card exists for in-house salaries or freelance day
# rates, so those cells describe behaviour rather than inventing a number; the
# Datalabs column uses only the published $250/hr consulting rate) ----------
CTH = "style=\"padding: 8px 14px; text-align: left; background-color: #000000 !important; border: none !important; border-bottom: 2px solid #c39f76 !important; font-family: 'Bebas Neue', sans-serif; font-size: 19px; font-weight: normal; letter-spacing: 1px; color: #ffffff !important;\""
CTHREC = CTH.replace('background-color: #000000 !important', 'background-color: #c39f76 !important').replace('color: #ffffff !important', 'color: #000000 !important')
def ctd(bg, align='left', color='#ffffff', bold=False):
    s = f'padding: 8px 14px; font-size: 15px; text-align: {align}; background-color: {bg} !important; border: none !important; border-bottom: 1px solid #2f2e3a !important; color: {color} !important;'
    if bold: s += ' font-weight: bold;'
    return f'style="{s}"'

rows = [
    ('How you pay', 'Ongoing salary and benefits', 'Per-project or hourly invoice', 'Fixed quote, or $250/hr consulting blocks'),
    ('Ramp-up time', 'Weeks to months to hire and onboard', 'Days, once you find the right person', 'Starts once the brief is agreed'),
    ('Design consistency', "Depends on one person's training", 'Resets with every new freelancer', 'Same design language on every project since 2012'),
    ('Backup if someone is unavailable', 'None, unless a second person is hired', 'None', 'A team, not one person'),
    ('Best for', 'Constant, ongoing dashboard or reporting work', 'A single small job, low stakes', 'Project-shaped work that needs agency-level polish'),
]
fmt_rows = []
for r, (crit, inhouse, free, ours) in enumerate(rows):
    cells = f'<td {ctd("#000000", bold=True)}>{crit}</td>'
    for val, bg in [(inhouse, '#000000'), (free, '#000000'), (ours, '#111111')]:
        cells += f'<td {ctd(bg)}>{val}</td>'
    fmt_rows.append('<tr>' + cells + '</tr>')
fmt_table = ('<div style="overflow-x: auto;">\n<table style="width: 100%; border-collapse: collapse !important; background-color: #000000 !important; border: none !important;">\n<thead>\n<tr>'
    + f'<th scope="col" {CTH}>&nbsp;</th><th scope="col" {CTH}>In-house hire</th><th scope="col" {CTH}>Freelancer</th><th scope="col" {CTHREC}>Datalabs Agency partner</th>'
    + '</tr>\n</thead>\n<tbody>\n' + '\n'.join(fmt_rows) + '\n</tbody>\n</table>\n</div>'
    + '\n<p style="text-align: left; font-size: 13px; font-style: italic; color: #8a8a95; margin-top: 10px;">The in-house and freelancer columns describe general behaviour for each path; specifics vary by the individual hire or freelancer. The $250/hr rate is inc GST, billed in one-hour blocks up to four hours.</p>')

def table_row(subtitle, heading, intro, table_html):
    block = fill(blocks['table'], {'TABLE_SUBTITLE': subtitle, 'TABLE_HEADING': heading})
    m = re.search(r'(\[vc_column_text css=""\]\n).*?(\n\[/vc_column_text\])', block, flags=re.S)
    guts = f'<p style="text-align: center;"><strong>{intro}</strong></p>\n\n{table_html}'
    return block[:m.start(1) + len(m.group(1))] + guts + block[m.end(2) - len(m.group(2)):]

t_compare = table_row(
    'Compare your options', 'In-house hire, freelancer, or an agency partner &mdash; which fits your workload?',
    'Here is how the three common paths for data visualisation work actually differ, criterion by criterion.',
    fmt_table)
# Lesson 1/9: 4 columns overflow the kit's default 1/3 table row -- widen to 1/6+2/3+1/6.
t_compare = t_compare.replace(
    '[vc_row_inner][vc_column_inner width="1/3"][/vc_column_inner][vc_column_inner width="1/3"][dfd_heading enable_delimiter="" style="style_02" heading_margin="margin-bottom:20px;" subtitle="Compare your options"',
    '[vc_row_inner][vc_column_inner width="1/6"][/vc_column_inner][vc_column_inner width="2/3"][dfd_heading enable_delimiter="" style="style_02" heading_margin="margin-bottom:20px;" subtitle="Compare your options"'
).replace(
    '[/vc_column_text][dfd_spacer screen_wide_resolution="1280" screen_wide_spacer_size="20" screen_normal_resolution="1024" screen_tablet_resolution="800" screen_mobile_resolution="480" screen_normal_spacer_size="20" screen_tablet_spacer_size="20" screen_mobile_spacer_size="20"][/vc_column_inner][vc_column_inner width="1/3"][/vc_column_inner][/vc_row_inner][/vc_column][vc_column][dfd_spacer',
    '[/vc_column_text][dfd_spacer screen_wide_resolution="1280" screen_wide_spacer_size="20" screen_normal_resolution="1024" screen_tablet_resolution="800" screen_mobile_resolution="480" screen_normal_spacer_size="20" screen_tablet_spacer_size="20" screen_mobile_spacer_size="20"][/vc_column_inner][vc_column_inner width="1/6"][/vc_column_inner][/vc_row_inner][/vc_column][vc_column][dfd_spacer',
    1
)
assert '1/6' in t_compare and t_compare.count('width="1/6"') >= 2, 'table row widening did not apply'

# ---------- sections ----------
def widen_section_row(block, label):
    n = block.count('[vc_column_inner width="1/3"]')
    assert n == 3, f'{label}: expected 3 x 1/3 inner columns, found {n}'
    parts = block.split('[vc_column_inner width="1/3"]')
    return '[vc_column_inner width="1/4"]'.join(parts[:2]) + '[vc_column_inner width="1/2"]' + '[vc_column_inner width="1/4"]'.join(parts[2:])

sec_c = fill(blocks['section1'], {
    'SECTION_C_SUBTITLE': 'When the maths favours us',
    'SECTION_C_HEADING': 'When does outsourcing data visualisation work make sense?',
    'SECTION_C_ANSWER': 'Outsourcing usually wins when the work is <strong>project-shaped</strong> rather than constant &mdash; a report, a dashboard rebuild, a one-off style guide &mdash; and you need a result that looks considered from day one instead of after a new hire&rsquo;s first few attempts.',
    'SECTION_C_DETAIL': 'That is exactly the shape of our own ' + LINK_DASHBOARD_SERVICE + ' &mdash; a fixed project with a fixed quote, not an ongoing role on your payroll. It also suits a team that already has someone doing this work but needs a second set of hands for one busy quarter.',
})
sec_c = widen_section_row(sec_c, 'section1')

sec_d = fill(blocks['section2'], {
    'SECTION_D_SUBTITLE': "When it doesn't",
    'SECTION_D_HEADING': 'When does an in-house hire make more sense?',
    'SECTION_D_ANSWER': 'If dashboard or reporting work lands on your desk <strong>every week</strong> rather than every quarter, a full-time hire usually costs less over a year than repeated outside engagements, and builds context about your business that no outside partner can shortcut.',
    'SECTION_D_RATIONALE': 'A specialist agency is not the right fit for constant, day-to-day reporting work inside one team &mdash; that is exactly when an in-house hire pays for itself. Where an outside partner still adds value even then is the parts that benefit from a fresh eye once: a style guide, an initial <strong>workshop</strong> to set the design standards, or a dashboard rebuild your own team can maintain afterward.',
})
sec_d = widen_section_row(sec_d, 'section2')

# ---------- FAQ ----------
faq_pairs = [
    ('Should I outsource data visualisation work, or hire someone in-house?',
     'It depends on how constant the work is. Outsourcing suits project-shaped work &mdash; a dashboard build, a style guide, a one-off report &mdash; where you need a result quickly without adding headcount. An in-house hire suits teams with enough steady dashboard or reporting work to fill a real role, week after week.'),
    ('How much does it cost to outsource dashboard or data visualisation work?',
     'There is no single outsourcing rate card, because every brief differs in scope. The two published reference points are our <strong>$250 per hour</strong> data visualisation consulting rate (inc GST, one-hour blocks up to four hours) and our <strong>$3,000&ndash;$8,000 per workshop day</strong> range for a facilitated session; a dashboard or report project is quoted once we understand the brief.'),
    ("What's the difference between hiring a freelancer and an agency like Datalabs?",
     'A freelancer is one person, with one set of availability and one style; when they are busy or unavailable, the project waits. Continuity is different at The Datalabs Agency, where a design process built up since 2012 means the work does not depend on a single person&rsquo;s calendar.'),
    ('Can The Datalabs Agency work alongside our in-house team?',
     'Yes. Many clients keep an in-house team for day-to-day reporting and bring us in for the parts that benefit from an outside eye &mdash; a style guide, an initial workshop to set the design standards, or a dashboard rebuild the in-house team then maintains.'),
    ('How do we get started?',
     'Send us your project, team size, and rough timing through the contact form on this site, and we will reply with a fixed quote or, for ongoing help, availability for consulting blocks. There is no obligation to commit before you see a price.'),
    ('Do you offer ongoing outsourced support, or only one-off projects?',
     'Both. One-off dashboard, style guide, and report projects are quoted per project; ongoing help runs as <strong>$250-per-hour</strong> consulting blocks (inc GST, up to four hours at a time), so you can keep an outside specialist on call without a full-time hire.'),
]
faq_map = {'FAQ_TOPIC': 'Data visualisation outsourcing', 'FAQ_CTA_TEXT': 'Get an outsourcing quote', 'FAQ_CTA_URL': CONTACT}
for i, (q, a) in enumerate(faq_pairs[:5], 1):
    faq_map[f'FAQ_Q{i}'] = q
    faq_map[f'FAQ_A{i}'] = a
faq = fill(blocks['faq'], faq_map)
q6, a6 = faq_pairs[5]
sec6 = f'[vc_tta_section title="{q6}" tab_id="1788600000001-outsourcing-ongoing-6q"][vc_column_text css=""]\n<p style="text-align: center;">{a6}</p>\n[/vc_column_text][/vc_tta_section]'
faq = faq.replace('[/dfd_accordion]', sec6 + '[/dfd_accordion]')

def plain(s):
    s = re.sub(r'<[^>]+>', '', s)
    for ent, ch in [('&mdash;', '—'), ('&ndash;', '–'), ('&amp;', '&'), ('&rsquo;', '’'), ('&times;', 'x')]:
        s = s.replace(ent, ch)
    return s
entities = [{"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in faq_pairs]
for e in entities:
    assert '<' not in e['name'] and '<' not in e['acceptedAnswer']['text'], 'markup leaked into FAQPage JSON-LD'
schema = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}, ensure_ascii=False) + '</script>'
enc = base64.b64encode(urllib.parse.quote(schema, safe='').encode()).decode()
faq = re.sub(r'\[vc_raw_html\][^\[]*\[/vc_raw_html\]', '[vc_raw_html]' + enc + '[/vc_raw_html]', faq)

# ---------- articles (both kept at 4 paragraphs -- at, not past, the lesson-10
# two-column threshold -- single column, same call as the Microsite Design page) ----------
P = '<p style="line-height: 22px; text-align: left;">'
art1_paras = [
    f'{P}I get asked some version of this question every month: should a company hire someone, hire a freelancer, or bring in The <strong>Datalabs Agency</strong>? Outsourcing is not free of trade-offs just because it is common. You give up some day-to-day control, and you give up the accumulated context an in-house person builds after a year on your team.</p>',
    f'{P}In exchange, you get a team that has already made most of its mistakes on someone else&rsquo;s project. I founded <strong>The Datalabs Agency</strong> in 2012, and the design process behind every dashboard, style guide, and workshop we deliver has been tested on clients including <strong>Mercedes-Benz</strong>, <strong>Adidas</strong>, and <strong>UPS</strong>. A freelancer starting a new engagement, or a new in-house hire in their first quarter, has not had that many chances to fail safely yet.</p>',
    f'{P}The trade-off changes shape depending on what you are outsourcing. Handing over one dashboard is low-risk either way &mdash; worst case, you pay again for a second attempt. Handing over your team&rsquo;s entire reporting standard is different: a <strong>BI style guide</strong> set by an outside partner has to survive years of use by people who were not in the room when it was designed. That is where our {LINK_STYLE_GUIDES} work spends most of its effort &mdash; a system built to hold up years after the handover meeting, not just impress in it.</p>',
    f'{P}None of this means outsourcing is always the answer. If I think a client would be better served by hiring someone <strong>permanent</strong>, I say so &mdash; the FAQ above spells out when an <strong>in-house hire</strong> wins. What I will not do is sell a <strong>one-off engagement</strong> as a substitute for a role that clearly needs to exist inside a company, because that model breaks down as soon as the next dashboard change comes through and nobody in the building knows why the last one looks the way it does.</p>',
]
art1 = fill(blocks['article1'], {
    'ARTICLE_1_SUBTITLE': "Here&rsquo;s what you actually give up&hellip;",
    'ARTICLE_1_HEADING': 'What do you actually give up when you outsource this work?',
    'ARTICLE_1_BODY': '\n'.join(art1_paras),
})

art2_paras = [
    f'{P}Every outsourcing conversation starts the same way for me: what does the client actually need built, and <strong>how often</strong> will they need it again? A dashboard that gets rebuilt <strong>once a year</strong> is a different conversation from one that changes <strong>every sprint</strong>. I ask this before I talk about price, because the answer decides which of the <strong>three paths</strong> in the comparison above actually fits.</p>',
    f'{P}When a <strong>freelancer</strong> is actually the better fit for a <strong>small one-off job</strong>, I say so &mdash; a single branded chart for one presentation does not need a <strong>twelve-year-old design process</strong> behind it.</p>',
    f'{P}When the answer is an <strong>in-house hire</strong>, I say that too. A company running dashboard requests through my inbox <strong>every single week</strong> would save money within a year by hiring someone permanent, and I would rather tell a prospective client that up front than keep invoicing <strong>consulting hours</strong> that no longer make sense for their situation.</p>',
    f'{P}What I actually get asked to do most often sits in the middle: a team that already has someone covering day-to-day reporting, who needs a specialist for one dashboard rebuild, one <strong>BI style guide</strong>, or one round of team <strong>training</strong> a year. See our {LINK_WORKSHOP_PRICING} page if that last one is the piece you are missing, and our {LINK_CASE_STUDIES} for what that has looked like for clients like <strong>Mercedes-Benz</strong> and <strong>Adidas</strong>.</p>',
]
art2 = fill(blocks['article2'], {
    'ARTICLE_2_SUBTITLE': "From the client&rsquo;s side of the table",
    'ARTICLE_2_HEADING': "How I decide what to recommend, even when it isn't us",
    'ARTICLE_2_BODY': '\n'.join(art2_paras),
})

# ---------- enquiry-form footer (Lesson 12): rewrite heading + subtitle to this page's topic ----------
fixed = blocks['fixed']
fixed = fixed.replace(
    '[dfd_heading delimiter_settings="border-bottom-style:solid;|border-bottom-width:1px;|width:50px;|border-bottom-color:#dddddd;" style="style_02" subtitle="Professional &amp; Thought-provoking" title_font_options="tag:h2" subtitle_font_options="tag:h3"]Looking for a speaker for your event?[/dfd_heading]',
    '[dfd_heading delimiter_settings="border-bottom-style:solid;|border-bottom-width:1px;|width:50px;|border-bottom-color:#dddddd;" style="style_02" subtitle="Tell us what you are trying to solve&hellip;" title_font_options="tag:h2" subtitle_font_options="tag:h3"]Not sure whether to outsource, hire, or do both?[/dfd_heading]'
)
assert fixed != blocks['fixed'], 'enquiry-form footer swap did not match'

# ---------- assemble, strip comments ----------
page = '\n'.join([hero, sec_c, sec_d, t_compare, faq, art1, blocks['offers'], art2, fixed])
page = re.sub(r'<!--(?! YOAST).*?-->\n?', '', page, flags=re.S).strip()

YOAST_TITLE = 'Data Visualisation Outsourcing | The Datalabs Agency'
YOAST_META = "Weighing up outsourcing data visualisation work? Compare in-house hire, freelancer, and The Datalabs Agency's $250/hr consulting or fixed-quote projects."
assert len(YOAST_TITLE) <= 60, f'Yoast title too long: {len(YOAST_TITLE)}'
assert len(YOAST_META) <= 155, f'Yoast meta too long: {len(YOAST_META)}'
yoast = f'<!-- YOAST SEO TITLE: {YOAST_TITLE} | META DESCRIPTION: {YOAST_META} -->'
print('\nSET THESE IN WP-ADMIN (Yoast):\n ' + yoast.strip())
print(f'(title {len(YOAST_TITLE)} chars, meta {len(YOAST_META)} chars)')

leftover = re.findall(r'\{\{[A-Z0-9_]+', page)
assert not leftover, 'unfilled tokens: ' + str(set(leftover))
SCRATCH_OUT.parent.mkdir(parents=True, exist_ok=True)
SCRATCH_OUT.write_text(page)
FINAL_OUT.parent.mkdir(parents=True, exist_ok=True)
FINAL_OUT.write_text(page)
print('composed chars:', len(page), '| tables:', page.count('<table'), '| tokens left: 0')
print('written to:', SCRATCH_OUT, 'and', FINAL_OUT)
