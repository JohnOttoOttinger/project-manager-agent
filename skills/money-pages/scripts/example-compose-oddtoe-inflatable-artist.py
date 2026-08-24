#!/usr/bin/env python3
# Compose the Oddtoe "Inflatable Artist" page on the Installation Artist (11178) template,
# with ONE template change: the FAQ row gains the homepage's 5-bubble left column (row 11).
# Output: inflatable-artist.html  (WPBakery raw body, ready for wp-post.sh)
#
# Slug decision (Aug 2026): /artist-designer/inflatable-artist/ — "artist" not "designer".
#   "inflatable designer" SERPs are wall-to-wall PVC manufacturers (Creative Inflatables, IDW,
#   Inflatable Design Group) selling 10-15 day turnarounds; "inflatable artist" returns named
#   practitioners (Steve Messam, Luke Jerram, Ant Farm) and commissioning programmes. Oddtoe's
#   moat is owned IP + humour = authorship, so claim the authorship word. "inflatable designer",
#   "custom giant inflatables" and "advertising inflatables" are covered in body copy + Yoast.
#
# PROOF CONSTRAINT: Oddtoe has NO delivered inflatable projects (brands.md media list =
#   projection, installation, topiary, generative-AI animation, comedy; no inflatable assets on
#   disk; sourcing is at supplier stage, factory trip ~Sept 2026). banned.md rule 3 forbids
#   invented projects, so NOTHING on this page claims past inflatable work. Every gap needing
#   Otto is marked [Otto: ...] and must be resolved before publish.
import base64, urllib.parse, io, os, json, re

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inflatable-artist.html")

# ─────────────────────────── IMAGE IDS ───────────────────────────
# Bubbles beside the FAQ. Swapped off the generic homepage characters to inflatables (Otto, 21 Aug):
# generic characters next to "Questions about giant inflatables?" was a missed connection.
# Chosen for CONTRAST and silhouette — these render as 80-160px circles, so the white-on-pale
# renders (16200/16201/16202/16203/16204) would read as pale blobs at that size and are excluded.
# Biggest slot gets the boldest image.
BUBBLES = [
    (16192,  "80x80",  "right",  "expandIn"),   # acorn character — simple silhouette, reads small
    (16197, "140x140", "",       "shrinkIn"),   # blue walk-in monster — strong blue
    (16199, "115x115", "center", "expandIn"),   # eyeball bubble — the odd one, alone in the middle row
    (16195, "120x120", "right",  "shrinkIn"),   # illuminated sphere — already a circle, ideal crop
    (16198, "160x160", "",       "expandIn"),   # orange octopus at a street festival — boldest, biggest slot
]
# REAL inflatables imagery, uploaded 21 Aug 2026 (Otto's set). Hero stays 16:9 (canvas background
# behind the h1); carousel images are square, they render at 250x250 with a 10px radius.
HERO_BG  = 16191   # giant acorn character, Australian paddock — 1820x1024
CAROUSEL = [
    # Sequenced design -> built, so the strip argues the "3D design resource" case as it scrolls.
    16194,  # panel-pattern render, eggs            [design]
    16192,  # acorn character, paddock              [built]
    16203,  # shell-creature render, panel lines    [design]
    16196,  # shell creature at scale, people in shot [built]
    16200,  # dome concept render                   [design: concept]
    16202,  # dome panel/seam render                [design: engineering]
    16201,  # the same dome built and walk-in       [built]  <- concept > engineering > built, adjacent
    16197,  # walk-in monster with doorway, festival[built]
    16198,  # octopus character, street crowd       [built]
    16199,  # eyeball bubble, field at dusk         [built]
    16193,  # eggs at a corporate campus            [built]
    16195,  # illuminated sphere at night           [built]
]
PORTFOLIO = [(14669, 20), (14808, 20), (14868, 40)]   # [Otto: confirm] trio

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

