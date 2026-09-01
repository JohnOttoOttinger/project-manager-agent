"""Stage 3: pre-score the pool so a human-sized shortlist can be read properly.

Three separate axes, deliberately NOT collapsed into one number too early:
  territory - does it cover what Oddtoe actually makes
  vibe      - playful / funny / curious, the thing Otto flagged as load-bearing
  bookable  - does it interview guests at all
A show scoring high on territory but zero on vibe is a worse fit than the
reverse, so both are kept visible.
"""
import json, re

TERRITORY = {
    3: ["public art", "sculpture", "installation art", "projection mapping",
        "light festival", "land art", "kinetic", "placemaking", "experiential",
        "immersive", "themed entertainment", "exhibition design", "biennale",
        "animation", "animator", "motion design", "character design",
        "art toy", "designer toy", "toy design", "generative art",
        "creative coding", "new media", "garden design", "topiary",
        "landscape architecture", "public space", "street art", "mural"],
    2: ["illustration", "illustrator", "cartoon", "puppet", "prop", "curator",
        "museum", "gallery", "robotics", "fabrication", "maker", "sculptor",
        "horticulture", "botanical", "garden", "design studio", "artist"],
}
VIBE = ["funny", "humour", "humor", "comedy", "playful", "whimsy", "whimsical",
        "weird", "odd", "quirky", "silly", "joy", "delight", "absurd",
        "curious", "curiosity", "wonder", "awe", "fun", "laugh", "grin"]
BOOKABLE = ["interview", "guest", "conversation", "we talk", "talks to",
            "chats with", "sits down with", "each week i talk"]
VETO = ["true crime", "murder", "serial killer", "fantasy football", "nfl",
        "nba", "crypto", "bitcoin", "real estate investing", "sermon",
        "gospel", "bible study", "weight loss", "keto", "parenting hacks",
        "dropshipping", "affiliate marketing", "sports betting"]

doc = json.load(open("enriched.json"))
scored = []
for s in doc["shows"]:
    if s.get("fetch_error"):
        continue
    hay = " ".join([
        s.get("show", ""), s.get("summary", ""), s.get("author", ""),
        " ".join(e["title"] for e in s.get("recent_episodes", [])),
    ]).lower()
    if any(v in hay for v in VETO):
        continue
    territory = 0
    hits = []
    for weight, words in TERRITORY.items():
        for w in words:
            if w in hay:
                territory += weight
                hits.append(w)
    vibe = [w for w in VIBE if w in hay]
    bookable = any(w in hay for w in BOOKABLE)
    if territory == 0:
        continue
    s2 = dict(s)
    s2.update(territory_score=territory, territory_hits=sorted(set(hits))[:12],
              vibe_score=len(vibe), vibe_hits=vibe[:10], bookable=bookable,
              rank=territory + 2 * len(vibe) + (3 if bookable else 0)
                   + (4 if s.get("email") else 0))
    scored.append(s2)

scored.sort(key=lambda r: r["rank"], reverse=True)
json.dump({"scored": len(scored), "shows": scored},
          open("scored.json", "w"), indent=2)
print(f"{len(scored)} shows survive territory+veto filter\n")
print(f"{'rank':>4} {'terr':>4} {'vibe':>4} {'bk':>2} {'email':>5}  show")
for s in scored[:45]:
    print(f"{s['rank']:>4} {s['territory_score']:>4} {s['vibe_score']:>4} "
          f"{'y' if s['bookable'] else '-':>2} {'y' if s['email'] else '-':>5}  "
          f"{s['show'][:62]}")
