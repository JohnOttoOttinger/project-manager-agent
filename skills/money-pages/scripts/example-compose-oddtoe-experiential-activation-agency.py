#!/usr/bin/env python3
# Compose the Oddtoe "Experiential Activation Agency" MONEY PAGE from design-kit-oddtoe.html.
# Output: skills/money-pages/references/composed/experiential-activation-agency-<date>.html
#
# SOURCE: Otto's shortlist reply "2" to "Money page candidates - 2026-09-08 - reply with a number"
# (thread 1a07fa77d54def70), Part A #2 "Experiential Activation Agency".
#
# CANNIBALISATION GUARDRAILS (GSC, 180d to 2026-09-08, next-best-page.py --json --limit 8):
#   - "experiential activation agency" cluster (+ "global experiential marketing agency", "best
#     experiential agency", "experiential marketing agency", "best experiential marketing agency")
#     = 380 impr / 0 clicks / avg pos 23.3, currently served by /experiential-marketing-agencies/
#     (that page's own weighted position for this cluster is also 23.3, 14% page-1 share --
#     do_not_target: [], below the "already ranking well" bar).
#   - /experiential-marketing-agencies/ is a listicle ranking OTHER agencies (Freeman, Jack Morton,
#     GPJ...) -- "who are the big players", not "hire Oddtoe". Linked OUT once for readers who want
#     to survey the market instead of restated.
#   - /global-brand-experience-agency/ went LIVE since the scout's GSC snapshot was taken (confirmed
#     200 this run, title "Global Brand Experience Agency in Melbourne * Oddtoe") -- the backlog entry
#     was stale (still marked [~]). Its query "global brand experience agency" sits close to this
#     cluster's own "global experiential marketing agency", so this page does NOT use "global brand
#     experience agency" as a heading or repeated keyphrase anywhere (verified by grep below), frames
#     itself as the SINGLE-MARKET/single-build counterpart, and FAQ 5 explicitly hands multi-market
#     readers to that page instead of competing with it.
#   - /brand-activation-ideas/ is a format/idea-brainstorm page ("which format fits your brief"), not
#     an agency-capability pitch -- linked OUT rather than restated.
#   - The near-page-1 individual query "best experiential agency" (pos 11.8, on /experiential-marketing-agencies/)
#     is never used as a heading or repeated keyphrase here (grep-verified below) to avoid bidding
#     against that page's own near-top-10 ranking.
# NO PRICES: design-kit-README + brands.md -- Oddtoe pricing is TO FILL, no Oddtoe page may quote one.
# NO EXTERNAL STATS: WebFetch to two candidate sources (eventmarketer.com, screenaustralia.gov.au) was
# blocked by this session's network egress policy (EGRESS_BLOCKED) -- the page carries no third-party
# statistic rather than an unverified one, per geo-playbook rule 3.
import re, io, os, base64, urllib.parse, sys, pathlib

HERE = os.path.dirname(os.path.abspath(__file__))
KIT  = os.path.join(HERE, "..", "references", "design-kit-oddtoe.html")
OUTDIR = os.path.join(HERE, "..", "references", "composed")
OUT  = os.path.join(OUTDIR, "experiential-activation-agency-2026-09-08.html")

sys.path.insert(0, HERE)
from oddtoe_theme import retint  # noqa: E402

CTA_URL = urllib.parse.quote("https://www.oddtoe.com/contact-oddtoe/", safe="")

def link(url, label):
    return f'<strong><a class="dfd-custom-link-decorated" href="{url}">{label}</a></strong>'
def plain(t):
    """FAQ answers carry markup for the accordion; the FAQPage JSON-LD must be plain text."""
    return re.sub(r"<[^>]+>", "", t).replace("&hellip;", "…").replace("&mdash;", "—")

CANONICAL = ("Oddtoe is an experiential design and generative-AI animation studio based in Melbourne, "
             "creating projection, installation, and animated work for events, venues, and galleries.")

P = 'style="line-height: 22px; text-align: left;"'

INSTALLATION = "https://www.oddtoe.com/artist-designer/installation-artist/"
PROJECTION   = "https://www.oddtoe.com/artist-designer/projection-artist/"
PROPMAKER    = "https://www.oddtoe.com/artist-designer/prop-designer-maker/"
GENAI        = "https://www.oddtoe.com/studio/generative-ai-animator/"
ROUNDUP      = "https://www.oddtoe.com/experiential-marketing-agencies/"
IDEAS        = "https://www.oddtoe.com/brand-activation-ideas/"
GLOBAL       = "https://www.oddtoe.com/global-brand-experience-agency/"
CONTACT      = "https://www.oddtoe.com/contact-oddtoe/"

