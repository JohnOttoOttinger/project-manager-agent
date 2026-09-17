#!/usr/bin/env python3
"""Put a page in the queue in your own words, and have it outrank the algorithm.

    python3 suggest.py oddtoe "an art toy designer page, sibling to Inflatable Artist"
    python3 suggest.py datalabs "power bi vs tableau comparison" --slug /power-bi-vs-tableau/
    python3 suggest.py --list                      # the whole queue, both brands
    python3 suggest.py --list oddtoe               # one brand
    python3 suggest.py --status od-art-toy-designer drafting
    python3 suggest.py --drop dl-dashboard-cost "pricing.md still has no rate to publish"

An idea goes in at priority 1 and pushes the algorithmic candidates down. No search volume is
required and none is invented: the item is marked volume-unvalidated and the next DataForSEO
sweep can attach a real figure. A page Otto wants built does not need to justify itself to a
keyword file first.
"""
from __future__ import annotations
import argparse, datetime, json, re, sys
from pathlib import Path

QUEUE = Path(__file__).resolve().parent.parent / "references" / "queue.json"
BRANDS = ("oddtoe", "datalabs")
STATUSES = ("queued", "drafting", "draft", "published", "blocked", "dropped")
LIVE = ("queued", "drafting", "draft", "blocked")


def load():
    return json.loads(QUEUE.read_text())


def save(d):
    QUEUE.write_text(json.dumps(d, indent=1) + "\n")


def make_id(brand, text, taken):
    stem = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    stem = "-".join([w for w in stem.split("-") if len(w) > 2][:4]) or "page"
    base = f"{'od' if brand == 'oddtoe' else 'dl'}-{stem}"
    out, n = base, 2
    while out in taken:
        out, n = f"{base}-{n}", n + 1
    return out


def show(items, brand=None):
    rows = [i for i in items if (not brand or i["brand"] == brand)]
    for b in BRANDS:
        mine = [i for i in rows if i["brand"] == b]
        if not mine:
            continue
        print(f"\n{b.upper()}")
        for i in sorted(mine, key=lambda x: (x["status"] not in LIVE, x["priority"])):
            mark = {"queued": " ", "drafting": ">", "draft": "~",
                    "published": "x", "blocked": "!", "dropped": "-"}[i["status"]]
            vol = f"{i['volume']:,}/mo" if i.get("volume") else "unvalidated"
            src = {"otto": "you", "sweep": "sweep", "scout": "scout"}[i["origin"]]
            print(f"  [{mark}] {i['priority']:>3}. {i['title']}  ({vol}, {src})")
            print(f"        {i['id']}")
    print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("brand", nargs="?", choices=BRANDS)
    ap.add_argument("text", nargs="?", help="the page you want, in your own words")
    ap.add_argument("--slug", help="proposed URL path, if you have one in mind")
    ap.add_argument("--term", help="the search term it should target, if you know it")
    ap.add_argument("--volume", type=int, help="monthly AU volume - ONLY from a real sweep")
    ap.add_argument("--priority", type=int, default=1)
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--status", nargs=2, metavar=("ID", "STATUS"))
    ap.add_argument("--drop", nargs=2, metavar=("ID", "WHY"))
    a = ap.parse_args()
    d = load()

    if a.status:
        _id, st = a.status
        if st not in STATUSES:
            sys.exit(f"status must be one of: {', '.join(STATUSES)}")
        item = next((i for i in d["items"] if i["id"] == _id), None)
        if not item:
            sys.exit(f"no queue item '{_id}' - run --list")
        item["status"], item["updated"] = st, str(datetime.date.today())
        save(d); print(f"{item['title']} -> {st}"); return

    if a.drop:
        _id, why = a.drop
        item = next((i for i in d["items"] if i["id"] == _id), None)
        if not item:
            sys.exit(f"no queue item '{_id}' - run --list")
        item.update(status="dropped", priority=99, updated=str(datetime.date.today()))
        item["note"] = f"DROPPED {datetime.date.today()}: {why}. " + (item.get("note") or "")
        save(d); print(f"dropped: {item['title']}"); return

    if a.list or not a.text:
        show(d["items"], a.brand); return
    if not a.brand:
        sys.exit("which brand? oddtoe or datalabs")

    # Everything at or below the new item's priority shifts down, so "priority 1" means it.
    for i in d["items"]:
        if i["brand"] == a.brand and i["status"] in LIVE and i["priority"] >= a.priority:
            i["priority"] += 1

    item = {"id": make_id(a.brand, a.text, {i["id"] for i in d["items"]}),
            "brand": a.brand, "priority": a.priority, "status": "queued", "origin": "otto",
            "title": a.text[:80], "slug": a.slug, "term": a.term, "volume": a.volume,
            "note": a.text if len(a.text) > 80 else None,
            "added": str(datetime.date.today())}
    if not a.volume:
        item["note"] = ((item["note"] or "") +
                        " VOLUME UNVALIDATED - attach a real figure at the next sweep.").strip()
    d["items"].append(item)
    save(d)
    print(f"\nqueued for {a.brand} at priority {a.priority}: {item['title']}")
    print(f"  id {item['id']}")
    if not a.volume:
        print("  no verified volume - it will build on your say-so, not the algorithm's")
    print()


if __name__ == "__main__":
    main()
