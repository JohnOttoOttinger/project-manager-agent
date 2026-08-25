#!/usr/bin/env python3
# Compose the Oddtoe "AI Animation Studios" MONEY PAGE from design-kit-oddtoe.html.
# Output: skills/money-pages/references/composed/ai-animation-studios-<date>.html
#
# SOURCE: Otto's shortlist reply "1" to "Money page candidates — 2026-08-25" (thread
# 1a0378efcfe97d1c), Part A #1 "AI animation studios".
#
# CANNIBALISATION GUARDRAILS (GSC, 180d to 2026-08-25):
#   - "ai animation studios" cluster = 351 impr / 1 click / avg pos 16.4, currently served by
#     /studio/generative-ai-animator/ (wrong page — only 12.1 avg pos / 20% page-1 share for this cluster).
#   - DO NOT target "most innovative animation studios using ai technology" — that phrase already
#     ranks PAGE ONE (pos 9.2) on /studio/generative-ai-animator/. Never write that exact phrase here.
#   - Framing: this page is COMPARISON/ROUNDUP intent ("what makes an AI animation studio, how do
#     you evaluate one") vs. the existing page's direct "hire us" service intent. Links out to
#     /studio/generative-ai-animator/ for the full direct-hire pitch rather than restating it.
# NO PRICES: design-kit-README + brands.md — Oddtoe pricing is TO FILL, no Oddtoe page may quote one.
# NO EXTERNAL STATS: outbound fetches to third-party stat sources (Grand View Research, Screen
# Australia) were blocked by the sandbox network policy this run, so no third-party statistic is
# cited — per geo-playbook, an unverified source is not used. Otto can add one once he re-verifies it.
import re, io, os, base64, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
KIT  = os.path.join(HERE, "..", "references", "design-kit-oddtoe.html")
OUTDIR = os.path.join(HERE, "..", "references", "composed")
OUT  = os.path.join(OUTDIR, "ai-animation-studios-2026-08-25.html")

CTA_URL = urllib.parse.quote("https://www.oddtoe.com/contact-oddtoe/", safe="")

def link(url, label):
    return f'<strong><a class="dfd-custom-link-decorated" href="{url}">{label}</a></strong>'
def plain(t):
    """FAQ answers carry markup for the accordion; the FAQPage JSON-LD must be plain text."""
    return re.sub(r"<[^>]+>", "", t).replace("&hellip;", "…").replace("&mdash;", "—")

CANONICAL = ("Oddtoe is an experiential design and generative-AI animation studio based in Melbourne, "
             "creating projection, installation, and animated work for events, venues, and galleries.")

P = 'style="line-height: 22px; text-align: left;"'

GEN_AI_PAGE = "https://www.oddtoe.com/studio/generative-ai-animator/"
AGENCY_PAGE = "https://www.oddtoe.com/animation-agency/"
CHAR_PAGE   = "https://www.oddtoe.com/artist-designer/character-designer/"
COMEDY_PAGE = "https://www.oddtoe.com/artist-designer/comedy-writer/"
PROP_PAGE   = "https://www.oddtoe.com/artist-designer/prop-designer-maker/"
WHATIS_PAGE = "https://www.oddtoe.com/what-is-generative-ai-animation/"

FAQ = [
 ("What exactly is an AI animation studio?",
  "A studio that uses generative AI somewhere in its pipeline &mdash; for imagery, motion, or both &mdash; "
  "rather than hand-animating every frame from scratch. That label says nothing on its own about "
  "<strong>quality</strong>. What matters is who <strong>directs</strong> the output and what happens to a shot "
  "after the AI generates a first pass."),
 ("Is Oddtoe an AI animation studio?",
  "Yes, among other things. Generative tools are one technique inside a pipeline that starts with "
  "<strong>illustration and motion design</strong> &mdash; the fuller pitch is on the "
  + link(GEN_AI_PAGE, "generative AI animator") + " page, and the studio's own definition sits near the "
  "top of this one."),
 ("How do I tell a good AI animation studio from a studio that just resells a prompt tool?",
  "Ask to see <strong>one full sequence</strong>, not a highlight reel of stills, ask who "
  "<strong>signs off</strong> on a shot before it reaches you, and ask what the studio's non-AI craft looks "
  "like. A studio that dodges the second and third questions is likely reselling a tool."),
 ("Can an AI animation studio still do physical or 3D work?",
  "Only if it has craft outside the AI tools. Oddtoe's own studio builds "
  + link(PROP_PAGE, "props and 3D pieces") + " and projection work by hand &mdash; there is no generative "
  "shortcut for an object a crowd can walk around or a building a projection has to fit exactly."),
 ("Does AI replace the animator entirely?",
  "Not for work meant to hold up under a close look. The tools speed up <strong>iteration</strong> and "
  "widen what a small team can attempt; a person still checks <strong>every shot</strong> before it ships."),
]

