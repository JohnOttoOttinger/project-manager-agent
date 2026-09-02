#!/usr/bin/env python3
"""Compose the Monash University Visual Case Study.

Content source: ODD & DLA Strategy/monash-case-study.md (2 Sep 2026).
Facts confirmed by Otto 2 Sep 2026: client was Monash Marketing, engaged direct,
figures publishable. Attribution decision (Otto, 2 Sep 2026): attribute to
"Otto Ottinger and team" — the results infographic carries Curated Content
branding and no corporate lineage to Datalabs has been verified, so the page
claims neither agency brand for the delivery.

Results are from the campaign results infographic (Google Analytics / YouTube
Analytics sourced): 1.4M views, >90% engagement, Monash YouTube channel
1,196.4k -> 2,425.5k (+102.7%), Dec 2012 - Jan 2013, Indonesia/Malaysia/Singapore.
Deliberately NOT claimed: duration, team size, anything about the 2013-15 analytics
template's own figures as campaign results.
"""
import sys, pathlib, os
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from vcs_lib import *

blocks = kit_blocks()
MEDIA = '/Users/Ottinger/Documents/Datalabs - iCloud Apple/Proposals/Monash University/Case Study/media'
OUT = '/private/tmp/claude-501/-Users-Ottinger-Documents-Datalabs---iCloud-Apple-Business-Development-2026-Workshop-Sales-Push/50fe977a-e011-4496-95cf-d863f26ded8b/scratchpad/composed-monash.html'

# Uploaded 2 Sep 2026 with alt text. Re-running must not duplicate library items,
# so the ids are pinned. Set REUPLOAD=1 only when the source images change.
ids = {'rankings-infographic.jpg': 54134, 'case-study-results.jpg': 54145,
       'analytics-dashboard.jpg': 54140}
# 54137 (uncropped case-study-panel.jpg) is superseded: it carried Curated Content
# branding in the header, the Solution body copy and the footer. Cropped to the
# results section only, which names no agency. Old item left in the library, unused.
if os.environ.get('REUPLOAD'):
    ids = upload_media([
        ('rankings-infographic.jpg',
         'Monash University world rankings infographic showing 18 subjects in the world top 50',
         'Monash University rankings infographic'),
        ('case-study-panel.jpg',
         'Campaign results for the Monash University rankings motion graphic across Indonesia, Malaysia and Singapore',
         'Monash rankings campaign results'),
        ('analytics-dashboard.jpg',
         'Monash University marketing analytics reporting template covering social channels, enquiries and languages',
         'Monash analytics reporting template'),
    ], MEDIA)
HERO_ID = ids['rankings-infographic.jpg']

# ---------- hero ----------
hero = widen_hero(fill(blocks['intro'], {
    'PAGE_SUBTITLE': 'A visual case study&hellip;',
    'PAGE_TITLE': 'Monash: 1.4 Million Views, 3 Markets',
    'UPDATED_DATE': 'September 2026',
    'HOOK': 'Monash University wanted to reach the <strong>parents of prospective international students</strong>. Otto Ottinger and team built a rankings motion graphic, subtitled it in Bahasa, and ran it across Indonesia, Malaysia and Singapore &mdash; <strong>1.4 million views</strong>, engagement above <strong>90%</strong>, and the university&rsquo;s YouTube channel up <strong>102.7%</strong> in a month.',
    'SECTION_A_SUBTITLE': 'The engagement in one paragraph',
    'SECTION_A_HEADING': 'What was built for Monash University?',
    'SECTION_A_INTRO': 'A single rankings dataset became three things: a <strong>printed infographic</strong>, an <strong>animated data video</strong>, and a <strong>30-second cut subtitled in Bahasa</strong> for the Indonesian market. The video ran as a YouTube TrueView campaign from <strong>December 2012 to January 2013</strong> and became Monash&rsquo;s outstanding video result for the year.',
    'CANONICAL_SENTENCE': CANONICAL,
    'SECTION_B_SUBTITLE': 'The problem behind the brief',
    'SECTION_B_HEADING': 'Why subtitle a university video in Bahasa?',
    'SECTION_B_ANSWER': 'Because the buyer was not the student. Monash needed to reach <strong>parents of prospective international students</strong> &mdash; the people who actually weigh up whether a degree abroad is worth it &mdash; and those parents were searching in their own language.',
    'SECTION_B_CONTEXT': 'Keyword research settled the creative direction before a frame was drawn. <strong>&ldquo;University rankings&rdquo;</strong> was by a distance the most-used search term in university searches, so the motion graphic was themed and tagged to that term. The Bahasa cut followed the same logic one step further: if the primary audience searches in Bahasa, the video has to be findable in Bahasa. Neither decision was a stylistic preference. Both came out of the data.',
    'PRIMARY_CTA_TEXT': 'Talk about your data story',
    'PRIMARY_CTA_URL': CONTACT,
}))
hero_p1, row_secB = split_hero(hero, HERO_ID)

