#!/usr/bin/env python3
# Compose the Oddtoe "Puppet Designer" page on the Installation Artist (11178) / Mascot
# Designer (16255) template — the 14-row Artist & Designer shape.
# Output: puppet-designer.html  (WPBakery raw body, ready for wp-post.sh)
#
# COMMISSIONED: Otto, 14 Sep 2026. He trained under Christopher Piper at The Puppet Co.,
#   Glen Echo Park, Maryland, in 2004, learning to build and string marionettes. He cleared
#   naming The Puppet Co. and Piper (14 Sep 2026). Source: his own 2004 nonfiction pieces and
#   the Piper interview, inventoried in
#   'Oddtoe New Growth Pages 2026/puppetry-page-source-inventory-2026-09-14.md'.
#
# TINT: #2d271d — the hero's bottom edge (#978563) composited under the row's 70% black
#   overlay, so the page ground blends out of the hero. Overlay is 70 rather than the usual
#   50 precisely to land the ground dark enough; at 50 it renders #4b4231, a mid-brown page.
#   Distinct from Sculptor umber #241b16 and Installation Artist plum #2f2e3a in this cluster.
#   Table cells composed for this ground: even #000000, odd #0d0b08, hairline #4a4034.
#
# IMAGERY: hero 16348 and carousel slide 16349 are Otto's own marionette renders, uploaded
#   14 Sep 2026 by upload-oddtoe-puppet-media.py. The rest of the carousel is existing site
#   media: 12662 (trilobite shadow puppet), and the carried-head construction details
#   16282/16286/16284/16283/16281 from the publicity stunts page.
#
# CAPABILITY PAGE, NOT PORTFOLIO. Oddtoe has designed carried heads and built the baobab;
#   there is no catalogue of delivered puppet commissions. No invented projects or clients.
#   The Glen Echo training is a credential, written as training, not as a client project.
#
# Portfolio trio carried over from the Mascot Designer page (16154 Babbling with Baobabs —
#   a built character operated live, the closest thing to puppetry in the library). Flagged
#   in the handoff for Otto to swap.
import base64, urllib.parse, io, os, json, re, pathlib

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "puppet-designer.html")

SP = ('[dfd_spacer screen_wide_resolution="1280" screen_wide_spacer_size="{w}" screen_normal_resolution="1024" '
      'screen_tablet_resolution="800" screen_mobile_resolution="480" screen_normal_spacer_size="{n}" '
      'screen_tablet_spacer_size="{t}" screen_mobile_spacer_size="{m}"]')
def sp(w, n=None, t=None, m=None):
    n = w if n is None else n; t = n if t is None else t; m = t if m is None else m
    return SP.format(w=w, n=n, t=t, m=m)

ARVO = '<span style="font-family: Arvo;">{}</span>'
def link(url, label):
    return f'<strong><a class="dfd-custom-link-decorated" href="{url}">{label}</a></strong>'

def plain(t):
    return re.sub(r"<[^>]+>", "", t).replace("&#8217;", "’").replace("&#8226;", "•")

CANONICAL = ("<strong>Oddtoe</strong> is an experiential design and generative-AI animation studio based in Melbourne, "
             "creating projection, installation, and animated work for events, venues, and galleries.")

# NOTE: no pricing figure and no market statistic here. Neither is verified for puppetry.
FAQ = [
 ("What does a puppet designer actually do?",
  "A <strong>puppet designer</strong> settles two things at once: <strong>what the character is</strong>, and "
  "<strong>how a person is going to work it</strong>. That means the face, and it means where the joints go, where "
  "the strings or rods attach, how much it weighs, and how long someone can hold it up."),
 ("What kinds of puppets does Oddtoe design?",
  "<strong>Marionettes</strong> on strings, <strong>rod and carried puppets</strong> held up on poles, "
  "<strong>oversized heads</strong> worn or carried at street level, <strong>shadow puppets</strong>, and characters "
  "puppeteered on screen through projection and animation."),
 ("Do you build the puppet as well as design it?",
  "Some of it. Small carried and rod work is built in the studio; larger runs and worn costumes go to "
  "<strong>a specialist maker</strong>, working from the design package. The design is drawn in "
  "<strong>Melbourne</strong> and the build happens wherever the job needs it, which sometimes means a fabricator "
  "near you rather than freight."),
 ("What is the difference between a marionette and a rod puppet?",
  "A <strong>marionette</strong> hangs on strings from a control bar above, so gravity does most of the acting and "
  "the puppeteer works from above. A <strong>rod puppet</strong> is held up from below or behind on poles, which is "
  "stronger, faster, and much better outdoors. Crowd and street work is nearly always rod or carried."),
 ("Can a puppet be used outdoors and at a festival?",
  "Yes, and it changes the design. Outdoor work has to survive <strong>wind, rain and being bumped</strong>, has to "
  "be carried by someone for a whole shift, and has to come apart to travel. Those constraints get settled early, "
  "because retro-fitting a stage puppet for a street is usually a rebuild."),
 ("How long does a puppet take?",
  "Design runs <strong>two to three weeks</strong> for a single character. Build depends entirely on what it is and "
  "who makes it. Send the brief with the date it has to appear and you get a schedule with the build quoted "
  "separately."),
 ("How much does a custom puppet cost?",
  "<strong>Oddtoe</strong> does not publish prices, because the cost of a puppet is decided by its size, how "
  "articulated it is, and how many of them there are. Send what it has to do and where it appears and you get a "
  f"quote. The build side is set out on {link('https://www.oddtoe.com/prop-fabrication-services/', 'prop fabrication services')}."),
 ("Where is Oddtoe based?",
  "<strong>Oddtoe</strong> is based in <strong>Melbourne, Australia</strong>. Supplier and business contacts run "
  "through <strong>Berlin and Los Angeles</strong>, and those are the starting points for work in Europe and the "
  "United States."),
]

