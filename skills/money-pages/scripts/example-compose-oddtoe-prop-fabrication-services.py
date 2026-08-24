#!/usr/bin/env python3
# Compose the Oddtoe "Prop Fabrication Services" MONEY PAGE from design-kit-oddtoe.html.
# Standing override build (Otto, 24 Aug 2026) — /prop-fabrication-services/ was 404, so this is
# tonight's build regardless of the shortlist thread.
#
# CANNIBALISATION GUARDRAILS (GSC, 180d):
#   Target: "prop fabrication services" cluster = 429 impr / 0 clicks / pos 37.3, currently served
#   by /artist-designer/prop-designer-maker/ (wrong page — that page is about the MAKERS, not the
#   service of fabrication).
#   DO NOT bid for the queries /artist-designer/prop-designer-maker/ already ranks page 1 for:
#   "prop making companies australia" (7.1), "theatrical prop makers australia" (4.5),
#   "theatre prop makers manufacturers australia" (4.6), "prop makers australia" (8.4),
#   "film prop fabrication companies australia" (6.9), "australian prop making companies theatre
#   film" (6.6). None of those phrases appear as headings or repeated keyphrases below. This page
#   targets the SERVICE/PROCESS framing only ("prop fabrication services", "prop fabrication",
#   "custom prop fabrication") and links OUT to prop-designer-maker for portfolio/maker credentials
#   rather than restating them (offers-row card + in-body link).
# NO PRICES: design-kit-README + brands.md — Oddtoe pricing is TO FILL, no Oddtoe page may quote one.
# NO EXTERNAL STATS: outbound egress to the one candidate source (Screen Australia) was blocked in
# this environment tonight, so no statistic could be freshly verified — the page carries no invented
# numbers rather than an unverified one.
import re, os, base64, urllib.parse, urllib.request, json

HERE = os.path.dirname(os.path.abspath(__file__))
KIT  = os.path.join(HERE, "..", "references", "design-kit-oddtoe.html")
OUT  = os.path.join(HERE, "..", "references", "composed", "prop-fabrication-services-2026-08-24.html")

CTA_URL = urllib.parse.quote("https://www.oddtoe.com/contact-oddtoe/", safe="")

def link(url, label):
    return f'<strong><a class="dfd-custom-link-decorated" href="{url}">{label}</a></strong>'
def plain(t):
    """FAQ answers carry markup for the accordion; the FAQPage JSON-LD must be plain text."""
    return re.sub(r"<[^>]+>", "", t).replace("&hellip;", "…").replace("&mdash;", "—")

CANONICAL = ("Oddtoe is an experiential design and generative-AI animation studio based in Melbourne, "
             "creating projection, installation, and animated work for events, venues, and galleries.")

P = 'style="line-height: 22px; text-align: left;"'

FAQ = [
 ("What is prop fabrication?",
  "Prop fabrication is turning a <strong>reference, sketch or brief</strong> into a physical object built to "
  "spec &mdash; carved foam, 3D print, cast resin or hand-finished timber, depending on what the piece needs "
  "to do. It covers the <strong>design, build and finish</strong> in one workshop, not just the making."),
 ("What materials do you fabricate props from?",
  "Whatever the piece calls for: <strong>EVA foam and Sintra</strong> for anything worn or carried, "
  "<strong>3D printing</strong> for repeatable or highly detailed parts, <strong>mould and cast resin</strong> "
  "for hero pieces that need to survive handling, and timber or steel where a prop has to bear real weight."),
 ("How long does prop fabrication take?",
  "It depends on the <strong>complexity, the finish and how many are needed</strong>. A single hero piece and "
  "a run of ten identical units are different jobs even at the same size. Oddtoe scopes a build timeline "
  "once the brief and reference material are in, rather than quoting a generic turnaround."),
 ("Do you fabricate for theatre, film and events, or just one?",
  "All three, plus brand and gallery work. The <strong>build process is the same</strong> whether the piece "
  "is walking on stage, appearing on camera, or standing on an event floor &mdash; what changes is the "
  "finish standard and how much the prop needs to withstand repeat use."),
 ("Where can I see examples of finished props?",
  "The studio's " + link("https://www.oddtoe.com/artist-designer/prop-designer-maker/", "prop design and making")
  + " page carries the <strong>finished portfolio</strong> and introduces the people doing the making."),
]