# ---------- Row: one dataset, three formats, three markets ----------
def svg_pipeline():
    p = [f'<svg viewBox="0 0 1200 620" xmlns="http://www.w3.org/2000/svg" role="img" '
         f'aria-label="One Monash rankings dataset rendered as an infographic, an animation and a Bahasa-subtitled cut, then run across Indonesia, Malaysia and Singapore" '
         f'style="width:100%;height:auto;display:block;">']
    # source dataset
    p.append(f'<rect x="34" y="248" width="232" height="126" rx="12" fill="#1f1e29" stroke="{TAN}" stroke-width="2.5"/>')
    p.append(f'<text x="150" y="300" text-anchor="middle" font-family="{BEBAS}" font-size="46" fill="{TAN}">ONE</text>')
    p.append(f'<text x="150" y="330" text-anchor="middle" font-family="{ARVO}" font-size="14" fill="#ffffff">rankings dataset</text>')
    p.append(f'<text x="150" y="352" text-anchor="middle" font-family="{ARVO}" font-size="11.5" fill="#8a8a95">THE, QS and NYT, 2012&#8211;13</text>')
    # three formats
    formats = [('INFOGRAPHIC', 'A3, print and web', 'doc', 96),
               ('MOTION GRAPHIC', '45 seconds, English', 'layers', 246),
               ('BAHASA CUT', '30 seconds, subtitled', 'people', 396)]
    for i, (t, sub, _g, y) in enumerate(formats):
        d = round(0.3 * (i + 1), 2)
        p.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="{d}s" fill="freeze"/>'
                 f'<rect x="392" y="{y}" width="286" height="96" rx="10" fill="#262532" stroke="#4a4860" stroke-width="1.5"/>'
                 f'<text x="416" y="{y+42}" font-family="{BEBAS}" font-size="24" letter-spacing="1.2" fill="#ffffff">{t}</text>'
                 f'<text x="416" y="{y+68}" font-family="{ARVO}" font-size="12.5" fill="#8a8a95">{sub}</text></g>')
        p.append(flow_line(266, 311, 392, y + 48, cx1=330))
    # three markets
    markets = [('INDONESIA', '887.0k views', '26% engagement', 96),
               ('MALAYSIA', '339.1k views', '15% engagement', 246),
               ('SINGAPORE', '270.2k views', '12% engagement', 396)]
    for i, (m, v, e, y) in enumerate(markets):
        d = round(1.3 + 0.3 * i, 2)
        p.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="{d}s" fill="freeze"/>'
                 f'<rect x="830" y="{y}" width="286" height="96" rx="10" fill="#1f1e29" stroke="{TAN}" stroke-width="2"/>'
                 f'<text x="854" y="{y+40}" font-family="{BEBAS}" font-size="24" letter-spacing="1.2" fill="{TAN}">{m}</text>'
                 f'<text x="854" y="{y+64}" font-family="{ARVO}" font-size="12.5" fill="#ffffff">{v}</text>'
                 f'<text x="854" y="{y+82}" font-family="{ARVO}" font-size="11.5" fill="#8a8a95">{e}</text></g>')
        p.append(flow_line(678, 444, 830, y + 48, cx1=760))
    # total band
    p.append(f'<rect x="392" y="530" width="724" height="58" rx="9" fill="#262532" stroke="{TAN}" stroke-width="1.5" stroke-dasharray="5 6"/>')
    p.append(f'<text x="754" y="559" text-anchor="middle" font-family="{BEBAS}" font-size="22" letter-spacing="1.5" fill="{TAN}">1.4 MILLION VIEWS &#183; ENGAGEMENT ABOVE 90%</text>')
    p.append(f'<text x="754" y="578" text-anchor="middle" font-family="{ARVO}" font-size="11.5" fill="#8a8a95">YouTube TrueView campaign, December 2012 &#8211; January 2013</text>')
    p.append('</svg>')
    return ''.join(p)

