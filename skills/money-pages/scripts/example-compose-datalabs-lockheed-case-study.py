#!/usr/bin/env python3
"""Compose the Lockheed Martin Visual Case Study — overnight batch, 25 Aug 2026.

Content: tier-1 reference, Lockheed section (the cleanest-facts case study).
Rules honoured: the phrase "three-tier engagement model" is NOT used (third tier
never documented); NO dollar figures from the rate breakdown (internal quote data —
Otto can add if he wants them public); facts used are all documented (287 LDP
participants, 0-3 yrs, six functions, LDC II capstone, 8 concurrent virtual
sessions / 4 slots / 2 days, 90-minute format, 40-50 per session, June 14-15 2022,
timeline Apr-Jun, 287 digital workbooks, custom datasets, coaches 20+ embedded,
engagement every 4-8 minutes, lived experience > generic case studies).
INTERACTIVE EXPERIMENT #1: animated delivery-machine SVG — 287 participants
fanning into 8 session blocks across two days, coach band beneath.
Media: 53898 title (hero), 53901/53904/53907 chapter cards, 53910 dataset.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from vcs_lib import *

blocks = kit_blocks()
OUT = '/private/tmp/claude-501/-Users-Ottinger-Claude-Projects-2026-project-manager-agent/1250d283-1a10-4416-b992-be81f96ce7a2/scratchpad/composed-lockheed.html'

# ---------- hero ----------
hero = widen_hero(fill(blocks['intro'], {
    'PAGE_SUBTITLE': 'A visual case study&hellip;',
    'PAGE_TITLE': 'Lockheed Martin: 287 Leaders, 2 Days',
    'UPDATED_DATE': 'August 2026',
    'HOOK': 'In June 2022, Lockheed Martin&rsquo;s Leadership Development Conference needed a capstone: data visualisation and storytelling training for <strong>287 emerging leaders</strong>. The answer: <strong>eight concurrent virtual sessions over two days</strong>, delivered by Datalabs with Lockheed&rsquo;s own leaders embedded as coaches in every room.',
    'SECTION_A_SUBTITLE': 'The engagement in one paragraph',
    'SECTION_A_HEADING': 'What did the Datalabs Agency deliver for Lockheed Martin?',
    'SECTION_A_INTRO': 'For <strong>Leadership Development Conference II</strong> (theme: Bold Leadership), the <strong>Datalabs Agency</strong> designed and facilitated virtual data visualisation and storytelling workshops for <strong>287 Leadership Development Program participants</strong> &mdash; eight 90-minute sessions across four time slots on 14&ndash;15 June 2022, with custom Lockheed Martin-branded materials, <strong>287 digital participant workbooks</strong>, and a full coach-support kit.',
    'CANONICAL_SENTENCE': CANONICAL,
    'SECTION_B_SUBTITLE': 'The problem behind the brief',
    'SECTION_B_HEADING': 'Why does a leadership program end with data storytelling?',
    'SECTION_B_ANSWER': 'The animation above is the delivery machine. The brief behind it: Lockheed&rsquo;s LDP participants &mdash; leaders with <strong>0&ndash;3 years&rsquo; experience</strong> drawn from <strong>six functions across the business</strong> &mdash; were finishing a program about leading boldly. The capstone had to teach the skill bold leadership runs on: <strong>making a case with data</strong>.',
    'SECTION_B_CONTEXT': 'A capstone audience is an unforgiving one &mdash; 287 people at the end of a long program, all attending virtually, across functions with very different relationships to data. The design answer was concurrency and coaching: sessions capped at <strong>40&ndash;50 participants</strong> so exercises stay personal, run eight times so nobody waits a month for their slot, and staffed with senior Lockheed Martin leaders <strong>embedded as coaches</strong>, so the conversation continues inside the business after the facilitator logs off.',
    'PRIMARY_CTA_TEXT': 'Plan your program capstone',
    'PRIMARY_CTA_URL': CONTACT,
}))
hero_p1, row_secB = split_hero(hero, 53898)

# ---------- Row: Animated Flow Diagram — the delivery machine ----------
def svg_delivery():
    parts = [f'<svg viewBox="0 0 1200 640" xmlns="http://www.w3.org/2000/svg" role="img" '
             f'aria-label="287 Lockheed Martin leadership participants delivered through eight concurrent virtual sessions across two days, with embedded coaches" '
             f'style="width:100%;height:auto;display:block;">']
    # left: participants hub
    parts.append(f'<rect x="40" y="210" width="250" height="150" rx="12" fill="#1f1e29" stroke="{TAN}" stroke-width="2.5"/>')
    parts.append(f'<text x="165" y="278" text-anchor="middle" font-family="{BEBAS}" font-size="64" fill="{TAN}">287</text>')
    parts.append(f'<text x="165" y="308" text-anchor="middle" font-family="{ARVO}" font-size="14" fill="#ffffff">emerging leaders</text>')
    parts.append(f'<text x="165" y="328" text-anchor="middle" font-family="{ARVO}" font-size="12" fill="#8a8a95">six functions, one capstone</text>')
    # two day columns, each with two slots, each slot two concurrent session blocks
    days = [('DAY 1', 'JUNE 14, 2022', 430), ('DAY 2', 'JUNE 15, 2022', 800)]
    slot_labels = ['MORNING SLOT', 'AFTERNOON SLOT']
    n = 0
    for day, date, x in days:
        parts.append(f'<text x="{x+150}" y="66" text-anchor="middle" font-family="{BEBAS}" font-size="28" letter-spacing="2" fill="#ffffff">{day}</text>')
        parts.append(f'<text x="{x+150}" y="88" text-anchor="middle" font-family="{ARVO}" font-size="12" fill="#8a8a95">{date}</text>')
        for s, sl in enumerate(slot_labels):
            sy = 110 + s * 210
            parts.append(f'<text x="{x+150}" y="{sy+14}" text-anchor="middle" font-family="{ARVO}" font-size="11" letter-spacing="1" fill="{TAN}">{sl}</text>')
            for b in range(2):
                by = sy + 28 + b * 84
                n += 1
                delay = round(0.25 * n, 2)
                parts.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="{delay}s" fill="freeze"/>'
                             f'<rect x="{x}" y="{by}" width="300" height="70" rx="9" fill="#262532" stroke="#4a4860" stroke-width="1.5"/>'
                             f'<text x="{x+18}" y="{by+30}" font-family="{BEBAS}" font-size="21" letter-spacing="1" fill="#ffffff">SESSION {n}</text>'
                             f'<text x="{x+18}" y="{by+52}" font-family="{ARVO}" font-size="12" fill="#8a8a95">90 minutes, 40&#8211;50 leaders</text>'
                             f'<circle cx="{x+272}" cy="{by+35}" r="13" fill="none" stroke="{TAN}" stroke-width="2"/>'
                             f'<circle cx="{x+272}" cy="{by+31}" r="4" fill="{TAN}"/>'
                             f'<path d="M {x+264} {by+43} C {x+264} {by+36}, {x+280} {by+36}, {x+280} {by+43}" fill="none" stroke="{TAN}" stroke-width="2"/></g>')
                # flow line from hub to block
                parts.append(flow_line(290, 285, x, by + 35, cx1=360))
    # coach band
    parts.append(f'<rect x="430" y="560" width="670" height="56" rx="9" fill="#262532" stroke="{TAN}" stroke-width="1.5" stroke-dasharray="5 6"/>')
    parts.append(f'<text x="765" y="588" text-anchor="middle" font-family="{BEBAS}" font-size="20" letter-spacing="1.5" fill="{TAN}">20+ LOCKHEED COACHES EMBEDDED ACROSS EVERY SESSION</text>')
    parts.append(f'<text x="765" y="606" text-anchor="middle" font-family="{ARVO}" font-size="11" fill="#8a8a95">Senior leaders, briefed and equipped before day one</text>')
    parts.append('</svg>')
    return ''.join(parts)

row_flow = svg_row('Watch the two days fill up', 'One capstone, eight rooms',
    'Every one of the <strong>287 participants</strong> landed in one of eight 90-minute sessions &mdash; small enough for exercises, concurrent enough to finish in two days.',
    svg_delivery())

# ---------- timeline table ----------
t_timeline = table_row(blocks, 'Contract to capstone', 'The ten-week delivery timeline',
    'The delivery cadence, contract to capstone.',
    ['Milestone', 'What happened'],
    [['Contract award', 'April 2022 &mdash; engagement confirmed'],
     ['Inside seven business days', 'Audience consultation call &mdash; who the leaders are and what they need'],
     ['Three weeks out', 'All participant materials submitted for review'],
     ['One week out', 'Virtual overview session for the embedded coaches'],
     ['Delivery', '14&ndash;15 June 2022 &mdash; eight sessions across four time slots']],
    footnote='All sessions delivered virtually, with the coach-support kit shipped ahead of the overview session.')

# ---------- gallery ----------
row_gallery = gallery_row('The materials, full size', 'Inside the workshop deck',
    'Click any card to view it full-screen &mdash; chapters from the <strong>custom Lockheed Martin-branded deck</strong> and the exercise dataset.',
    [(53901, 'Telling Visual Stories', 'The core chapter'),
     (53904, 'White Space', 'Design fundamentals, fast'),
     (53907, 'What Not To Do', 'The anti-patterns chapter'),
     (53910, 'The Custom Dataset', 'Built for the final exercises')])

# ---------- Row: Design Principle Tiles ----------
row_tiles = svg_row('The rules under every session', 'The principles behind the design',
    'Six principles shaped all eight sessions &mdash; and the <strong>coach kit</strong> built on them stayed with Lockheed.',
    svg_tiles('The six design principles behind the Lockheed Martin workshops', [
        ('ENGAGEMENT EVERY 4&#8211;8 MIN', 'No stretch of the session runs passive', 'clock'),
        ('LIVED EXPERIENCE', 'Real project stories over stock case studies', 'doc'),
        ('DELIBERATE PRACTICE', 'Structured exercises, not passive watching', 'target'),
        ('PRACTICE DATASETS', 'Custom-built dummy data, shaped like the work', 'grid'),
        ('COACHES IN THE ROOM', '20+ senior leaders embedded in sessions', 'people'),
        ('BUILT FOR VIRTUAL', 'Motion graphics made for screen delivery', 'layers'),
    ]))

# ---------- deliverables ----------
sec_deliver = widen_inner(fill(blocks['section2'], {
    'SECTION_D_SUBTITLE': 'Delivered, documented, taught',
    'SECTION_D_HEADING': 'What did Lockheed Martin receive at the end?',
    'SECTION_D_ANSWER': 'Lockheed received a custom <strong>90-minute slide deck</strong> in its own branding, <strong>287 professionally designed digital workbooks</strong>, visual examples and motion graphics built for virtual delivery, custom practice datasets for the final exercises, and a complete <strong>coach-support kit</strong>.',
    'SECTION_D_RATIONALE': 'The coach kit is the part that outlasts the two days. Because the coaches were <strong>Lockheed&rsquo;s own senior leaders</strong>, every session ended with someone inside the business who had seen the method work and could hold participants to it. Training that embeds the client&rsquo;s own leaders becomes capability building rather than a guest lecture &mdash; and it has been the <strong>Datalabs Agency</strong> model ever since.',
}), '1/4', '1/2')

# ---------- quote ----------
row_quote = quote_row('Otto Ottinger', 'The design principle behind the Lockheed sessions',
    'Lived experience beats generic case studies &mdash; a leader remembers the story of a real project, not a stock chart.')

# ---------- FAQ ----------
row_faq = faq_row(blocks, 'The Lockheed Martin program', 'Ask about your program', [
    ('How many people did the Datalabs Agency train at Lockheed Martin?',
     '<strong>287 Leadership Development Program participants</strong>, all with 0&ndash;3 years of leadership experience, drawn from six functions across the business. The workshops were the <strong>capstone of Leadership Development Conference II</strong> in June 2022.'),
    ('How were 287 people trained in two days?',
     '<strong>Eight concurrent 90-minute virtual sessions</strong> across four time slots on 14 and 15 June 2022, each capped at <strong>40&ndash;50 participants</strong> so the exercises stayed hands-on. Two slots ran each day, morning and afternoon US Eastern time.'),
    ('What materials did participants receive?',
     'A custom slide deck in Lockheed Martin branding, a professionally designed <strong>digital workbook for each of the 287 participants</strong>, visual examples and motion graphics built for virtual delivery, and <strong>custom practice datasets</strong> &mdash; dummy data shaped like the work &mdash; for the final exercises.'),
    ('What role did the coaches play?',
     '<strong>More than twenty senior Lockheed Martin leaders</strong> were <strong>embedded in the sessions</strong>, briefed and equipped with a full coach-support kit ahead of delivery. They carried the method back into the business after the program ended.'),
    ('Can the Datalabs Agency run a capstone like this for our leadership program?',
     'Yes. Concurrent virtual sessions, custom-branded materials, digital workbooks, and a <strong>coach-support layer</strong> is a repeatable format &mdash; the schedule <strong>scales to your cohort size and time zones</strong>. Send your program shape through the contact form and we will reply with a delivery plan.'),
])

# ---------- articles ----------
art1 = fill(blocks['article1'], {
    'ARTICLE_1_SUBTITLE': 'Attention is the deliverable',
    'ARTICLE_1_HEADING': 'Designing a virtual workshop leaders do not tab away from',
    'ARTICLE_1_BODY': f'''{P}A virtual room is the hardest room. Nobody has to look at you; the second monitor is right there. So the Lockheed sessions were engineered around one number: <strong>something changes every four to eight minutes</strong>. A prompt, an exercise, a critique, a story &mdash; the format never sits still long enough for attention to leave.</p>
{P}The exercises did the heavy lifting. <strong>Deliberate practice</strong> &mdash; structured, repeatable exercises with feedback &mdash; beats demonstration every time, so participants spent their minutes building, not watching. The final exercises ran on <strong>custom-built practice datasets</strong> &mdash; dummy data shaped like the work &mdash; because a leader in operations or finance takes a lesson seriously when the exercise feels like their world.</p>
{P}The materials were built natively for the medium: <strong>motion graphics</strong> and visual examples designed for screen delivery, and a digital workbook for every participant &mdash; all 287 of them &mdash; so the session left something behind that survives the meeting-ends chime.</p>
{P}You will find the same care in our {LINK("/?page_id=661", "data visualisation training workshops")} &mdash; that rhythm of constant engagement is what virtual training owes its audience.</p>''',
})
art2 = fill(blocks['article2'], {
    'ARTICLE_2_SUBTITLE': 'Ten weeks, no drift&hellip;',
    'ARTICLE_2_HEADING': 'What a capstone workshop has to do',
    'ARTICLE_2_BODY': f'''{P}A capstone is not just another session &mdash; it is the last thing a development program says to its participants. Lockheed&rsquo;s Leadership Development Conference II carried the theme <strong>Bold Leadership</strong>, and the closing argument was that boldness needs evidence: leaders who can <strong>make a case with data</strong> get their boldness funded.</p>
{P}The audience made the brief interesting. All 287 participants were <strong>early-career leaders</strong> &mdash; zero to three years in &mdash; but they came from six different functions. An engineer&rsquo;s relationship with a chart is not an HR leader&rsquo;s. The content held the middle: storytelling structure and visual judgement, taught through examples broad enough for every function and exercises specific enough to bite.</p>
{P}The delivery discipline mattered as much as the content. From <strong>contract award in April</strong> to delivery on <strong>14&ndash;15 June</strong>, the timeline ran through a fixed sequence &mdash; audience consultation inside seven business days, materials submitted three weeks out, a coach overview one week out. Corporate training earns trust by hitting dates, and this engagement hit every one.</p>
{P}The embedded-coach layer is the piece I would keep from this project above all others &mdash; and the piece most programs skip. If you are planning a capstone, start with our {LINK("/?page_id=687", "Introduction to Data Visualization workshop")} as the base and ask about the coach kit; the format and economics are on our {LINK("https://www.datalabsagency.com/data-visualisation-workshop-pricing/", "workshop pricing page")}.</p>''',
})

# ---------- assemble & push ----------
page = assemble([hero_p1, row_flow, row_secB, t_timeline, row_gallery, row_tiles,
                 sec_deliver, row_quote, row_faq, art1, blocks['offers'], art2, blocks['fixed']])
page = apply_theme(page, '#1a2230')  # per-page tint (Otto-approved palette, 25 Aug)
print('composed chars:', len(page))
import os, json, base64, urllib.request
pathlib.Path(OUT).write_text(page)
user, pw = os.environ['WP_DATALABS_USER'], os.environ['WP_DATALABS_APP_PASSWORD']
req = urllib.request.Request('https://www.datalabsagency.com/wp-json/wp/v2/pages/53913',
    data=json.dumps({'content': page, 'status': 'draft'}).encode(),
    headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
             'Authorization': 'Basic ' + base64.b64encode(f'{user}:{pw}'.encode()).decode()}, method='POST')
print('WP updated:', json.load(urllib.request.urlopen(req))['id'])
print('\nYOAST: SEO TITLE: Lockheed Martin Case Study: Leadership Workshops | Datalabs')
print('META DESCRIPTION: How the Datalabs Agency trained 287 Lockheed Martin emerging leaders in data storytelling - eight virtual sessions in two days, with embedded coaches.')
