#!/usr/bin/env python3
"""Rank the next money page to build, from live Search Console data.

The pattern this is built to find is the one that produced /animation-agency/:
a query with real demand that the site ALREADY shows up for, ranking badly,
converting at nothing, because the page Google is serving is the wrong page.

    python3 next-best-page.py                 # top 10, human readable
    python3 next-best-page.py --json          # machine readable (for the 6am job)
    python3 next-best-page.py --days 90       # shorter window
    python3 next-best-page.py --limit 5

Read-only. Nothing here writes to Google or WordPress.
"""
from __future__ import annotations
import argparse, json, math, os, re, sys, urllib.parse, urllib.request
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "analytics" / "scripts"))
import ga_client  # noqa: E402  (auth + config already solved there)

SITE = "https://www.oddtoe.com/"

# Queries we never want to propose a page for.
BRAND = re.compile(r"\boddtoe|otto ottinger|ottinger\b", re.I)
# Named people / navigational — someone looking for a person, not a service.
PEOPLE = re.compile(r"\b(uta|jason burns|andrew cannava|natanya rose|julie kane|zac simmons|"
                    r"anna berthold|sandy weinberg|john goldsmith|donna felten)\b", re.I)
# Commercial intent lifts a query's value: these are buyers, not researchers.
COMMERCIAL = re.compile(r"\b(cost|costs|price|pricing|hire|hiring|quote|agency|agencies|"
                        r"company|companies|service|services|studio|studios|near me|best|"
                        r"for hire|commission)\b", re.I)
STOP = set("a an the for of in on to and or with your you my is are what how much does do "
           "can i it that this be by from at as".split())


