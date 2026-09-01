#!/usr/bin/env python3
"""Compose the ZIM Visual Case Study — 1 Sep 2026, Otto's commission.

Content sources: Proposals/ZIM/Proposal-Quote-ZIM-DatalabsAgency.pdf (29 Jan 2026,
quote QU-0348 dated 26 Jan 2026) + Client Projects/ZIM assets + the Gmail record
(Feb-Mar 2026 delivery; Teams invites; ZIM L&D's own key-takeaways email 26 Mar 2026).
FACTS: ZIM Integrated Shipping Services Ltd, Haifa, Israel — global container line.
Scope: two one-hour open lectures ("Data Accessibility and Understandability through
Storytelling", open to all ZIM analysts, designed for audiences of up to 140 — one for
Hong Kong & Israel, one for the Americas) + three four-hour workshops (Intro to Data
Viz & Storytelling / Creative Data Presentations with PowerPoint / Infographics &
Report Design), up to 20 analysts each, each run as two two-hour sessions per cohort.
Delivered live on Microsoft Teams from Melbourne, Feb-Mar 2026; cohorts spanned
Israel, Hong Kong, the US, and Brazil (session titles: "USA & Brazil"). Tailoring:
deck built to ZIM's own brand guidelines (client provided access); custom lightweight
workbook with exercises + a dummy dataset; circle-exercise sheets. Aftercare: slide
packs, per-cohort summary packs, session recordings. OUTCOME EVIDENCE: ZIM's L&D team
circulated its own key-takeaways email restating the method (three-act structure,
six-question filter, micro-stories, five pillars, thinking in arrays, plot patterns)
— PARAPHRASED on page, never quoted; no client staff named; fee NOT published
($16,625 AUD documented if Otto wants it). "Up to 140" stays capacity language.
Media: 54112 workshop title (hero), 54115 lecture title, 54118 micro-stories,
54121 macro-stories, 54124 story design process, 54127 teaching dashboard (hotspot).
Tint: deep indigo #201c2c (ZIM purple family, Otto's near-black-with-a-tinge rule).
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from vcs_lib import *

blocks = kit_blocks()
OUT = '/private/tmp/claude-501/-Users-Ottinger-Claude-Projects-2026-project-manager-agent/1250d283-1a10-4416-b992-be81f96ce7a2/scratchpad/composed-zim.html'

hero = widen_hero(fill(blocks['intro'], {
    'PAGE_SUBTITLE': 'A visual case study&hellip;',
    'PAGE_TITLE': 'ZIM: One Method, Four Time Zones',
    'UPDATED_DATE': 'September 2026',
    'HOOK': 'In early 2026, <strong>ZIM Integrated Shipping Services</strong> &mdash; the Israeli global container line &mdash; wanted its analysts telling better data stories. Datalabs delivered a <strong>lecture-and-workshop program</strong> across Israel, Hong Kong, and the Americas: two open lectures to light the fuse, <strong>three hands-on workshops</strong> to do the training, all live from Melbourne.',
    'SECTION_A_SUBTITLE': 'The program in one paragraph',
    'SECTION_A_HEADING': 'What did the Datalabs Agency deliver for ZIM?',
    'SECTION_A_INTRO': 'Across February and March 2026, the <strong>Datalabs Agency</strong> ran a data storytelling program for ZIM&rsquo;s analysts: <strong>two one-hour open lectures</strong> on data accessibility and storytelling &mdash; one for the Hong Kong and Israel offices, one for the Americas &mdash; and <strong>three four-hour workshops</strong> (data visualisation and storytelling, creative data presentations with PowerPoint, and infographics and report design), each capped at 20 analysts and run as two two-hour sessions per cohort.',
    'CANONICAL_SENTENCE': CANONICAL,
    'SECTION_B_SUBTITLE': 'The problem behind the brief',
    'SECTION_B_HEADING': 'Why does a shipping line train analysts in storytelling?',
    'SECTION_B_ANSWER': 'The animation above is the program&rsquo;s shape. The brief behind it, from ZIM&rsquo;s <strong>Learning &amp; Development team</strong>: analysts across the fleet of offices had deep data and solid tooling, and the gap was <strong>accessibility and understandability</strong> &mdash; getting what the analysis means across to the business, in reports people actually read.',
    'SECTION_B_CONTEXT': 'A global analyst community makes that a design problem twice over. The training had to land in <strong>Jerusalem, Hong Kong, and Americas working hours</strong> without diluting into a webinar, and it had to give analysts in different regions <strong>one shared method</strong> &mdash; so a report drafted in Haifa reads the same way in Norfolk or Hong Kong. The funnel design answered both: broad lectures open to every analyst, then small hands-on workshops for the people who build the reports.',
    'PRIMARY_CTA_TEXT': 'Plan a program like this',
    'PRIMARY_CTA_URL': CONTACT,
}))
hero_p1, row_secB = split_hero(hero, 54112)

# ---------- Row: Animated Flow Diagram — the lecture-to-workshop funnel ----------
def svg_funnel():
    lectures = [('OPEN LECTURE ONE', 'Hong Kong &amp; Israel &mdash; every analyst invited'),
                ('OPEN LECTURE TWO', 'The Americas &mdash; every analyst invited')]
    workshops = [('DATA VIZ &amp; STORYTELLING', 'Two 2-hour sessions, up to 20 analysts'),
                 ('CREATIVE DATA PRESENTATIONS', 'PowerPoint &mdash; same format, same cap'),
                 ('INFOGRAPHICS &amp; REPORTS', 'Design fundamentals for reporting')]
    parts = [f'<svg viewBox="0 0 1200 640" xmlns="http://www.w3.org/2000/svg" role="img" '
             f'aria-label="Two open ZIM lectures for audiences of up to 140 analysts funnel into three hands-on workshops of up to 20" '
             f'style="width:100%;height:auto;display:block;">']
    ys_l = [130, 400]
    for (name, sub), y in zip(lectures, ys_l):
        parts.append(f'<rect x="40" y="{y}" width="300" height="110" rx="10" fill="#262532" stroke="#4a4860" stroke-width="1.5"/>')
        parts.append(f'<text x="64" y="{y+40}" font-family="{BEBAS}" font-size="25" letter-spacing="1.5" fill="#ffffff">{name}</text>')
        parts.append(f'<text x="64" y="{y+66}" font-family="{ARVO}" font-size="12" fill="#8a8a95">{sub}</text>')
        parts.append(f'<text x="64" y="{y+90}" font-family="{ARVO}" font-size="12" fill="#c39f76">one hour, audiences up to 140</text>')
        parts.append(flow_line(340, y + 55, 494, 320, cx1=420))
    parts.append(f'<circle cx="600" cy="320" r="108" fill="#1f1e29" stroke="{TAN}" stroke-width="2.5"/>')
    parts.append(f'<circle cx="600" cy="320" r="122" fill="none" stroke="{TAN}" stroke-width="1" opacity="0.35" stroke-dasharray="3 7"/>')
    parts.append(f'<text x="600" y="300" text-anchor="middle" font-family="{BEBAS}" font-size="34" letter-spacing="1" fill="{TAN}">140 &#8594; 20</text>')
    parts.append(f'<text x="600" y="330" text-anchor="middle" font-family="{ARVO}" font-size="14" fill="#ffffff">inspire wide, train deep</text>')
    parts.append(f'<text x="600" y="352" text-anchor="middle" font-family="{ARVO}" font-size="12" fill="#8a8a95">live from Melbourne, on Teams</text>')
    ys_w = [80, 265, 450]
    for j, ((name, sub), y) in enumerate(zip(workshops, ys_w)):
        parts.append(flow_line(708, 320, 870, y + 55, cx1=790))
        parts.append(f'<rect x="870" y="{y}" width="290" height="110" rx="10" fill="#262532" stroke="{TAN}" stroke-width="1.5"/>')
        parts.append(f'<text x="892" y="{y+36}" font-family="{BEBAS}" font-size="21" letter-spacing="1" fill="#ffffff">{name}</text>')
        parts.append(f'<text x="892" y="{y+60}" font-family="{ARVO}" font-size="12" fill="#c39f76">{sub}</text>')
        # mini bars — stepping highlight with pulse
        for i, h in enumerate([16, 26, 20, 30, 24]):
            bx = 892 + i * 26
            if i == j:
                parts.append(f'<rect x="{bx}" y="{y+96-h}" width="16" height="{h}" rx="2" fill="{TAN}">'
                             f'<animate attributeName="opacity" values="1;0.5;1" dur="2s" repeatCount="indefinite"/></rect>')
            else:
                parts.append(f'<rect x="{bx}" y="{y+96-h}" width="16" height="{h}" rx="2" fill="#4a4860"/>')
    parts.append('</svg>')
    return ''.join(parts)

row_flow = svg_row('Watch the funnel work', 'Two lectures in, three workshops out',
    'The program&rsquo;s shape: open lectures for <strong>audiences of up to 140 analysts</strong> on the left, and the <strong>hands-on workshops of 20</strong> they feed on the right.',
    svg_funnel())

# ---------- schedule table ----------
t_shape = table_row(blocks, 'Five deliveries, one method', 'The program, piece by piece',
    'The delivery schedule, from the program&rsquo;s own planning documents.',
    ['Delivery', 'Cohort', 'Format'],
    [['Open lecture', 'Hong Kong &amp; Israel', 'One hour, all analysts invited'],
     ['Open lecture', 'The Americas', 'One hour, all analysts invited'],
     ['Data Viz &amp; Storytelling workshop', 'Regional cohorts', 'Four hours as two 2-hour sessions, up to 20'],
     ['Creative Data Presentations workshop', 'Regional cohorts', 'Four hours as two 2-hour sessions, up to 20'],
     ['Infographics &amp; Report Design workshop', 'Regional cohorts', 'Four hours as two 2-hour sessions, up to 20']],
    footnote='All sessions ran live on Microsoft Teams from Melbourne across February and March 2026, placed in Jerusalem, Hong Kong, and Americas working hours &mdash; cohorts spanned Israel, Hong Kong, the United States, and Brazil.')

# ---------- gallery ----------
row_gallery = gallery_row('The teaching assets, full size', 'Inside the workshop materials',
    'Click any asset to view it full-screen &mdash; chapters and process frames from the <strong>ZIM-branded decks</strong>.',
    [(54118, 'Micro-Stories', 'Finding the small stories in big data'),
     (54121, 'Macro-Stories', 'Zooming back out to the big picture'),
     (54124, 'The Story Design Process', 'Seven steps, audience first'),
     (54115, 'The Open Lecture', 'Where the program began')])

# ---------- hotspot: the teaching dashboard ----------
row_hotspot = hotspot_row('Click the markers', 'Read the teaching dashboard',
    'Workshop cohorts practised on this <strong>teaching dashboard</strong>, built on dummy portfolio data. Five markers explain how it reads.',
    54127, [
        (12, 8, 'The KPI band', 'Four headline numbers - budget, actual spend, forecast, average completion - the read-first row every dashboard needs.'),
        (25, 38, 'Budget vs actual', 'The core comparison, one bar per project - where the money went against where it was planned to go.'),
        (72, 32, 'The completion tracker', 'Project-by-project progress with status flags, so the laggards surface without hunting.'),
        (78, 75, 'Anomalies and signals', 'Written callouts naming what the numbers mean - flat forecasts, spend risks, odd completions - the storytelling layer.'),
        (25, 80, 'Risk vs completion', 'A scatter placing every project by risk and progress, the 360-degree view of the same portfolio.'),
    ])

# ---------- Row: Design Principle Tiles — the method the client wrote back ----------
row_tiles = svg_row('The method that stuck', 'Six ideas the analysts took home',
    'Six devices from the curriculum &mdash; the ones ZIM&rsquo;s own L&amp;D team later summarised back to attendees in its wrap-up.',
    svg_tiles('Six data storytelling devices taught in the ZIM program', [
        ('THE THREE-ACT STRUCTURE', 'Context, insight, then the call to action', 'doc'),
        ('THE SIX-QUESTION FILTER', 'Scope, context, insight, plot, motive, ask', 'target'),
        ('MICRO-STORIES', 'Segments, outliers, and gaps carry the plot', 'charts'),
        ('THE FIVE PILLARS', 'Charts, icons, diagrams, type, photography', 'layers'),
        ('THINKING IN ARRAYS', 'Sketch many options before choosing one', 'grid'),
        ('PLOT PATTERNS', 'Linear, reverse-engineered, or 360-degree', 'hierarchy'),
    ]))

# ---------- deliverables ----------
sec_deliver = widen_inner(fill(blocks['section2'], {
    'SECTION_D_SUBTITLE': 'Delivered, documented, taught',
    'SECTION_D_HEADING': 'What did ZIM receive at the end?',
    'SECTION_D_ANSWER': 'ZIM received the five live deliveries, decks designed to <strong>ZIM&rsquo;s own brand guidelines</strong>, a custom <strong>workbook with exercises and a dummy dataset</strong>, and a full aftercare layer: curated <strong>slide packs</strong>, per-cohort summary packs, and session recordings for attendees to revisit.',
    'SECTION_D_RATIONALE': 'The outcome that matters most arrived a few weeks later, unprompted: ZIM&rsquo;s Learning &amp; Development team circulated its <strong>own written summary of the method</strong> to attendees &mdash; the three-act structure, the six-question filter, micro-stories, the five pillars &mdash; in the team&rsquo;s own words. When the client can teach the material back, the <strong>shared language</strong> has landed &mdash; and a shared language is what separates training from consulting.',
}), '1/4', '1/2')

row_quote = quote_row('Otto Ottinger', 'The principle behind the ZIM curriculum',
    'Don&rsquo;t just show the data &mdash; show what it means. The analyst&rsquo;s job is the route and the destination, never just the map.')

row_faq = faq_row(blocks, 'The ZIM program', 'Ask about your analyst program', [
    ('What did the Datalabs Agency deliver for ZIM?',
     'A data storytelling program for the analysts of <strong>ZIM Integrated Shipping Services</strong>, the Israeli global container line, across February and March 2026: two one-hour open lectures &mdash; one for the Hong Kong and Israel offices, one for the Americas &mdash; and <strong>three four-hour workshops</strong> covering data visualisation and storytelling, creative data presentations with PowerPoint, and infographics and report design.'),
    ('How was the program delivered across so many time zones?',
     'Live on <strong>Microsoft Teams from Melbourne</strong>, with every session placed inside the cohort&rsquo;s own working hours &mdash; morning in Jerusalem, afternoon in Hong Kong, morning in the Americas. Each workshop ran as <strong>two two-hour sessions</strong>, which keeps a virtual room hands-on and lets a global schedule breathe.'),
    ('What made the training ZIM-specific?',
     'The decks were designed to <strong>ZIM&rsquo;s own brand guidelines</strong>, which the client provided at the start, and attendees worked from a custom <strong>workbook with exercises and a dummy dataset</strong> built for the program &mdash; so the practice looked and felt like the reports analysts actually produce.'),
    ('Who attended?',
     'The lectures were open to analysts across ZIM&rsquo;s offices, designed for <strong>audiences of up to 140</strong>; the workshops were capped at <strong>20 analysts</strong> so the exercises stayed personal. Cohorts spanned Israel, Hong Kong, the United States, and Brazil.'),
    ('Can the Datalabs Agency run this program for my analysts?',
     'Yes. The funnel shape &mdash; an <strong>open lecture to inspire broadly</strong>, then small hands-on workshops for the practitioners &mdash; is a repeatable format, and the time-zone scheduling scales to wherever your analysts sit. Send your team shape through the contact form and we will reply with a program outline.'),
])

# ---------- articles ----------
art1 = fill(blocks['article1'], {
    'ARTICLE_1_SUBTITLE': 'Small stories, big picture',
    'ARTICLE_1_HEADING': 'Micro-stories and macro-stories',
    'ARTICLE_1_BODY': f'''{P}The centre of the ZIM curriculum is a pairing. A <strong>micro-story</strong> is the small, sharp narrative hiding inside a big dataset &mdash; a segment behaving oddly, an outlier worth naming, the <strong>most profitable</strong> or <strong>least reliable</strong> of anything, a gap where numbers should be. Analysts learn to hunt these deliberately: cohorts, superlatives, overlaps.</p>
{P}The <strong>macro-story</strong> is the discipline that stops micro-stories becoming trivia. Once the small narratives are on the table, the analyst zooms back out: what do these add up to, and what should the business do about it? The workshops drilled the <strong>three-act structure</strong> for exactly this &mdash; context, insight, call to action &mdash; so a report ends with a recommendation, never a shrug.</p>
{P}Between the two sits craft. The <strong>six-question filter</strong> forces scope, context, insight, plot, motivation, and ask to be settled before any software opens; <strong>thinking in arrays</strong> means sketching several visual options on paper before committing; and the <strong>five pillars</strong> &mdash; charts, icons, diagrams, typography, photography &mdash; keep the toolbox wider than a default bar chart.</p>
{P}The same devices run through our {LINK("/?page_id=687", "Introduction to Data Visualization workshop")} &mdash; on your data instead of a dummy set. The chapter cards above are from the ZIM decks themselves.</p>''',
})
art2 = fill(blocks['article2'], {
    'ARTICLE_2_SUBTITLE': 'Wide doors, small rooms&hellip;',
    'ARTICLE_2_HEADING': 'Designing a program for a global analyst community',
    'ARTICLE_2_BODY': f'''{P}The ZIM brief had a scale mismatch built in: the message mattered to <strong>every analyst in the company</strong>, and hands-on training only works in <strong>small rooms</strong>. Most programs pick one and lose the other. A funnel keeps both &mdash; open one-hour lectures for the many, four-hour workshops for the twenty.</p>
{P}The lecture is not a teaser; it does real work. An hour on <strong>data accessibility and storytelling</strong> gives the whole analyst community shared vocabulary and tells the business change is coming. The workshops then take the people who build the reports through the method properly &mdash; exercises, critique, and a <strong>workbook</strong> they keep.</p>
{P}Geography shaped everything else. Sessions were placed inside <strong>Jerusalem, Hong Kong, and Americas working hours</strong> from Melbourne, and the Americas cohort grew to include <strong>Brazil</strong> along the way &mdash; a reminder that global programs should be designed to stretch. Splitting each workshop into <strong>two two-hour sessions</strong> kept virtual attention honest and gave attendees a week to apply the first half before the second.</p>
{P}Aftercare closed the loop: curated slide packs, summary packs per cohort, and session recordings &mdash; the materials a busy analyst returns to at report-writing time. The format is repeatable, and the economics live on our {LINK("https://www.datalabsagency.com/data-visualisation-workshop-pricing/", "workshop pricing page")}; the program shape is yours for the asking via our {LINK("/?page_id=661", "training workshops")}.</p>''',
})

page = assemble([hero_p1, row_flow, row_secB, t_shape, row_gallery, row_hotspot, row_tiles,
                 sec_deliver, row_quote, row_faq, art1, blocks['offers'], art2, blocks['fixed']])
page = apply_theme(page, '#201c2c')  # ZIM tint: deep indigo (Otto's near-black-with-a-tinge rule)
assert 'Elisha' not in page and 'Lev' not in page and '16,625' not in page and 'Goelman' not in page
print('composed chars:', len(page))
import os, json, base64, urllib.request
pathlib.Path(OUT).write_text(page)
user, pw = os.environ['WP_DATALABS_USER'], os.environ['WP_DATALABS_APP_PASSWORD']
req = urllib.request.Request('https://www.datalabsagency.com/wp-json/wp/v2/pages/54130',
    data=json.dumps({'content': page, 'status': 'draft'}).encode(),
    headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
             'Authorization': 'Basic ' + base64.b64encode(f'{user}:{pw}'.encode()).decode()}, method='POST')
print('WP updated:', json.load(urllib.request.urlopen(req))['id'])
print('\nYOAST: SEO TITLE: ZIM Case Study: Data Storytelling for Analysts | Datalabs')
print('META DESCRIPTION: How the Datalabs Agency trained the analysts of ZIM Integrated Shipping Services - two open lectures and three workshops across Israel, Hong Kong, and the Americas.')
