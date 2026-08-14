#!/bin/bash
# Push a page to WordPress as a DRAFT and print the wp-admin edit link.
# Usage: wp-post.sh <datalabs|oddtoe> "<Page Title>" <path-to-html-body-file>
# Requires in the repo .env: WP_DATALABS_USER, WP_DATALABS_APP_PASSWORD,
#                            WP_ODDTOE_USER,   WP_ODDTOE_APP_PASSWORD
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/../../.." && pwd)"
[ -f "$REPO_DIR/.env" ] && set -a && source "$REPO_DIR/.env" && set +a

BRAND="${1:?brand required: datalabs|oddtoe}"
TITLE="${2:?page title required}"
BODY_FILE="${3:?path to html body file required}"
[ -f "$BODY_FILE" ] || { echo "Body file not found: $BODY_FILE" >&2; exit 1; }

case "$BRAND" in
  datalabs) SITE="https://www.datalabsagency.com"; USER="${WP_DATALABS_USER:?WP_DATALABS_USER missing from .env}"; PASS="${WP_DATALABS_APP_PASSWORD:?WP_DATALABS_APP_PASSWORD missing from .env}"; AUTHOR_ID="${WP_DATALABS_AUTHOR_ID:-}";;
  oddtoe)   SITE="https://www.oddtoe.com";        USER="${WP_ODDTOE_USER:?WP_ODDTOE_USER missing from .env}";   PASS="${WP_ODDTOE_APP_PASSWORD:?WP_ODDTOE_APP_PASSWORD missing from .env}"; AUTHOR_ID="${WP_ODDTOE_AUTHOR_ID:-}";;
  *) echo "Unknown brand: $BRAND (use datalabs|oddtoe)" >&2; exit 1;;
esac

# Public byline belongs to the human/brand author, never the agent user.
PAYLOAD="$(python3 - "$TITLE" "$BODY_FILE" "$AUTHOR_ID" <<'PY'
import json, sys
page = {"title": sys.argv[1],
        "content": open(sys.argv[2], encoding="utf-8").read(),
        "status": "draft",
        # Design-kit pages need the Ronneby full-width template (no theme title band).
        # NOTE: the dark page background is Ronneby post meta REST can't set —
        # crum_page_custom_bg_color=#2f2e3a + dfd_headers_header_style=2 must be
        # set in the page's wp-admin settings after creation (see SKILL.md).
        "template": "page-custom.php"}
if len(sys.argv) > 3 and sys.argv[3].strip():
    page["author"] = int(sys.argv[3])
print(json.dumps(page))
PY
)"

# Browser-like UA required: Cloudflare/WP Engine WAF 403s generic client UAs on POST (seen 14 Aug 2026)
RESPONSE="$(curl -sf -u "$USER:$PASS" -H "Content-Type: application/json" \
  -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -d "$PAYLOAD" "$SITE/wp-json/wp/v2/pages")" || { echo "WordPress API call failed for $SITE" >&2; exit 1; }

PAGE_ID="$(printf '%s' "$RESPONSE" | python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])')"
echo "Draft created: $TITLE"
echo "Review & publish: $SITE/wp-admin/post.php?post=$PAGE_ID&action=edit"
