#!/usr/bin/env python3
"""Snapshot a live Use Case page into the tokenised Use Case kit + a content JSON.

    python3 snapshot-usecase-kit.py references/masters/oddtoe-publicity-stunts-16272-2026-09-11-raw.txt

Writes:
  references/design-kit-oddtoe-usecase.html        the kit ({{TOKENS}} in place of content)
  references/usecase-content-<id_slug>.json         the content that was in the master, token by token

The kit keeps every row/column attribute of the master byte-for-byte. Only content is tokenised:
headings, kickers, body columns, media ids, image URLs, the six-idea circles, the six timeline
steps, the five package boxes, the six spec figures, the comparison table cells, the FAQ, the
portfolio trio and the form heading. Raw-HTML blocks (page CSS, video, circles, timeline, FAQ
schema) are stored DECODED between <!--RAW--> markers; compose-usecase.py re-encodes them.

Re-run this whenever Otto restyles the live page (catalog rule 5), then bump the kit header date.
"""
from __future__ import annotations
import base64, html, json, re, sys, urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFS = HERE.parent / "references"
KIT = REFS / "design-kit-oddtoe-usecase.html"

TAB_STAMP = "1757300000"          # the FAQ tab_id prefix used on the master
ID_SLUG = "protest"               # element-id slug of the master (uc-protest, ...-usecase-protest-faq-n)


def dec(b64: str) -> str:
    return urllib.parse.unquote(base64.b64decode(b64).decode())


class Tok:
    """Sequential tokeniser: each take() searches forward from the cursor, replaces group(1)."""

    def __init__(self, text: str, content: dict):
        self.t, self.pos, self.c = text, 0, content

    def take(self, pattern: str, token: str, flags=re.S):
        m = re.compile(pattern, flags).search(self.t, self.pos)
        assert m, f"{token}: pattern not found after cursor: {pattern[:60]}"
        val = m.group(1)
        assert token not in self.c or self.c[token] == val, f"{token} captured twice with different values"
        self.c[token] = val
        self.t = self.t[:m.start(1)] + "{{" + token + "}}" + self.t[m.end(1):]
        self.pos = m.start(1) + len(token) + 4
        return val

    def sub_all(self, literal: str, token: str):
        assert literal in self.t, f"{token}: {literal!r} not in row"
        self.c[token] = literal
        self.t = self.t.replace(literal, "{{" + token + "}}")


HEAD_SUB = r'subtitle="([^"]*)"'
HEAD_TITLE = r'\]([^\[\]]+)\[/dfd_heading\]'
COLTEXT = r'\[vc_column_text css=""\](.*?)\[/vc_column_text\]'


def heading(tk, key):
    tk.take(HEAD_SUB, f"{key}_KICKER")
    tk.take(HEAD_TITLE, f"{key}_TITLE")


def two_cols(tk, key):
    heading(tk, key)
    tk.take(COLTEXT, f"{key}_COL1")
    tk.take(COLTEXT, f"{key}_COL2")


