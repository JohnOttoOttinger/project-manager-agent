#!/usr/bin/env python3
"""Compose the Oddtoe 'What Is Generative AI Animation?' page from design-kit-oddtoe.html v1."""
import re, base64, urllib.parse, pathlib, json, os, urllib.request

KIT = pathlib.Path('skills/money-pages/references/design-kit-oddtoe.html').read_text()
OUT = pathlib.Path('/private/tmp/claude-501/-Users-Ottinger-Claude-Projects-2026-project-manager-agent/a78a6ab8-b8af-4f3d-9842-393c8ffff22d/scratchpad/composed-ai-animation.html')

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
    'PAGE_SUBTITLE': 'Animation with an artist at the wheel...',
    'PAGE_TITLE': 'Generative AI Animation',
    'UPDATED_DATE': 'August 2026',
    'HOOK': 'Generative AI animation is animation made with AI image and video models under an artist&rsquo;s direction &mdash; <strong>designed, directed, and edited</strong> like any other film. Here is what it is, where it works, and how a <strong>Melbourne studio</strong> uses it for brands, documentaries, events, and original series.',
    'SECTION_A_SUBTITLE': 'The plain-language definition...',
    'SECTION_A_HEADING': 'What is generative AI animation?',
    'SECTION_A_INTRO': 'Generative AI animation is animation created with artificial-intelligence image and video models, directed by an artist rather than typed into existence. At Oddtoe it is a <strong>hybrid workflow</strong> &mdash; generative AI combined with <strong>advanced rigging</strong> and <strong>traditional motion design</strong> &mdash; so the result holds one consistent style instead of a lucky dip of outputs.',
    'CANONICAL_SENTENCE': CANON,
    'SECTION_B_SUBTITLE': 'Brands, filmmakers, institutions...',
    'SECTION_B_HEADING': 'Who uses it, and for what?',
    'SECTION_B_ANSWER': 'Brands use generative AI animation for <strong>branded content</strong>, characters, and campaign loops; documentary makers use it for <strong>animated maps, diagrams, and reconstructions</strong>; venues and events use it for screen and <strong>projection content</strong>. Oddtoe works both as a studio in its own right and as a resource inside other studios&rsquo; productions.',
    'SECTION_B_CONTEXT': 'Inside other productions, Oddtoe takes whichever seat the project needs &mdash; art director, head of animation, lead animator, character designer, or background artist. That flexibility is a feature of the medium: generative AI compresses the production pipeline, so one experienced <a href="/studio/generative-ai-animator/">generative AI animator</a> can carry roles that once needed a department. For brand teams, that means animated content at a pace and budget that hand animation rarely allows.',
    'PRIMARY_CTA_TEXT': 'Start a conversation',
    'PRIMARY_CTA_URL': CONTACT,
})

art1 = fill(blocks['article1'], {
    'ARTICLE_1_SUBTITLE': 'From campaign loops to documentaries...',
    'ARTICLE_1_HEADING': 'Where AI animation fits in real work',
    'ARTICLE_1_BODY': f'''{P}<strong>Branded content and campaign loops.</strong> Short, styled animation for campaigns, YouTube channels, and social &mdash; where a brand needs a <strong>cohesive look</strong> across many pieces, not one lucky render. This is where art direction earns its keep: the hundredth asset still looks like the first.</p>
{P}<strong>Documentary graphics.</strong> Animated maps, ways to visualise time and place, conceptual diagrams, reconstructions &mdash; the visual library of <a href="/studio/documentary-animator/">documentary animation</a> is enormous, and generative tools widen it further. Oddtoe works in 2D and 3D non-fiction animation, with a visual-storytelling background that began at National Geographic.</p>
{P}<strong>Characters that persist.</strong> A <a href="/artist-designer/character-designer/">designed character</a>, kept consistent across episodes, formats, and campaigns &mdash; the hardest thing to get from raw AI tools and the most valuable thing a directed workflow delivers.</p>
{P}<strong>Screens, events, and projection.</strong> Looping animated content for event screens and <a href="/artist-designer/projection-artist/">projection</a> &mdash; AI animation is a natural feed for physical experiences, which is why it appears throughout our <a href="/brand-activation-ideas/">brand activation ideas</a>.</p>
{P}<strong>Original series and art.</strong> Oddtoe also makes its own work &mdash; <a href="/studio/original-stories/">original stories</a> generated with AI and the human mind, including <em>The Top 100 Comedians of All Time Will Be Bots</em> (Oddtoe, 2023). Making our own series is how the studio stays ahead of the tools.</p>''',
})

# comparison table: recommended column = artist-led AI studio
CTH = "style=\"padding: 8px 14px; text-align: left; background-color: #000000 !important; border: none !important; border-bottom: 2px solid #ddccb1 !important; font-family: 'Bebas Neue', sans-serif; font-size: 19px; font-weight: normal; letter-spacing: 1px; color: #ffffff !important;\""
CTHREC = CTH.replace('background-color: #000000 !important', 'background-color: #ddccb1 !important').replace('color: #ffffff !important', 'color: #000000 !important')
def ctd(bg, bold=False):
    s = f'padding: 8px 14px; font-size: 15px; text-align: left; background-color: {bg} !important; border: none !important; border-bottom: 1px solid #26161f !important; color: #ffffff !important;'
    if bold: s += ' font-weight: bold;'
    return f'style="{s}"'
