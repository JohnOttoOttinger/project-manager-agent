#!/usr/bin/env python3
# Compose the Oddtoe "Animation Agency" MONEY PAGE from design-kit-oddtoe.html.
# Output: animation-agency.html (WPBakery raw body, ready for wp-post.sh)
#
# CANNIBALISATION GUARDRAILS (GSC, 180d to 21 Aug 2026 — see animation-agency-page-spec.md §Purpose):
#   - `animation agency` = 3,597 impr / 1 click / pos 22.4, currently served by /animation-agents/ (wrong page).
#   - DO NOT bid for: "ai animation studio" cluster (owned by /studio/generative-ai-animator/, pos 4.7-9.7)
#     or "animation talent agency" (owned by /animation-agents/, pos 1.8).
#   - So: AI is named as a capability and linked out, never claimed as a phrase; representation seekers
#     are handed to /animation-agents/ rather than served here.
# NO PRICES: design-kit-README + brands.md — Oddtoe pricing is TO FILL, no Oddtoe page may quote one.
import re, io, os, base64, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
KIT  = os.path.join(HERE, "..", "references", "design-kit-oddtoe.html")
OUT  = os.path.join(HERE, "animation-agency.html")

CONTACT = "https://%3A%2F%2F"  # placeholder guard, real one below
CTA_URL = urllib.parse.quote("https://www.oddtoe.com/contact-oddtoe/", safe="")

def link(url, label):
    return f'<strong><a class="dfd-custom-link-decorated" href="{url}">{label}</a></strong>'
def extlink(url, label):
    return (f'<strong><a class="dfd-custom-link-decorated" href="{url}" target="_blank" '
            f'rel="noopener">{label}</a></strong>')
def plain(t):
    """FAQ answers carry markup for the accordion; the FAQPage JSON-LD must be plain text."""
    return re.sub(r"<[^>]+>", "", t).replace("&hellip;", "\u2026").replace("&mdash;", "\u2014")

CANONICAL = ("Oddtoe is an experiential design and generative-AI animation studio based in Melbourne, "
             "creating projection, installation, and animated work for events, venues, and galleries.")

P = 'style="line-height: 22px; text-align: left;"'

FAQ = [
 ("How much does it cost to work with an animation agency?",
  "It depends on <strong>length</strong>, <strong>technique</strong> and how much <strong>original design</strong> "
  "the piece needs. A short generative loop and a fully character-designed series sit at very different ends. "
  "Oddtoe quotes per project after a short scoping conversation, so the number reflects your brief rather than a "
  "rate card you have to reverse-engineer."),
 ("How do I choose the right animation agency?",
  "Look at three things: whether the work on the reel <strong>resembles what you actually need</strong>, whether "
  "<strong>one person will own your project end to end</strong>, and whether they will tell you when an idea will "
  "not work. Ask who is doing the animating and how <strong>revisions</strong> are handled before you sign anything."),
 ("What kinds of projects does an animation agency take on?",
  "For Oddtoe: <strong>television and film work</strong>, commercials, character design, comedy and story writing, "
  "and <strong>projection and experiential pieces</strong>. Some clients want a single fifteen-second spot, others "
  "want a whole world built. Both get scoped the same way, <strong>idea first</strong> and then the team to make it."),
 ("Can an animation agency handle AI or generative animation?",
  "Yes, where the brief calls for it. Oddtoe treats AI as <strong>a tool in the pipeline</strong> and not a "
  "gimmick to sell. It speeds up iteration and opens looks hand-drawing cannot reach, while a "
  "<strong>human director still owns the taste</strong>. There is a fuller explanation on the "
  + link("https://www.oddtoe.com/studio/generative-ai-animator/", "generative AI animator") + " page."),
 ("I am an animator looking for representation. Is this the right page?",
  "No. This page is for people who want animation <strong>made</strong>. If you are an animator, character designer "
  "or writer looking for an <strong>agent</strong>, Oddtoe keeps a separate guide to the "
  + link("https://www.oddtoe.com/animation-agents/", "animation agents and talent firms")
  + " worth approaching. Start there instead."),
]

