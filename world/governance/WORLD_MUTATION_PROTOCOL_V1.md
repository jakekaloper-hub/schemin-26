# WORLD MUTATION PROTOCOL V1

**Status:** RELEASE CANDIDATE

## Purpose
Unify durable Universe OS changes without replacing the active Atlas Phase 5 Weekly World Evolution Engine.

## Mutation classes
### A — active state/history
Examples: damage, cleanup, contamination, repair, memorialization, route condition memory.
Execution: delegate to `world/evolution/engine/world_evolution.py`.
Approvals: verified release + Umpire + Closer.

### B — candidate evidence
Attach evidence to an existing CAND-* record. No active geography change.

### C — candidate promotion / new active geography
Requires complete proposed LOC/ROUTE payload, Umpire, Closer and Commissioner approval. Never implicit.

### D — ontology / authority migration
Examples: principal population clarification, source hierarchy change, schema migration.
Requires migration-ledger entry and regression fanout.

## Required request fields
REQUEST_ID, SOURCE, REQUESTER, CURRENT_STATE, PROPOSED_STATE, WHY, CANON_CLASS, CONFIDENCE, AFFECTED_ENTITIES, AFFECTED_LOCATIONS, AFFECTED_ATLAS_LAYERS, AFFECTED_SYSTEMS, MIGRATION, TESTS, ROLLBACK, APPROVALS, RESULT.

## Spatial propagation
A mutation must declare affected Atlas layers:
- route closure → Roads/Travel + Encounter + State;
- flood → Physical consequences + Weather + State + Travel;
- bridge construction → Civil + Travel + Visibility;
- building damage → Civil + State + Memory;
- rename → all consumer-facing views.

## Anti-automation
No renderer, draft Memo, or Novel prose may call an active mutation implicitly.
