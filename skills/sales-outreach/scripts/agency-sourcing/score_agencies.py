"""Score each agency on whether it commissions the work Oddtoe actually makes.

The prospect here is an agency that BUILDS physical brand experiences and would
subcontract fabrication, installation, projection or character/animation work -
not a digital-marketing shop that happens to rank for "brand agency".
"""
import json, re

STRONG = ["experiential", "brand activation", "brand experience", "activation",
          "immersive", "installation", "exhibition", "pop-up", "popup",
          "spatial", "scenic", "set build", "fabrication", "custom build",
          "projection", "interactive", "stand design", "trade show",
          "event production", "festival", "placemaking", "themed"]
WEAK = ["event", "brand", "creative", "production", "design", "studio",
        "campaign", "live", "experience"]
VETO = ["seo agency", "search engine optimisation", "search engine optimization",
        "ppc", "google ads", "social media management", "web design agency",
        "lead generation", "real estate", "wedding photograph", "recruitment"]

rows = json.load(open("crawled.json"))
scored = []
for r in rows:
    hay = " ".join([r.get("site_title",""), r.get("site_desc",""),
                    r.get("sample","")[:2000], r.get("company",""), r.get("type","")]).lower()
    if not hay.strip() or r["crawl_note"]:
        r["fit"] = None; scored.append(r); continue
    if any(v in hay for v in VETO):
        r["fit"] = -1; r["hits"] = []; scored.append(r); continue
    hits = [w for w in STRONG if w in hay]
    r["hits"] = hits
    r["fit"] = len(hits) * 3 + sum(1 for w in WEAK if w in hay)
    scored.append(r)

live = [r for r in scored if r.get("fit") is not None and r["fit"] > 0]
live.sort(key=lambda r: (-r["fit"], -(r.get("reviews") or 0)))
json.dump(live, open("scored.json","w"), indent=2)

vetoed = [r for r in scored if r.get("fit") == -1]
dead   = [r for r in scored if r.get("fit") is None]
print(f"{len(live)} scored fit>0 | {len(vetoed)} vetoed (digital-marketing shops) | {len(dead)} unreadable\n")
strong = [r for r in live if len(r["hits"]) >= 4]
print(f"{len(strong)} have 4+ strong experiential signals; {sum(1 for r in strong if r['emails'])} of those publish an email\n")
for r in strong[:30]:
    e = r["emails"][0] if r["emails"] else "-"
    print(f"  [{r['fit']:>3}] {r['company'][:36]:38} {r['city'][:9]:10} {e[:32]:34} {','.join(r['hits'][:4])[:44]}")