FAQ = [
 ("How much does an experiential activation agency cost?",
  "It depends on <strong>how ambitious the build</strong> is, the <strong>techniques</strong> involved and "
  "how much of the install day the agency runs. A single branded moment and a full immersive takeover sit "
  "at very different ends. Oddtoe quotes per project after a scoping conversation, so the number reflects "
  "your brief rather than a rate card."),
 ("How do I choose the right experiential activation agency?",
  "Ask to see <strong>photos from an actual install day</strong> instead of only renders, and check whether "
  "<strong>one team designs and builds</strong> the piece instead of handing it to a separate fabricator. "
  "Ask who is on site if something needs to change, and how <strong>revisions</strong> are handled before "
  "you sign anything."),
 ("What kinds of activations does an experiential activation agency handle?",
  "For Oddtoe: <strong>projection and installation pieces</strong>, generative-AI animated content, and the "
  "<strong>props and 3D objects</strong> a brand moment needs on site. Some clients want a single evening; "
  "others want a piece that tours for a season. Both get scoped the same way, <strong>the concept first</strong>."),
 ("Can an experiential activation agency include AI or generative animation in the build?",
  "Yes, where the brief calls for it. Oddtoe treats AI as <strong>one tool in the build</strong>, not the "
  "pitch itself. It speeds up iteration on content that plays inside an installation or projection piece, "
  "while a <strong>human director still owns the taste</strong>. There is a fuller explanation on the "
  + link(GENAI, "generative AI animator") + " page."),
 ("I need the same activation running in more than one market. Is this the right page?",
  "Not quite. This page covers a <strong>single build in one place</strong>. For a concept that has to "
  "travel and be rebuilt correctly by different local partners in different cities, see the "
  + link(GLOBAL, "global brand experience agency") + " page instead — it is scoped for exactly that."),
]

