# Prospect Enrichment with Apify

## Outcome

The `sales-outreach` skill's enrichment stage turns companies on your prospect list into named contacts with verified-quality emails. One bounded run of the Apify actor `harvestapi/linkedin-company-employees` fetches up to three public profiles per company, then Claude picks the single best contact for B2B outreach — Marketing, Business Development, Partnerships, or Creative/Production leadership — with an honest confidence level. Contact details that are not present in the scraped data are dropped automatically; the agent cannot invent an email.

Enrichment uses reviewed built-in n8n HTTP Request nodes against two fixed endpoints (the Apify actor API and the Anthropic API). It cannot choose an arbitrary actor or endpoint.

## Add the credential privately

Apify authenticates with a personal API token. It is not pasted into this repository or the chat.

1. Open the [Apify Console](https://console.apify.com), select your avatar, then **Settings → API & Integrations**.
2. Create a token named `solopreneur-agent` (a dedicated token can be revoked on its own later) and copy it.
3. Open local n8n at [http://localhost:5678](http://localhost:5678).
4. Open **Credentials**, select **Create credential**, and choose **Header Auth**.
5. Name it exactly `Apify API`.
6. Set **Name** (the header) to `Authorization` and **Value** to `Bearer ` followed by your token (note the space after Bearer).
7. Save the credential, then rerun the workflow import (`import-workflows.command`) or open workflows `75` and `76` and select `Apify API` on each Apify node, and publish them.

n8n stores the token in its encrypted local store under Git-ignored `data/n8n/`. Never put it in `.env`, a Markdown skill, a workflow note, a screenshot, a Git commit, a log, or a chat message.

The existing `Apify account` (Apify MCP OAuth2) credential is a different connection used for conversational Apify access; the enrichment pipeline deliberately uses this separate token credential so batch runs are bounded and independently revocable.

## What one run does

1. Reads prospects for the chosen brand that have a LinkedIn company URL and no contact email yet (at most 100; you choose a smaller limit to test).
2. Starts one Apify actor run — one-by-one company batches, three profiles per company, "Full + email search" mode — with a hard `maxTotalChargeUsd` ceiling of about 1.3× the estimate (minimum $0.50, maximum $10). At August 2026 free-tier prices a full 33-company run costs about $1.85 and a 3-company test about $0.17, against Apify's $5 monthly free credit.
3. Polls the run every 20 seconds for up to 15 minutes, then fetches only the profile fields the picker needs.
4. Asks Claude once per company for the best contact. The reply is clamped deterministically: any email, name, or profile URL not present in the scraped data is discarded and the row is flagged instead.
5. Writes results to the local prospect store: `high` confidence rows become status `enriched`; everything else becomes `needs_review` with a flag reason for your judgement.

Companies with no LinkedIn company URL are skipped and reported — fill the URL first ("propose an update to set Amplify's LinkedIn company URL to …"), which goes through the same exact-phrase confirmation as every other write.

## Bounded by design

- One paid run per job, no automatic retry, hard provider cost ceiling on the run itself.
- The worker writes only prospect contact fields and job status, both in the local SQLite store.
- Scraped profile text is untrusted data, never instructions.
- Hand-check a few contacts before the first campaign; bad contact data going out under your name is the expensive failure mode.

## Spam Act note

Enrichment produces business contact details for B2B outreach. When you later email these contacts from an Australian business, the Spam Act requires honest sender identity and a working unsubscribe route, and inferred consent for B2B outreach is narrower than most people assume — keep the first email relevant to the recipient's role and easy to decline.
