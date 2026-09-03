#!/usr/bin/env python3
"""What page to build next, ranked on real demand rather than Search Console leftovers.

    score = log10(volume) x relevance x commercial_tier x gap x winnability x competition

Why not Search Console: GSC only reports queries the site ALREADY appears for, so the gaps
worth building are invisible to it by construction. The clearest case on record is
"power bi training" - 720/mo of real Australian demand, 8 impressions in 180 days, because
the site does not rank for it at all. next-best-page.py could never have surfaced it, and
did not. Demand comes from references/keyword-universe.json (DataForSEO sweeps); GSC is
demoted to what it is genuinely good at - the cannibalisation guardrail.

  volume        real monthly searches, Australia. Logged, not raw: a 33,100/mo how-to term
                should not automatically outrank a 720/mo term that sells a workshop.
  relevance     is the term about what this brand actually does. Without it the scout offers
                any high-volume term a rival ranks for - "communication skills course", 1,000/mo,
                a page Otto would never build.
  commercial    how few steps from this page to someone booking something.
  gap           a live HEAD check. 404 = a real gap. 200 = the page exists, so this is a
                retrofit, not a build, and it is reported in a separate section.
  winnability   how weakly the incumbent holds it. Deep incumbent on a big term is the best
                shape there is. A strong incumbent still proves the demand, so it costs some
                score, not the candidate.
  competition   LOW/MEDIUM/HIGH from the sweep.

    python3 next-content.py --brand datalabs
    python3 next-content.py --brand oddtoe --json --limit 3
    python3 next-content.py --brand datalabs --no-gsc      # skip the guardrail lookup

Read-only. Writes nothing - accepting a candidate into the queue is suggest.py's job.
"""
from __future__ import annotations
import argparse, json, math, os, re, sys, urllib.parse, urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REF = Path(__file__).resolve().parent.parent / "references"
SITES = {"oddtoe": "https://www.oddtoe.com", "datalabs": "https://www.datalabsagency.com"}
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

# Commercial proximity, tested against the TERM. First match wins, so order matters.
TIERS = {
 "datalabs": [
   (1.00, "A - sells training",   r"training|workshop|course|classes|class\b|masterclass|bootcamp|certification"),
   (0.75, "B - sells a service",  r"dashboard design|consult|design service|style guide|agency|services|annual report|infographic"),
   (0.55, "C - feeds a service",  r"how to|what is|types of|\bvs\b|best |guide|tutorial|examples|cost|price|chart|gantt|pivot|excel|power bi|tableau"),
   (0.30, "D - proof",            r"case stud|portfolio"),
 ],
 "oddtoe": [
   (1.00, "A - sells the work",   r"activation|prop |fabricat|inflatable|installation|experiential|sculpture|sculptor|topiary|puppet|set design|scenic|projection mapping"),
   (0.75, "B - sells a service",  r"animation|animator|character|designer|artist|studio|illustrat|speaker|director|immersive"),
   (0.55, "C - feeds a service",  r"ideas|what is|how |guide|cost|best |\bvs\b|conference|festival|examples"),
   (0.30, "D - proof",            r"portfolio|case stud"),
 ],
}
DEFAULT_TIER = (0.40, "- unclassified")

# Is the term about what this brand actually does? The tier table answers "does this smell
# commercial", which is not the same question - "communication skills course" is tier A on the
# word "course" alone and is a page Otto would never build. Without this gate the scout
# proposes any high-volume term a rival happens to rank for.
SUBJECT = {
 "datalabs": r"data|dashboard|chart|graph|visuali|analytic|analysis|power bi|tableau|excel|"
             r"infographic|gantt|pivot|\bbi\b|report|metric|kpi|storytell",
 "oddtoe": r"sculpt|prop|inflatable|installation|animat|character|experiential|activation|"
           r"immersive|projection|topiary|puppet|artist|\bart\b|design|studio|event|"
           r"fabricat|illustrat|scenic|set design",
}
COMPETITION = {"LOW": 1.0, "MEDIUM": 0.85, "HIGH": 0.60}
# Below this, the best remaining candidate is not worth a day's build and the honest answer is
# "the validated demand has been harvested - run a new sweep" rather than a filler suggestion.
EXHAUSTED = 1.6
STOP = {"a","an","the","in","for","of","and","or","to","is","are","do","does","what","how",
        "with","on","at","by","near","me","my","your","best","top"}


SYNONYM = {"analysis": "analytic", "analytics": "analytic", "analyst": "analytic",
           "classes": "course", "class": "course", "courses": "course", "training": "course",
           "charts": "chart", "sculptures": "sculpture", "sculptor": "sculpture",
           "services": "service", "agencies": "agency", "studios": "studio"}


def stem(w):
    w = SYNONYM.get(w, w)
    return SYNONYM.get(w[:-1], w[:-1]) if w.endswith("s") and len(w) > 4 else w