TOKENS = {
 "PAGE_SUBTITLE": "Looking for an&hellip;",            # runs into the H1 -- ellipsis rule, shape 1
 "PAGE_TITLE": "Experiential activation agency",
 "UPDATED_DATE": "September 2026",
 "HOOK": ("Oddtoe is an <strong>experiential activation agency</strong> based in Melbourne. One team "
          "designs the concept and builds the piece that runs it — projection, installation, or "
          "generative-AI animated content for a single event, launch or campaign. You brief "
          "<strong>one studio</strong>, not a planner and three separate vendors, and <strong>one producer</strong> "
          "owns the day it actually runs."),

 "SECTION_A_SUBTITLE": "The short version",
 "SECTION_A_HEADING": "What does an experiential activation agency actually do?",
 "SECTION_A_INTRO": ("An experiential activation agency designs a brand experience and builds the physical "
          "or technical piece that delivers it, rather than handing the idea to a separate fabricator once "
          "the concept deck is signed off. Oddtoe designs the piece, builds it in <strong>projection</strong>, "
          "<strong>installation</strong> or <strong>generative-AI animation</strong>, and stays on site for "
          "the day it runs."),
 "CANONICAL_SENTENCE": CANONICAL,

 "SECTION_B_SUBTITLE": "One brief, two different jobs",
 "SECTION_B_HEADING": "Event agency or experiential activation agency, and does the difference matter?",
 "SECTION_B_ANSWER": ("An event or marketing agency plans the campaign and briefs the physical build out to "
          "someone else. An experiential activation agency designs the piece <strong>and</strong> builds it, "
          "so the idea that gets approved in the deck is the <strong>same idea</strong> that gets fabricated, "
          "not a version handed down through a second brief."),
 "SECTION_B_CONTEXT": (
   f'<p {P}>The distinction matters most once the concept is more ambitious than a banner and a '
   'step-and-repeat. A marketing agency that designs on paper hands the real risk — can this actually be '
   'built, on this budget, by this date — to whoever wins the fabrication brief next. Oddtoe carries that '
   'risk from the <strong>first sketch</strong>, because the team drawing the concept is the team '
   '<strong>pricing and building it</strong>.</p>\n'
   f'<p {P}>It matters again on the day itself. A piece designed by one company and installed by another '
   'usually has a gap between them — a detail the fabricator improvised, a fixing the installer worked '
   'around. Oddtoe designs and builds under <strong>one roof</strong>, so the thing that arrives on site is '
   'the thing that was actually <strong>approved</strong>.</p>\n'
   f'<p {P}>It cuts both ways: for a straightforward stand, or a piece in a format the studio already has on '
   f'the shelf, a general event production company is often the simpler, cheaper hire. See {link(INSTALLATION, "installation artist")} '
   f'or {link(PROJECTION, "projection artist")} for what Oddtoe builds directly.</p>'),

 "PRIMARY_CTA_TEXT": "Scope an activation",
 "PRIMARY_CTA_URL": CTA_URL,

 "SECTION_C_SUBTITLE": "What actually gets built",
 "SECTION_C_HEADING": "What can an experiential activation agency build for you?",
 "SECTION_C_ANSWER": ("<strong>Projection and installation pieces</strong>, generative-AI animated content, "
          "and the <strong>props and 3D objects</strong> an activation needs on site. Oddtoe scopes a single "
          "pop-up moment and a full brand takeover the same way: <strong>the concept first</strong>, then "
          "the build."),
 "SECTION_C_DETAIL": (
   f'<p {P}>Each of those is a craft in its own right. {link(INSTALLATION, "Installation")} covers the built '
   f'structures and environments people walk through. {link(PROJECTION, "Projection")} takes the piece off '
   f'a screen and onto a surface that already exists. {link(PROPMAKER, "Prop and 3D making")} covers the '
   'physical objects an activation needs on the day, from a hero prop to a full set dressing.</p>\n'
   f'<p {P}>Where a brief calls for it the studio also works in generative AI, as <strong>one layer of the '
   f'build</strong> rather than the whole pitch. There is a fuller account on the {link(GENAI, "generative AI animator")} '
   'page.</p>\n'
   f'<p {P}>Still deciding what the activation even looks like? The studio keeps a running '
   f'{link(IDEAS, "guide to activation formats")} for brand teams shaping the brief, and a '
   f'{link(ROUNDUP, "roundup of the biggest experiential and brand activation agencies")} in the world '
   'for anyone wanting to see who else works at this scale.</p>'),

 "SECTION_D_SUBTITLE": "How to pick one",
 "SECTION_D_HEADING": "How do you choose an experiential activation agency?",
 "SECTION_D_ANSWER": ("<strong>Three tests.</strong> Does the reel show pieces that were actually "
          "<strong>built</strong>, not just rendered? Will <strong>one team own the concept and the "
          "fabrication</strong>? And who is on site for <strong>install and strike</strong>? Ask to see a "
          "past build's install-day photos before you sign anything."),
 "SECTION_D_RATIONALE": (
   f'<p {P}>The built-versus-rendered test catches the <strong>most common mismatch</strong>. A beautiful '
   'render tells you nothing about whether the piece survives a load-in dock, a fire-safety check, or four '
   'days in front of a public crowd.</p>\n'
   f'<p {P}>The ownership test matters because a gap between designer and fabricator is usually where a '
   '<strong>budget blows out</strong>. If the team pricing the build did not draw it, someone is guessing at '
   'both ends, and you pay for the guess.</p>\n'
   f'<p {P}>The install-day test is the one people skip because it feels like a <strong>logistics '
   'question</strong>, not a creative one. It is both. I would rather tell a client an idea will not survive '
   'the venue while there is still time to change it, than watch it fail on site.</p>'),

 "ARTICLE_1_SUBTITLE": "Why one studio beats a relay",
 "ARTICLE_1_HEADING": "One concept, one build, one team on site",
 "ARTICLE_1_BODY": (
   f'<p {P}>The case for splitting an activation across a marketing agency, a fabricator and an install crew '
   'is that each one is a specialist. On paper that is true. What the pitch decks do not show is the '
   '<strong>handoff between them</strong> — the point where a concept sketch becomes a materials list, and '
   'the materials list becomes a thing that has to physically stand up in a venue.</p>\n'
   f'<p {P}>That handoff is where I have watched budgets and timelines slip the most. A fabricator working '
   'from someone else’s drawing has to guess at intent on every detail the drawing did not specify, and '
   'every guess either goes back to the client for a decision or gets made silently and shows up wrong on '
   'install day. Running the design and the build as <strong>one job</strong> removes that guess — I am the '
   'person who drew it, and the person pricing and building it.</p>\n'
   f'<p {P}>The second thing one studio buys is <strong>accountability on the day</strong>. When the '
   'designer, the fabricator and the installer are three different companies, a problem on site becomes a '
   'conversation about whose fault it is before anyone fixes it. When it is one team, that conversation does '
   'not happen, because we already know which decision caused it — we made every decision.</p>\n'
   f'<p {P}>None of that means a single studio is the right call for everything. A straightforward stand, in '
   'a format the venue already knows, does not need a bespoke build process behind it — a good general '
   'production company handles that well. The rule I use: <strong>the more the piece is a genuine one-off</strong>, '
   'and the more it depends on getting a technical detail right, the more it is worth keeping the design and '
   'the build under one roof.</p>\n'
   f'<p {P}>The objects on site matter as much as the concept. {link(PROPMAKER, "Prop and 3D making")} and '
   f'{link(GENAI, "generative AI animation")} both sit inside that same build here, briefed once with '
   'everything else and built by the same team that designed them.</p>'),

 "TABLE_SUBTITLE": "Who's actually building it?",
 "TABLE_HEADING": "In-house team, production agency, or experiential activation agency?",
 "TABLE_INTRO": "The same activation can be resourced three ways. This is what changes between them.",

 "ARTICLE_2_SUBTITLE": "What helps first&hellip;",     # hands over to the content -- ellipsis rule, shape 2
 "ARTICLE_2_HEADING": "How to brief an experiential activation agency",
 "ARTICLE_2_BODY": (
   f'<p {P}>Tell me <strong>the outcome, not the shot list</strong>. Who the activation is for, where it '
   'runs, when it has to be live, and one or two references for the feeling you want. Rough is fine. Working '
   'the plan out from a loose brief is part of what you are paying for.</p>\n'
   f'<p {P}>Four things change a quote more than anything else: <strong>the scale of the build</strong>, the '
   '<strong>technique</strong>, how much of the <strong>install day</strong> the agency runs, and how many '
   '<strong>rounds of revision</strong> you expect before the concept is locked.</p>\n'
   f'<p {P}><strong>Say what you already have.</strong> A venue, a load-in time, brand guidelines, even a '
   'past activation that did not survive its own venue all <strong>shorten the scoping conversation</strong>. '
   'So does saying what went wrong last time.</p>\n'
   f'<p {P}>If you are still deciding what the activation even <strong>looks like</strong>, say that too — '
   f'the {link(IDEAS, "guide to activation formats")} is a reasonable place to start before the brief is '
   f'locked. Send it through the {link(CONTACT, "contact page")} and a real person reads it.</p>'),

 "FAQ_TOPIC": "experiential activation agencies",
 "FAQ_CTA_TEXT": "Scope an activation",
 "FAQ_CTA_URL": CTA_URL,
}
for i,(q,a) in enumerate(FAQ, start=1):
    TOKENS[f"FAQ_Q{i}"]=q; TOKENS[f"FAQ_A{i}"]=a