# FAQ — (icon, question, answer). Icons are FontAwesome 5 names, matching the homepage row.
# COMPLIANCE NOTE (21 Aug 2026, Otto's call): NOTHING here claims Oddtoe holds certification.
# sourcing/references/suppliers.md lists every factory as an unverified candidate ("confirm on first
# contact"), and CE is an EU regime that does not apply in Australia anyway. These answers instead show
# knowledge of what an Australian site actually triggers — AS/NZS 1170.2 wind actions, AS 1530.3 fire
# indices indoors, AS 3533.4.1 for public-entry devices. Authority without a promise. Revisit once the
# factories are vetted and Oddtoe holds real documentation it can produce on request.
FAQ = [
 ("fas fa-wind",
  "What is an inflatable artist?",
  "An inflatable artist works out what the object should be and how it holds its shape. It is <strong>3D design "
  "work</strong>: modelling the character, testing how it reads from a hundred metres away and from directly "
  "underneath, then breaking that shape into <strong>panels a fabricator can cut and sew</strong>. Oddtoe designs the "
  "piece and hands over a <strong>finished pattern set</strong>."),
 ("fas fa-cube",
  "Can Oddtoe design an inflatable if someone else is manufacturing it?",
  "Yes, and agencies with an existing factory relationship often work this way. Oddtoe develops the <strong>character "
  "and the 3D model</strong>, produces the <strong>client-facing renders</strong>, and delivers a <strong>pattern "
  "set</strong> your own fabricator can build from. On that arrangement Oddtoe is the design resource on the job and "
  "your factory stays the supplier."),
 ("fas fa-dollar-sign",
  "How much does a giant custom inflatable cost?",
  "Cost is driven by <strong>height</strong>, how many separate panels the shape needs, whether it is <strong>lit from "
  "inside</strong>, whether the <strong>public can enter it</strong>, and how long it stays up. A single figure and a "
  "walk-in tunnel with lighting are very different budgets. Oddtoe quotes each brief individually &mdash; send the "
  "site, the dates, and a rough height."),
 ("fas fa-expand-arrows-alt",
  "How big can a large-scale inflatable be?",
  "Custom display inflatables are commonly made from about <strong>4 metres up to 20 metres tall</strong>, and walk-in "
  "structures spread further across the ground than they rise. The limit is usually set by the site: <strong>available "
  "anchor points</strong>, wind exposure, overhead clearance, and how much <strong>ballast</strong> can physically be "
  "brought in."),
 ("far fa-clock",
  "How long does it take to design and make one?",
  "Allow <strong>four to eight weeks</strong>. Design and pattern work take <strong>one to two weeks</strong>, "
  "fabrication <strong>two to three</strong>, and freight the rest. Rush builds are possible when the shape is simple. "
  "Booking the fabrication slot early is what protects the date."),
 ("fas fa-clipboard-check",
  "What approvals, engineering and insurance do giant inflatables need in Australia?",
  "It depends on the venue and on whether the public can enter the piece. Expect to be asked for an <strong>engineering "
  "design certificate</strong> covering hold-down ballast and a maximum design wind speed as a three-second gust under "
  "<strong>AS/NZS 1170.2</strong>, a wind management plan, and <strong>public liability cover</strong>. Indoor and "
  "shopping-centre sites also want fire-retardant test evidence against <strong>AS 1530.3</strong>. Anything the public "
  "enters or bounces on counts as an amusement device under <strong>AS 3533.4.1</strong>, which is a heavier regime "
  "again. Oddtoe works out which of these a site triggers during design, so the build is specified to suit the site "
  "from the start."),
 ("fas fa-sync-alt",
  "Can an inflatable be reused at another event?",
  "Usually. A giant inflatable <strong>packs into crates</strong>, travels as freight, and goes back up at the next "
  "site with the same blowers. <strong>Seasonal pieces</strong> are common &mdash; the same character returns each year "
  "and stores flat in between."),
 ("fas fa-map-marker-alt",
  "Where is Oddtoe based, and can you deliver internationally?",
  "Oddtoe designs from <strong>Melbourne, Australia</strong>, and finished pieces <strong>ship worldwide</strong> "
  "direct from the fabricator, so the studio's location does not limit where a piece can stand. Installation is a "
  "separate decision: plenty of clients use their own local crew, and where you would rather Oddtoe ran the install, "
  "<strong>travel and time are quoted up front</strong>."),
]