row_flow = svg_row('Follow the dataset', 'One dataset, three formats, three markets',
    'The same rankings data was rendered three ways, then pointed at the three markets where Monash was recruiting.',
    svg_pipeline())

# ---------- results table ----------
t_results = table_row(blocks, 'What the campaign returned', 'The numbers, market by market',
    'Campaign performance as recorded at the time, sourced to Google Analytics and YouTube Analytics.',
    ['Metric', 'Indonesia', 'Malaysia', 'Singapore'],
    [['Ad impressions', '3,376.1k', '2,251.9k', '623.0k'],
     ['Total video views', '887.0k', '339.1k', '270.2k'],
     ['Engagement rate', '26%', '15%', '12%'],
     ['Website clicks', '151.9k', '43.3k', '8.8k'],
     ['Website visits', '19.3k', '8.2k', '3.7k'],
     ['Click-through rate', '17.6%', '13.7%', '7.8%'],
     ['Social engagement rate', '26.3%', '14.7%', '12.2%']],
    footnote='Across the whole campaign, Monash&rsquo;s YouTube channel views rose from 1,196.4k in December 2012 to 2,425.5k in January 2013 &mdash; an increase of 102.7%.')

# ---------- gallery ----------
# Two cards, not three. gallery_row lays out 2-up, so a third cell orphans in a
# half-width column and reads off-centre. These two are also near-identical in
# proportion (1:1.46 and 1:1.39), so they sit level. The campaign-results
# infographic is 1:2.85 and was being shrunk to ~360px wide by img_size="large";
# it now has its own row below at full size.
row_gallery = gallery_row('The work, full size', 'What was designed',
    'Click either card to open it full-screen.',
    [(ids['rankings-infographic.jpg'], 'The Rankings Infographic', 'The source artefact'),
     (ids['analytics-dashboard.jpg'], 'The Reporting Template', 'Built for Monash Marketing')])

# ---------- Row: the period reporting artefact, full width (house 'big statement + image' shape) ----------
row_results_img = ('[vc_row bg_check="row-background-dark" dfd_enable_overlay=""]'
    '[vc_column width="1/6"][/vc_column][vc_column width="4/6"]' + SP(40)
    + '[dfd_heading enable_delimiter="" style="style_02" heading_margin="margin-bottom:20px;" '
      'subtitle="How it was reported at the time" '
      'title_font_options="tag:h2|font_size:70|line_height:64" '
      'subtitle_font_options="tag:h3|font_size:38|line_height:32"]\n'
      '<p style="text-align: center;">The results, as they were recorded</p>\n[/dfd_heading]' + SP(20)
    + '[vc_column_text css=""]\n'
      '<p style="line-height: 22px; text-align: left;">This is the <strong>campaign report</strong> produced when the '
      'work closed, sourced to Google Analytics and YouTube Analytics. It carries the '
      '<strong>102.7% jump in channel views</strong> across a single month and the full '
      'per-market breakdown &mdash; ad impressions, view duration, click-through and social '
      'engagement for <strong>Indonesia, Malaysia and Singapore</strong> side by side.</p>\n[/vc_column_text]' + SP(20)
    + f'[vc_single_image image="{ids["case-study-results.jpg"]}" img_size="full" alignment="center" '
      'style="vc_box_rounded" onclick="link_image"]'
    + SP(40) + '[/vc_column][vc_column width="1/6"][/vc_column][/vc_row]')