TOKENS = {
 "PAGE_SUBTITLE": "Need it built to spec?",
 "PAGE_TITLE": "Prop Fabrication Services",
 "UPDATED_DATE": "August 2026",
 "HOOK": ("Oddtoe's <strong>prop fabrication services</strong> take a reference or a rough sketch and build "
          "the physical object &mdash; foam, resin, 3D-printed or hand-finished &mdash; ready for camera, "
          "stage or an event floor. <strong>One workshop</strong> handles the design, the build and the "
          "finish, so you brief once and collect a <strong>finished piece</strong>."),

 "SECTION_A_SUBTITLE": "The short version",
 "SECTION_A_HEADING": "What does a prop fabrication service actually do?",
 "SECTION_A_INTRO": ("A prop fabrication service turns a brief into a built object: it designs the piece, "
          "chooses the <strong>materials and build method</strong>, and finishes it to the standard the job "
          "needs. Oddtoe runs that whole path in one workshop, so you are not coordinating a "
          "<strong>sculptor</strong>, a <strong>painter</strong> and a <strong>rigger</strong> separately."),
 "CANONICAL_SENTENCE": CANONICAL,

 "SECTION_B_SUBTITLE": "The question behind the question",
 "SECTION_B_HEADING": "What actually changes the cost of a build?",
 "SECTION_B_ANSWER": ("Four things: <strong>scale</strong>, how much <strong>original design</strong> the "
          "piece needs versus working from a known reference, the <strong>finish standard</strong> it has to "
          "hold up to, and whether you need <strong>one piece or several</strong> identical units."),
 "SECTION_B_CONTEXT": (
   f'<p {P}>Scale is the obvious one, but handling frequency matters just as much. A <strong>small hero prop</strong> '
   'that has to survive a close-up camera shot can take longer than a large background piece nobody examines '
   'closely, because the finish has to hold up under scrutiny.</p>\n'
   f'<p {P}>Original design adds time before the build even starts. Working from a <strong>tight reference</strong> '
   '&mdash; a photo, a drawing, an existing product &mdash; is faster than inventing a form from a paragraph '
   'of description, because there is less to resolve before cutting begins.</p>\n'
   f'<p {P}>Quantity changes the method as much as the hours. A single piece gets sculpted or 3D-printed '
   'directly; a run of <strong>ten identical props</strong> usually gets a mould made first, which costs more '
   'upfront and less per unit. Oddtoe scopes the build and the timeline once it has seen the brief, rather '
   f'than quoting a generic day rate &mdash; {link("https://www.oddtoe.com/contact-oddtoe/", "send the brief")} '
   'and a real person answers.</p>'),

 "PRIMARY_CTA_TEXT": "Send a brief",
 "PRIMARY_CTA_URL": CTA_URL,

 "SECTION_C_SUBTITLE": "What actually gets built",
 "SECTION_C_HEADING": "What can a prop fabrication service build?",
 "SECTION_C_ANSWER": ("Anything a production, event or campaign needs to hold, wear, carry or stand next "
          "to &mdash; from a <strong>hand prop</strong> the size of a coffee cup to an <strong>oversized "
          "piece</strong> built to be photographed against. Hero pieces, background dressing and "
          "<strong>functional builds</strong> that need to open, light up or move all go through the same "
          "workshop."),
 "SECTION_C_DETAIL": (
   f'<p {P}>Fabrication is one half of the job; knowing what to build is the other. Oddtoe\'s '
   f'{link("https://www.oddtoe.com/artist-designer/prop-designer-maker/", "prop design and making")} page '
   'carries the finished portfolio and introduces the people doing the making &mdash; worth a look before '
   'you brief, so you can point at the piece closest to what you need.</p>\n'
   f'<p {P}>An oversized fabricated piece also does double duty as an <strong>activation moment</strong> '
   f'&mdash; see the {link("https://www.oddtoe.com/brand-activation-ideas/", "brand activation ideas")} '
   'page for how a well-built prop earns its own photo queue at an event.</p>'),

 "SECTION_D_SUBTITLE": "How a build gets scoped",
 "SECTION_D_HEADING": "How does a prop fabrication brief turn into a build plan?",
 "SECTION_D_ANSWER": ("Reference material and intended use come first, then <strong>material and method</strong> "
          "get chosen to fit the budget and the timeline, then the build is scheduled against the delivery "
          "date &mdash; not the other way around."),
 "SECTION_D_RATIONALE": (
   f'<p {P}>Method follows brief, not the reverse. A piece that only needs to look right in one photograph '
   'can be built faster and lighter than one that has to be handled every night of a season. Deciding the '
   '<strong>method before the use case</strong> is how budgets blow out on props that were over-built for '
   'their actual job.</p>\n'
   f'<p {P}>The delivery date also decides the method. <strong>3D printing</strong> suits a tight turnaround '
   'on a detailed small piece; <strong>hand carving and casting</strong> suit a hero piece with weeks to '
   'spare. Scoping the build against the date, before committing to a technique, is what keeps a fabrication '
   'project on schedule.</p>'),

 "ARTICLE_1_SUBTITLE": "Where the build actually starts",
 "ARTICLE_1_HEADING": "Inside a prop fabrication brief",
 "ARTICLE_1_BODY": (
   f'<p {P}>I ask for the <strong>reference and the use case</strong> before anything else. A photo, a '
   'drawing, a description of the world the piece lives in &mdash; and how it will actually be used on the '
   'day. Something handled every performance is a different build to something that sits in a single wide '
   'shot, even if they look identical in a sketch.</p>\n'
   f'<p {P}>From there the <strong>material choice</strong> does most of the work. Foam and Sintra carve fast '
   'and suit anything worn or carried. 3D printing is the right call for repeatable detail or a part that '
   'needs to be exact. Cast resin holds up to handling and repaints well, which matters for a hero piece '
   'that has to survive a whole season or shoot.</p>\n'
   f'<p {P}>What surprises most first-time clients is how much of the timeline goes to <strong>finishing</strong>, '
   'well after the object is already built. A raw foam or print looks nothing like the reference until it is '
   'sealed, painted and aged to match the world it sits in. I budget real time for that stage, because a '
   'rushed finish is the fastest way to make an otherwise good build look wrong on camera.</p>\n'
   f'<p {P}>None of this needs a <strong>technical brief</strong>. I would rather work from a <strong>bad photo '
   'of the right idea</strong> than a precise spec for the wrong one &mdash; the material and the method are my '
   '<strong>problem to solve</strong> once I understand what the piece has to do.</p>'),

 "TABLE_SUBTITLE": "Which build method fits your prop?",
 "TABLE_HEADING": "Foam, print or cast: how the three build methods compare",
 "TABLE_INTRO": "The same prop can be built three different ways. This is what changes between them.",

 "ARTICLE_2_SUBTITLE": "What to send when you brief a build",
 "ARTICLE_2_HEADING": "How to brief a prop fabrication project",
 "ARTICLE_2_BODY": (
   f'<p {P}>Send <strong>reference images first</strong>, even rough ones. A photo of something close to '
   'what you want, or a sketch on a napkin, tells me more than a paragraph of adjectives. Say what the piece '
   'is for and where it will be seen &mdash; camera, stage, or an event floor &mdash; because that decides '
   'the finish standard before the design even starts.</p>\n'
   f'<p {P}>Tell me <strong>how it gets used</strong>. Something picked up and set down once is a '
   'different build to something carried through a full run of performances. Say how many are needed too &mdash; '
   'one hero piece and a set of <strong>ten identical units</strong> are scoped and priced differently from '
   'the first conversation.</p>\n'
   f'<p {P}>Share whatever <strong>constraints</strong> already exist: a weight limit for something worn, a '
   'size limit for transport, a colour that has to match an existing set or costume. Constraints narrow the '
   'material choice fast and save a round of revisions later.</p>\n'
   f'<p {P}>If you are not sure fabrication is even the right approach &mdash; sometimes an existing piece '
   'can be sourced and modified faster than one built from scratch &mdash; say that too. Send the brief '
   f'through the {link("https://www.oddtoe.com/contact-oddtoe/", "contact page")} and I will tell you '
   'honestly which path suits the timeline and the budget.</p>'),

 "FAQ_TOPIC": "prop fabrication services",
 "FAQ_CTA_TEXT": "Send a brief",
 "FAQ_CTA_URL": CTA_URL,
}
for i,(q,a) in enumerate(FAQ, start=1):
    TOKENS[f"FAQ_Q{i}"]=q; TOKENS[f"FAQ_A{i}"]=a

