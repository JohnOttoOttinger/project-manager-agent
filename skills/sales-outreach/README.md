# Sales Outreach Pipeline (optional skill)

Give the agent a local prospect list it can actually keep. Attach or paste a CSV of companies, confirm the import with an exact phrase, and from then on "how's outreach going?" gets a real answer with counts by stage.

Best for: agency and venue prospect lists, and any outbound campaign you run in batches.

This is Phase 1 of the sales pipeline: import and reporting. Enrichment, campaign drafting, open tracking, and follow-ups are later phases — the skill knows the lifecycle but will tell you honestly which stages are not built yet.

## Before you start

The prospect list is saved in the same local database as your chats. Columns follow the outreach workplan: Company, Region, Tier, Source, Website, Contact Name, Contact Email, LinkedIn URL, PDF Sent, Sent Date, Opened, Follow-up Sent, Status, Notes. Company is the only required column.

## Turn it on

1. Open `skills/enabled.txt` and add this line at the end:

   ```text
   sales-outreach
   ```

2. Save the file. Do not change any other line in it.
3. Make sure the local app is running, then sync:
   - macOS: double-click `sync-skills.command`.
   - Windows: double-click `sync-skills-windows.cmd`.

## Try it

1. Pick the Sales agent and your brand.
2. Attach your prospect CSV and ask: "Import this as my agency list."
3. Reply with the exact confirmation phrase the agent gives you.
4. Ask: "Show me the pipeline."
