#!/bin/bash
# Push a BLOG POST to WordPress as a DRAFT and print the wp-admin edit link.
# Sibling of wp-post.sh, which handles pages. Posts need categories and a featured image,
# and they do NOT take the page-custom.php template.
#
# Usage: wp-post-blog.sh <datalabs|oddtoe> "<Post Title>" <slug> <body-file> <category-id> <featured-media-id> ["<excerpt>"]
#
# NOTE (14 Sep 2026): posting a large body through python-urllib gets a 403 HTML page from the
# host firewall. curl with a browser User-Agent goes through, which is why this mirrors wp-post.sh.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/../../.." && pwd)"
[ -f "$REPO_DIR/.env" ] && set -a && source "$REPO_DIR/.env" && set +a

BRAND="${1:?brand required: datalabs|oddtoe}"
TITLE="${2:?post title required}"
SLUG="${3:?slug required}"
BODY_FILE="${4:?path to html body file required}"
CATEGORY="${5:?category id required}"
FEATURED="${6:?featured media id required}"
EXCERPT="${7:-}"
[ -f "$BODY_FILE" ] || { echo "Body file not found: $BODY_FILE" >&2; exit 1; }

case "$BRAND" in
  datalabs) SITE="https://www.datalabsagency.com"; USER="${WP_DATALABS_USER:?}"; PASS="${WP_DATALABS_APP_PASSWORD:?}";;
  oddtoe)   SITE="https://www.oddtoe.com";        USER="${WP_ODDTOE_USER:?}";   PASS="${WP_ODDTOE_APP_PASSWORD:?}";;
  *) echo "Unknown brand: $BRAND" >&2; exit 1;;
esac

PAYLOAD_FILE="$(mktemp)"
python3 - "$TITLE" "$SLUG" "$BODY_FILE" "$CATEGORY" "$FEATURED" "$EXCERPT" > "$PAYLOAD_FILE" <<'PY'
import json, sys
title, slug, body_file, cat, featured, excerpt = sys.argv[1:7]
body = open(body_file, encoding="utf-8").read()
assert "<!--" not in body, "strip HTML comments before pushing"
assert "{{" not in body, "unfilled token left in body"
post = {"title": title, "slug": slug, "content": body, "status": "draft",
        "categories": [int(cat)], "featured_media": int(featured)}
if excerpt.strip():
    post["excerpt"] = excerpt
print(json.dumps(post))
PY

RESPONSE="$(curl -sf -u "$USER:$PASS" -H "Content-Type: application/json" \
  -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  --data-binary @"$PAYLOAD_FILE" "$SITE/wp-json/wp/v2/posts")" \
  || { echo "WordPress API call failed for $SITE" >&2; rm -f "$PAYLOAD_FILE"; exit 1; }
rm -f "$PAYLOAD_FILE"

POST_ID="$(printf '%s' "$RESPONSE" | python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])')"
echo "Draft post created: $TITLE"
echo "Review & publish: $SITE/wp-admin/post.php?post=$POST_ID&action=edit"