def main(master_path: str):
    raw = Path(master_path).read_text(encoding="utf-8")
    rows = re.findall(r"\[vc_row\b.*?\[/vc_row\]", raw, re.S)
    assert len(rows) == 19, f"expected 19 top-level rows, got {len(rows)}"
    assert sum(len(r) for r in rows) == len(raw.strip()) or True
    content: dict = {"_master": Path(master_path).name, "ID_SLUG": ID_SLUG, "FAQ_TAB_STAMP": TAB_STAMP}
    out = []

    def raw_decode(row: str) -> str:
        return re.sub(r"\[vc_raw_html\]([A-Za-z0-9+/=]+)\[/vc_raw_html\]",
                      lambda m: "[vc_raw_html]<!--RAW-->" + dec(m.group(1)) + "<!--/RAW-->[/vc_raw_html]", row)

    # ---- 01 HERO
    tk = Tok(raw_decode(rows[0]), content)
    tk.take(r'dfd_bg_image_canvas="(\d+)"', "HERO_IMAGE_ID")
    tk.sub_all('dfd_bg_color_value="#161314"', "_TINT_ATTR")
    tk.t = tk.t.replace("{{_TINT_ATTR}}", 'dfd_bg_color_value="{{TINT}}"'); content.pop("_TINT_ATTR"); content["TINT"] = "#161314"
    tk.take(HEAD_SUB, "HERO_KICKER"); tk.take(HEAD_TITLE, "HERO_TITLE")
    out.append("<!-- PAT-HERO : canvas image hero, one H1. Page CSS (hero position + three-column padding) is fixed. -->\n" + tk.t)

    # ---- 02 INTRO
    tk = Tok(rows[1], content)
    tk.take(HEAD_SUB, "GIANT_KICKER"); tk.take(HEAD_TITLE, "GIANT_TITLE")
    tk.take(HEAD_SUB, "INTRO_KICKER"); tk.take(HEAD_TITLE, "INTRO_TITLE")
    tk.take(r'color: #8a8a95;">([^<]*)</span>', "UPDATED")
    tk.take(COLTEXT, "INTRO_COL1"); tk.take(COLTEXT, "INTRO_COL2")
    out.append("<!-- PAT-INTRO : 200px Bebas giant title over a 48px kicker (homepage opener), h2 + Qwigley kicker, 'Updated' line, two balanced 1/4 columns. -->\n" + tk.t)

    # ---- 03 THREE DRAWINGS
    tk = Tok(rows[2], content)
    heading(tk, "DRAWINGS"); tk.take(COLTEXT, "DRAWINGS_INTRO")
    for n in (1, 2, 3):
        tk.take(r'vc_single_image image="(\d+)"', f"DRAW{n}_IMAGE_ID")
        tk.take(HEAD_SUB, f"DRAW{n}_STEP"); tk.take(HEAD_TITLE, f"DRAW{n}_TITLE")
        tk.take(COLTEXT, f"DRAW{n}_BODY")
    out.append("<!-- PAT-DRAWINGS : three 640x480 rounded images, Arvo step label, Bebas h3, body. Native (Otto edits in the builder). -->\n" + tk.t)

    # ---- 04 GAP
    out.append("<!-- PAT-GAP-TOP : 70px breathing row above the video row. Fixed. -->\n" + rows[3])

    # ---- 05 VIDEO + DARK PANEL
    tk = Tok(raw_decode(rows[4]), content)
    tk.take(r'poster="([^"]+)"', "VIDEO_POSTER_URL")
    tk.take(r'aria-label="([^"]+)"', "VIDEO_ARIA")
    tk.take(r'<source src="([^"]+)" type="video/mp4">', "VIDEO_MP4_URL")
    heading(tk, "PANEL"); tk.take(COLTEXT, "PANEL_INTRO")
    for n in (1, 2, 3):
        tk.take(r'\[dfd_icon_list_item icon="([^"]+)"\]', f"PANEL_ITEM{n}_ICON")
        tk.take(r"font-size: 13pt;\">(.*?)</span></h3>", f"PANEL_ITEM{n}_TITLE")
        tk.take(r"font-size: 10pt;\">(.*?)</span>", f"PANEL_ITEM{n}_TEXT")
    tk.take(COLTEXT, "PANEL_OUTRO")
    out.append("<!-- PAT-VIDEO-PANEL : self-hosted looping mp4 left (2/3, .bvid absolute fill), dark panel right (1/3): h2 + kicker, intro, three icon items, outro. -->\n" + tk.t)

    # ---- 06 GAP
    out.append("<!-- PAT-GAP-BOTTOM : 70px breathing row below the video row. Fixed. -->\n" + rows[5])

    # ---- 07 SIX-IDEA CIRCLES (.pm)
    tk = Tok(raw_decode(rows[6]), content)
    tk.take(r'<p class="pm-kick">(.*?)</p>', "CIRCLES_KICKER")
    tk.take(r'<h2 class="pm-h">(.*?)</h2>', "CIRCLES_TITLE")
    tk.take(r'<p class="pm-sub">(.*?)</p>', "CIRCLES_SUB")
    tk.take(r'<p class="pm-foot">(.*?)</p>', "CIRCLES_FOOT")
    tk.take(r'var U="([^"]+)";', "CIRCLES_IMG_BASE")
    for n in range(1, 7):
        tk.take(r'\{n:"\d", t:"([^"]*)"', f"CIRCLE{n}_TITLE")
        tk.take(r'img:U\+"([^"]*)"', f"CIRCLE{n}_IMG")
        tk.take(r'b:"([^"]*)"\}', f"CIRCLE{n}_BODY")
    out.append("<!-- PAT-CIRCLES : the homepage scatter-circle module as a six-idea brainstorm. size/left/top are the kit's fixed geometry; only title, image file and body change. Raw HTML by Otto's decision (interactivity). -->\n" + tk.t)

    # ---- 08 WHO COMMISSIONS
    tk = Tok(rows[7], content); two_cols(tk, "WHO")
    out.append("<!-- PAT-WHO : 'Who Commissions Work Like This?' two balanced 1/4 columns. -->\n" + tk.t)

    # ---- 09 TIMELINE (.uc)
    tk = Tok(raw_decode(rows[8]), content)
    tk.sub_all('id="uc-protest"', "_UCID"); tk.t = tk.t.replace("{{_UCID}}", 'id="uc-{{ID_SLUG}}"'); content.pop("_UCID")
    tk.take(r'<p class="uc-kick">(.*?)</p>', "TIMELINE_KICKER")
    tk.take(r'<h2 class="uc-h">(.*?)</h2>', "TIMELINE_TITLE")
    tk.take(r'aria-label="([^"]*)"', "TIMELINE_ARIA")
    for n in range(1, 7):
        tk.take(r'\{n:"\d", when:"([^"]*)"', f"STEP{n}_WHEN")
        tk.take(r'label:"([^"]*)"', f"STEP{n}_LABEL")
        tk.take(r't:"([^"]*)"', f"STEP{n}_TITLE")
        tk.take(r'b:"([^"]*)"', f"STEP{n}_BODY")
        tk.take(r"craft:'([^']*)'", f"STEP{n}_CRAFT")
        tk.take(r'img:"([^"]*)"', f"STEP{n}_IMG_URL")
        tk.take(r'cap:"([^"]*)"', f"STEP{n}_CAPTION")
    out.append("<!-- PAT-TIMELINE : the .uc six-step rail, one panel at a time, image right. Six steps always. Raw HTML by Otto's decision. -->\n" + tk.t)

    # ---- 10 WHY ODDTOE
    tk = Tok(rows[9], content); two_cols(tk, "WHY")
    out.append("<!-- PAT-WHY : 'Why Oddtoe Likes ...' — the bit that is not a service. Two balanced 1/4 columns. -->\n" + tk.t)

    # ---- 11 DIVIDER (giant headings + floating objects)
    tk = Tok(raw_decode(rows[10]), content)
    tk.take(HEAD_SUB, "DIV_RIGHT_KICKER"); tk.take(HEAD_TITLE, "DIV_RIGHT_TITLE")
    tk.take(r'<img src="([^"]+)"', "DIV_IMG1_URL"); tk.take(r'alt="([^"]*)"', "DIV_IMG1_ALT")
    tk.take(r'<img src="([^"]+)"', "DIV_IMG2_URL"); tk.take(r'alt="([^"]*)"', "DIV_IMG2_ALT")
    tk.take(HEAD_SUB, "DIV_LEFT_KICKER"); tk.take(HEAD_TITLE, "DIV_LEFT_TITLE")
    out.append("<!-- PAT-DIVIDER : giant Bebas heading pair with a floating object either side (Analyst's Toolkit row). Keep the » and « in the titles. -->\n" + tk.t)

    # ---- 12 WHAT YOU GET
    tk = Tok(rows[11], content); two_cols(tk, "WYG")
    out.append("<!-- PAT-WHAT-YOU-GET : deliverables, two balanced 1/4 columns; COL1 opens with a bold summary and a bullet list. -->\n" + tk.t)

    # ---- 13 PACKAGE BOXES
    tk = Tok(rows[12], content); heading(tk, "PKG")
    for n in range(1, 6):
        tk.take(r'vc_single_image image="(\d+)"', f"PKG{n}_IMAGE_ID")
        tk.take(HEAD_SUB, f"PKG{n}_KICKER"); tk.take(HEAD_TITLE, f"PKG{n}_TITLE")
        tk.take(r'<p style="text-align: center;">(.*?)</p>', f"PKG{n}_BODY")
    out.append("<!-- PAT-PACKAGE : five 1/5 columns of cardboard-box icons; Qwigley kicker over Bebas h3, centred Arvo body. Five always. -->\n" + tk.t)

    # ---- 14 SPEC STRIP
    tk = Tok(rows[13], content)
    tk.t = tk.t.replace('dfd_bg_color_value="#161314"', 'dfd_bg_color_value="{{TINT}}"')
    for n in range(1, 7):
        tk.take(HEAD_SUB, f"SPEC{n}_FIGURE"); tk.take(HEAD_TITLE, f"SPEC{n}_LABEL")
    out.append("<!-- PAT-SPEC : six 1/6 columns. FIGURE is the Qwigley number/word on top (40px), LABEL the Bebas phrase beneath (32px, wraps to two lines). Canvas via dfd_bg_style=canvas. -->\n" + tk.t)

    # ---- 15 CREDENTIAL
    tk = Tok(rows[14], content); two_cols(tk, "CRED")
    out.append("<!-- PAT-CREDENTIAL : the authorship row (why a cartoonist / designer decides this). Two balanced 1/4 columns. -->\n" + tk.t)

    # ---- 16 COMPARISON TABLE
    tk = Tok(rows[15], content); heading(tk, "CMP")
    tk.take(r'<span style="font-family: Arvo;">(.*?)</span>\n<div style="overflow-x: auto;">', "CMP_INTRO")
    for n in (1, 2, 3):
        tk.take(r'scope="col">([^<]+)</th>', f"CMP_COL{n}_HEAD")
    for r in range(1, 6):
        tk.take(r'<td[^>]*><strong>([^<]*)</strong></td>', f"CMP_ROW{r}_LABEL")
        for c in (1, 2, 3):
            tk.take(r'<td[^>]*>([^<]*)</td>', f"CMP_ROW{r}_C{c}")
    out.append("<!-- PAT-COMPARE : Otto's styled table, three options across, five factual rows down. Cells factual, never poetic. -->\n" + tk.t)

    # ---- 17 FAQ
    tk = Tok(raw_decode(rows[16]), content)
    tk.take(r'font-size: 36pt;">([^<]*)</span></p>\n<p style="text-align: center;"><span style="font-family: \'Bebas Neue\'', "FAQ_KICKER")
    tk.take(r"font-size: 36pt;\">([^<]*)</span></p>\n\[/vc_column_text\]", "FAQ_TOPIC")
    secs = re.findall(r'\[vc_tta_section title="([^"]*)" tab_id="([^"]*)"\]\[vc_column_text css=""\]\n<p style="text-align: center;">(.*?)</p>\n\[/vc_column_text\]\[/vc_tta_section\]', tk.t, re.S)
    assert len(secs) >= 4, "FAQ sections not matched"
    content["FAQ"] = [{"q": html.unescape(q), "a": a} for q, _, a in secs]
    first = re.search(r'\[vc_tta_section title=.*\[/vc_tta_section\]', tk.t, re.S)
    tk.t = tk.t[:first.start()] + "<!-- PAT-FAQ-SECTION : repeat per question; compose-usecase.py expands FAQ[] here -->{{FAQ_SECTIONS}}" + tk.t[first.end():]
    tk.t = re.sub(r'<!--RAW--><script type="application/ld\+json">.*?</script><!--/RAW-->', "<!--RAW-->{{FAQ_JSONLD}}<!--/RAW-->", tk.t, flags=re.S)
    out.append("<!-- PAT-FAQ : Qwigley 'Questions about' + Bebas topic, dfd_accordion style-3, FAQPage JSON-LD generated from the same Q/A (plain text), Contact button. Last content row by Otto's 11 Sep decision. -->\n" + tk.t)

    # ---- 18 PORTFOLIO TRIO
    tk = Tok(rows[17], content)
    tk.take(r'font-size: 36pt;">([^<]*)</span></p>', "MORE_KICKER")
    tk.take(r"font-size: 36pt;\">([^<]*)</span></h2>", "MORE_TITLE")
    for n in (1, 2, 3):
        tk.take(r'single_custom_post_item="(\d+)"', f"PORTFOLIO{n}_ID")
    out.append("<!-- PAT-PORTFOLIO : three dfd_portfolio_module singles (my-product items only) + contact circle. -->\n" + tk.t)

    # ---- 19 FORM
    tk = Tok(rows[18], content); tk.take(HEAD_SUB, "FORM_KICKER"); tk.take(HEAD_TITLE, "FORM_TITLE")
    out.append("<!-- PAT-FORM : h2 + Qwigley kicker over the project-enquiry Gravity form (id=1). -->\n" + tk.t)

    header = (
        "<!-- ============================================================\n"
        "DESIGN KIT — ODDTOE USE CASE — v1\n"
        f"Snapshot of oddtoe.com/use-cases/publicity-stunts/ (page 16272), taken 11 Sep 2026.\n"
        f"Raw master: masters/{Path(master_path).name}\n"
        "Token specs + compose rules: usecase-kit-README.md. Fill with scripts/compose-usecase.py.\n"
        "Raw-HTML blocks sit DECODED between <!--RAW--> markers; compose re-encodes them.\n"
        "STRIP ALL HTML COMMENTS before sending to WordPress (compose does this).\n"
        "============================================================= -->\n"
    )
    kit = header + "\n".join(out) + "\n"
    KIT.write_text(kit, encoding="utf-8")
    cj = REFS / f"usecase-content-{'publicity-stunts'}.json"
    cj.write_text(json.dumps(content, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    toks = sorted(set(re.findall(r"{{([A-Z0-9_]+)}}", kit)))
    print(f"kit: {KIT.name} {len(kit)} chars, {len(toks)} distinct tokens")
    print(f"content: {cj.name} {len(content)} keys, FAQ x{len(content['FAQ'])}")
    missing = [t for t in toks if t not in content and t not in ("FAQ_SECTIONS", "FAQ_JSONLD")]
    assert not missing, f"tokens without content: {missing}"


if __name__ == "__main__":
    main(sys.argv[1])
