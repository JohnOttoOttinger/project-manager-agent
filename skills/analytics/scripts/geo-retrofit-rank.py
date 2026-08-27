#!/usr/bin/env python3
"""Which EXISTING pages should get the GEO retrofit first, ranked by business result?

Otto, 26 Aug 2026: the 4pm new-build emails ranked on search demand, which is a proxy he does
not care about. "I'd like a list of pages ranked by where the GEO/SEO uplift can bring greater
business results. Where I can gain traffic, customers, workshop clients, and new business."

    score = sqrt(impressions) x geo_gap x commercial_proximity x position_band

- geo_gap        only the elements Otto put IN SCOPE (Q&A + FAQ schema, canonical sentence,
                 question-shaped H2s, meta description). Comparison tables are OUT — they are a
                 design change and the designs stay as they are.
- commercial     how few steps from this page to someone booking something, weighted to the two
                 lines Otto named: Datalabs workshop bookings, Oddtoe activations & fabrication.
- position_band  pages at 10-20 have the most room to move; pages already top-3 gain citation,
                 not rank; pages past 40 rarely move on structure alone.

    python3 geo-retrofit-rank.py --brand datalabs --audit 60 --limit 25
    python3 geo-retrofit-rank.py --brand oddtoe --json

Read-only: fetches public HTML and Search Console, writes nothing.
"""
from __future__ import annotations
import argparse, json, re, sys, urllib.parse, urllib.request, datetime
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ga_client

SITES = {"oddtoe": "https://www.oddtoe.com/", "datalabs": "https://www.datalabsagency.com/"}
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
CANON = {
 "oddtoe": "experiential design and generative-ai animation studio based in melbourne",
 "datalabs": "melbourne-based data visualization consultancy founded in 2012",
}

# Commercial proximity. First match wins, so order matters.
# Tier A = Otto's named priority line; B = other direct service; C = feeds a service;
# D = proof/portfolio; E = admin. Heuristics on the slug — override by hand where wrong.
TIERS = {
 "datalabs": [
   (1.00, "A · workshop / training service",  r"workshop|training|course|masterclass|pricing|bootcamp"),
   (0.75, "B · other service",                r"dashboard-design|style-guide|consult|annual-report|services|design-service|infographic|data-visualisation-agency|data-visualization-agency"),
   (0.55, "C · feeds a service",              r"how-to|guide|types-of|vs-|-vs-|best-|what-is|tutorial|examples|power-bi|tableau|excel|chart|cost|tips"),
   (0.30, "D · proof / portfolio",            r"case-stud|portfolio|our-work|clients|testimonial"),
   (0.10, "E · admin",                        r"about|contact|team|career|privacy|terms|author|category|tag|thank-you|blog/?$"),
 ],
 "oddtoe": [
   (1.00, "A · activation / fabrication",     r"activation|prop|fabricat|inflatable|installation|experiential|sculpture|topiary|puppet|set-design|scenic"),
   (0.75, "B · other service",                r"animation|animator|character|designer|artist|studio|illustrat|speaker|director"),
   (0.55, "C · feeds a service",              r"ideas|what-is|how-|guide|cost|best-|-vs-|vs-|conference|festival|examples"),
   (0.30, "D · proof / portfolio",            r"portfolio|case-stud|original-stories|project|blog/|/20\d\d/"),
   (0.10, "E · admin",                        r"about|contact|team|career|privacy|terms|author|category|tag|thank-you"),
 ],
}
DEFAULT_TIER = (0.40, "· unclassified")

# Checked BEFORE the tier table: clear admin slugs, so a commercial keyword in the slug
# (e.g. /about-us-data-visualization-agency/) cannot promote a page that sells nothing.
ADMIN = r"^/(contact|privacy|terms|careers?|thank-you|author/|category/|tag/|wp-|feed)"
# Otto's homepages both target a commercial head term, so they are a service page, not admin.
HOMEPAGE = (0.75, "B · homepage")
# A dated post is proof/portfolio unless its slug carries a service topic, in which case it feeds one.
DATED = re.compile(r"^/\d{4}/\d{2}/\d{2}/")


def commercial(path: str, brand: str):
    if path in ("/", ""):
        return HOMEPAGE
    if re.search(ADMIN, path, re.I):
        return 0.10, "E · admin"
    for weight, label, pat in TIERS[brand]:
        if re.search(pat, path, re.I):
            # a dated post never counts as a service page, only as something that feeds one
            if DATED.match(path) and weight > 0.55:
                return 0.55, "C · post that feeds a service"
            return weight, label
    if DATED.match(path):
        return 0.30, "D · post, off-topic"
    return DEFAULT_TIER


def position_band(pos: float) -> tuple[float, str]:
    if pos <= 3:   return 0.60, "top-3 — citation upside only"
    if pos <= 10:  return 1.00, "page 1 — consolidate"
    if pos <= 20:  return 1.15, "page 2 — best room to move"
    if pos <= 40:  return 0.80, "page 3-4"
    return 0.45, "deep — structure alone rarely moves it"