# ---------- principle tiles ----------
row_tiles = svg_row('The decisions that carried it', 'Six choices behind the result',
    'None of these were creative preferences. Each one came from something the data said.',
    svg_tiles('Six design decisions behind the Monash rankings campaign', [
        ('SEARCH DECIDED THE THEME', '&ldquo;University rankings&rdquo; led the keyword research', 'target'),
        ('PARENTS, NOT STUDENTS', 'The brief named the actual decision-maker', 'people'),
        ('SUBTITLED FOR FINDABILITY', 'Bahasa so the primary audience could search it', 'doc'),
        ('ONE DATASET, THREE CUTS', 'Print, animation, and a 30-second version', 'layers'),
        ('MEASURED PER MARKET', 'Indonesia, Malaysia and Singapore reported apart', 'grid'),
        ('REPORTING BUILT TO REUSE', 'A template Monash could fill each cycle', 'clock'),
    ]))

# ---------- deliverables ----------
sec_deliver = widen_inner(fill(blocks['section2'], {
    'SECTION_D_SUBTITLE': 'Designed, animated, localised, measured',
    'SECTION_D_HEADING': 'What did Monash Marketing receive?',
    'SECTION_D_ANSWER': 'A Monash-branded rankings <strong>infographic</strong> drawing on Times Higher Education, QS and New York Times data; an <strong>animated version</strong> of the same story; a <strong>30-second cut with Bahasa subtitles</strong> for the Indonesian market; and an <strong>analytics reporting template</strong> covering social channels, enquiry volumes, languages and international web traffic.',
    'SECTION_D_RATIONALE': 'The <strong>reporting template</strong> is the piece that kept working after the campaign closed. It was built as a layout <strong>Monash Marketing</strong> could fill each reporting cycle, pulling from Google Analytics, Facebook Insights, LinkedIn Analytics and Hootsuite &mdash; so the team could see the next campaign&rsquo;s audience the same way this one had been aimed.',
}), '1/4', '1/2')

# ---------- quote ----------
row_quote = quote_row('Otto Ottinger', 'The decision that made the Monash campaign work',
    'We did not translate the video because translation is nice. We subtitled it because the people deciding were searching in Bahasa, and an English video is invisible to them.')
# Otto asked for more air between the quote and the Q&A row (2 Sep 2026). Widen only this
# page's trailing spacer -- vcs_lib's quote_row is Otto-approved v1 and stays untouched, so
# every other case study keeps its existing rhythm.
_TAIL = '[/vc_column][vc_column width="1/4"][/vc_column][/vc_row]'
assert row_quote.endswith(SP(40) + _TAIL)
row_quote = row_quote[:-len(SP(40) + _TAIL)] + SP(120, 80) + _TAIL

# ---------- FAQ ----------
row_faq = faq_row(blocks, 'The Monash rankings campaign', 'Ask about your campaign', [
    ('What did the Monash University rankings campaign achieve?',
     'The motion graphic ran as a YouTube TrueView campaign across Indonesia, Malaysia and Singapore between December 2012 and January 2013. It drew <strong>close to 1.4 million views</strong> at an engagement rate <strong>above 90%</strong>, and Monash&rsquo;s YouTube channel views rose <strong>102.7%</strong> across the same period.'),
    ('Why was the video subtitled in Bahasa?',
     'The audience Monash needed was <strong>parents of prospective international students</strong>, and Indonesia was the largest of the three target markets. Subtitling made the video findable for people searching in their own language &mdash; Indonesia went on to return 887,000 views and a 26% engagement rate, the strongest of the three markets.'),
    ('How was the creative direction decided?',
     'By keyword research, before any design work started. <strong>&ldquo;University rankings&rdquo;</strong> was the dominant search term in university searches, so the motion graphic was themed and tagged to it. The rankings dataset then drove the infographic and the animation as well.'),
    ('Who did the work?',
     '<strong>Otto Ottinger and team</strong>, working with Monash Marketing directly. Otto now runs the <strong>Datalabs Agency</strong>, which delivers data visualisation design and training on the same method.'),
    ('Can you do something similar for our organisation?',
     'Yes. The pattern &mdash; find the search behaviour, build one dataset into several formats, localise for the audience that actually decides, then measure per market &mdash; transfers to most communications problems. Send yours through the contact form and we will reply with an approach.'),
])

