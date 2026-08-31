#!/usr/bin/env node
// Demo rows for the Festivals and Press modes, so every status, stream and
// segment has something in it. These are INVENTED organisations, marked with
// a demo- source id and badged in the UI. Real festivals are never given a
// fake status: a real event showing "submitted" when it has not been would
// be a worse error than an obviously invented row.
//
//   node scripts/bd-seed-demo.mjs [add|remove] [--brand oddtoe]

import { fileURLToPath } from "node:url";
import { DatabaseSync } from "node:sqlite";
import { randomUUID } from "node:crypto";

const args = process.argv.slice(2);
const command = args[0] ?? "add";
const brandIndex = args.indexOf("--brand");
const brand = brandIndex === -1 ? "oddtoe" : args[brandIndex + 1];
const db = new DatabaseSync(
  process.env.CHAT_DB_PATH ??
    fileURLToPath(new URL("../data/chat/chat.sqlite", import.meta.url)),
);
const now = new Date().toISOString();
const day = (offset) => {
  const d = new Date();
  d.setUTCDate(d.getUTCDate() + offset);
  return d.toISOString().slice(0, 10);
};

const OPPORTUNITIES = [
  ["demo-southern-light", "Southern Light Award for Generative Art", "Southern Light Foundation",
   "prize", "Melbourne", "Australia", day(21), day(60), "", day(21), "shortlisted",
   "Annual award for generative and computational work. Shortlist announced six weeks after close."],
  ["demo-meridian-prize", "Meridian Digital Arts Prize", "Meridian Arts Trust",
   "prize", "London", "United Kingdom", day(45), day(120), "", day(45), "preparing",
   "Open to studios as well as individuals. Requires a 3-minute showreel and a written statement."],
  ["demo-port-arlen", "Port Arlen City Public Art Register", "City of Port Arlen",
   "register", "Port Arlen", "Australia", "", "", "", day(9), "submitted",
   "Standing register for commissionable public artists. Council draws from it for two years."],
  ["demo-northern-rivers", "Northern Rivers Creative Register", "Northern Rivers Arts Board",
   "register", "Lismore", "Australia", "", "", "", day(-30), "accepted",
   "Accepted onto the register. Expect briefs by email; no further action needed."],
  ["demo-verge-opencall", "Verge Festival Open Call", "Verge Collective",
   "opencall", "Wellington", "New Zealand", day(75), day(90), "", day(-12), "declined",
   "Applied for the projection strand. Declined: programme filled from returning artists."],
  ["demo-tidewater", "Tidewater Animation Prize", "Tidewater Screen Trust",
   "prize", "Halifax", "Canada", "", "", "", day(30), "passed",
   "Chose not to enter — entry fee and rights terms did not suit."],
  ["demo-halcyon-call", "Halcyon Media Arts Open Call", "Halcyon Media Arts",
   "opencall", "Berlin", "Germany", day(140), day(150), "", day(-4), "missed",
   "Deadline passed before a submission was prepared. Next round opens in the new year."],
  ["demo-brightwater", "Brightwater Digital Biennale", "Brightwater Biennale",
   "opencall", "Vancouver", "Canada", day(200), day(215), "", day(52), "preparing",
   "Large-scale outdoor projection strand. Needs a site plan and a technical rider."],
];

const MEDIA = [
  ["demo-rendered-hour", "podcast", "The Rendered Hour", "Priya Anand", "Host and producer",
   "https://example.com/rendered-hour", "priya@renderedhour.example", "drafted",
   "Episode format is a single 40-minute maker interview — a good fit for the generative process story.", ""],
  ["demo-motion-theory", "youtube", "Motion Theory", "Dev Okonkwo", "Creator",
   "https://example.com/motion-theory", "dev@motiontheory.example", "sent",
   "Breaks down technique in 15-minute videos. Pitched the projection-mapping build.", ""],
  ["demo-marlow-finch", "pr_agency", "Marlow & Finch PR", "Simone Baptiste", "Director",
   "https://example.com/marlow-finch", "simone@marlowfinch.example", "outcome",
   "Arts and culture PR. Approached about representation.", "Declined — not taking new arts clients this year."],
  ["demo-northlight", "journalist", "Northlight Quarterly", "Ines Farrow", "Arts editor",
   "https://example.com/northlight", "ines@northlight.example", "sent",
   "Commissions long-form studio profiles. Pitched the Melbourne studio piece.", ""],
  ["demo-studio-signal", "podcast", "Studio Signal", "Tom Vasquez", "Producer",
   "https://example.com/studio-signal", "tom@studiosignal.example", "qualified",
   "Covers studios working at the art/technology edge. No pitch sent yet.", ""],
];

if (command === "remove") {
  const a = db.prepare("DELETE FROM opportunities WHERE brand = ? AND source_id LIKE 'demo-%'").run(brand);
  const b = db.prepare("DELETE FROM media_contacts WHERE brand = ? AND source_id LIKE 'demo-%'").run(brand);
  console.log(`removed ${a.changes} demo opportunities and ${b.changes} demo media contacts`);
} else {
  const opp = db.prepare(
    `INSERT INTO opportunities (opportunity_id, brand, source_id, name, organiser,
       kind, city, country, url, event_start, event_end, press_deadline,
       submission_deadline, contact, relevance, next_action, status, verified,
       notes, created_at, updated_at)
     VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
     ON CONFLICT(brand, name) DO UPDATE SET status=excluded.status, updated_at=excluded.updated_at`,
  );
  for (const [id, name, org, kind, city, country, start, end, press, sub, status, why] of OPPORTUNITIES) {
    opp.run(randomUUID(), brand, id, name, org, kind, city, country,
      "https://example.com/" + id, start, end, press, sub, "", why, "",
      status, "", "INVENTED demo row — not a real organisation.", now, now);
  }
  const med = db.prepare(
    `INSERT INTO media_contacts (media_id, brand, source_id, segment, outlet, person,
       role, url, email, contact_page, linkedin, hook, why_fit, evidence_url,
       relevance, status, outcome, notes, created_at, updated_at)
     VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
     ON CONFLICT(brand, outlet, person) DO UPDATE SET status=excluded.status, updated_at=excluded.updated_at`,
  );
  for (const [id, segment, outlet, person, role, url, email, status, why, outcome] of MEDIA) {
    med.run(randomUUID(), brand, id, segment, outlet, person, role, url, email,
      "", "", why, why, "", "", status, outcome,
      "INVENTED demo row — not a real outlet.", now, now);
  }
  console.log(`added ${OPPORTUNITIES.length} demo opportunities and ${MEDIA.length} demo media contacts for ${brand}`);
}
