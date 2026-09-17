#!/usr/bin/env python3
# Compose the Oddtoe blog post "A Yurt Full of Puppets" — The Puppet Co., Glen Echo, 2004.
# Output: puppet-co-post.html (WPBakery raw body for a POST, not a page)
#
# COMMISSIONED: Otto, 14 Sep 2026, off the four 2004 nonfiction pieces he wrote while training
#   under Christopher Piper. Every fact and every quote below comes from those files:
#   'Old Computer/Graduate School/Nonfiction Techniques/' — "Puppet Theater (Final 2)",
#   "Christopher Piper is a puppet 2", "Interview", and the two earlier drafts.
#   Inventory: 'Oddtoe New Growth Pages 2026/puppetry-page-source-inventory-2026-09-14.md'.
#   Otto cleared naming The Puppet Co. and Piper on 14 Sep 2026.
#
# SHAPE: the Oddtoe blog-post shape taken from post 14493 "Oddtoe's Studios in Australia" —
#   one vc_row of 1/4 + 1/2 + 1/4, sections separated by a dotted dfd_delimiter with a Qwigley
#   label, images as vc_single_image with a caption, body as Arvo 12pt spans, closing hoverbox
#   + the 50x50 circle mark. This post pays off that post's own promise of "another blog post".
#
# IMAGERY: 16348 / 16349 are Otto's own marionette renders. 16354 is Otto's own photograph of
#   the Playhouse stage (his camera, June 2006), uploaded 14 Sep 2026. The remaining Glen Echo
#   photographs in the 2020 social folder were saved from the web and are NOT used — they belong
#   to The Puppet Co. or the park. See the handoff.
#
# NO INVENTED DETAIL. Where the drafts disagree (the stage has three trap doors in one and five
#   in another) the post gives no number. The eye patch appears in one draft only and is left out.
import io, os, re

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "puppet-co-post.html")

SP = ('[dfd_spacer screen_wide_resolution="1280" screen_wide_spacer_size="{w}" screen_normal_resolution="1024" '
      'screen_tablet_resolution="800" screen_mobile_resolution="480" screen_normal_spacer_size="{n}" '
      'screen_tablet_spacer_size="{t}" screen_mobile_spacer_size="{m}"]')
def sp(w, n=None, t=None, m=None):
    n = w if n is None else n; t = n if t is None else t; m = t if m is None else m
    return SP.format(w=w, n=n, t=t, m=m)

def delim(text):
    return ('[dfd_delimiter delimiter_style="dfd-delimiter-with-text" text_delimiter="' + text + '" '
            'delimiter_border_style="dotted" '
            'custom_fonts="font_family:Qwigley%3Aregular|font_style:400%20regular%3A400%3Anormal" '
            'module_animation="transition.expandIn" use_google_fonts="show" '
            'title_font_options="font_size:30|line_height:38"]')

def image(mid, title):
    return (f'[vc_single_image image="{mid}" img_size="full" add_caption="yes" alignment="center" '
            f'style="vc_box_shadow_3d" css="" onclick="link_one_page" item_animation="transition.fadeIn" '
            f'title="{title}"]')

LEAD = ('<p style="text-align: left;"><span style="font-size: 12pt;">'
        '<span style="font-family: Arvo, serif;">{}</span></span></p>')

def text(lead, *paras):
    """First paragraph in the wrapped lead style, the rest as plain blocks (matches post 14493)."""
    body = LEAD.format(lead)
    if paras:
        body += '\n' + '\n\n'.join(paras)
    return '[vc_column_text css=""]\n' + body + '[/vc_column_text]'

def link(url, label):
    return f'<a href="{url}"><strong>{label}</strong></a>'

PUPPET_DESIGNER = 'https://www.oddtoe.com/artist-designer/puppet-designer/'
STUDIOS_POST = 'https://www.oddtoe.com/oddtoes-studios-in-australia/'

body = ['[vc_row][vc_column width="1/4"][/vc_column][vc_column width="1/2"]' + sp(20)]

# ---------------------------------------------------------------- opening
body.append(delim('A Yurt Full of Puppets'))
body.append(image(16348, 'A marionette hangs from a control bar'))
body.append(sp(40, 40, 30, 38))
body.append(text(
  'In a post about ' + link(STUDIOS_POST, 'the places I have worked') + ', I mentioned a Mongolian '
  'yurt that was part of a puppetry centre in <strong>Glen Echo Park, Maryland</strong>, across the '
  'river from the CIA. I said there was probably another post in it. This is that post.',

  'In <strong>2004</strong> I trained under <strong>Christopher Piper</strong> at '
  '<strong>The Puppet Co.</strong> in Glen Echo, learning to build and string marionettes. I was '
  'doing a graduate course in nonfiction writing at the same time, so I spent that year taking notes '
  'on the place and interviewing the man teaching me.',

  'Those pieces have been in a folder for <strong>twenty-two years</strong>. Everything below comes '
  'out of them.'))