TOKENS = {
 "PAGE_SUBTITLE": "So you want an&hellip;",           # runs into the H1 — ellipsis rule, shape 1
 "PAGE_TITLE": "Animation agency",
 "UPDATED_DATE": "August 2026",
 "HOOK": ("Oddtoe is an <strong>animation agency</strong> and working studio in Melbourne and Los Angeles. "
          "One team scopes the idea, assembles the right animators and runs the project from first sketch to "
          "final frame. You brief <strong>one studio</strong>, not twelve freelancers, and <strong>one producer</strong> owns "
          "the delivery date."),

 "SECTION_A_SUBTITLE": "The short version",
 "SECTION_A_HEADING": "What does an animation agency actually do?",
 "SECTION_A_INTRO": ("An animation agency turns a brief into finished animated work and manages everyone who "
          "touches it. Oddtoe scopes the idea, assembles the <strong>animators, directors and writers</strong> "
          "the job needs, and runs it <strong>end to end</strong>, so you brief <strong>one team</strong> instead of hiring and coordinating a "
          "dozen separate people."),
 "CANONICAL_SENTENCE": CANONICAL,

 "SECTION_B_SUBTITLE": "Two words, two different jobs",
 "SECTION_B_HEADING": "Agency or studio, and does the difference matter?",
 "SECTION_B_ANSWER": ("A studio makes the frames. An agency handles the frames and also the people, the "
          "schedule and the client. Oddtoe runs as both, so you get studio craft with a <strong>single point "
          "of contact</strong> who owns the <strong>delivery date</strong>, instead of a group chat full of freelancers."),
 "SECTION_B_CONTEXT": (
   f'<p {P}>The distinction matters most <strong>when something goes wrong</strong>. A freelancer who gets sick is your '
   'problem to solve. A studio <strong>reassigns the work internally</strong>. An agency does the same, and also absorbs the '
   'scheduling, the client updates and the <strong>revision rounds</strong> that come with it.</p>\n'
   f'<p {P}>It matters again when a brief needs <strong>more than one discipline</strong>. A piece that wants character '
   'design, a writer and a compositor is <strong>three separate hires</strong> if you are managing it yourself. Oddtoe casts '
   'those roles against the brief and <strong>carries the coordination</strong>, which is usually the part nobody '
   'budgets for.</p>\n'
   f'<p {P}>It cuts both ways: for a single short piece in a style one person already owns, a '
   f'freelancer is often the better buy. See {link("https://www.oddtoe.com/artist-designer/character-designer/", "character design")} '
   f'or {link("https://www.oddtoe.com/studio/documentary-animator/", "documentary animation")} for what the studio does directly.</p>'),

 "PRIMARY_CTA_TEXT": "Start a project",
 "PRIMARY_CTA_URL": CTA_URL,

 "SECTION_C_SUBTITLE": "What actually gets made",
 "SECTION_C_HEADING": "What can an animation agency make for you?",
 "SECTION_C_ANSWER": ("<strong>Television and film work</strong>, commercials, character design, comedy and story writing, "
          "projection and experiential pieces. Oddtoe scopes a fifteen-second spot and a built world the same "
          "way: <strong>the idea first</strong>, then the people to make it."),
 "SECTION_C_DETAIL": (
   f'<p {P}>Each of those is a practice in its own right. '
   f'{link("https://www.oddtoe.com/artist-designer/character-designer/", "Character design")} builds casts you can '
   f'put a franchise around. {link("https://www.oddtoe.com/artist-designer/comedy-writer/", "Comedy and story writing")} '
   'is where the structure comes from. '
   f'{link("https://www.oddtoe.com/artist-designer/prop-designer-maker/", "Prop and 3D making")} covers the physical and '
   'digital objects a production needs. '
   f'{link("https://www.oddtoe.com/artist-designer/projection-artist/", "projection")} takes the work off the screen '
   'and onto a building.</p>\n'
   f'<p {P}>Where a brief calls for it the studio also works in generative AI, as <strong>one technique among '
   f'several</strong> rather than the headline. There is a fuller account on the '
   f'{link("https://www.oddtoe.com/studio/generative-ai-animator/", "generative AI animator")} page.</p>\n'
   f'<p {P}>Knowing who is doing good work is part of the job. The studio keeps a running guide to the '
   f'{link("https://www.oddtoe.com/animation-conferences/", "animation conferences and festivals")} worth '
   'attending, and the industry still does much of its business at '
   + extlink("https://www.annecyfestival.com/le-mifa/presentation-mifa", "Annecy&#8217;s MIFA market")
   + '.</p>'),

 "SECTION_D_SUBTITLE": "How to pick one",
 "SECTION_D_HEADING": "How do you choose an animation agency?",
 "SECTION_D_ANSWER": ("<strong>Three tests.</strong> Does the reel resemble what you actually need, will <strong>one person own the "
          "project end to end</strong>, and will they tell you when an idea will not work? Ask who is doing the "
          "animating and how <strong>revisions</strong> are handled before signing."),
 "SECTION_D_RATIONALE": (
   f'<p {P}>The reel test catches the most common mismatch. Agencies show their <strong>best work, not their most '
   'typical</strong>. If the piece you love was made by somebody who has since left, nobody will mention it unless '
   'you ask.</p>\n'
   f'<p {P}>The ownership test matters because <strong>animation runs long</strong>. If the person who understood the '
   'brief is not the person answering your email in week six, you will <strong>explain it all again</strong>. That is '
   'usually where a <strong>fixed quote</strong> starts growing.</p>\n'
   f'<p {P}>The third test is the one people skip. If an agency agrees with everything you suggest, you are paying '
   'for <strong>hours rather than an opinion</strong>. I would rather tell you an idea will not work while there is '
   'still time to change it.</p>'),

 "ARTICLE_1_SUBTITLE": "Why one team beats twelve",
 "ARTICLE_1_HEADING": "One brief, one producer, one delivery date",
 "ARTICLE_1_BODY": (
   f'<p {P}>The pitch for hiring freelancers directly is that it is <strong>cheaper</strong>, and on a single piece it often '
   'is. The cost that does not appear in the quote is <strong>coordination</strong>. Somebody has to hold the schedule, chase '
   'the files, keep the style consistent between two people who have never spoken, and decide what happens '
   'when the storyboard changes in week three. On a direct-hire job that somebody is you.</p>\n'
   f'<p {P}>That is the part an agency <strong>absorbs</strong>. I take a brief, work out which disciplines it actually '
   'needs, and put a producer on it to carry the schedule and the revisions. You get <strong>one contact '
   'and one delivery date</strong>. Internally the job might touch a character designer, a writer, an animator and a '
   'compositor, and you never have to hold that org chart in your head.</p>\n'
   f'<p {P}>The second thing an agency buys is <strong>casting</strong>. A freelancer works in the style they '
   'already have, and a studio in its house style. An agency picks the hands to suit the '
   'brief, which is how the same team delivers a broad comedy spot one month and a restrained '
   f'{link("https://www.oddtoe.com/studio/documentary-animator/", "documentary sequence")} the next.</p>\n'
   f'<p {P}>None of that makes an agency the right answer <strong>every time</strong>. A fifteen-second loop in a style one '
   'illustrator already owns does not need a producer sitting on top of it. The rule I use is simple: '
   '<strong>the more disciplines a brief touches</strong>, and the longer it runs, the more the coordination is '
   '<strong>worth paying for</strong>.</p>\n'
   f'<p {P}>There is also more work about than usual. '
   + extlink("https://www.screenaustralia.gov.au/drama-report-2024-25-2-7-billion-spent-on-drama-production-in-australia-points-to-holistic-industry-growth/", "Screen Australia&#8217;s Drama Report 2024/25")
   + ' records a record <strong>$2.7 billion</strong> spent on drama production in Australia, up 43 per cent, '
   'with post, digital and visual effects work accounting for <strong>$762 million</strong> of it, up 33 per cent. '
   'When that much is in production the good animators are already busy, which is a practical reason to '
   '<strong>book a team</strong> rather than go looking for one.</p>'),

 "TABLE_SUBTITLE": "Which one is your brief?",
 "TABLE_HEADING": "Freelancer, studio or agency?",
 "TABLE_INTRO": "The same animation can be bought three ways. This is what changes between them.",

 "ARTICLE_2_SUBTITLE": "What to send&hellip;",        # hands over to the content — ellipsis rule, shape 2
 "ARTICLE_2_HEADING": "How to brief an animation agency",
 "ARTICLE_2_BODY": (
   f'<p {P}>Tell me <strong>the outcome, not the shot list</strong>. Who it is for, where it runs, when it has to be live, '
   'and one or two references for the feeling you want. Rough is fine. Working the plan out from a loose '
   'brief is part of what you are paying for, and a brief that arrives as a <strong>locked shot list</strong> often costs more, because the first '
   'thing that happens is unpicking it.</p>\n'
   f'<p {P}>Four things change a quote more than anything else: <strong>the run time</strong>, <strong>the technique</strong>, how much '
   '<strong>original design</strong> the piece needs, and how many <strong>rounds of revision</strong> you expect. A thirty-second piece using '
   'existing brand characters and a thirty-second piece that invents a cast are different jobs at the same '
   'length.</p>\n'
   f'<p {P}><strong>Say what you already have.</strong> Scripts, brand guidelines, a character bible, previous animation, '
   'even a rejected treatment from another agency all <strong>shorten the scoping conversation</strong>. So does saying what '
   'you did not like about the last piece you commissioned.</p>\n'
   f'<p {P}>If you are still deciding whether animation is <strong>the right medium at all</strong>, say that too. I '
   f'also build {link("https://www.oddtoe.com/experiential-marketing/", "experiential and physical work")}, '
   'and some briefs that arrive asking for a film are better served by something people can stand in front '
   f'of. Send it through the {link("https://www.oddtoe.com/contact-oddtoe/", "contact page")} and a real '
   'person reads it.</p>'),

 "FAQ_TOPIC": "animation agencies",
 "FAQ_CTA_TEXT": "Brief us",
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
 ("Who you brief",        "One person",                    "A studio producer",              "One producer who assembles the team"),
 ("Range of styles",      "That person's style",           "The studio's house style",       "Cast to suit the brief"),
 ("Who holds the schedule","You do",                       "The studio",                     "The agency"),
 ("If someone drops out", "You find a replacement",        "The studio reassigns internally", "The agency reassigns internally"),
 ("Revisions",            "Negotiated per round",          "Scoped in the quote",            "Scoped in the quote"),
 ("Disciplines covered",  "One",                           "Whatever is in-house",           "Hired against the brief"),
 ("Best suited to",       "A short piece in a known style","A series in one house style",    "A brief touching several crafts"),
]
head = ("<tr>"
  + f'<th scope="col" style="{TH % ("#000000","#ffffff")}">Criterion</th>'
  + f'<th scope="col" style="{TH % ("#000000","#ffffff")}">Freelancer</th>'
  + f'<th scope="col" style="{TH % ("#000000","#ffffff")}">Studio</th>'
  + f'<th scope="col" style="{TH % ("#ddccb1","#000000")}">Animation agency</th></tr>')
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
# remove pricing block + the 40px spacer div between the two
start, end = tables[0].start(), tables[1].start()
kit = kit[:start] + kit[end:]
kit = re.sub(r'<div style="overflow-x: auto;">\s*<table.*?</table>\s*</div>',
             '<div style="overflow-x: auto;">\n'+newtable+'\n</div>', kit, count=1, flags=re.S)
