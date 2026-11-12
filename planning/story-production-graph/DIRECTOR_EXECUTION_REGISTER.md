# Story Production Graph V1 — Director Execution Register

**Mission:** #306  
**Implementation:** draft PR #307  
**Rule:** a Director lane is COMPLETE only when a repository artifact and corresponding verification exist. Discussion alone does not count.

| Director | Domain deliverable | Current implementation |
|---|---|---|
| Closer | one mission / one North Star / dependency order | Issue #306 + this register |
| Setup Man | deterministic build graph + partial recompilation | `dependency_invalidation.py`, `build_compiler_manifest.py` |
| Scout | verified evidence boundary / HOLD propagation | `adapt_week9_matchups.py` |
| Umpire | fail-closed conformance and negative tests | `tests/test_story_production_graph.py`, `tests/test_director_lanes.py` |
| Beat Writer | source-preserving scene translation | `adapt_week9_scenes.py` |
| Groundskeeper | repeatable weekly operating procedure | `OPERATIONS_RUNBOOK.md` |
| GM | product criterion: reusable multi-surface scene graph, not document count | compiler surfaces + KPIs in runbook |
| Pitching Coach | generation remains downstream of bounded Scene + Render Adapter packets | compiler render-profile mapping; no direct model calls |
| Warden | public/private boundary, dependency restraint | `security_policy.py`; no new dependency |
| Commissioner | league identity/result preservation | Week 9 adapter preserves team/character/result identifiers |
| Analyst | coverage/reuse/risk metrics | `production_metrics.py` |
| Librarian | lineage and supersession/provenance graph | `provenance_graph.py` |
| Agent | cross-surface identity | shared Scene IDs drive PNG/MOTION/WEB/NOVEL_CONTEXT jobs |
| Bookkeeper | reuse before regeneration | encounter anchors inherited once, reused by scenes |
| Commissioner General | publication remains separate authority | compiler `auto_publish_allowed=false` |
| Clubhouse Manager | owner/character boundary | character IDs preserved independently from team names |
| Scout Master | distribution expansion remains downstream | surfaces represented as jobs; no commercialization claim |
| Architect | typed Event/Encounter/Scene/Chronicle/Compiler contracts | schemas + adapters + source mapping |

## Current acceptance state
- Initial and six-matchup adapter tranches passed Repository Merge Gate and Bullpen Runtime CI on their exact HEADs.
- Current Director implementation tranche requires a fresh exact-HEAD CI pass.
- Sports Desk Week 9 source still reports `data_release_status: HOLD`; Event adapter therefore remains provisional/branchable.
- No Project Control promotion.
- No renderer execution.
- No automatic world writeback.
- No publication promotion.

## Next domain work after green CI
1. Generate all four Chronicle projection classes from full Week 9 event/scene data.
2. Introduce dependency classes (RESULT, CHARACTER, LOCATION, COPY, AUDIO) for more precise invalidation.
3. Bind compiler jobs to `planning/render-adapter/render_request_v1.schema.json`.
4. Add accepted artifact lineage receipt shape.
5. Run independent Umpire review on exact HEAD and resolve findings.

## Domain completion update — current branch

### IMPLEMENTED / awaiting exact-HEAD CI
- **Architect:** Event, Encounter, Scene, Chronicle and Compiler schemas; explicit scene source mapping; typed dependency edge schema.
- **Setup Man:** transitive invalidation, minimal rebuild-job selection, typed BASE/RESULT/CHARACTER/LOCATION dependencies, compiler manifest builder.
- **Scout:** six-matchup Week 9 source adapter with Data Release HOLD propagation.
- **Beat Writer:** all Week 9 written storyboard pages adapt into Scene objects; no source rewrite.
- **Librarian:** provenance graph and source lineage edges.
- **Analyst:** coverage/reuse/risk metrics.
- **Warden:** fail-closed private-intelligence scan and no-dependency policy.
- **Groundskeeper:** weekly Story Graph operations runbook and KPIs.
- **Pitching Coach:** compiler-to-existing-Render-Adapter request bridge; blocked jobs cannot emit render requests.
- **Character/Chronicle lane:** 12 character timelines, 6 Week 9 relationship views, 6 place-memory views; artifact custody stays empty when no artifact event exists.
- **Umpire implementation support:** negative tests for authority escalation, private-intelligence leakage, blocked render bridging, and selective invalidation. Independent acceptance is still OPEN and cannot be self-certified by this implementation branch.

### VERIFIED ON EARLIER EXACT HEAD
- Repository Merge Gate: PASS.
- Bullpen Runtime CI: PASS.

### OPEN GATES ON CURRENT HEAD
- fresh Repository Merge Gate;
- fresh Bullpen Runtime CI;
- external Netlify preview status inspection if still failing;
- independent Umpire acceptance;
- Project Control promotion decision;
- actual renderer execution remains out of scope until upstream readiness.