PAGE_STYLES = '[vc_raw_html]JTNDc3R5bGUlM0UlMjNoZXJvJTIwLmRmZC1yb3ctYmctY2FudmFzJTdCYmFja2dyb3VuZC1wb3NpdGlvbiUzQWNlbnRlciUyMGNlbnRlciUyMCUyMWltcG9ydGFudCU3RCU0MG1lZGlhJTIwJTI4bWluLXdpZHRoJTNBODAwcHglMjklN0IudmNfaW5uZXIlMjAuY29sdW1ucy50aHJlZSU3QnBhZGRpbmctbGVmdCUzQTIwcHglMjAlMjFpbXBvcnRhbnQlM0JwYWRkaW5nLXJpZ2h0JTNBMjBweCUyMCUyMWltcG9ydGFudCU3RCU3RCUzQyUyRnN0eWxlJTNF[/vc_raw_html]'

rows = []

# 1. HERO ---------------------------------- canvas 16362 (own render, 1920px JPEG of 16348)
#    16348 is the 2048px PNG master at 7.7 MB — far too heavy for a hero. 16362 is the same
#    image resized to 1920 and saved as JPEG at quality 82 (1.1 MB), uploaded 14 Sep 2026.
rows.append(
 '[vc_row bg_check="row-background-dark" dfd_bg_style="canvas" dfd_bg_image_canvas="16362" '
 'dfd_bg_image_repeat_canvas="no-repeat" dfd_overlay_color="#000000" dfd_overlay_pattern="transperant" '
 'dfd_overlay_pattern_opacity="70" dfd_row_config="full_width_content" dfd_bg_color_value="#2d271d" '
 'anchor="hero"][vc_column]' + PAGE_STYLES
 + sp(520, 520, 340, 270) +
 '[dfd_heading enable_delimiter="" style="style_02" subtitle="Characters a person has to work" '
 'title_font_options="tag:h1|font_family:BebasNeueRegular|letter_spacing:0" '
 'subtitle_font_options="tag:h2|line_height:20" heading_margin="margin-bottom:10px;" '
 'subheading_margin="margin-bottom:10px;"]Puppet Designer[/dfd_heading]'
 + sp(700, 580, 480, 430) +
 '[/vc_column][/vc_row]')

# 2. INTRO --------------------------------------------------------------------
intro_a = ARVO.format(
  f'{CANONICAL} As a <strong>puppet designer</strong>, I design characters that somebody operates &#8212; '
  'on strings, on a pole, or worn &#8212; and the mechanics that let them do it. That covers a stage puppet, a head '
  'carried through a street, and a character worked on a screen.')
intro_b = ARVO.format(
  'Every puppet is <strong>a machine and a face at the same time</strong>. Where a joint sits and where a string '
  'attaches decide what the character can do, and those get settled while the drawing is still open. I learned that '
  'part by <strong>building and stringing marionettes</strong>, and it still decides where I start. See '
  f'{link("https://www.oddtoe.com/artist-designer/mascot-designer/", "mascot design")} for characters with a person '
  f'inside, or {link("https://www.oddtoe.com/artist-designer/character-designer/", "character design")} for the '
  'artwork side.')

