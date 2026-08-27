#!/usr/bin/env python3
"""Q&A block for CLASSIC-editor posts (plain HTML, no WPBakery row structure).

The page kits emit [vc_row]…[dfd_accordion] shortcodes, which assume a builder template.
Datalabs and Oddtoe blog posts are plain h2/h3/p HTML, so they get a plain section instead:
question <h3>s (which also satisfies the "2+ question headings" GEO check) and the FAQPage
JSON-LD carried in a [vc_raw_html] shortcode.

Why [vc_raw_html] and not a bare <script>: WordPress runs wp_kses on post content for any
user without unfiltered_html and strips <script> outright. vc_raw_html stores the markup
base64-encoded inside a shortcode, so it survives the filter and WPBakery renders it back.
"""
from __future__ import annotations
import base64, json, re, urllib.parse


def plain(s: str) -> str:
    t = re.sub(r"<[^>]+>", "", s)
    for a, b in (("&amp;", "&"), ("&mdash;", "—"), ("&rsquo;", "’"), ("&nbsp;", " ")):
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t).strip()


def build(heading: str, qa: list[tuple[str, str]]) -> str:
    html = [f"\n<h2>{heading}</h2>"]
    for q, a in qa:
        html.append(f"<h3>{q}</h3>")
        html.append(f"<p>{a}</p>")
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q,
                          "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in qa]}
    payload = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
    enc = base64.b64encode(urllib.parse.quote(payload, safe="").encode()).decode()
    html.append(f"[vc_raw_html]{enc}[/vc_raw_html]")
    out = "\n".join(html)

    back = re.search(r"\[vc_raw_html\](.*?)\[/vc_raw_html\]", out, re.S).group(1)
    dec = json.loads(re.search(r"<script[^>]*>(.*?)</script>", urllib.parse.unquote(
        base64.b64decode(back).decode()), re.S).group(1))
    assert len(dec["mainEntity"]) == len(qa)
    assert out.count("<h3>") == len(qa)
    return out
