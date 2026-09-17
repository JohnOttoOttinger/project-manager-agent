#!/usr/bin/env python3
# Compose the Oddtoe "Use Case: Protest & Press Day" page (16272).
# First page of the Use Cases family. The spine is a NEW reusable interactive row
# (usecase-row.html) driven by a single UC array — swap that array for the next use case.
# Output: usecase-protest.html
import base64, urllib.parse, io, os, json

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "usecase-protest.html")
ROW  = os.environ.get("UC_ROW", "/private/tmp/claude-501/-Users-Ottinger-Documents-Oddtoe---iCloud-Apple-Marketing-Oddtoe-New-Growth-Pages-2026/2a58b03a-5cf4-4272-9ddc-771176569fda/scratchpad/usecase-row.html")

SP=('[dfd_spacer screen_wide_resolution="1280" screen_wide_spacer_size="{w}" screen_normal_resolution="1024" '
    'screen_tablet_resolution="800" screen_mobile_resolution="480" screen_normal_spacer_size="{n}" '
    'screen_tablet_spacer_size="{t}" screen_mobile_spacer_size="{m}"]')
def sp(w,n=None,t=None,m=None):
    n=w if n is None else n; t=n if t is None else t; m=t if m is None else m
    return SP.format(w=w,n=n,t=t,m=m)

ARVO='<span style="font-family: Arvo;">{}</span>'
def link(u,l): return f'<strong><a class="dfd-custom-link-decorated" href="{u}">{l}</a></strong>'

CANON=('<strong>Oddtoe</strong> is an experiential design and generative-AI animation studio based in Melbourne, '
       'creating projection, installation, and animated work for events, venues, and galleries.')

FAQ=[
 ("What is this use case, exactly?",
  "A worked example. It follows one brief - a campaign with a press day and no picture - "
  "from the first question through design, fabrication, the day itself, and what the campaign still owns afterwards. "
  "The same shape applies to any object-led action."),
 ("How long does it take?",
  "Six to eight weeks from brief to press day for a set of four heads. Design and approval take the first fortnight, "
  "fabrication the next three weeks, and the rest is packing and freight. A rush is possible but it comes out of the "
  "design stage, which is the part worth protecting."),
 ("Can they be shipped outside Australia?",
  "Yes. They are built to crate, and freight and paperwork are handled from this end. Cane and paper are plant "
  "material, so treatment and certification are part of the job rather than an afterthought."),
 ("What does a set cost?",
  "<strong>Oddtoe</strong> does not publish prices. Cost is driven by how many characters, how large, how much "
  "structure each one needs, and where they have to travel. Send the brief and the date and you get a quote."),
 ("Do we need council permits?",
  "Usually not for the objects themselves - they are carried, not installed, with no power and no rigging. The permit "
  "conversation is about the assembly or the march, which the campaign is already having."),
 ("Can we use them more than once?",
  "That is the point. They go back in the crate and come out at the next action. A set built for one press day has "
  "usually paid for itself by its third outing."),
 ("Can you do the animation and projection as well?",
  "Yes, and they are designed together when the brief calls for it - the same characters animated as loops and "
  "projected after dark. See " + link("/artist-designer/projection-artist/","projection art") + " and " +
  link("/what-is-generative-ai-animation/","generative AI animation") + "."),
 ("Where is <strong>Oddtoe</strong> based?",
  "<strong>Oddtoe</strong> is based in Melbourne, Australia. Supplier and business contacts run through Berlin and "
  "Los Angeles, and those are the starting points for work in Europe and the United States."),
]

PAGE_STYLES=('[vc_raw_html]JTNDc3R5bGUlM0UlMjNoZXJvJTIwLmRmZC1yb3ctYmctY2FudmFzJTdCYmFja2dyb3VuZC1wb3NpdGlvbiUzQWNlbnRlciUyMGNlbnRlciUyMCUyMWltcG9ydGFudCU3RCU0MG1lZGlhJTIwJTI4bWluLXdpZHRoJTNBODAwcHglMjklN0IudmNfaW5uZXIlMjAuY29sdW1ucy50aHJlZSU3QnBhZGRpbmctbGVmdCUzQTIwcHglMjAlMjFpbXBvcnRhbnQlM0JwYWRkaW5nLXJpZ2h0JTNBMjBweCUyMCUyMWltcG9ydGFudCU3RCU3RCUzQyUyRnN0eWxlJTNF[/vc_raw_html]')