rows.append(
 '[vc_row bg_check="row-background-dark"][vc_column]' + sp(80) +
 '[dfd_heading style="style_02" subtitle="Marionettes, rod puppets, carried heads, and shadow work" '
 'title_font_options="tag:h2|font_family:BebasNeueRegular|letter_spacing:0" '
 'subtitle_font_options="tag:h3|font_family:QwigleyRegular" '
 'heading_margin="margin-bottom:10px;"]Puppet Design &amp; Puppet Making[/dfd_heading]'
 + sp(14, 14, 12, 10) +
 '[vc_column_text css=""]</p>\n'
 '<p style="text-align: center;"><span style="font-family: Arvo; font-size: 13px; '
 'color: #8a8a95;">Updated September 2026</span></p>\n'
 '<p>[/vc_column_text]'
 + sp(20, 20, 15, 10) +
 '[vc_row_inner][vc_column_inner width="1/4"][/vc_column_inner][vc_column_inner width="1/4"]'
 f'[vc_column_text css=""]{intro_a}[/vc_column_text]' + sp(20) +
 '[/vc_column_inner][vc_column_inner width="1/4"]'
 f'[vc_column_text]{intro_b}[/vc_column_text]' + sp(20) +
 '[/vc_column_inner][vc_column_inner width="1/4"][/vc_column_inner][/vc_row_inner]'
 + sp(80, 80, 70, 60) + '[/vc_column][/vc_row]')

# 3. SECTION HEAD -------------------------------------------------------------
rows.append(
 '[vc_row bg_check="row-background-dark" dfd_row_responsive_enable="dfd-row-responsive-enable" '
 'responsive_styles="padding_left_mobile:10|padding_right_mobile:10"][vc_column]' + sp(60, 60, 50, 40) +
 '[dfd_heading module_animation="transition.swoopIn" enable_delimiter="" style="style_02" '
 'title_font_options="tag:h2|font_family:BebasNeueRegular" '
 'subtitle_font_options="tag:h3|font_family:QwigleyRegular" '
 'subtitle="Puppet design, puppet making, and the mechanics underneath" '
 'heading_margin="margin-bottom:10px;"]Puppet Designer &amp; Puppet Maker[/dfd_heading]'
 + sp(10) + '[/vc_column][/vc_row]')

# 4. CAROUSEL -----------------------------------------------------------------
CAROUSEL = [12662,  # trilobite shadow puppet — own work, already live
            16285,  # padded shoulder yoke with a timber pole socketed in
            16286,  # hand working a control rod linked to a hinged jaw
            16284,  # head mounted on a single vertical support pole
            16283,  # woven mesh sight panel set into the chin
            16273,  # hand-drawn construction studies with proportion grids
            16263]  # a family of worn costume characters
imgs = ''.join(f'[dfd_single_image image="{i}" image_size="custom" image_width="250" image_height="250" '
               f'image_border_radius="10"]' for i in CAROUSEL)
rows.append(
 '[vc_row dfd_enable_overlay="" anchor="work"][vc_column]' + sp(20) +
 '[dfd_carousel center_mode="on" center_mode_scale="on" adaptive_height="" module_animation="transition.fadeIn" '
 'slides_to_show="3" screen_normal_resolution="1024" screen_normal_slides="3" screen_tablet_resolution="800" '
 'screen_tablet_slides="3" screen_mobile_resolution="480" slider_type="horizontal" dots_style="dfdfillrounded" '
 'dots_color="#000000" arrows_position="aside2" arrows_style="style_3" arrows_bg="#252525"]'
 + imgs + '[/dfd_carousel]' + sp(60, 40, 30, 40) + '[/vc_column][/vc_row]')

