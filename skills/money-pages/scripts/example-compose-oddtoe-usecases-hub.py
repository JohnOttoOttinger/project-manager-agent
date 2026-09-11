#!/usr/bin/env python3
# Compose the Oddtoe "Use Cases" hub page (16296) — parent of every /use-cases/ page.
# Shape: Portfolio-page opener (no hero photo; kicker + h1, two text columns, a bullet, an icon divider),
# then Ronneby info_banner cards in a row of three (the same asset as the Experiential Activation
# Agency page's related-pages row), then the contact form. Add one info_banner per new use case.
import io, os, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "usecases-hub.html")

SP=('[dfd_spacer screen_wide_resolution="1280" screen_wide_spacer_size="{w}" screen_normal_resolution="1024" '
    'screen_tablet_resolution="800" screen_mobile_resolution="480" screen_normal_spacer_size="{n}" '
    'screen_tablet_spacer_size="{t}" screen_mobile_spacer_size="{m}"]')
def sp(w,n=None,t=None,m=None):
    n=w if n is None else n; t=n if t is None else t; m=t if m is None else m
    return SP.format(w=w,n=n,t=t,m=m)
A=lambda s: f'<span style="font-family: Arvo;">{s}</span>'
CANON=('<strong>Oddtoe</strong> is an experiential design and generative-AI animation studio based in Melbourne, '
       'creating projection, installation, and animated work for events, venues, and galleries.')

def card(image, title, subtitle, body, url=None):
    link = (f' link="url:{urllib.parse.quote(url, safe="")}|title:{urllib.parse.quote(title, safe="")}"') if url else ''
    return (f'[info_banner image="{image}" img_height="225" read_more="box" image_effect="dfd-image-scale" style="style-04" '
            f'title="{title}" subtitle="{subtitle}" '
            'title_font_options="tag:div|font_size:18|font_family:BebasNeueRegular|line_height:22" '
            'subtitle_font_options="tag:div|font_size:10|color:%23ddccb1|line_height:12" '
            f'font_options="tag:div|font_size:12|line_height:14"{link}]{body}[/info_banner]')

# One-line divider: dotted rule with the sitemap icon and the Qwigley line in the middle.
# Ronneby's dfd_delimiter only does line OR icon OR text, so this is hand-rolled (9 Sep 2026).
DIVIDER=('<style>.ucd{display:flex;align-items:center;gap:18px;max-width:1180px;margin:0 auto;padding:0 10px}'
 '.ucd-l{flex:1 1 auto;border-top:1px dotted rgba(221,204,177,.55);height:0}'
 '.ucd-i{color:#ddccb1;font-size:20px;line-height:1;flex:0 0 auto}'
 '.ucd-t{font-family:Qwigley,cursive!important;font-size:30px;line-height:38px;color:#fff;white-space:nowrap;flex:0 0 auto}'
 '@media(max-width:600px){.ucd{gap:12px}.ucd-t{font-size:24px;white-space:normal;text-align:center}}</style>'
 '<div class="ucd"><span class="ucd-l"></span><i class="ucd-i fas fa-sitemap" aria-hidden="true"></i>'
 '<span class="ucd-t">Pick the brief that looks like yours&hellip;</span><span class="ucd-l"></span></div>')
import base64
DIV64=base64.b64encode(urllib.parse.quote(DIVIDER, safe="!*'()").encode()).decode()

rows=[]
# (hero row removed 9 Sep 2026 on Otto's instruction: the page opens on the text row so the use cases show sooner)

