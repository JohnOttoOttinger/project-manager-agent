"""Crawl each agency site for a fit signal AND a published contact address.

Free, local, and the same shape as the podcast RSS pass: read what the
organisation publishes about itself rather than inferring. Homepage first,
then /contact, for a mailto: or a plain address in the markup.
"""
import concurrent.futures as cf, json, re, urllib.error, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
      "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
      "Accept-Language": "en-AU,en;q=0.9", "Accept-Encoding": "identity"}
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
# Addresses that are never a business contact.
JUNK = re.compile(r"(sentry|wixpress|example\.|\.png|\.jpg|\.gif|\.webp|\.svg|"
                  r"godaddy|squarespace|@2x|core-js|sentry\.io|u003e)", re.I)
CAP = 220_000

def get(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=18) as r:
            ct = r.headers.get("Content-Type", "")
            if "html" not in ct and "text" not in ct:
                return ""
            return r.read(CAP).decode("utf-8", "ignore")
    except Exception:
        return ""

def tag(html, name):
    m = re.search(rf'<meta[^>]+name=["\']{name}["\'][^>]+content=["\']([^"\']*)', html, re.I)
    if m: return m.group(1)
    m = re.search(rf'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']{name}["\']', html, re.I)
    return m.group(1) if m else ""

def emails_from(html, domain):
    found = []
    for m in re.findall(r'mailto:([^"\'?>\s]+)', html) + EMAIL.findall(html):
        e = m.strip().lower().rstrip(".,;:")
        if JUNK.search(e) or len(e) > 80 or e in found:
            continue
        found.append(e)
    # Prefer an address on the company's own domain.
    own = [e for e in found if domain and e.endswith("@" + domain)]
    return (own or found)[:4]

def crawl(row):
    out = dict(row); out.update(site_title="", site_desc="", emails=[], crawl_note="")
    site = row["website"]
    if not site:
        out["crawl_note"] = "no website"; return out
    domain = re.sub(r"^https?://(www\.)?", "", site.lower()).split("/")[0]
    html = get(site)
    if not html:
        out["crawl_note"] = "homepage unreachable"; return out
    out["site_title"] = re.sub(r"\s+", " ", (re.search(r"<title[^>]*>(.*?)</title>", html, re.S|re.I) or
                        re.match(r"()", "")).group(1) if re.search(r"<title", html, re.I) else "").strip()[:200]
    out["site_desc"] = re.sub(r"\s+", " ", tag(html, "description"))[:400]
    found = emails_from(html, domain)
    if not found:
        for path in ("/contact", "/contact-us", "/contact/"):
            page = get(site.rstrip("/") + path)
            if page:
                found = emails_from(page, domain)
                if found: break
    out["emails"] = found
    # Keep a compressed text sample for the fit scorer.
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", html, flags=re.S|re.I)
    out["sample"] = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text))[:2500]
    return out

rows = json.load(open("raw.json"))
print(f"crawling {len(rows)} sites…", flush=True)
with cf.ThreadPoolExecutor(max_workers=14) as pool:
    done = list(pool.map(crawl, rows))
json.dump(done, open("crawled.json", "w"), indent=2)
ok = [d for d in done if not d["crawl_note"]]
mail = [d for d in done if d["emails"]]
print(f"{len(ok)}/{len(rows)} sites read; {len(mail)} published an email")