# The visible accordion carries the <strong> markup; the FAQPage JSON-LD gets plain text.
def plain(t):
    return re.sub(r"<[^>]+>", "", t).replace("&mdash;", "\u2014").replace("&agrave;", "\u00e0")

PAGE_STYLES = '[vc_raw_html]JTNDc3R5bGUlM0UlMjNoZXJvJTIwLmRmZC1yb3ctYmctY2FudmFzJTdCYmFja2dyb3VuZC1wb3NpdGlvbiUzQWNlbnRlciUyMGNlbnRlciUyMCUyMWltcG9ydGFudCU3RCU0MG1lZGlhJTIwJTI4bWluLXdpZHRoJTNBODAwcHglMjklN0IudmNfaW5uZXIlMjAuY29sdW1ucy50aHJlZSU3QnBhZGRpbmctbGVmdCUzQTIwcHglMjAlMjFpbXBvcnRhbnQlM0JwYWRkaW5nLXJpZ2h0JTNBMjBweCUyMCUyMWltcG9ydGFudCU3RCU3RCUzQyUyRnN0eWxlJTNF[/vc_raw_html]'

rows = []

# 1. HERO ---------------------------------------------------------------------
rows.append(
 '[vc_row bg_check="row-background-dark" dfd_bg_style="canvas" dfd_bg_image_canvas="%d" '
 'dfd_bg_image_repeat_canvas="no-repeat" dfd_overlay_color="#000000" dfd_overlay_pattern="transperant" '
 'dfd_overlay_pattern_opacity="50" dfd_row_config="full_width_content" dfd_bg_color_value="#241834" '
 'anchor="hero"][vc_column]' % HERO_BG + PAGE_STYLES
 + sp(520, 520, 340, 270) +
 '[dfd_heading enable_delimiter="" style="style_02" subtitle="Spectacle you can stand under" '
 'title_font_options="tag:h1|font_family:BebasNeueRegular|letter_spacing:0" '
 'subtitle_font_options="tag:h2|line_height:20" heading_margin="margin-bottom:10px;" '
 'subheading_margin="margin-bottom:10px;"]Inflatable Artist[/dfd_heading]'
 + sp(700, 580, 480, 430) +
 '[/vc_column][/vc_row]')

# 2. INTRO --------------------------------------------------------------------
intro_a = ARVO.format(
  f'{CANONICAL} As an <strong>inflatable artist</strong>, Oddtoe designs objects built to be photographed — '
  '<strong>giant characters</strong>, walk-in environments, illuminated night pieces and oversized product replicas '
  'that make people stop in the street and want a picture of themselves underneath.')
intro_b = ARVO.format(
  'The studio works as a <strong>3D design resource</strong> first. Most briefs arrive with a site, a budget and no '
  'settled idea of what the object should be. Oddtoe takes it from sketch to a model a client can be walked around, '
  'then hands a fabricator the pattern set. See the studio&#8217;s '
  f'{link("https://www.oddtoe.com/experiential-marketing/", "experiential marketing services")} or the '
  f'{link("https://www.oddtoe.com/brand-activation-ideas/", "brand activation ideas")} list.')

rows.append(
 '[vc_row bg_check="row-background-dark"][vc_column]' + sp(80) +
 '[dfd_heading style="style_02" subtitle="Characters, environments, and night pieces at building scale" '
 'title_font_options="tag:h2|font_family:BebasNeueRegular|letter_spacing:0" '
 'subtitle_font_options="tag:h3|font_family:QwigleyRegular" '
 'heading_margin="margin-bottom:10px;"]Giant Inflatables &amp; Inflatable Art[/dfd_heading]'
 + sp(20, 20, 15, 10) +
 '[vc_column_text css=""]\n'
 '<p style="text-align: center;"><strong><em>Updated August 2026</em></strong></p>\n'
 '[/vc_column_text]'
 + sp(30, 30, 20, 20) +
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
 'subtitle="Characters built to be seen from the other end of the street" '
 'heading_margin="margin-bottom:10px;"]Inflatable Artist &amp; Character Designer[/dfd_heading]'
 + sp(10) + '[/vc_column][/vc_row]')

