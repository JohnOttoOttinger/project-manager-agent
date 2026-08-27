#!/usr/bin/env python3
"""Build a kit-native Q&A row (accordion + FAQPage JSON-LD) for a page that has none.

Used by the GEO retrofit. The two halves MUST agree: an accordion whose schema lists
different questions is worse than no schema at all, so build() derives the JSON-LD from
the same list that fills the accordion and asserts the base64 round trip before returning.

The kit ships FIVE vc_tta_section slots; for a different count, replace the joined run of
sections rather than appending after the last one.
"""
from __future__ import annotations
import base64, json, pathlib, re, urllib.parse

REPO = pathlib.Path(__file__).resolve().parents[3]
KITS = {"datalabs": REPO / "skills/money-pages/references/design-kit.html",
        "oddtoe":   REPO / "skills/money-pages/references/design-kit-oddtoe.html"}


def plain(s: str) -> str:
    """Answer text as a machine reads it — tags out, entities resolved."""
    t = re.sub(r"<[^>]+>", "", s)
    for a, b in (("&amp;", "&"), ("&mdash;", "—"), ("&rsquo;", "’"), ("&nbsp;", " ")):
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t).strip()


def build(brand: str, topic: str, qa: list[tuple[str, str]], slug: str) -> str:
    kit = KITS[brand].read_text()
    i = kit.index("<!-- PATTERN: faq")
    blk = kit[i:kit.index("<!-- PATTERN:", i + 10)]
    blk = blk[blk.index("[vc_row"):]
    blk = blk[: blk.rindex("[/vc_row]") + len("[/vc_row]")]
    blk = blk.replace("{{FAQ_TOPIC}}", topic)

    secs = re.findall(r"\[vc_tta_section.*?\[/vc_tta_section\]", blk, re.S)
    tpl, filled = secs[0], []
    for n, (q, a) in enumerate(qa, 1):
        s = re.sub(r'title="[^"]*"', f'title="{q}"', tpl)
        s = re.sub(r'tab_id="[^"]*"', f'tab_id="faq-{slug}-{n}-2026"', s)
        s = re.sub(r'<p style="text-align: center;">.*?</p>',
                   f'<p style="text-align: center;">{a}</p>', s, flags=re.S)
        filled.append(s)
    blk = blk.replace("".join(secs), "".join(filled))

    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q,
                          "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in qa]}
    payload = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    enc = base64.b64encode(urllib.parse.quote(payload, safe="").encode()).decode()
    if "[vc_raw_html]" in blk:
        blk = re.sub(r"\[vc_raw_html\].*?\[/vc_raw_html\]",
                     f"[vc_raw_html]{enc}[/vc_raw_html]", blk, flags=re.S)
    else:
        blk = blk.replace("[/vc_row]", f"[vc_raw_html]{enc}[/vc_raw_html][/vc_row]", 1)

    # the round trip is the whole point — fail loudly here, never on the live page
    back = re.search(r"\[vc_raw_html\](.*?)\[/vc_raw_html\]", blk, re.S).group(1)
    dec = json.loads(re.search(r"<script[^>]*>(.*?)</script>", urllib.parse.unquote(
        base64.b64decode(back).decode()), re.S).group(1))
    assert len(dec["mainEntity"]) == len(qa), "schema/accordion mismatch"
    assert blk.count("[vc_tta_section") == len(qa), "section count mismatch"
    return blk


def insert_before_last_row(content: str, block: str) -> str:
    """Drop the Q&A row above the page's final row (the contact form on both kits)."""
    return content[: content.rindex("[vc_row")] + block + content[content.rindex("[vc_row"):]
