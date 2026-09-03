# Routine prompts - the source of truth

The four cloud routines at claude.ai/code/routines hold their own copy of these prompts, and
nothing syncs them. Before 3 Sep 2026 there was no copy in the repo at all, so what was actually
running each day was invisible to this project and had no version history.

**These files are the source of truth. After editing one, paste it into the matching routine.**

| File | Routine | Trigger | Cron (UTC) |
|---|---|---|---|
| `scout-oddtoe.md` | Oddtoe money page scout | `trig_01VWVM4TBJVa8DgjeU5bajCz` | `0 6 * * *` |
| `scout-datalabs.md` | Datalabs money page scout | `trig_01VxZgGuEdLSeYTQJ2oFcQus` | `0 6 * * *` |
| `builder-oddtoe.md` | Oddtoe money page builder | `trig_016TFL4AeXTT2Ak3AK8mE9Lr` | `0 19 * * *` |
| `builder-datalabs.md` | Datalabs money page builder | `trig_01A9etKicfxjFnHJNiRFWGCA` | `0 19 * * *` |

Environment `env_015TabFYTnKaAZq1GAAjSggY`, model sonnet-5, repo
`JohnOttoOttinger/project-manager-agent`, Gmail MCP attached.

**The email subject prefix is the brand router.** Each builder matches its own scout's prefix and
no other. Changing a subject line silently breaks the pairing.

**Crons are UTC and do not follow daylight saving.** When AEDT starts in October these run an hour
later in local time - shift both crons back one hour to hold 4pm/5am.
