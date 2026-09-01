// Proves the BD outbound loop end to end: draft -> sent -> follow-up ->
// auto-close, and the reply path that hands a prospect to Sales.
//
// Runs against a throwaway database, never the real board. Time is moved by
// backdating fixture rows through a second connection, because the loop is
// mostly a set of date comparisons and testing it any other way would mean
// waiting a fortnight.
//
//   node scripts/test-bd-loop.mjs

import { DatabaseSync } from "node:sqlite";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const { ChatStore } = await import("../apps/chat/dist/chat-store.js");

const directory = mkdtempSync(join(tmpdir(), "bd-loop-"));
const databasePath = join(directory, "test.sqlite");
const store = new ChatStore(databasePath);
const BRAND = "oddtoe";

let failures = 0;
function check(label, actual, expected) {
  const ok = JSON.stringify(actual) === JSON.stringify(expected);
  if (!ok) {
    failures += 1;
    console.log(`  FAIL ${label}\n       expected ${JSON.stringify(expected)}\n       actual   ${JSON.stringify(actual)}`);
  } else {
    console.log(`  ok   ${label}`);
  }
}

/** Move a stored timestamp or date backwards, so a due date can arrive. */
function backdate(column, prospectId, days) {
  const raw = new DatabaseSync(databasePath);
  const date = new Date();
  date.setUTCDate(date.getUTCDate() - days);
  const value = column === "follow_up_due"
    ? date.toISOString().slice(0, 10)
    : date.toISOString();
  raw.prepare(`UPDATE prospects SET ${column} = ? WHERE prospect_id = ?`)
    .run(value, prospectId);
  raw.close();
}

function seed(company, email) {
  const added = store.addProspect(BRAND, "TEST — bd loop", {
    company,
    contactEmail: email,
    status: "enriched",
  });
  return added.prospect.prospectId;
}

store.saveOutreachSettings(BRAND, {
  senderName: "Otto Ottinger",
  senderContact: "otto@example.com",
  unsubscribeLine: "Reply STOP and I will not write again.",
  dailyCap: 20,
  followUpDays: 7,
  guidePageUrl: "https://example.com/guide",
});

console.log("\nthe happy path: drafted, sent, chased once, closed");
const a = seed("Loop Test Co", "a@example.com");
store.recordProspectDrafts(BRAND, [{ prospectId: a, draftId: "draft-a", hook: "guide feature" }]);
check("draft moves the card to emailed", store.getProspect(a).status, "emailed");
check("a follow-up date is set", store.getProspect(a).followUpDue !== "", true);
check("it is awaiting a reply", store.listAwaitingReply(BRAND).length, 1);

check("a sent signal is recorded",
  store.recordOutreachSignals(BRAND, [{ prospectId: a, kind: "sent" }])[0].outcome, "recorded");
check("sent_at is stamped", store.getProspect(a).sentAt !== "", true);
check("re-running the scan does not double-record",
  store.recordOutreachSignals(BRAND, [{ prospectId: a, kind: "sent" }])[0].outcome, "already");

check("nothing is due yet", store.followUpDueProspects(BRAND).length, 0);
backdate("follow_up_due", a, 2);
const due = store.followUpDueProspects(BRAND);
check("once the date passes it is due", due.length, 1);
check("overdue days are counted", due[0].daysOverdue, 2);

check("the follow-up is recorded",
  store.recordFollowUpDrafts(BRAND, [{ prospectId: a, draftId: "draft-a2" }])[0].outcome, "recorded");
check("the card moves to followed_up", store.getProspect(a).status, "followed_up");
check("the due date is cleared", store.getProspect(a).followUpDue, "");
check("only one follow-up is allowed",
  store.recordFollowUpDrafts(BRAND, [{ prospectId: a, draftId: "draft-a3" }])[0].outcome, "already");

check("a fresh follow-up is not stale", store.autoCloseStale(BRAND, 14).length, 0);
backdate("followed_up_at", a, 20);
check("silence after the follow-up closes it", store.autoCloseStale(BRAND, 14).length, 1);
check("the card is closed", store.getProspect(a).status, "closed");
check("the reason is recorded", store.getProspect(a).closeReason, "No reply 14 days after follow-up");

console.log("\nthe reply path: the handoff to Sales");
const b = seed("Replier Ltd", "b@example.com");
store.recordProspectDrafts(BRAND, [{ prospectId: b, draftId: "draft-b" }]);
check("a reply is recorded",
  store.recordOutreachSignals(BRAND, [{ prospectId: b, kind: "replied" }])[0].outcome, "recorded");
check("the card reaches replied", store.getProspect(b).status, "replied");
check("a replier is never chased", store.getProspect(b).followUpDue, "");
check("a later click cannot drag it backwards",
  store.recordOutreachSignals(BRAND, [{ prospectId: b, kind: "clicked" }])[0].outcome, "already");
check("it is still replied", store.getProspect(b).status, "replied");
check("it has left the awaiting set",
  store.listAwaitingReply(BRAND).some((row) => row.prospectId === b), false);

console.log("\nguardrails");
const c = seed("Opted Out Pty", "c@example.com");
store.recordProspectDrafts(BRAND, [{ prospectId: c, draftId: "draft-c" }]);
backdate("follow_up_due", c, 1);
check("it is due before the opt-out",
  store.followUpDueProspects(BRAND).some((row) => row.prospectId === c), true);
store.addSuppression({ brand: BRAND, email: "c@example.com", reason: "asked" });
check("an opt-out removes it from the due list",
  store.followUpDueProspects(BRAND).some((row) => row.prospectId === c), false);
check("and refuses the write even if asked directly",
  store.recordFollowUpDrafts(BRAND, [{ prospectId: c, draftId: "draft-c2" }])[0].outcome, "suppressed");

const d = seed("Clicker Inc", "d@example.com");
store.recordProspectDrafts(BRAND, [{ prospectId: d, draftId: "draft-d" }]);
check("a click moves emailed to clicked",
  store.recordOutreachSignals(BRAND, [{ prospectId: d, kind: "clicked" }])[0].status, "opened");
check("an unknown prospect is reported, not invented",
  store.recordOutreachSignals(BRAND, [{ prospectId: "nope", kind: "replied" }])[0].outcome, "not_found");

console.log("\nthe brief");
const counts = store.bdBriefCounts(BRAND);
check("it counts the reply waiting to be worked", counts.repliedUnworked, 1);
check("it counts what is still awaiting a reply", counts.awaitingReply, 2);

store.close?.();
rmSync(directory, { recursive: true, force: true });

console.log(failures === 0 ? "\nBD loop: all checks passed\n" : `\nBD loop: ${failures} check(s) failed\n`);
process.exit(failures === 0 ? 0 : 1);
