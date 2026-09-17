# Shared helpers, generated from compose-usecase.py. Do not edit; edit compose-usecase.py and regenerate.
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


