#!/usr/bin/env python3
# Compose the Oddtoe "Installation Artist" page on the Documentary Animator (page 15400) template.
# Output: installation-artist.html  (WPBakery raw body, ready for wp-post.sh)
import base64, urllib.parse, io, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "installation-artist.html")

SP = ('[dfd_spacer screen_wide_resolution="1280" screen_wide_spacer_size="{w}" screen_normal_resolution="1024" '
      'screen_tablet_resolution="800" screen_mobile_resolution="480" screen_normal_spacer_size="{n}" '
      'screen_tablet_spacer_size="{t}" screen_mobile_spacer_size="{m}"]')
def sp(w, n=None, t=None, m=None):
    n = w if n is None else n; t = n if t is None else t; m = t if m is None else m
    return SP.format(w=w, n=n, t=t, m=m)

ARVO = '<span style="font-family: Arvo;">{}</span>'
def link(url, label):
    return f'<strong><a class="dfd-custom-link-decorated" href="{url}">{label}</a></strong>'
def extlink(url, label):
    return f'<strong><a class="dfd-custom-link-decorated" href="{url}" target="_blank" rel="noopener">{label}</a></strong>'

# ---------------------------------------------------------------- content ----
CANONICAL = ("Oddtoe is an experiential design and generative-AI animation studio based in Melbourne, "
             "creating projection, installation, and animated work for events, venues, and galleries.")

FAQ = [
 ("What does an installation artist actually do?",
  "An installation artist designs and builds three-dimensional work for a specific location, then installs it there. "
  "The job covers the concept, the 3D design, the choice of materials, the build with fabricators, and the install "
  "itself. Oddtoe works across topiary, robotics, kinetic sculpture, and projected light."),
 ("What is the difference between installation art and sculpture?",
  "A sculpture is an object that can be moved and shown almost anywhere. An installation is built around its site, so "
  "the room, the lighting, and the path the audience takes are part of the work. Many installations contain sculptures; "
  "the installation is the whole arrangement."),
 ("How much does an art installation cost?",
  "Cost is driven by scale, materials, how much fabrication is needed, site access, power and rigging, and how long the "
  "piece stays up. A single indoor object and a multi-piece outdoor commission are very different budgets. Oddtoe quotes "
  "each brief individually — send the site details and the dates."),
 ("How long does it take to design and build an installation?",
  "Two to three weeks from brief to install day for a typical piece. Larger multi-piece commissions run longer, because "
  "the schedule is driven by fabrication, permits, and site access. Booking early keeps the build window comfortable."),
 ("Can an installation be reused at another site?",
  "Sometimes. Modular pieces, props, and kinetic elements can be re-rigged for a second site if that is planned into the "
  "design from the start. Work built into a specific facade, garden, or room usually cannot move without being redesigned."),
 ("Do you work with agencies and producers, or only galleries?",
  "Both. Oddtoe works with curators and venues on gallery and public work, and with advertising, marketing, and activation "
  "agencies on brand installations. For agency briefs the studio handles fabrication, projection, animation, and install "
  "under one roof."),
 ("Where is Oddtoe based, and where do you install?",
  "Oddtoe is based in Melbourne, Australia, and works with clients in Los Angeles and Berlin. Installations are delivered "
  "in Melbourne and across Australia, with travel quoted up front for interstate and overseas sites."),
]

PAGE_STYLES = '[vc_raw_html]JTNDc3R5bGUlM0UlMjNoZXJvJTIwLmRmZC1yb3ctYmctY2FudmFzJTdCYmFja2dyb3VuZC1wb3NpdGlvbiUzQWNlbnRlciUyMGNlbnRlciUyMCUyMWltcG9ydGFudCU3RCU0MG1lZGlhJTIwJTI4bWluLXdpZHRoJTNBODAwcHglMjklN0IudmNfaW5uZXIlMjAuY29sdW1ucy50aHJlZSU3QnBhZGRpbmctbGVmdCUzQTIwcHglMjAlMjFpbXBvcnRhbnQlM0JwYWRkaW5nLXJpZ2h0JTNBMjBweCUyMCUyMWltcG9ydGFudCU3RCU3RCUzQyUyRnN0eWxlJTNF[/vc_raw_html]'

# ------------------------------------------------------------------ rows -----
rows = []