TOKENS = {
 "PAGE_SUBTITLE": "So you&#8217;re comparing&hellip;",   # ellipsis 1/2 — runs into the H1
 "PAGE_TITLE": "AI Animation Studios",
 "UPDATED_DATE": "August 2026",
 "HOOK": ("&#8220;<strong>AI animation studio</strong>&#8221; is not one thing yet. The label covers a "
          "hobbyist running prompts through a template and a working studio that uses generative tools "
          "for part of a much larger pipeline. Here, that is Oddtoe: <strong>illustration and motion "
          "design first</strong>, AI as <strong>one technique</strong> among several, directed by a human "
          "at every stage."),

 "SECTION_A_SUBTITLE": "The short version",
 "SECTION_A_HEADING": "What actually makes an AI animation studio different?",
 "SECTION_A_INTRO": ("An AI animation studio uses generative tools somewhere in its pipeline instead of "
          "hand-animating every frame by default. That alone says nothing about the "
          "<strong>quality</strong> of the result. The real difference is who is <strong>directing</strong> "
          "the generation, and whether <strong>rigging, compositing and edit</strong> happen properly after "
          "the first AI pass or not at all."),
 "CANONICAL_SENTENCE": CANONICAL,

 "SECTION_B_SUBTITLE": "Not all &#8220;AI&#8221; means the same thing",
 "SECTION_B_HEADING": "Built around AI from the start, or added it later &mdash; does it matter?",
 "SECTION_B_ANSWER": ("Less than the label suggests. A studio <strong>built around AI from the start</strong> "
          "and a studio that <strong>added AI to an existing pipeline</strong> can both produce "
          "<strong>directed, finished work</strong> &mdash; or both can ship a raw generation with no edit. "
          "The tool tells you less than the <strong>process around it</strong>."),
 "SECTION_B_CONTEXT": (
   f'<p {P}>Being built around AI from the start sounds newer and therefore better, and sometimes it is: a '
   'studio set up that way has usually already solved the <strong>rigging and consistency</strong> problems '
   'that trip up a first attempt. But it can equally describe a shop with '
   '<strong>no traditional craft to fall back on</strong> when a generation does not do what the brief '
   'needs.</p>\n'
   f'<p {P}>Adding AI to an established studio carries the opposite risk: years of habits built around '
   '<strong>hand animation</strong> can turn the tools into an afterthought instead of a proper part of the '
   'pipeline. I run it the other way on purpose &mdash; the <strong>illustration and motion-design '
   'background</strong> comes first, and AI gets added where it speeds the work up.</p>\n'
   f'<p {P}>Either way, ask the same question: what happens to a <strong>generated shot</strong> before it '
   'reaches you? A vague answer there matters more than which side of the split a studio sits on.</p>'),

 "PRIMARY_CTA_TEXT": "Start a project",
 "PRIMARY_CTA_URL": CTA_URL,

 "SECTION_C_SUBTITLE": "Before you sign anything",
 "SECTION_C_HEADING": "What should you actually check before hiring an AI animation studio?",
 "SECTION_C_ANSWER": ("<strong>Four things.</strong> Who directs the output after the AI generates it, "
          "whether <strong>consistency</strong> holds shot to shot, what the studio's non-AI craft looks "
          "like, and how <strong>revisions</strong> work when a generation misses the brief. Vague answers "
          "to the second and third are the giveaway that a studio is <strong>just reselling a tool</strong>."),
 "SECTION_C_DETAIL": (
   f'<p {P}>Consistency is the one that actually breaks projects: these tools are excellent at a '
   '<strong>single striking frame</strong> and much less reliable at holding a character&#8217;s face, a '
   'brand colour or a prop steady across a hundred shots. Ask to see a <strong>full sequence</strong>, not '
   'a showreel of stills.</p>\n'
   f'<p {P}>The non-AI craft question matters because it is the fallback. When a generation will not do '
   'what the brief needs, someone has to be able to <strong>draw, rig or composite the shot '
   'properly</strong>. Oddtoe&#8217;s own pipeline runs through illustration and motion design first &mdash; '
   'there is a fuller account of how the AI fits into it on the '
   + link(GEN_AI_PAGE, "generative AI animator") + ' page, and a plainer explainer on '
   + link(WHATIS_PAGE, "what generative AI animation actually is") + '.</p>\n'
   f'<p {P}>It is also worth knowing what a studio will not pretend AI can do. Physical and 3D work &mdash; '
   + link(PROP_PAGE, "props and 3D making") + ' among them &mdash; still gets made by hand, because there is '
   'no generative shortcut for an object a crowd can walk around.</p>'),

 "SECTION_D_SUBTITLE": "Plainly put",
 "SECTION_D_HEADING": "Should the whole animation come from AI?",
 "SECTION_D_ANSWER": ("Not yet, for anything meant to hold up under a close look. Generative tools are "
          "strong at <strong>speed and scale</strong> &mdash; more variations, faster, than hand animation "
          "alone &mdash; and weak at <strong>holding a specific design steady</strong> without a human "
          "checking every shot. Speed is the real advantage. Supervision does not disappear."),
 "SECTION_D_RATIONALE": (
   f'<p {P}>I would rather say that plainly than sell &#8220;fully AI-generated&#8221; as a feature. The '
   'subjects worth animating well &mdash; <strong>science, history, a client&#8217;s actual brand</strong> '
   '&mdash; are exactly the ones where a slightly wrong detail gets noticed, and a generative model does '
   'not know the difference between a good shot and a wrong one.</p>\n'
   f'<p {P}>Where AI earns its place is <strong>volume</strong>: a small studio producing work that would '
   'once have needed a much bigger crew, because a first pass now takes hours instead of days. That is a '
   'real advantage. It is a different claim than &#8220;no humans required,&#8221; and worth asking any '
   'studio to be specific about which one it is making.</p>'),

 "ARTICLE_1_SUBTITLE": "Where the label comes from",
 "ARTICLE_1_HEADING": "Why &#8220;AI animation studio&#8221; is a wide net, and I don&#8217;t mind being caught in it",
 "ARTICLE_1_BODY": (
   f'<p {P}>I get found under &#8220;AI animation studio&#8221; alongside operations that are, to put it '
   'plainly, one person running a <strong>subscription tool</strong>. That is fine &mdash; search does not '
   'know the difference yet, and telling the two apart is not its job. What matters is what a client finds '
   'once they <strong>click through</strong>.</p>\n'
   f'<p {P}>My own path into this runs through <strong>illustration first</strong>. I have been a political '
   'cartoonist, a puppeteer, a data visualiser and a street artist, and my foundational skill through all '
   'of it has been illustration. Oddtoe has worked with organisations including <strong>National '
   'Geographic</strong> since 2006. Generative AI built on top of that background; it did not replace it '
   '&mdash; the full pitch for how the studio runs is on the '
   + link(GEN_AI_PAGE, "generative AI animator") + ' page.</p>\n'
   f'<p {P}>What changed with the tools is <strong>scale</strong>, and judgement did not change with it. A '
   'small studio with twenty years of animation experience can now produce work that used to need a much '
   'bigger crew &mdash; more variations, faster iteration, a first pass in hours rather than days. Someone '
   'still has to look at every one of those variations and say <strong>yes or no</strong>.</p>\n'
   f'<p {P}>That is the part I do not think the &#8220;AI animation studio&#8221; label captures well. It '
   'describes a <strong>technique</strong>, and technique is not a level of care. Two studios can use the '
   'identical tool and produce very different reliability &mdash; one checks every shot against the brief, '
   'the other ships whatever generates cleanly.</p>\n'
   f'<p {P}>Comparing studios under this label, the technique is the least useful thing to ask about. Ask '
   'what a bad generation costs you: time, a revision round, or nothing at all because someone already '
   'caught it before you saw the cut. See the ' + link(AGENCY_PAGE, "animation agency page")
   + ' when the brief needs more than one discipline running at once.</p>'),

 "TABLE_SUBTITLE": "Three ways to buy AI animation",
 "TABLE_HEADING": "DIY prompt tool, another studio, or Oddtoe?",
 "TABLE_INTRO": "Same starting point, generative AI, three very different pipelines behind it.",

 "ARTICLE_2_SUBTITLE": "What to actually ask&hellip;",   # ellipsis 2/2 — hands over to the content
 "ARTICLE_2_HEADING": "The questions that separate a studio from a subscription",
 "ARTICLE_2_BODY": (
   f'<p {P}>Ask to see <strong>one full sequence</strong>, not a showreel of stills. A striking single '
   'frame is the easiest thing a generative model produces; a character that holds its face for sixty '
   'consecutive shots is the hard part, and it is the part that actually ships in your project.</p>\n'
   f'<p {P}>Ask who <strong>signs off</strong> on a shot before it reaches you &mdash; software does not '
   'count as an answer. A named person means you can ask what their background is outside AI, and '
   + link(CHAR_PAGE, "character design") + ' or ' + link(COMEDY_PAGE, "comedy and story writing")
   + ' are the kind of craft that tells you someone can catch a bad shot instead of only generating another '
   'one.</p>\n'
   f'<p {P}>Ask what happens when a generation is close but not right. A cheap tool makes a re-prompt free, '
   'which sounds good until you are the eleventh re-prompt with no idea why the tenth one did not work '
   'either. A properly run pipeline treats that as a <strong>revision round</strong> with a person driving '
   'it, priced and scoped like the rest of the project.</p>\n'
   f'<p {P}>And ask what the studio does when AI is not the right tool for the brief. Some briefs want a '
   'physical presence &mdash; a ' + link(PROP_PAGE, "prop or a built piece")
   + ' &mdash; and no amount of generation replaces someone who can build or install the real thing. One '
   'answer to every brief is a <strong>warning sign</strong> &mdash; the studio you want has a different '
   'one ready for the brief that does not fit its main tool.</p>\n'
   f'<p {P}>If none of that sounds like the operation you are evaluating, it is worth saying so '
   '<strong>directly</strong> rather than working around it. I would rather lose the job at the '
   '<strong>scoping stage</strong> than at the delivery date.</p>'),

 "FAQ_TOPIC": "AI Animation Studios",
 "FAQ_CTA_TEXT": "Brief the studio",
 "FAQ_CTA_URL": CTA_URL,
}
for i,(q,a) in enumerate(FAQ, start=1):
    TOKENS[f"FAQ_Q{i}"]=q; TOKENS[f"FAQ_A{i}"]=a

