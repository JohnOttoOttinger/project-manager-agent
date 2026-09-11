#!/usr/bin/env python3
# Compose the Oddtoe "Mascot Designer" page on the Installation Artist (page 11178) template.
# Output: mascot-designer.html  (WPBakery raw body, ready for wp-post.sh)
#
# TINT: #172b36 - Otto's call 7 Sep. It is the shark hero's bottom edge AS RENDERED, i.e. the
#       image's #2d5268 composited under the row's 50% black overlay, so the page ground blends
#       seamlessly out of the hero. Table cells retuned for that ground (seps 38 / 19).
# IMAGERY 7 Sep 2026: hero 16257 and carousel 16258-16261 are Otto's own mascot renders.
# rev_slider: compare-slider-prop-designer-1 was tried and does NOT port - it renders 903px of empty
# black on a dummy.png with a permanent spinner. Using the 3D design video, proven on 2 pages.
# Portfolio trio swapped 7 Sep: Babbling with Baobabs (16154, replaced Jackalope Factory
# on Otto's call - a built character sculpture, closer to made characters than a comic novella) /
# 3D Sculptor / Gag Cartoonist. No placeholders remain.
# All four are marked SWAP below.
import base64, urllib.parse, io, os, json, re

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mascot-designer.html")

SP = ('[dfd_spacer screen_wide_resolution="1280" screen_wide_spacer_size="{w}" screen_normal_resolution="1024" '
      'screen_tablet_resolution="800" screen_mobile_resolution="480" screen_normal_spacer_size="{n}" '
      'screen_tablet_spacer_size="{t}" screen_mobile_spacer_size="{m}"]')
def sp(w, n=None, t=None, m=None):
    n = w if n is None else n; t = n if t is None else t; m = t if m is None else m
    return SP.format(w=w, n=n, t=t, m=m)

ARVO = '<span style="font-family: Arvo;">{}</span>'
def link(url, label):
    return f'<strong><a class="dfd-custom-link-decorated" href="{url}">{label}</a></strong>'

# The visible accordion carries the <strong> markup; the FAQPage JSON-LD gets plain text.
def plain(t):
    return re.sub(r"<[^>]+>", "", t).replace("&#8217;", "\u2019").replace("&#8226;", "\u2022")

CANONICAL = ("<strong>Oddtoe</strong> is an experiential design and generative-AI animation studio based in Melbourne, "
             "creating projection, installation, and animated work for events, venues, and galleries.")

# NOTE: the design-IP question ("Who owns the mascot design?") is deliberately NOT here.
# Oddtoe's position is unrecorded and figures were not invented. See handoff.
FAQ = [
 ("What does a mascot designer actually do?",
  "The job splits in two: <strong>who the character is</strong>, and <strong>what the costume has to survive</strong>. "
  "That means the face and the personality, and it also means <strong>the performer inside it</strong> - sightlines, "
  "ventilation, weight, how long a shift can run, and whether the costume fits through a standard doorway."),
 ("Do you manufacture the costume?",
  "No. <strong>Oddtoe</strong> designs; <strong>a specialist costume manufacturer</strong> builds. The design package is made to be "
  "handed straight to a maker - <strong>3D model</strong>, turnarounds, <strong>colour and material specification</strong> "
  "- so the build starts from a signed-off character rather than an interpretation of a drawing."),
 ("How long does it take to get a mascot made?",
  "Manufacture typically runs <strong>eight to twelve weeks</strong>, excluding delivery, which is the standard lead "
  "time across specialist costume makers. Design sits in front of that and takes <strong>two to three weeks</strong>. "
  "Commission today and the first appearance is realistically <strong>three to four months</strong> away."),
 ("Do I need to supply a drawing?",
  "No. Most briefs arrive as <strong>a description, a logo, or a rough sketch</strong>, and some arrive with nothing "
  "at all. The first stage is working out what the character is and what it has to do, which happens "
  "<strong>before anything is drawn</strong>."),
 ("How much does a mascot cost?",
  "Cost is driven by what the brief decides: <strong>how structural the character is</strong>, <strong>how many "
  "costumes</strong> are needed, whether it <strong>requires cooling</strong>, and whether the design also has to work "
  "as an inflatable or on screen. Send the brief and where it will be used, and you get a quote."),
 ("What is the difference between a mascot and a brand character?",
  "A brand character <strong>lives in artwork</strong> - packaging, advertising, animation. Build it so "
  "<strong>a person can wear it</strong> and stand in a crowd and you have a mascot. Many brand characters need "
  "redesigning to make that move, because a design that reads flat does not always read <strong>at three metres with "
  "a human inside</strong> it."),
 ("Can the same character work as a giant inflatable?",
  "Yes, and it is worth deciding early. A character <strong>designed once in 3D</strong> can be built as "
  "<strong>a worn costume</strong>, as <strong>a giant inflatable</strong>, and as <strong>animated content</strong> "
  "for screens or projection. Retro-fitting a flat mascot drawing into a ten-metre inflatable afterwards usually "
  "means redesigning it."),
 ("Where is Oddtoe based?",
  "<strong>Oddtoe</strong> is based in <strong>Melbourne, Australia</strong>. Supplier and business contacts run through "
  "<strong>Berlin and Los Angeles</strong>, and those are the starting points for work in Europe and the "
  "United States."),
]

