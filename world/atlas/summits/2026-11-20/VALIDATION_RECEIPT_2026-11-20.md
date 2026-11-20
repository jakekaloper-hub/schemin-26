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

## Upstream PR #322 data defect — resolved in subsequent hardening

The current founder-v2 island topology has **45 edge objects**, but its summary `checks.edge_count` is **41**. Preserve the actual edge records and rederive this field, then run the source's own tests. This handoff was added to PR #322, comment **#7047540118**.

## Test contract

Repeatable Python gate: `python3 world/atlas/summits/2026-11-20/test_atlas_summit.py`. The Python command was **executed successfully** on the connected Mac in a fresh isolated sparse checkout at source commit `edb335df313b1046c2f71d88db1f8cda002b1440` (2026-11-20): `test_atlas_summit.py` returned `PASS_WITH_UPSTREAM_HOLD`, **exit 0**. The independent, more comprehensive repository validator `validate_location_summit.py` was also run against the same checkout and returned `PASS_STRUCTURAL_ONLY`, **exit 0**, including 132 slot-season records, 33 podium checks, and 155 total dossiers/handles. These are structural assertions, not a third-party Umpire signoff.

## Identity control

`CAND-CHAMP-LAST-FIELD` (legacy Central Basin placeholder), `CAND-POST-LAST-FIELD` (Island Foundation arena) and `LAST_FIELD` (island network node) describe one intended championship destination and must not become multiple active locations. No active `world/data/locations.json` mutation performed.

## Continuation: current source-state correction and independent topology gate

Earlier statements above describing the 41-versus-45 discrepancy capture the **original audit finding**, not its current status. The current PR #322 source now declares **45 edges** and actually contains **45**, with **23 nodes**, source topology Git blob `2edc3efcb8e50dba35f851a0a861c785680bffad`. PR #324 now pins this source in `ISLAND_TOPOLOGY_PINNED_SOURCE_V1.json` and reconciles `PLAYOFF_ISLAND_THREE_LAYER_RECONCILIATION_V1.json` to `recorded=45, actual=45, status=RESOLVED_IN_UPSTREAM_PR_322`.

Fresh isolated Mac execution:

- `validate_island_topology_pin.py`: `PASS_TOPOLOGY_SOURCE_LOCK_NOT_WORLD_CANON`, exit 0. Checks all 23 source node identities, the 45 edge IDs, per-node neighbors, directions/modes, status, access policy, Losers' Beach evacuation, and public exclusion from contender housing.
- `test_island_topology_pin.py`: **15/15 PASS**, exit 0. Each adversarial mutation to linked route source, protected access, source hash, map coordinates or site status is rejected.
- `test_atlas_summit.py`: `PASS_STRUCTURAL_SOURCE_RECONCILED`, exit 0.
- `validate_location_summit.py`: `PASS_STRUCTURAL_ONLY`, exit 0.

**Remaining independent release holds:** actual island coastline and route siting, Last Field versioned supersession, modern technology exception, independent Umpire/creative approval, and 2026 postseason outcome publication. Fixing a declared edge count did **not** make a hypothetical source route into a World Engine route.
