# Atlas Summit — Cross-Registry Validation Receipt (2026-11-20)

Status: **STRUCTURAL_PASS_WITH_SOURCE_HOLDS**. Source: connected GitHub live reads of the committed branch, tested in-memory with deterministic assertions. Bullpen routing is separately recorded; this is **not** an independent Umpire acceptance, a local Python CI run or publication evidence.

## Observed registry counts

- mainland_locations: **23**
- mainland_routes: **18**
- legacy_candidates: **48**
- new_candidates: **40**
- new_held_duplicates: **4**
- new_reusable_proposals: **36**
- island_source_handles: **44**
- total_cross_atlas_handles: **155**
- owner_domains: **12**
- history_seasons: **11**
- historical_fixtures_source_bound: **56**
- physical_trace_proposals: **56**

## Actual assertions passed

- PASS — 155 cross-registry IDs distinct
- PASS — Three layers present on all 155 handles
- PASS — 12/12 current owners bind to active 2026 home anchor
- PASS — 40 new proposals exist; 4 speculative island duplicates held; 36 eligible to future review
- PASS — Losers Beach source node present; 11 seasons of nonqualifier/beach outcomes modeled as fiction
- PASS — Island 9 arenas, 23 nodes, 9 dormant heritage remnants, 3 neutral hypotheses indexed
- PASS — 18 active world routes not mutated; 45 source island edges are proposal-only
- PASS — Source internal edge-count mismatch 41 vs 45 is detected and left as upstream defect
- PASS — Last Field original candidate and PR 322 proposal explicitly not merged

## Explicit release blockers

- HOLD — No independent Umpire or Director/author production signoff established by these structural tests
- HOLD — No approved atlas island landform, causeway route or stadium engineering
- HOLD — No World technology exception or public hosted viewer integration
- HOLD — No current 2026 qualification or championship outcome
- HOLD — No evidence that fictional island hosted real 2015–2025 matchups

## Upstream PR #322 data defect

The current founder-v2 island topology has **45 edge objects**, but its summary `checks.edge_count` is **41**. Preserve the actual edge records and rederive this field, then run the source's own tests. This handoff was added to PR #322, comment **#7047540118**.

## Test contract

Repeatable Python gate: `python3 world/atlas/summits/2026-11-20/test_atlas_summit.py`. This source checkout has not been executed through that Python command in this operation; the values above reflect the separately executed equivalent JSON assertions.

## Identity control

`CAND-CHAMP-LAST-FIELD` (legacy Central Basin placeholder), `CAND-POST-LAST-FIELD` (Island Foundation arena) and `LAST_FIELD` (island network node) describe one intended championship destination and must not become multiple active locations. No active `world/data/locations.json` mutation performed.
