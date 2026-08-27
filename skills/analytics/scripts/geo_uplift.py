#!/usr/bin/env python3
"""Estimate the CLICKS a GEO retrofit could add to an existing page.

Replaces the index-score in geo-retrofit-rank.py, which ranked on raw Search Console
impressions. Otto, 26 Aug 2026, after those impressions turned out to be contaminated:
"Can you get this GEO Retrofit in order to make better assumptions or do the proper math?"

    extra_clicks = clean_impressions x (benchmark_ctr(position) - current_ctr)
                                     x geo_headroom x commercial_weight

Every term is a real quantity, and the output is clicks per 180 days, not an index.

  clean_impressions  Search Console impressions minus machine-shaped queries. The filter is
                     on query FORM only (quotes, boolean operators, negation, unnatural
                     length) and never on click performance — using CTR to decide what is
                     real, then feeding CTR back into the estimate, would be circular.
  benchmark_ctr      what a page at that position normally earns. The gap between benchmark
                     and actual is the recoverable part.
  geo_headroom       share of the in-scope elements still missing. A page at 4/4 scores 0 —
                     the retrofit has nothing left to add, whatever its traffic.
  commercial_weight  how few steps to a booking, weighted to Otto's named service lines.

Clicks are the human anchor: only a person clicks, so a page with impressions and no clicks
across a long window is either mis-serving its queries or being counted by machines. Both
mean those impressions are not bankable, and `contamination` reports the share dropped.
"""
from __future__ import annotations
import re

# Position -> CTR a page at that rank typically earns. Deliberately conservative: these are
# below most published curves, so the estimate under-promises rather than over-promises.
CTR_CURVE = [(1.5, .180), (3, .105), (5, .060), (7, .040), (10, .028),
             (15, .016), (20, .011), (30, .006), (40, .004), (999, .002)]


def benchmark_ctr(pos: float) -> float:
    for edge, ctr in CTR_CURVE:
        if pos <= edge:
            return ctr
    return .002


# Query FORM tests. A human types a few words into a box; they do not type quotation marks,
# boolean operators, or six-word stacked noun strings. Validated against the prop-designer
# page, where the excluded cohort had 0 clicks across 2,351 impressions at positions 1-6.
_QUOTE = re.compile(r'["“”]')
_BOOL = re.compile(r'\b(or|and)\b', re.I)
_NEG = re.compile(r'(^|\s)-\w')


def machine_shaped(q: str) -> bool:
    if _QUOTE.search(q) or _NEG.search(q):
        return True
    if len(_BOOL.findall(q)) >= 2:            # "x or y or z" enumeration
        return True
    words = q.split()
    if len(words) >= 6 and not q.rstrip().endswith("?"):
        return True                            # stacked supplier permutations; real long
    return False                               # queries are usually questions


STOP = {"a","an","the","in","for","of","and","or","to","is","are","do","does","what","how",
        "with","on","at","by","near","me","my","your","best","top"}


def _tokens(q: str) -> frozenset:
    return frozenset(w for w in re.findall(r"[a-z0-9]+", q.lower()) if w not in STOP)


def permutation_cluster(query_rows: list[dict], min_shared: int = 3, min_size: int = 5) -> set:
    """Queries that are permutations of one another, en masse, are enumeration not search.

    The tell that cracked this (Oddtoe homepage, 26 Aug 2026): 21 queries reading
    "oddtoe prop maker melbourne", "oddtoe melbourne props", "oddtoe 3d prop designer
    melbourne" ... 1,791 impressions at position 2, two clicks between them. Short, no
    operators, so the form tests miss them entirely — but no person types eighteen
    reorderings of the same four words.

    Returns the set of query strings belonging to a cluster of >= min_size queries that
    each share >= min_shared significant tokens with the cluster's seed. Structural only:
    click behaviour is never consulted, so the result stays independent of the CTR maths.
    """
    toks = {r["query"]: _tokens(r["query"]) for r in query_rows}
    flagged, seen = set(), set()
    for q, tq in toks.items():
        if q in seen or len(tq) < min_shared:
            continue
        members = [o for o, to in toks.items() if len(tq & to) >= min_shared]
        if len(members) >= min_size:
            flagged.update(members)
            seen.update(members)
    return flagged


def clean_demand(query_rows: list[dict], page_impressions: int = 0,
                 page_clicks: int = 0) -> dict:
    """query_rows: [{query, impressions, clicks, position}] for ONE page.

    Search Console withholds rare queries, so the query rows are a SAMPLE — their sums are
    far below the page totals, and clicks are hit hardest (the Oddtoe homepage sums to 2
    clicks against a true 60). So the sample is used only for the two things it estimates
    well, both ratios: what share of impressions are machine-shaped, and where the human
    queries actually rank. Absolute counts come from the page row.
    """
    perms = permutation_cluster(query_rows)
    bad = lambda r: machine_shaped(r["query"]) or r["query"] in perms
    keep = [r for r in query_rows if not bad(r)]
    drop = [r for r in query_rows if bad(r)]
    ki = sum(r["impressions"] for r in keep)
    kc = sum(r["clicks"] for r in keep)
    di = sum(r["impressions"] for r in drop)
    # impression-weighted position over the queries we kept
    pos = (sum(r["position"] * r["impressions"] for r in keep) / ki) if ki else 0.0
    contamination = di / (ki + di) if (ki + di) else 0.0
    # scale the page's TRUE impressions by the sample's machine-shaped share
    clean_impr = round(page_impressions * (1 - contamination)) if page_impressions else ki
    # every click is a human, so page clicks carry over whole
    clicks = page_clicks if page_impressions else kc
    return {"clean_impressions": clean_impr, "clean_clicks": clicks,
            "sample_impressions": ki + di, "sample_share": round((ki + di) / page_impressions, 3)
            if page_impressions else 1.0,
            "contamination": round(contamination, 3),
            "clean_position": round(pos, 1),
            "clean_ctr": round(clicks / clean_impr, 5) if clean_impr else 0.0}


def uplift(clean: dict, geo_have: int, geo_total: int, commercial_weight: float,
           rank_gain: float = 0.75) -> dict:
    """Extra clicks per 180 days if the retrofit lifts this page's rank a little.

    Two different things look like "underperformance" and only one is a CTR problem:

      rank gap  the page sits at 25 for queries people really type. Structure, Q&A depth
                and internal links move rank. This is what the retrofit actually does.
      CTR gap   the page ranks well and still is not clicked. That is a title and snippet
                problem, not something a Q&A block fixes.

    Modelling a modest rank improvement (default: 25% better position) covers both — a page
    already converting at benchmark still gains from ranking higher, and a page converting
    below benchmark gains more. Subtracting the clicks it already earns keeps the figure
    incremental. geo_headroom means a page at 4/4 scores zero: nothing in scope is left.
    """
    ci = clean["clean_impressions"]
    if not ci:
        return {"benchmark_ctr": 0.0, "potential_clicks": 0, "geo_headroom": 0.0,
                "improved_position": 0.0, "extra_clicks_180d": 0.0}
    headroom = (geo_total - geo_have) / geo_total
    improved = max(1.0, clean["clean_position"] * rank_gain)
    potential = ci * benchmark_ctr(improved)
    extra = max(0.0, potential - clean["clean_clicks"]) * headroom * commercial_weight
    return {"benchmark_ctr": round(benchmark_ctr(improved), 4),
            "improved_position": round(improved, 1),
            "potential_clicks": round(potential),
            "geo_headroom": round(headroom, 2),
            "extra_clicks_180d": round(extra, 1)}