# ---------------------------------------------------------------------------
# Three-up image row. Structure lifted from the Use Case kit's "drawings" row
# (Otto's art direction, live on 16272): 640x480 rounded image, a small Arvo 700
# step label in olive, a 30px Bebas h3, then body copy.
# ---------------------------------------------------------------------------
def three_up(heading, subtitle, intro, items, anchor=None):
    def cell(image_id, step, title, body):
        return ('[vc_column_inner width="1/3"]'
          f'[vc_single_image image="{image_id}" img_size="640x480" style="vc_box_rounded" css=""]'
          + sp(22, 22, 16, 16) +
          '[dfd_heading content_alignment="text-left" enable_delimiter="" subtitle_google_fonts="yes" '
          'subtitle_custom_fonts="font_family:Arvo%3A700|font_style:700%20bold%20regular%3A700%3Anormal" '
          f'style="style_02" subtitle="{step}" '
          'title_font_options="tag:h3|font_size:30|font_family:BebasNeueRegular|line_height:30|letter_spacing:0" '
          'subtitle_font_options="tag:div|font_size:12|line_height:16|color:%238a9f6a|letter_spacing:1" '
          f'heading_margin="margin-bottom:12px;" subheading_margin="margin-bottom:6px;"]{title}[/dfd_heading]'
          f'[vc_column_text css=""]{body}[/vc_column_text]'
          + sp(40, 40, 30, 30) + '[/vc_column_inner]')

    attrs = ['bg_check="row-background-dark"', 'dfd_enable_overlay=""']
    if anchor: attrs.append(f'anchor="{anchor}"')
    attrs += ['dfd_row_responsive_enable="dfd-row-responsive-enable"',
              'responsive_styles="padding_left_mobile:10|padding_right_mobile:10"']
    return ('[vc_row ' + ' '.join(attrs) + '][vc_column]' + sp(70, 70, 50, 40) +
      '[dfd_heading style="style_02" '
      'title_font_options="tag:h2|font_size:90|font_family:BebasNeueRegular|line_height:84|letter_spacing:0" '
      'title_responsive="font_size_tablet:66|line_height_tablet:62|font_size_mobile:44|line_height_mobile:42" '
      'subtitle_font_options="tag:h3|font_size:40|font_family:QwigleyRegular" '
      f'subtitle="{subtitle}" heading_margin="margin-bottom:10px;"]{heading}[/dfd_heading]'
      + sp(16, 16, 14, 12) +
      '[vc_row_inner][vc_column_inner width="1/6"][/vc_column_inner][vc_column_inner width="2/3"]'
      f'[vc_column_text css=""]{intro}[/vc_column_text]'
      '[/vc_column_inner][vc_column_inner width="1/6"][/vc_column_inner][/vc_row_inner]'
      + sp(34, 34, 26, 22) +
      '[vc_row_inner]' + ''.join(cell(*it) for it in items) + '[/vc_row_inner]'
      + sp(30, 30, 20, 20) + '[/vc_column][/vc_row]')


# ---------------------------------------------------------------------------
# Six-step timeline. The whole interactive block (CSS + markup + JS) is lifted
# from the Use Case kit's "the-day" row and refilled. The kit stores raw blocks
# decoded between <!--RAW--> markers; WPBakery wants rawurlencode-then-base64,
# which is what enc() below does — same convention as compose_usecase_lib.
# ---------------------------------------------------------------------------
KIT = pathlib.Path(__file__).resolve().parents[1] / 'references/design-kit-oddtoe-usecase.html'
SAFE = "!*'()"
def enc(x):
    return base64.b64encode(urllib.parse.quote(x, safe=SAFE).encode()).decode()

def timeline(tokens):
    kit_rows = re.split(r'(?=\[vc_row )', KIT.read_text(encoding='utf-8'))
    row = next(r for r in kit_rows if 'anchor="the-day"' in r)
    row = row.split('[/vc_row]')[0] + '[/vc_row]'
    row = re.sub(r'\{\{([A-Z0-9_]+)\}\}', lambda m: tokens[m.group(1)], row)
    row = re.sub(r'<!--(?!RAW-->|/RAW-->).*?-->\n?', '', row, flags=re.S)
    row = re.sub(r'<!--RAW-->(.*?)<!--/RAW-->', lambda m: enc(m.group(1)), row, flags=re.S)
    assert '{{' not in row, 'unfilled timeline token: ' + (re.search(r'{{[^}]+}}', row) or [''])[0]
    assert '<!--' not in row, 'a comment survived in the timeline row'
    return row


def qsection(heading, subtitle, col_a, col_b, anchor=None, one_page=None, parallax=False, top=60):
    attrs = ['bg_check="row-background-dark"', 'dfd_enable_overlay=""', 'dfd_row_config="default_row_small_paddings"']
    if one_page: attrs.append(f'one_page_title="{one_page}"')
    if anchor: attrs.append(f'anchor="{anchor}"')
    if parallax: attrs.append('dfd_row_parallax="dfd-row-parallax"')
    attrs.append('dfd_row_responsive_enable="dfd-row-responsive-enable"')
    attrs.append('responsive_styles="padding_left_mobile:10|padding_right_mobile:10"')
    return ('[vc_row ' + ' '.join(attrs) + '][vc_column]' + sp(top, top, 50, 40) +
      '[dfd_heading enable_delimiter="" style="style_02" '
      'title_font_options="tag:h2|font_family:BebasNeueRegular|letter_spacing:0" '
      'subtitle_font_options="tag:h3|font_family:QwigleyRegular" '
      f'subtitle="{subtitle}" heading_margin="margin-bottom:10px;"]'
      f'{heading}[/dfd_heading]' + sp(20) +
      '[vc_row_inner][vc_column_inner width="1/4"][/vc_column_inner][vc_column_inner width="1/4"]'
      f'[vc_column_text css=""]{col_a}[/vc_column_text][/vc_column_inner][vc_column_inner width="1/4"]'
      f'[vc_column_text css=""]{col_b}[/vc_column_text][/vc_column_inner]'
      '[vc_column_inner width="1/4"][/vc_column_inner][/vc_row_inner]' + sp(40, 40, 30, 30) +
      '[/vc_column][/vc_row]')