# ───────────────────────────── build ─────────────────────────────
kit = io.open(KIT, encoding="utf-8").read()

# 1. FAQ JSON-LD: decode the pre-encoded payload, fill with PLAIN TEXT, re-encode (urlencode THEN base64)
def fill(txt):
    for k,v in TOKENS.items():
        txt = re.sub(r'\{\{'+k+r'(?::[^}]*)?\}\}', lambda m: v, txt)
    return txt
def redo_raw_html(m):
    dec = urllib.parse.unquote(base64.b64decode(m.group(1)).decode())
    for k, v in TOKENS.items():
        dec = re.sub(r'\{\{'+k+r'(?::[^}]*)?\}\}', lambda mm, v=v: plain(v), dec)
    return "[vc_raw_html]" + base64.b64encode(urllib.parse.quote(dec, safe="").encode()).decode() + "[/vc_raw_html]"
kit = re.sub(r'\[vc_raw_html\]([A-Za-z0-9+/=]+)\[/vc_raw_html\]', redo_raw_html, kit)
_faqld = urllib.parse.unquote(base64.b64decode(re.search(r'\[vc_raw_html\]([A-Za-z0-9+/=]+)\[/vc_raw_html\]', kit).group(1)).decode())
assert "<" not in re.sub(r'"name":"[^"]*"', '', _faqld).replace('"text":"','').split('"text":"')[0] or True
import json as _json
_ld = _json.loads(_faqld[_faqld.index("{"):_faqld.rindex("}")+1])
for _q in _ld["mainEntity"]:
    assert "<" not in _q["acceptedAnswer"]["text"], _q["acceptedAnswer"]["text"]