def qsection(heading, subtitle, a, b, anchor=None, top=60):
    at=['bg_check="row-background-dark"','dfd_enable_overlay=""','dfd_row_config="default_row_small_paddings"']
    if anchor: at.append(f'anchor="{anchor}"')
    at+=['dfd_row_responsive_enable="dfd-row-responsive-enable"',
         'responsive_styles="padding_left_mobile:10|padding_right_mobile:10"']
    return ('[vc_row '+' '.join(at)+'][vc_column]'+sp(top,top,50,40)+
      '[dfd_heading enable_delimiter="" style="style_02" '
      'title_font_options="tag:h2|font_family:BebasNeueRegular|letter_spacing:0" '
      'subtitle_font_options="tag:h3|font_family:QwigleyRegular" '
      f'subtitle="{subtitle}" heading_margin="margin-bottom:10px;"]{heading}[/dfd_heading]'+sp(20)+
      '[vc_row_inner][vc_column_inner width="1/4"][/vc_column_inner][vc_column_inner width="1/4"]'
      f'[vc_column_text css=""]{a}[/vc_column_text][/vc_column_inner][vc_column_inner width="1/4"]'
      f'[vc_column_text css=""]{b}[/vc_column_text][/vc_column_inner]'
      '[vc_column_inner width="1/4"][/vc_column_inner][/vc_row_inner]'+sp(40,40,30,30)+'[/vc_column][/vc_row]')

rows=[]

# 1 HERO
rows.append('[vc_row bg_check="row-background-dark" dfd_bg_style="canvas" dfd_bg_image_canvas="16244" '
 'dfd_bg_image_repeat_canvas="no-repeat" dfd_overlay_color="#000000" dfd_overlay_pattern="transperant" '
 'dfd_overlay_pattern_opacity="60" dfd_row_config="full_width_content" dfd_bg_color_value="#161314" anchor="hero"]'
 '[vc_column]'+PAGE_STYLES+sp(460,460,300,240)+
 '[dfd_heading enable_delimiter="" style="style_02" subtitle="One press day, one photograph" '
 'title_font_options="tag:h1|font_family:BebasNeueRegular|letter_spacing:0" '
 'subtitle_font_options="tag:h2|line_height:20" heading_margin="margin-bottom:10px;" '
 'subheading_margin="margin-bottom:10px;"]Protest &amp; Press Day[/dfd_heading]'
 +sp(620,520,420,360)+'[/vc_column][/vc_row]')

# 2 INTRO
a=ARVO.format(f'{CANON} This is a <strong>use case</strong>: what a campaign gets, and in what order, when the '
  'brief is a press day.')
b=ARVO.format('The work is designed by a <strong>political cartoonist</strong> &#8212; chief designer for a '
  'Washington DC paper, and an editorial cartoonist before that. It matters here because a rally photograph and a '
  'daily cartoon are the same problem: <strong>one frame, one argument</strong>, no second chance to explain.')
rows.append('[vc_row bg_check="row-background-dark"][vc_column]'+sp(80)+
 '[dfd_heading style="style_02" subtitle="For non-profits, grassroots campaigns, and unions" '
 'title_font_options="tag:h2|font_family:BebasNeueRegular|letter_spacing:0" '
 'subtitle_font_options="tag:h3|font_family:QwigleyRegular" '
 'heading_margin="margin-bottom:10px;"]Use Case: The Protest Press Day[/dfd_heading]'+sp(14,14,12,10)+
 '[vc_column_text css=""]</p>\n<p style="text-align: center;"><span style="font-family: Arvo; font-size: 13px; '
 'color: #8a8a95;">Updated September 2026</span></p>\n<p>[/vc_column_text]'+sp(20,20,15,10)+
 '[vc_row_inner][vc_column_inner width="1/4"][/vc_column_inner][vc_column_inner width="1/4"]'
 f'[vc_column_text css=""]{a}[/vc_column_text]'+sp(20)+'[/vc_column_inner][vc_column_inner width="1/4"]'
 f'[vc_column_text css=""]{b}[/vc_column_text]'+sp(20)+'[/vc_column_inner]'
 '[vc_column_inner width="1/4"][/vc_column_inner][/vc_row_inner]'+sp(70,70,60,50)+'[/vc_column][/vc_row]')

