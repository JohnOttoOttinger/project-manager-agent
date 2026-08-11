# Claude → WordPress → Live: Automation Checklist

Work through these in order during the AI Solopreneur session. Each step is testable before moving on. No paid plugin should be needed.

## 1. Credentials (10 min, do first)
- [ ] datalabsagency.com wp-admin → Users → Profile → **Application Passwords** → create one named `content-agent`. Copy it once (shown only once).
- [ ] Same on oddtoe.com.
- [ ] Store both in the repo's `.env` (pattern already exists via `.env.example`): `WP_DATALABS_USER`, `WP_DATALABS_APP_PASSWORD`, `WP_ODDTOE_USER`, `WP_ODDTOE_APP_PASSWORD`. Never commit `.env`.

## 2. Prove the connection (5 min)
- [ ] One curl per site: `GET /wp-json/wp/v2/posts?per_page=1` with Basic auth. Expect JSON, not 401.
- [ ] Create a throwaway draft via `POST /wp-json/wp/v2/pages` with `"status":"draft"`. Confirm it appears in wp-admin → Pages → Drafts. Delete it.

## 3. Draft push (the core, ~1 hr)
- [ ] `skills/money-pages/scripts/wp-post.sh`: takes site + title + HTML body, POSTs a draft, prints the wp-admin edit link.
- [ ] Wire it so the chat agent calls it after you approve a page draft in chat.
- [ ] Reuse the app's existing exact-confirmation-phrase gate before any write.

## 4. Publish step (30 min)
- [ ] Same endpoint, `"status":"publish"` — but ONLY behind a second explicit confirmation ("publish page 123").
- [ ] Default stays draft. The agent must never publish unprompted.

## 5. Cache purge — the step everyone forgets (30 min)
- [ ] Published ≠ live: Cloudflare caches HTML ~4 h in front of WP Engine.
- [ ] Create a **scoped** Cloudflare API token (Zone → Cache Purge permission only, both zones).
- [ ] After publish, purge that page's URL: `POST /client/v4/zones/{zone}/purge_cache` with `{"files":["<page url>"]}`.
- [ ] Verify with the cache-buster pattern from the oddtoe-canonical-monitor task: `curl -s "https://<url>?cb=$(date +%s)" | grep -o '<title>[^<]*'`.

## 6. SEO fields
- [ ] Update Oddtoe's Yoast first (currently 24.5, old REST surface) via wp-admin → Plugins.
- [ ] Test whether Yoast title/meta are settable via REST on each site. If not, don't fight it: the skill prints the meta as a copy-paste block at the top of each draft and you paste it in the Yoast box during review. Revisit automation later.

## 7. End-to-end acceptance test
- [ ] In chat: "Write the Datalabs workshop pricing page" → interview → draft lands in wp-admin → you edit/approve → "publish it" in chat → page live → cache purged → curl with cache-buster shows the new page.
- [ ] When this passes once, the loop is done. Everything after is content, not plumbing.

## Fallbacks (only if REST hits a wall)
1. Automattic `wordpress-mcp` plugin (free) — MCP-native access to the same REST API.
2. Uncanny Automator / WP Webhooks (paid) — last resort; you probably won't need it.
