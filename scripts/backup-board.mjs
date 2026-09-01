// Hot backup of the board database. Safe to run on a schedule while the app
// is up: `npm run backup` stops chat and n8n for consistency, which is fine
// by hand and unacceptable every two hours. `VACUUM INTO` takes a consistent
// snapshot of a live database without stopping anything.
//
//   node scripts/backup-board.mjs [--keep N] [--quiet]
//
// Writes backups/board/chat-YYYYMMDD-HHMMSS.sqlite, verifies the copy opens
// and holds the same prospect count, prunes to the newest N, and appends one
// line to backups/board/backup.log. Exits non-zero if anything fails, so a
// scheduler can surface it.

import { DatabaseSync } from "node:sqlite";
import { mkdirSync, readdirSync, statSync, unlinkSync, chmodSync, appendFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const source = join(root, "data", "chat", "chat.sqlite");
const outDir = join(root, "backups", "board");
const logPath = join(outDir, "backup.log");

const args = process.argv.slice(2);
const keep = Math.max(2, Number(args[args.indexOf("--keep") + 1]) || 48);
const quiet = args.includes("--quiet");
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

let expected = 0;
let live;
try {
  live = new DatabaseSync(source, { readOnly: true });
  expected = live.prepare("SELECT COUNT(*) AS n FROM prospects").get().n;
} catch (error) {
  fail("could not read the live board", error);
}

// Second-granularity stamps collide if the job is run twice in one second
// (a manual run landing on top of a scheduled one).
let target = join(outDir, `chat-${stamp(new Date())}.sqlite`);
for (let n = 2; existsSync(target); n += 1) {
  target = join(outDir, `chat-${stamp(new Date())}-${n}.sqlite`);
}
try {
  // VACUUM INTO is atomic and needs no write lock on the source.
  live.prepare("VACUUM INTO ?").run(target);
  live.close();
} catch (error) {
  fail("snapshot could not be written", error);
}

// A backup nobody has opened is a rumour, not a backup.
try {
  const copy = new DatabaseSync(target, { readOnly: true });
  const integrity = copy.prepare("PRAGMA integrity_check").get();
  const got = copy.prepare("SELECT COUNT(*) AS n FROM prospects").get().n;
  copy.close();
  const verdict = integrity.integrity_check ?? Object.values(integrity)[0];
  if (verdict !== "ok") {
    fail(`copy failed integrity_check: ${verdict}`);
  }
  if (got !== expected) {
    fail(`copy holds ${got} prospects, live board has ${expected}`);
  }
  chmodSync(target, 0o600);
  say(`backed up ${expected} prospects -> ${target}`);
  log(`ok ${expected} prospects ${target.split("/").pop()}`);
} catch (error) {
  fail("copy could not be verified", error);
}

// Prune oldest, newest `keep` retained.
try {
  const snapshots = readdirSync(outDir)
    .filter((name) => name.startsWith("chat-") && name.endsWith(".sqlite"))
    .map((name) => ({ name, at: statSync(join(outDir, name)).mtimeMs }))
    .sort((a, b) => b.at - a.at);
  const stale = snapshots.slice(keep);
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