# 3 THE INTERACTIVE
uc=open(ROW,encoding='utf-8').read()
uc64=base64.b64encode(urllib.parse.quote(uc, safe="!*'()").encode()).decode()
rows.append('[vc_row bg_check="row-background-dark" dfd_enable_overlay="" '
 'dfd_row_responsive_enable="dfd-row-responsive-enable" '
 'responsive_styles="padding_left_mobile:10|padding_right_mobile:10" anchor="the-day"][vc_column]'
 +sp(70,70,50,40)+f'[vc_raw_html]{uc64}[/vc_raw_html]'+sp(80,80,60,50)+'[/vc_column][/vc_row]')

# 3b DRAWINGS — art in progress
U='https://www.oddtoe.com/wp-content/uploads/2026/09/'
LBL=('font-family: Arvo, Georgia, serif; font-size: 12px; font-weight:700; letter-spacing:.09em; '
     'text-transform:uppercase; color:#8a9f6a; margin:0 0 6px;')
STT=("font-family: 'Bebas Neue', BebasNeueRegular, Impact, sans-serif; font-size: 30px; line-height:1; "
     'color:#fff; margin:0 0 12px;')
BDY=('font-family: Arvo, Georgia, serif; font-size: 16px; line-height:1.62; color:rgba(255,255,255,.9); '
     'margin:0 auto; max-width:760px;')
def study(img, label, title, body):
    return ('<div style="margin:0 0 56px;">'
            f'<img src="{U}{img}" alt="" loading="lazy" '
            'style="width:100%;height:auto;display:block;border-radius:8px;" />'
            '<div style="text-align:center;margin:22px auto 0;max-width:760px;">'
            f'<p style="{LBL}">{label}</p><p style="{STT}">{title}</p><p style="{BDY}">{body}</p>'
            '</div></div>')
DRAW=('<div style="max-width:1180px;margin:0 auto;">'
 + study('oddtoe-protest-head-construction-studies.jpg', 'Study one', 'Drawing practice',
   'Everything starts on paper, on a grid. Proportions get argued out in elevation and section long before '
   'anything is cut, because a head that is wrong at this stage is wrong in cane and paper too, only more '
   'expensively. The annotations are what a fabricator actually works from.')
 + study('oddtoe-protest-head-puppet-studies.jpg', 'Study two', 'The people inside it',
   'Working out how protesters and puppeteers handle a kinetic sculpture. Where the handlers stand, how many '
   'it takes, how the weight sits over a shoulder for an hour, and how the whole thing turns a corner without '
   'hitting anyone. Safety and mobility are design problems, and they get solved on the drawing, not on the day.')
 + study('oddtoe-protest-head-monumental-scale.jpg', 'Study three', 'Ideation: a modern Trojan horse',
   'This one is a concept rather than a plan. A modern-day Trojan horse crossed with the Mount Rushmore idea of '
   'a face carved as a monument &#8212; except it arrives on a truck, stands in a street for a day, and leaves. '
   'A monument that turns up uninvited and does not stay long enough to be argued about.')
 + '</div>')
rows.append('[vc_row bg_check="row-background-dark" dfd_enable_overlay="" '
 'dfd_row_responsive_enable="dfd-row-responsive-enable" '
 'responsive_styles="padding_left_mobile:10|padding_right_mobile:10" anchor="drawings"][vc_column]'
 +sp(70,70,50,40)+
 '[dfd_heading enable_delimiter="" style="style_02" '
 'title_font_options="tag:h2|font_family:BebasNeueRegular|letter_spacing:0" '
 'subtitle_font_options="tag:h3|font_family:QwigleyRegular" '
 'subtitle="Three studies, in progress" heading_margin="margin-bottom:10px;"]'
 'The Drawings Behind the Heads[/dfd_heading]'+sp(16,16,14,12)+
 '[vc_row_inner][vc_column_inner width="1/6"][/vc_column_inner][vc_column_inner width="2/3"]'
 '[vc_column_text css=""]'
 +ARVO.format('Three working studies, each answering a different question: how the thing is drawn, how people carry it, and how far the idea goes.')+
 '[/vc_column_text][/vc_column_inner][vc_column_inner width="1/6"][/vc_column_inner][/vc_row_inner]'
 +sp(34,34,26,22)+'[vc_raw_html]'+base64.b64encode(urllib.parse.quote(DRAW, safe="!*'()").encode()).decode()+'[/vc_raw_html]'+sp(80,80,60,50)+'[/vc_column][/vc_row]')


