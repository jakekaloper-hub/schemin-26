# Story Production Graph V1 — Groundskeeper Operations Runbook

**Status:** implementation-candidate operating procedure under Issue #306.  
**Does not override:** Project Control, Memo OS, Character Canon, World Engine/Atlas, data release, Umpire or publication gates.

## Weekly operating objective
Reduce manual re-creation and correction by translating existing accepted/provisional weekly source packets into one dependency-aware graph.

## Run order
1. Read active Project Control + weekly source/data release state.
2. Adapt matchup cards into Event envelopes.
3. Adapt cards into Encounter objects.
4. Adapt written storyboard beats into Scene objects.
5. Run provenance/security/authority checks.
6. Build Chronicle projections as disposable read models.
7. Build compiler manifest and dependency edges.
8. Determine ready vs blocked jobs.
9. Pass ready jobs to existing Render Adapter only.
10. Store artifact lineage + QA receipt.
11. After accepted publication only, propose governed world-memory writeback.

## Fail-closed conditions
- source/data release state is HOLD and a consumer requests ACCEPTED canon;
- missing active Character Canon reference for a depicted principal;
- missing active LOC/world packet for a location-bearing scene;
- scene attempts to mutate upstream authority;
- public artifact contains Mercer-private intelligence;
- renderer output is used as evidence for its own factual/canon claim;
- dependency edge is missing for a result-dependent artifact;
- output is marked published without existing publication authority.

## Partial-recompile policy
A changed dependency invalidates its transitive downstream nodes only.

Examples:
- final score correction -> result event fields -> resolution scenes / scoreboard / standings / result-sensitive copy;
- character reference supersession -> scenes/jobs depicting that character;
- location-state correction -> scenes/jobs at that LOC;
- typography-only layout fix -> affected presentation jobs, not league Event truth;
- soundtrack revision -> motion/audio jobs only.

## Operational KPIs
- manual rebuild rate;
- correction/re-render rate;
- event-to-scene coverage;
- provenance completeness;
- character-reference reuse rate;
- location-anchor reuse rate;
- stale artifact rate after source corrections;
- selective invalidation precision;
- average artifacts produced per accepted scene;
- percentage of blocked jobs blocked for a correctly identified upstream gate.

## Week 9 conformance target
All six matchup cards and all written storyboard pages must translate without modifying source Week 9 files. Scores may remain represented while Data Release is HOLD, but events remain BRANCHABLE and world writeback stays disabled.