# 1. HERO ---------------------------------------------------------------------
rows.append(
 '[vc_row bg_check="row-background-dark" dfd_bg_style="canvas" dfd_bg_image_canvas="16054" '
 'dfd_bg_image_repeat_canvas="no-repeat" dfd_overlay_color="#000000" dfd_overlay_pattern="transperant" '
 'dfd_overlay_pattern_opacity="50" dfd_row_config="full_width_content" dfd_bg_color_value="#241834" '
 'anchor="hero"][vc_column]' + PAGE_STYLES
 + sp(520, 520, 340, 270) +
 '[dfd_heading enable_delimiter="" style="style_02" subtitle="Art you can walk around" '
 'title_font_options="tag:h1|font_family:BebasNeueRegular|letter_spacing:0" '
 'subtitle_font_options="tag:h2|line_height:20" heading_margin="margin-bottom:10px;" '
 'subheading_margin="margin-bottom:10px;"]Installation Artist[/dfd_heading]'
 + sp(700, 580, 480, 430) +
 '[/vc_column][/vc_row]')

# 2. INTRO (two 1/4 text columns, like the template) ---------------------------
intro_a = ARVO.format(
  f'<strong>{CANONICAL}</strong> As an <strong>installation artist</strong>, I build pieces that occupy a room '
  'rather than hang on its wall. <strong>Topiary, robotics, kinetic sculpture</strong>, and <strong>projected '
  'light</strong>, assembled into one thing an audience can walk around. <em>Updated August 2026.</em>')
intro_b = ARVO.format(
  'The work is <strong>site-specific</strong>. A gallery, a hotel foyer, a laneway, a festival field, and a shopping '
  'centre atrium all want different objects, so the design starts with the space and the route people take through it. '
  'I design in <strong>3D</strong> first, then work with fabricators to get the piece built and installed. See the '
  f'studio&#8217;s {link("https://www.oddtoe.com/experiential-marketing/", "experiential marketing services")} or the '
  f'{link("https://www.oddtoe.com/brand-activation-ideas/", "brand activation ideas")} list.')

rows.append(
 '[vc_row bg_check="row-background-dark"][vc_column]' + sp(80) +
 '[dfd_heading style="style_02" subtitle="Sculpture, topiary, robotics, and light in one room" '
 'title_font_options="tag:h2|font_family:BebasNeueRegular|letter_spacing:0" '
 'subtitle_font_options="tag:h3|font_family:QwigleyRegular" '
 'heading_margin="margin-bottom:10px;"]Installation Art &amp; Experiential Design[/dfd_heading]'
 + sp(20, 20, 15, 10) +
 '[vc_row_inner][vc_column_inner width="1/4"][/vc_column_inner][vc_column_inner width="1/4"]'
 f'[vc_column_text css=""]{intro_a}[/vc_column_text]' + sp(20) +
 '[/vc_column_inner][vc_column_inner width="1/4"]'
 f'[vc_column_text]{intro_b}[/vc_column_text]' + sp(20) +
 '[/vc_column_inner][vc_column_inner width="1/4"][/vc_column_inner][/vc_row_inner]'
 + sp(80, 80, 70, 60) + '[/vc_column][/vc_row]')

# 3. SECTION HEAD above the carousel ------------------------------------------
rows.append(
 '[vc_row bg_check="row-background-dark" dfd_row_responsive_enable="dfd-row-responsive-enable" '
 'responsive_styles="padding_left_mobile:10|padding_right_mobile:10"][vc_column]' + sp(60, 60, 50, 40) +
 '[dfd_heading module_animation="transition.swoopIn" enable_delimiter="" style="style_02" '
 'title_font_options="tag:h2|font_family:BebasNeueRegular" '
 'subtitle_font_options="tag:h3|font_family:QwigleyRegular" '
 'subtitle="Installation art, kinetic sculpture, topiary, and projection" '
 'heading_margin="margin-bottom:10px;"]Installation Artist &amp; Experiential Designer[/dfd_heading]'
 + sp(10) + '[/vc_column][/vc_row]')

# 4. CAROUSEL -----------------------------------------------------------------
CAROUSEL = [12831, 12665, 12666, 13121, 12646, 14757, 14739, 14755,
            13033, 15394, 15389, 13302, 12848, 12846, 12644]
imgs = ''.join(f'[dfd_single_image image="{i}" image_size="custom" image_width="250" image_height="250" '
               f'image_border_radius="10"]' for i in CAROUSEL)