rows = []
for crit, trad, diy, led in [
    ('Style consistency', 'Handcrafted and consistent', 'Changes shot to shot', 'Directed and consistent'),
    ('Speed to first cut', 'Slowest', 'Instant, but generic', 'Fast, with direction'),
    ('Works from a brand brief', 'Yes, at a price', 'Rarely survives one', 'Yes &mdash; that is the job'),
    ('Revisions that stick', 'Slow to change', 'Every change is a re-roll', 'Rigged and editable'),
]:
    cells = f'<td {ctd("#000000", bold=True)}>{crit}</td><td {ctd("#000000")}>{trad}</td><td {ctd("#000000")}>{diy}</td><td {ctd("#111111")}>{led}</td>'
    rows.append('<tr>' + cells + '</tr>')
fmt_table = ('<div style="overflow-x: auto;">\n<table style="width: 100%; border-collapse: collapse !important; background-color: #000000 !important; border: none !important;">\n<thead>\n<tr>'
    + f'<th scope="col" {CTH}>&nbsp;</th><th scope="col" {CTH}>Traditional animation</th><th scope="col" {CTH}>DIY prompt tools</th><th scope="col" {CTHREC}>Artist-led AI studio</th>'
    + '</tr>\n</thead>\n<tbody>\n' + '\n'.join(rows) + '\n</tbody>\n</table>\n</div>')

tbl = fill(blocks['table'], {'TABLE_SUBTITLE': 'Three ways to make animation...', 'TABLE_HEADING': 'AI, DIY, or traditional &mdash; which fits?'})
guts = '<p style="text-align: center;"><strong>The honest comparison &mdash; where each approach shines:</strong></p>\n\n' + fmt_table
tbl = re.sub(r'(\[vc_column_text css=""\]).*?(\[/vc_column_text\])', lambda m2: m2.group(1) + '\n' + guts + '\n' + m2.group(2), tbl, count=1, flags=re.S)

art2 = fill(blocks['article2'], {
    'ARTICLE_2_SUBTITLE': 'Why direction beats prompting...',
    'ARTICLE_2_HEADING': 'Artist-led, not prompt-fed',
    'ARTICLE_2_BODY': f'''{P}Anyone can generate a striking image. The hard part &mdash; the part clients actually pay for &mdash; is generating the <strong>same world twice</strong>: a character who looks like herself in shot forty, a palette that holds across a campaign, a style a brand can own. Raw AI consistency simply is not there yet, which is why every Oddtoe method <strong>begins with a quality illustration</strong> and lets the AI interpret the scene &mdash; direction first, generation second. That is a craft problem, not a prompting problem, and it is why Oddtoe treats AI models as crew rather than as vending machines.</p>
{P}The studio&rsquo;s range comes from an unusual r&eacute;sum&eacute;: political cartoonist, puppeteer, <strong>data visualiser</strong>, street artist &mdash; and, since 2006, work for organisations including <strong>National Geographic</strong>. Each of those trades is a different way of deciding what an image must say before deciding how it looks. Generative AI rewards exactly that kind of decision-making, and punishes its absence.</p>
{P}There is also an honest artistic case for the medium. AI systems produce permutations, glitches, and odd choices &mdash; and under direction, those become material. Oddtoe&rsquo;s <a href="/studio/original-stories/">original stories</a> lean into that strangeness deliberately; commercial work tames it deliberately. Both are choices an artist makes, which is the whole point.</p>
{P}If your team is weighing up AI animation, the practical question is not &ldquo;which tool?&rdquo; but &ldquo;who is directing?&rdquo; Bring the brief; the <a href="/studio/generative-ai-animator/">studio</a> brings the taste, the rigging, and the motion design that turn generated frames into finished film.</p>''',
})

sec_c = fill(blocks['section1'], {
    'SECTION_C_SUBTITLE': 'Generative AI plus craft...',
    'SECTION_C_HEADING': 'How does the hybrid workflow work?',
    'SECTION_C_ANSWER': 'Oddtoe&rsquo;s process is a <strong>hybrid workflow</strong>: generative AI models supply imagery and movement, combined with <strong>advanced rigging</strong> and <strong>traditional motion design</strong>. The artist designs first, generates second, then rigs, edits, and composites &mdash; so revisions are edits, not re-rolls.',
    'SECTION_C_DETAIL': 'That structure is what makes the medium dependable enough for client work: a change to a character, a colour, or a line of action is made the way animators have always made it, with the AI doing the expensive rendering underneath. Oddtoe has prototyped and documented five distinct methods &mdash; from illustration-first motion design to repeatable AI-rigged characters and straight-to-video with an illustration filter &mdash; on our <a href="/my-product/atheism-documentary/">AI animation process</a> page, and the full capability lives on the <a href="/studio/generative-ai-animator/">generative AI animator</a> page.',
})
sec_d = fill(blocks['section2'], {
    'SECTION_D_SUBTITLE': 'The right tool for the brief...',
    'SECTION_D_HEADING': 'When should you choose AI animation?',
    'SECTION_D_ANSWER': 'Choose generative AI animation when you need animated content at <strong>pace or scale</strong> &mdash; series, campaigns, loops &mdash; or looks that would be impractical to shoot or hand-animate, and when <strong>style consistency</strong> matters enough that you want an artist directing it.',
    'SECTION_D_RATIONALE': 'It is not the right tool for everything: some briefs deserve hand animation&rsquo;s line, and some need live action&rsquo;s truth. A studio that works across generative AI, traditional motion design, and physical media will tell you which &mdash; and that honesty is worth more than any single technique.',
})