# ───────────────────────────── build ─────────────────────────────
kit = open(KIT, encoding="utf-8").read()

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
 ("Best for",              "Worn or carried pieces, fast turnaround", "Repeatable or highly detailed parts", "Hero pieces that get handled repeatedly"),
 ("Turnaround",            "Fastest",                                  "Fast for one part, slower for many",  "Slower — a mould has to be made first"),
 ("Repeat units",          "Each one hand-carved separately",          "Reprints identically",                "Cheap per unit once the mould exists"),
 ("Durability",            "Light knocks only",                        "Depends on the print material",       "Holds up to nightly handling"),
 ("Weight",                "Very light",                               "Light to moderate",                   "Heavier, closer to the real object"),
 ("Fine detail",           "Limited by the carving",                   "Very high",                            "High, and repeats exactly"),
]
head = ("<tr>"
  + f'<th scope="col" style="{TH % ("#000000","#ffffff")}">Criterion</th>'
  + f'<th scope="col" style="{TH % ("#000000","#ffffff")}">Foam &amp; Sintra</th>'
  + f'<th scope="col" style="{TH % ("#000000","#ffffff")}">3D printing</th>'
  + f'<th scope="col" style="{TH % ("#ddccb1","#000000")}">Mould &amp; cast resin</th></tr>')
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
                  "Oddtoe quotes each build after a scoping conversation. Materials and finish standard decide the price.")

