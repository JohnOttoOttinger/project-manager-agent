#!/usr/bin/env python3
"""Analytics reporting for Oddtoe — GA4 + Search Console, read-only.

    python3 report.py digest              weekly digest, compared to last snapshot
    python3 report.py watch               only what crossed an alert threshold
    python3 report.py verify <url>        did a published page get indexed and ranked
    python3 report.py queries [--contains X] [--days N] [--limit N]
    python3 report.py pages   [--days N]
    python3 report.py enquiries [--days N]
    python3 report.py snapshot            record today's numbers for future deltas

Every command takes --json for machine-readable output.
Nothing here writes to Google. It only reads.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ga_client as ga  # noqa: E402

SKILL_ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_DIR = SKILL_ROOT / "references" / "snapshots"
WATCHLIST = SKILL_ROOT / "references" / "watchlist.json"

# Alert thresholds — see SKILL.md for why these values.
POSITION_MOVE = 5.0        # a watched term shifting this many places
NEW_QUERY_IMPRESSIONS = 100  # a query appearing from nowhere at this scale


def _days_ago(n: int) -> str:
    return (date.today() - timedelta(days=n)).isoformat()


def load_watchlist() -> dict:
    if not WATCHLIST.exists():
        return {"queries": [], "pages": []}
    return json.loads(WATCHLIST.read_text())


# --- data gathering --------------------------------------------------------

def gather(days: int = 28) -> dict:
    """One consistent pull of everything the digest and watch commands need."""
    start, end = _days_ago(days), _days_ago(1)

    totals = ga.ga4_report(["activeUsers", "sessions", "screenPageViews"], start=f"{days}daysAgo")
    pages = ga.ga4_report(
        ["screenPageViews"], ["pagePath"], start=f"{days}daysAgo",
        limit=15, order_by_metric="screenPageViews",
    )
    queries = ga.gsc_query(["query"], start, end, limit=100)
    landing = ga.gsc_query(["page"], start, end, limit=25)

    enquiries = 0
    for row in ga.ga4_report(["eventCount"], ["eventName"], start=f"{days}daysAgo", limit=50):
        if row.get("eventName") == "ThankYouOddtoeClicks":
            enquiries = row["eventCount"]

    return {
        "captured": date.today().isoformat(),
        "window_days": days,
        "totals": totals[0] if totals else {},
        "enquiries": enquiries,
        "pages": pages,
        "queries": queries,
        "landing_pages": landing,
    }


def latest_snapshot() -> dict | None:
    files = sorted(SNAPSHOT_DIR.glob("*.json"))
    return json.loads(files[-1].read_text()) if files else None


def save_snapshot(data: dict) -> Path:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = SNAPSHOT_DIR / f"{data['captured']}.json"
    path.write_text(json.dumps(data, indent=2))
    return path


# --- commands --------------------------------------------------------------

def cmd_digest(args) -> dict:
    now = gather(args.days)
    previous = latest_snapshot()
    watch = load_watchlist()

    by_query = {row["query"]: row for row in now["queries"]}
    prev_queries = {row["query"]: row for row in (previous or {}).get("queries", [])}

    movers, new_queries = [], []
    for term, row in by_query.items():
        before = prev_queries.get(term)
        if before is None:
            if row["impressions"] >= NEW_QUERY_IMPRESSIONS:
                new_queries.append(row)
        else:
            delta = before["position"] - row["position"]  # positive = improved
            if abs(delta) >= POSITION_MOVE:
                movers.append({**row, "was": before["position"], "moved": round(delta, 1)})

    watched = [by_query[t] for t in watch.get("queries", []) if t in by_query]
    opportunities = sorted(
        [r for r in now["queries"] if r["clicks"] == 0 and r["impressions"] >= 200],
        key=lambda r: -r["impressions"],
    )[:8]

    return {
        "window": f"last {args.days} days",
        "compared_to": (previous or {}).get("captured", "no earlier snapshot"),
        "totals": now["totals"],
        "enquiries": now["enquiries"],
        "watched_queries": watched,
        "movers": sorted(movers, key=lambda r: -abs(r["moved"]))[:10],
        "new_queries": sorted(new_queries, key=lambda r: -r["impressions"])[:10],
        "unconverted_impressions": opportunities,
        "top_pages": now["pages"][:8],
        "_snapshot": now,
    }


def cmd_watch(args) -> dict:
    digest = cmd_digest(args)
    alerts = []

    for row in digest["movers"]:
        direction = "improved" if row["moved"] > 0 else "dropped"
        alerts.append({
            "kind": "position_move",
            "detail": f"'{row['query']}' {direction} {abs(row['moved'])} places "
                      f"({row['was']} -> {row['position']})",
        })
    for row in digest["new_queries"]:
        alerts.append({
            "kind": "new_query",
            "detail": f"'{row['query']}' appeared with {row['impressions']} impressions "
                      f"at position {row['position']}",
        })

    for page in load_watchlist().get("pages", []):
        try:
            state = ga.gsc_inspect(page)
        except ga.ConfigError as exc:
            alerts.append({"kind": "inspect_failed", "detail": f"{page}: {exc}"})
            continue
        if state["verdict"] != "PASS":
            alerts.append({
                "kind": "not_indexed",
                "detail": f"{page} is {state['verdict']} — {state['coverage']}",
            })

    return {"alerts": alerts, "checked": digest["compared_to"]}


def cmd_verify(args) -> dict:
    url = args.url
    state = ga.gsc_inspect(url)

    path = url.replace("https://www.oddtoe.com", "") or "/"
    search = ga.gsc_query(["query"], _days_ago(args.days), _days_ago(1),
                          page_equals=url, limit=15)
    views = [r for r in ga.ga4_report(["screenPageViews"], ["pagePath"],
                                      start=f"{args.days}daysAgo", limit=200)
             if r["pagePath"] == path]

    return {
        "url": url,
        "indexed": state["verdict"] == "PASS",
        "index_state": f"{state['verdict']} — {state['coverage']}",
        "last_crawl": state["last_crawl"],
        "pageviews": views[0]["screenPageViews"] if views else 0,
        "queries": search,
        "impressions": sum(r["impressions"] for r in search),
        "clicks": sum(r["clicks"] for r in search),
    }


def cmd_queries(args) -> dict:
    rows = ga.gsc_query(["query"], _days_ago(args.days), _days_ago(1),
                        contains=args.contains, limit=args.limit)
    return {"window_days": args.days, "filter": args.contains or "(none)", "rows": rows}


def cmd_pages(args) -> dict:
    return {"window_days": args.days,
            "rows": ga.ga4_report(["screenPageViews", "activeUsers"], ["pagePath"],
                                  start=f"{args.days}daysAgo", limit=args.limit,
                                  order_by_metric="screenPageViews")}


def cmd_enquiries(args) -> dict:
    rows = ga.ga4_report(["eventCount"], ["eventName"], start=f"{args.days}daysAgo", limit=50)
    count = next((r["eventCount"] for r in rows if r.get("eventName") == "ThankYouOddtoeClicks"), 0)
    landing = ga.ga4_report(["sessions"], ["landingPage"], start=f"{args.days}daysAgo",
                            limit=10, order_by_metric="sessions")
    return {"window_days": args.days, "enquiries": count, "top_landing_pages": landing}


def cmd_snapshot(args) -> dict:
    path = save_snapshot(gather(args.days))
    return {"saved": str(path.relative_to(SKILL_ROOT.parents[1]))}


# --- output ----------------------------------------------------------------

def render(name: str, data: dict) -> str:
    if name == "digest":
        t, out = data["totals"], []
        out.append(f"ODDTOE · {data['window']} · vs {data['compared_to']}")
        out.append(f"  {t.get('activeUsers', 0)} users · {t.get('sessions', 0)} sessions "
                   f"· {t.get('screenPageViews', 0)} views · {data['enquiries']} enquiries")
        for title, key, fmt in (
            ("MOVED", "movers", lambda r: f"{r['query'][:44]:46s} {r['was']:>5} -> {r['position']:<5} ({r['moved']:+})"),
            ("NEW", "new_queries", lambda r: f"{r['query'][:44]:46s} {r['impressions']:>6} impr  pos {r['position']}"),
            ("WATCHED", "watched_queries", lambda r: f"{r['query'][:44]:46s} {r['clicks']:>4} clicks {r['impressions']:>6} impr  pos {r['position']}"),
            ("IMPRESSIONS, NO CLICKS", "unconverted_impressions", lambda r: f"{r['query'][:44]:46s} {r['impressions']:>6} impr  pos {r['position']}"),
        ):
            rows = data.get(key) or []
            if rows:
                out.append(f"\n{title}")
                out += [f"  {fmt(r)}" for r in rows]
        return "\n".join(out)

    if name == "watch":
        if not data["alerts"]:
            return "No alerts. Nothing crossed a threshold."
        return "\n".join(f"  [{a['kind']}] {a['detail']}" for a in data["alerts"])

    if name == "verify":
        return (f"{data['url']}\n"
                f"  indexed      {data['indexed']} ({data['index_state']})\n"
                f"  last crawl   {data['last_crawl']}\n"
                f"  pageviews    {data['pageviews']}\n"
                f"  search       {data['clicks']} clicks / {data['impressions']} impressions\n"
                + "".join(f"    {r['query'][:44]:46s} {r['clicks']:>3} / {r['impressions']:>5}  pos {r['position']}\n"
                          for r in data["queries"]))

    if name in ("queries", "pages"):
        rows = data["rows"]
        if not rows:
            return "No rows."
        keys = list(rows[0].keys())
        head = "  " + "  ".join(f"{k[:22]:>22s}" if i else f"{k[:44]:44s}" for i, k in enumerate(keys))
        body = "\n".join(
            "  " + "  ".join(f"{str(r[k])[:22]:>22s}" if i else f"{str(r[k])[:44]:44s}"
                             for i, k in enumerate(keys))
            for r in rows)
        return head + "\n" + body

    return json.dumps(data, indent=2)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("digest", "watch", "snapshot"):
        p = sub.add_parser(name)
        p.add_argument("--days", type=int, default=28)

    p = sub.add_parser("verify")
    p.add_argument("url")
    p.add_argument("--days", type=int, default=28)

    p = sub.add_parser("queries")
    p.add_argument("--contains")
    p.add_argument("--days", type=int, default=90)
    p.add_argument("--limit", type=int, default=25)

    p = sub.add_parser("pages")
    p.add_argument("--days", type=int, default=28)
    p.add_argument("--limit", type=int, default=15)

    p = sub.add_parser("enquiries")
    p.add_argument("--days", type=int, default=28)

    args = parser.parse_args()
    handler = globals()[f"cmd_{args.command}"]

    try:
        data = handler(args)
    except ga.ConfigError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    data.pop("_snapshot", None) if args.json else None
    print(json.dumps(data, indent=2) if args.json else render(args.command, data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
