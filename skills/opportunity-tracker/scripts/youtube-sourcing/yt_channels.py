"""Stage 2: channel detail. channels.list is 1 unit per call of up to 50 ids.

Two things the scrapers could never give: a real subscriberCount, and the full
channel description - which is where creators publish a business email in
plain text. That is a published address, not a guess.
"""
import json, os, re, time, urllib.parse, urllib.request

KEY = os.environ["YOUTUBE_API_KEY"]
API = "https://www.googleapis.com/youtube/v3"
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

def api(path, **p):
    p["key"] = KEY
    for attempt in range(3):
        try:
            with urllib.request.urlopen(f"{API}/{path}?{urllib.parse.urlencode(p)}", timeout=30) as r:
                return json.load(r)
        except Exception:
            if attempt == 2: return {}
            time.sleep(2 * (attempt + 1))

doc = json.load(open("search.json"))
by_id = {c["channel_id"]: c for c in doc["channels"]}
ids = list(by_id)
out, used = [], 0
for i in range(0, len(ids), 50):
    batch = ids[i:i+50]
    d = api("channels", part="snippet,statistics,brandingSettings",
            id=",".join(batch), maxResults=50)
    used += 1
    for it in d.get("items", []):
        sn, st = it["snippet"], it.get("statistics", {})
        desc = sn.get("description", "") or ""
        brand_desc = (it.get("brandingSettings", {}).get("channel", {}) or {}).get("description", "") or ""
        blob = desc + " " + brand_desc
        emails = [e.lower() for e in EMAIL.findall(blob)]
        seed = by_id.get(it["id"], {})
        out.append({
            "channel_id": it["id"],
            "title": sn.get("title", ""),
            "handle": sn.get("customUrl", ""),
            "country": sn.get("country", ""),
            "published_at": sn.get("publishedAt", ""),
            "description": re.sub(r"\s+", " ", blob)[:1500],
            "subscribers": int(st["subscriberCount"]) if st.get("subscriberCount") else None,
            "hidden_subs": st.get("hiddenSubscriberCount", False),
            "video_count": int(st["videoCount"]) if st.get("videoCount") else None,
            "view_count": int(st["viewCount"]) if st.get("viewCount") else None,
            "emails_in_description": list(dict.fromkeys(emails))[:3],
            "queries": seed.get("queries", []),
            "hits": seed.get("hits", 0),
        })
json.dump(out, open("channels.json", "w"), indent=2)

sized = [c for c in out if c["subscribers"]]
band = [c for c in sized if 5_000 <= c["subscribers"] <= 1_000_000]
with_mail = [c for c in out if c["emails_in_description"]]
print(f"{len(out)} channels detailed ({used} units)")
print(f"{len(band)} sit in the 5k-1M subscriber band (runbook target is 10k-500k)")
print(f"{len(with_mail)} publish an email in their channel description")
