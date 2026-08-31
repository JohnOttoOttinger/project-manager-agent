#!/usr/bin/env node
// Load or remove the synthetic BD prototype list.
//
// The fixture is deliberately fake: invented agency names on reserved
// .example domains, which cannot route, so nothing can reach a real person
// even if a draft were sent by accident. Every row is marked
// source=synthetic-prototype and lives under its own list name, so it is
// easy to tell apart from a real list and easy to remove.
//
//   node scripts/bd-prototype.mjs load     [--brand oddtoe]
//   node scripts/bd-prototype.mjs status   [--brand oddtoe]
//   node scripts/bd-prototype.mjs remove   [--brand oddtoe]

import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";

const BASE = process.env.CHAT_BASE_URL ?? "http://127.0.0.1:3000";
const LIST_NAME = "PROTOTYPE — synthetic agencies";
const SUPPRESSED = "grace@fernwoodbrandworks.example";
const CSV_PATH = fileURLToPath(
  new URL("../skills/sales-outreach/references/prototype-prospects.csv", import.meta.url),
);

const args = process.argv.slice(2);
const command = args[0] ?? "status";
const brandIndex = args.indexOf("--brand");
const brand = brandIndex === -1 ? "oddtoe" : args[brandIndex + 1];

async function call(path, init) {
  const response = await fetch(BASE + path, init);
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload?.error?.message ?? `${path} failed (${response.status})`);
  }
  return payload;
}

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = "";
  let quoted = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    if (quoted) {
      if (ch === '"') {
        if (text[i + 1] === '"') { field += '"'; i += 1; } else { quoted = false; }
      } else { field += ch; }
    } else if (ch === '"') { quoted = true; }
    else if (ch === ",") { row.push(field); field = ""; }
    else if (ch === "\n") { row.push(field); rows.push(row); row = []; field = ""; }
    else if (ch !== "\r") { field += ch; }
  }
  if (field !== "" || row.length > 0) { row.push(field); rows.push(row); }
  return rows.filter((line) => line.some((cell) => cell.trim() !== ""));
}

const FIELDS = {
  "Company": "company", "Region": "region", "Tier": "tier", "Source": "source",
  "Website": "website", "Contact Name": "contactName", "Email": "contactEmail",
  "Status": "status", "Sent Date": "sentDate", "Notes": "notes",
};

async function load() {
  const table = parseCsv(await readFile(CSV_PATH, "utf8"));
  const header = table[0].map((cell) => FIELDS[cell.trim()] ?? null);
  const rows = table.slice(1).map((cells) => {
    const record = {};
    header.forEach((field, index) => {
      const value = (cells[index] ?? "").trim();
      if (field && value !== "") record[field] = value;
    });
    return record;
  });

  const imported = await call("/api/prospects", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ brand, listName: LIST_NAME, rows }),
  });
  console.log(`imported ${imported.result.inserted} of ${rows.length}` +
    (imported.result.duplicates ? ` (${imported.result.duplicates} already there)` : ""));

  await call("/api/suppressions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ brand, email: SUPPRESSED, reason: "unsubscribed",
      detail: "Synthetic prototype: proves a suppression beats a good prospect." }),
  });
  console.log(`do-not-contact: ${SUPPRESSED}`);

  const campaign = await call("/api/outreach/campaigns", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      brand, name: "PROTOTYPE — agency outreach",
      offer: "Specialist generative-animation and projection content supplier",
      guidePageUrl: "https://www.oddtoe.com/experiential-marketing-agencies/",
      utmCampaign: "prototype-agency-outreach",
    }),
  });
  console.log(`campaign: ${campaign.campaign.name} (${campaign.campaign.campaignId})`);
  await status();
}

async function status() {
  const board = await call(`/api/prospects?brand=${brand}&limit=500`);
  const mine = board.prospects.filter((p) => p.listName === LIST_NAME);
  if (mine.length === 0) {
    console.log(`\nNothing loaded for ${brand}.`);
    return;
  }
  const byStatus = {};
  for (const p of mine) byStatus[p.status] = (byStatus[p.status] ?? 0) + 1;
  console.log(`\nboard (${mine.length} synthetic rows):`,
    Object.entries(byStatus).map(([k, v]) => `${k} ${v}`).join(" · "));

  const draftable = await call(`/api/prospects/draftable?brand=${brand}`);
  const reasons = {};
  for (const s of draftable.skipped) reasons[s.reason] = (reasons[s.reason] ?? 0) + 1;
  console.log(`draftable: ${draftable.eligible.length} eligible, ` +
    `${draftable.skipped.length} skipped, cap ${draftable.dailyCap}, ` +
    `${draftable.remainingToday} left today`);
  for (const [reason, count] of Object.entries(reasons)) {
    console.log(`  skipped ×${count} — ${reason}`);
  }
  const warned = draftable.eligible.filter((e) => e.warning !== "");
  for (const e of warned) console.log(`  warning — ${e.prospect.company}: ${e.warning}`);
}

async function remove() {
  const { DatabaseSync } = await import("node:sqlite");
  const dbPath = process.env.CHAT_DB_PATH ??
    fileURLToPath(new URL("../data/chat/chat.sqlite", import.meta.url));
  const db = new DatabaseSync(dbPath);
  db.exec("PRAGMA foreign_keys = ON");
  const ids = db.prepare("SELECT prospect_id FROM prospects WHERE brand = ? AND list_name = ?")
    .all(brand, LIST_NAME);
  for (const { prospect_id } of ids) {
    db.prepare("DELETE FROM outreach_events WHERE prospect_id = ?").run(prospect_id);
    db.prepare("DELETE FROM prospects WHERE prospect_id = ?").run(prospect_id);
  }
  db.prepare("DELETE FROM suppressions WHERE brand = ? AND email_key = ?").run(brand, SUPPRESSED);
  db.prepare("DELETE FROM campaigns WHERE brand = ? AND name = ?")
    .run(brand, "PROTOTYPE — agency outreach");
  console.log(`removed ${ids.length} synthetic prospects, the suppression and the campaign.`);
  console.log("Restart the local app so it reloads the store.");
}

const commands = { load, status, remove };
if (!commands[command]) {
  console.error("Usage: node scripts/bd-prototype.mjs load|status|remove [--brand oddtoe]");
  process.exit(1);
}
await commands[command]().catch((error) => {
  console.error("Failed:", error.message);
  process.exit(1);
});
