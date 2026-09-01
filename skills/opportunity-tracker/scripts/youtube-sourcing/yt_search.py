"""Stage 1: find channels via RECENT on-topic videos, using the official API.

Why this beats the scrapers tried earlier: `publishedAfter` is enforced by the
API, so the stale canon (12-year-old Creators Project videos) never enters the
pool in the first place. Quota: search.list = 100 units/call, 10,000/day free.
"""
import json, os, sys, time, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

KEY = os.environ["YOUTUBE_API_KEY"]
API = "https://www.googleapis.com/youtube/v3"
SINCE = (datetime.now(timezone.utc) - timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%SZ")

QUERIES = [
    # physical practice
    "public art installation artist", "kinetic sculpture artist",
    "projection mapping installation", "light festival installation art",
    "immersive art installation", "land art environmental sculpture",
    "topiary garden design", "sensory garden design",
    "prop making fabrication studio", "puppet building",
    "art toy designer", "character design process",
    # animation / AI strand
    "AI animation workflow artist", "generative art process",
    "motion design studio process",
    # the vibe axis - Otto's correction: humour is load-bearing
    "weird art project", "playful public art", "funny sculpture project",
    "artist studio tour workshop", "how it's made art installation",
]

def api(path, **params):
    params["key"] = KEY
    url = f"{API}/{path}?{urllib.parse.urlencode(params)}"
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.load(r)
        except Exception as exc:
            if attempt == 2:
                print(f"  ! {path} {params.get('q','')}: {exc}", file=sys.stderr)
                return {}
            time.sleep(2 * (attempt + 1))

channels, videos = {}, []
for q in QUERIES:
    d = api("search", part="snippet", q=q, type="video", maxResults=50,
            order="relevance", publishedAfter=SINCE, relevanceLanguage="en")
    items = d.get("items", [])
    for it in items:
        sn = it["snippet"]
        cid = sn["channelId"]
        videos.append({"channel_id": cid, "title": sn["title"],
                       "published": sn["publishedAt"], "query": q,
                       "video_id": it["id"].get("videoId", "")})
        c = channels.setdefault(cid, {"channel_id": cid,
                                      "channel_title": sn["channelTitle"],
                                      "queries": [], "hits": 0})
        c["hits"] += 1
        if q not in c["queries"]:
            c["queries"].append(q)
    print(f"  {q[:38]:40} +{len(items):>2}  channels so far {len(channels)}", file=sys.stderr)

json.dump({"since": SINCE, "channels": list(channels.values()), "videos": videos},
          open("search.json", "w"), indent=2)
print(f"\n{len(videos)} recent on-topic videos across {len(channels)} channels", file=sys.stderr)
print(f"quota used ~{len(QUERIES)*100} units of 10000", file=sys.stderr)