# 2 OPENER — Portfolio-page shape: kicker + heading, two columns, one bullet, icon divider
a=A(CANON+' Each use case takes one kind of brief and follows it from the first drawing to the day itself, so you know what gets made, in what order, and what you keep afterwards.')
b=A('Most people arrive with a date and a rough idea, and no way to picture what I would do with it. These pages fix that. Pick the one closest to your brief, read it in five minutes, and you will know whether to send me the date. If your brief is not here yet, send it anyway. The steps rarely change. Only the object does.')
rows.append('[vc_row bg_check="row-background-dark" dfd_enable_overlay="" anchor="top"][vc_column]'+sp(200,180,150,130)+
 '[dfd_heading enable_delimiter="" style="style_02" subtitle="Use cases, one brief at a time" '
 'title_font_options="tag:h1|font_family:BebasNeueRegular|letter_spacing:0" '
 'subtitle_font_options="tag:h3|font_family:QwigleyRegular" heading_margin="margin-bottom:10px;"]'
 'See the Whole Job Before You Ask for a Quote[/dfd_heading]'+sp(20,20,15,10)+
 '[vc_row_inner][vc_column_inner width="1/4"][/vc_column_inner]'
 f'[vc_column_inner width="1/4"][vc_column_text css=""]{a}[/vc_column_text][/vc_column_inner]'
 f'[vc_column_inner width="1/4"][vc_column_text css=""]{b}[/vc_column_text][/vc_column_inner]'
 '[vc_column_inner width="1/4"][/vc_column_inner][/vc_row_inner]'+sp(40,40,30,20)+
 '[vc_row_inner][vc_column_inner width="1/6"][/vc_column_inner][vc_column_inner width="2/3"][vc_column_text css=""]\n'
 '<p style="text-align: center;"><span style="font-family: Arvo;">&#8226;  Next use case:&raquo;  </span>'
 '<strong style="font-family: Arvo;">Museum Late Opening.</strong></p>\n[/vc_column_text]'+sp(60,60,40,40)+
 '[/vc_column_inner][vc_column_inner width="1/6"][/vc_column_inner][/vc_row_inner]'
 '[/vc_column][/vc_row]')

# 3 CARDS — Ronneby info_banner, row of three (add a card per new use case)
cards=[
 card(16244,'Publicity Stunts &amp; Cheeky PR Campaigns','Campaigns, PR &amp; grassroots','One idea, one press day, one photograph',
      'https://www.oddtoe.com/use-cases/publicity-stunts/'),
 card(16248,'Museum Late Opening','Galleries &amp; museums','In the works. Back soon.'),
 card(16254,'A Brief That Is Not Here Yet','Any venue, any date','Send it anyway. Rough is fine.',
      'https://www.oddtoe.com/contact-oddtoe/'),
]
rows.append('[vc_row bg_check="row-background-dark" anchor="use-cases"][vc_column]'+sp(30,30,20,20)+
 f'[vc_raw_html]{DIV64}[/vc_raw_html]'+sp(20)+
 '[/vc_column]'+''.join(f'[vc_column width="1/3"]{c}{sp(50)}[/vc_column]' for c in cards)+
 '[vc_column][dfd_delimiter delimiter_style="dfd-delimiter-with-line" delimiter_border_style="dotted" '
 'custom_fonts="font_family:Qwigley%3Aregular|font_style:400%20regular%3A400%3Anormal" module_animation="transition.expandIn"]'
 +sp(40)+'[/vc_column][/vc_row]')

# 4 CONTACT
rows.append('[vc_row bg_check="row-background-dark" dfd_enable_overlay="" anchor="form" bg_type="canvas_animated"]'
 '[vc_column][dfd_heading subtitle_google_fonts="yes" subtitle_custom_fonts="font_family:Qwigley%3Aregular" '
 'style="style_02" subtitle="Tell me the date and what has to happen on it." '
 'title_font_options="tag:h2|font_family:BebasNeueRegular" subtitle_font_options="tag:h3"]'
 'Got a brief?[/dfd_heading]'+sp(30,30,20,20)+
 '[gravityform id="1" title="false" description="false" ajax="false"]'+sp(40,30,20,20)+'[/vc_column][/vc_row]')

body=''.join(rows)
with io.open(OUT,'w',encoding='utf-8') as f: f.write(body)
print('YOAST TITLE: Use Cases | Oddtoe')
print('YOAST DESC : Worked examples of what you get from Oddtoe, brief by brief: publicity stunts, museum late openings, and more, with real drawings and timelines.')
print('wrote',OUT,len(body),'chars,',len(rows),'rows')
