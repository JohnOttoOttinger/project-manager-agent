#!/usr/bin/env python3
"""What is due from the Oddtoe opportunity register, soonest first.

    python3 due.py              next 90 days
    python3 due.py --days 30
    python3 due.py --all        everything, including unverified dates

Reads references/opportunities.md. Rows whose deadline is still TO VERIFY are
listed separately — they are the real risk, because an unverified date cannot
warn you.
"""
import argparse, re, sys
from datetime import date, datetime
from pathlib import Path

REG = Path(__file__).resolve().parents[1] / "references" / "opportunities.md"
DATE_PATTERNS = ["%Y-%m-%d", "%d %b %Y", "%d %B %Y", "%b %Y", "%B %Y"]


def parse_date(s):
    s = s.strip()
    for f in DATE_PATTERNS:
        try:
            d = datetime.strptime(s, f).date()
            return d.replace(day=1) if f in ("%b %Y", "%B %Y") else d
        except ValueError:
            continue
    return None


def rows():
    stream = None
    for line in REG.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s+(\w+)", line)
        if m:
            stream = m.group(1)
            continue
        if not line.startswith("|") or stream is None:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 5 or cells[0].lower() in ("event", "market", "award", "opportunity", "body"):
            continue
        if set(cells[0]) <= set("-: "):
            continue
        if cells[0].startswith("*("):
            continue
        yield stream, cells


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=90)
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()

    today = date.today()
    dated, unverified = [], []
    for stream, c in rows():
        name, deadline, status = c[0], c[-3], c[-2]
        d = parse_date(deadline)
        if d:
            dated.append((d, stream, name, status))
        else:
            unverified.append((stream, name, c[1] if len(c) > 4 else "", status, c[-1]))

    dated.sort()
    horizon = [x for x in dated if a.all or 0 <= (x[0] - today).days <= a.days]
    print(f"Opportunity register — {today.isoformat()}\n")
    if horizon:
        print(f"DUE within {a.days} days:" if not a.all else "ALL dated rows:")
        for d, stream, name, status in horizon:
            n = (d - today).days
            flag = "  <-- OVERDUE" if n < 0 else ("  <-- SOON" if n <= 30 else "")
            print(f"   {d.isoformat()}  ({n:>4}d)  [{stream:<8}] {name[:44]:<46}{status}{flag}")
    else:
        print(f"Nothing dated falls within {a.days} days.")

    if unverified:
        print(f"\nNO VERIFIED DEADLINE — {len(unverified)} rows. These cannot warn you:")
        for stream, name, when, status, source in unverified:
            print(f"   [{stream:<8}] {name[:40]:<42}{when[:16]:<18}{status:<13}{source}")
        print("\nRead each organiser's own press/submissions page and replace TO VERIFY")
        print("with a real date. Press deadlines usually close 2-3 months before the event.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
