#!/usr/bin/env python3
# Compose the Oddtoe "Global Brand Experience Agency" MONEY PAGE from design-kit-oddtoe.html.
# Output: skills/money-pages/references/composed/global-brand-experience-agency-<date>.html
#
# SOURCE: Otto's shortlist reply "1" to "Money page candidates - 2026-08-31" (thread
# 1a05670d55988d70), Part A #1 "Global brand experience agency".
#
# CANNIBALISATION GUARDRAILS (GSC, 180d to 2026-08-31, next-best-page.py --json --limit 40):
#   - "global brand experience agency" + "global brand activation agency" cluster = 120 impr /
#     0 clicks / avg pos 18.1, currently served by /experiential-marketing-agencies/ (that page's
#     own weighted position for this cluster is also 18.1, 0% page-1 share -- do_not_target: []).
#   - /experiential-marketing-agencies/ is a listicle ranking OTHER agencies (Freeman, Jack Morton,
#     GPJ, Momentum...) -- it answers "who are the big players", not "hire Oddtoe". This page is the
#     opposite framing (hire Oddtoe to run a multi-market brand experience), so intents do not overlap;
#     link OUT to the roundup for readers who want to survey the market instead.
#   - /brand-activation-ideas/ is a format/idea-brainstorm page ("which format fits your brief"), not
#     an agency-capability pitch -- also linked OUT rather than restated.
#   - No do_not_target queries were flagged by next-best-page.py for this cluster.
# NO PRICES: design-kit-README + brands.md -- Oddtoe pricing is TO FILL, no Oddtoe page may quote one.
# NO EXTERNAL STATS: two candidate real sources (Event Marketer EventTrack 2026, Forrester's B2B
# event-budget report) were both blocked by this session's network egress policy on WebFetch, so
# neither could be verified this run -- the page carries no third-party statistic rather than an
# unverified one, per geo-playbook rule 3. Otto can add one later once re-verified.
import re, io, os, base64, urllib.parse, sys, pathlib

HERE = os.path.dirname(os.path.abspath(__file__))
KIT  = os.path.join(HERE, "..", "references", "design-kit-oddtoe.html")
OUTDIR = os.path.join(HERE, "..", "references", "composed")
OUT  = os.path.join(OUTDIR, "global-brand-experience-agency-2026-08-31.html")

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
CONTACT      = "https://www.oddtoe.com/contact-oddtoe/"

FAQ = [
 ("How much does a global brand experience agency cost?",
  "It depends on <strong>how many markets</strong> the rollout covers, <strong>how much original design</strong> "
  "the concept needs, and how much of the local build the agency runs versus hands off. A single-city "
  "activation and a five-market rollout of the same idea sit at very different ends. Oddtoe quotes per "
  "project after a scoping conversation, so the number reflects your brief rather than a rate card."),
 ("How do I choose the right agency for a multi-market brand experience?",
  "Check whether they <strong>design the concept once and adapt it</strong>, or redesign it per market, "
  "whether <strong>one team owns the whole rollout</strong>, and how they find and manage local production "
  "partners. Ask to see the <strong>build spec</strong> behind a past multi-market job — the working "
  "document a local partner actually received."),
 ("What kinds of activations can a global brand experience agency run?",
  "For Oddtoe: <strong>projection and installation pieces</strong>, generative-AI animated content, and the "
  "<strong>production documentation</strong> that lets a local partner build the same piece correctly in a "
  "different city. Some clients need one build in one city; others need the same concept live in five."),
 ("Can a global brand experience agency handle AI-generated or animated content as part of the rollout?",
  "Yes, where the brief calls for it. Oddtoe treats AI as <strong>one tool inside the production pipeline</strong>, "
  "with a <strong>human director owning the taste</strong> across every market it runs in. There is a fuller "
  "explanation on the " + link(GENAI, "generative AI animator") + " page."),
 ("I only need one market covered. Is this the right page?",
  "Probably not. This page is for a <strong>concept that has to travel</strong>, run correctly by different "
  "local hands in different cities. For a single build in one place, a working " +
  link(INSTALLATION, "installation artist") + " or " + link(PROJECTION, "projection artist") +
  " is usually the simpler, cheaper hire. Start there instead."),
]

