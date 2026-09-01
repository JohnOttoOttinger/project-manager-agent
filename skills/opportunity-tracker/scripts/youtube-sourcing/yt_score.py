"""Stage 3: true last-upload date + fit scoring.

A channel's uploads playlist id is its channel id with UC -> UU, so the latest
upload costs 1 quota unit per channel with no extra lookup. That gives the
runbook's real "uploaded in the last 60 days" filter rather than an inference.
Scoring keeps territory and vibe separate, per Otto's direction.
"""
import concurrent.futures as cf, json, os, urllib.parse, urllib.request
from datetime import datetime, timezone

KEY = os.environ["YOUTUBE_API_KEY"]
API = "https://www.googleapis.com/youtube/v3"
NOW = datetime.now(timezone.utc)

TERRITORY = {3: ["public art","installation","sculpture","projection","kinetic","land art",
                 "immersive","topiary","garden design","sensory garden","fabrication",
                 "prop making","puppet","art toy","generative","creative coding",
                 "light festival","mural","placemaking","exhibition"],
             2: ["animation","animator","motion design","character design","illustration",
                 "studio","artist","maker","workshop","design","craft","build"]}
VIBE = ["funny","humour","humor","comedy","playful","whimsy","whimsical","weird","odd",
        "quirky","silly","joy","delight","absurd","curious","curiosity","wonder","fun","laugh"]
VETO = ["crypto","forex","betting","onlyfans","weight loss","make money online",
        "day trading","dropship","sermon","tarot"]

def latest_upload(c):
    pid = "UU" + c["channel_id"][2:]
    try:
        u = f"{API}/playlistItems?{urllib.parse.urlencode({'part':'snippet','playlistId':pid,'maxResults':1,'key':KEY})}"
        with urllib.request.urlopen(u, timeout=25) as r:
            d = json.load(r)
        items = d.get("items", [])
        if items:
            c["last_upload"] = items[0]["snippet"]["publishedAt"]
            c["last_video"] = items[0]["snippet"]["title"][:160]
    except Exception as exc:
        c["last_upload"] = ""; c["upload_note"] = str(type(exc).__name__)
    return c

chans = json.load(open("channels.json"))
band = [c for c in chans if c["subscribers"] and 5_000 <= c["subscribers"] <= 1_000_000]
print(f"checking latest upload for {band and len(band)} channels ({len(band)} units)…", flush=True)
with cf.ThreadPoolExecutor(max_workers=12) as pool:
    band = list(pool.map(latest_upload, band))

scored = []
for c in band:
    stamp = c.get("last_upload", "")
    if not stamp:
        continue
    days = (NOW - datetime.fromisoformat(stamp.replace("Z", "+00:00"))).days
    c["days_since_upload"] = days
    if days > 60:                       # the runbook's active-channel filter
        continue
    hay = " ".join([c["title"], c["description"], " ".join(c["queries"]),
                    c.get("last_video", "")]).lower()
    if any(v in hay for v in VETO):
        continue
    hits = [w for wt, ws in TERRITORY.items() for w in ws if w in hay]
    terr = sum(wt for wt, ws in TERRITORY.items() for w in ws if w in hay)
    vibe = [w for w in VIBE if w in hay]
    if terr == 0:
        continue
    c.update(territory=terr, territory_hits=sorted(set(hits))[:10],
             vibe=len(vibe), vibe_hits=vibe[:8],
             rank=terr + 2*len(vibe) + (4 if c["emails_in_description"] else 0) + 2*c["hits"])
    scored.append(c)

scored.sort(key=lambda c: -c["rank"])
json.dump(scored, open("scored.json", "w"), indent=2)
print(f"\n{len(scored)} channels pass ALL filters: 5k-1M subs, uploaded in the last 60 days, on-territory")
print(f"{sum(1 for c in scored if c['emails_in_description'])} of them publish an email\n")
for c in scored[:28]:
    e = c["emails_in_description"][0] if c["emails_in_description"] else "-"
    print(f"  [{c['rank']:>3}] {c['title'][:34]:36} {c['subscribers']:>9,} {c['days_since_upload']:>3}d "
          f"{(c['country'] or '--'):3} {e[:30]:32} v{c['vibe']}")