body.append(sp(40, 40, 30, 38))

# ---------------------------------------------------------------- founding
body.append(delim('Two Puppeteers and One Cinderella'))
body.append(sp(20, 20, 15, 19))
body.append(text(
  'Piper started the company in <strong>1983</strong> with <strong>Allan Stevens</strong>. They had '
  'met at Glen Echo three years earlier, both working with puppets and both running their own '
  'companies. Stevens had won a grant for a new production of <em>Cinderella</em> and had no '
  'Cinderella. Piper had one.',

  '&#8220;So we decided to join up,&#8221; he told me. They then moved into a group house with '
  'twenty-five other people, and twenty years later were still living under the same roof. Stevens '
  'does not drive.',

  'Stevens had run the <strong>Smithsonian Puppet Theater</strong> from 1969 to 1975. Piper is '
  'second-generation: his father <strong>Len</strong> ran a travelling puppet show out of Hawaii and '
  'Piper grew up on the road with it. &#8220;I lived in Hawaii for 17 years, but I&#8217;ve been to '
  'every state except Alaska. I broke my leg before I got there.&#8221;',

  'Their first playhouse opened in <strong>1987</strong>, in an annex of the park&#8217;s dance hall '
  'that had been condemned before they got to it.'))
body.append(sp(40, 40, 30, 38))

# ---------------------------------------------------------------- scale
body.append(delim('Five Hundred Shows a Year'))
body.append(sp(20, 20, 15, 19))
body.append(text(
  'By 2004 the company was performing close to <strong>500 shows a year</strong> and owned more than '
  '<strong>300 puppets</strong>. &#8220;That&#8217;s the problem,&#8221; Piper said. &#8220;We&#8217;ve '
  'got a storage issue.&#8221; Two units out in Gaithersburg, both full.',

  'What they perform is not entirely their decision. &#8220;Name recognition helps,&#8221; he said. '
  '&#8220;Years of Disney animation have pretty much decided what plays we&#8217;re going to '
  'produce.&#8221;',

  'There is no casting couch in puppetry, and being young is no advantage at the box office. The '
  'bankable names are made of felt, wire and wood, and they stay famous into their second and third '
  'centuries. Cinderella, Snow White, Rapunzel. Even a villain like Rumpelstiltskin keeps drawing '
  'children in.'))
body.append(sp(40, 40, 30, 38))

# ---------------------------------------------------------------- new theatre
body.append(delim('The New Theatre'))
body.append(image(16354, 'The Puppet Co. Playhouse stage, Glen Echo Park'))
body.append(sp(20, 20, 15, 19))
body.append(text(
  'That February the company moved across the park walkway into the <strong>North Arcade</strong>, an '
  'Art Deco wing with neon signage. <strong>Six thousand square feet</strong>, <strong>250 seats</strong>, '
  '<strong>two million dollars</strong>. The stage was twenty feet by twenty, with trap doors for hand '
  'puppets and a catwalk to fly things across. Some of the lights were hand-me-downs from a wealthier '
  'theatre up the road.',

  'A week out it was a half-dressed shell that smelled of sawdust and paint, with lumber stacked down '
  'the hallways. Everything in it had been chosen for children, which means rounded edges, '
  'industrial-strength, or detachable and easy to replace. My notes describe the carpet as '
  'vomit-repellent. The box office glass was the kind you see in a late-night convenience store, which '
  'tells you something about selling tickets to a children&#8217;s show. A sign in the theatre read '
  '&#8220;Benches are for adults only. Priority basis.&#8221;',

  'Six days before opening, the curtain was still in a box in the basement.',

  'The first production in the new building was <em>The Jungle Book</em>, and what Piper wanted out of '
  'the move was size. &#8220;The productions we&#8217;ve done up to this point have been built so we '
  'could take them around to schools. Smaller puppets. Now we can build larger backgrounds and set '
  'pieces.&#8221;',

  'The sound system was muffled on the first night. &#8220;The warranty expired,&#8221; he said. '
  '&#8220;But what can you do?&#8221;'))
body.append(sp(40, 40, 30, 38))

