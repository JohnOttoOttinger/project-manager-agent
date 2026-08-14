#!/usr/bin/env python3
"""Compose the Oddtoe 'Brand Activation Ideas' page from design-kit-oddtoe.html v1."""
import re, base64, urllib.parse, pathlib, json, os, urllib.request

KIT = pathlib.Path('skills/money-pages/references/design-kit-oddtoe.html').read_text()
OUT = pathlib.Path('/private/tmp/claude-501/-Users-Ottinger-Claude-Projects-2026-project-manager-agent/a78a6ab8-b8af-4f3d-9842-393c8ffff22d/scratchpad/composed-activation.html')

markers = [
    ('intro',    '<!-- PATTERN: intro'),
    ('faq',      '<!-- PATTERN: faq'),
    ('section1', '<!-- PATTERN: section (variant 1'),
    ('section2', '<!-- PATTERN: section (variant 2'),
    ('article1', '<!-- PATTERN: article (long-form slot 1'),
    ('offers',   '<!-- PATTERN: offers'),
    ('table',    '<!-- PATTERN: table'),
    ('article2', '<!-- PATTERN: article (long-form slot 2'),
    ('form',     '<!-- FIXED: project enquiry'),
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

CONTACT = 'https%3A%2F%2Fwww.oddtoe.com%2Fcontact-oddtoe%2F'
CANON = 'Oddtoe is an experiential design and generative-AI animation studio based in Melbourne, creating projection, installation, and animated work for events, venues, and galleries.'
P = '<p style="line-height: 22px; text-align: left;">'

hero = fill(blocks['intro'], {
    'PAGE_SUBTITLE': 'Ideas people stop for...',
    'PAGE_TITLE': 'Brand Activation Ideas',
    'UPDATED_DATE': 'August 2026',
    'HOOK': 'Ten brand activation ideas you can actually build &mdash; <strong>projection mapping</strong>, <strong>kinetic sculpture</strong>, living topiary, AI-animated characters, and oversized props. Collected by Oddtoe, a <strong>Melbourne experiential studio</strong> that designs and fabricates activations for agencies and brand teams, across Australia and internationally.',
    'SECTION_A_SUBTITLE': 'Before the ideas, the principle...',
    'SECTION_A_HEADING': 'What makes a brand activation work?',
    'SECTION_A_INTRO': 'A brand activation works when it gives people something they could not have scrolled past &mdash; an object, a moment, or a character that exists only <strong>here and now</strong>. The strongest activations are built around one clear physical idea, made well, and photographed a thousand times by strangers.',
    'CANONICAL_SENTENCE': CANON,
    'SECTION_B_SUBTITLE': 'Agencies, producers, brand teams...',
    'SECTION_B_HEADING': 'Who are these ideas for?',
    'SECTION_B_ANSWER': 'These concepts suit <strong>agencies and event producers</strong> looking for a build partner, and <strong>brand-side marketers</strong> planning launches, festivals, retail moments, or conference activations. Every idea below is something Oddtoe designs and fabricates in <strong>Melbourne</strong> and delivers Australia-wide, with international commissions welcome.',
    'SECTION_B_CONTEXT': 'Use the list as a briefing tool rather than a menu. Each idea scales &mdash; the same concept can fill a retail corner or anchor a festival site, and most of them combine well (a projection-mapped reveal with a fabricated photo moment, for instance). If your team already has a concept of its own, Oddtoe also works as a fabrication and production partner behind agencies &mdash; see how that works on our <a href="/experiential-marketing/">experiential marketing</a> page.',
    'PRIMARY_CTA_TEXT': 'Start a conversation',
    'PRIMARY_CTA_URL': CONTACT,
})

art1 = fill(blocks['article1'], {
    'ARTICLE_1_SUBTITLE': 'Five ideas built on light and motion...',
    'ARTICLE_1_HEADING': 'Ideas built on light and motion',
    'ARTICLE_1_BODY': f'''{P}<strong>1. A projection-mapped reveal.</strong> Wrap a building fa&ccedil;ade, a stage set, or the product itself in <a href="/artist-designer/projection-artist/">projection mapping</a> and let the launch happen in light. It turns architecture the audience already knows into the announcement itself, and it photographs like nothing else after dark.</p>
{P}<strong>2. An animated environment.</strong> Instead of one reveal moment, give a wall, floor, or interior a continuously animated skin &mdash; an environment that shifts through the evening and makes the venue the talking point. It suits conferences and venue takeovers where people dwell rather than pass through.</p>
{P}<strong>3. A kinetic sculpture centrepiece.</strong> A <a href="/artist-designer/kinetic-sculptor/">kinetic sculpture</a> earns a second look in a way a static display cannot &mdash; movement reads as alive. Long-run retail installs, lobbies, and exhibitions get the most from it, because the piece keeps performing for weeks.</p>
{P}<strong>4. An AI-animated brand character.</strong> A <a href="/artist-designer/character-designer/">designed character</a> brought to life with <a href="/studio/generative-ai-animator/">generative AI animation</a> can greet visitors on screens, loop through projection content, and carry the campaign onto social afterwards &mdash; one character, everywhere at once.</p>
{P}<strong>5. A robotic moment.</strong> A prop that moves when nobody expects it to &mdash; a <a href="/artist-designer/roboticist/">robotic build</a> timed to react to the crowd &mdash; creates the story people tell when they get home. Small mechanism, outsized memory.</p>''',
})

TH = "style=\"padding: 14px 18px; text-align: left; background-color: #000000 !important; border: none !important; border-bottom: 2px solid #ddccb1 !important; font-family: 'Bebas Neue', sans-serif; font-size: 21px; font-weight: normal; letter-spacing: 1px; color: #ffffff !important; white-space: nowrap;\""
def td(bg, bold=False):
    s = f'padding: 12px 18px; text-align: left; background-color: {bg} !important; border: none !important; border-bottom: 1px solid #26161f !important; color: #ffffff !important;'
    if bold: s += ' font-weight: bold;'
    return f'style="{s}"'
rows = []
data = [
    ('Projection mapping', 'Product reveals and night-time launches', 'Fa&ccedil;ades, stages, large interiors'),
    ('Kinetic sculpture', 'Long-run installs that reward a second look', 'Retail, lobbies, exhibitions'),
    ('AI-animated characters', 'One character across screens, loops and social', 'Event screens, projection content'),
    ('Living topiary', 'Slow-burn brand landmarks', 'Gardens, festivals, campuses'),
    ('Fabricated props', 'The photo moment', 'Launches, pop-ups, photo walls'),
]
for i, (a, b, c) in enumerate(data):
    bg = '#111111' if i % 2 else '#000000'
    rows.append(f'<tr>\n<td {td(bg, bold=True)}>{a}</td>\n<td {td(bg)}>{b}</td>\n<td {td(bg)}>{c}</td>\n</tr>')
fmt_table = ('<div style="overflow-x: auto;">\n<table style="width: 100%; border-collapse: collapse !important; background-color: #000000 !important; border: none !important;">\n<thead>\n<tr>'
    + f'<th scope="col" {TH}>Format</th><th scope="col" {TH}>Best for</th><th scope="col" {TH}>Strongest setting</th>'
    + '</tr>\n</thead>\n<tbody>\n' + '\n'.join(rows) + '\n</tbody>\n</table>\n</div>')

tbl = fill(blocks['table'], {'TABLE_SUBTITLE': 'A quick matching matrix...', 'TABLE_HEADING': 'Which format fits your brief?'})
guts = '<p style="text-align: center;"><strong>Formats compared by what they do best &mdash; shortlist two or three before you brief:</strong></p>\n\n' + fmt_table
tbl = re.sub(r'(\[vc_column_text css=""\]).*?(\[/vc_column_text\])', lambda m2: m2.group(1) + '\n' + guts + '\n' + m2.group(2), tbl, count=1, flags=re.S)

art2 = fill(blocks['article2'], {
    'ARTICLE_2_SUBTITLE': 'Five ideas built on craft and character...',
    'ARTICLE_2_HEADING': 'Ideas built on craft and character',
    'ARTICLE_2_BODY': f'''{P}<strong>6. A living topiary sculpture.</strong> A brand shape grown and sculpted as <a href="/artist-designer/topiarist/">living topiary</a> is the opposite of disposable event build &mdash; it gets better with time, and it belongs anywhere a festival, campus, or garden wants a landmark rather than a banner.</p>
{P}<strong>7. An oversized prop photo moment.</strong> The reliable heart of an activation: a <a href="/artist-designer/prop-designer-maker/">fabricated prop</a> at impossible scale. Done with craft, the prop is the campaign &mdash; people queue to be photographed with it and publish the evidence for you.</p>
{P}<strong>8. A live mural wall.</strong> Commission a <a href="/artist-designer/street-artist-muralist/">mural</a> painted live across the day of the event &mdash; the artwork is the entertainment, and the finished wall keeps working for the brand long after pack-down.</p>
{P}<strong>9. A sensory garden pop-up.</strong> A <a href="/artist-designer/sensory-garden-designer/">sensory garden</a> slows people down &mdash; scent, texture, and green space in a retail or event setting. It suits wellbeing, food, and lifestyle brands that want dwell time rather than spectacle.</p>
{P}<strong>10. A scripted character performance.</strong> Give the activation a voice: a <a href="/artist-designer/comedy-writer/">comedy-written</a> character &mdash; performed live or animated &mdash; that plays with the audience instead of presenting at them. Humour is the shortest path from stranger to participant.</p>''',
})

sec_c = fill(blocks['section1'], {
    'SECTION_C_SUBTITLE': 'Make it, run it, or both...',
    'SECTION_C_HEADING': 'Does Oddtoe build it, run it, or both?',
    'SECTION_C_ANSWER': 'Both. Oddtoe designs and fabricates the activation, and can also <strong>project-manage and run it</strong> on the day &mdash; or hand a finished build to your event team. Agencies often use the studio as a quiet <strong>build partner</strong> behind their own client work.',
    'SECTION_C_DETAIL': 'That flexibility matters when timelines are tight: one studio carrying an idea from concept sketch to fabrication to bump-out removes the hand-off risk between a creative agency, a fabricator, and an event crew. If you are an agency or producer, the working relationship is described on the <a href="/experiential-marketing/">experiential marketing</a> page; if you are a brand team, start with the moment you want people to have.',
})
sec_d = fill(blocks['section2'], {
    'SECTION_D_SUBTITLE': 'A good brief in five lines...',
    'SECTION_D_HEADING': 'How do you brief an experiential studio?',
    'SECTION_D_ANSWER': 'Bring the <strong>audience</strong>, the <strong>venue or setting</strong>, the <strong>moment you want people to have</strong>, your date, and the rough scale. You do not need a finished concept &mdash; two or three ideas from this page plus a clear objective is a strong brief.',
    'SECTION_D_RATIONALE': 'Briefs written around outcomes leave room for the craft that makes an activation memorable, while briefs written as shopping lists tend to buy exactly what every other event already had. Describe the reaction you want &mdash; stopped, delighted, photographing, talking &mdash; and let the format be chosen to earn it.',
})

faq_pairs = [
    ('Does Oddtoe build activations for agencies as a production partner?',
     'Yes. Agencies and event producers brief Oddtoe as a design and fabrication partner, and the studio is comfortable staying behind the scenes on client-facing work. You bring the client relationship; Oddtoe brings the build.'),
    ('Does Oddtoe run the activation on the day?',
     'It can. Alongside design and fabrication, Oddtoe offers event and project management &mdash; or hands a finished, tested build to your own event team. The split is agreed up front so nothing falls between crews.'),
    ('Where does Oddtoe work?',
     'The studio is based in Melbourne and delivers activations across Australia, with international commissions welcome &mdash; Oddtoe also maintains ties to <a href="/about-oddtoe/berlin/">Berlin</a> and <a href="/about-oddtoe/los-angeles/">Los Angeles</a>.'),
    ('Can generative AI animation be part of a physical activation?',
     'Yes. Artist-led generative AI animation supplies looping screen content, projection material, and brand characters that carry an activation onto social media afterwards &mdash; designed and directed by the studio, not left to a prompt.'),
    ('What if we already have a concept?',
     'Bring it. Oddtoe regularly fabricates and produces other teams&rsquo; concepts, and will tell you honestly what will and will not survive contact with a real venue, budget, and crowd.'),
]
faq_map = {'FAQ_TOPIC': 'Brand activations', 'FAQ_CTA_TEXT': 'Plan an activation', 'FAQ_CTA_URL': CONTACT}
for i, (q, a) in enumerate(faq_pairs, 1):
    faq_map[f'FAQ_Q{i}'] = q
    faq_map[f'FAQ_A{i}'] = a
faq = fill(blocks['faq'], faq_map)

def plain(s):
    s = re.sub(r'<[^>]+>', '', s)
    for ent, ch in [('&mdash;', '—'), ('&ndash;', '–'), ('&amp;', '&'), ('&rsquo;', '’'), ('&ccedil;', 'ç')]:
        s = s.replace(ent, ch)
    return s
entities = [{"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in faq_pairs]
schema = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}, ensure_ascii=False) + '</script>'
enc = base64.b64encode(urllib.parse.quote(schema, safe='').encode()).decode()
faq = re.sub(r'\[vc_raw_html\][^\[]*\[/vc_raw_html\]', '[vc_raw_html]' + enc + '[/vc_raw_html]', faq)

# offers: swap seeded banners for Prop Maker + AI Process (Otto's own homepage banners)
auth = 'Basic ' + base64.b64encode(f"{os.environ['WP_ODDTOE_USER']}:{os.environ['WP_ODDTOE_APP_PASSWORD']}".encode()).decode()
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
r = urllib.request.Request('https://www.oddtoe.com/wp-json/wp/v2/pages/15922?context=edit&nc=of1', headers={'Authorization': auth, 'User-Agent': UA})
home = json.load(urllib.request.urlopen(r))['content']['raw']
hb = re.findall(r'\[info_banner.*?\[/info_banner\]', home, re.S)
pick = [b for b in hb if 'Prop Maker' in b] + [b for b in hb if 'A Process for AI Animation' in b]
offers = blocks['offers']
ob = re.findall(r'\[info_banner.*?\[/info_banner\]', offers, re.S)
offers = offers.replace(ob[0], pick[0]).replace(ob[1], pick[1])

page = '\n'.join([hero, art1, tbl, art2, sec_c, sec_d, faq, offers, blocks['form']])
page = re.sub(r'<!--(?! YOAST).*?-->\n?', '', page, flags=re.S).strip()
# in-content links get the Oddtoe sand accent (theme renders plain links white-on-dark, invisible)
page = re.sub(r'<a href=', '<a style="color: #ddccb1;" href=', page)
yoast = '<!-- YOAST SEO TITLE: Brand Activation Ideas — 10 Concepts That Stop People | Oddtoe | META DESCRIPTION: Ten brand activation ideas from Melbourne experiential studio Oddtoe: projection mapping, kinetic sculpture, AI animation, living topiary and props people stop for. -->\n'
page = yoast + page

leftover = re.findall(r'\{\{[A-Z0-9_]+', page)
assert not leftover, 'unfilled: ' + str(set(leftover))
OUT.write_text(page)
print('composed:', len(page), 'chars | tables:', page.count('<table'), '| internal links:', page.count('href="/'), '| tokens left: 0')
