"""Stage 1: find candidate podcasts via the free iTunes Search API.

No key, no cost. `releaseDate` on a podcast result is the most recent episode
date, which gives the runbook's "still publishing" filter for free.
"""
import json, sys, time, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

TERMS = [
    "animation", "animation industry", "animator", "character design",
    "motion design", "motion graphics", "visual effects", "vfx",
    "AI art", "generative art", "creative coding", "new media art",
    "creative technology", "immersive art", "installation art",
    "public art", "experiential marketing", "brand experience",
    "digital art", "art and technology",
]
COUNTRIES = ["US", "AU", "GB"]
CUTOFF = datetime.now(timezone.utc) - timedelta(days=90)

found = {}
for term in TERMS:
    for country in COUNTRIES:
        q = urllib.parse.urlencode(
            {"term": term, "media": "podcast", "limit": 200, "country": country}
        )
        url = f"https://itunes.apple.com/search?{q}"
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                data = json.load(r)
        except Exception as exc:            # a dead term must not kill the run
            print(f"  ! {term}/{country}: {exc}", file=sys.stderr)
            continue
        for row in data.get("results", []):
            cid = row.get("collectionId")
            if cid is None or cid in found:
                continue
            found[cid] = {
                "collection_id": cid,
                "show": row.get("collectionName") or "",
                "artist": row.get("artistName") or "",
                "feed_url": row.get("feedUrl") or "",
                "itunes_url": row.get("collectionViewUrl") or "",
                "genres": row.get("genres") or [],
                "episode_count": row.get("trackCount"),
                "last_episode": row.get("releaseDate") or "",
                "found_by": [],
            }
        for row in data.get("results", []):
            cid = row.get("collectionId")
            if cid in found and term not in found[cid]["found_by"]:
                found[cid]["found_by"].append(term)
        time.sleep(0.25)                    # be polite to a free endpoint
    print(f"  {term}: running total {len(found)}", file=sys.stderr)

live = []
for row in found.values():
    stamp = row["last_episode"]
    if not stamp:
        continue
    try:
        when = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except ValueError:
        continue
    if when >= CUTOFF:
        live.append(row)

live.sort(key=lambda r: r["last_episode"], reverse=True)
out = {
    "sourced": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    "method": "iTunes Search API (free, keyless); filter = episode in last 90 days",
    "searched_terms": TERMS,
    "total_seen": len(found),
    "still_publishing": len(live),
    "shows": live,
}
print(json.dumps(out, indent=2))
print(f"\nSEEN {len(found)} shows, {len(live)} still publishing", file=sys.stderr)