# 5. What does a puppet designer do -------------------------------------------
rows.append(qsection(
  "What Does a Puppet Designer Do?",
  "The character, and the mechanics under it",
  ARVO.format(
    'A puppet designer decides <strong>who the character is</strong> and <strong>how a person works it</strong>. '
    'Those are the same decision. A jaw that opens changes the face; a hand that has to hold a pole at head height '
    'for two hours changes the weight, and the weight changes the whole build.') + '\n\n' + ARVO.format(
    'Get the order wrong and you end up with a beautiful drawing nobody can operate.'),
  ARVO.format(
    'So the mechanics come in early: <strong>where the joints go</strong>, where the strings or rods attach, how the '
    'head is carried, how the puppeteer sees out, and how the whole thing comes apart to travel.') + '\n\n' + ARVO.format(
    'The visible half is the character. The half that decides whether it works is underneath. Related practices often '
    f'land in the same commission &#8212; {link("https://www.oddtoe.com/artist-designer/prop-designer-maker/", "prop making")} '
    f'and {link("https://www.oddtoe.com/artist-designer/roboticist/", "animatronics")}.'),
  anchor="what", one_page="What?", parallax=True))

# 6. What goes into one --------------------------------------------------------
rows.append(qsection(
  "What Goes Into an Oddtoe Puppet Design?",
  "A character, a mechanism, and a set of drawings someone can build from",
  ARVO.format(
    'A <strong>character definition</strong>, a <strong>3D model</strong> seen from every angle, a '
    '<strong>mechanism</strong> worked out against a human body, and <strong>drawings a maker can build from</strong>.') +
  '\n\n' + ARVO.format('The forms this ends up in each have their own page:') + '\n\n' + ARVO.format(
    f'&#8226; {link("https://www.oddtoe.com/artist-designer/mascot-designer/", "Worn characters and mascots")}<br />'
    f'&#8226; {link("https://www.oddtoe.com/artist-designer/inflatable-artist/", "Giant inflatables and walk-in structures")}<br />'
    f'&#8226; {link("https://www.oddtoe.com/artist-designer/prop-designer-maker/", "Props and fabricated objects")}<br />'
    f'&#8226; {link("https://www.oddtoe.com/artist-designer/projection-artist/", "Projection and screen work")}'),
  ARVO.format(
    'Everything is <strong>designed in 3D</strong>, which means the character is animated and seen moving before '
    'anything is cut. You watch the walk, the turn and the jaw before committing to a build.') +
  '\n\n' + ARVO.format(
    'The same model then does the other jobs: the renders that get the piece approved, the '
    f'{link("https://www.oddtoe.com/what-is-generative-ai-animation/", "animated content")} it appears in, and a '
    'larger version of the character later if the job grows.')))

# 6b. THREE-UP IMAGE ROW — the visual lead-in to the comparison table below.
#     Added 14 Sep 2026 on Otto's note that the page read as unvisual.
rows.append(three_up(
  "Three Kinds of Puppet",
  "One word, three different objects",
  ARVO.format('Most briefs arrive asking for <strong>a puppet</strong>. Almost always it is one of these three, '
              'and which one is decided by where it appears and who has to work it.'),
  [(16349, "ON STRINGS", "Marionette",
    ARVO.format('Hung from <strong>a control bar above</strong> and worked from a bridge or a ladder. Gravity does '
                'a lot of the acting, which is why a marionette moves the way nothing else does. It suits a stage '
                'and an audience sitting close.')),
   (16281, "ON POLES", "Rod &amp; Carried",
    ARVO.format('Held up <strong>from below or behind</strong>. Stronger, faster, and far better outdoors, so nearly '
                'everything built for a street, a parade or a festival is rod or carried. Height is the point: it has '
                'to be seen over a crowd.')),
   (16264, "WORN", "Worn Character",
    ARVO.format('<strong>A performer inside the character</strong>, shaking hands and being photographed. The design '
                'problem moves to sightlines, weight and ventilation. Oddtoe designs these and '
                f'{link("https://www.oddtoe.com/artist-designer/mascot-designer/", "a specialist maker builds them")}.'))],
  anchor="kinds"))