PAGE_STYLES = '[vc_raw_html]JTNDc3R5bGUlM0UlMjNoZXJvJTIwLmRmZC1yb3ctYmctY2FudmFzJTdCYmFja2dyb3VuZC1wb3NpdGlvbiUzQWNlbnRlciUyMGNlbnRlciUyMCUyMWltcG9ydGFudCU3RCU0MG1lZGlhJTIwJTI4bWluLXdpZHRoJTNBODAwcHglMjklN0IudmNfaW5uZXIlMjAuY29sdW1ucy50aHJlZSU3QnBhZGRpbmctbGVmdCUzQTIwcHglMjAlMjFpbXBvcnRhbnQlM0JwYWRkaW5nLXJpZ2h0JTNBMjBweCUyMCUyMWltcG9ydGFudCU3RCU3RCUzQyUyRnN0eWxlJTNF[/vc_raw_html]'

rows = []

# 1. HERO ------------------------------------------- hero canvas 16256 (own image, uploaded 7 Sep)
rows.append(
 '[vc_row bg_check="row-background-dark" dfd_bg_style="canvas" dfd_bg_image_canvas="16262" '
 'dfd_bg_image_repeat_canvas="no-repeat" dfd_overlay_color="#000000" dfd_overlay_pattern="transperant" '
 'dfd_overlay_pattern_opacity="50" dfd_row_config="full_width_content" dfd_bg_color_value="#172b36" '
 'anchor="hero"][vc_column]' + PAGE_STYLES
 + sp(520, 520, 340, 270) +
 '[dfd_heading enable_delimiter="" style="style_02" subtitle="Characters built to be worn" '
 'title_font_options="tag:h1|font_family:BebasNeueRegular|letter_spacing:0" '
 'subtitle_font_options="tag:h2|line_height:20" heading_margin="margin-bottom:10px;" '
 'subheading_margin="margin-bottom:10px;"]Mascot Designer[/dfd_heading]'
 + sp(700, 580, 480, 430) +
 '[/vc_column][/vc_row]')

# 2. INTRO --------------------------------------------------------------------
intro_a = ARVO.format(
  f'{CANONICAL} As a <strong>mascot designer</strong>, I design the character and everything a '
  'costume maker needs to build it. Somebody has to wear the result, which changes the job. Most of the '
  'design work happens before a single panel is cut.')
intro_b = ARVO.format(
  'The face has to <strong>read from thirty metres</strong>, the performer inside has to see, breathe, and last a shift, and the '
  'whole thing has to fit through a doorway and into the back of a van. I design in <strong>3D</strong> first, then '
  'hand the finished design to a specialist costume manufacturer to build. See '
  f'{link("https://www.oddtoe.com/artist-designer/character-designer/", "character design")} for the artwork and '
  f'animation side, or {link("https://www.oddtoe.com/artist-designer/inflatable-artist/", "giant inflatables")} for '
  'the same character at ten metres.')

