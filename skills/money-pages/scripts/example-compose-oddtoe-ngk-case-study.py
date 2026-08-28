#!/usr/bin/env python3
"""Compose the Oddtoe 'National Geographic Kids' Visual Case Study (first Oddtoe VCS).

Follows the Otto-approved VCS shape (template-catalog: "Visual Case Study — Datalabs",
Marriott 53852) but composes from design-kit-oddtoe.html v1 and retargets the accent
to Oddtoe sand (#ddccb1). Content facts come from the archive aggregation session
(00_Oddtoe-Curated-Library/INVENTORY.md): monthly layered Immersive homepage features
(738x330, fore/mid/background), the binocular splash homepage, and the games —
Back Talk, What in the World?, Wild & Wacky, Brainteasers, Green-o-Meter, NG Dog,
virtual-pet e-cards, WordGirl Funny Fill-Ins (PBS crossover), FunBook promo.
NO DATES in copy or media (Otto, 27 Aug 2026). Media 16211-16218 uploaded with
date-free alt text via upload-oddtoe-ngk-media.py. Draft only.
"""
import re, base64, json, os, pathlib, urllib.parse, urllib.request
import sys as _sys; _sys.path.insert(0, str(pathlib.Path(__file__).parent))
import vcs_lib
from vcs_lib import (fill, widen_hero, widen_inner, SP, HEAD_ROW, raw_html, svg_row,
                     svg_tiles, gallery_row, hotspot_row, table_row, faq_row, split_hero,
                     assemble, flow_line, DARKROW, BEBAS, ARVO, lighten)