# 7. COMPARISON TABLE ----------------------------------------------------------
TH = ('padding: 14px 18px; text-align: left; background-color: #000000 !important; border: none !important; '
      'border-bottom: 2px solid #ddccb1 !important; font-family: \'Bebas Neue\', sans-serif; font-size: 21px; '
      'font-weight: normal; letter-spacing: 1px; color: #ffffff !important;')
def td(bg):
    return (f'padding: 12px 18px; text-align: left; background-color: {bg} !important; border: none !important; '
            f'border-bottom: 1px solid #4a4034 !important; color: #ffffff !important;')

TABLE_ROWS = [
 ("How it is worked",
  "Strings from a control bar above",
  "Poles from below or behind",
  "A performer wearing the character"),
 ("Where it suits",
  "Indoors, close up, on a stage",
  "Streets, festivals, parades, crowds",
  "Match days, store openings, expos"),
 ("What it is good at",
  "Fine, strange, floating movement",
  "Height, speed, and standing up to weather",
  "Handshakes, photos, direct contact"),
 ("Puppeteer visible?",
  "Hidden above, or in view by choice",
  "In view, usually dressed as part of it",
  "Fully inside the character"),
 ("Takes to travel",
  "Tangles; needs a case and a rack",
  "Comes apart into poles and a body",
  "Packs into a costume case"),
 ("What Oddtoe delivers",
  "Character, mechanism, stringing plan",
  "Character, 3D model, build drawings",
  "Character, 3D model, maker-ready spec"),
]
tbody = ''
for i, (crit, a, b, c) in enumerate(TABLE_ROWS):
    bg = '#000000' if i % 2 == 0 else '#0d0b08'
    tbody += (f'<tr><td style="{td(bg)}"><strong>{crit}</strong></td>'
              f'<td style="{td(bg)}">{a}</td><td style="{td(bg)}">{b}</td><td style="{td(bg)}">{c}</td></tr>\n')

table_html = (
 '<div style="overflow-x: auto;">\n'
 '<table style="width: 100%; border-collapse: collapse !important; background-color: #000000 !important; border: none !important;">\n'
 '<thead>\n<tr>'
 f'<th scope="col" style="{TH} white-space: nowrap;">&nbsp;</th>'
 f'<th scope="col" style="{TH}">Marionette</th>'
 f'<th scope="col" style="{TH}">Rod or carried puppet</th>'
 f'<th scope="col" style="{TH}">Worn character</th>'
 '</tr>\n</thead>\n<tbody>\n' + tbody + '</tbody>\n</table>\n</div>')

rows.append(
 '[vc_row bg_check="row-background-dark" dfd_enable_overlay="" dfd_row_responsive_enable="dfd-row-responsive-enable" '
 'responsive_styles="padding_left_mobile:10|padding_right_mobile:10"][vc_column]' + sp(60, 60, 50, 40) +
 '[dfd_heading enable_delimiter="" style="style_02" '
 'title_font_options="tag:h2|font_family:BebasNeueRegular|letter_spacing:0" '
 'subtitle_font_options="tag:h3|font_family:QwigleyRegular" '
 'subtitle="Which one does your job need?" heading_margin="margin-bottom:10px;"]'
 'Marionette, Rod Puppet, or Worn Character?[/dfd_heading]' + sp(20) +
 '[vc_row_inner][vc_column_inner width="1/6"][/vc_column_inner][vc_column_inner width="2/3"][vc_column_text css=""]'
 + ARVO.format('Most briefs arrive asking for <strong>a puppet</strong>. Which of these three it turns out to be is '
               'decided by where it appears and who has to work it.')
 + '\n\n' + table_html +
 '[/vc_column_text][/vc_column_inner][vc_column_inner width="1/6"][/vc_column_inner][/vc_row_inner]'
 + sp(60, 60, 40, 40) + '[/vc_column][/vc_row]')