# 2. table row: drop the PRICING exemplar (no Oddtoe prices permitted), keep + refill the COMPARISON one
TH  = ("padding: 14px 18px; text-align: left; background-color: %s !important; border: none !important; "
       "border-bottom: 2px solid #ddccb1 !important; font-family: 'Bebas Neue', sans-serif; font-size: 21px; "
       "font-weight: normal; letter-spacing: 1px; color: %s !important; white-space: nowrap;")
TD  = ("padding: 12px 18px; text-align: left; background-color: %s !important; border: none !important; "
       "border-bottom: 1px solid #26161f !important; color: #ffffff !important;%s")
ROWS = [
 ("Who directs the shot",          "You, alone",              "Varies by studio",        "One director, every shot"),
 ("Non-AI fallback craft",         "None",                    "Sometimes",                "Illustration & motion design"),
 ("Consistency shot to shot",      "Manual re-prompting",     "Depends on the studio",    "Rigged and checked"),
 ("Who fixes a bad generation",    "You, manually",           "Depends on the plan",      "The studio reworks it"),
 ("Physical or 3D elements",       "Not offered",             "Rarely offered",           "Made in-house"),
 ("Revisions",                     "Free, unlimited re-prompts","Varies by plan",         "Scoped in the quote"),
 ("Best suited to",                "A single quick test",     "High volume, lower stakes","Work that has to hold up to scrutiny"),
]
head = ("<tr>"
  + f'<th scope="col" style="{TH % ("#000000","#ffffff")}">Criterion</th>'
  + f'<th scope="col" style="{TH % ("#000000","#ffffff")}">DIY prompt tool</th>'
  + f'<th scope="col" style="{TH % ("#000000","#ffffff")}">Another AI studio</th>'
  + f'<th scope="col" style="{TH % ("#ddccb1","#000000")}">Oddtoe</th></tr>')
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
                  "Oddtoe quotes per project after a scoping conversation. Travel outside Melbourne is quoted separately.")

