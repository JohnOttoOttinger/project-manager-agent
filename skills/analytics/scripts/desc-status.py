#!/usr/bin/env python3
"""Live status of meta descriptions across a site. Ground truth, not bookkeeping.

Fetches every sitemap URL with a cache-buster (WP Engine serves a 600s page
cache that will otherwise show stale <meta> tags) and reports which pages still
have no description, grouped by language and page type.

  python3 desc-status.py --brand datalabs
  python3 desc-status.py --brand datalabs --lang de --json out.json
"""
import argparse, concurrent.futures as cf, html, json, random, re, sys, urllib.parse, urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36"
SITEMAPS = {
    "datalabs": "https://www.datalabsagency.com/sitemap_index.xml",
    "oddtoe":   "https://www.oddtoe.com/sitemap_index.xml",
}
UTILITY = re.compile(
    r"/(cart|checkout|my-account|footer|fusszeile|tez?yil|"
    r"[\w-]*dashboard[\w-]*|submit-[\w-]*form|[\w-]*formular[\w-]*)/|/our-work/\d+/"
)


def get(url, timeout=45):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", "ignore")


def sitemap_urls(index):
    urls, seen = [], set()
    for sm in re.findall(r"<loc>(.*?)</loc>", get(index)):
        if not sm.endswith(".xml"):
            continue
        try:
            for u in re.findall(r"<loc>(.*?)</loc>", get(sm)):
                if u not in seen:
                    seen.add(u)
                    urls.append(html.unescape(u))
        except Exception as e:
            print(f"  ! {sm}: {e}", file=sys.stderr)
    return urls


def lang_of(path):
    return "de" if path.startswith("/de/") else "ar" if path.startswith("/ar/") else "en"


def check(url):
    bust = url + ("&" if "?" in url else "?") + f"cb={random.randint(10**6, 10**7)}"
    path = urllib.parse.unquote(urllib.parse.urlparse(url).path)
    row = {"url": url, "lang": lang_of(urllib.parse.urlparse(url).path),
           "utility": bool(UTILITY.search(path)), "desc": None, "error": None}
    try:
        h = get(bust)
    except Exception as e:
        row["error"] = str(e)[:60]
        return row
    m = re.search(r'<meta name="description" content="(.*?)"\s*/?>', h, re.S)
    row["desc"] = html.unescape(m.group(1)).strip() if m else None
    r = re.search(r'<meta name="robots" content="([^"]*)"', h)
    row["noindex"] = bool(r and "noindex" in r.group(1))
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brand", default="datalabs", choices=SITEMAPS)
    ap.add_argument("--lang", choices=["en", "de", "ar"])
    ap.add_argument("--json")
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()

    urls = sitemap_urls(SITEMAPS[a.brand])
    if a.lang:
        urls = [u for u in urls if lang_of(urllib.parse.urlparse(u).path) == a.lang]
    print(f"checking {len(urls)} URLs ...", file=sys.stderr)

    rows = []
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for i, r in enumerate(ex.map(check, urls), 1):
            rows.append(r)
            if i % 50 == 0:
                print(f"  {i}/{len(urls)}", file=sys.stderr)

    print(f"\n{'lang':5} {'have':>5} {'missing':>8} {'  (of which utility)':>21}")
    for L in ["en", "de", "ar"]:
        g = [r for r in rows if r["lang"] == L and not r["error"]]
        if not g:
            continue
        miss = [r for r in g if not r["desc"] and not r["noindex"]]
        util = [r for r in miss if r["utility"]]
        print(f"{L:5} {len(g)-len(miss):>5} {len(miss):>8} {len(util):>21}")

    errs = [r for r in rows if r["error"]]
    if errs:
        print(f"\n{len(errs)} fetch errors")
    for L in ["en", "de", "ar"]:
        miss = [r for r in rows if r["lang"] == L and not r["error"]
                and not r["desc"] and not r["noindex"]]
        if not miss:
            continue
        print(f"\n--- {L.upper()} still missing ({len(miss)}) ---")
        for r in sorted(miss, key=lambda x: x["utility"]):
            tag = "util " if r["utility"] else "     "
            print(f"  {tag}{urllib.parse.unquote(urllib.parse.urlparse(r['url']).path)}")

    if a.json:
        json.dump(rows, open(a.json, "w"), indent=1, ensure_ascii=False)
        print(f"\nwrote {a.json}")


if __name__ == "__main__":
    main()