# 4 WHAT YOU GET
rows.append(qsection("What Does a Campaign Actually Get?","Objects, artwork, and the footage afterwards",
  ARVO.format('<strong>A set of characters, built to be carried, plus the artwork they came from and the '
    'documentation from the day.</strong>')+'\n\n'+ARVO.format(
    '&#8226; <strong>Four oversized heads</strong> &#8212; cane frame, papier-m&acirc;ch&eacute; skin, matte '
    'finish<br />&#8226; <strong>The character artwork</strong> &#8212; the same designs flat, for placards, '
    'posters and social<br />&#8226; <strong>A crate</strong> they pack into and travel in<br />'
    '&#8226; <strong>Stills and video</strong> from the day, cut for news desks and for vertical'),
  ARVO.format('The artwork is the part people underestimate. The heads are built from finished character designs, '
    'so the campaign also owns a set of drawings that work on a poster, a placard, a t-shirt and a social tile '
    'without redrawing anything.')+'\n\n'+ARVO.format(
    'Where a brief calls for it, the same characters are animated as loops and projected after dark &#8212; see '
    +link("/artist-designer/projection-artist/","projection art")+' and '
    +link("/what-is-generative-ai-animation/","generative AI animation")+'. The heads and the loops are designed together, so the projection is the same character.'),
  anchor="what-you-get"))

# 5 THE CARTOONIST CREDENTIAL
rows.append(qsection("Why a Cartoonist Designs This","One frame, one argument",
  ARVO.format('A political cartoon and a protest photograph do the same job. Both get one frame to carry an '
    'argument, both are read in about a second, and both fail the same way &#8212; by needing explanation.')+
  '\n\n'+ARVO.format('<strong>Oddtoe</strong> drew editorial cartoons at college in Delaware, then worked as '
    'political cartoonist and chief designer for a Washington DC paper. That is years of deciding which single '
    'image a political story runs with, and watching which ones an editor throws away. Not an abstract skill: '
    'it is knowing the reader gives you about a second, and building for that second.'),
  ARVO.format('More recently, an illustration and cover design for a US House candidate&#8217;s fundraiser '
    '&#8212; a donkey bullying an elephant, which is exactly the kind of blunt, legible idea that survives being '
    'printed small.')+'\n\n'+ARVO.format('The same instinct decides what a protest object should be. Not the '
    'prettiest object, and not the biggest. The one a picture editor picks out of twelve on the wire.')+
  '\n\n'+ARVO.format('It also decides what to leave out. A head that needs a caption has already failed, '
    'and so has one that reads as a blob from across a square.'),
  anchor="cartoonist"))

# 6 COMPARISON TABLE
TH=('padding: 14px 18px; text-align: left; background-color: #000000 !important; border: none !important; '
    'border-bottom: 2px solid #ddccb1 !important; font-family: \'Bebas Neue\', sans-serif; font-size: 21px; '
    'font-weight: normal; letter-spacing: 1px; color: #ffffff !important;')
def td(bg):
    return (f'padding: 12px 18px; text-align: left; background-color: {bg} !important; border: none !important; '
            f'border-bottom: 1px solid #3a2f2c !important; color: #ffffff !important;')
TBL=[("What it costs","Cheap per unit, spent again every action","A large single-day hire","One build, amortised over years"),
     ("How long it lasts","One rally, if it does not rain","Struck by Monday morning","Years, in a crate between actions"),
     ("What a photo desk does","Scrolls past it","Crops it out of the frame","Runs it, because nothing else looks like it"),
     ("Who has to operate it","Whoever is holding it","A crew and a technician","Four volunteers"),
     ("What you own afterwards","Nothing","Nothing","The objects and the character artwork")]
tb=''
for i,(c1,c2,c3,c4) in enumerate(TBL):
    bg='#000000' if i%2==0 else '#140f0e'
    tb+=(f'<tr><td style="{td(bg)}"><strong>{c1}</strong></td><td style="{td(bg)}">{c2}</td>'
         f'<td style="{td(bg)}">{c3}</td><td style="{td(bg)}">{c4}</td></tr>\n')
table=('<div style="overflow-x: auto;">\n<table style="width: 100%; border-collapse: collapse !important; '
 'background-color: #000000 !important; border: none !important;">\n<thead>\n<tr>'
 f'<th scope="col" style="{TH} white-space: nowrap;">&nbsp;</th>'
 f'<th scope="col" style="{TH}">Placards</th><th scope="col" style="{TH}">A hired stage</th>'
 f'<th scope="col" style="{TH}">Four heads</th></tr>\n</thead>\n<tbody>\n'+tb+'</tbody>\n</table>\n</div>')