TOKENS = {
 "PAGE_SUBTITLE": "So you need a&hellip;",             # runs into the H1 -- ellipsis rule, shape 1
 "PAGE_TITLE": "Global brand experience agency",
 "UPDATED_DATE": "August 2026",
 "HOOK": ("Oddtoe is a Melbourne-based <strong>global brand experience agency</strong>, running "
          "<strong>projection, installation and animated activations</strong> for brands that need the "
          "same idea to work in more than one market. One creative direction, one production spec, and "
          "<strong>local build partners</strong> wherever it lands, so the experience reads as one brand, "
          "not a translated copy."),

 "SECTION_A_SUBTITLE": "The short version",
 "SECTION_A_HEADING": "What does a global brand experience agency actually do?",
 "SECTION_A_INTRO": ("A global brand experience agency designs <strong>one concept</strong> and the system "
          "for repeating it well, rather than briefing a new idea into every city on the schedule. Oddtoe "
          "designs the piece, writes the <strong>build spec</strong> it travels on, and works with vetted "
          "local partners so each market's build matches that spec <strong>precisely</strong>."),
 "CANONICAL_SENTENCE": CANONICAL,

 "SECTION_B_SUBTITLE": "One idea, many stamps",
 "SECTION_B_HEADING": "Local vendor or global brand experience agency, and does the difference matter?",
 "SECTION_B_ANSWER": ("A local vendor builds what you already designed, in one city. A global brand "
          "experience agency designs the concept <strong>and</strong> the spec for repeating it well, so "
          "the version in Singapore and the version in Sydney both read as the <strong>same brand</strong>, "
          "run by people who know the market they are actually building in."),
 "SECTION_B_CONTEXT": (
   f'<p {P}>The distinction matters most <strong>once a second market joins the schedule</strong>. Briefing '
   'each city separately means the idea gets reinterpreted every time, and a small drift in one build reads as '
   'a <strong>different brand</strong> by the third city. An agency that owns the concept keeps that drift out '
   'by design, not by luck.</p>\n'
   f'<p {P}>It matters again on <strong>who finds the local hands</strong>. Sourcing and vetting a production '
   'partner in a city you do not work in is its own project, done on top of the actual creative work. Oddtoe '
   'runs that search, hands the local partner a <strong>build-ready spec</strong> instead of a moodboard, and '
   'stays the single point of contact while it happens.</p>\n'
   f'<p {P}>It cuts both ways: for one activation in one city you already know, a local specialist is often the '
   f'simpler buy. See {link(INSTALLATION, "installation artist")} or {link(PROJECTION, "projection artist")} '
   'for what the studio builds directly.</p>'),

 "PRIMARY_CTA_TEXT": "Scope a rollout",
 "PRIMARY_CTA_URL": CTA_URL,

 "SECTION_C_SUBTITLE": "What actually travels",
 "SECTION_C_HEADING": "What can a global brand experience agency deliver across markets?",
 "SECTION_C_ANSWER": ("<strong>Projection and installation pieces</strong>, generative-AI animated content, "
          "and the <strong>production documentation</strong> that lets a local partner build the same piece "
          "correctly in a different city. Oddtoe designs the concept once and hands local partners a "
          "<strong>build-ready spec</strong> they can follow directly."),
 "SECTION_C_DETAIL": (
   f'<p {P}>Each of those is a craft in its own right. {link(INSTALLATION, "Installation")} covers the built '
   f'environments and structures. {link(PROJECTION, "Projection")} takes the piece off the wall and onto a '
   f'surface that already exists. {link(PROPMAKER, "Prop and 3D making")} covers the physical and digital '
   'objects a rollout needs, wherever it is fabricated.</p>\n'
   f'<p {P}>Where a brief calls for it the studio also works in generative AI, as <strong>one technique among '
   f'several</strong> rather than the whole pitch. There is a fuller account on the '
   f'{link(GENAI, "generative AI animator")} page.</p>\n'
   f'<p {P}>Deciding what the concept even is comes first. The studio keeps a running '
   f'{link(IDEAS, "guide to activation formats")} for brand teams still shaping the brief, and a '
   f'{link(ROUNDUP, "roundup of the biggest experiential and brand activation agencies")} in the world for '
   'anyone wanting to see who else works at this scale.</p>'),

 "SECTION_D_SUBTITLE": "How to pick one",
 "SECTION_D_HEADING": "How do you choose a global brand experience agency?",
 "SECTION_D_ANSWER": ("<strong>Three tests.</strong> Do they design the concept once and adapt it, instead "
          "of reinventing it per market? Will <strong>one team own the whole rollout</strong>, start to "
          "finish? And how do they find and manage the <strong>local partners</strong> who actually build "
          "it? Ask for a build spec from a past job, and who on the ground actually built it."),
 "SECTION_D_RATIONALE": (
   f'<p {P}>The concept test catches the <strong>most common failure mode</strong>. An agency that treats every market as a '
   'fresh brief will show you five different-looking activations and call it <strong>localisation</strong>. '
   'It is really just drift.</p>\n'
   f'<p {P}>The ownership test matters because a multi-market rollout <strong>runs long</strong> and touches '
   'more people than a single build. If the person who understood the original brief is not the person '
   'managing the third city, you will <strong>explain it all again</strong>, in a language the local build '
   'crew does not share.</p>\n'
   f'<p {P}>The local-partner test is the one clients skip because it feels like a <strong>logistics '
   'question</strong>, not a <strong>creative one</strong>. It is both. I would rather show you exactly '
   '<strong>who builds it on the ground</strong> and how the <strong>spec gets handed over</strong>, before '
   'you sign anything.</p>'),

 "ARTICLE_1_SUBTITLE": "Why one idea, more than one build",
 "ARTICLE_1_HEADING": "One concept, run correctly in more than one market",
 "ARTICLE_1_BODY": (
   f'<p {P}>The pitch for briefing each market separately is that it is <strong>simpler</strong>, and for a '
   'single activation it often is. The cost that does not show up in any one quote is <strong>consistency</strong>. '
   'Somebody has to hold the original idea in their head while three different local vendors interpret it '
   'three different ways, and decide which version is actually right when they disagree. On a direct-hire '
   'rollout that somebody is you.</p>\n'
   f'<p {P}>That is the part a global brand experience agency <strong>absorbs</strong>. I take a brief, design '
   'the concept once, and write the build spec that a local partner in any city can follow without guessing '
   'what I meant. You get <strong>one creative direction and one point of contact</strong>, and the version '
   'that lands in each market stays a build of the same idea, <strong>executed to the same spec</strong>.</p>\n'
   f'<p {P}>The second thing an agency buys is <strong>the local search</strong>. Finding a fabricator or '
   'installer you trust, in a city you have never worked in, on a deadline, is its own project. I run that '
   'search, brief the partner against the spec, and stay on the job while they build, so you are not left '
   '<strong>managing a stranger</strong> on the other side of the world by yourself.</p>\n'
   f'<p {P}>None of that makes an agency the right answer <strong>every time</strong>. A single activation in '
   'a city the client already knows does not need a travelling concept or a spec written for handoff. The '
   'rule I use is simple: <strong>the more markets a brief touches</strong>, and the more it needs to look '
   'like <strong>one brand</strong> doing it, the more that coordination is worth paying for.</p>\n'
   f'<p {P}>Most of the work I get asked about starts as a single-market conversation that grows once the '
   'client sees it working. That is a reasonable way to test an idea before committing a whole rollout to '
   f'it, and it is why the {link(INSTALLATION, "installation")} and {link(PROJECTION, "projection")} pages '
   'exist as starting points in their own right.</p>'),

 "TABLE_SUBTITLE": "One market or five?",
 "TABLE_HEADING": "Local specialist, in-market vendor, or global brand experience agency?",
 "TABLE_INTRO": "The same brand experience can be built three ways. This is what changes once the rollout spans more than one market.",

 "ARTICLE_2_SUBTITLE": "What to send&hellip;",         # hands over to the content -- ellipsis rule, shape 2
 "ARTICLE_2_HEADING": "How to brief a global brand experience agency",
 "ARTICLE_2_BODY": (
   f'<p {P}>Tell me <strong>the outcome you want</strong>, and let the shot list come later. Who it is for, '
   'which <strong>cities or markets</strong> it needs to run in, when each one has to be live, and one or two '
   'references for the feeling you want. Rough is fine. Working the plan out from a loose brief is part of '
   'what you are paying for.</p>\n'
   f'<p {P}>Four things change a quote more than anything else: <strong>how many markets</strong> it runs in, '
   'the <strong>technique</strong>, how much <strong>original design</strong> the concept needs, and how much '
   'of the local build the agency runs versus hands to your own team on the ground.</p>\n'
   f'<p {P}><strong>Say what you already have.</strong> Brand guidelines, a global campaign brief, existing '
   'local vendor relationships, even a rollout that went wrong last time all <strong>shorten the scoping '
   'conversation</strong>. So does saying which market has to launch first.</p>\n'
   f'<p {P}>If you are still deciding what the activation even <strong>looks like</strong>, say that too. The '
   f'studio keeps a {link(IDEAS, "guide to activation formats")} worth a look before the brief is locked. '
   f'Send it through the {link(CONTACT, "contact page")} and a real person reads it.</p>'),

 "FAQ_TOPIC": "global brand experience agencies",
 "FAQ_CTA_TEXT": "Scope a rollout",
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
 ("Who designs the concept",   "You brief each vendor separately", "A local vendor interprets your brief", "One agency designs it once"),
 ("Consistency across markets","Depends what you write each time", "Varies by vendor",                     "Built into the spec"),
 ("Who finds local partners",  "You do",                           "Already local",                        "The agency sources and manages them"),
 ("Build documentation",       "Rarely formalised",                "The vendor's own standard",             "One shared spec, market to market"),
 ("Who holds the schedule",    "You do",                           "The vendor, for their leg only",        "The agency, end to end"),
 ("Revisions",                 "Negotiated per vendor",            "Negotiated per vendor",                 "Scoped in the quote"),
 ("Best suited to",            "A single market, one-off",         "A market you already know well",        "A brand experience running in more than one market"),
]
head = ("<tr>"
  + f'<th scope="col" style="{TH % ("#000000","#ffffff")}">Criterion</th>'
  + f'<th scope="col" style="{TH % ("#000000","#ffffff")}">Local specialist</th>'
  + f'<th scope="col" style="{TH % ("#000000","#ffffff")}">In-market vendor</th>'
  + f'<th scope="col" style="{TH % ("#ddccb1","#000000")}">Global brand experience agency</th></tr>')
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
                  "Oddtoe quotes per project after a scoping conversation. Travel and local production are quoted per market.")