# 4. CAROUSEL -----------------------------------------------------------------
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

# 5. What is an inflatable artist? --------------------------------------------
rows.append(qsection(
  "What Is an Inflatable Artist?",
  "A 3D designer who works in air",
  ARVO.format(
    'An <strong>inflatable artist</strong> is responsible for the form. The work is '
    '<strong>3D design</strong>: modelling the character, checking how it reads from a hundred metres away and from '
    'directly beneath, then breaking that shape into panels a fabricator can cut and sew.') + '\n\n' + ARVO.format(
    'The medium has a long history in art. Ant Farm were building architectural-scale inflatables in 1970, and the '
    'form now runs from gallery pieces through to the lit night sculptures that hold a festival crowd after dark.'),
  ARVO.format(
    'Plenty of companies will manufacture an inflatable to supplied dimensions. Fewer will work out what the object '
    'should be. Oddtoe is engaged at that earlier stage, by agencies, producers and councils who bring the studio in '
    'before there is anything to quote.') + '\n\n' + ARVO.format(
    'Closely related Oddtoe practices often end up inside the same commission: '
    f'{link("https://www.oddtoe.com/artist-designer/installation-artist/", "installation art")} and '
    f'{link("https://www.oddtoe.com/artist-designer/kinetic-sculptor/", "kinetic sculpture")}.'),
  anchor="what", one_page="What?", parallax=True))

# 6. What can Oddtoe make? ----------------------------------------------------
rows.append(qsection(
  "What Can Oddtoe Make?",
  "Characters, walk-ins, night pieces, mascots, and replicas",
  ARVO.format(
    '<strong>Giant brand characters</strong>, walk-in environments, illuminated night pieces, wearable mascot costumes, '
    'and oversized food or product replicas. Most briefs land in one of those <strong>five</strong>, and several can be combined '
    'into one site: a character by day that lights from the inside after dark.') + '\n\n' + ARVO.format(
    'The starting point is usually a character. Oddtoe owns a cast of them — see '
    f'{link("https://www.oddtoe.com/artist-designer/character-designer/", "character design")} — and an existing '
    'character survives being scaled to ten metres better than a logo does.'),
  ARVO.format(
    f'&#8226; <strong>Giant characters</strong> — a single figure, 4m and up<br />'
    f'&#8226; <strong>Walk-in environments</strong> — arches, domes, tunnels people enter<br />'
    f'&#8226; <strong>Illuminated night pieces</strong> — lit from within for after dark<br />'
    f'&#8226; <strong>Wearable mascot costumes</strong> — roaming, crowd-facing<br />'
    f'&#8226; <strong>Product replicas</strong> — the oversized bottle, jar, or burger') + '\n\n' + ARVO.format(
    'The <strong>3D model</strong> is reusable. The same asset that proves the piece to a client produces pitch '
    'renders, animated content for screens or '
    f'{link("https://www.oddtoe.com/artist-designer/projection-artist/", "projection")}, and social cutdowns. Related '
    f'studio practices: {link("https://www.oddtoe.com/artist-designer/prop-designer-maker/", "props and fabrication")} '
    f'and {link("https://www.oddtoe.com/artist-designer/topiarist/", "topiary and planted forms")}.')))

# 7. COMPARISON TABLE ---------------------------------------------------------
TH = ('padding: 14px 18px; text-align: left; background-color: #180f0c !important; border: none !important; '
      'border-bottom: 2px solid #ddccb1 !important; font-family: \'Bebas Neue\', sans-serif; font-size: 21px; '
      'font-weight: normal; letter-spacing: 1px; color: #ffffff !important;')
def td(bg):
    return (f'padding: 12px 18px; text-align: left; background-color: {bg} !important; border: none !important; '
            f'border-bottom: 1px solid #35251d !important; color: #ffffff !important;')