# ───────────────────────────── build ─────────────────────────────
kit = io.open(KIT, encoding="utf-8").read()

# 1. FAQ JSON-LD: decode the pre-encoded payload, fill, re-encode (urlencode THEN base64)
def fill(txt):
    for k,v in TOKENS.items():
        txt = re.sub(r'\{\{'+k+r'(?::[^}]*)?\}\}', lambda m: v, txt)
    return txt
def redo_raw_html(m):
    dec = urllib.parse.unquote(base64.b64decode(m.group(1)).decode())
    for k, v in TOKENS.items():                      # schema gets PLAIN text, never markup
        dec = re.sub(r'\{\{'+k+r'(?::[^}]*)?\}\}', lambda mm, v=v: plain(v), dec)
    return "[vc_raw_html]" + base64.b64encode(urllib.parse.quote(dec, safe="").encode()).decode() + "[/vc_raw_html]"
kit = re.sub(r'\[vc_raw_html\]([A-Za-z0-9+/=]+)\[/vc_raw_html\]', redo_raw_html, kit)

# 2. table row: drop the PRICING exemplar (no Oddtoe prices permitted), keep + refill the COMPARISON one
TH  = ("padding: 14px 18px; text-align: left; background-color: %s !important; border: none !important; "
       "border-bottom: 2px solid #ddccb1 !important; font-family: 'Bebas Neue', sans-serif; font-size: 21px; "
       "font-weight: normal; letter-spacing: 1px; color: %s !important; white-space: nowrap;")
