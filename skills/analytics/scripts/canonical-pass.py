#!/usr/bin/env python3
"""Insert each brand's canonical sentence into pages that lack it.

The sentence must survive VERBATIM and unbolded (de-ai-check enforces this), so the only
judgment is WHERE it lands. It needs a real prose paragraph — dropped into a caption, a
button label or a table cell it reads as debris.

    python3 canonical-pass.py --brand oddtoe            # dry run, prints the host paragraph
    python3 canonical-pass.py --brand oddtoe --push     # writes, backing up each page first
"""
from __future__ import annotations
import argparse, json, os, re, sys, urllib.request, base64, pathlib

REPO = pathlib.Path(__file__).resolve().parents[3]
BRANDS = {
 "oddtoe": ("https://www.oddtoe.com", "WP_ODDTOE_USER", "WP_ODDTOE_APP_PASSWORD",
   "Oddtoe is an experiential design and generative-AI animation studio based in Melbourne, "
   "creating projection, installation, and animated work for events, venues, and galleries."),
 "datalabs": ("https://www.datalabsagency.com", "WP_DATALABS_USER", "WP_DATALABS_APP_PASSWORD",
   "The <strong>Datalabs Agency</strong> is a Melbourne-based data visualization consultancy "
   "founded in 2012 that delivers corporate training workshops (Power BI, Tableau, data "
   "storytelling), dashboard design, and BI style guides for clients including Mercedes-Benz, "
   "Adidas, and UPS."),
}
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

# A host paragraph must be prose the reader actually reads.
# NOTE: do NOT disqualify on font-family — Ronneby wraps ordinary body copy in styled
# <span>s, so testing the inner HTML for it rejects almost every real paragraph. Test the
# TEXT for junk markers, and the markup only for display faces used as headings.
JUNK = re.compile(r'indicates required|&copy;|^\W*$|^\s*\[', re.I)
DISPLAY = re.compile(r'Bebas|Qwigley|text-transform\s*:\s*uppercase', re.I)


def host_paragraph(content: str) -> tuple[int, int, str] | None:
    """Return (start, end, text) of the best paragraph to append the sentence to."""
    best = None
    for m in re.finditer(r'<p(?![^>]*class="p2")[^>]*>(.*?)</p>', content, re.S):
        inner = m.group(1)
        text = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', inner)).strip()
        if not (140 <= len(text) <= 900) or JUNK.search(text) or DISPLAY.search(inner):
            continue
        if text.endswith(':') or text.isupper():
            continue
        if not text.endswith(('.', '!', '?')):      # must be a finished sentence
            continue
        # prefer the earliest qualifying paragraph — highest on the page is best for citation
        best = (m.start(1), m.end(1), text)
        break
    return best


def fetch(site, user, pw, page_id):
    req = urllib.request.Request(f"{site}/wp-json/wp/v2/pages/{page_id}?context=edit",
        headers={"Authorization": "Basic " + base64.b64encode(f"{user}:{pw}".encode()).decode(),
                 "User-Agent": UA})
    return json.load(urllib.request.urlopen(req))


def push(site, user, pw, page_id, content):
    req = urllib.request.Request(f"{site}/wp-json/wp/v2/pages/{page_id}",
        data=json.dumps({"content": content}).encode(), method="POST",
        headers={"Authorization": "Basic " + base64.b64encode(f"{user}:{pw}".encode()).decode(),
                 "Content-Type": "application/json", "User-Agent": UA})
    return json.load(urllib.request.urlopen(req))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--brand", choices=sorted(BRANDS), required=True)
    ap.add_argument("--queue", default=str(REPO / "skills/analytics/references/geo-retrofit-phase1-2026-08-27.json"))
    ap.add_argument("--push", action="store_true")
    ap.add_argument("--limit", type=int, default=99)
    a = ap.parse_args()
    site, ukey, pkey, CANON = BRANDS[a.brand]
    user, pw = os.environ[ukey], os.environ[pkey]
    plain = re.sub(r"<[^>]+>", "", CANON)

    queue = [r for r in json.load(open(a.queue))
             if r["brand"] == a.brand and not r.get("done")
             and "canonical sentence" in r.get("missing", [])][: a.limit]
    backups = REPO / "skills/money-pages/references/site-backups"
    ok = skipped = failed = 0
    for r in queue:
        try:
            slug = [s for s in r["path"].strip("/").split("/") if s][-1] if r["path"].strip("/") else ""
            listing = urllib.request.urlopen(urllib.request.Request(
                f"{site}/wp-json/wp/v2/pages?slug={slug}&context=edit&per_page=3" if slug else
                f"{site}/wp-json/wp/v2/pages?per_page=100&context=edit",
                headers={"Authorization": "Basic " + base64.b64encode(f"{user}:{pw}".encode()).decode(),
                         "User-Agent": UA}))
            found = json.load(listing)
            match = next((p for p in found if p.get("link", "").endswith(r["path"])), None)
            if not match and len(found) == 1:
                match = found[0]          # unique slug hit, path differs only by parent
            if not match:
                print(f"  SKIP  no page match      {r['name'][:46]}"); skipped += 1; continue
            content = match["content"]["raw"]
            if plain in re.sub(r"<[^>]+>", "", content):
                print(f"  SKIP  already present    {r['name'][:46]}"); skipped += 1; continue
            spot = host_paragraph(content)
            if not spot:
                print(f"  SKIP  no prose paragraph {r['name'][:46]}"); skipped += 1; continue
            s, e, text = spot
            new = content[:e] + " " + CANON + content[e:]
            if a.push:
                (backups / f"{a.brand}-{match['id']}-pre-canonical-2026-08-27.json").write_text(json.dumps(match))
                res = push(site, user, pw, match["id"], new)
                good = plain in re.sub(r"<[^>]+>", "", res["content"]["raw"])
                print(f"  {'OK   ' if good else 'FAIL '} {match['id']:>6}  {r['name'][:44]}")
                ok += good; failed += (not good)
            else:
                print(f"  would append after: …{text[-90:]}")
                print(f"        {match['id']:>6}  {r['name'][:44]}\n")
                ok += 1
        except Exception as ex:
            print(f"  ERROR {str(ex)[:60]}  {r['name'][:40]}"); failed += 1
    print(f"\n{a.brand}: {ok} {'pushed' if a.push else 'ready'}, {skipped} skipped, {failed} failed")


if __name__ == "__main__":
    main()
