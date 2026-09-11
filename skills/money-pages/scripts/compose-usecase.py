#!/usr/bin/env python3
"""Compose a Use Case page from the Use Case kit and a content JSON.

    python3 compose-usecase.py references/usecase-content-museum-late-opening.json
    python3 compose-usecase.py references/usecase-content-publicity-stunts.json --verify references/masters/oddtoe-publicity-stunts-16272-2026-09-11-raw.txt

Reads  references/design-kit-oddtoe-usecase.html and the JSON, fills every {{TOKEN}}, expands the
FAQ, generates the FAQPage JSON-LD from the same questions, re-encodes the raw-HTML blocks the way
WPBakery expects (rawurlencode then base64), strips HTML comments, and writes
references/composed/usecase-<slug>-<date>.html. Draft only: sending it to WordPress is the
money-pages workflow's job, never this script's.

--verify decodes the raw blocks on both sides and diffs the result row by row against a master
snapshot, which is how the kit is proven to reproduce the live page.
"""
from __future__ import annotations
import base64, datetime, html, json, re, sys, urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFS = HERE.parent / "references"
KIT = REFS / "design-kit-oddtoe-usecase.html"
SAFE = "!*'()"   # matches encodeURIComponent; the convention every Oddtoe compose script uses


def enc(s: str) -> str:
    return base64.b64encode(urllib.parse.quote(s, safe=SAFE).encode()).decode()


def dec(b64: str) -> str:
    return urllib.parse.unquote(base64.b64decode(b64).decode())


def plain(s: str) -> str:
    """Visible answer -> schema text: strip tags, unescape entities, collapse whitespace."""
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def faq_sections(faq: list, stamp: str, slug: str) -> str:
    out = []
    for i, qa in enumerate(faq, 1):
        out.append(f'[vc_tta_section title="{html.escape(qa["q"], quote=True)}" tab_id="{stamp}{i:03d}-usecase-{slug}-faq-{i}"]'
                   f'[vc_column_text css=""]\n<p style="text-align: center;">{qa["a"]}</p>\n[/vc_column_text][/vc_tta_section]')
    return "".join(out)


def faq_jsonld(faq: list) -> str:
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": plain(qa["q"]),
         "acceptedAnswer": {"@type": "Answer", "text": plain(qa["a"])}} for qa in faq]}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "</script>"


def compose(content: dict) -> str:
    kit = KIT.read_text(encoding="utf-8")
    c = dict(content)
    c["FAQ_SECTIONS"] = faq_sections(c["FAQ"], c["FAQ_TAB_STAMP"], c["ID_SLUG"])
    c["FAQ_JSONLD"] = faq_jsonld(c["FAQ"])
    body = re.sub(r"{{([A-Z0-9_]+)}}", lambda m: str(c[m.group(1)]), kit)
    body = re.sub(r"<!--(?!RAW-->|/RAW-->).*?-->\n?", "", body, flags=re.S)          # kit comments
    body = re.sub(r"<!--RAW-->(.*?)<!--/RAW-->", lambda m: enc(m.group(1)), body, flags=re.S)
    assert "{{" not in body, "unfilled token: " + re.search(r"{{[^}]+}}", body).group(0)
    assert "<!--" not in body, "an HTML comment survived"
    return body.strip()


def verify(body: str, master_path: str) -> bool:
    master = Path(master_path).read_text(encoding="utf-8").strip()
    norm = lambda s: re.sub(r"\[vc_raw_html\]([A-Za-z0-9+/=]+)\[/vc_raw_html\]",
                            lambda m: "[vc_raw_html]" + dec(m.group(1)) + "[/vc_raw_html]", s)
    a, b = re.findall(r"\[vc_row\b.*?\[/vc_row\]", norm(body), re.S), re.findall(r"\[vc_row\b.*?\[/vc_row\]", norm(master), re.S)
    ok = True
    for i, (x, y) in enumerate(zip(a, b), 1):
        if x != y:
            ok = False
            j = next(k for k in range(min(len(x), len(y))) if x[k] != y[k]) if x[:min(len(x), len(y))] != y[:min(len(x), len(y))] else min(len(x), len(y))
            print(f"row {i:02d} DIFFERS at char {j}:\n  composed: {x[max(0,j-60):j+80]!r}\n  master:   {y[max(0,j-60):j+80]!r}")
    if len(a) != len(b):
        ok = False; print(f"row count differs: composed {len(a)} vs master {len(b)}")
    print("VERIFY:", "identical (decoded) in all rows" if ok else "DIFFERENCES FOUND")
    return ok


def main():
    args = sys.argv[1:]
    content = json.loads(Path(args[0]).read_text(encoding="utf-8"))
    body = compose(content)
    slug = content.get("URL_SLUG", Path(args[0]).stem.replace("usecase-content-", ""))
    out = REFS / "composed" / f"usecase-{slug}-{datetime.date.today().isoformat()}.html"
    out.write_text(body, encoding="utf-8")
    print(f"composed: {out.relative_to(REFS.parent)}  {len(body)} chars, {body.count('[vc_row ')} rows, "
          f"{body.count('[vc_raw_html]')} raw blocks, FAQ x{len(content['FAQ'])}")
    print("PAGE SETTINGS (wp-admin): template page-custom.php · parent 16296 /use-cases/ · "
          f"Custom bg {content['TINT']} · header style 13")
    for k in ("YOAST_TITLE", "YOAST_DESC"):
        if k in content: print(f"{k}: {content[k]}")
    if "--verify" in args:
        sys.exit(0 if verify(body, args[args.index("--verify") + 1]) else 1)


if __name__ == "__main__":
    main()