def gsc_pages(site: str, days: int, country: str | None = None) -> dict:
    end = datetime.date.today() - datetime.timedelta(days=3)
    start = end - datetime.timedelta(days=days)
    body = {"startDate": str(start), "endDate": str(end), "dimensions": ["page"], "rowLimit": 25000}
    if country:
        body["dimensionFilterGroups"] = [{"filters": [
            {"dimension": "country", "operator": "equals", "expression": country}]}]
    req = urllib.request.Request(
        f"https://www.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(site, safe='')}/searchAnalytics/query",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {ga_client.get_token()}", "Content-Type": "application/json"})
    return {r["keys"][0]: {"impressions": r["impressions"], "clicks": r["clicks"],
                           "position": round(r["position"], 1)}
            for r in json.load(urllib.request.urlopen(req)).get("rows", [])}


def audit(html: str, brand: str) -> dict:
    stripped = re.sub(r"<(script|style|noscript)\b.*?</\1>", " ", html, flags=re.S | re.I)
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", stripped))
    heads = [re.sub(r"<[^>]+>", "", h).strip()
             for h in re.findall(r"<h[23][^>]*>(.*?)</h[23]>", html, re.S | re.I)]
    md = re.search(r'<meta name="description" content="([^"]*)"', html)
    return {"canonical_sentence": CANON[brand] in text.lower(),
            "qa_block": "FAQPage" in html,
            "question_headings": sum(1 for h in heads if h.rstrip().endswith("?")),
            "meta_description": bool(md and len(md.group(1)) > 60),
            "words": len(text.split())}


IN_SCOPE = [("qa_block", "Q&A + FAQ schema"), ("canonical_sentence", "canonical sentence"),
            ("question_headings", "question H2s"), ("meta_description", "meta description")]


def fetch(url):
    try:
        return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read().decode("utf-8", "ignore")
    except Exception as e:
        return f"__ERROR__{e}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--brand", choices=sorted(SITES), default="datalabs")
    ap.add_argument("--days", type=int, default=180)
    ap.add_argument("--audit", type=int, default=60, help="how many pages to fetch and audit")
    ap.add_argument("--limit", type=int, default=25, help="how many to report")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--exclude", default=r"^/(de|ar|es|fr|zh|ja|ru)/",
                    help="path regex to drop before ranking (default: translated pages)")
    ap.add_argument("--tier", default="", help="only report tiers whose label starts with this, e.g. A")
    ap.add_argument("--country", default="aus",
                    help="ISO-3 country filter (default aus). Measured 27 Aug 2026: filtering the "
                         "Oddtoe prop page to Australia dropped machine-shaped impressions from 78%% "
                         "to 5%%, because the query enumeration is almost entirely offshore. Pass an "
                         "empty string for worldwide, and expect the noise back.")
    a = ap.parse_args()
    site = SITES[a.brand]

    pages = gsc_pages(site, a.days, a.country or None)
    if a.exclude:
        drop = re.compile(a.exclude, re.I)
        before = len(pages)
        pages = {u: m for u, m in pages.items()
                 if not drop.match(u.replace(site.rstrip("/"), "") or "/")}
        print(f"(excluded {before - len(pages)} pages matching {a.exclude})", file=sys.stderr)
    top = sorted(pages.items(), key=lambda kv: -kv[1]["impressions"])[: a.audit]
    with ThreadPoolExecutor(max_workers=8) as ex:
        htmls = list(ex.map(fetch, [u for u, _ in top]))

    rows = []
    for (url, m), html in zip(top, htmls):
        path = url.replace(site.rstrip("/"), "") or "/"
        if html.startswith("__ERROR__"):
            rows.append({"path": path, **m, "error": html[9:69]}); continue
        au = audit(html, a.brand)
        have = sum([au["qa_block"], au["canonical_sentence"],
                    au["question_headings"] >= 2, au["meta_description"]])
        gap = (4 - have) / 4
        cw, clabel = commercial(path, a.brand)
        pw, plabel = position_band(m["position"])
        missing = [label for key, label in IN_SCOPE
                   if not (au[key] >= 2 if key == "question_headings" else au[key])]
        rows.append({"path": path, **m,
                     "ctr": round(m["clicks"] / m["impressions"], 4) if m["impressions"] else 0,
                     "geo_have": have, "missing": missing, "words": au["words"],
                     "tier": clabel, "band": plabel,
                     "score": round((m["impressions"] ** 0.5) * gap * cw * pw, 1)})

    rows.sort(key=lambda r: -r.get("score", 0))
    if a.tier:
        rows = [r for r in rows if r.get("tier", "").startswith(a.tier)]
    rows = rows[: a.limit]
    if a.json:
        print(json.dumps({"brand": a.brand, "audited": len(top), "pages": rows}, indent=1)); return

    print(f"\nGEO RETROFIT PRIORITY — {a.brand}, {a.days}d, audited {len(top)} pages, top {len(rows)}")
    print("=" * 118)
    print(f"{'score':>6} {'impr':>7} {'clk':>5} {'pos':>5} {'GEO':>4} {'words':>6}  {'tier':<32} page")
    for r in rows:
        if "error" in r:
            print(f"{'--':>6} {r['impressions']:>7} {'':>5} {'':>5} {'??':>4} {'':>6}  {'':<32} {r['path'][:40]} ({r['error'][:34]})")
            continue
        print(f"{r['score']:>6} {r['impressions']:>7} {r['clicks']:>5} {r['position']:>5} "
              f"{r['geo_have']}/4 {r['words']:>6}  {r['tier']:<32} {r['path'][:40]}")
        print(f"{'':>32}missing: {', '.join(r['missing']) or 'nothing in scope'}   ({r['band']})")
    print("\nscore = sqrt(impressions) x geo_gap x commercial_proximity x position_band")
    print("in scope: Q&A + FAQ schema · canonical sentence · question H2s · meta description")
    print("tables are OUT of scope — designs stay as they are.\n")


if __name__ == "__main__":
    main()