kit = kit.replace("Footnote, e.g. All prices include GST. Travel outside Melbourne quoted separately.",
                  "Oddtoe quotes per project after a scoping conversation. Travel outside Melbourne is quoted separately.")

# 3. fill every remaining token
kit = fill(kit)

# 4. strip HTML comments (WPBakery mangles stray text between rows)
kit = re.sub(r'<!--.*?-->', '', kit, flags=re.S)

# 5. WIDEN THE TABLE COLUMN (Otto, 21 Aug 2026). The kit puts the table row's content in the middle
#    of a 1/3+1/3+1/3 inner row. Three columns just fit there; this page's comparison table has FOUR,
#    so it overflowed into a horizontal scrollbar on desktop. Widen to 1/6 + 2/3 + 1/6 — the same split
#    the Installation Artist page uses for its own four-column table. Table row ONLY.
rows=[m.start() for m in re.finditer(r'\[vc_row(?![_a-z])', kit)]+[len(kit)]
ti=next(i for i in range(len(rows)-1) if '<table' in kit[rows[i]:rows[i+1]])
seg=kit[rows[ti]:rows[ti+1]]
assert seg.count('[vc_column_inner width="1/3"]')==3, seg.count('[vc_column_inner width="1/3"]')
seg=seg.replace('[vc_column_inner width="1/3"]','[vc_column_inner width="1/6"]',1)          # left gutter
seg=seg.replace('[vc_column_inner width="1/3"]','[vc_column_inner width="2/3"]',1)          # content
seg=seg.replace('[vc_column_inner width="1/3"]','[vc_column_inner width="1/6"]',1)          # right gutter
kit=kit[:rows[ti]]+seg+kit[rows[ti+1]:]

# 6. (removed 24 Aug 2026) The Qwigley cross-promo delimiter is now the KIT DEFAULT — patched into
#    master 16132 and design-kit-oddtoe.html, so every money page inherits it. No per-page step needed.

io.open(OUT,"w",encoding="utf-8").write(kit)
left = re.findall(r'\{\{([A-Z0-9_]+)', kit)
print("YOAST SEO TITLE: Animation Agency Melbourne & Los Angeles | Oddtoe")
print("META DESCRIPTION: Oddtoe is an animation agency and studio in Melbourne and Los Angeles — one team to scope, staff and make your animation, from first sketch to final frame.")
print("wrote", OUT, len(kit), "chars | unfilled tokens:", left or "none")
