#!/usr/bin/env node
// Seed the Festivals and Press modes from the opportunity-tracker skill's
// research files. Those JSON files stay the researcher's source of truth;
// this copies them into the app store so the screens have real data.
//
//   node scripts/bd-seed-streams.mjs [--brand oddtoe]

import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { DatabaseSync } from "node:sqlite";
import { randomUUID } from "node:crypto";

const args = process.argv.slice(2);
const brandIndex = args.indexOf("--brand");
const brand = brandIndex === -1 ? "oddtoe" : args[brandIndex + 1];
const refs = fileURLToPath(
  new URL("../skills/opportunity-tracker/references/", import.meta.url),
);
const dbPath = process.env.CHAT_DB_PATH ??
  fileURLToPath(new URL("../data/chat/chat.sqlite", import.meta.url));

const read = async (name) => JSON.parse(await readFile(refs + name, "utf8"));
const [opportunities, festivals, media] = await Promise.all([
  read("opportunities.json"), read("festivals.json"), read("media-contacts.json"),
]);

const db = new DatabaseSync(dbPath);
const now = new Date().toISOString();
const KINDS = new Set(["press", "market", "prize", "opencall", "register", "scouting"]);
const SEGMENTS = new Set(["podcast", "youtube", "journalist", "pr_agency"]);

const oppStmt = db.prepare(
  `INSERT INTO opportunities (opportunity_id, brand, source_id, name, organiser,
     kind, city, country, url, event_start, event_end, press_deadline,
     submission_deadline, contact, relevance, next_action, status, verified,
     notes, created_at, updated_at)
   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
   ON CONFLICT(brand, name) DO UPDATE SET
     organiser=excluded.organiser, kind=excluded.kind, city=excluded.city,
     country=excluded.country, url=excluded.url, event_start=excluded.event_start,
     event_end=excluded.event_end, press_deadline=excluded.press_deadline,
     submission_deadline=excluded.submission_deadline, contact=excluded.contact,
     relevance=excluded.relevance, next_action=excluded.next_action,
     verified=excluded.verified, notes=excluded.notes, updated_at=excluded.updated_at`,
);

let opps = 0;
for (const e of opportunities.entries) {
  const kind = KINDS.has(e.type) ? e.type : "press";
  oppStmt.run(
    randomUUID(), brand, e.id ?? "", e.name, e.organiser ?? "", kind,
    e.city ?? "", e.country ?? "", e.url ?? "", e.start ?? "", e.end ?? "",
    e.press_deadline ?? "", e.submission_deadline ?? "",
    e.press_contact ?? "", e.blurb ?? "", "", "researching",
    String(e.verified ?? ""), e.note ?? "", now, now,
  );
  opps += 1;
}
for (const e of festivals.entries) {
  const streams = e.streams ?? [];
  const kind = streams.find((s) => KINDS.has(s)) ?? "scouting";
  oppStmt.run(
    randomUUID(), brand, e.id ?? "", e.name, e.organiser ?? "", kind,
    e.city ?? "", e.country ?? "", e.url ?? "", e.start ?? "", e.end ?? "",
    "", "", "", e.relevance ?? e.focus ?? "", e.next_action ?? "",
    "researching", String(e.verified ?? ""),
    [e.dates_note, e.attending_2026 ? `Attending 2026: ${e.attending_2026}` : ""]
      .filter(Boolean).join(" — "),
    now, now,
  );
  opps += 1;
}

const mediaStmt = db.prepare(
  `INSERT INTO media_contacts (media_id, brand, source_id, segment, outlet,
     person, role, url, email, contact_page, linkedin, hook, why_fit,
     evidence_url, relevance, status, outcome, notes, created_at, updated_at)
   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
   ON CONFLICT(brand, outlet, person) DO UPDATE SET
     segment=excluded.segment, role=excluded.role, url=excluded.url,
     email=excluded.email, contact_page=excluded.contact_page,
     linkedin=excluded.linkedin, hook=excluded.hook, why_fit=excluded.why_fit,
     evidence_url=excluded.evidence_url, relevance=excluded.relevance,
     notes=excluded.notes, updated_at=excluded.updated_at`,
);
let contacts = 0;
for (const c of media.contacts) {
  mediaStmt.run(
    randomUUID(), brand, c.id ?? "",
    SEGMENTS.has(c.segment) ? c.segment : "journalist",
    c.outlet ?? "(unnamed outlet)", c.person ?? "", c.role ?? "", c.url ?? "",
    c.email ?? "", c.contact_page ?? "", c.linkedin ?? "", c.hook ?? "",
    c.why_fit ?? "", c.evidence_url ?? "", String(c.relevance ?? ""),
    ["sourced", "qualified", "drafted", "sent", "outcome"].includes(c.status)
      ? c.status : "sourced",
    c.outcome ?? "", c.notes ?? "", now, now,
  );
  contacts += 1;
}

console.log(`seeded ${opps} opportunities and ${contacts} media contacts for ${brand}`);