REPO = pathlib.Path(__file__).resolve().parents[3]
for line in (REPO / '.env').read_text().splitlines():
    if '=' in line and not line.strip().startswith('#'):
        k, v = line.split('=', 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

KIT = (REPO / 'skills/money-pages/references/design-kit-oddtoe.html').read_text()
OUT = pathlib.Path('/private/tmp/claude-501/-Users-Ottinger-Claude-Projects-2026-project-manager-agent/998d6b6b-3365-4175-a0c5-39ee67e4bcc8/scratchpad/composed-ngk.html')

SAND = '#ddccb1'
vcs_lib.TAN = SAND  # svg helpers (flow_line, svg_tiles, glyph) must emit the Oddtoe accent
TINT = '#999900'          # the NGK stage green, sampled from the SWF captures (Otto, 27 Aug: match + blend)
KIT_PLUM = '#26161f'
CONTACT = 'https%3A%2F%2Fwww.oddtoe.com%2Fcontact-oddtoe%2F'
LINK = lambda href, label: f'<strong><a class="dfd-custom-link-decorated" href="{href}">{label}</a></strong>'
P = '<p style="line-height: 22px; text-align: left;">'
CANON = ('Oddtoe is an experiential design and generative-AI animation studio based in Melbourne, '
         'creating projection, installation, and animated work for events, venues, and galleries.')

# media (uploaded 27 Aug, ids from upload-oddtoe-ngk-media.py)
M_SPLASH, M_IMMERSIVE, M_BACKTALK, M_WITW, M_WACKY, M_GREEN, M_BRAIN, M_DOG = (
    16211, 16212, 16213, 16214, 16215, 16216, 16217, 16218)
ANIMATED = (M_SPLASH, M_IMMERSIVE, M_BACKTALK, M_WITW, M_DOG)  # GIFs: must render img_size="full"

# ---------- kit blocks (oddtoe kit: 'form' is the fixed footer) ----------
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

# ---------- hero ----------
hero = widen_hero(fill(blocks['intro'], {
    'PAGE_SUBTITLE': 'A visual case study&hellip;',
    'PAGE_TITLE': 'National Geographic Kids, Made Playable',
    'UPDATED_DATE': 'August 2026',
    'HOOK': 'The <em>National Geographic Kids</em> homepage was built like a toy: a pair of binoculars kids could look through, with the magazine&rsquo;s franchises &mdash; <strong>Back Talk, What in the World?, Wild &amp; Wacky</strong> and more &mdash; rebuilt as things to type into, unscramble, and print. Oddtoe designed and animated that homepage and <strong>a dozen of the interactive modules behind it</strong>. Every image on this page is the real work, running again &mdash; starting with the homepage itself: <strong>click the five markers</strong> to read it the way a nine-year-old did, region by region.',
    'SECTION_A_SUBTITLE': 'The project in one paragraph',
    'SECTION_A_HEADING': 'What did Oddtoe make for National Geographic Kids?',
    'SECTION_A_INTRO': 'Oddtoe ran the digital side of <em>National Geographic Kids</em> &mdash; online editor, designer, and cartoonist in one &mdash; and produced the award-winning site&rsquo;s <strong>interactive homepage</strong> &mdash; the binocular navigation above &mdash; and designed its games and content for <strong>nearly six years</strong>: a rolling <strong>immersive feature</strong> in layered parallax, plus the game modules that turned magazine pages into play &mdash; caption tools, photo puzzles, fill-in stories, and quiz engines the editorial team could refill themselves.',
    'CANONICAL_SENTENCE': CANON,
    'SECTION_B_SUBTITLE': 'The design problem',
    'SECTION_B_HEADING': 'How do you move a kids&rsquo; magazine onto a screen?',
    'SECTION_B_ANSWER': 'Not by scanning the pages. A nine-year-old opens a website the way they open a toy box &mdash; so the homepage became <strong>a pair of binoculars</strong>, the subscribe card a magazine cover that flips, and every franchise from the printed magazine became <strong>something to do</strong> rather than something to read.',
    'SECTION_B_CONTEXT': 'The brief had a second audience: the editors. A game that needs a developer for every new issue dies after three issues. So the modules were built as <strong>refillable engines</strong> &mdash; the fill-in stories read from a plain text file, the quizzes from an XML file &mdash; and the monthly immersive feature ran on a repeatable layered template. The magazine could keep the site as fresh as the print run without rebuilding anything.',
    'PRIMARY_CTA_TEXT': 'Talk characters &amp; play with Oddtoe',
    'PRIMARY_CTA_URL': CONTACT,
}))
hero_p1, row_secB = split_hero(hero, M_SPLASH)
hero_p1 = hero_p1.replace('image="16126"', f'image="{M_SPLASH}"')  # kit placeholder, if split missed it
# The hero image IS the interactive piece (Otto, 27 Aug: merge the hotspot into the first
# homepage appearance instead of showing the screen twice).
HOTSPOTS = [
    (27, 46, 'The featured lens', 'The left lens carries the monthly feature - a new story or activity each issue, framed like something spotted in the wild.'),
    (39, 24, 'Stories', 'The globe takes kids to the story archive - the magazine features, rewritten for the screen.'),
    (74, 28, 'Games', 'The soccer ball opens the games shelf: the puzzles, quizzes and fill-ins on this page.'),
    (88, 52, 'The franchise rail', 'World News, Wild and Wacky, Back Talk, What in the World - the printed magazine departments, each one a clickable destination.'),
    (91, 15, 'The magazine itself', 'The current issue sits top-right with a subscribe card - the site always pointed back to print.'),
]
_hs_data = urllib.parse.quote(json.dumps([
    {"index": i + 1, "x": x, "y": y, "Title": t, "Message": msg}
    for i, (x, y, t, msg) in enumerate(HOTSPOTS)]), safe='')
_hotspot_module = ('[dfd_hotspot module_animation="transition.fadeIn" marker_background="#c39f76" tooltip_position="dfd-button-tooltip-right" '
    f'tooltip_width="300" image="{M_SPLASH}" box_shadow="box_shadow_enable:enable|shadow_horizontal:0|shadow_vertical:15|shadow_blur:50|'
    'shadow_spread:0|box_shadow_color:rgba(0%2C0%2C0%2C0.15)" title_font_options="font_size:18|color:%23333333|line_height:32|letter_spacing:0" '
    'content_font_options="font_size:14|color:%23202c2d|line_height:18" title_google_fonts="yes" '
    'title_custom_fonts="font_family:Arvo%3Aregular%2Citalic%2C700%2C700italic" '
    f'hotspot_data="{_hs_data}"]')
hero_p1 = re.sub(r'\[vc_single_image image="%d"[^\]]*\]' % M_SPLASH, lambda _: _hotspot_module, hero_p1)
assert 'dfd_hotspot' in hero_p1, 'hero image swap for hotspot failed'

# ---------- hub-and-spoke SVG: the homepage hub, twelve real builds as spokes ----------
def svg_hub():
    spokes = [
        ('IMMERSIVE FEATURE', 'Monthly 3-layer scene'),
        ('MAGAZINE COVER FLIP', 'The subscribe card'),
        ('SECTION FRONTS', 'Stories, Games, Try This'),
        ('BACK TALK', 'Interactive game'),
        ('WHAT IN THE WORLD?', 'Interactive puzzle'),
        ('WILD &amp; WACKY', 'Interactive story'),
        ('BRAINTEASERS', 'Quiz game'),
        ('GREEN-O-METER', 'Educational interactive'),
        ('NG DOG', 'Character animation'),
        ('VIRTUAL PET E-CARDS', 'Send-a-card engine'),
        ('WORDGIRL FILL-INS', 'PBS crossover promo'),
        ('FUNBOOK PROMOS', 'The book range'),
    ]
    import math as _m
    CX, CY, RX, RY = 600, 420, 462, 322
    CW, CH = 196, 62
    parts = [f'<svg viewBox="0 0 1200 840" xmlns="http://www.w3.org/2000/svg" role="img" '
             f'aria-label="Twelve builds Oddtoe designed for National Geographic Kids, radiating from the binocular homepage" '
             f'style="width:100%;height:auto;display:block;">']
    # spokes first (lines under cards)
    pos = []
    for i in range(len(spokes)):
        ang = -_m.pi/2 + i * 2*_m.pi/len(spokes)
        x = CX + RX*_m.cos(ang); y = CY + RY*_m.sin(ang)
        pos.append((x, y))
        parts.append(f'<line x1="{CX + 128*_m.cos(ang):.0f}" y1="{CY + 128*_m.sin(ang):.0f}" x2="{x:.0f}" y2="{y:.0f}" '
                     f'stroke="#f7f7ec" stroke-width="1.8" stroke-dasharray="5 7" opacity="0.9">'
                     f'<animate attributeName="stroke-dashoffset" from="0" to="-48" dur="3s" repeatCount="indefinite"/></line>')
    # hub
    parts.append(f'<circle cx="{CX}" cy="{CY}" r="118" fill="#1f1e29" stroke="#c39f76" stroke-width="2.5"/>')
    parts.append(f'<circle cx="{CX}" cy="{CY}" r="132" fill="none" stroke="#c39f76" stroke-width="1" opacity="0.35" stroke-dasharray="3 7"/>')
    parts.append(f'<text x="{CX}" y="{CY-26}" text-anchor="middle" font-family="{ARVO}" font-size="11" letter-spacing="2.5" fill="#c39f76">NGKIDS.COM</text>')
    parts.append(f'<text x="{CX}" y="{CY+14}" text-anchor="middle" font-family="{BEBAS}" font-size="40" letter-spacing="1" fill="#ffffff">THE HOMEPAGE</text>')
    parts.append(f'<text x="{CX}" y="{CY+44}" text-anchor="middle" font-family="{ARVO}" font-size="12.5" fill="#8a8a95">the binocular front door</text>')
    # spoke cards
    for (title, sub), (x, y) in zip(spokes, pos):
        cx, cy = x - CW/2, y - CH/2
        parts.append(f'<rect x="{cx:.0f}" y="{cy:.0f}" width="{CW}" height="{CH}" rx="10" fill="#262532" stroke="#4a4860" stroke-width="1.5"/>')
        parts.append(f'<text x="{x:.0f}" y="{cy+26:.0f}" text-anchor="middle" font-family="{BEBAS}" font-size="17" letter-spacing="1.2" fill="#ffffff">{title}</text>')
        parts.append(f'<text x="{x:.0f}" y="{cy+46:.0f}" text-anchor="middle" font-family="{ARVO}" font-size="11" fill="#c39f76">{sub}</text>')
    parts.append('</svg>')
    return ''.join(parts)

row_flow = svg_row('Everything hung off one front door', 'One homepage, twelve builds',
    'The hub is the binocular homepage &mdash; the site&rsquo;s playful front door. Around it, the <strong>twelve interactive builds</strong> '
    'Oddtoe designed for <em>National Geographic Kids</em>: the games and puzzles kids played, the monthly immersive scene, the characters, '
    'and the promos that pointed back to print.',
    svg_hub())

# ---------- discovery section (variant 1): the immersive system ----------
sec_discovery = widen_inner(fill(blocks['section1'], {
    'SECTION_C_SUBTITLE': 'A scene, not a banner',
    'SECTION_C_HEADING': 'How did the immersive homepage feature work?',
    'SECTION_C_ANSWER': 'The homepage carried a rolling <strong>immersive feature</strong>: a 738&times;330 scene built in <strong>three animated layers</strong> &mdash; foreground, middleground, background &mdash; so an underwater world or a wolf pack had depth kids could feel. Each edition was a fresh scene composed on the <strong>same layered template</strong>.',
    'SECTION_C_DETAIL': f'The template is the quiet hero. Because every scene decomposed into the same three layers, a new edition meant new artwork, not new engineering &mdash; the design rounds in the archive move from underwater scenes to wolves to outer space on one production system. It is the same character-and-world thinking Oddtoe now sells as {LINK("/character-design-services/", "character design services")} for brands.',
}), '1/4', '1/2')

# ---------- table: the module lineup (oddtoe kit carries a {{TABLE_INTRO}} token) ----------
def oddtoe_table(subtitle, title, intro, heads, rows, footnote):
    body = []
    for r, cells in enumerate(rows):
        bg = '#111111' if r % 2 == 1 else '#000000'
        body.append('<tr>' + ''.join(
            f'<td {vcs_lib._td(bg, bold=(c == 0), nowrap=(c == 0))}>{cell}</td>'
            for c, cell in enumerate(cells)) + '</tr>')
    html = ('<div style="overflow-x: auto;">\n<table style="width: 100%; border-collapse: collapse !important; '
            'background-color: #000000 !important; border: none !important;">\n<thead>\n<tr>'
            + ''.join(f'<th scope="col" {vcs_lib.TH}>{h}</th>' for h in heads)
            + '</tr>\n</thead>\n<tbody>\n' + '\n'.join(body) + '\n</tbody>\n</table>\n</div>'
            + f'\n<p style="text-align: left; font-size: 13px; font-style: italic; color: #8a8a95; margin-top: 10px;">{footnote}</p>')
    guts = f'<p style="text-align: center;"><strong>{intro}</strong></p>\n\n{html}'
    block = fill(blocks['table'], {'TABLE_SUBTITLE': subtitle, 'TABLE_HEADING': title})
    # the kit's text block carries {{TABLE_INTRO}} plus two exemplar tables — replace it wholesale
    block = re.sub(r'\[vc_column_text css=""\].*?\[/vc_column_text\]',
                   lambda _: '[vc_column_text css=""]\n' + guts + '\n[/vc_column_text]',
                   block, count=1, flags=re.S)
    return widen_inner(block, '1/6', '2/3')

t_modules = oddtoe_table('The lineup', 'The interactive modules',
    'Every module was built around one franchise and one verb.',
    ['Module', 'Franchise', 'What kids do'],
    [
        ['Binocular homepage', 'The whole magazine', 'Explore Stories, Games, Sound Off and Try This through the lenses'],
        ['Immersive feature', 'Homepage lead', 'Watch a layered scene animate; click through to the story'],
        ['Back Talk', 'Caption feature', 'Type a thought balloon onto a real animal photo, then print it'],
        ['What in the World?', 'Photo puzzles', 'Unscramble letters while a mystery close-up zooms out'],
        ['Wild &amp; Wacky', 'Fill-in stories', 'Fill fifteen blanks and get an illustrated story back'],
        ['Brainteasers &amp; Green-o-Meter', 'Quizzes', 'Answer questions, get a rank &mdash; refilled by editors via XML'],
        ['Characters &amp; e-cards', 'Mascots', 'Meet the dog, raise the virtual pet, send the cards'],
    ],
    'Alongside these: a magazine-cover animation for the subscribe card, a WordGirl Funny Fill-Ins crossover with PBS, and promotional builds for the book range.')

# ---------- gallery 2x2 ----------
M_F_BACKTALK, M_F_WITW, M_F_WACKY, M_F_BRAIN = 16220, 16221, 16222, 16223  # flat clipped stills (27 Aug)
def small_gal_cell(image_id, title, sub):
    return ('[vc_column_inner el_class="ngk-gal-cell" width="1/3"]'
            f'[dfd_heading enable_delimiter="" style="style_02" heading_margin="margin-bottom:8px;" subtitle="{sub}" '
            'title_font_options="tag:h3|font_size:32|line_height:32" subtitle_font_options="tag:h4|font_size:24|line_height:24"]\n'
            f'<p style="text-align: center;">{title}</p>\n[/dfd_heading]' + SP(8)
            + f'[vc_single_image image="{image_id}" img_size="medium" alignment="center" style="vc_box_rounded" onclick="link_image"]'
            + SP(30, 20) + '[/vc_column_inner]')
GAL_CELLS = [(M_F_BACKTALK, 'Back Talk', 'Type &amp; print'),
             (M_F_WITW, 'What in the World?', 'Unscramble the photo'),
             (M_F_WACKY, 'Wild &amp; Wacky', 'The story payoff')]
row_gallery = (DARKROW + '[vc_column]' + SP(40)
    + HEAD_ROW('The work, up close', 'Play the archive',
               'Three modules as kids saw them &mdash; captured from <strong>the original builds running</strong>, not mock-ups. Click any screen to view it full size.')
    + SP(30)
    + '[vc_row_inner el_class="ngk-gal-row"]' + ''.join(small_gal_cell(*c) for c in GAL_CELLS) + '[/vc_row_inner]'
    + SP(20) + '[/vc_column][/vc_row]')

# ---------- hotspot: read the homepage like a nine-year-old ----------
row_hotspot = hotspot_row('Click the markers', 'Read the homepage like a nine-year-old',
    'Five markers explain what each region of the binocular homepage does for the <strong>kid holding the mouse</strong>.',
    M_SPLASH, [
        (27, 46, 'The featured lens', 'The left lens carries the monthly feature - a new story or activity each issue, framed like something spotted in the wild.'),
        (39, 24, 'Stories', 'The globe takes kids to the story archive - the magazine features, rewritten for the screen.'),
        (74, 28, 'Games', 'The soccer ball opens the games shelf: the puzzles, quizzes and fill-ins on this page.'),
        (88, 52, 'The franchise rail', 'World News, Wild and Wacky, Back Talk, What in the World - the printed magazine departments, each one a clickable destination.'),
        (91, 15, 'The magazine itself', 'The current issue sits top-right with a subscribe card - the site always pointed back to print.'),
    ])

# ---------- big statement + animated immersive ----------
RUFFLE_EMBED = """<div style="max-width:738px;margin:0 auto;border-radius:10px;overflow:hidden;box-shadow:0 12px 34px rgba(0,0,0,0.28);">
<div id="ngk-immersive" style="position:relative;width:100%;padding-top:44.72%;background:#999900;">
<img src="/wp-content/uploads/2026/08/Immersive_Feature_Loaded.png" alt="The National Geographic Kids immersive homepage feature" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;">
</div>
</div>
<script src="/wp-content/uploads/ngk/ruffle/ruffle.js"></script>
<script>
(function(){
  var tries = 0;
  function mount(){
    if (!window.RufflePlayer || !window.RufflePlayer.newest) {
      if (++tries < 40) return setTimeout(mount, 250);
      return; /* Ruffle unavailable: the still stays */
    }
    try {
      var holder = document.getElementById('ngk-immersive');
      var player = window.RufflePlayer.newest().createPlayer();
      player.style.position = 'absolute';
      player.style.inset = '0';
      player.style.width = '100%';
      player.style.height = '100%';
      holder.innerHTML = '';
      holder.appendChild(player);
      player.ruffle().load({url:'/wp-content/uploads/ngk/immersive/home_flash738x330.swf',
        base:'/wp-content/uploads/ngk/immersive/', allowScriptAccess:false,
        autoplay:'on', unmuteOverlay:'hidden', scale:'showAll',
        backgroundColor:'#999900'});
    } catch(e) {}
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
  else mount();
})();
</script>"""

row_big = ('[vc_row bg_check="row-background-dark"]'
    '[vc_column width="1/6"][/vc_column][vc_column width="4/6"]' + SP(40)
    + '[dfd_heading enable_delimiter="" style="style_02" heading_margin="margin-bottom:20px;" subtitle="Three layers deep" '
      'title_font_options="tag:h2|font_size:70|line_height:64" subtitle_font_options="tag:h3|font_size:38|line_height:32"]\n'
      '<p style="text-align: center;">The scene is the welcome mat</p>\n[/dfd_heading]' + SP(20)
    + '[vc_column_text css=""]\n'
      f'{P}The immersive feature &mdash; running here, live, in a Flash emulator: an underwater world painted in three layers behind the welcome banner, with the photo rail racked underneath &mdash; sea lions in the middleground, '
      'the foreground waiting for a click. It never begged for attention &mdash; it made the page feel <strong>inhabited</strong>, the way a good toy shop window does. That restraint is a '
      'design position: motion sells the world, the words sell the click.</p>\n[/vc_column_text]' + SP(20)
    + raw_html(RUFFLE_EMBED)
    + SP(10)
    + '[vc_column_text css=""]\n<p style="text-align: center; font-size: 13px; font-style: italic;">This is the original module running live in your browser &mdash; move around it; the &ldquo;explore&rdquo; button pointed at the old site, so it politely stays put.</p>\n[/vc_column_text]'
    + SP(40) + '[/vc_column][vc_column width="1/6"][/vc_column][/vc_row]')

# ---------- principle tiles ----------
def svg_tiles_desc(aria, tiles):
    """Case-study tiles with multi-line subtext: (TITLE, [sub lines], glyph_kind)."""
    from vcs_lib import glyph
    parts = [f'<svg viewBox="0 0 1200 620" xmlns="http://www.w3.org/2000/svg" role="img" '
             f'aria-label="{aria}" style="width:100%;height:auto;display:block;">']
    for i, (title, subs, kind) in enumerate(tiles):
        x = 40 + (i % 3) * 390
        y = 30 + (i // 3) * 280
        parts.append(f'<rect x="{x}" y="{y}" width="330" height="250" rx="12" fill="#262532" stroke="#4a4860" stroke-width="1.5"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="330" height="4" rx="2" fill="#c39f76"/>')
        parts.append(glyph(kind, x + 165, y + 58))
        parts.append(f'<text x="{x+165}" y="{y+126}" text-anchor="middle" font-family="{BEBAS}" font-size="23" letter-spacing="1.6" fill="#ffffff">{title}</text>')
        for j, line in enumerate(subs):
            parts.append(f'<text x="{x+165}" y="{y+152+j*19}" text-anchor="middle" font-family="{ARVO}" font-size="12.5" fill="#8a8a95">{line}</text>')
    parts.append('</svg>')
    return ''.join(parts)

TILES = [
    ('HOMEPAGE DESIGN &amp; NAVIGATION',
     ['The binocular homepage: navigation as a toy,', 'with Stories, Games, Sound Off and Try This', 'seen through the lenses, not listed in a menu.'],
     'target'),
    ('MONTHLY IMMERSIVE FEATURES',
     ['A rolling homepage scene in three animated', 'layers &mdash; foreground, middleground, background &mdash;', 'a fresh world composed on one template.'],
     'layers'),
    ('GAME &amp; PUZZLE MODULES',
     ['A dozen interactives: caption tools, photo', 'anagrams, fill-in stories, quizzes and character', 'e-cards &mdash; one magazine franchise per module.'],
     'charts'),
    ('CHARACTER &amp; SCENE ILLUSTRATION',
     ['Mascots and layered scene art designed for kids:', 'big silhouettes, instant personality, built to', 'survive small screens and classroom printers.'],
     'people'),
    ('EDITOR-FRIENDLY ENGINES',
     ['Fill-in stories fed by plain text files, quizzes', 'by XML &mdash; editors refreshed every issue', 'without touching a developer.'],
     'grid'),
    ('PRINT-TO-WEB STRATEGY',
     ['Every module carried a printed franchise and', 'pointed back to the magazine &mdash; cover, subscribe', 'card, and a print button on the games themselves.'],
     'doc'),
]
row_tiles = svg_row('What the engagement covered', 'Six workstreams, one site',
    'The <em>National Geographic Kids</em> work ran across six fronts &mdash; each tile is a slice of what shipped.',
    svg_tiles_desc('The six workstreams of Oddtoe&apos;s National Geographic Kids engagement', TILES))

# ---------- deliverables section (variant 2) ----------
sec_deliver = widen_inner(fill(blocks['section2'], {
    'SECTION_D_SUBTITLE': 'Character work, engine work',
    'SECTION_D_HEADING': 'What does this project say about Oddtoe now?',
    'SECTION_D_ANSWER': 'Everything on this page is <strong>character design plus systems thinking</strong>: mascots with personality, worlds with depth, and engines an editorial team could drive without a developer. That combination &mdash; not any single game &mdash; is the deliverable.',
    'SECTION_D_RATIONALE': f'It is also the through-line to the studio&rsquo;s current work. The layered scenes and refillable engines have become {LINK("/what-is-generative-ai-animation/", "generative AI animation")} pipelines; the mascots and side characters have become {LINK("/character-design-services/", "character design services")}; and the instinct that a screen should be a toy runs straight into Oddtoe&rsquo;s {LINK("/brand-activation-ideas/", "brand activations")} for venues and events.',
}), '1/4', '1/2')


# ---------- results stat band (figures from Otto's own record; duration-phrased, date-free) ----------
def svg_stats():
    stats = [
        ('1,500%', ['growth in monthly visitors', 'over four years']),
        ('4,000%', ['growth in monthly page views', 'over the same period']),
        ('916%', ['growth in magazine subscriptions', 'sold through the site']),
    ]
    parts = [f'<svg viewBox="0 0 1200 280" xmlns="http://www.w3.org/2000/svg" role="img" '
             f'aria-label="Traffic and subscription growth while Oddtoe ran the National Geographic Kids site" '
             f'style="width:100%;height:auto;display:block;">']
    for i, (num, subs) in enumerate(stats):
        x = 40 + i * 390
        parts.append(f'<rect x="{x}" y="30" width="330" height="220" rx="12" fill="#262532" stroke="#4a4860" stroke-width="1.5"/>')
        parts.append(f'<rect x="{x}" y="30" width="330" height="4" rx="2" fill="#c39f76"/>')
        parts.append(f'<text x="{x+165}" y="135" text-anchor="middle" font-family="{BEBAS}" font-size="72" fill="#c39f76">{num}</text>')
        for j, line in enumerate(subs):
            parts.append(f'<text x="{x+165}" y="{172+j*22}" text-anchor="middle" font-family="{ARVO}" font-size="13.5" fill="#ffffff">{line}</text>')
    parts.append('</svg>')
    return ''.join(parts)

row_stats = svg_row('The needle, moved', 'What the playable magazine did',
    'Play was the strategy, not the reward. While Oddtoe ran the site&rsquo;s digital side, the audience &mdash; and the magazine behind it &mdash; grew with it.',
    svg_stats())

# ---------- FAQ ----------
faq_pairs = [
    ('What did Oddtoe actually build for National Geographic Kids?',
     'The interactive homepage &mdash; the binocular navigation &mdash; plus the rolling <strong>immersive homepage feature</strong> in three animated layers, and a lineup of game modules: <strong>Back Talk</strong> (caption and print), <strong>What in the World?</strong> (photo anagrams), <strong>Wild &amp; Wacky</strong> (fill-in stories), quiz engines, character e-cards, and promotional builds including a <strong>WordGirl</strong> crossover with PBS.'),
    ('Are the images on this page mock-ups?',
     'No. They are the original builds captured live in a Flash emulator &mdash; the animated frames show the real modules running, including a fill-in story completed end to end.'),
    ('How could the magazine update the games without a developer?',
     'The engines were <strong>refillable</strong>: fill-in stories read from a plain text file, quizzes from an XML file, and the monthly immersive feature ran on a repeatable three-layer template. New issue, new content, same engines.'),
    ('What made the homepage design work for kids?',
     'It behaved like a toy. Navigation lived inside <strong>a pair of binoculars</strong>, franchises were verbs &mdash; type, unscramble, fill in, rate &mdash; and motion was used to make the page feel inhabited rather than to shout. Every module still pointed back to the printed magazine.'),
    ('Does Oddtoe still do this kind of work?',
     'Yes &mdash; the same skills, with a modern pipeline. Character and mascot work runs through <strong>character design services</strong>; layered scene-building now runs through <strong>generative AI animation</strong>; and playable-first thinking drives the studio&rsquo;s experiential and brand-activation projects. Start with the enquiry form on this page.'),
]
faq = faq_row(blocks, 'The National Geographic Kids work', 'Ask about your project', faq_pairs)
faq = faq.replace(vcs_lib.CONTACT, CONTACT)

# ---------- articles ----------
art1 = fill(blocks['article1'], {
    'ARTICLE_1_SUBTITLE': 'Verbs, not pages',
    'ARTICLE_1_HEADING': 'The pig, the balloon, and the print button',
    'ARTICLE_1_BODY': f'''{P}The clearest statement of the whole project is <strong>Back Talk</strong>. A real photograph &mdash; a pig staring into an open fridge &mdash; and one empty thought balloon with the words <strong>TYPE HERE!</strong> The kid supplies the joke, and the punchline of the interface is the button underneath: <strong>PRINT</strong>.</p>
{P}That print button is doing serious work. It turns a web page into a thing a kid makes and takes away &mdash; onto the fridge, into the classroom, next to the magazine it came from. The interactive is not competing with print; it is <strong>feeding it</strong>.</p>
{P}Each franchise got the same treatment: find the one verb a kid wants to do, and build the whole screen around it. What in the World? is <em>unscramble</em>. Wild &amp; Wacky is <em>fill in the blanks</em> &mdash; fifteen of them, rewarded with an illustrated story starring whatever the kid typed. The quizzes are <em>rate yourself</em>, with ranks like &ldquo;Supreme Sea Monster&rdquo; doing the encouragement.</p>
{P}One verb per screen is still how Oddtoe starts an interactive brief, whether the audience is nine or thirty-nine. It is the fastest way to find out whether an idea is an experience or just a layout &mdash; and it is the thinking behind the studio&rsquo;s {LINK("/brand-activation-ideas/", "brand activation")} work today.</p>''',
})
row_cover = ('[vc_row bg_check="row-background-dark" dfd_enable_overlay="" el_class="ngk-quote-row"][vc_column width="1/6"][/vc_column][vc_column width="2/3"]'
    + '[vc_row_inner][vc_column_inner width="1/2"]'
    + '[vc_single_image image="16226" img_size="medium" alignment="center" style="vc_box_shadow_3d" onclick="link_image" css=""]'
    + '[/vc_column_inner][vc_column_inner width="1/2"]'
    + '[new_testimonials main_style="style-1" main_layout="layout-1" image="15762" author="Oddtoe" '
      'subtitle="About the National Geographic Kids years" title_font_options="tag:h4" '
      'subtitle_font_options="tag:div|color:%23f0f0e6" '
      'description="This is really when Oddtoe took off. Comic strips, game design, interactive storytelling &mdash; all at National Geographic. Loved it." '
      'content_font_options="line_height:22" thumb_radius="20" thumb_color="rgba(81,86,52,0.46)"]'
    + '[/vc_column_inner][/vc_row_inner]' + SP(16, 12)
    + '[vc_column_text css=""]\n<p style="text-align: center; font-size: 13px; font-style: italic;">The magazine behind the site: over 1.3 million copies in circulation, a readership in the millions.</p>\n[/vc_column_text]'
    + SP(50, 40)
    + '[/vc_column][vc_column width="1/6"][/vc_column][/vc_row]')

art2 = fill(blocks['article2'], {
    'ARTICLE_2_SUBTITLE': 'From flea circus to front page',
    'ARTICLE_2_HEADING': 'Where the characters came from',
    'ARTICLE_2_BODY': f'''{P}Before and alongside the National Geographic Kids work, Oddtoe was drawing its own characters &mdash; the <strong>Parasite Island</strong> cast and the illustrated portfolio the studio was built on.</p>
{P}Those characters carried into the magazine work: the quiz engine&rsquo;s logo is a cartoon toe &mdash; the studio&rsquo;s namesake &mdash; and original characters run through the games, e-cards and homepage scenes. Oddtoe also drew a <strong>comic strip that ran in the printed magazine</strong> &mdash; a story this site will tell in its own case study.</p>
{P}Characters built for kids have to survive rough handling. They get printed badly, animated at small sizes, and judged in half a second. Designing under those constraints is a discipline, and it is the reason the studio&rsquo;s {LINK("/character-design-services/", "character design services")} start with silhouette and personality before style.</p>
{P}The archive behind this case study &mdash; the layered scenes, the engines, the cast &mdash; is also the seedbed for Oddtoe&rsquo;s own stories, now made with a {LINK("/what-is-generative-ai-animation/", "generative AI animation")} pipeline the original Flash toolkit could only dream about. Same instinct, faster hands.</p>''',
})

# ---------- offers: poach two banners from the Oddtoe homepage ----------
auth = 'Basic ' + base64.b64encode(f"{os.environ['WP_ODDTOE_USER']}:{os.environ['WP_ODDTOE_APP_PASSWORD']}".encode()).decode()
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
r = urllib.request.Request('https://www.oddtoe.com/wp-json/wp/v2/pages/15922?context=edit&nc=ngk', headers={'Authorization': auth, 'User-Agent': UA})
home = json.load(urllib.request.urlopen(r))['content']['raw']
hb = re.findall(r'\[info_banner.*?\[/info_banner\]', home, re.S)
pick = ([b for b in hb if 'A Process for AI Animation' in b] + [b for b in hb if 'Non-Fiction Animator' in b] + hb)[:2]
offers = blocks['offers']
ob = re.findall(r'\[info_banner.*?\[/info_banner\]', offers, re.S)
offers = offers.replace(ob[0], pick[0]).replace(ob[1], pick[1])

# ---------- assemble ----------
page = assemble([hero_p1, row_flow, row_secB, sec_discovery, t_modules, row_gallery,
                 row_big, row_tiles, sec_deliver, row_stats, faq, art1, row_cover, offers, art2, blocks['form']])

# Heading delimiters (Otto, 28 Aug): a hint of a graphic under each section heading,
# before the body text — a short dotted sand rule, centred.
HINT = ('[vc_column_text css=""]\n<div style="width: 64px; margin: 6px auto 0; border-bottom: 2px dotted #ddccb1;"></div>\n[/vc_column_text]')
page, n_hints = re.subn(r'(\[dfd_heading[^\]]*font_size:70[^\]]*\].*?\[/dfd_heading\])',
                        lambda m: m.group(1) + HINT, page, flags=re.S)
assert n_hints >= 11, f'expected hints under all section headings, got {n_hints}'
print('heading hints inserted:', n_hints)

# Oddtoe accent: VCS helpers emit Datalabs tan — retarget to sand.
page = page.replace('#c39f76', SAND).replace('%23c39f76', urllib.parse.quote(SAND, safe=''))
# Tint: hero overlay + vcs panel shades derive from the page ground (ink).
page = page.replace(f'dfd_overlay_color="{KIT_PLUM}"', f'dfd_overlay_color="{TINT}"')
page = vcs_lib.apply_theme(page, TINT)
# ---------- DARK TEXT MODE (Otto, 27 Aug: try dark lettering on the NGK green) ----------
# The theme colours text per-row from bg_check: "row-background-dark" renders class
# dfd-background-dark (light text). Emptying the check gives the theme's default dark
# lettering. SVGs keep black panels (matching the tables) so their internals stay light.
DARK_TEXT = True
MUTED = '#4f4f1f'
if DARK_TEXT:
    page = page.replace('bg_check="row-background-dark"', 'bg_check=""')
    page = page.replace('bg_check="column-background-dark"', 'bg_check=""')
    page = page.replace('color: #8a8a95;', f'color: {MUTED};')  # table footnote on the green
    def _restyle_svg(m):
        html = urllib.parse.unquote(base64.b64decode(m.group(1)).decode())
        if not html.startswith('<svg'):
            return m.group(0)
        html = (html.replace('#262532', '#000000')   # panel cards -> black, like the tables
                    .replace('#1f1e29', '#000000')   # hub circle
                    .replace('#4a4860', '#33331a')   # card strokes + dim bars -> dark olive
                    .replace('#8a8a95', '#b3b384'))  # card sub-text -> olive-grey on black
        return '[vc_raw_html]' + base64.b64encode(urllib.parse.quote(html, safe='').encode()).decode() + '[/vc_raw_html]'
    page = re.sub(r'\[vc_raw_html\]([^\[]+)\[/vc_raw_html\]', _restyle_svg, page)
    # Quigley subtitles wash out in dark-text mode (Otto, 27 Aug): force a very light grey
    SUBTITLE_GREY = '%23f0f0e6'
    # the offers delimiter ("More from the Oddtoe studio...") is Qwigley too — same light grey
    page = page.replace('title_font_options="font_size:30|line_height:38"',
                        f'title_font_options="font_size:30|line_height:38|color:{"%23f0f0e6"}"')
    # ...and the plain dotted line closing that section: the theme's with-line renderer
    # dims whatever colour it gets, so draw the rule ourselves (matches the with-text flanks)
    page = re.sub(r'\[dfd_delimiter delimiter_style="dfd-delimiter-with-line"[^\]]*\]',
                  '[vc_column_text css=""]\n<div style="border-bottom: 1px dotted #f0f0e6;"></div>\n[/vc_column_text]', page)
    page = re.sub(r'subtitle_font_options="([^"]*)"',
                  lambda m: m.group(0) if 'color' in m.group(1)
                  else f'subtitle_font_options="{m.group(1)}|color:{SUBTITLE_GREY}"', page)
    # Body + link colours for the olive ground (Otto, 27 Aug): body in Oddtoe plum-ink
    # (red-violet counterweight to the yellow-green ground); links light like the
    # subtitles with a sand underline, inverting to plum on hover. Page-scoped CSS —
    # inline colours would kill the theme hover (kit rule), and the site-wide Ronneby
    # link options (tan/olive) disappear against this background.
    PAGE_CSS = '''<style>
body.page-id-16219 .vc_row p,
body.page-id-16219 .vc_row li,
body.page-id-16219 .vc_row .dfd-info-box .content-wrap { color: #26161f; }
body.page-id-16219 .vc_row .dfd-heading p { color: inherit; }
body.page-id-16219 .ngk-quote-row { margin-top: -60px; }
body.page-id-16219 .dfd-info-banner .delimiter,
body.page-id-16219 .dfd-info-banner .delimiter * ,
body.page-id-16219 .dfd-delimiter-with-line .line,
body.page-id-16219 .dfd-delimiter-with-text .line { outline-color: rgba(240,240,230,0.55) !important; border-color: rgba(240,240,230,0.55) !important; }
body.page-id-16219 .ngk-quote-row .wpb_single_image { margin-bottom: 0; }
body.page-id-16219 .ngk-gal-row > .row { display: flex; justify-content: center; flex-wrap: wrap; gap: 28px; }
body.page-id-16219 .ngk-gal-row .ngk-gal-cell { width: auto; min-width: 0; float: none; padding-left: 0; padding-right: 0; }
body.page-id-16219 .vc_tta-panel .vc_tta-panel-title > a,
body.page-id-16219 .vc_tta-panel .vc_tta-panel-title > a:hover,
body.page-id-16219 .vc_tta-panel .vc_tta-title-text { color: #26161f !important; }
body.page-id-16219 .vc_tta-panel .vc_tta-controls-icon::before,
body.page-id-16219 .vc_tta-panel .vc_tta-controls-icon::after { border-color: #26161f !important; }
body.page-id-16219 .vc_tta-panel .vc_tta-panel-body,
body.page-id-16219 .vc_tta-panel .vc_tta-panel-body p { color: #26161f; }
body.page-id-16219 .vc_tta-panel .vc_tta-panel-heading { border-color: #7d7d00 !important; }
body.page-id-16219 .vc_row a.dfd-custom-link-decorated,
body.page-id-16219 .vc_row a.dfd-custom-link-decorated strong,
body.page-id-16219 .vc_row strong a.dfd-custom-link-decorated {
  color: #f7f7ec !important;
  border-bottom: 1px dotted #ddccb1;
  background-image: none !important;
}
body.page-id-16219 .vc_row a.dfd-custom-link-decorated:hover,
body.page-id-16219 .vc_row strong a.dfd-custom-link-decorated:hover {
  color: #26161f !important;
  border-bottom: 1px solid #26161f;
}
</style>'''
    page = page + '[vc_row][vc_column]' + raw_html(PAGE_CSS) + '[/vc_column][/vc_row]'

# Animated GIFs must render the original file, not a resized (static) thumbnail.
for mid in ANIMATED:
    page = page.replace(f'image="{mid}" img_size="large"', f'image="{mid}" img_size="full"')
assert f'image="{M_SPLASH}"' in page  # the splash lives in the hero hotspot now
assert page.count('dfd_hotspot') == 1 and page.count('<table') == 1

OUT.write_text(page)
print('composed chars:', len(page), '| images:', page.count('vc_single_image'),
      '| svg rows:', page.count('<svg'), '| sand accents:', page.count(SAND))

# ---------- create the draft ----------
body = {'title': 'National Geographic Kids, Made Playable', 'content': page, 'status': 'publish',
        'slug': 'national-geographic-kids-case-study', 'template': 'page-custom.php'}
if os.environ.get('WP_ODDTOE_AUTHOR_ID'):
    body['author'] = int(os.environ['WP_ODDTOE_AUTHOR_ID'])
req = urllib.request.Request('https://www.oddtoe.com/wp-json/wp/v2/pages/16219',
    data=json.dumps(body).encode(),
    headers={'Content-Type': 'application/json', 'Authorization': auth, 'User-Agent': UA},
    method='POST')
with urllib.request.urlopen(req) as r:
    d = json.load(r)
print('WP draft updated:', d['id'], '| slug:', d['slug'], '| status:', d['status'])
print('Review:', f"https://www.oddtoe.com/wp-admin/post.php?post={d['id']}&action=edit")
print('\nSET IN WP-ADMIN: Page Options > Background color =', TINT, '(ink) + repeat + header style 6')
print('YOAST TITLE: National Geographic Kids Case Study — Interactive Design by Oddtoe')
print('YOAST DESC: How Oddtoe turned National Geographic Kids into a playable website: the binocular homepage, layered immersive scenes, and a dozen game modules — shown running.')
