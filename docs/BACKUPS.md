# Backups

Set up 1 Sep 2026, after noticing the last manual backup was 6 August. The
design assumption is that Otto will not run a backup command, so anything
requiring him to remember one is not a backup strategy.

## What runs by itself

A launchd agent, `com.oddtoe.board-backup`, runs `scripts/backup-board.mjs`
every two hours and once at load. It survives closing the terminal, survives
reboots, and catches up after sleep. Nothing has to be open.

    launchctl list | grep board-backup     # second column is the last exit code
    ~/Library/LaunchAgents/com.oddtoe.board-backup.plist

**It does not stop anything.** `npm run backup` stops chat and n8n to get a
consistent copy — correct by hand, unusable every two hours. This uses
`VACUUM INTO`, which snapshots a live SQLite database atomically without a
write lock, so it can run mid-session.

**It verifies.** Every snapshot is reopened, `PRAGMA integrity_check` run, and
the row count compared against the live store. A backup nobody has opened is a
rumour. A failure exits non-zero and writes to the log rather than passing
silently.

**It skips unchanged stores.** n8n's database is 20MB and only moves when a
workflow runs; copying it every two hours would push ~240MB/day of identical
bytes through iCloud. If the source has not changed since the newest snapshot,
it is skipped.

## Where things go, and why they go to different places

| What | Where | Why |
| --- | --- | --- |
| `data/chat/chat.sqlite` — the board, prospects, conversations | **iCloud Drive** → `Oddtoe Agent Backups/` | Changes constantly, painful to lose, survives the Mac dying |
| `data/n8n/.n8n/database.sqlite` — workflows | **iCloud Drive**, same folder | Same, but changes rarely |
| `.env` — WordPress app passwords, Apify token, YouTube key, Gravity Forms secret | **local only** → `backups/secrets/` | Credentials. See below |
| `data/n8n/.n8n/config` — the n8n encryption key | **local only** → `backups/secrets/` | Same |

Retention is the newest 48 snapshots per store, so roughly four days of board
history at the two-hour cadence.

### Why secrets are not in iCloud

Putting `.env` in iCloud uploads WordPress admin passwords and live API tokens
to Apple's servers and syncs them to every device on the Apple ID. That is a
worse trade than the disk-loss risk it covers, so the script deliberately keeps
them out of `--dest`.

**That leaves one real gap**, and it needs a human decision rather than a
script: if this Mac dies, `backups/secrets/` dies with it. Most of those
credentials are regenerable — WordPress app passwords, the Apify token, the
YouTube key can all be reissued. **The n8n encryption key cannot.** Without it
the n8n credential store is undecryptable and every credential has to be
re-entered by hand.

It is 56 bytes and changes almost never. **Save it once into 1Password**:

    cat data/n8n/.n8n/config

That is a one-time action, not a habit, which is why it is the recommendation
rather than a scheduled job.

## Running it by hand

    npm run backup-board                    # to the configured destination
    npm run backup-board -- --dest /tmp/x    # somewhere else
    npm run backup-board -- --keep 12        # different retention

The log is `backups/backup.log`, kept local rather than in the synced
destination: iCloud applies file coordination to appends and two runs landing
together can lose one. launchd stderr goes to `backups/launchd.err.log`.

## Installing the agent on another Mac

    npm run backup-agent                       # install and load
    npm run backup-agent -- --status           # check it
    npm run backup-agent -- --dest /some/dir    # different destination
    npm run backup-agent -- --interval 3600     # different cadence
    npm run backup-agent -- --uninstall        # remove, snapshots kept

The plist is generated rather than committed: it holds absolute paths to this
checkout and to the private Node runtime, both of which differ per machine.
Re-running the installer is how you change the schedule.

## Restoring

Stop the app, copy the snapshot over the live file, start again:

    npm run stop
    cp "<snapshot>.sqlite" data/chat/chat.sqlite
    npm run start

## What this does not cover

`npm run backup` still exists and is the only thing that also archives the n8n
data directory wholesale alongside `.env`. It is no longer needed on a
schedule, but it remains the right command before anything destructive — a
migration, a reset, a version upgrade.
