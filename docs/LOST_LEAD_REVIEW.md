# Track lost leads and gather honest feedback

The Business Development agent records the jobs you did not win, helps you
ask the prospect why in one short, friendly email, saves their answer, and
shows patterns once enough losses are on file.

Everything stays on this computer. The agent drafts emails but never sends
them, and nothing is recorded until you reply with the exact `CONFIRM`
phrase it shows you.

## Record a loss

Select **Business Development** in the left panel and tell the agent what
happened, or paste the email thread:

```text
We lost the Mannheim workshop job to another quote. Log the lost lead.
```

The agent gathers what the conversation already shows, asks for at most two
missing details, then proposes a record: contact, company, offer, source,
dates, whether competitors were present, concerns they raised, and whether
they left the door open. Check every field, then reply with the exact
confirmation phrase within five minutes. A plain `yes` must not save
anything.

## Ask for feedback

Ask the agent to draft the feedback email. It stays under 120 words, thanks
the prospect, and asks one open question — was it mainly price, or something
else? Copy the draft into your own email app and send it yourself. After
sending, tell the agent so it can record the date.

## Save the answer

When a reply arrives, paste it in. The agent stores the prospect's words
exactly as written and maps them to loss reasons conservatively — an
ambiguous answer stays `unknown` rather than becoming a guess. This update
also needs the exact confirmation phrase. Records can never be deleted by
the agent, only added to and updated.

## See the pattern

```text
Show me my lost leads and any patterns in why we lose.
```

The agent reads the saved records and answers plainly, for example "price
appears in 3 of 5 losses". With fewer than five records it says there is
too little data for a pattern instead of quoting misleading percentages.

## Privacy

Lost-lead records are stored unencrypted in the local n8n database. Keep
them minimal: a name, a company, what was offered, and what happened. Do
not record phone numbers, addresses, or another company's confidential
information.

## If something fails

Run the diagnose helper first. If a lost-lead tool reports that its data is
not ready, open n8n and run `13 - SETUP - Lost Lead Data` once, then try
again. See the [troubleshooting table](TROUBLESHOOTING.md).
