"""Turn the crawl into prospect rows, with the email hygiene the board needs.

Rules learned across this session, applied here:
  * a placeholder or a third-party vendor address is NOT a contact
  * an address must sit on the company's own domain to count as confident
  * dedupe against what is already on the board, not just within this batch
"""
import json, re, sqlite3, urllib.parse

DB = "/Users/Ottinger/Claude-Projects-2026/project-manager-agent/data/chat/chat.sqlite"
PLACEHOLDER = re.compile(r"^(user|name|your|email|someone|test|admin|no-?reply|"
                         r"info)@(domain|example|email|yourdomain|company)\.", re.I)
VENDOR = re.compile(r"(searchitlocal|wixpress|godaddy|squarespace|shopify|"
                    r"mailchimp|hubspot|sentry)", re.I)
FILEISH = re.compile(r"(_|\d{4,}|\.(png|jpe?g|webp|svg|gif|css|js)$)", re.I)

def domain_of(url):
    return re.sub(r"^https?://(www\.)?", "", (url or "").lower()).split("/")[0]

def pick_email(emails, domain):
    for e in emails:
        if PLACEHOLDER.match(e) or VENDOR.search(e) or FILEISH.search(e):
            continue
        if "@" not in e or len(e) > 70:
            continue
        return e, ("high" if domain and e.endswith("@" + domain) else "low")
    return "", "none"

FABRICATOR = ["display", "expo", "exhibition stand", "signage", "stand design",
              "printing", "print", "manufactur"]

rows = json.load(open("scored.json"))
db = sqlite3.connect(DB)
existing_names = {n.strip().lower() for (n,) in
                  db.execute("select company from prospects where brand='oddtoe'")}
existing_domains = {domain_of(w) for (w,) in
                    db.execute("select website from prospects where brand='oddtoe'") if w}

out, skipped_dupe = [], []
for r in rows:
    if r["fit"] < 6 or not r["website"]:
        continue
    dom = domain_of(r["website"])
    if r["company"].strip().lower() in existing_names or (dom and dom in existing_domains):
        skipped_dupe.append(r["company"]); continue
    email, confidence = pick_email(r.get("emails", []), dom)
    blob = " ".join([r.get("site_title",""), r.get("company",""), r.get("type","")]).lower()
    tier = ("Fabricator / display" if any(f in blob for f in FABRICATOR)
            else "Experiential agency" if any(h in ("experiential","brand activation",
                 "brand experience","immersive","activation") for h in r["hits"])
            else "Event / production")
    flag = ""
    if confidence == "none":
        flag = "No published email found on the site — needs a contact-finding pass"
    elif confidence == "low":
        flag = f"Email is not on the company domain ({dom}) — confirm it belongs to them"
    out.append({
        "company": r["company"][:200],
        "region": {"melbourne":"Melbourne, AU","sydney":"Sydney, AU","brisbane":"Brisbane, AU"}[r["city"]],
        "tier": tier,
        "source": "Google Maps sweep 2026-09-01 + site crawl",
        "website": r["website"][:400],
        "contactEmail": email,
        "confidence": confidence,
        "flagReason": flag,
        "notes": (f"Fit score {r['fit']} from site copy. Signals: "
                  f"{', '.join(r['hits'][:6]) or 'none'}. "
                  f"Found via Google Maps search '{r['term']}'. "
                  f"{('Site says: ' + r['site_desc'][:180]) if r.get('site_desc') else ''}").strip(),
    })

json.dump({"brand":"oddtoe","listName":"Australian experiential agencies Sep 2026","rows":out},
          open("import-agencies.json","w"), indent=2)
from collections import Counter
print(f"{len(out)} prospect rows built  |  {len(skipped_dupe)} skipped as already on the board: {skipped_dupe}\n")
print("by tier:      ", dict(Counter(r['tier'] for r in out)))
print("by region:    ", dict(Counter(r['region'] for r in out)))
print("by confidence:", dict(Counter(r['confidence'] for r in out)))
print(f"\nwith a usable email: {sum(1 for r in out if r['contactEmail'])}/{len(out)}")