# ---------------------------------------------------------------- the yurt
body.append(delim('To the Yurt We Go'))
body.append(sp(20, 20, 15, 19))
body.append(text(
  'The yurt had been bought from the <strong>Smithsonian</strong> when a Mongolia exhibit closed, about '
  'twenty years earlier, and put up in the park by volunteers. It was the company&#8217;s workshop, and '
  'it was where the puppets went when a show finished. Most of the cast hung from hooks or lay folded '
  'into impossible positions in boxes marked <em>Nutcracker</em> and <em>Oz</em>.',

  'An hour after the last show of the weekend, it had to be emptied. Piper is not a large man and he '
  'visibly went out at the thought of an afternoon of work that was not creative. Then he straightened '
  'up and announced, &#8220;To the yurt we go!&#8221;',

  'He spent the afternoon under the new stage, standing on scaffolding in the pit while volunteers '
  'passed puppets down through the trap doors. Rapunzel, Cinderella, the Three Little Pigs. He had not '
  'seen some of them in years.',

  'His favourite came down in a clear bag with its nose pressed against the plastic, a '
  '<strong>Pinocchio</strong> that Stevens had sculpted and wired. I had asked him about it earlier. '
  '&#8220;The way the face looks, the way it moves,&#8221; he said. &#8220;He has a few favorites of '
  'mine, too. We&#8217;ve been working together for so long. It goes both ways.&#8221;',

  'Then a red wooden box came down through the floor, dusty, hand-lettered in gold along the side: '
  '<strong>Len Piper Puppet Theater, Hawaii</strong>. Piper looked at it the way you would look at '
  'something holy. He picked two puppets out of the bagged audience at his feet and started loading his '
  'father&#8217;s old trunk.',

  '&#8220;There you go.&#8221;'))
body.append(sp(40, 40, 30, 38))

# ---------------------------------------------------------------- what it was for
body.append(delim('What I Took From It'))
body.append(image(16349, 'Where the strings attach decides what the puppet can do'))
body.append(sp(20, 20, 15, 19))
body.append(text(
  'What I learned there was <strong>building and stringing marionettes</strong>, and stringing is the '
  'part nobody watches. Where each string attaches decides what the puppet is able to do. A head hung a '
  'centimetre out will never look alive, whoever is working it, and you find that out by getting it '
  'wrong and doing it again.',

  'That has been the useful part ever since. Everything I have made since is the same problem at a '
  'different size. An oversized head carried on a pole through a street, a costume with somebody inside '
  'it, a character worked live through a projector. They are all objects <strong>a person has to '
  'operate</strong>, and the ones that fail are the ones where that was worked out after the drawing was '
  'finished.',

  'Piper was in his fifties when I met him and had been doing it since he could walk. I got one year of '
  'it. It was the most useful apprenticeship I have had.'))
body.append(sp(40, 40, 30, 38))

# ---------------------------------------------------------------- CTA hoverbox + mark
body.append(
 '[vc_hoverbox image="16348" primary_title="Puppet Design" hover_title="Puppet Designer" '
 'hover_title_use_theme_fonts="yes" hover_title_css_animation="none" hover_background_color="custom" '
 'use_custom_fonts_hover_title="true" hover_custom_background="rgba(97,124,62,0.38)" '
 'hover_title_link="url:https%3A%2F%2Fwww.oddtoe.com%2Fartist-designer%2Fpuppet-designer%2F|'
 'title:Puppet%20Designer"]<span style="font-family: Arvo; font-size: 14px;">Marionettes, '
 '<strong>rod and carried puppets</strong>, oversized heads and shadow work &#8212; designed in 3D and '
 'drawn for <strong>a maker to build</strong>.</span>[/vc_hoverbox]')
body.append(sp(10, 10, 10, 5))
body.append('[vc_column_text css=""]\n'
            '<p style="text-align: right;"><span style="font-family: arvo; font-size: 10px;">'
            'What does Oddtoe do? For one thing: he&#8217;s a '
            f'<a href="{PUPPET_DESIGNER}">puppet designer</a>.</span></p>\n[/vc_column_text]')
body.append(sp(40, 40, 30, 38))
body.append('[vc_single_image image="11978" img_size="50x50" alignment="center" '
            'style="vc_box_shadow_border_circle_2" item_animation="transition.fadeIn"]')
body.append(sp(20))
body.append('[/vc_column][vc_column width="1/4"][/vc_column][/vc_row]')

out = ''.join(body)
with io.open(OUT, 'w', encoding='utf-8') as f:
    f.write(out)

YOAST = ('YOAST SEO TITLE: A Yurt Full of Puppets | The Puppet Co., Glen Echo, 2004 | Oddtoe | '
         'META DESCRIPTION: In 2004 Oddtoe trained under master puppeteer Christopher Piper at '
         'The Puppet Co. in Glen Echo Park, Maryland, building and stringing marionettes. Notes from '
         'that year.')
print(YOAST)
print("wrote", OUT, len(out), "chars")
print("images:", re.findall(r'image="(\d+)"', out))