TABLE_ROWS = [
 ("What it is",
  "A designed sculptural form, made as a one-off",
  "A branded shape made for a campaign",
  "A structure the public walks inside"),
 ("Typical size",
  "4m to 20m tall",
  "3m to 10m tall",
  "Low but wide — arches, domes, tunnels"),
 ("Where it lives",
  "Festivals, galleries, public art sites, parks",
  "Shopping centres, expos, sports grounds, retail",
  "Festival grounds, expos, family events"),
 ("How long it stays up",
  "Days to a season",
  "Days to a few weeks",
  "Days, usually staffed while open"),
 ("Who commissions it",
  "Festivals, councils, curators, property owners",
  "Marketing and activation agencies, brands",
  "Event producers, councils, shopping centres"),
 ("Site requirements",
  "Anchor points or ballast, blower power, wind plan",
  "Anchor points, blower power, run schedule",
  "Flat footprint, ballast, staffed entry, wind plan"),
 ("What Oddtoe delivers",
  "Concept, character, patterns, fabrication, install",
  "Concept, artwork, fabrication, install, run",
  "Concept, layout, fabrication, install, run"),
]
tbody = ''
for i, (crit, a, b, c) in enumerate(TABLE_ROWS):
    bg = '#180f0c' if i % 2 == 0 else '#281c16'
    tbody += (f'<tr><td style="{td(bg)}"><strong>{crit}</strong></td>'
              f'<td style="{td(bg)}">{a}</td><td style="{td(bg)}">{b}</td><td style="{td(bg)}">{c}</td></tr>\n')

table_html = (
 '<div style="overflow-x: auto;">\n'
 '<table style="width: 100%; border-collapse: collapse !important; background-color: #180f0c !important; border: none !important;">\n'
 '<thead>\n<tr>'
 f'<th scope="col" style="{TH} white-space: nowrap;">&nbsp;</th>'
 f'<th scope="col" style="{TH}">Inflatable art</th>'
 f'<th scope="col" style="{TH}">Advertising inflatable</th>'
 f'<th scope="col" style="{TH}">Walk-in structure</th>'
 '</tr>\n</thead>\n<tbody>\n' + tbody + '</tbody>\n</table>\n</div>')

rows.append(
 '[vc_row bg_check="row-background-dark" dfd_enable_overlay="" dfd_row_responsive_enable="dfd-row-responsive-enable" '
 'responsive_styles="padding_left_mobile:10|padding_right_mobile:10"][vc_column]' + sp(60, 60, 50, 40) +
 '[dfd_heading enable_delimiter="" style="style_02" '
 'title_font_options="tag:h2|font_family:BebasNeueRegular|letter_spacing:0" '
 'subtitle_font_options="tag:h3|font_family:QwigleyRegular" '
 'subtitle="Which one is your brief?" heading_margin="margin-bottom:10px;"]'
 'Inflatable Art, Advertising Inflatable, or Walk-In Structure?[/dfd_heading]' + sp(20) +
 '[vc_row_inner][vc_column_inner width="1/6"][/vc_column_inner][vc_column_inner width="2/3"][vc_column_text css=""]'
 + ARVO.format('Three things get ordered using the same word. This table sets out what each one is, where it '
               'goes, and what Oddtoe hands over.')
 + '\n\n' + table_html +
 '[/vc_column_text][/vc_column_inner][vc_column_inner width="1/6"][/vc_column_inner][/vc_row_inner]'
 + sp(60, 60, 40, 40) + '[/vc_column][/vc_row]')