rows.append(
 '[vc_row dfd_enable_overlay="" anchor="work"][vc_column]' + sp(20) +
 '[dfd_carousel center_mode="on" center_mode_scale="on" adaptive_height="" module_animation="transition.fadeIn" '
 'slides_to_show="5" screen_normal_resolution="1024" screen_normal_slides="4" screen_tablet_resolution="800" '
 'screen_tablet_slides="3" screen_mobile_resolution="480" slider_type="horizontal" dots_style="dfdfillrounded" '
 'dots_color="#000000" arrows_position="aside2" arrows_style="style_3" arrows_bg="#252525"]'
 + imgs + '[/dfd_carousel]' + sp(60, 40, 30, 40) + '[/vc_column][/vc_row]')

# --- reusable two-column question section ------------------------------------
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

# 5. What is installation art? -------------------------------------------------
rows.append(qsection(
  "What Is Installation Art?",
  "The room is part of the artwork",
  ARVO.format(
    '<strong>Installation art is three-dimensional work made for a particular space, where the room, the route '
    'through it, and the audience are all part of the piece.</strong> A painting works on any wall. An installation '
    'is designed around its site, its lighting, and the way people move past it.') + '\n\n' + ARVO.format(
    'The term covers a lot of ground. It can be one large object under a spotlight, a whole room the audience walks '
    'into, or a set of pieces spread across a park.'),
  ARVO.format(
    'What those have in common is that the location is not a backdrop. Move the work somewhere else and it becomes a '
    'different work.') + '\n\n' + ARVO.format(
    'Oddtoe treats that as the interesting part of the job. If a viewer has to walk around something, then their path, '
    'their eye line, and what they see when they turn around are all things to design. Closely related practices — '
    f'{link("https://www.oddtoe.com/artist-designer/kinetic-sculptor/", "kinetic sculpture")} and '
    f'{link("https://www.oddtoe.com/artist-designer/projection-artist/", "projection art")} — often end up inside the '
    'same commission.'),
  anchor="what", one_page="What?", parallax=True))

# 6. What goes into one ---------------------------------------------------------
rows.append(qsection(
  "What Goes Into an Oddtoe Installation?",
  "Living material, metal, machinery, and light",
  ARVO.format(
    '<strong>Topiary, robotics, kinetic sculpture, projected light, and generative-AI animation.</strong> Most Oddtoe '
    'installations combine several of these in one piece — a planted form with a moving mechanical element, projected '
    'onto after dark. Materials run from living plants and metal through to composites, resin, and very black paint.') +
  '\n\n' + ARVO.format(
    'Each of those is a practice in its own right, and each has its own page:'),
  ARVO.format(
    f'&#8226; {link("https://www.oddtoe.com/artist-designer/topiarist/", "Topiary and planted forms")}<br />'
    f'&#8226; {link("https://www.oddtoe.com/artist-designer/kinetic-sculptor/", "Kinetic sculpture")}<br />'
    f'&#8226; {link("https://www.oddtoe.com/artist-designer/roboticist/", "Robotics and animatronics")}<br />'
    f'&#8226; {link("https://www.oddtoe.com/artist-designer/projection-artist/", "Projection and light")}<br />'
    f'&#8226; {link("https://www.oddtoe.com/artist-designer/prop-designer-maker/", "Props and fabricated objects")}<br />'
    f'&#8226; {link("https://www.oddtoe.com/artist-designer/sensory-garden-designer/", "Sensory garden design")}') +
  '\n\n' + ARVO.format(
    'The newer ingredient is <strong>generative AI</strong>, used for concept exploration and for the animated content '
    'that gets projected onto a built piece. There is a full explainer on '
    f'{link("https://www.oddtoe.com/what-is-generative-ai-animation/", "what generative AI animation is")}.')))

# 7. COMPARISON TABLE -----------------------------------------------------------
TH = ('padding: 14px 18px; text-align: left; background-color: #000000 !important; border: none !important; '
      'border-bottom: 2px solid #ddccb1 !important; font-family: \'Bebas Neue\', sans-serif; font-size: 21px; '
      'font-weight: normal; letter-spacing: 1px; color: #ffffff !important;')
def td(bg, bold=False):
    return (f'padding: 12px 18px; text-align: left; background-color: {bg} !important; border: none !important; '
            f'border-bottom: 1px solid #26161f !important; color: #ffffff !important;')