rows.append('[vc_row bg_check="row-background-dark" dfd_enable_overlay="" '
 'dfd_row_responsive_enable="dfd-row-responsive-enable" '
 'responsive_styles="padding_left_mobile:10|padding_right_mobile:10" anchor="compare"][vc_column]'+sp(60,60,50,40)+
 '[dfd_heading enable_delimiter="" style="style_02" '
 'title_font_options="tag:h2|font_family:BebasNeueRegular|letter_spacing:0" '
 'subtitle_font_options="tag:h3|font_family:QwigleyRegular" '
 'subtitle="Where the money actually goes" heading_margin="margin-bottom:10px;"]'
 'Placards, a Stage, or Four Heads?[/dfd_heading]'+sp(20)+
 '[vc_row_inner][vc_column_inner width="1/6"][/vc_column_inner][vc_column_inner width="2/3"][vc_column_text css=""]'
 +ARVO.format('A campaign budget usually has one line for the visible part of an action. This is what that line '
   'buys three different ways.')+'\n\n'+table+
 '[/vc_column_text][/vc_column_inner][vc_column_inner width="1/6"][/vc_column_inner][/vc_row_inner]'
 +sp(60,60,40,40)+'[/vc_column][/vc_row]')

# 7 WHO COMMISSIONS
rows.append(qsection("Who Commissions Work Like This?","Campaigns, unions, and NGOs",
  ARVO.format('Non-profits and NGOs, grassroots campaigns, unions, advocacy organisations, and political '
    'campaigns. What they have in common is a date, a message, and a press list.')+'\n\n'+ARVO.format(
    '<strong>Campaigns with a fixed date</strong> commission for a launch, a vote, or a summit, where one day '
    'has to produce a month of coverage.')+'\n\n'+ARVO.format(
    '<strong>Unions</strong> commission objects that get used repeatedly, because the same members turn out '
    'several times a year.'),
  ARVO.format('<strong>NGOs and advocacy organisations</strong> commission a visual identity that survives being '
    'used by volunteers in three cities without a designer present.')+'\n\n'+ARVO.format(
    '<strong>Political campaigns</strong> commission artwork and objects the same way they commission any other '
    'asset. <strong>Oddtoe</strong> has done fundraiser illustration for a US House candidate.')+'\n\n'+ARVO.format(
    'Agencies working for any of the above are welcome too: see '
    +link("/experiential-marketing/","experiential marketing")+'.'),
  anchor="who"))

# 8 IN ODDTOE'S WORDS
rows.append(qsection("Why Oddtoe Makes Protest Work","The bit that is not a service",
  ARVO.format('Street art is punk rock for visual artists. You do not need a gallery, a commission or anyone&#8217;s '
    'permission, and the work is seen by people who did not choose to look at art that day. Few art forms can '
    'say that.')+'\n\n'+ARVO.format(
    'Most of why this subject interests me sits right there. An object carried down a street is doing the same thing as a '
    'piece pasted on a wall at four in the morning: putting an argument where people actually are.'),
  ARVO.format('I make my own work as well as client work, and sculpture street art is where I want to take that '
    'next. So a protest brief is not a category I added to a service list. It is the closest thing to what I would '
    'be making anyway.')+'\n\n'+ARVO.format('The practical upside for a campaign is that the person designing the '
    'object has a stake in whether it works. I want the photograph to be good for the same reason you do.'),
  anchor="words"))

# 9 FAQ + SCHEMA
import re as _re
def plain(t): return _re.sub(r"<[^>]+>","",t).replace("&#8217;","’").replace("&#8212;","—").replace("&#8226;","•")
acc=''
for i,(q,ans) in enumerate(FAQ,1):
    acc+=(f'[vc_tta_section title="{plain(q)}" tab_id="1757300000{i:03d}-usecase-protest-faq-{i}"]'
          f'[vc_column_text css=""]\n<p style="text-align: center;">{ans}</p>\n[/vc_column_text][/vc_tta_section]')
schema=('<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
        +','.join('{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
                  %(json.dumps(plain(q)),json.dumps(plain(a))) for q,a in FAQ)+']}</script>')
