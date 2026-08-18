#!/usr/bin/env python3
"""Media outreach stream — pipeline state from media-contacts.json.

    python3 media.py                 pipeline summary + actionable rows
    python3 media.py --segment journalist
    python3 media.py --status sourced
    python3 media.py --md            markdown register view (for pasting/reading,
                                     never hand-edited back — the JSON is canonical)

Source of truth is references/media-contacts.json. This script only reads it.
One dataset, every view generated.
"""
import argparse, json, sys
from pathlib import Path

REG = Path(__file__).resolve().parents[1] / "references" / "media-contacts.json"


def load():
    return json.loads(REG.read_text(encoding="utf-8"))


def summary(d, rows):
    flow = d["status_flow"]
    print(f"Media stream — updated {d['updated']} — {len(rows)} contacts\n")
    segs = sorted({c["segment"] for c in rows})
    hdr = "segment".ljust(12) + "".join(s.ljust(11) for s in flow)
    print("   " + hdr)
    for seg in segs:
        srows = [c for c in rows if c["segment"] == seg]
        counts = "".join(str(sum(1 for c in srows if c["status"] == s)).ljust(11) for s in flow)
        print("   " + seg.ljust(12) + counts)
    unver = [c for c in rows if c["status"] != "sourced" and not c.get("verified")]
    if unver:
        print(f"\nUNVERIFIED past 'sourced' — {len(unver)} rows should not have advanced:")
        for c in unver:
            print(f"   {c['id']}  [{c['status']}]")
    noperson = [c for c in rows if c["status"] == "sourced" and not c.get("person")]
    if noperson:
        print(f"\nNext sourcing pass: {len(noperson)} rows have an outlet but no named person yet.")


def table(rows):
    for c in rows:
        who = c.get("person") or "(person TO FILL)"
        print(f"   [{c['segment']:<10}] {c['outlet'][:28]:<30} {who[:22]:<24} "
              f"{c['status']:<10} rel:{c.get('relevance') or '-'}  hook:{c.get('hook') or '-'}")


def markdown(d, rows):
    print("## media — podcasts, YouTube, journalists, PR agencies\n")
    print(f"Generated from `media-contacts.json` (updated {d['updated']}). "
          "Do not hand-edit rows here — edit the JSON.\n")
    print("| Segment | Outlet / show | Person | Status | Hook | Why it fits |")
    print("|---|---|---|---|---|---|")
    for c in rows:
        why = (c.get("why_fit") or "").split(".")[0]
        print(f"| {c['segment']} | [{c['outlet']}]({c['url']}) | {c.get('person') or 'TO FILL'} "
              f"| {c['status']} | {c.get('hook') or '—'} | {why} |")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--segment")
    ap.add_argument("--status")
    ap.add_argument("--md", action="store_true")
    a = ap.parse_args()
    d = load()
    rows = d["contacts"]
    if a.segment:
        rows = [c for c in rows if c["segment"] == a.segment]
    if a.status:
        rows = [c for c in rows if c["status"] == a.status]
    if a.md:
        markdown(d, rows)
        return 0
    summary(d, d["contacts"])
    if a.segment or a.status:
        print()
        table(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