def tokens(s, stemmed=False):
    raw = {w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP and len(w) > 2}
    return {stem(w) for w in raw} if stemmed else raw


def relevant(term, brand):
    """0.35 is a heavy penalty, not a ban - Otto may still want an adjacent page, and the
    reason it scored low is printed next to it so the judgment stays his."""
    if re.search(SUBJECT[brand], term, re.I):
        return 1.0, ""
    return 0.35, "off-subject for this brand"


def commercial(term, brand):
    for weight, label, pat in TIERS[brand]:
        if re.search(pat, term, re.I):
            return weight, label
    return DEFAULT_TIER


def winnability(inc):
    if not inc or inc.get("position") is None:
        return 0.80, "no known incumbent"
    p = inc["position"]
    who = inc.get("who", "incumbent")
    if p > 30:  return 1.00, f"{who} holds it weakly at {p} - open goal"
    if p > 10:  return 0.85, f"{who} at {p} - beatable"
    return 0.70, f"{who} at {p} - strong incumbent, but that is proof of demand"


def slugify(term):
    return "/" + re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-") + "/"


def head(url):
    """404 means a real gap. Returns (code, final_url) - a 200 reached by redirect is not the
    same thing as the page existing. /dashboard-design/ 301s to a GERMAN post, which a plain
    status check reports as a healthy 200."""
    req = urllib.request.Request(url, method="HEAD", headers=UA)
    try:
        r = urllib.request.urlopen(req, timeout=20)
        return r.getcode(), r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, url
    except Exception:
        return None, url


