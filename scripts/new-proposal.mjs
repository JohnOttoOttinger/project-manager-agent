#!/usr/bin/env node
// Scaffold a client deal folder from the client-proposal skill templates.
// Usage: node scripts/new-proposal.mjs "Monash University" [--short Monash] [--force]

import { readFile, writeFile, mkdir, access } from "node:fs/promises";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { homedir } from "node:os";

const here = dirname(fileURLToPath(import.meta.url));
const TEMPLATES = join(here, "..", ".claude", "skills", "client-proposal", "templates");
const PROPOSALS = join(homedir(), "Documents", "Datalabs - iCloud Apple", "Proposals");

const args = process.argv.slice(2);
const force = args.includes("--force");
const shortIndex = args.indexOf("--short");
const positional = args.filter((a, i) =>
  !a.startsWith("--") && i !== shortIndex + 1 || shortIndex === -1 && !a.startsWith("--"));
const client = positional[0];

if (!client) {
  console.error('Usage: node scripts/new-proposal.mjs "<Client name>" [--short <Short>] [--force]');
  process.exit(1);
}
const short = shortIndex !== -1 ? args[shortIndex + 1] : client.split(/[\s,]+/)[0];
const today = new Date().toLocaleDateString("en-AU", {
  day: "numeric", month: "short", year: "numeric", timeZone: "Australia/Melbourne",
});

const exists = async (p) => { try { await access(p); return true; } catch { return false; } };

const FILES = [
  ["deal-tracker.md",   `${short}-Deal-Tracker.md`],
  ["session-outline.md", `${short}-Session-Outline.md`],
  ["todos.md",          `${short}-ToDos.md`],
];

const folder = join(PROPOSALS, client);
await mkdir(folder, { recursive: true });

let written = 0, skipped = 0;
for (const [template, outName] of FILES) {
  const out = join(folder, outName);
  if (await exists(out) && !force) {
    console.log(`  skip   ${outName} (exists — pass --force to overwrite)`);
    skipped += 1;
    continue;
  }
  const body = (await readFile(join(TEMPLATES, template), "utf8"))
    .replaceAll("{{CLIENT_SHORT}}", short)
    .replaceAll("{{CLIENT}}", client)
    .replaceAll("{{DATE_OPENED}}", today)
    .replaceAll("{{DATE}}", today);
  await writeFile(out, body, "utf8");
  console.log(`  create ${outName}`);
  written += 1;
}

console.log(`\n${folder}`);
console.log(`${written} created, ${skipped} skipped.`);
console.log("\nNext: read the Gmail thread and fill from evidence — never from memory.");
console.log("Unverified fields stay as open questions.");