# 3. fill every remaining token
kit = fill(kit)

# 4. strip HTML comments (WPBakery mangles stray text between rows)
kit = re.sub(r'<!--.*?-->', '', kit, flags=re.S)

# 5. WIDEN THE TABLE COLUMN (lesson 1/9 — 4 columns overflow the kit's default 1/3 table row).
rows=[m.start() for m in re.finditer(r'\[vc_row(?![_a-z])', kit)]+[len(kit)]
ti=next(i for i in range(len(rows)-1) if '<table' in kit[rows[i]:rows[i+1]])
seg=kit[rows[ti]:rows[ti+1]]
assert seg.count('[vc_column_inner width="1/3"]')==3, seg.count('[vc_column_inner width="1/3"]')
seg=seg.replace('[vc_column_inner width="1/3"]','[vc_column_inner width="1/6"]',1)          # left gutter
seg=seg.replace('[vc_column_inner width="1/3"]','[vc_column_inner width="2/3"]',1)          # content
seg=seg.replace('[vc_column_inner width="1/3"]','[vc_column_inner width="1/6"]',1)          # right gutter
kit=kit[:rows[ti]]+seg+kit[rows[ti+1]:]

# 6. offers row: swap the seeded banners for real cards pulled live from the site (Prop Maker is the
#    REQUIRED guardrail link — portfolio + maker credentials live there, not restated here).
auth = 'Basic ' + base64.b64encode(f"{os.environ['WP_ODDTOE_USER']}:{os.environ['WP_ODDTOE_APP_PASSWORD']}".encode()).decode()
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
def wp_get(path):
    req = urllib.request.Request(f'https://www.oddtoe.com/wp-json/wp/v2/{path}',
                                  headers={'Authorization': auth, 'User-Agent': UA})
    return json.load(urllib.request.urlopen(req))
def page_raw_by_slug(slug):
    results = wp_get(f'pages?slug={slug}&context=edit')
    assert results, f"no page found for slug {slug}"
    return results[0]['content']['raw']

def find_banner(raw, title):
    for b in re.findall(r'\[info_banner.*?\[/info_banner\]', raw, re.S):
        if title in b:
            return b
    return None

prop_maker_banner = find_banner(page_raw_by_slug('brand-activation-ideas'), 'Prop Maker')
portfolio_banner = find_banner(page_raw_by_slug('thank-you-oddtoe'), 'Portfolio of Work')
assert prop_maker_banner and portfolio_banner, "could not find Prop Maker / Portfolio of Work banners live"

offers_block = re.search(r'\[vc_row bg_check="row-background-dark" anchor="related-workshops".*?\[/vc_row\]', kit, re.S)
ob = re.findall(r'\[info_banner.*?\[/info_banner\]', kit[offers_block.start():offers_block.end()], re.S)
assert len(ob) == 2, f"expected 2 seeded offer banners, found {len(ob)}"
kit = kit.replace(ob[0], prop_maker_banner, 1)
kit = kit.replace(ob[1], portfolio_banner, 1)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(kit)

left = re.findall(r'\{\{([A-Z0-9_]+)', kit)
print("YOAST SEO TITLE: Prop Fabrication Services Melbourne | Oddtoe")
print("META DESCRIPTION: Oddtoe's prop fabrication services turn a brief into a built object in foam, resin, 3D print or cast — one workshop for theatre, film, events and brand work.")
print("wrote", OUT, len(kit), "chars | unfilled tokens:", left or "none")