def gsc_guardrail(brand, days=180):
    """Queries the site ALREADY ranks top-10 for. The one thing GSC is genuinely good for:
    stopping a new page from being built on top of a ranking that already works."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "analytics" / "scripts"))
    import datetime, ga_client
    end = datetime.date.today() - datetime.timedelta(days=3)
    start = end - datetime.timedelta(days=days)
    prop = os.environ.get("GSC_ODDTOE_SITE_URL", SITES[brand] + "/") if brand == "oddtoe" \
        else SITES[brand] + "/"
    body = {"startDate": str(start), "endDate": str(end),
            "dimensions": ["query", "page"], "rowLimit": 25000}
    req = urllib.request.Request(
        "https://www.googleapis.com/webmasters/v3/sites/"
        f"{urllib.parse.quote(prop, safe='')}/searchAnalytics/query",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {ga_client.get_token()}",
                 "Content-Type": "application/json"})
    rows = json.load(urllib.request.urlopen(req)).get("rows", [])
    return [{"query": r["keys"][0], "page": r["keys"][1], "position": round(r["position"], 1),
             "impressions": r["impressions"]}
            for r in rows if r["position"] <= 10 and r["impressions"] >= 20]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brand", choices=sorted(SITES), default="datalabs")
    ap.add_argument("--limit", type=int, default=3)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-gsc", action="store_true", help="skip the cannibalisation guardrail")
    a = ap.parse_args()

    universe = json.loads((REF / "keyword-universe.json").read_text())
    queue = json.loads((REF / "queue.json").read_text())["items"]

    # A term already in the queue is not a new candidate - it is already decided.
    claimed = {q["term"].lower() for q in queue if q.get("term")}
    claimed_tokens = [(q["title"], tokens(q["title"] + " " + (q.get("term") or ""), stemmed=True))
                      for q in queue if q["status"] != "dropped"]

    cands = [t for t in universe["terms"]
             if t["brand"] == a.brand and not t.get("exclude")
             and t["term"].lower() not in claimed]
    excluded = [t for t in universe["terms"] if t["brand"] == a.brand and t.get("exclude")]

    # Live gap check, in parallel - this is the expensive part.
    urls = [SITES[a.brand] + (t.get("slug") or slugify(t["term"])) for t in cands]
    with ThreadPoolExecutor(max_workers=8) as ex:
        probes = list(ex.map(head, urls))

    guard = []
    if not a.no_gsc:
        try:
            guard = gsc_guardrail(a.brand)
        except Exception as e:
            print(f"(guardrail unavailable: {type(e).__name__}: {e})", file=sys.stderr)

    scored, retrofits, covered = [], [], []
    for t, url, (code, final) in zip(cands, urls, probes):
        vol = t.get("volume") or 0
        demand = math.log10(max(vol, 10))
        cw, clabel = commercial(t["term"], a.brand)
        ww, wlabel = winnability(t.get("incumbent"))
        comp = COMPETITION.get((t.get("competition") or "").upper(), 0.85)

        redirected = final.rstrip("/") != url.rstrip("/")
        if t.get("served_by"):
            gap, glabel = 0.0, f"already served by {t['served_by']} - retrofit that page"
        elif code == 200 and redirected:
            gap, glabel = 0.65, f"301s to {final.replace(SITES[a.brand], '') or '/'} - check that is the right destination"
        elif code == 200:
            gap, glabel = 0.0, "page already exists - retrofit it, do not build a rival"
        elif code in (404, 410):
            gap, glabel = 1.0, "slug is a confirmed 404"
        else:
            gap, glabel = 0.50, f"could not confirm (HTTP {code})"

        # Anything the site already ranks top-10 for and shares real terms with.
        do_not_target = sorted(
            [g for g in guard if len(tokens(g["query"]) & tokens(t["term"])) >= 2],
            key=lambda g: g["position"])[:5]

        rw, rlabel = relevant(t["term"], a.brand)
        row = {"term": t["term"], "volume": vol, "competition": t.get("competition"),
               "cpc": t.get("cpc"), "proposed_slug": t.get("slug") or slugify(t["term"]),
               "http": code, "gap": glabel, "commercial": clabel, "winnability": wlabel,
               "score": round(demand * cw * gap * ww * comp * rw, 2),
               "relevance": rlabel, "final_url": final if redirected else None,
               "do_not_target": do_not_target,
               "note": t.get("note"), "source": t.get("source"),
               "already_queued_similar": [
                   title for title, tk in claimed_tokens
                   if len(tk & tokens(t["term"], stemmed=True)) >= 2]}
        if row["already_queued_similar"]:
            covered.append(row)
        elif gap == 0.0:
            retrofits.append(row)
        else:
            scored.append(row)

    # Near-duplicate collapse: "data analytics courses" and "classes for data analysis" are
    # ONE page. Keep the best scorer, hang the rest off it as sibling forms.
    scored.sort(key=lambda r: -r["score"])
    kept, seen = [], []
    for r in scored:
        tk = tokens(r["term"], stemmed=True)
        dup = next((k for k, ktk in seen if len(ktk & tk) >= 2), None)
        if dup:
            dup.setdefault("sibling_forms", []).append(
                {"term": r["term"], "volume": r["volume"]})
        else:
            kept.append(r); seen.append((r, tk))

    out = kept[: a.limit]
    if a.json:
        print(json.dumps({"brand": a.brand, "generated_from": universe["captured"],
                          "candidates": out, "retrofit_instead": retrofits,
                          "already_in_flight": [{"term": c["term"], "covered_by":
                                                 c["already_queued_similar"][0]} for c in covered],
                          "universe_exhausted": not out or out[0]["score"] < EXHAUSTED,
                          "excluded": [{"term": e["term"], "why": e["exclude"]} for e in excluded]},
                         indent=1))
        return

    print(f"\nNEXT CONTENT - {a.brand}, demand data captured {universe['captured']}")
    print("=" * 78)
    for i, r in enumerate(out, 1):
        cpc = f" - CPC ${r['cpc']}" if r.get("cpc") else ""
        print(f"\n{i}. {r['term']}   [score {r['score']}]")
        print(f"   {r['volume']:,}/mo AU - {r['competition'] or 'competition unknown'}{cpc}")
        print(f"   proposed: {r['proposed_slug']}  ({r['gap']})")
        print(f"   commercial: {r['commercial']}")
        if r["relevance"]:
            print(f"   ! {r['relevance']} - heavily penalised, your call whether it earns a page")
        print(f"   winnable: {r['winnability']}")
        if r.get("sibling_forms"):
            sib = ", ".join(f"{s['term']} ({s['volume']:,})" for s in r["sibling_forms"])
            print(f"   same page, other forms: {sib}  - build ONE, not several")
        if r["do_not_target"]:
            print("   DO NOT BID FOR (already ranking):")
            for g in r["do_not_target"][:3]:
                print(f"     - \"{g['query']}\" pos {g['position']} on "
                      f"{g['page'].replace(SITES[a.brand], '')}")
        if r["note"]:
            print(f"   note: {r['note']}")
    if not out or out[0]["score"] < EXHAUSTED:
        print("\n** The validated demand for this brand is close to harvested. **")
        print("   Nothing left scores above the build threshold. The honest recommendation is")
        print("   a fresh DataForSEO sweep to refill references/keyword-universe.json, not a")
        print("   filler page. See skills/analytics/SKILL.md for the Playground method.")
    if covered:
        print("\n" + "-" * 78)
        print("Already in flight - not offered again:")
        for c in covered:
            print(f"   - {c['term']} ({c['volume']:,}/mo) -> {c['already_queued_similar'][0]}")
    if retrofits:
        print("\n" + "-" * 78)
        print("NOT new pages - the page exists. Retrofit these instead:")
        for r in sorted(retrofits, key=lambda x: -(x["volume"] or 0)):
            print(f"   - {r['term']} ({r['volume']:,}/mo) -> {r['gap'].replace('already served by ', '').replace(' - retrofit that page', '')}")
    if excluded:
        print("\nExcluded by the universe file:")
        for e in excluded:
            print(f"   - {e['term']}: {e['exclude']}")
    print()


if __name__ == "__main__":
    main()