# 8. Who commissions -----------------------------------------------------------
rows.append(qsection(
  "Who Commissions a Puppet Designer?",
  "Theatres, festivals, campaigns, and screens",
  ARVO.format(
    'Theatre companies, festivals, campaign organisers, museums, brands, and producers. The craft is the same each '
    'time. What changes is <strong>how close the audience gets</strong>.') + '\n\n' + ARVO.format(
    '<strong>Theatre and children&#8217;s programs</strong> commission characters for a stage, where the audience is '
    'near and small movements read.') + '\n\n' + ARVO.format(
    '<strong>Festivals and parades</strong> commission carried and rod work, built tall enough to be seen over a '
    'crowd and tough enough for a day outdoors.'),
  ARVO.format(
    '<strong>Campaigns and protests</strong> commission oversized heads that a group carries through a street. That '
    f'brief has its own page: {link("https://www.oddtoe.com/use-cases/publicity-stunts/", "publicity stunts and cheeky PR campaigns")}.')
  + '\n\n' + ARVO.format(
    '<strong>Museums and galleries</strong> commission puppetry inside an exhibition or a late opening, often '
    'crossed with projection, and usually built to run unattended for weeks rather than for one night.')
  + '\n\n' + ARVO.format(
    '<strong>Producers and brands</strong> commission characters that are puppeteered on screen, or a physical '
    f'character that also lives in {link("https://www.oddtoe.com/ai-animation-studios/", "animation")}.'),
  anchor="who"))

# 9. (removed) The six-step timeline rail sat here. Added 14 Sep 2026 in the visual pass and
#    REMOVED the same day on Otto's instruction: "You can get rid of the row: Six steps, brief to
#    build / How a Puppet Gets Made". The timeline() helper above is left in place because it is the
#    reusable lift from the Use Case kit; nothing calls it now. The two-column process text this row
#    originally replaced is in git-less history only — it is reproduced in the page spec if it is
#    ever wanted back.

# 10. In Oddtoe's words ---------------------------------------------------------
# Otto cleared naming The Puppet Co. and Christopher Piper, 14 Sep 2026. Facts from his own
# 2004 nonfiction pieces and interview. Written as training, not as a client project.
rows.append(qsection(
  "Why Oddtoe Makes Puppets",
  "Where the craft was learned",
  ARVO.format(
    'In <strong>2004</strong> I trained under <strong>Christopher Piper</strong> at <strong>The Puppet Co.</strong> '
    'in Glen Echo Park, Maryland. He is a second-generation puppeteer &#8212; his father ran a travelling show out of '
    'Hawaii &#8212; and what I learned from him was <strong>building and stringing marionettes</strong>.') +
  '\n\n' + ARVO.format(
    'Stringing is the part nobody watches. Where each string attaches decides what the puppet is able to do, and a '
    'head hung a centimetre out will never look alive, whoever is working it. You find that out by getting it wrong '
    'and restringing it.'),
  ARVO.format(
    'That company had hundreds of puppets and a new theatre to fill, so the work was constant and the standard was '
    'set by people who had been doing it for twenty years. It is the most useful apprenticeship I have had.') +
  '\n\n' + ARVO.format(
    'Everything since has been the same problem at a different size. A head carried on a pole through a street, a '
    'costume with a person inside it, a character puppeteered live through a projector &#8212; all of them are '
    'objects <strong>a human being has to operate</strong>. The ones that fail are the ones where that was worked '
    'out after the drawing was finished.'),
  anchor="words"))

# 11. FAQ + JSON-LD + CTA -------------------------------------------------------
acc = ''
for i, (q, a) in enumerate(FAQ, start=1):
    tab_id = f"1757900000{i:03d}-puppet-designer-faq-{i}"
    acc += (f'[vc_tta_section title="{q}" tab_id="{tab_id}"][vc_column_text css=""]\n'
            f'<p style="text-align: center;">{a}</p>\n[/vc_column_text][/vc_tta_section]')

schema = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
          + ','.join('{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
                     % (json.dumps(q), json.dumps(plain(a))) for q, a in FAQ)
          + ']}</script>')
schema_b64 = base64.b64encode(urllib.parse.quote(schema, safe='').encode()).decode()

rows.append(
 '[vc_row bg_check="row-background-dark" dfd_enable_overlay=""][vc_column width="1/4"][/vc_column]'
 '[vc_column width="1/2"]' + sp(120, 100, 80, 80) +
 '[vc_column_text item_animation="transition.fadeIn"]\n'
 '<p style="text-align: center;"><span style="font-family: Qwigley; font-size: 36pt;">Questions about</span></p>\n'
 '<p style="text-align: center;"><span style="font-family: \'Bebas Neue\'; font-size: 36pt;">Puppet design?</span></p>\n'
 '[/vc_column_text]' + sp(40, 30, 20, 20) +
 '[dfd_accordion style="style-3" active_section="1" font_size="18" tab_title_google_fonts="yes" '
 'tab_title_custom_fonts="font_family:Arvo%3Aregular%2Citalic%2C700%2C700italic|'
 'font_style:700%20bold%20regular%3A700%3Anormal" icon_size="14"]' + acc + '[/dfd_accordion]'
 + f'[vc_raw_html]{schema_b64}[/vc_raw_html]' + sp(40, 30, 20, 20) +
 '[dfd_button button_text="Contact Oddtoe" '
 'buttom_link_src="url:https%3A%2F%2Fwww.oddtoe.com%2Fcontact-oddtoe%2F|title:Contact%20Oddtoe" style="style_6" '
 'background="#8a8f6a" hover_background="#4e5041" border="border-style:none;|border-radius:5px;" '
 'hover_border="border-style:none;|border-radius:5px;"]' + sp(120, 90, 60, 60) +
 '[/vc_column][vc_column width="1/4"][/vc_column][/vc_row]')