rows.append(
 '[vc_row bg_check="row-background-dark"][vc_column]' + sp(80) +
 '[dfd_heading style="style_02" subtitle="Brand, sports, council, and retail characters" '
 'title_font_options="tag:h2|font_family:BebasNeueRegular|letter_spacing:0" '
 'subtitle_font_options="tag:h3|font_family:QwigleyRegular" '
 'heading_margin="margin-bottom:10px;"]Mascot Design &amp; Character Costume Design[/dfd_heading]'
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
 'subtitle="Mascot design, character design, and 3D" '
 'heading_margin="margin-bottom:10px;"]Mascot Designer &amp; Character Costume Designer[/dfd_heading]'
 + sp(10) + '[/vc_column][/vc_row]')

# 4. CAROUSEL --------------------------------------- SWAP: Character Designer placeholders (13701)
CAROUSEL = [16267,  # shaggy mascot on the workbench with fabric panels - design
            #        (replaced 16259 on Otto's call 7 Sep - better framing, no person in shot)
            16265,  # the five sharks as a 3D wireframe mesh - the 3D model stage
            16268,  # stitching panels onto a mascot head form - patterning
            16261,  # marking a stitched panel - specification
            16264,  # fish mascot in the costume workshop - build
            16263,  # the finished family of shark characters - result
            16256]  # caricature character heads at street level - in use  # caricature character heads at street level - in use  # caricature character heads at street level
imgs = ''.join(f'[dfd_single_image image="{i}" image_size="custom" image_width="250" image_height="250" '
               f'image_border_radius="10"]' for i in CAROUSEL)
rows.append(
 '[vc_row dfd_enable_overlay="" anchor="work"][vc_column]' + sp(20) +
 '[dfd_carousel center_mode="on" center_mode_scale="on" adaptive_height="" module_animation="transition.fadeIn" '
 'slides_to_show="3" screen_normal_resolution="1024" screen_normal_slides="3" screen_tablet_resolution="800" '
 'screen_tablet_slides="3" screen_mobile_resolution="480" slider_type="horizontal" dots_style="dfdfillrounded" '
 'dots_color="#000000" arrows_position="aside2" arrows_style="style_3" arrows_bg="#252525"]'
 + imgs + '[/dfd_carousel]' + sp(60, 40, 30, 40) + '[/vc_column][/vc_row]')

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

# 5. What does a mascot designer do -------------------------------------------
rows.append(qsection(
  "What Does a Mascot Designer Do?",
  "The character, and the person inside it",
  ARVO.format(
    'A mascot designer decides <strong>what the character is</strong> and <strong>what it has to survive</strong>. '
    'That covers the face and the personality, and it covers the performer inside: sightlines, ventilation, weight, '
    'how long a shift can run, and whether the costume fits through a standard doorway.') + '\n\n' + ARVO.format(
    'A brand character lives in artwork. Turning one into something a person can wear in a crowd is a different job, '
    'and plenty of characters fail that transition.'),
  ARVO.format(
    'A design that works flat on packaging does not automatically work <strong>at three metres with a human inside</strong>, '
    'holding a pose, being photographed from below by someone&#8217;s child.') + '\n\n' + ARVO.format(
    'The designer&#8217;s job is to settle both halves before anything is patterned: who this character is, and what '
    'the body has to do. Closely related practices — '
    f'{link("https://www.oddtoe.com/artist-designer/character-designer/", "character design")} and '
    f'{link("https://www.oddtoe.com/artist-designer/prop-designer-maker/", "prop making")} — often end up inside the '
    'same commission.'),
  anchor="what", one_page="What?", parallax=True))

