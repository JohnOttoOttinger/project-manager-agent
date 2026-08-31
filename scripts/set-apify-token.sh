#!/usr/bin/env bash
# Reads the Apify token from the clipboard and writes it into .env, then
# restarts the app. The token is never printed, never typed, and never lands
# in shell history.
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${PROJECT_ROOT}/.env"

say() { printf '%s\n' "$1"; }
fail() { printf '\n❌ %s\n\n' "$1"; printf 'Nothing was changed. Fix that and run this again.\n'; exit 1; }

say ""
say "Setting your Apify token"
say "────────────────────────"

# Trim only the edges: copying often picks up a trailing newline, but a space
# in the MIDDLE means the wrong thing was copied and must not be glued shut.
TOKEN="$(pbpaste 2>/dev/null || true)"
TOKEN="$(printf '%s' "$TOKEN" | tr -d '\r\n' | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"

[ -n "$TOKEN" ] && [ -e "$ENV_FILE" ] || {
  [ -n "$TOKEN" ] || fail "Your clipboard is empty. Copy the token from Apify first, then run this again."
  fail "Could not find the settings file at ${ENV_FILE}."
}

case "$TOKEN" in
  PASTE_HERE*) fail "Your clipboard still says PASTE_HERE. Copy the real token from Apify." ;;
  *" "*)       fail "That does not look like a token — it has spaces in it." ;;
esac

if [ "${#TOKEN}" -lt 20 ]; then
  fail "That looks too short to be an Apify token (${#TOKEN} characters). Did you copy the whole thing?"
fi

# One entry only: drop any previous lines before adding the new one.
TMP="$(mktemp)"
grep -v '^APIFY_TOKEN=' "$ENV_FILE" > "$TMP" || true
[ -s "$TMP" ] && [ "$(tail -c1 "$TMP" | wc -l)" -eq 0 ] && printf '\n' >> "$TMP"
printf 'APIFY_TOKEN=%s\n' "$TOKEN" >> "$TMP"
cat "$TMP" > "$ENV_FILE"
rm -f "$TMP"

say "✅ Token saved (${#TOKEN} characters, starts \"$(printf '%s' "$TOKEN" | cut -c1-6)…\")."
say ""
say "Restarting the app — this takes a minute or two…"
"${PROJECT_ROOT}/stop.command" >/dev/null 2>&1 || true
"${PROJECT_ROOT}/start.command" || fail "The app did not restart cleanly. Run ./start.command yourself to see why."

say ""
if curl -fsS --max-time 8 "http://localhost:3000/api/enrichment/quote?brand=oddtoe" 2>/dev/null | grep -q '"configured":true'; then
  say "✅ Done. The app can see your token — the Run enrichment button is live."
else
  say "⚠  Saved, but the app is not reporting the token yet. Tell Claude and it will check."
fi
say ""
