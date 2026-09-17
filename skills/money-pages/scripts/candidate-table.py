#!/usr/bin/env python3
"""One table joining every source we have, so the next-page decision can be argued about.

Columns come from four places, and the point is that they disagree:

  SWEEP (DataForSEO)   what Australia actually searches for, whether or not we rank.
  GSC                  what we earn today, AU-filtered and machine-filtered. Answers "is
                       anything of ours already absorbing this demand, and how well".
  GA4                  what the nearest existing page does for the BUSINESS - ENGAGED sessions
                       from human channels, and key events. Raw `sessions` is not usable here:
                       Datalabs' Direct channel ran 14,616 sessions in Feb 2026 at 8% engagement
                       and 5.7 seconds average duration. Bots. Excluding Direct is the point.
  LIVE                 is the proposed slug a real 404.

    python3 candidate-table.py                  # 10 rows, markdown
    python3 candidate-table.py --limit 15 --json
    python3 candidate-table.py --brand oddtoe

Read-only.
"""
from __future__ import annotations
import argparse, datetime, json, math, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REF = HERE.parent / "references"
sys.path.insert(0, str(HERE.parents[1] / "analytics" / "scripts"))
sys.path.insert(0, str(HERE))
import ga_client, geo_uplift                                        # noqa: E402
import importlib.util                                               # noqa: E402
_spec = importlib.util.spec_from_file_location("nc", HERE / "next-content.py")
nc = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(nc)

SITES = {"oddtoe": "https://www.oddtoe.com", "datalabs": "https://www.datalabsagency.com"}
GA4 = {"oddtoe": None, "datalabs": "265583155"}          # None = the env default (Oddtoe)


def gsc_rows(brand, days=180, country="aus"):
    """query+page rows, filtered to Australia. The country filter is not cosmetic: filtering
    the Oddtoe prop page to AU dropped machine-shaped impressions from 78% to 5%."""
    import os, urllib.parse, urllib.request
    end = datetime.date.today() - datetime.timedelta(days=3)
    start = end - datetime.timedelta(days=days)
    prop = os.environ.get("GSC_ODDTOE_SITE_URL") if brand == "oddtoe" else SITES[brand] + "/"
    body = {"startDate": str(start), "endDate": str(end),
            "dimensions": ["query", "page"], "rowLimit": 25000,
            "dimensionFilterGroups": [{"filters": [
                {"dimension": "country", "operator": "equals", "expression": country}]}]}
    req = urllib.request.Request(
        "https://www.googleapis.com/webmasters/v3/sites/"
        f"{urllib.parse.quote(prop or SITES[brand] + '/', safe='')}/searchAnalytics/query",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {ga_client.get_token()}",
                 "Content-Type": "application/json"})
    return [{"query": r["keys"][0], "page": r["keys"][1], "clicks": r["clicks"],
             "impressions": r["impressions"], "position": r["position"]}
            for r in json.load(urllib.request.urlopen(req)).get("rows", [])]


# Channels whose sessions are people. Datalabs' Direct channel was 14,616 sessions in Feb 2026
# at 8% engagement and an average duration of 5.7 SECONDS — bots, and they made raw `sessions`
# useless for ranking anything. Measured 4 Sep 2026; same disease as the GSC impression
# contamination, different metric. Organic Search that month: 916 sessions, 78% engaged, 119s.
HUMAN_CHANNELS = ["Organic Search", "AI Assistant", "Referral", "Organic Social", "Paid Search"]