# 6. What goes into one --------------------------------------------------------
rows.append(qsection(
  "What Goes Into an Oddtoe Mascot Design?",
  "Character, 3D model, and a maker-ready spec",
  ARVO.format(
    'A <strong>character definition</strong>, a <strong>3D model</strong>, turnarounds from every angle, a '
    'performer and practicality check, and a <strong>colour and material specification</strong> a costume '
    'manufacturer can quote and build from.') +
  '\n\n' + ARVO.format('Each of these connects to a practice with its own page:') + '\n\n' + ARVO.format(
    f'&#8226; {link("https://www.oddtoe.com/artist-designer/character-designer/", "Character design")}<br />'
    f'&#8226; {link("https://www.oddtoe.com/artist-designer/inflatable-artist/", "Giant inflatables and walk-in structures")}<br />'
    f'&#8226; {link("https://www.oddtoe.com/artist-designer/prop-designer-maker/", "Props and fabricated objects")}<br />'
    f'&#8226; {link("https://www.oddtoe.com/artist-designer/roboticist/", "Robotics and animatronics")}'),
  ARVO.format(
    'The newer ingredient is <strong>generative AI</strong>, used for concept exploration and for the animated '
    'content a mascot ends up in — screens at the venue, social cutdowns, projection. There is a full explainer on '
    f'{link("https://www.oddtoe.com/what-is-generative-ai-animation/", "what generative AI animation is")}.') +
  '\n\n' + ARVO.format(
    'The 3D model is <strong>the reusable part</strong>. The same asset that proves the character to a client produces the pitch '
    'renders, the animated content, and, if it is wanted later, the inflatable version.')))

# 7. COMPARISON TABLE ----------------------------------------------------------
TH = ('padding: 14px 18px; text-align: left; background-color: #000000 !important; border: none !important; '
      'border-bottom: 2px solid #ddccb1 !important; font-family: \'Bebas Neue\', sans-serif; font-size: 21px; '
      'font-weight: normal; letter-spacing: 1px; color: #ffffff !important;')
def td(bg):
    return (f'padding: 12px 18px; text-align: left; background-color: {bg} !important; border: none !important; '
            f'border-bottom: 1px solid #2c4a5a !important; color: #ffffff !important;')

TABLE_ROWS = [
 ("What it is",
  "A wearable character a performer operates",
  "A character that lives in artwork and animation",
  "An inflated character or structure, metres tall"),
 ("Where it lives",
  "Match days, store openings, expos, school visits",
  "Packaging, ads, apps, animation, social",
  "Festival fields, forecourts, atriums, rooftops"),
 ("Contact with the audience",
  "Handshakes, photos, direct interaction",
  "Screens and print",
  "Photographed from a distance, walked under"),
 ("Who commissions it",
  "Sports clubs, councils, retail, charities",
  "Brands, publishers, studios",
  "Festivals, brands, precinct associations"),
 ("Lead time",
  "Design, then eight to twelve weeks manufacture",
  "Design only",
  "Design, then fabrication"),
 ("What Oddtoe delivers",
  "Character, 3D model, maker-ready specification",
  "Character, turnarounds, on-model sheets",
  "Character, 3D model, pattern set"),
]
tbody = ''
for i, (crit, a, b, c) in enumerate(TABLE_ROWS):
    bg = '#000000' if i % 2 == 0 else '#0a1720'
    tbody += (f'<tr><td style="{td(bg)}"><strong>{crit}</strong></td>'
              f'<td style="{td(bg)}">{a}</td><td style="{td(bg)}">{b}</td><td style="{td(bg)}">{c}</td></tr>\n')

table_html = (
 '<div style="overflow-x: auto;">\n'
 '<table style="width: 100%; border-collapse: collapse !important; background-color: #000000 !important; border: none !important;">\n'
 '<thead>\n<tr>'
 f'<th scope="col" style="{TH} white-space: nowrap;">&nbsp;</th>'
 f'<th scope="col" style="{TH}">Costume mascot</th>'
 f'<th scope="col" style="{TH}">Brand character</th>'
 f'<th scope="col" style="{TH}">Giant inflatable</th>'
 '</tr>\n</thead>\n<tbody>\n' + tbody + '</tbody>\n</table>\n</div>')