TD  = ("padding: 12px 18px; text-align: left; background-color: %s !important; border: none !important; "
       "border-bottom: 1px solid #26161f !important; color: #ffffff !important;%s")
ROWS = [
 ("Who designs the concept",       "Your own team",                    "You supply it, they execute",     "One agency designs it"),
 ("Who builds the piece",          "An outsourced fabricator you find","Their production network",         "The same team that designed it"),
 ("Who holds the schedule",        "You do",                           "Their production manager",         "The agency, concept to strike"),
 ("Who is on site for install",    "Whoever you send",                 "An install crew, hired separately","The team that built it"),
 ("Revisions",                     "Negotiated with each vendor",      "Scoped per trade",                 "Scoped in the quote"),
 ("If something changes on site",  "You coordinate between vendors",   "Raised up their chain",            "Decided on the spot"),
 ("Best suited to",                "A format you already run every year","A straightforward stand",        "A one-off that has to survive a real venue"),
]
head = ("<tr>"
  + f'<th scope="col" style="{TH % ("#000000","#ffffff")}">Criterion</th>'
  + f'<th scope="col" style="{TH % ("#000000","#ffffff")}">In-house team</th>'
  + f'<th scope="col" style="{TH % ("#000000","#ffffff")}">Event production agency</th>'
  + f'<th scope="col" style="{TH % ("#ddccb1","#000000")}">Experiential activation agency</th></tr>')
body = ""
for c,a,b,cc in ROWS:
    body += ("<tr>"
      + f'<td style="{TD % ("#000000"," font-weight: bold;")}">{c}</td>'
      + f'<td style="{TD % ("#000000","")}">{a}</td>'
      + f'<td style="{TD % ("#000000","")}">{b}</td>'
      + f'<td style="{TD % ("#111111","")}">{cc}</td></tr>')
newtable = ('<table style="width: 100%; border-collapse: collapse !important; background-color: #000000 '
            '!important; border: none !important;">\n<thead>\n'+head+'\n</thead>\n<tbody>\n'+body+'\n</tbody>\n</table>')

tables = list(re.finditer(r'<div style="overflow-x: auto;">\s*<table.*?</table>\s*</div>', kit, re.S))
assert len(tables)==2, f"expected 2 table blocks, found {len(tables)}"
start, end = tables[0].start(), tables[1].start()
kit = kit[:start] + kit[end:]
kit = re.sub(r'<div style="overflow-x: auto;">\s*<table.*?</table>\s*</div>',
             '<div style="overflow-x: auto;">\n'+newtable+'\n</div>', kit, count=1, flags=re.S)
kit = kit.replace("Footnote, e.g. All prices include GST. Travel outside Melbourne quoted separately.",
                  "Oddtoe quotes per project after a scoping conversation. Travel and venue fees are quoted separately.")

