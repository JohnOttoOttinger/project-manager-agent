#!/usr/bin/env python3
"""Which live pages carry demand but NOT the GEO treatment?

Otto, 24 Aug 2026: "I have a lot of pages that have not had the GEO treatment, yet."
This ranks existing pages by (traffic they already earn) x (how little GEO structure they have),
so the cheapest wins come first. It never proposes a new page — that is next-best-page.py's job.

    python3 geo-coverage.py --brand datalabs
    python3 geo-coverage.py --brand oddtoe --limit 30 --json

Scored against the six geo-playbook rules that leave a machine-detectable trace.
Read-only: it fetches public HTML and Search Console, and writes nothing.
"""
from __future__ import annotations
import argparse, json, re, sys, urllib.parse, urllib.request, datetime
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ga_client

SITES = {"oddtoe": "https://www.oddtoe.com/", "datalabs": "https://www.datalabsagency.com/"}
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
CANON = {
 "oddtoe": "experiential design and generative-AI animation studio based in Melbourne",
 "datalabs": "Melbourne-based data visualization consultancy founded in 2012",
}

def gsc_pages(site: str, days: int) -> dict:
    end = datetime.date.today() - datetime.timedelta(days=3)
    start = end - datetime.timedelta(days=days)
    tok = ga_client.get_token()
    body = {"startDate": str(start), "endDate": str(end), "dimensions": ["page"], "rowLimit": 25000}
    req = urllib.request.Request(
        f"https://www.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(site, safe='')}/searchAnalytics/query",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    out = {}
    for r in json.load(urllib.request.urlopen(req)).get("rows", []):
        out[r["keys"][0]] = {"impressions": r["impressions"], "clicks": r["clicks"],
                             "position": round(r["position"], 1)}
    return out

def audit(html: str, brand: str) -> dict:
    body = html
    text = re.sub(r"<[^>]+>", " ", body)
    text = re.sub(r"\s+", " ", text)
    heads = re.findall(r"<h[23][^>]*>(.*?)</h[23]>", body, re.S | re.I)
    heads = [re.sub(r"<[^>]+>", "", h).strip() for h in heads]
    q_heads = [h for h in heads if h.rstrip().endswith("?")]
    md = re.search(r'<meta name="description" content="([^"]*)"', body)
    return {
        "canonical_sentence": CANON[brand].lower() in text.lower(),
        "faq_schema": "FAQPage" in body,
        "question_headings": len(q_heads),
        "comparison_table": bool(re.search(r"<table", body, re.I)),
        "visible_date": bool(re.search(r"Updated\s+(January|February|March|April|May|June|July|August|"
                                       r"September|October|November|December)\s+20\d\d", text, re.I)),
        "meta_description": bool(md and len(md.group(1)) > 60),
        "word_count": len(text.split()),
    }

def score(a: dict) -> int:
    """0-6: how much of the GEO treatment this page already has."""
    return sum([a["canonical_sentence"], a["faq_schema"], a["question_headings"] >= 2,
                a["comparison_table"], a["visible_date"], a["meta_description"]])

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--brand", choices=sorted(SITES), default="datalabs")
    ap.add_argument("--days", type=int, default=180)
    ap.add_argument("--limit", type=int, default=25)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    site = SITES[a.brand]

    pages = gsc_pages(site, a.days)
    ranked = sorted(pages.items(), key=lambda kv: -kv[1]["impressions"])[: a.limit]

    rows = []
    for url, m in ranked:
        try:
            html = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read().decode("utf-8", "ignore")
        except Exception as e:
            rows.append({"url": url, **m, "error": str(e)[:60]}); continue
        au = audit(html, a.brand)
        s = score(au)
        missing = [k for k in ("canonical_sentence", "faq_schema", "comparison_table",
                               "visible_date", "meta_description") if not au[k]]
        if au["question_headings"] < 2:
            missing.append("question_headings")
        rows.append({"url": url.replace(site.rstrip("/"), "") or "/", **m,
                     "geo_score": s, "missing": missing, "words": au["word_count"],
                     # biggest prize = most traffic, least treatment
                     "priority": round((m["impressions"] ** 0.5) * (6 - s), 1)})

    rows.sort(key=lambda r: -r.get("priority", 0))
    if a.json:
        print(json.dumps({"brand": a.brand, "pages": rows}, indent=1)); return

    print(f"\nGEO COVERAGE — {a.brand}, last {a.days} days, top {a.limit} pages by impressions")
    print("=" * 100)
    print(f"{'impr':>7} {'clicks':>6} {'pos':>5}  {'GEO':>5}  page")
    for r in rows:
        if "error" in r:
            print(f"{r['impressions']:>7} {'':>6} {'':>5}  {'??':>5}  {r['url'][:52]}  ({r['error']})"); continue
        flag = "  ← " + ", ".join(r["missing"][:3]) if r["geo_score"] <= 3 else ""
        print(f"{r['impressions']:>7} {r['clicks']:>6} {r['position']:>5}  {r['geo_score']}/6  {r['url'][:50]:52}{flag}")
    print("\nGEO score = canonical sentence · FAQ schema · 2+ question headings · table · visible date · meta description")
    print("Ranked by (traffic already earned) x (treatment missing) — the cheapest wins first.\n")

if __name__ == "__main__":
    main()
