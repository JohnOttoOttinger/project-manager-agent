// Hot backup of the board and the n8n store. Safe to run on a schedule while
// both are up: `npm run backup` stops chat and n8n for consistency, which is
// fine by hand and unacceptable every two hours. `VACUUM INTO` takes a
// consistent snapshot of a live SQLite database without stopping anything, so
// this replaces the manual command for everything except secrets.
//
//   node scripts/backup-board.mjs [--keep N] [--quiet] [--dest DIR]
//
// --dest defaults to $BOARD_BACKUP_DEST, then backups/board. Secrets (.env and
// the n8n encryption key) are deliberately NOT written to --dest: that path is
// a cloud-synced folder, and credentials do not belong there. They go to
// backups/secrets locally instead. See docs/BACKUPS.md.
//
// Writes backups/board/chat-YYYYMMDD-HHMMSS.sqlite, verifies the copy opens
// and holds the same prospect count, prunes to the newest N, and appends one
// line to backups/board/backup.log. Exits non-zero if anything fails, so a
// scheduler can surface it.

import { DatabaseSync } from "node:sqlite";
import { mkdirSync, readdirSync, statSync, unlinkSync, chmodSync, appendFileSync, existsSync, copyFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");

const args = process.argv.slice(2);
const keep = Math.max(2, Number(args[args.indexOf("--keep") + 1]) || 48);
const quiet = args.includes("--quiet");
const destArg = args.includes("--dest") ? args[args.indexOf("--dest") + 1] : "";
const outDir = destArg || process.env.BOARD_BACKUP_DEST
  || join(root, "backups", "board");
const secretsDir = join(root, "backups", "secrets");
const logPath = join(outDir, "backup.log");

// Every live SQLite store worth losing sleep over.
const SOURCES = [
  { name: "chat", path: join(root, "data", "chat", "chat.sqlite"),
    countSql: "SELECT COUNT(*) AS n FROM prospects", unit: "prospects" },
  { name: "n8n", path: join(root, "data", "n8n", ".n8n", "database.sqlite"),
    countSql: "SELECT COUNT(*) AS n FROM sqlite_master", unit: "objects" },
];

// Credentials. Copied locally only — never into a synced destination.
const SECRETS = [
  { from: join(root, ".env"), to: "env.backup" },
  { from: join(root, "data", "n8n", ".n8n", "config"), to: "n8n-config.backup" },
];
const say = (line) => { if (!quiet) console.log(line); };

function stamp(date) {
  const p = (n) => String(n).padStart(2, "0");
  return `${date.getFullYear()}${p(date.getMonth() + 1)}${p(date.getDate())}-`
    + `${p(date.getHours())}${p(date.getMinutes())}${p(date.getSeconds())}`;
}

function log(line) {
  try {
    appendFileSync(logPath, `${new Date().toISOString()} ${line}\n`);
  } catch {
    // A backup that cannot write its log still counts as a backup.
  }
}

function fail(message, error) {
  const detail = error ? ` — ${error.message}` : "";
  console.error(`board backup FAILED: ${message}${detail}`);
  log(`FAILED ${message}${detail}`);
  process.exit(1);
}

mkdirSync(outDir, { recursive: true, mode: 0o700 });

const when = stamp(new Date());
let backedUp = 0;

for (const src of SOURCES) {
  if (!existsSync(src.path)) {
    say(`skipped ${src.name} — not present at ${src.path}`);
    log(`skipped ${src.name} (absent)`);
    continue;
  }
  // n8n's store is 20MB and changes only when a workflow runs. Re-copying an
  // unchanged file every two hours would push ~240MB/day of identical bytes
  // through iCloud for nothing, so skip when the source has not moved.
  try {
    const sourceAt = statSync(src.path).mtimeMs;
    const newest = readdirSync(outDir)
      .filter((name) => name.startsWith(`${src.name}-`) && name.endsWith(".sqlite"))
      .map((name) => statSync(join(outDir, name)).mtimeMs)
      .sort((a, b) => b - a)[0];
    if (newest !== undefined && sourceAt <= newest) {
      say(`${src.name}: unchanged since the last snapshot, skipped`);
      backedUp += 1;
      continue;
    }
  } catch {
    // If the check itself fails, take the backup rather than skip it.
  }

  let live;
  let expected = 0;
  try {
    live = new DatabaseSync(src.path, { readOnly: true });
    expected = live.prepare(src.countSql).get().n;
  } catch (error) {
    fail(`could not read the live ${src.name} store`, error);
  }

  // Second-granularity stamps collide if the job is run twice in one second
  // (a manual run landing on top of a scheduled one).
  let target = join(outDir, `${src.name}-${when}.sqlite`);
  for (let n = 2; existsSync(target); n += 1) {
    target = join(outDir, `${src.name}-${when}-${n}.sqlite`);
  }
  try {
    // VACUUM INTO is atomic and needs no write lock on the source.
    live.prepare("VACUUM INTO ?").run(target);
    live.close();
  } catch (error) {
    fail(`${src.name} snapshot could not be written`, error);
  }

  // A backup nobody has opened is a rumour, not a backup.
  try {
    const copy = new DatabaseSync(target, { readOnly: true });
    const integrity = copy.prepare("PRAGMA integrity_check").get();
    const got = copy.prepare(src.countSql).get().n;
    copy.close();
    const verdict = integrity.integrity_check ?? Object.values(integrity)[0];
    if (verdict !== "ok") {
      fail(`${src.name} copy failed integrity_check: ${verdict}`);
    }
    if (got !== expected) {
      fail(`${src.name} copy holds ${got}, live store has ${expected}`);
    }
    chmodSync(target, 0o600);
    say(`${src.name}: ${expected} ${src.unit} -> ${target}`);
    log(`ok ${src.name} ${expected} ${src.unit} ${target.split("/").pop()}`);
    backedUp += 1;
  } catch (error) {
    fail(`${src.name} copy could not be verified`, error);
  }
}

if (backedUp === 0) {
  fail("no stores were backed up");
}

// Secrets stay on this machine. They change rarely, and a cloud-synced copy of
// WordPress passwords and the n8n encryption key is a worse trade than the
// disk-loss risk it covers. docs/BACKUPS.md says what to do about that once.
try {
  mkdirSync(secretsDir, { recursive: true, mode: 0o700 });
  for (const secret of SECRETS) {
    if (!existsSync(secret.from)) continue;
    const to = join(secretsDir, secret.to);
    copyFileSync(secret.from, to);
    chmodSync(to, 0o600);
  }
} catch (error) {
  console.error(`warning: secrets copy failed — ${error.message}`);
  log(`WARNING secrets copy failed — ${error.message}`);
}

// Prune oldest, newest `keep` retained.
try {
  const snapshots = readdirSync(outDir)
    .filter((name) => /^(chat|n8n)-/.test(name) && name.endsWith(".sqlite"))
    .map((name) => ({ name, at: statSync(join(outDir, name)).mtimeMs }))
    .sort((a, b) => b.at - a.at);
  const stale = snapshots.slice(keep * SOURCES.length);
  for (const { name } of stale) {
    unlinkSync(join(outDir, name));
  }
  if (stale.length > 0) {
    say(`pruned ${stale.length} older snapshot(s), keeping ${keep}`);
    log(`pruned ${stale.length}`);
  }
} catch (error) {
  // Pruning is housekeeping; a full disk is a problem but not a failed backup.
  console.error(`warning: could not prune old snapshots — ${error.message}`);
}