faq_pairs = [
    ('Is generative AI animation just typing prompts?',
     'No. At Oddtoe it is a hybrid workflow combining generative AI with advanced rigging and traditional motion design, under an artist&rsquo;s direction. Prompting produces raw material; design, rigging, editing, and compositing turn it into finished, revisable film.'),
    ('Can AI animation keep a consistent brand style?',
     'Yes &mdash; with character design and art direction up front. Brands have longer-term needs and a cohesive style to protect, and holding that consistency across shots and campaigns is precisely what an artist-led workflow delivers and raw prompt tools do not.'),
    ('Can generative AI animation be used in documentaries?',
     'Yes. Animated maps, ways to visualise time and place, conceptual diagrams, and reconstructions all suit the medium. Oddtoe works as a 2D and 3D documentary animator, with a visual-storytelling background that began at National Geographic.'),
    ('Can AI animation be part of a live event or activation?',
     'Naturally &mdash; looping content for event screens and projection is one of its best uses, and it pairs with physical builds in our <a href="/brand-activation-ideas/">brand activation ideas</a>. One directed character or world can run on screens, projection, and social at once.'),
    ('Do you work inside other studios&rsquo; productions?',
     'Yes. Oddtoe regularly joins other studios&rsquo; projects as art director, head of animation, lead animator, character designer, or background artist &mdash; whichever seat the production needs.'),
]
faq_map = {'FAQ_TOPIC': 'Generative AI animation', 'FAQ_CTA_TEXT': 'Talk about your project', 'FAQ_CTA_URL': CONTACT}
for i, (q, a) in enumerate(faq_pairs, 1):
    faq_map[f'FAQ_Q{i}'] = q
    faq_map[f'FAQ_A{i}'] = a
faq = fill(blocks['faq'], faq_map)

def plain(s):
    s = re.sub(r'<[^>]+>', '', s)
    for ent, ch in [('&mdash;', '—'), ('&ndash;', '–'), ('&amp;', '&'), ('&rsquo;', '’'), ('&ldquo;', '“'), ('&rdquo;', '”'), ('&eacute;', 'é')]:
        s = s.replace(ent, ch)
    return s
entities = [{"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in faq_pairs]
schema = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}, ensure_ascii=False) + '</script>'
enc = base64.b64encode(urllib.parse.quote(schema, safe='').encode()).decode()
faq = re.sub(r'\[vc_raw_html\][^\[]*\[/vc_raw_html\]', '[vc_raw_html]' + enc + '[/vc_raw_html]', faq)

# offers: 'A Process for AI Animation' + 'Non-Fiction Animator' banners from Otto's homepage
auth = 'Basic ' + base64.b64encode(f"{os.environ['WP_ODDTOE_USER']}:{os.environ['WP_ODDTOE_APP_PASSWORD']}".encode()).decode()
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
r = urllib.request.Request('https://www.oddtoe.com/wp-json/wp/v2/pages/15922?context=edit&nc=of2', headers={'Authorization': auth, 'User-Agent': UA})
home = json.load(urllib.request.urlopen(r))['content']['raw']
hb = re.findall(r'\[info_banner.*?\[/info_banner\]', home, re.S)
pick = [b for b in hb if 'A Process for AI Animation' in b] + [b for b in hb if 'Non-Fiction Animator' in b]
offers = blocks['offers']
ob = re.findall(r'\[info_banner.*?\[/info_banner\]', offers, re.S)
offers = offers.replace(ob[0], pick[0]).replace(ob[1], pick[1])

page = '\n'.join([hero, art1, tbl, sec_c, art2, sec_d, faq, offers, blocks['form']])
page = re.sub(r'<!--(?! YOAST).*?-->\n?', '', page, flags=re.S).strip()
page = re.sub(r'<a href=', '<a style="color: #ddccb1;" href=', page)
yoast = '<!-- YOAST SEO TITLE: What Is Generative AI Animation? An Artist-Led Guide | Oddtoe | META DESCRIPTION: Generative AI animation explained by Melbourne studio Oddtoe: a hybrid of AI models, rigging and motion design — for brands, documentaries, events and series. -->\n'
page = yoast + page

leftover = re.findall(r'\{\{[A-Z0-9_]+', page)
assert not leftover, 'unfilled: ' + str(set(leftover))
OUT.write_text(page)
print('composed:', len(page), 'chars | tables:', page.count('<table'), '| internal links:', page.count('href="/'), '| tokens left: 0')
