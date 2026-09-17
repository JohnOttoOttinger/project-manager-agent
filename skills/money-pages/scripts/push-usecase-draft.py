#!/usr/bin/env python3
"""Push a composed Use Case page to oddtoe.com as a DRAFT under the Use Cases hub.

    python3 push-usecase-draft.py <composed.html> "<Title>" <url-slug>

Sets status=draft, parent=16296 (/use-cases/), template=page-custom.php, author=WP_ODDTOE_AUTHOR_ID.
Runs merge-spacers.py first, like wp-post.sh. Prints the page id and the wp-admin edit link.
Never publishes (banned.md rule 4). Page background and header style are Ronneby meta REST cannot
set: Custom bg = the JSON's TINT, header style 13, both in wp-admin after creation.
"""
from __future__ import annotations
import base64, importlib.util, json, os, sys, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent
SITE = "https://www.oddtoe.com"
HUB = 16296
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"


def load_env():
    for line in (REPO / ".env").read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1); os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def merged(body: str) -> str:
    spec = importlib.util.spec_from_file_location("m", HERE / "merge-spacers.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    try:
        new, before, after, runs = m.process(body)
        print(f"spacer merge: {before} -> {after}", file=sys.stderr); return new
    except Exception as e:
        print(f"spacer merge skipped ({e}) - pushing unmerged", file=sys.stderr); return body


def main():
    html_path, title, slug = sys.argv[1:4]
    load_env()
    auth = base64.b64encode(f"{os.environ['WP_ODDTOE_USER']}:{os.environ['WP_ODDTOE_APP_PASSWORD']}".encode()).decode()
    page = {"title": title, "slug": slug, "content": merged(Path(html_path).read_text(encoding="utf-8")),
            "status": "draft", "parent": HUB, "template": "page-custom.php"}
    if os.environ.get("WP_ODDTOE_AUTHOR_ID", "").strip():
        page["author"] = int(os.environ["WP_ODDTOE_AUTHOR_ID"])
    req = urllib.request.Request(f"{SITE}/wp-json/wp/v2/pages", data=json.dumps(page).encode(), method="POST",
                                 headers={"Authorization": "Basic " + auth, "User-Agent": UA, "Content-Type": "application/json"})
    d = json.load(urllib.request.urlopen(req))
    assert d["status"] == "draft", d["status"]
    print(f"Draft created: {title}  (id {d['id']}, slug {d['slug']}, parent {d['parent']}, template {d.get('template')})")
    print(f"Review: {SITE}/wp-admin/post.php?post={d['id']}&action=edit")
    print(f"Preview: {SITE}/?page_id={d['id']}&preview=true")


if __name__ == "__main__":
    main()