# 8. Who commissions ----------------------------------------------------------
rows.append(qsection(
  "Who Commissions Large-Scale Inflatables?",
  "Brands, festivals, councils, and shopping centres",
  ARVO.format(
    '<strong>Marketing and activation agencies</strong>, festivals and event producers, local councils, shopping '
    'centres, and museums doing placemaking work. Each wants a different outcome from the same object, and the design '
    'changes accordingly.') + '\n\n' + ARVO.format(
    'Australia&#8217;s event promotion and management industry is worth $13.1 billion in 2026, according to '
    f'{extlink("https://www.ibisworld.com/au/market-size/event-promotion-management-services/", "IBISWorld")}. '
    'Inflatables sit inside that spend as the hero object — the thing on site that is visible from the car park.'),
  ARVO.format(
    '<strong>Agencies and brands</strong> commission a character or a product replica as the centrepiece of an '
    f'activation. See {link("https://www.oddtoe.com/experiential-marketing/", "experiential marketing")} and the '
    f'{link("https://www.oddtoe.com/experiential-marketing-agencies/", "agency list")}.') + '\n\n' + ARVO.format(
    '<strong>Festivals and event producers</strong> commission night pieces and walk-in structures that hold a crowd '
    'in one part of the site.') + '\n\n' + ARVO.format(
    '<strong>Councils and placemaking teams</strong> commission seasonal pieces that draw foot traffic into a precinct '
    'and pack away afterwards.') + '\n\n' + ARVO.format(
    '<strong>Shopping centres and retail</strong> commission the returning seasonal install, photographed by every '
    'family who walks past it.'),
  anchor="who"))

# 9. Process ------------------------------------------------------------------
rows.append(qsection(
  "How Does an Oddtoe Inflatable Get Made?",
  "Designed in 3D, built by specialists, planned around the site",
  ARVO.format(
    '<strong>Six steps</strong>: brief and site, character and concept in 3D, pattern and engineering, fabrication, '
    'test inflate, then install and run. Design sits with the studio; fabrication goes to a specialist inflatable '
    'maker.') + '\n\n' + ARVO.format(
    '<strong>1. Brief and site.</strong> Footprint, anchor points or ballast, overhead clearance, wind exposure, '
    'blower power, and how long the piece has to stand.') + '\n\n' + ARVO.format(
    '<strong>2. Character and concept.</strong> Modelled in <strong>3D</strong> so the piece can be seen at true scale '
    'in the actual space before any fabric is cut. Early exploration uses '
    f'{link("https://www.oddtoe.com/what-is-generative-ai-animation/", "generative AI")}; the drawings a fabricator '
    'works from are drawn properly.'),
  ARVO.format(
    '<strong>3. Pattern and engineering.</strong> The form is broken into panels, seams are placed where they will not '
    'distort the shape, and blower sizing, internal baffling and anchor points are specified.') + '\n\n' + ARVO.format(
    '<strong>4. Fabrication.</strong> Built by a specialist inflatable maker. Material and test documentation are '
    'specified here against the venue&#8217;s own rules, because an open field and a shopping centre ask for different '
    'paperwork.') + '\n\n' + ARVO.format(
    '<strong>5. Test inflate.</strong> Fully inflated and photographed at the factory before it ships.') +
  '\n\n' + ARVO.format(
    '<strong>6. Install and run.</strong> Anchored and ballasted on the agreed day, to a wind management plan that '
    'sets the speed at which the piece comes down.'),
  anchor="how"))

# 10. Why Oddtoe makes inflatables --------------------------------------------
rows.append(qsection(
  "Why Oddtoe Makes Inflatables",
  "The thing people stand under and photograph",
  ARVO.format(
    'A giant inflatable is built to be photographed. Someone walking past has to stop, look up, and want a picture of '
    'themselves underneath it. Everything else about the piece follows from that.') + '\n\n' + ARVO.format(
    'Most of them fail at it because they start from a logo. A logo at ten metres is still a logo. A character at ten '
    'metres reads as somebody who has turned up.'),
  ARVO.format(
    'So the design covers the moment as well as the object: where a person stands, what is behind them in the frame, '
    'and what the thing appears to be doing while they are there. A figure that leans out over a crowd or reaches down '
    'gives people a position to take up. A smooth branded shape gives them nothing to work with.') + '\n\n' + ARVO.format(
    'Inflatables are the best. Air is the cheapest and most reliable medium to design in, and the easiest to ship. '
    'Fun shapes, odd forms. Then voil&agrave; &mdash; a two-storey sculpture.'),
  anchor="words"))

