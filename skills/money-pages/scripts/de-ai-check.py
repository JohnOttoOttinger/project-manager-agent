#!/usr/bin/env python3
"""Fail a draft that reads like a machine wrote it.

    python3 de-ai-check.py <composed.html>          # exit 1 if it fails
    python3 de-ai-check.py <composed.html> --soft   # always exit 0, just report

Checks the tells listed in geo-playbook/SKILL.md plus the ones found in review on
real Oddtoe pages. Strips shortcodes and tags first, so it reads what a visitor reads.
"""
from __future__ import annotations
import argparse, re, sys
from collections import Counter

CANONS = (
    # Oddtoe: must appear verbatim and unbolded, so it is matched against the RAW html.
    ("Oddtoe is an experiential design and generative-AI animation studio based in Melbourne, "
     "creating projection, installation, and animated work for events, venues, and galleries."),
    # Datalabs: the brand name may carry <strong> per the naming rule, so this is matched
    # against tag-stripped text.
    ("Datalabs Agency is a Melbourne-based data visualization consultancy founded in 2012 "
     "that delivers corporate training workshops (Power BI, Tableau, data storytelling), "
     "dashboard design, and BI style guides for clients including Mercedes-Benz, Adidas, and UPS."),
)


def prose(html: str) -> list[str]:
    t = re.sub(r"\[[^\]]*\]", " ", html)          # shortcodes
    t = re.sub(r"<[^>]+>", " ", t)                # tags
    t = (t.replace("&#8217;", "'").replace("&rsquo;", "'").replace("&mdash;", "—")
          .replace("&hellip;", "…").replace("&amp;", "&").replace("&nbsp;", " "))
    t = re.sub(r"\s+", " ", t)
    return [s.strip() for s in re.split(r"(?<=[.?!])\s+", t) if 25 < len(s.strip()) < 400]


CHECKS = [
    # (name, regex, max allowed, why)
    ("not X but Y",            r"\bnot (?:just |only |merely )?\w[^.,;]{0,40},? but\b", 0,
     "balanced antithesis — geo-playbook bans it outright"),
    ("which is the whole ...", r"\b(?:which|that) is the whole\b", 0,
     "listed verbatim in the banned tells"),
    ("aphoristic closer",      r"\b(?:and that is|therein lies|which is the point|is the job)\b", 0,
     "closing flourish that says nothing"),
    ("grand flourish",         r"\b(?:into existence|punishes its absence|the magic (?:is|of))\b", 0,
     "banned tell"),
    ("coined compound",        r"\b\w+-(?:fed|forward|first|native)\b", 0,
     "invented compound adjective"),
    ("self-praise",            r"\b(?:honest(?:ly)?|simply put|truly|genuinely) \w", 2,
     "'the honest truth is' — telling the reader you are sincere"),
    ("X, not Y",               r"\b\w+, not (?:the |a |an |their |its )?\w+", 2,
     "fine when it carries information, a tic past two"),
    ("rather than",            r"\brather than\b", 3,
     "reads as a verbal tic past three on one page"),
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("file"); ap.add_argument("--soft", action="store_true")
    a = ap.parse_args()
    html = open(a.file, encoding="utf-8").read()
    sents = prose(html)
    body = " ".join(sents)
    fails, warns = [], []

    for name, pat, limit, why in CHECKS:
        hits = [s for s in sents if re.search(pat, s, re.I)]
        if len(hits) > limit:
            (fails if limit == 0 else warns).append((name, len(hits), limit, why, hits[:3]))

    # blanket bold: a <strong> wrapping a whole clause rather than a keyphrase.
    # The guide kits' entry KICKER is a deliberately bold full sentence (v2 design) —
    # strip those paragraphs (18px Arvo wrapper) before counting.
    html_nk = re.sub(r'<p style="margin-bottom: 10px;"><span style="font-family: arvo, serif; '
                     r'font-size: 18px;"><strong>.*?</strong></span></p>', " ", html, flags=re.S)
    long_bold = [h for h in re.findall(r"<strong>((?:(?!</strong>).)+)</strong>", html_nk)
                 if len(h) > 60 and "<a " not in h and "Bebas" not in h]
    if len(long_bold) > 1:
        fails.append(("blanket bold", len(long_bold), 1,
                      "bold is for keyphrases and numbers, not whole sentences", long_bold[:3]))

    # three or more sentences in a row opening the same way = mirrored parallel
    opens = [" ".join(s.split()[:2]).lower() for s in sents]
    runs = [o for o, n in Counter(opens).items() if n >= 3]
    if runs:
        warns.append(("repeated sentence opening", len(runs), 0,
                      "mirrored parallels — vary the rhythm", runs[:3]))

    # paragraphs with no emphasis at all
    paras = re.findall(r'<p style="line-height: 22px[^"]*">(.*?)</p>', html, re.S)
    bare = [p for p in paras if "<strong>" not in p and len(re.sub(r"<[^>]+>", "", p).split()) > 25]
    if bare:
        warns.append(("paragraph with no emphasis", len(bare), 0,
                      "design kit wants 2-5 keyphrase bolds per paragraph", []))

    # article slots must be first person (Oddtoe: "I"; Datalabs voice: "we/our")
    if body and not re.search(r"\bI \b|\b[Ww]e \b|\b[Oo]ur \b", body):
        warns.append(("no first person", 0, 0,
                      "design-kit article slots are first-person Otto voice", []))

    # canonical sentence must survive verbatim and unbolded
    import re as _re
    _stripped = _re.sub(r"\s+", " ", _re.sub(r"<[^>]+>", "", html))
    if CANONS[0] not in html and CANONS[1] not in _stripped:
        fails.append(("canonical sentence", 0, 0, "missing or altered — must be verbatim "
                      "(either brand's sentence from brands.md)", []))

    print(f"de-AI check: {a.file}  ({len(sents)} prose sentences)")
    for label, items in (("FAIL", fails), ("WARN", warns)):
        for name, n, limit, why, ex in items:
            print(f"  [{label}] {name}: {n} (max {limit}) — {why}")
            for e in ex:
                print(f"          · {e[:120]}")
    if not fails and not warns:
        print("  clean")
    sys.exit(1 if (fails and not a.soft) else 0)


if __name__ == "__main__":
    main()