# ---------- articles ----------
art1 = fill(blocks['article1'], {
    'ARTICLE_1_SUBTITLE': 'Design after research&hellip;',
    'ARTICLE_1_HEADING': 'How keyword research chose the creative',
    'ARTICLE_1_BODY': f'''{P}Most university video starts from a brand brief. This one started from a search log. Before anyone drew a frame, the research question was simple: what are people actually typing when they look up universities? The answer came back clearly enough to settle the creative direction &mdash; <strong>&ldquo;university rankings&rdquo;</strong> dominated, by a wide margin.</p>
{P}So the motion graphic was built around <strong>rankings</strong> and tagged to match. That is a narrower brief than &ldquo;promote the university&rdquo;, and the narrowness is the point: it meant the video <strong>answered a question people were already asking</strong> instead of one Monash wanted to raise.</p>
{P}The same dataset then carried an <strong>A3 infographic</strong> and a <strong>30-second cut</strong>. Three formats, one set of facts, each aimed at a different moment &mdash; a page someone reads, a video someone watches, a short someone is served.</p>
{P}That sequence is still how we teach format choice in our {LINK("/?page_id=661", "data visualisation training workshops")}: work out what the audience is looking for, then decide what to build.</p>''',
})
art2 = fill(blocks['article2'], {
    'ARTICLE_2_SUBTITLE': 'Reaching the actual decision-maker&hellip;',
    'ARTICLE_2_HEADING': 'The audience was never the student',
    'ARTICLE_2_BODY': f'''{P}The brief said something most university marketing skips over. The primary audience was not prospective students &mdash; it was their <strong>parents</strong>. Students may pick the country; parents weigh the cost, the safety and the standing of the institution, and a ranking is exactly the kind of evidence that settles a family argument.</p>
{P}Once the audience is named that precisely, the language question answers itself. <strong>Parents in Indonesia search in Bahasa.</strong> An English-only video is not simply less convenient for them, it is effectively invisible &mdash; it does not surface for the searches they run. Subtitling was a <strong>findability decision</strong>.</p>
{P}The results bore it out. Indonesia returned <strong>887,000 views</strong> and a <strong>26% engagement rate</strong>, well clear of Malaysia at 15% and Singapore at 12%, and it produced 151,900 website clicks against Singapore&rsquo;s 8,800.</p>
{P}Thirteen years on, the lesson has not aged. Identify who actually decides, find out how they search, and build for that. If you want your team working this way, the {LINK("/?page_id=687", "Introduction to Data Visualization workshop")} is where the method is taught, and the format and costs sit on our {LINK("https://www.datalabsagency.com/data-visualisation-workshop-pricing/", "workshop pricing page")}.</p>''',
})

# ---------- assemble & push ----------
page = assemble([hero_p1, row_flow, row_secB, t_results, row_results_img, row_gallery, row_tiles,
                 sec_deliver, row_quote, row_faq, art1, blocks['offers'], art2, blocks['fixed']])
page = apply_theme(page, '#101a2e')
print('composed chars:', len(page))
PAGE_ID = 54143  # created 2 Sep 2026
pathlib.Path(OUT).write_text(page)
import json, base64, urllib.request
_u, _p = os.environ['WP_DATALABS_USER'], os.environ['WP_DATALABS_APP_PASSWORD']
_req = urllib.request.Request(
    f'https://www.datalabsagency.com/wp-json/wp/v2/pages/{PAGE_ID}',
    data=json.dumps({'content': page, 'status': 'draft'}).encode(),
    headers={'Content-Type': 'application/json',
             'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
             'Authorization': 'Basic ' + base64.b64encode(f'{_u}:{_p}'.encode()).decode()},
    method='POST')
print('WP draft updated:', json.load(urllib.request.urlopen(_req))['id'])
print('Review: https://www.datalabsagency.com/wp-admin/post.php?post=%d&action=edit' % PAGE_ID)
print()
print('YOAST SEO TITLE: Monash University Case Study: 1.4M View Video Campaign')
print('META DESCRIPTION: How a Monash University rankings motion graphic, subtitled in Bahasa, drew 1.4 million views across Indonesia, Malaysia and Singapore.')