rows.append(
 '[vc_row bg_check="row-background-dark" dfd_enable_overlay="" dfd_row_responsive_enable="dfd-row-responsive-enable" '
 'responsive_styles="padding_left_mobile:10|padding_right_mobile:10"][vc_column]' + sp(60, 60, 50, 40) +
 '[dfd_heading enable_delimiter="" style="style_02" '
 'title_font_options="tag:h2|font_family:BebasNeueRegular|letter_spacing:0" '
 'subtitle_font_options="tag:h3|font_family:QwigleyRegular" '
 'subtitle="Which one is your brief?" heading_margin="margin-bottom:10px;"]'
 'Mascot, Brand Character, or Giant Inflatable?[/dfd_heading]' + sp(20) +
 '[vc_row_inner][vc_column_inner width="1/6"][/vc_column_inner][vc_column_inner width="2/3"][vc_column_text css=""]'
 + ARVO.format('Three things get asked for using <strong>the same words</strong>. This table sets out what each one is, '
               'where it goes, and what <strong>Oddtoe</strong> hands over.')
 + '\n\n' + table_html +
 '[/vc_column_text][/vc_column_inner][vc_column_inner width="1/6"][/vc_column_inner][/vc_row_inner]'
 + sp(60, 60, 40, 40) + '[/vc_column][/vc_row]')

# 8. Who commissions -----------------------------------------------------------
# NOTE: no market statistic here. The Installation Artist page cites IBISWorld; no verified
# equivalent exists for mascots and none was invented. See handoff.
rows.append(qsection(
  "Who Commissions a Mascot Designer?",
  "Clubs, councils, centres, and brands",
  ARVO.format(
    'Sports clubs, local councils, shopping centres, visitor attractions, charities, and the agencies that '
    'run campaigns for brands. Each wants <strong>a different outcome from the same craft</strong>: a match-day character, a '
    'safety campaign children remember, a photographed school holiday, or a brand moment on an expo floor.') +
  '\n\n' + ARVO.format(
    '<strong>Sports clubs</strong> commission a mascot that works on a match day and then does community and school '
    'visits all week.') + '\n\n' + ARVO.format(
    '<strong>Local councils</strong> commission campaign characters — road safety, recycling, water, libraries — '
    'that have to be liked by children and defensible to ratepayers.'),
  ARVO.format(
    '<strong>Shopping centres and retail</strong> commission a resident character for school holidays and store '
    'openings, where the whole return is photographs.') + '\n\n' + ARVO.format(
    '<strong>Visitor attractions, zoos, and museums</strong> commission a character that becomes part of the visit '
    'rather than a costume that turns up once.') + '\n\n' + ARVO.format(
    '<strong>Charities</strong> commission a character for fundraising drives and fun runs, where it has to be '
    'approachable to children and read well in a photograph.') + '\n\n' + ARVO.format(
    '<strong>Agencies and brands</strong> commission a mascot as one element of a campaign build: see '
    f'{link("https://www.oddtoe.com/experiential-marketing/", "experiential marketing")} and the '
    f'{link("https://www.oddtoe.com/brand-activation-ideas/", "brand activation ideas")} list.'),
  anchor="who"))