# 3. swap the offers row info_banner cards to something relevant (real, live-verified media/pages)
kit = kit.replace(
  'info_banner image="15398" img_height="225" read_more="box" image_effect="dfd-image-scale" style="style-04" '
  'title="Non-Fiction Animator" subtitle="Documentaries &amp; Exhibits" title_font_options="tag:div|font_size:18|'
  'font_family:BebasNeueRegular|line_height:22" subtitle_font_options="tag:div|font_size:10|color:%23ddccb1|'
  'line_height:12" font_options="tag:div|font_size:12|line_height:14" link="url:https%3A%2F%2Fwww.oddtoe.com%2Fstudio%2Fdocumentary-animator%2F|title:Documentary%20Animator"',
  'info_banner image="12848" img_height="225" read_more="box" image_effect="dfd-image-scale" style="style-04" '
  'title="Projection Artist" subtitle="Light &amp; Surface" title_font_options="tag:div|font_size:18|'
  'font_family:BebasNeueRegular|line_height:22" subtitle_font_options="tag:div|font_size:10|color:%23ddccb1|'
  'line_height:12" font_options="tag:div|font_size:12|line_height:14" link="url:https%3A%2F%2Fwww.oddtoe.com%2Fartist-designer%2Fprojection-artist%2F|title:Projection%20Artist"'
)
kit = kit.replace(
  'info_banner image="14219" img_height="225" read_more="box" image_effect="dfd-image-scale" style="style-04" '
  'title="Animation Agents" subtitle="Networking" title_font_options="tag:div|font_size:18|font_family:BebasNeueRegular|'
  'line_height:22" subtitle_font_options="tag:div|font_size:10|color:%23ddccb1|line_height:12" '
  'font_options="tag:div|font_size:12|line_height:14" link="url:https%3A%2F%2Fwww.oddtoe.com%2Fanimation-agents%2F|title:Animation%20Agents"',
  'info_banner image="16055" img_height="225" read_more="box" image_effect="dfd-image-scale" style="style-04" '
  'title="Installation Artist" subtitle="Builds &amp; Environments" title_font_options="tag:div|font_size:18|'
  'font_family:BebasNeueRegular|line_height:22" subtitle_font_options="tag:div|font_size:10|color:%23ddccb1|'
  'line_height:12" font_options="tag:div|font_size:12|line_height:14" link="url:https%3A%2F%2Fwww.oddtoe.com%2Fartist-designer%2Finstallation-artist%2F|title:Installation%20Artist"'
)
# card captions (the shortcode's inner text): card 1 "Melbourne, Australia" already fits Projection Artist
# unchanged; card 2's leftover "USA, Europe, Asia" (from Animation Agents) does not fit Installation
# Artist, so retarget it to what the card is actually showing.
assert 'title:Installation%20Artist"]USA, Europe, Asia[/info_banner]' in kit, "card 2 caption swap target not found"
kit = kit.replace('title:Installation%20Artist"]USA, Europe, Asia[/info_banner]',
                   'title:Installation%20Artist"]Design to Install[/info_banner]')

# 4. enquiry-form heading + subtitle -- tailored to THIS page's job, never left as kit stock copy (lesson 12)
kit = kit.replace(
  '[dfd_heading delimiter_settings="border-bottom-style:solid;|border-bottom-width:1px;|width:50px;|border-bottom-color:#dddddd;" '
  'style="style_02" subtitle="Tell us what you are imagining&hellip;" title_font_options="tag:h2" '
  'subtitle_font_options="tag:h3"]Want to talk about a project?[/dfd_heading]',
  '[dfd_heading delimiter_settings="border-bottom-style:solid;|border-bottom-width:1px;|width:50px;|border-bottom-color:#dddddd;" '
  'style="style_02" subtitle="Tell us what you want people to experience&hellip;" title_font_options="tag:h2" '
  'subtitle_font_options="tag:h3"]Planning a brand activation that has to actually get built?[/dfd_heading]'
)

# 5. fill every remaining token
kit = fill(kit)

# 6. strip HTML comments (WPBakery mangles stray text between rows)
kit = re.sub(r'<!--.*?-->', '', kit, flags=re.S)

# 7. WIDEN THE TABLE ROW to 1/6 + 2/3 + 1/6 -- this table has FOUR columns (lesson 1 / design-kit-README).
rows=[m.start() for m in re.finditer(r'\[vc_row(?![_a-z])', kit)]+[len(kit)]
ti=next(i for i in range(len(rows)-1) if '<table' in kit[rows[i]:rows[i+1]])
seg=kit[rows[ti]:rows[ti+1]]
assert seg.count('[vc_column_inner width="1/3"]')==3, seg.count('[vc_column_inner width="1/3"]')
seg=seg.replace('[vc_column_inner width="1/3"]','[vc_column_inner width="1/6"]',1)
seg=seg.replace('[vc_column_inner width="1/3"]','[vc_column_inner width="2/3"]',1)
seg=seg.replace('[vc_column_inner width="1/3"]','[vc_column_inner width="1/6"]',1)
kit=kit[:rows[ti]]+seg+kit[rows[ti+1]:]