# 11. FAQ ROW — with the homepage 5-bubble left column (TEMPLATE CHANGE) -------
bubble_col_shadow = ('col_inner_shadow="box_shadow_enable:disable|shadow_horizontal:0|shadow_vertical:15|'
                     'shadow_blur:50|shadow_spread:0|box_shadow_color:rgba(0%2C0%2C0%2C.35)" '
                     'col_inner_shadow_hover="box_shadow_enable:disable|shadow_horizontal:0|shadow_vertical:15|'
                     'shadow_blur:50|shadow_spread:0|box_shadow_color:rgba(0%2C0%2C0%2C.35)"')
def bubble(idx):
    img, size, align, anim = BUBBLES[idx]
    a = f'alignment="{align}" ' if align else ''
    return (f'[vc_single_image image="{img}" img_size="{size}" {a}style="vc_box_border_circle_2" css="" '
            f'item_animation="transition.{anim}"]')

bubbles_left = (
 '[vc_column width="1/3" offset="vc_hidden-xs" '
 'col_shadow="box_shadow_enable:disable|shadow_horizontal:0|shadow_vertical:15|shadow_blur:50|shadow_spread:0|'
 'box_shadow_color:rgba(0%2C0%2C0%2C.35)" '
 'col_shadow_hover="box_shadow_enable:disable|shadow_horizontal:0|shadow_vertical:15|shadow_blur:50|shadow_spread:0|'
 'box_shadow_color:rgba(0%2C0%2C0%2C.35)"]'
 + sp(80, 70, 50, 40) +
 # 2 - 1 - 2 scatter, spread down the column so it tracks the accordion's height.
 # Stagger comes from alignment only: no vc_custom_* padding class (that CSS is
 # generated per-page and would NOT exist on this page — silent no-op if copied).
 '[vc_row_inner]'
 f'[vc_column_inner width="1/2" {bubble_col_shadow}]' + bubble(0) + '[/vc_column_inner]'
 '[vc_column_inner width="1/2"]' + bubble(1) + '[/vc_column_inner]'
 '[/vc_row_inner]'
 + sp(70, 60, 45, 30) +
 '[vc_row_inner]'
 f'[vc_column_inner width="1/1" {bubble_col_shadow}]' + bubble(2) + '[/vc_column_inner]'
 '[/vc_row_inner]'
 + sp(70, 60, 45, 30) +
 '[vc_row_inner]'
 f'[vc_column_inner width="1/2" {bubble_col_shadow}]' + bubble(3) + '[/vc_column_inner]'
 f'[vc_column_inner width="1/2" {bubble_col_shadow}]' + bubble(4) + '[/vc_column_inner]'
 '[/vc_row_inner]'
 + sp(40, 30, 20, 20) + '[/vc_column]')

acc = ''
for i, (icon, q, a) in enumerate(FAQ, start=1):
    tab_id = f"1756100000{i:03d}-inflatable-artist-faq-{i}"
    acc += (f'[vc_tta_section i_icon_fontawesome="{icon}" add_icon="true" title="{q}" tab_id="{tab_id}"]'
            f'[vc_column_text css=""]\n<p style="text-align: left;">{a}</p>\n[/vc_column_text][/vc_tta_section]')

schema = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
          + ','.join('{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
                     % (json.dumps(q), json.dumps(plain(a))) for _, q, a in FAQ)
          + ']}</script>')
schema_b64 = base64.b64encode(urllib.parse.quote(schema, safe='').encode()).decode()