# 3. fill every remaining token
kit = fill(kit)

# 4. strip HTML comments (WPBakery mangles stray text between rows)
kit = re.sub(r'<!--.*?-->', '', kit, flags=re.S)

# 5. WIDEN THE TABLE ROW to 1/6 + 2/3 + 1/6 — this table has FOUR columns (lesson 1 / design-kit-README).
rows=[m.start() for m in re.finditer(r'\[vc_row(?![_a-z])', kit)]+[len(kit)]
ti=next(i for i in range(len(rows)-1) if '<table' in kit[rows[i]:rows[i+1]])
seg=kit[rows[ti]:rows[ti+1]]
assert seg.count('[vc_column_inner width="1/3"]')==3, seg.count('[vc_column_inner width="1/3"]')
seg=seg.replace('[vc_column_inner width="1/3"]','[vc_column_inner width="1/6"]',1)
seg=seg.replace('[vc_column_inner width="1/3"]','[vc_column_inner width="2/3"]',1)
seg=seg.replace('[vc_column_inner width="1/3"]','[vc_column_inner width="1/6"]',1)
kit=kit[:rows[ti]]+seg+kit[rows[ti+1]:]

# 6. WIDEN HERO + SECTION-1 + SECTION-2 inner rows to 1/4 + 1/2 + 1/4 (lessons 7 & 8: head noun
#    "AI animation studio" is 3 words, and several headings on this page run 7-9 words long —
#    e.g. "What should you actually check before hiring an AI animation studio?" — which wraps
#    badly in a 1/3 column. Hero row_inner carries offset= attrs that override width at desktop
#    sizes (lesson 7), so those must change too; pat-section-1/2 have no offset attr, width alone
#    suffices there.
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

# ─────────────────────────── write + report ───────────────────────────
os.makedirs(OUTDIR, exist_ok=True)
io.open(OUT,"w",encoding="utf-8").write(kit)
left = re.findall(r'\{\{([A-Z0-9_]+)', kit)
banned_phrase = "most innovative animation studios using ai technology"
assert banned_phrase not in kit.lower(), "GUARDRAIL VIOLATION: banned phrase present"
print("YOAST SEO TITLE: AI Animation Studios | Oddtoe, Melbourne")
print("META DESCRIPTION: What makes an AI animation studio worth hiring, and how to tell one from a studio just reselling a prompt tool. Oddtoe is one working example, Melbourne-based.")
print("wrote", OUT, len(kit), "chars | unfilled tokens:", left or "none")
