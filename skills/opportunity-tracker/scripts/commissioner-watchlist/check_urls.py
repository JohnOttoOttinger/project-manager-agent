"""Resolve each watchlist URL before it goes on the board.

A watchlist whose links 404 is worse than no watchlist - it looks maintained
and isn't. Tries the specific opportunities path first, falls back to the
organisation's homepage, and records which one answered.
"""
import concurrent.futures as cf, json, urllib.error, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}

def probe(url):
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, headers=UA, method=method)
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.status, r.geturl()
        except urllib.error.HTTPError as e:
            if method == "GET" or e.code not in (403, 405, 501):
                return e.code, url
        except Exception as e:
            if method == "GET":
                return f"ERR {type(e).__name__}", url
    return "ERR", url

def resolve(entry):
    out = dict(entry); out["url"] = ""; out["url_status"] = ""; out["url_note"] = ""
    for i, candidate in enumerate(entry["try"]):
        status, final = probe(candidate)
        if status == 200:
            out["url"] = final
            out["url_status"] = "200"
            out["url_note"] = ("opportunities page" if i == 0 and len(entry["try"]) > 1
                               else "homepage — find the opportunities page on it")
            return out
        out["url_note"] = f"{candidate} -> {status}"
    out["url"] = entry["try"][-1]
    out["url_status"] = "UNRESOLVED"
    return out

rows = json.load(open("candidates.json"))
with cf.ThreadPoolExecutor(max_workers=12) as pool:
    resolved = list(pool.map(resolve, rows))
json.dump(resolved, open("resolved.json", "w"), indent=2)
ok = [r for r in resolved if r["url_status"] == "200"]
print(f"{len(ok)}/{len(resolved)} resolved to a live URL\n")
for r in resolved:
    flag = "  " if r["url_status"] == "200" else "!!"
    print(f"{flag} {r['n'][:44]:46} {r['url_status']:11} {r['url'][:58]}")
    if r["url_status"] != "200":
        print(f"     last tried: {r['url_note'][:100]}")
