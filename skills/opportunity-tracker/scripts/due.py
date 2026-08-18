#!/usr/bin/env python3
"""What is due from the Oddtoe opportunity register, soonest first.

    python3 due.py                next 90 days
    python3 due.py --days 30
    python3 due.py --all
    python3 due.py --unverified   only rows whose dates were never checked

Source of truth is references/opportunities.json — the same file that generates
the public animation-conferences page. One dataset, two views.

Rows with no verified date are listed separately and loudly. They are the real
risk: an unverified deadline cannot warn you, and a confident wrong date is
worse than a blank.
"""
import argparse, json, sys
from datetime import date
from pathlib import Path

REG = Path(__file__).resolve().parents[1] / "references" / "opportunities.json"


def load():
    return json.loads(REG.read_text(encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=90)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--unverified", action="store_true")
    a = ap.parse_args()

    d = load()
    today = date.today()
    ents = d["entries"]

    print(f"Oddtoe opportunity register — {today.isoformat()}  (updated {d['updated']})\n")

    if not a.unverified:
        upcoming = []
        for e in ents:
            if not e.get("start"):
                continue
            start = date.fromisoformat(e["start"])
            days = (start - today).days
            if a.all or 0 <= days <= a.days:
                upcoming.append((start, days, e))
        upcoming.sort(key=lambda x: (x[0], x[2]['name']))
        if upcoming:
            print("EVENT" if a.all else f"Events starting within {a.days} days:")
            for start, days, e in upcoming:
                flag = "  <-- SOON" if days <= 45 else ""
                pd = e.get("press_deadline") or "-"
                print(f"   {start.isoformat()}  ({days:>4}d)  [{e['type']:<7}] "
                      f"{e['name'][:40]:<42} press:{pd:<11}{flag}")
        else:
            print(f"No events start within {a.days} days.")

        past = [e for e in ents if e.get("end") and date.fromisoformat(e["end"]) < today]
        if past:
            print(f"\nPAST — {len(past)} entr{'y' if len(past)==1 else 'ies'} already finished. "
                  "Roll forward or unpublish:")
            for e in past:
                print(f"   {e['end']}  {e['name'][:52]}")

    unver = [e for e in ents if not e.get("verified")]
    if unver:
        print(f"\nNEVER VERIFIED — {len(unver)} rows. These cannot warn you:")
        for e in unver:
            print(f"   [{e['type']:<7}] {e['name'][:44]:<46}{e.get('label','')[:34]}")

    todo = [e for e in ents if e.get("press_deadline") == "TO VERIFY"
            or e.get("submission_deadline") == "TO VERIFY"]
    if todo:
        print(f"\nDEADLINE UNKNOWN — {len(todo)} rows need a read of the organiser's own page.")
        print("Press deadlines usually close 2-3 months before the event.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