s64=base64.b64encode(urllib.parse.quote(schema, safe="!*'()").encode()).decode()
rows.append('[vc_row bg_check="row-background-dark" dfd_enable_overlay=""][vc_column width="1/4"][/vc_column]'
 '[vc_column width="1/2"]'+sp(110,90,70,70)+
 '[vc_column_text item_animation="transition.fadeIn"]\n'
 '<p style="text-align: center;"><span style="font-family: Qwigley; font-size: 36pt;">Questions about</span></p>\n'
 '<p style="text-align: center;"><span style="font-family: \'Bebas Neue\'; font-size: 36pt;">Protest work?</span></p>\n'
 '[/vc_column_text]'+sp(40,30,20,20)+
 '[dfd_accordion style="style-3" active_section="1" font_size="18" tab_title_google_fonts="yes" '
 'tab_title_custom_fonts="font_family:Arvo%3Aregular%2Citalic%2C700%2C700italic|'
 'font_style:700%20bold%20regular%3A700%3Anormal" icon_size="14"]'+acc+'[/dfd_accordion]'
 +f'[vc_raw_html]{s64}[/vc_raw_html]'+sp(40,30,20,20)+
 '[dfd_button button_text="Contact Oddtoe" '
 'buttom_link_src="url:https%3A%2F%2Fwww.oddtoe.com%2Fcontact-oddtoe%2F|title:Contact%20Oddtoe" style="style_6" '
 'background="#8a8f6a" hover_background="#4e5041" border="border-style:none;|border-radius:5px;" '
 'hover_border="border-style:none;|border-radius:5px;"]'+sp(110,90,60,60)+
 '[/vc_column][vc_column width="1/4"][/vc_column][/vc_row]')

# 10 PORTFOLIO TRIO (cartooning / satire)
def pf(pid,off=20):
    return (f'[dfd_portfolio_module items="single" single_custom_post_item="{pid}" items_offset="{off}" columns="3" '
            'sort_panel="" enabled_excerpt="" enabled_read_more="" enabled_share="" enabled_comments="" '
            'enabled_likes="" enabled_anim_com_like="" image_width="900" image_height="600" style="fitRows" '
            'title_font_options="tag:div"]')
rows.append('[vc_row bg_check="row-background-dark" dfd_enable_overlay="" one_page_title="More" anchor="more"]'
 '[vc_column]'+sp(100,90,80,80)+
 '[vc_column_text css="" item_animation="transition.fadeIn"]\n'
 '<p style="text-align: center;"><span style="font-family: Qwigley; font-size: 36pt;">Interested in seeing more&#8230; </span></p>\n\n'
 '<h2 style="text-align: center;"><span style="font-family: \'Bebas Neue\'; font-size: 36pt;">drawn work?</span></h2>\n'
 '[/vc_column_text]'+sp(60,60,40,40)+
 '[vc_row_inner][vc_column_inner width="1/3"]'+pf(15269)+sp(90,90,60,60)+'[/vc_column_inner]'
 '[vc_column_inner width="1/3"]'+pf(14059)+sp(90,90,60,60)+'[/vc_column_inner]'
 '[vc_column_inner width="1/3"]'+pf(12586,40)+sp(60,60,40,40)+'[/vc_column_inner][/vc_row_inner]'
 +sp(60,60,30,30)+
 '[vc_single_image image="11978" img_size="50x50" alignment="center" style="vc_box_outline_circle_2" '
 'image_opacity="70" onclick="custom_link" link="https://www.oddtoe.com/contact-oddtoe/"]'
 +sp(90,90,60,60)+'[/vc_column][/vc_row]')

# 11 CONTACT
rows.append('[vc_row bg_check="row-background-dark" dfd_enable_overlay="" anchor="form" bg_type="canvas_animated"]'
 '[vc_column][dfd_heading subtitle_google_fonts="yes" subtitle_custom_fonts="font_family:Qwigley%3Aregular" '
 'style="style_02" subtitle="Tell me the date and what the picture has to say." '
 'title_font_options="tag:h2|font_family:BebasNeueRegular" subtitle_font_options="tag:h3"]'
 'Got a press day coming?[/dfd_heading]'+sp(30,30,20,20)+
 '[gravityform id="1" title="false" description="false" ajax="false"]'+sp(40,30,20,20)+'[/vc_column][/vc_row]')

body=''.join(rows)
with io.open(OUT,'w',encoding='utf-8') as f: f.write(body)
print('YOAST TITLE: Protest & Press Day Use Case | Oddtoe')
print('YOAST DESC : How a campaign turns one press day into a photograph news desks run - four carried heads, '
      'designed by a political cartoonist, built in Melbourne and shipped.')
print("wrote", OUT, len(body), "chars,", len(rows), "rows |", len(FAQ), "FAQs")