def ga4_pages(brand, days=180):
    """Engaged sessions from human channels only. Raw `sessions` is not a business signal here."""
    import urllib.request
    body = {"dateRanges": [{"startDate": f"{days}daysAgo", "endDate": "yesterday"}],
            "dimensions": [{"name": "pagePath"}],
            "metrics": [{"name": "sessions"}, {"name": "engagedSessions"}, {"name": "keyEvents"}],
            "dimensionFilter": {"filter": {"fieldName": "sessionDefaultChannelGroup",
                                           "inListFilter": {"values": HUMAN_CHANNELS}}},
            "limit": 500,
            "orderBys": [{"metric": {"metricName": "engagedSessions"}, "desc": True}]}
    prop = GA4[brand] or ga_client.config()["property_id"]
    try:
        req = urllib.request.Request(
            f"https://analyticsdata.googleapis.com/v1beta/properties/{prop}:runReport",
            data=json.dumps(body).encode(),
            headers={"Authorization": f"Bearer {ga_client.get_token()}",
                     "Content-Type": "application/json"})
        d = json.load(urllib.request.urlopen(req))
    except Exception as e:
        print(f"(GA4 {brand} unavailable: {type(e).__name__}: {e})", file=sys.stderr)
        return {}
    out = {}
    for row in d.get("rows", []):
        path = row["dimensionValues"][0]["value"].split("?")[0].rstrip("/") + "/"
        m = [v["value"] for v in row["metricValues"]]
        out[path] = {"sessions": int(m[0]), "engagedSessions": int(m[1]), "keyEvents": int(m[2])}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brand", choices=sorted(SITES))
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--days", type=int, default=180)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--sort", choices=("score", "volume"), default="score")
    ap.add_argument("--per-brand", type=int, default=0,
                    help="cap rows per brand so one brand's bigger numbers cannot fill the table")
    a = ap.parse_args()

    universe = json.loads((REF / "keyword-universe.json").read_text())
    queue = json.loads((REF / "queue.json").read_text())["items"]
    brands = [a.brand] if a.brand else sorted(SITES)

    rows = []
    for brand in brands:
        gsc = gsc_rows(brand, a.days)
        ga4 = ga4_pages(brand, a.days)
        # Machine-shaped queries, structurally identified - never by click performance.
        perms = geo_uplift.permutation_cluster(
            [{"query": r["query"]} for r in {x["query"]: x for x in gsc}.values()])
        claimed = {(q.get("term") or "").lower() for q in queue}
        claimed_titles = [(q["title"], nc.tokens(q["title"] + " " + (q.get("term") or ""), True))
                          for q in queue if q["status"] != "dropped"]

        for t in universe["terms"]:
            if t["brand"] != brand or t.get("exclude"):
                continue
            tk = nc.tokens(t["term"], stemmed=True)
            # everything we ALREADY earn on queries that mean this term
            hits = [r for r in gsc
                    if len(nc.tokens(r["query"], stemmed=True) & tk) >= max(1, len(tk) - 1)
                    and not geo_uplift.machine_shaped(r["query"])
                    and r["query"] not in perms]
            impr = sum(h["impressions"] for h in hits)
            clicks = sum(h["clicks"] for h in hits)
            pos = (sum(h["position"] * h["impressions"] for h in hits) / impr) if impr else None
            near = max({h["page"] for h in hits},
                       key=lambda p: sum(h["impressions"] for h in hits if h["page"] == p),
                       default=None)
            npath = near.replace(SITES[brand], "") if near else None
            g = ga4.get(npath) if npath else None

            slug = t.get("served_by") or t.get("slug") or nc.slugify(t["term"])
            code, final = nc.head(SITES[brand] + slug)
            cw, _ = nc.commercial(t["term"], brand)
            ww, _ = nc.winnability(t.get("incumbent"))
            rw, _ = nc.relevant(t["term"], brand)
            comp = nc.COMPETITION.get((t.get("competition") or "").upper(), 0.85)
            gap = 0.0 if (t.get("served_by") or code == 200) else (1.0 if code in (404, 410) else 0.5)
            inc = t.get("incumbent") or {}
            rows.append({
                "brand": brand, "term": t["term"], "volume": t.get("volume") or 0,
                "competition": t.get("competition"), "cpc": t.get("cpc"),
                "incumbent": f"{inc.get('who','-')} #{inc['position']}" if inc else "-",
                "au_clicks_180d": clicks, "au_impressions_180d": impr,
                "our_position": round(pos, 1) if pos else None,
                "nearest_page": npath or "-",
                "ga4_engaged_sessions": g["engagedSessions"] if g else None,
                "ga4_key_events": g["keyEvents"] if g else None,
                "slug_status": "EXISTS" if gap == 0.0 else ("404" if gap == 1.0 else f"HTTP {code}"),
                "in_queue": next((ti for ti, tkq in claimed_titles
                                  if len(tkq & tk) >= 2), None),
                "score": round(math.log10(max(t.get("volume") or 0, 10))
                               * rw * cw * gap * ww * comp, 2),
                "note": t.get("note"),
            })

    rows.sort(key=lambda r: -r[a.sort])
    if a.per_brand:
        kept, seen = [], {}
        for r in rows:
            if seen.get(r["brand"], 0) < a.per_brand:
                kept.append(r); seen[r["brand"]] = seen.get(r["brand"], 0) + 1
        rows = kept
    rows = rows[: a.limit]
    if a.json:
        print(json.dumps({"generated": str(datetime.date.today()),
                          "window_days": a.days, "rows": rows}, indent=1)); return

    print(f"\n# Next-page candidates — every source, {a.days}d, Australia only")
    print(f"\nSweep captured {universe['captured']}. GSC/GA4 to "
          f"{datetime.date.today() - datetime.timedelta(days=3)}. "
          "AU clicks are machine-filtered; impressions are not bankable, clicks are.\n")
    h = ("| # | term | brand | AU vol/mo | comp | CPC | incumbent | our AU clicks | our impr | "
         "our pos | nearest page | GA4 sess | GA4 events | slug | score | already queued |")
    print(h); print("|" + "---|" * (h.count("|") - 1))
    for i, r in enumerate(rows, 1):
        print(f"| {i} | {r['term']} | {r['brand']} | {r['volume']:,} | "
              f"{r['competition'] or '?'} | {('$%.2f' % r['cpc']) if r['cpc'] else '-'} | "
              f"{r['incumbent']} | {r['au_clicks_180d']} | {r['au_impressions_180d']:,} | "
              f"{r['our_position'] or '-'} | {r['nearest_page']} | "
              f"{r['ga4_engaged_sessions'] if r['ga4_engaged_sessions'] is not None else '-'} | "
              f"{r['ga4_key_events'] if r['ga4_key_events'] is not None else '-'} | "
              f"{r['slug_status']} | {r['score']} | {r['in_queue'] or '-'} |")
    print()


if __name__ == "__main__":
    main()
