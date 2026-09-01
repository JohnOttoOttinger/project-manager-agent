# Oddtoe Gmail MCP — setup runbook

Decided 1 Sep 2026. The claude.ai Gmail connector reaches only
`otto@datalabsagency.com` and its tools have no account switch, so
`oddtoe@oddtoe.com` gets its own MCP server. Once this is done, Oddtoe
drafting and the Oddtoe reply scan run through the API like Datalabs does,
and the browser-automation path in `bd-draft-outreach` becomes the fallback
rather than the method.

Server: `@gongrzhe/server-gmail-autoauth-mcp` — the widely used community
Gmail MCP. It authenticates once via a local OAuth flow and stores the token
in `~/.gmail-mcp/`.

## One-time setup (about 10 minutes, needs you — not Claude)

Claude cannot do steps 1–3: they mean signing into Google and approving an
OAuth consent screen, which is account security and stays human.

1. **OAuth client.** In Google Cloud Console, in the existing
   `oddtoe-analytics` project (the one whose service account reads GA4):
   - APIs & Services → Enable APIs → enable **Gmail API**.
   - Credentials → Create credentials → **OAuth client ID** → type
     **Desktop app**, name it `gmail-mcp-oddtoe`, download the JSON.
2. **Put the key where the server looks:**

       mkdir -p ~/.gmail-mcp && mv ~/Downloads/client_secret*.json ~/.gmail-mcp/gcp-oauth.keys.json

3. **Authorise as Oddtoe** (a browser window opens — pick
   `oddtoe@oddtoe.com`, not the Datalabs account):

       npx @gongrzhe/server-gmail-autoauth-mcp auth

4. **Add the server** (any terminal, then restart Claude Code):

       claude mcp add gmail-oddtoe --scope user -- npx @gongrzhe/server-gmail-autoauth-mcp

## Verify

In a new session: ask Claude to list Gmail drafts via `gmail-oddtoe` and
confirm it sees the Oddtoe mailbox (the Ham-Bag drafts are the tell), not
the Datalabs one.

## Then update the skills

`bd-draft-outreach` and `bd-reply-scan` both carry a "verified 1 Sep 2026"
mailbox section that routes Oddtoe through the browser. Once `gmail-oddtoe`
verifies, rewrite those sections: Oddtoe drafts and scans go through
`gmail-oddtoe` tools, Datalabs through the existing connector, browser only
as fallback. If the consent screen warns the app is unverified, that is
expected for a personal OAuth client — Advanced → continue.

## Note on the token

`~/.gmail-mcp/` then holds a live token for the Oddtoe mailbox. It is
outside the repo and must stay out of backups that leave this machine.