# 9. Process --------------------------------------------------------------------
rows.append(qsection(
  "How Does an Oddtoe Mascot Get Designed and Built?",
  "From brief to a costume maker&#8217;s bench",
  ARVO.format(
    '<strong>Six steps</strong>: the brief and the use, the character, the 3D model, the performer check, the '
    'specification, and handover to a manufacturer. Design takes <strong>two to three weeks</strong>. Manufacture is '
    'a separate <strong>eight to twelve weeks</strong> on top of that.') + '\n\n' + ARVO.format(
    '<strong>1. Brief and use.</strong> Where it appears, how often, how long a shift runs, indoors or out, and who '
    'or what it has to stand next to.') + '\n\n' + ARVO.format(
    '<strong>2. The character.</strong> Who this is, not only what it looks like. The personality settles the '
    'posture, and the maker needs the posture before anything is patterned.'),
  ARVO.format(
    '<strong>3. 3D model and turnarounds.</strong> Built in 3D so you see the character from every angle, and in the '
    'space it will actually appear in, before a sculpt exists.') + '\n\n' + ARVO.format(
    '<strong>4. Performer and practicality.</strong> Height range, sightlines, ventilation, weight, hand function, '
    'doorways, transport, and storage.') + '\n\n' + ARVO.format(
    '<strong>5. Specification for the maker.</strong> Colour references, fabric notes, branding placement, and the '
    'files a costume manufacturer needs to quote and build.') + '\n\n' + ARVO.format(
    '<strong>6. Handover.</strong> The design goes to a specialist manufacturer. The 3D asset stays useful '
    'afterwards for renders and animation.'),
  anchor="how"))

# 10. In Oddtoe's words ---------------------------------------------------------
rows.append(qsection(
  "Why Oddtoe Designs Mascots",
  "Why bother designing it properly",
  ARVO.format(
    'Most mascots are <strong>a logo with arms</strong>. Someone takes a flat brand character, adds a body, sends it to a '
    'manufacturer, and what turns up is a costume nobody wants to be photographed with.') + '\n\n' + ARVO.format(
    'It is <strong>a performance object</strong>. Someone inside has to see, breathe, and hold the '
    'character for <strong>a four-hour shift</strong>. The crowd outside decides <strong>in a second</strong> whether it is friendly. '
    'Both are design problems, settled before the drawing is finished.'),
  ARVO.format(
    'Everything I make is <strong>built in 3D and animated</strong>, so a mascot design arrives having already been seen from every '
    'angle and <strong>in motion</strong>, rather than as a front view and a guess. You see the walk before anyone cuts fabric.')
  + '\n\n' + ARVO.format(
    'The cheeky part is the bit I care about. A mascot that <strong>behaves a little unexpectedly</strong> is the one people '
    'photograph, and photographs are what the client actually gets out of the thing, long after the event is '
    'packed up and the costume is back in its case.'),
  anchor="words"))

# 11. FAQ + JSON-LD + CTA -------------------------------------------------------
acc = ''
for i, (q, a) in enumerate(FAQ, start=1):
    tab_id = f"1757200000{i:03d}-mascot-designer-faq-{i}"
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
 '<p style="text-align: center;"><span style="font-family: \'Bebas Neue\'; font-size: 36pt;">Mascot design?</span></p>\n'
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

# 12. rev slider band ------------------------------------- SWAP: Character Designer's slider
rows.append('[vc_row dfd_row_config="full_width_content"][vc_column]'
            '[rev_slider slidertitle="Video Hero — Stained Glass Art in 3D" '
            'alias="video-hero-stained-glass-art-in-3d-1"]'
            '[/vc_column][/vc_row]')

# 13. Portfolio trio -------------------------------------- SWAP: Character Designer's trio
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
 'subtitle="Commission a mascot designer who specifies it properly." '
 'title_font_options="tag:h2|font_family:BebasNeueRegular" subtitle_font_options="tag:h3"]'
 'Interested in working with Oddtoe?[/dfd_heading]' + sp(30, 30, 20, 20) +
 '[gravityform id="1" title="false" description="false" ajax="false"]' + sp(40, 30, 20, 20) +
 '[/vc_column][/vc_row]')

YOAST = ('YOAST SEO TITLE: Mascot Designer Melbourne | Custom Mascot Design | Oddtoe | '
         'META DESCRIPTION: Oddtoe is a Melbourne mascot designer - brand, sports, council and retail mascots '
         'designed in 3D and specified for a costume maker to build.')

body = ''.join(rows)
with io.open(OUT, 'w', encoding='utf-8') as f:
    f.write(body)
print(YOAST)
print("wrote", OUT, len(body), "chars,", len(rows), "rows")
print("carousel images:", CAROUSEL)
print("faq entries:", len(FAQ))