# 3. swap the offers row info_banner cards to something relevant (real, live-verified media/pages)
kit = kit.replace(
  'info_banner image="15398" img_height="225" read_more="box" image_effect="dfd-image-scale" style="style-04" '
  'title="Non-Fiction Animator" subtitle="Documentaries &amp; Exhibits" title_font_options="tag:div|font_size:18|'
  'font_family:BebasNeueRegular|line_height:22" subtitle_font_options="tag:div|font_size:10|color:%23ddccb1|'
  'line_height:12" font_options="tag:div|font_size:12|line_height:14" link="url:https%3A%2F%2Fwww.oddtoe.com%2Fstudio%2Fdocumentary-animator%2F|title:Documentary%20Animator"',
  'info_banner image="16055" img_height="225" read_more="box" image_effect="dfd-image-scale" style="style-04" '
  'title="Installation Artist" subtitle="Builds &amp; Environments" title_font_options="tag:div|font_size:18|'
  'font_family:BebasNeueRegular|line_height:22" subtitle_font_options="tag:div|font_size:10|color:%23ddccb1|'
  'line_height:12" font_options="tag:div|font_size:12|line_height:14" link="url:https%3A%2F%2Fwww.oddtoe.com%2Fartist-designer%2Finstallation-artist%2F|title:Installation%20Artist"'
)
kit = kit.replace(
  'info_banner image="14219" img_height="225" read_more="box" image_effect="dfd-image-scale" style="style-04" '
  'title="Animation Agents" subtitle="Networking" title_font_options="tag:div|font_size:18|font_family:BebasNeueRegular|'
  'line_height:22" subtitle_font_options="tag:div|font_size:10|color:%23ddccb1|line_height:12" '
  'font_options="tag:div|font_size:12|line_height:14" link="url:https%3A%2F%2Fwww.oddtoe.com%2Fanimation-agents%2F|title:Animation%20Agents"',
  'info_banner image="15008" img_height="225" read_more="box" image_effect="dfd-image-scale" style="style-04" '
  'title="Portfolio of Work" subtitle="Experiences &amp; Designs" title_font_options="tag:div|font_size:18|'
  'font_family:BebasNeueRegular|line_height:22" subtitle_font_options="tag:div|font_size:10|color:%23ddccb1|'
  'line_height:12" font_options="tag:div|font_size:12|line_height:14" link="url:https%3A%2F%2Fwww.oddtoe.com%2Fportfolio-aggregate%2F|title:Portfolio%20of%20Work"'
)
# card captions (the shortcode's inner text): card 1 "Melbourne, Australia" already fits Installation
# Artist unchanged; card 2's leftover "USA, Europe, Asia" (from Animation Agents) does not fit a
# portfolio card, so retarget it to what the card is actually showing.
assert 'title:Portfolio%20of%20Work"]USA, Europe, Asia[/info_banner]' in kit, "card 2 caption swap target not found"
kit = kit.replace('title:Portfolio%20of%20Work"]USA, Europe, Asia[/info_banner]',
                   'title:Portfolio%20of%20Work"]Experiences &amp; Designs[/info_banner]')

