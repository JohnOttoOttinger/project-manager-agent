"""Stage 2: read each show's RSS feed for the published contact + evidence.

Podcast feeds carry <itunes:owner><itunes:email> — a real, published address,
not a guessed pattern. Also grabs the show site, author, description and the
most recent episode titles, which are what the relevance scoring reads.
Caps each read at 400KB: channel metadata and newest episodes come first.
"""
import json, re, socket, urllib.request
from concurrent.futures import ThreadPoolExecutor
from xml.etree import ElementTree as ET

ITUNES = "{http://www.itunes.com/dtds/podcast-1.0.dtd}"
CAP = 400_000
UA = {"User-Agent": "Mozilla/5.0 (compatible; OddtoePressResearch/1.0)"}
socket.setdefaulttimeout(25)


def text(node):
    return (node.text or "").strip() if node is not None else ""


def fetch(show):
    out = dict(show)
    out.update(email="", website="", author="", summary="",
               recent_episodes=[], fetch_error="")
    url = show.get("feed_url") or ""
    if not url.startswith("http"):
        out["fetch_error"] = "no feed url"
        return out
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=25) as r:
            raw = r.read(CAP)
    except Exception as exc:
        out["fetch_error"] = f"{type(exc).__name__}: {exc}"[:160]
        return out
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:                       # truncated mid-element: close it
        try:
            root = ET.fromstring(raw[:raw.rfind(b"<item>")] + b"</channel></rss>")
        except Exception as exc:
            out["fetch_error"] = f"parse: {exc}"[:160]
            return out
    ch = root.find("channel")
    if ch is None:
        out["fetch_error"] = "no channel element"
        return out

    owner = ch.find(f"{ITUNES}owner")
    email = text(owner.find(f"{ITUNES}email")) if owner is not None else ""
    if not email:
        managing = text(ch.find("managingEditor"))
        hit = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", managing)
        email = hit.group(0) if hit else ""
    out["email"] = email.lower()
    out["website"] = text(ch.find("link"))
    out["author"] = text(ch.find(f"{ITUNES}author"))
    summary = text(ch.find(f"{ITUNES}summary")) or text(ch.find("description"))
    out["summary"] = re.sub(r"<[^>]+>", " ", summary)[:900].strip()
    eps = []
    for item in ch.findall("item")[:12]:
        eps.append({"title": text(item.find("title"))[:200],
                    "date": text(item.find("pubDate"))[:31],
                    "link": text(item.find("link"))[:300]})
    out["recent_episodes"] = eps
    return out


doc = json.load(open("candidates.json"))
shows = doc["shows"]
print(f"fetching {len(shows)} feeds…", flush=True)
with ThreadPoolExecutor(max_workers=16) as pool:
    enriched = list(pool.map(fetch, shows))

ok = [s for s in enriched if not s["fetch_error"]]
with_email = [s for s in ok if s["email"]]
doc["shows"] = enriched
doc["feeds_read"] = len(ok)
doc["with_published_email"] = len(with_email)
json.dump(doc, open("enriched.json", "w"), indent=2)
print(f"read {len(ok)}/{len(shows)} feeds; {len(with_email)} publish an email")
