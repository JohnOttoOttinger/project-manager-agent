// Generate and load the launchd agent that runs the board backup.
//
//   node scripts/install-backup-agent.mjs [--dest DIR] [--interval SECONDS]
//   node scripts/install-backup-agent.mjs --uninstall
//   node scripts/install-backup-agent.mjs --status
//
// The plist cannot live in the repo: it holds absolute paths to this checkout
// and to the private Node runtime, both of which differ per machine. So it is
// generated here instead, which is also what makes this reproducible on a new
// Mac — see docs/BACKUPS.md.
//
// macOS only. launchd is the point; there is no cross-platform equivalent
// worth pretending about.

import { writeFileSync, mkdirSync, existsSync, unlinkSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { homedir, platform } from "node:os";

const LABEL = "com.oddtoe.board-backup";
const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const plistPath = join(homedir(), "Library", "LaunchAgents", `${LABEL}.plist`);

const args = process.argv.slice(2);
const flag = (name) => {
  const i = args.indexOf(name);
  return i === -1 ? "" : (args[i + 1] ?? "");
};

if (platform() !== "darwin") {
  console.error("This installer is macOS-only (it uses launchd).");
  console.error("Elsewhere, run `npm run backup-board` from cron or a timer.");
  process.exit(1);
}

function launchctl(...argv) {
  try {
    return execFileSync("launchctl", argv, { encoding: "utf8" }).trim();
  } catch (error) {
    return (error.stdout ?? "").trim();
  }
}

if (args.includes("--status")) {
  const line = launchctl("list").split("\n").find((row) => row.includes(LABEL));
  if (!line) {
    console.log(`${LABEL} is not loaded. Run this script with no arguments to install it.`);
    process.exit(1);
  }
  const [pid, exit] = line.split(/\s+/);
  console.log(`${LABEL} loaded — last exit ${exit}${pid === "-" ? "" : `, running as pid ${pid}`}`);
  console.log(`plist: ${plistPath}`);
  process.exit(exit === "0" ? 0 : 1);
}

if (args.includes("--uninstall")) {
  launchctl("unload", plistPath);
  if (existsSync(plistPath)) {
    unlinkSync(plistPath);
  }
  console.log(`removed ${LABEL}. Existing snapshots are left alone.`);
  process.exit(0);
}

// Prefer the project's private runtime: launchd starts with a minimal PATH and
// will not find a Node installed by nvm or Homebrew.
const bundled = join(root, ".runtime", "node-v24.18.0-darwin-arm64", "bin", "node");
const hasBundled = existsSync(bundled);
const nodeBin = hasBundled ? bundled : process.execPath;
if (!hasBundled) {
  console.warn(`warning: bundled runtime not found, falling back to ${nodeBin}`);
  console.warn("         if that path moves the agent stops silently — run setup.command");
  console.warn("         to install the private runtime, then re-run this installer.");
}

const dest = flag("--dest")
  || join(homedir(), "Library", "Mobile Documents", "com~apple~CloudDocs", "Oddtoe Agent Backups");
const interval = Math.max(600, Number(flag("--interval")) || 7200);

mkdirSync(dirname(plistPath), { recursive: true });
mkdirSync(dest, { recursive: true });
mkdirSync(join(root, "backups"), { recursive: true });

const escape = (value) =>
  value.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

writeFileSync(plistPath, `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>${escape(nodeBin)}</string>
    <string>${escape(join(root, "scripts", "backup-board.mjs"))}</string>
    <string>--quiet</string>
    <string>--dest</string>
    <string>${escape(dest)}</string>
  </array>
  <key>WorkingDirectory</key>
  <string>${escape(root)}</string>
  <key>StartInterval</key>
  <integer>${interval}</integer>
  <key>RunAtLoad</key>
  <true/>
  <key>StandardErrorPath</key>
  <string>${escape(join(root, "backups", "launchd.err.log"))}</string>
  <key>ProcessType</key>
  <string>Background</string>
  <key>LowPriorityIO</key>
  <true/>
</dict>
</plist>
`);

try {
  execFileSync("plutil", ["-lint", plistPath], { stdio: "pipe" });
} catch {
  console.error(`generated plist is malformed: ${plistPath}`);
  process.exit(1);
}

// Unload first so re-running is how you change the schedule, not an error.
launchctl("unload", plistPath);
launchctl("load", plistPath);

const line = launchctl("list").split("\n").find((row) => row.includes(LABEL));
if (!line) {
  console.error(`launchd did not accept ${LABEL}. Check ${plistPath}`);
  process.exit(1);
}

const hours = (interval / 3600).toFixed(interval % 3600 === 0 ? 0 : 1);
console.log(`installed ${LABEL}`);
console.log(`  every ${hours}h, and once now`);
console.log(`  snapshots -> ${dest}`);
console.log(`  plist     -> ${plistPath}`);
console.log(`\nCheck it later with: npm run backup-agent -- --status`);