TABLE_ROWS = [
 ("What it is",
  "Physical objects built into a space",
  "Light and animation thrown onto a surface",
  "A branded experience built for a campaign"),
 ("Where it lives",
  "Galleries, foyers, parks, festival grounds",
  "Building facades, walls, laneways, interiors",
  "Shopping centres, expos, festivals, retail"),
 ("How long it stays up",
  "Weeks to months",
  "One night to a season, indoors or after dark",
  "Days to a few weeks"),
 ("Who commissions it",
  "Curators, councils, venues, property owners",
  "Festivals, councils, precinct associations",
  "Marketing and activation agencies, brands"),
 ("Site requirements",
  "Structural mounting, floor space, often power",
  "Projector positions, throw distance, darkness",
  "Build access, power, and a run schedule"),
 ("What Oddtoe delivers",
  "Concept, 3D design, fabrication, install",
  "Concept, animation content, projection",
  "Concept, props, fabrication, install, run"),
]
tbody = ''
for i, (crit, a, b, c) in enumerate(TABLE_ROWS):
    bg = '#000000' if i % 2 == 0 else '#111111'
    tbody += (f'<tr><td style="{td(bg)}"><strong>{crit}</strong></td>'
              f'<td style="{td(bg)}">{a}</td><td style="{td(bg)}">{b}</td><td style="{td(bg)}">{c}</td></tr>\n')

table_html = (
 '<div style="overflow-x: auto;">\n'
 '<table style="width: 100%; border-collapse: collapse !important; background-color: #000000 !important; border: none !important;">\n'
 '<thead>\n<tr>'
 f'<th scope="col" style="{TH} white-space: nowrap;">&nbsp;</th>'
 f'<th scope="col" style="{TH}">Installation art</th>'
 f'<th scope="col" style="{TH}">Projection art</th>'
 f'<th scope="col" style="{TH}">Brand activation</th>'
 '</tr>\n</thead>\n<tbody>\n' + tbody + '</tbody>\n</table>\n</div>')

rows.append(
 '[vc_row bg_check="row-background-dark" dfd_enable_overlay="" dfd_row_responsive_enable="dfd-row-responsive-enable" '
 'responsive_styles="padding_left_mobile:10|padding_right_mobile:10"][vc_column]' + sp(60, 60, 50, 40) +
 '[dfd_heading enable_delimiter="" style="style_02" '
 'title_font_options="tag:h2|font_family:BebasNeueRegular|letter_spacing:0" '
 'subtitle_font_options="tag:h3|font_family:QwigleyRegular" '
 'subtitle="Which one is your brief?" heading_margin="margin-bottom:10px;"]'
 'Installation Art, Projection Art, or Brand Activation?[/dfd_heading]' + sp(20) +
 '[vc_row_inner][vc_column_inner width="1/6"][/vc_column_inner][vc_column_inner width="2/3"][vc_column_text css=""]'
 + ARVO.format('<strong>Three things get asked for using the same words. This table sets out what each one is, '
               'where it goes, and what Oddtoe hands over.</strong>')
 + '\n\n' + table_html +
 '[/vc_column_text][/vc_column_inner][vc_column_inner width="1/6"][/vc_column_inner][/vc_row_inner]'
 + sp(60, 60, 40, 40) + '[/vc_column][/vc_row]')

# 8. Who commissions -------------------------------------------------------------
rows.append(qsection(
  "Who Commissions an Installation Artist?",
  "Galleries, festivals, venues, and agencies",
  ARVO.format(
    '<strong>Galleries and museums, festivals and local councils, property owners and venues, and the marketing and '
    'activation agencies working for brands.</strong> Each wants a different outcome from the same craft: a curated '
    'exhibit, a crowd after dark, a photographed foyer, or a campaign moment.') + '\n\n' + ARVO.format(
    'Australia&#8217;s art galleries and museums are a $2.6 billion industry in 2025-26, according to '
    f'{extlink("https://www.ibisworld.com/australia/industry/art-galleries-and-museums/644/", "IBISWorld")}, '
    'which notes that institutions are staging immersive and experiential exhibitions that audiences will pay premium '
    'prices to see.'),
  ARVO.format(
    '<strong>Curators and cultural institutions</strong> commission work that carries an idea and survives a season of '
    'public traffic.') + '\n\n' + ARVO.format(
    '<strong>Festivals and councils</strong> commission work that pulls people into a laneway, a park, or a main street '
    'after dark.') + '\n\n' + ARVO.format(
    '<strong>Venues, resorts, and property owners</strong> commission a hero piece — the thing in the foyer or the '
    'courtyard that guests photograph.') + '\n\n' + ARVO.format(
    '<strong>Agencies and brands</strong> commission installations as part of an activation. Oddtoe works as the junior '
    f'partner on those: see {link("https://www.oddtoe.com/experiential-marketing/", "experiential marketing")}.'),
  anchor="who"))

