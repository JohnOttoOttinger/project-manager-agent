#!/usr/bin/env python3
"""Bulk-set Yoast meta descriptions over REST.

Depends on the TEMPORARY WPCode snippet that registers Yoast's meta keys for
REST (added 18 Aug 2026). Delete that snippet when the pass is done, after which
this script stops working — by design.

Dry run by default. Pass --apply to write.
"""
import argparse, base64, json, os, re, sys, urllib.error, urllib.parse, urllib.request

SITES = {
    "datalabs": ("https://www.datalabsagency.com", "WP_DATALABS_USER", "WP_DATALABS_APP_PASSWORD"),
    "oddtoe":   ("https://www.oddtoe.com",         "WP_ODDTOE_USER",   "WP_ODDTOE_APP_PASSWORD"),
}
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/126 Safari/537.36"
DESC_KEY = "_yoast_wpseo_metadesc"
NOINDEX_KEY = "_yoast_wpseo_meta-robots-noindex"


def load_env(path=".env"):
    if not os.path.exists(path):
        return
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def call(base, auth, path, payload=None, method=None):
    url = base + path
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method or ("POST" if data else "GET"))
    req.add_header("Authorization", "Basic " + base64.b64encode(auth.encode()).decode())
    req.add_header("User-Agent", UA)
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        raw = urllib.request.urlopen(req, timeout=45).read()
        try:
            return json.loads(raw)
        except ValueError:
            raise RuntimeError(f"non-JSON response on {path}: {raw[:200]!r}") from None
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} on {path}: {e.read()[:300].decode('utf-8','ignore')}") from None


def resolve(base, auth, url):
    """Find (route, id) for a public URL by trying each post type's slug lookup."""
    path = urllib.parse.urlparse(url).path.rstrip("/")
    slug = urllib.parse.unquote(path.rsplit("/", 1)[-1])
    # WPML filters REST queries to the default language unless lang= is passed.
    seg = path.lstrip("/").split("/", 1)[0]
    lang = f"&lang={seg}" if seg in ("de", "ar") else ""
    for route in ("pages", "posts", "product", "my-product", "portfolio"):
        try:
            hits = call(base, auth,
                        f"/wp-json/wp/v2/{route}?slug={urllib.parse.quote(slug)}"
                        f"{lang}&_fields=id,link,type")
        except RuntimeError:
            continue
        for h in hits:
            if urllib.parse.urlparse(h["link"]).path.rstrip("/") == path:
                return route, h["id"]
    return None, None


ROUTE = {"page": "pages", "post": "posts", "product": "product",
         "my-product": "my-product", "portfolio": "portfolio"}


def live_description(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
    except Exception as e:
        return f"<fetch failed: {e}>"
    m = re.search(r'<meta name="description" content="(.*?)"\s*/?>', html, re.S)
    return m.group(1) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan", help="JSON file: [{url, description}, ...]")
    ap.add_argument("--brand", default="datalabs", choices=SITES)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--noindex", action="store_true",
                    help="plan is a list of URLs; set noindex,follow on each")
    a = ap.parse_args()

    load_env()
    base, uk, pk = SITES[a.brand]
    auth = f"{os.environ[uk]}:{os.environ[pk]}"
    plan = json.load(open(a.plan, encoding="utf-8"))

    ok = skipped = failed = 0

    if a.noindex:
        for url in plan:
            route, pid = resolve(base, auth, url)
            if not pid:
                print(f"FAIL  could not resolve  {url}", flush=True)
                failed += 1
                continue
            if not a.apply:
                print(f"DRY   {route}/{pid}  {url}", flush=True)
                ok += 1
                continue
            try:
                call(base, auth, f"/wp-json/wp/v2/{route}/{pid}", {"meta": {NOINDEX_KEY: "1"}})
                got = call(base, auth, f"/wp-json/wp/v2/{route}/{pid}?context=edit&_fields=meta")
            except RuntimeError as e:
                print(f"FAIL  {route}/{pid}  {url}\n      {e}", flush=True)
                failed += 1
                continue
            if got.get("meta", {}).get(NOINDEX_KEY) == "1":
                print(f"OK    {route}/{pid}  noindex  {url}", flush=True)
                ok += 1
            else:
                print(f"FAIL  readback not 1     {url}", flush=True)
                failed += 1
        print(f"\n{'applied' if a.apply else 'dry run'}: {ok} ok, {failed} failed")
        return 1 if failed else 0

    for item in plan:
        url, desc = item["url"], item["description"]
        if len(desc) > 160:
            print(f"SKIP  {len(desc):3}c too long  {url}")
            skipped += 1
            continue
        route, pid = resolve(base, auth, url)
        if not pid:
            print(f"FAIL  could not resolve  {url}")
            failed += 1
            continue
        existing = live_description(url)
        if existing:
            print(f"SKIP  already has one    {url}\n      -> {existing[:80]}")
            skipped += 1
            continue
        if not a.apply:
            print(f"DRY   {route}/{pid} {len(desc):3}c  {url}")
            ok += 1
            continue
        call(base, auth, f"/wp-json/wp/v2/{route}/{pid}", {"meta": {DESC_KEY: desc}})
        got = call(base, auth, f"/wp-json/wp/v2/{route}/{pid}?context=edit&_fields=meta")
        stored = got.get("meta", {}).get(DESC_KEY, "")
        if stored.strip() == desc.strip():
            print(f"OK    {route}/{pid} {len(desc):3}c  {url}", flush=True)
            ok += 1
        else:
            print(f"FAIL  wrote but readback differs  {url}\n      got: {stored[:90]!r}")
            failed += 1

    print(f"\n{'applied' if a.apply else 'dry run'}: {ok} ok, {skipped} skipped, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