# 12. rev slider band -----------------------------------------------------------
rows.append('[vc_row dfd_row_config="full_width_content"][vc_column]'
            '[rev_slider slidertitle="Video Hero — Stained Glass Art in 3D" '
            'alias="video-hero-stained-glass-art-in-3d-1"]'
            '[/vc_column][/vc_row]')

# 13. Portfolio trio ------------------------------------------ carried from Mascot Designer
def portfolio(pid, offset=20):
    return (f'[dfd_portfolio_module items="single" single_custom_post_item="{pid}" items_offset="{offset}" columns="3" '
            'sort_panel="" enabled_excerpt="" enabled_read_more="" enabled_share="" enabled_comments="" '
            'enabled_likes="" enabled_anim_com_like="" image_width="900" image_height="600" style="fitRows" '
            'title_font_options="tag:div"]')

rows.append(
 '[vc_row bg_check="row-background-dark" dfd_enable_overlay="" one_page_title="More" anchor="more"][vc_column]'
 + sp(100, 90, 80, 80) +
 '[vc_column_text css="" item_animation="transition.fadeIn"]\n'
 '<p style="text-align: center;"><span style="font-family: Qwigley; font-size: 36pt;">Interested in seeing more&#8230; </span></p>\n\n'
 '<h2 style="text-align: center;"><span style="font-family: \'Bebas Neue\'; font-size: 36pt;">character work?</span></h2>\n'
 '[/vc_column_text]' + sp(60, 60, 40, 40) +
 '[vc_row_inner][vc_column_inner width="1/3"]' + portfolio(16154) + sp(90, 90, 60, 60) + '[/vc_column_inner]'
 '[vc_column_inner width="1/3"]' + portfolio(14669) + sp(90, 90, 60, 60) + '[/vc_column_inner]'
 '[vc_column_inner width="1/3"]' + portfolio(15269, 40) + sp(60, 60, 40, 40) + '[/vc_column_inner][/vc_row_inner]'
 + sp(60, 60, 30, 30) +
 '[vc_single_image image="11978" img_size="50x50" alignment="center" style="vc_box_outline_circle_2" '
 'image_opacity="70" onclick="custom_link" link="https://www.oddtoe.com/contact-oddtoe/"]'
 + sp(90, 90, 60, 60) + '[/vc_column][/vc_row]')

# 14. Contact form --------------------------------------------------------------
rows.append(
 '[vc_row bg_check="row-background-dark" dfd_enable_overlay="" anchor="form" bg_type="canvas_animated"][vc_column]'
 '[dfd_heading subtitle_google_fonts="yes" subtitle_custom_fonts="font_family:Qwigley%3Aregular" style="style_02" '
 'subtitle="Commission a puppet from someone who strung them first." '
 'title_font_options="tag:h2|font_family:BebasNeueRegular" subtitle_font_options="tag:h3"]'
 'Interested in working with Oddtoe?[/dfd_heading]' + sp(30, 30, 20, 20) +
 '[gravityform id="1" title="false" description="false" ajax="false"]' + sp(40, 30, 20, 20) +
 '[/vc_column][/vc_row]')

YOAST = ('YOAST SEO TITLE: Puppet Designer Melbourne | Marionette & Puppet Design | Oddtoe | '
         'META DESCRIPTION: Oddtoe is a Melbourne puppet designer - marionettes, rod and carried puppets, '
         'oversized heads and shadow work, designed in 3D and drawn for a maker to build.')

body = ''.join(rows)
with io.open(OUT, 'w', encoding='utf-8') as f:
    f.write(body)
print(YOAST)
print("wrote", OUT, len(body), "chars,", len(rows), "rows")
print("hero:", 16348, "carousel images:", CAROUSEL)
print("faq entries:", len(FAQ))