# 8. WIDEN HERO + SECTION-1 + SECTION-2 inner rows to 1/4 + 1/2 + 1/4 (lessons 7 & 8: head noun
#    "experiential activation agency" is 3 words, and several headings on this page run 7-9 words
#    long -- e.g. "What does an experiential activation agency actually do?" -- which wraps badly in
#    a 1/3 column. Hero row_inner carries offset= attrs that override width at desktop sizes (lesson
#    7), so those must change too; pat-section-1/2 have no offset attr, width alone suffices there.
def widen_hero(seg):
    assert seg.count('offset="vc_col-lg-4 vc_col-md-2 vc_col-xs-1"') == 2, "expected 2 gutter columns in hero row_inner"
    assert 'offset="vc_col-lg-4 vc_col-md-8 vc_col-xs-10"' in seg
    seg = seg.replace('el_class="dfd_col-tablet-12" width="1/3" offset="vc_col-lg-4 vc_col-md-2 vc_col-xs-1"',
                       'el_class="dfd_col-tablet-12" width="1/4" offset="vc_col-lg-3 vc_col-md-2 vc_col-xs-1"')
    seg = seg.replace('width="1/3" dfd_column_responsive_enable="dfd-column-responsive-enable" offset="vc_col-lg-4 vc_col-md-8 vc_col-xs-10"',
                       'width="1/2" dfd_column_responsive_enable="dfd-column-responsive-enable" offset="vc_col-lg-6 vc_col-md-8 vc_col-xs-10"')
    return seg

rows=[m.start() for m in re.finditer(r'\[vc_row(?![_a-z])', kit)]+[len(kit)]
hi=next(i for i in range(len(rows)-1) if 'el_id="pat-intro"' in kit[rows[i]:rows[i+1]])
kit = kit[:rows[hi]] + widen_hero(kit[rows[hi]:rows[hi+1]]) + kit[rows[hi+1]:]

def widen_plain_third(seg, pat_id):
    n = seg.count('[vc_column_inner width="1/3"]')
    assert n==3, f"{pat_id}: expected 3 plain 1/3 columns, found {n}"
    seg = seg.replace('[vc_column_inner width="1/3"]','[vc_column_inner width="1/4"]',1)
    seg = seg.replace('[vc_column_inner width="1/3"]','[vc_column_inner width="1/2"]',1)
    seg = seg.replace('[vc_column_inner width="1/3"]','[vc_column_inner width="1/4"]',1)
    return seg

for pat in ("pat-section-1", "pat-section-2"):
    rows=[m.start() for m in re.finditer(r'\[vc_row(?![_a-z])', kit)]+[len(kit)]
    si=next(i for i in range(len(rows)-1) if f'el_id="{pat}"' in kit[rows[i]:rows[i+1]])
    kit = kit[:rows[si]] + widen_plain_third(kit[rows[si]:rows[si+1]], pat) + kit[rows[si+1]:]

# 9. PER-PAGE NEAR-BLACK (README lesson 13) -- unused tint. Slate (#1a1e26) is already spoken for by
#    Global Brand Experience Agency, the closest neighbouring page in this same experiential/activation
#    cluster, so it is excluded per design-language.md's "never give the same tint to two pages in one
#    cluster" rule even though it is otherwise free. Using ink (#171d2a), still unused in the ledger.
#    crum_page_custom_bg_color is Ronneby post meta and still cannot be set over REST -- set it to the
#    same hex (#171d2a) in wp-admin Page Options.
kit, tint_notes = retint(kit, 'ink')

# 10. Guardrail assertions -- fail the build rather than ship a cannibalising page.
BANNED_PHRASES = ["global brand experience agency", "best experiential agency",
                   "best experiential marketing agencies", "top experiential agencies"]
plain_kit = re.sub(r"<[^>]+>", " ", kit).lower()
for phrase in BANNED_PHRASES:
    if phrase == "global brand experience agency":
        # allowed exactly once, inside the FAQ 5 handoff link text
        assert plain_kit.count(phrase) <= 1, f"'{phrase}' appears {plain_kit.count(phrase)}x -- should be 0 or 1 (FAQ handoff only)"
    else:
        assert phrase not in plain_kit, f"banned near-duplicate phrase found: '{phrase}'"

# ─────────────────────────── write + report ───────────────────────────
os.makedirs(OUTDIR, exist_ok=True)
io.open(OUT,"w",encoding="utf-8").write(kit)
left = re.findall(r'\{\{([A-Z0-9_]+)', kit)
print("TINT NOTES:", tint_notes)
print("YOAST SEO TITLE: Experiential Activation Agency | Oddtoe, Melbourne")
print("META DESCRIPTION: Oddtoe is an experiential activation agency in Melbourne -- one studio designs the concept and builds it, from projection to installation to AI animation.")
print("wrote", OUT, len(kit), "chars | unfilled tokens:", left or "none")