# 9. Process -----------------------------------------------------------------------
rows.append(qsection(
  "How Does an Oddtoe Installation Get Built?",
  "From site visit to install day",
  ARVO.format(
    '<strong>Six steps: the brief and the site, concept renders in 3D, a materials and fabrication plan, the build, '
    'the install, and documentation. Typical lead time is two to three weeks from brief to install day.</strong> '
    'Fabrication, projection, animation, and install are handled from one '
    'studio, so there is no chasing a prop maker, a content studio, and an AV contractor who have never met.') +
  '\n\n' + ARVO.format(
    '<strong>1. Brief and site.</strong> Dimensions, access, power, rigging points, sightlines, and how long the piece '
    'needs to stand up.') + '\n\n' + ARVO.format(
    '<strong>2. Concept renders.</strong> Designed in 3D so the client sees the piece in the actual space before '
    'anything is cut or planted.'),
  ARVO.format(
    '<strong>3. Materials and fabrication plan.</strong> What gets made in the studio, what goes to a fabricator, and '
    'what the schedule and the budget look like.') + '\n\n' + ARVO.format(
    '<strong>4. Build.</strong> Working with fabricators and suppliers, with regular progress updates rather than '
    'a long silence.') + '\n\n' + ARVO.format(
    '<strong>5. Install.</strong> On site, on the agreed day, with the crew and the permits sorted.') +
  '\n\n' + ARVO.format(
    '<strong>6. Documentation.</strong> Photography and video of the finished piece, which is usually what the client '
    'actually circulates afterwards.'),
  anchor="how"))

# 10. In Otto's words ----------------------------------------------------------------
rows.append(qsection(
  "Why Oddtoe Makes Installation Art",
  "The bit of the old interview worth keeping",
  ARVO.format(
    'An installation artist is interested in the viewer and in the location the piece is seen. I&#8217;d hate to not '
    'have those two things in my creative thinking anyway. I like installations that make the viewer think, or see '
    'something differently. My own twist is that I don&#8217;t mind messing with the viewer in a cheeky, friendly way.') +
  '\n\n' + ARVO.format(
    'I haven&#8217;t seen much creative cheekiness mixed with state-of-the-art technology. That is what I am after with '
    'Oddtoe.') + '\n\n' + ARVO.format(
    'My ingredients are part of what makes the work different. The art world was furious at '
    f'{extlink("https://en.wikipedia.org/wiki/Anish_Kapoor", "Anish Kapoor")} for '
    f'{extlink("https://archpaper.com/2017/07/anish-kapoor-blackest-black/", "securing exclusive rights to the deepest black paint ever invented")}. '
    'I understand why he did it. I&#8217;d give a kidney for a litre of that stuff. That paint is on my list, along with '
    'magnets, projected light, taxidermy, kinetic sculptures, and whatever else catches my fancy.'),
  ARVO.format(
    '<strong>The perfect client</strong> is a gallery owner or a museum curator who thinks in future terms. A lot of what '
    'I make has today&#8217;s zeitgeist in it, even when that is not obvious on the surface — how artificial intelligence '
    'will play with humanity, robots, sustainability. Collectors who see value in the collision of design and technology, '
    'too. What Oddtoe makes is not hang-it-on-the-wall-and-forget-it art.') + '\n\n' + ARVO.format(
    '<strong>The perfect project</strong> would involve the person standing next to it. One idea I am working through in '
    'my installation series <em>Botanikus Goiterus</em> is plants that speak to people through elaborately designed '
    'translators. The messages are generated by an AI and adapt through the back-and-forth, so more of the person ends up '
    'in the plant&#8217;s sentences.') + '\n\n' + ARVO.format(
    '<strong>The genuinely crazy thought</strong> is uplifting art. Humorous art. The world can be a bleak place, and the '
    'arts celebrate melancholy and stark subjects pretty often. Positive psychology earned a seat at the table in its '
    'field. I&#8217;d like positive art to do the same.'),
  anchor="words"))