def terms(q: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", q.lower()) if w not in STOP and len(w) > 2}


def slug_terms(url: str) -> set[str]:
    path = urllib.parse.urlparse(url).path
    return {w for w in re.findall(r"[a-z0-9]+", path.lower()) if len(w) > 2}


def fetch(days: int) -> list[dict]:
    import datetime
    end = datetime.date.today() - datetime.timedelta(days=3)
    start = end - datetime.timedelta(days=days)
    tok = ga_client.get_token()
    site = urllib.parse.quote(SITE, safe="")
    body = {"startDate": str(start), "endDate": str(end),
            "dimensions": ["query", "page"], "rowLimit": 25000}
    req = urllib.request.Request(
        f"https://www.googleapis.com/webmasters/v3/sites/{site}/searchAnalytics/query",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req)).get("rows", [])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=180)
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    rows = fetch(a.days)

    # Everything the site already ranks WELL for — the cannibalisation guardrail set.
    strong: dict[str, list] = defaultdict(list)          # page -> [(query, pos, impr)]
    for r in rows:
        q, page = r["keys"]
        if r["position"] <= 10 and r["impressions"] >= 20 \
           and not BRAND.search(q) and not PEOPLE.search(q):
            strong[page].append((q, r["position"], r["impressions"]))

    # Term frequency across all queries — the two most common terms in a query are its topic.
    # This is what merges "character design services / studio / company" into ONE page opportunity
    # instead of proposing three near-identical pages.
    freq = defaultdict(int)
    for r in rows:
        for t in terms(r["keys"][0]):
            freq[t] += 1

    def cluster_key(q: str):
        t = terms(q)
        return frozenset(sorted(t, key=lambda w: (-freq[w], w))[:2])

    clusters: dict[frozenset, dict] = {}
    for r in rows:
        q, page = r["keys"]
        if BRAND.search(q) or PEOPLE.search(q):
            continue
        if r["impressions"] < 25:
            continue
        key = cluster_key(q)
        if not key:
            continue
        c = clusters.setdefault(key, {"queries": [], "impr": 0, "clicks": 0,
                                      "pages": defaultdict(int), "pos": []})
        c["queries"].append((q, r["impressions"], r["clicks"], r["position"], page))
        c["impr"] += r["impressions"]; c["clicks"] += r["clicks"]
        c["pages"][page] += r["impressions"]
        c["pos"].append((r["position"], r["impressions"]))

    scored = []
    for key, c in clusters.items():
        if c["impr"] < 100:
            continue
        wpos = sum(p * i for p, i in c["pos"]) / max(1, sum(i for _, i in c["pos"]))
        ctr = c["clicks"] / c["impr"] if c["impr"] else 0
        top_page = max(c["pages"], key=c["pages"].get)
        head = max(c["queries"], key=lambda x: x[1])[0]

        # A page ranking top-10 is the RIGHT page — if it earns no clicks that is a
        # title/meta problem, not a missing page. Never propose building a page over it.
        ranks_well = wpos <= 10
        overlap = len(terms(head) & slug_terms(top_page)) / max(1, len(terms(head)))
        mismatch = (overlap < 0.5) and not ranks_well

        volume = math.log10(c["impr"])
        band = 1.0 if 11 <= wpos <= 40 else 0.15          # page 2-4 is the winnable band
        waste = 1.0 if (ctr < 0.01 and c["impr"] >= 300 and not ranks_well) else 0.0
        commercial = 0.7 if COMMERCIAL.search(head) else 0.0
        score = volume * band + 1.6 * mismatch + 1.3 * waste + commercial
        kind = "title-meta-fix" if (ranks_well and ctr < 0.01 and c["impr"] >= 300) else "new-page"
        if kind == "title-meta-fix":
            score = volume * 0.5 + commercial          # ranked separately, never competes for #1

        # --- guardrails: strong rankings on OTHER pages that share terms with this cluster ---
        guards = []
        for page, lst in strong.items():
            if page == top_page:
                continue
            for gq, gpos, gimpr in lst:
                if len(terms(gq) & terms(head)) >= 2:
                    guards.append({"query": gq, "page": page, "position": round(gpos, 1),
                                   "impressions": gimpr})
        guards.sort(key=lambda g: g["position"])

        scored.append({
            "head_query": head,
            "cluster_size": len(c["queries"]),
            "impressions": c["impr"], "clicks": c["clicks"],
            "ctr_pct": round(ctr * 100, 2), "avg_position": round(wpos, 1),
            "served_by": top_page.replace("https://www.oddtoe.com", "") or "/",
            "wrong_page": mismatch,
            "wasted_demand": bool(waste),
            "commercial_intent": bool(commercial),
            "kind": kind,
            "score": round(score, 2),
            "proposed_slug": "/" + re.sub(r"[^a-z0-9]+", "-", head.lower()).strip("-") + "/",
            "do_not_target": guards[:6],
            "top_queries": [{"q": q, "impr": i, "clicks": cl, "pos": round(p, 1)}
                            for q, i, cl, p, _ in sorted(c["queries"], key=lambda x: -x[1])[:5]],
        })

    scored.sort(key=lambda x: -x["score"])
    out = scored[:a.limit]

    if a.json:
        print(json.dumps({"window_days": a.days, "opportunities": out}, indent=1)); return

    newp = [o for o in scored if o["kind"] == "new-page"][:a.limit]
    fixes = [o for o in scored if o["kind"] == "title-meta-fix"][:5]

    print(f"\nNEXT BEST PAGE — Oddtoe, last {a.days} days\n" + "=" * 78)
    for i, o in enumerate(newp, 1):
        flags = " ".join(f for f, on in
                         [("WRONG-PAGE", o["wrong_page"]), ("WASTED-DEMAND", o["wasted_demand"]),
                          ("COMMERCIAL", o["commercial_intent"])] if on) or "—"
        print(f"\n{i}. {o['head_query']}   [score {o['score']}]  ({o['cluster_size']} queries in cluster)")
        print(f"   {o['impressions']:,} impr · {o['clicks']} clicks · {o['ctr_pct']}% CTR · pos {o['avg_position']}")
        print(f"   served by: {o['served_by']}")
        print(f"   flags: {flags}")
        print(f"   proposed: {o['proposed_slug']}")
        if o["do_not_target"]:
            print("   DO NOT BID FOR (already ranking elsewhere):")
            for g in o["do_not_target"][:4]:
                print(f"     · \"{g['query']}\" pos {g['position']} on {g['page'].replace('https://www.oddtoe.com','')}")
    if fixes:
        print("\n" + "-" * 78)
        print("NOT pages — these already rank top-10 and earn no clicks. Fix the title/meta.")
        for o in fixes:
            print(f"   · {o['head_query']}  —  {o['impressions']:,} impr, pos {o['avg_position']}, "
                  f"{o['ctr_pct']}% CTR  on {o['served_by']}")
    print()


if __name__ == "__main__":
    main()