rows.append(
 '[vc_row bg_check="row-background-dark" dfd_enable_overlay="" one_page_title="Questions" anchor="faq"]'
 + bubbles_left +
 '[vc_column width="2/3"]' + sp(80, 70, 50, 40) +
 '[vc_column_text item_animation="transition.fadeIn"]\n'
 '<p style="text-align: center;"><span style="font-family: Qwigley; font-size: 36pt;">Questions about</span></p>\n'
 '<p style="text-align: center;"><strong><span style="font-family: \'Bebas Neue\'; font-size: 36pt;">Giant inflatables?</span></strong></p>\n'
 '[/vc_column_text]' + sp(40, 30, 20, 20) +
 '[dfd_accordion style="style-3" active_section="1" font_size="18" tab_title_google_fonts="yes" '
 'tab_title_custom_fonts="font_family:Arvo%3Aregular%2Citalic%2C700%2C700italic|'
 'font_style:700%20bold%20regular%3A700%3Anormal" icon_size="18" icon_color="#000000" active_two_px_border="on"]'
 + acc + '[/dfd_accordion]'
 + f'[vc_raw_html]{schema_b64}[/vc_raw_html]' + sp(40, 30, 20, 20) +
 '[dfd_button button_text="Contact Oddtoe" '
 'buttom_link_src="url:https%3A%2F%2Fwww.oddtoe.com%2Fcontact-oddtoe%2F|title:Contact%20Oddtoe" style="style_6" '
 'background="#8a8f6a" hover_background="#4e5041" border="border-style:none;|border-radius:5px;" '
 'hover_border="border-style:none;|border-radius:5px;"]' + sp(80, 70, 50, 50) +
 '[/vc_column][/vc_row]')

# 12. rev slider band ---------------------------------------------------------
rows.append('[vc_row dfd_row_config="full_width_content"][vc_column]'
            '[rev_slider slidertitle="Video Hero — Homepage" alias="video-hero-stained-glass-art-in-3d-1"]'
            '[/vc_column][/vc_row]')

# 13. Portfolio trio ----------------------------------------------------------
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
 '<h2 style="text-align: center;"><span style="font-family: \'Bebas Neue\'; font-size: 36pt;">large-scale work?</span></h2>\n'
 '[/vc_column_text]' + sp(60, 60, 40, 40) +
 '[vc_row_inner]'
 + ''.join(f'[vc_column_inner width="1/3"]{portfolio(pid, off)}{sp(90, 90, 60, 60)}[/vc_column_inner]'
           for pid, off in PORTFOLIO)
 + '[/vc_row_inner]' + sp(60, 60, 30, 30) +
 '[vc_single_image image="11978" img_size="50x50" alignment="center" style="vc_box_outline_circle_2" '
 'image_opacity="70" onclick="custom_link" link="https://www.oddtoe.com/contact-oddtoe/"]'
 + sp(90, 90, 60, 60) + '[/vc_column][/vc_row]')

# 14. Contact form ------------------------------------------------------------
rows.append(
 '[vc_row bg_check="row-background-dark" dfd_enable_overlay="" anchor="form" bg_type="canvas_animated"][vc_column]'
 '[dfd_heading subtitle_google_fonts="yes" subtitle_custom_fonts="font_family:Qwigley%3Aregular" style="style_02" '
 'subtitle="Commission an inflatable artist who designs the object and the moment around it." '
 'title_font_options="tag:h2|font_family:BebasNeueRegular" subtitle_font_options="tag:h3"]'
 'Interested in working with Oddtoe?[/dfd_heading]' + sp(30, 30, 20, 20) +
 '[gravityform id="1" title="false" description="false" ajax="false"]' + sp(40, 30, 20, 20) +
 '[/vc_column][/vc_row]')

# ------------------------------------------------------------------- output ---
YOAST_TITLE = "Inflatable Artist Melbourne | Giant Inflatables | Oddtoe"
YOAST_DESC  = ("Melbourne inflatable artist and 3D designer. Oddtoe designs giant custom inflatables — brand "
               "characters, walk-in structures and illuminated night pieces.")

body = ''.join(rows)
with io.open(OUT, 'w', encoding='utf-8') as f:
    f.write(body)

print(f"YOAST SEO TITLE: {YOAST_TITLE}  ({len(YOAST_TITLE)} chars)")
print(f"META DESCRIPTION: {YOAST_DESC}  ({len(YOAST_DESC)} chars)")
print("wrote", OUT, len(body), "chars,", len(rows), "rows")
print("faq entries:", len(FAQ), "| bubbles:", [b[0] for b in BUBBLES])