# 4. enquiry-form heading + subtitle -- tailored to THIS page's job, never left as kit stock copy (lesson 12)
kit = kit.replace(
  '[dfd_heading delimiter_settings="border-bottom-style:solid;|border-bottom-width:1px;|width:50px;|border-bottom-color:#dddddd;" '
  'style="style_02" subtitle="Tell us what you are imagining&hellip;" title_font_options="tag:h2" '
  'subtitle_font_options="tag:h3"]Want to talk about a project?[/dfd_heading]',
  '[dfd_heading delimiter_settings="border-bottom-style:solid;|border-bottom-width:1px;|width:50px;|border-bottom-color:#dddddd;" '
  'style="style_02" subtitle="Tell us which markets it needs to run in&hellip;" title_font_options="tag:h2" '
  'subtitle_font_options="tag:h3"]Running a brand experience in more than one market?[/dfd_heading]'
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
#    "global brand experience agency" is 4 words, and several headings on this page run 7-11 words
#    long -- e.g. "Local vendor or global brand experience agency, and does the difference matter?" --
#    which wraps badly in a 1/3 column. Hero row_inner carries offset= attrs that override width at
#    desktop sizes (lesson 7), so those must change too; pat-section-1/2 have no offset attr, width
#    alone suffices there.
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

# 9. PER-PAGE NEAR-BLACK (README lesson 13) -- unused tint (not plum/teal/umber, per design-language.md's
#    "never give the same tint to two pages in one cluster" ledger). crum_page_custom_bg_color is Ronneby
#    post meta and STILL cannot be set over REST -- set it to the same hex (#1a1e26) in wp-admin Page Options.
kit, tint_notes = retint(kit, 'slate')

# ─────────────────────────── write + report ───────────────────────────
os.makedirs(OUTDIR, exist_ok=True)
io.open(OUT,"w",encoding="utf-8").write(kit)
left = re.findall(r'\{\{([A-Z0-9_]+)', kit)
print("TINT NOTES:", tint_notes)
print("YOAST SEO TITLE: Global Brand Experience Agency | Oddtoe, Melbourne")
print("META DESCRIPTION: Oddtoe is a Melbourne-based global brand experience agency -- one creative direction, one build spec, and local partners wherever your activation runs.")
print("wrote", OUT, len(kit), "chars | unfilled tokens:", left or "none")