# 11. FAQ + JSON-LD + CTA ---------------------------------------------------------
acc = ''
for i, (q, a) in enumerate(FAQ, start=1):
    tab_id = f"1755300000{i:03d}-installation-artist-faq-{i}"
    acc += (f'[vc_tta_section title="{q}" tab_id="{tab_id}"][vc_column_text css=""]\n'
            f'<p style="text-align: center;">{a}</p>\n[/vc_column_text][/vc_tta_section]')

schema = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
          + ','.join('{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
                     % (__import__("json").dumps(q), __import__("json").dumps(a)) for q, a in FAQ)
          + ']}</script>')
schema_b64 = base64.b64encode(urllib.parse.quote(schema, safe='').encode()).decode()

rows.append(
 '[vc_row bg_check="row-background-dark" dfd_enable_overlay=""][vc_column width="1/4"][/vc_column]'
 '[vc_column width="1/2"]' + sp(120, 100, 80, 80) +
 '[vc_column_text item_animation="transition.fadeIn"]\n'
 '<p style="text-align: center;"><span style="font-family: Qwigley; font-size: 36pt;">Questions about</span></p>\n'
 '<p style="text-align: center;"><span style="font-family: \'Bebas Neue\'; font-size: 36pt;">Installation art?</span></p>\n'
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

# 12. rev slider band ---------------------------------------------------------------
rows.append('[vc_row dfd_row_config="full_width_content"][vc_column]'
            '[rev_slider slidertitle="Oddview — C: Youtube Hero TV Credit" alias="oddview-c-youtube-hero-1"]'
            '[/vc_column][/vc_row]')

# 13. Portfolio trio ----------------------------------------------------------------
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
 '<h2 style="text-align: center;"><span style="font-family: \'Bebas Neue\'; font-size: 36pt;">installation work?</span></h2>\n'
 '[/vc_column_text]' + sp(60, 60, 40, 40) +
 '[vc_row_inner][vc_column_inner width="1/3"]' + portfolio(14669) + sp(90, 90, 60, 60) + '[/vc_column_inner]'
 '[vc_column_inner width="1/3"]' + portfolio(14808) + sp(90, 90, 60, 60) + '[/vc_column_inner]'
 '[vc_column_inner width="1/3"]' + portfolio(14868, 40) + sp(60, 60, 40, 40) + '[/vc_column_inner][/vc_row_inner]'
 + sp(60, 60, 30, 30) +
 '[vc_single_image image="11978" img_size="50x50" alignment="center" style="vc_box_outline_circle_2" '
 'image_opacity="70" onclick="custom_link" link="https://www.oddtoe.com/contact-oddtoe/"]'
 + sp(90, 90, 60, 60) + '[/vc_column][/vc_row]')

# 14. Contact form ------------------------------------------------------------------
rows.append(
 '[vc_row bg_check="row-background-dark" dfd_enable_overlay="" anchor="form" bg_type="canvas_animated"][vc_column]'
 '[dfd_heading subtitle_google_fonts="yes" subtitle_custom_fonts="font_family:Qwigley%3Aregular" style="style_02" '
 'subtitle="Commission an installation artist who designs, builds, and installs it." '
 'title_font_options="tag:h2|font_family:BebasNeueRegular" subtitle_font_options="tag:h3"]'
 'Interested in working with Oddtoe?[/dfd_heading]' + sp(30, 30, 20, 20) +
 '[gravityform id="1" title="false" description="false" ajax="false"]' + sp(40, 30, 20, 20) +
 '[/vc_column][/vc_row]')

# ------------------------------------------------------------------- output ---
YOAST = ('<!-- YOAST SEO TITLE: Installation Artist in Melbourne | Oddtoe | '
         'META DESCRIPTION: Oddtoe is a Melbourne installation artist building topiary, robotics, kinetic and '
         'projection pieces for galleries, festivals, venues and brand activations. -->\n')

# The Yoast block is NOT written into the body: WordPress wpautop-wraps a leading HTML
# comment in a <p>, which renders as a 22px + 17px margin empty block ABOVE the hero and
# kills the full-bleed top (found on 16136, 16 Aug 2026). Yoast values go in the real
# Yoast fields in wp-admin; they are printed here for the handoff instead.
body = ''.join(rows)
with io.open(OUT, 'w', encoding='utf-8') as f:
    f.write(body)
print(YOAST.strip())

print("wrote", OUT, len(body), "chars,", len(rows), "rows")
print("carousel images:", CAROUSEL)
print("faq entries:", len(FAQ))
