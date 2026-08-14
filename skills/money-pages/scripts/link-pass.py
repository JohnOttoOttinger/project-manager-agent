#!/usr/bin/env python3
"""Retrospective internal-linking pass for money pages.

Two modes:

  plan  — read-only discovery. Scans the site's published pages+posts via the
          public REST API, scores them as link-source candidates for a target
          money page, and prints the ranked candidates with the sentences
          where a link could live. The agent turns this into an edit plan
          (exact search/replace JSON) for Otto to approve.

              python3 link-pass.py plan datalabs \
                  --target 52962 --keywords workshop pricing training cost

  apply — applies an APPROVED edit-plan JSON via authenticated REST. Each
          entry is an exact-string replacement; anything that doesn't match
          exactly is skipped and reported, never guessed. Every applied link
          is appended to references/links-ledger.md.

              python3 link-pass.py apply datalabs --plan plan.json

Plan JSON format (written by the agent, approved by Otto):
  {"target": 52962,
   "edits": [{"source_id": 123, "type": "pages",
              "search": "<exact existing HTML substring>",
              "replace": "<same substring with the <a href> added>"}]}

Guardrails baked in: apply refuses a plan without "approved": true; max 5
edits per run; a source that already links to the target URL is skipped;
edits never touch pages listed in EXCLUDE_SLUGS.
"""

import argparse
import base64
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
LEDGER = Path(__file__).resolve().parents[1] / "references" / "links-ledger.md"

SITES = {"datalabs": "https://www.datalabsagency.com", "oddtoe": "https://www.oddtoe.com"}
ENV_PREFIX = {"datalabs": "WP_DATALABS", "oddtoe": "WP_ODDTOE"}

EXCLUDE_SLUGS = {"cart", "checkout", "my-account", "refund_returns", "privacy-policy",
                 "website-disclaimer", "terms", "login", "thank-you"}
MAX_EDITS_PER_RUN = 5
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) datalabs-link-pass"}


def load_env():
    env = {}
    env_file = REPO / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def req(url, auth=None, data=None, method="GET"):
    headers = dict(UA)
    if auth:
        headers["Authorization"] = "Basic " + base64.b64encode(auth.encode()).decode()
    if data is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(data).encode()
    r = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(r, timeout=60) as resp:
        return json.loads(resp.read().decode())


def fetch_all(site, kind):
    out, page = [], 1
    while True:
        url = (f"{site}/wp-json/wp/v2/{kind}?per_page=100&page={page}&status=publish"
               f"&_fields=id,link,slug,title,content")
        try:
            batch = req(url)
        except Exception as e:
            if page == 1:
                raise
            break
        if not isinstance(batch, list) or not batch:
            break
        out.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return out


def sentences_with(text, keywords):
    plain = re.sub(r"<[^>]+>", " ", text)
    plain = re.sub(r"\s+", " ", plain)
    hits = []
    for s in re.split(r"(?<=[.!?])\s+", plain):
        if any(k.lower() in s.lower() for k in keywords) and 40 < len(s) < 300:
            hits.append(s.strip())
    return hits[:3]


def cmd_plan(args):
    site = SITES[args.brand]
    target_url = args.target if str(args.target).startswith("http") else None
    target_id = None if target_url else int(args.target)

    items = [(p, "pages") for p in fetch_all(site, "pages")] + \
            [(p, "posts") for p in fetch_all(site, "posts")]
    print(f"fetched {len(items)} published pages/posts from {site}", file=sys.stderr)

    # Resolve target URL if an ID was given and the page is published
    for p, kind in items:
        if target_id and p["id"] == target_id:
            target_url = p["link"]
    if not target_url:
        print("NOTE: target not found among published items (still a draft?). "
              "Existing-link detection will use the ID only.", file=sys.stderr)

    scored = []
    for p, kind in items:
        if target_id and p["id"] == target_id:
            continue
        if p.get("slug", "") in EXCLUDE_SLUGS:
            continue
        title = re.sub(r"<[^>]+>", "", p.get("title", {}).get("rendered", ""))
        content = p.get("content", {}).get("rendered", "") or ""
        if target_url and target_url.rstrip("/") in content:
            continue  # already links to target
        score = sum(3 for k in args.keywords if k.lower() in title.lower()) + \
                sum(min(content.lower().count(k.lower()), 5) for k in args.keywords)
        if score >= args.min_score:
            scored.append((score, p["id"], kind, title, p["link"],
                           sentences_with(content, args.keywords)))

    scored.sort(reverse=True)
    print(f"\n# Link-source candidates (target: {target_url or args.target})\n")
    for score, pid, kind, title, link, snippets in scored[:args.top]:
        print(f"## [{score:>3}] {kind[:-1]} {pid} — {title}\n   {link}")
        for s in snippets:
            print(f"   · …{s}…")
        print()


def cmd_apply(args):
    site = SITES[args.brand]
    env = load_env()
    prefix = ENV_PREFIX[args.brand]
    user, pw = env.get(f"{prefix}_USER"), env.get(f"{prefix}_APP_PASSWORD")
    if not (user and pw):
        sys.exit(f"{prefix}_USER / {prefix}_APP_PASSWORD missing from repo .env")
    auth = f"{user}:{pw}"

    plan = json.loads(Path(args.plan).read_text())
    if plan.get("approved") is not True:
        sys.exit('Plan is not approved — add "approved": true after Otto signs off.')
    edits = plan.get("edits", [])[:MAX_EDITS_PER_RUN]

    applied, skipped = [], []
    for e in edits:
        kind, pid = e.get("type", "pages"), e["source_id"]
        url = f"{site}/wp-json/wp/v2/{kind}/{pid}?context=edit"
        item = req(url, auth=auth)
        raw = item["content"]["raw"]
        # Compare href-agnostically: WP plugins rewrite stored hrefs (e.g. pretty URL
        # -> /?page_id=N), so a literal `replace in raw` check misses an already-applied
        # edit and re-applying DUPLICATES the sentence (happened 14 Aug 2026).
        strip_href = lambda s: re.sub(r'href="[^"]*"', 'href=""', s)
        if strip_href(e["replace"]) in strip_href(raw):
            skipped.append((pid, "link already present"))
            continue
        if e["search"] not in raw:
            skipped.append((pid, "search text not found — page changed, re-plan"))
            continue
        new = raw.replace(e["search"], e["replace"], 1)
        req(f"{site}/wp-json/wp/v2/{kind}/{pid}", auth=auth,
            data={"content": new}, method="POST")
        applied.append((pid, item.get("link", "")))
        print(f"applied: {kind[:-1]} {pid}")

    if applied:
        with open(LEDGER, "a", encoding="utf-8") as f:
            for pid, link in applied:
                f.write(f"- {date.today()} · {args.brand} · source {pid} ({link}) → "
                        f"target {plan.get('target')}\n")
    print(f"\napplied {len(applied)}, skipped {len(skipped)}")
    for pid, why in skipped:
        print(f"  skipped {pid}: {why}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="mode", required=True)
    p = sub.add_parser("plan")
    p.add_argument("brand", choices=SITES)
    p.add_argument("--target", required=True, help="page ID or URL of the money page")
    p.add_argument("--keywords", nargs="+", required=True)
    p.add_argument("--top", type=int, default=8)
    p.add_argument("--min-score", type=int, default=3)
    p.set_defaults(func=cmd_plan)
    a = sub.add_parser("apply")
    a.add_argument("brand", choices=SITES)
    a.add_argument("--plan", required=True, help="path to approved edit-plan JSON")
    a.set_defaults(func=cmd_apply)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
