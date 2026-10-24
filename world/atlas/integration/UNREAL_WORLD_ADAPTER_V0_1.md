# Schemin ’26 — Unreal World Adapter v0.1

**Status:** RELEASE CANDIDATE / local prototype; no canonical promotion.  
**Authority:** World Engine + Atlas own world truth. Character Canon owns morphology. Memo/Novel own publication semantics. Umpire owns acceptance.

## Decision

Unreal Engine is a **derived spatial/cinematic client of the existing Schemin reality**, not an alternate World Engine, Atlas, or character generator. The local macOS prototype at `~/Developer/ai/Schemin_UE_Prototype` is an engineering worktree, not canon.

Flow: `world/data + canon + governed events → versioned read-only export → provenance validation → Unreal preview scenes → evidence + QA → release`.

The current local prototype has 23 location proxy maps, one Atlas overview, a walkable-test map, and a blank Sequencer asset. These are **development blockouts**, not finished or canon-approved visuals.

## Authority and risk

1. Source files include `world/data/locations.json`, `world/data/routes.json`, `world/data/world_state_events.json`, World Engine V1.1, Atlas V2, location-control-plane and character canon. Resolve conflicts through existing release/control hierarchies.
2. Preserve each location's original `canon_status`. Never silently promote provisional or interpretive records.
3. `schemin-local-v1` coordinates are **abstract/non-metric**: do not infer real dimensions, heightmaps, distance, travel time, or building dimensions.
4. No character-bearing Unreal assets until independently verified visual-reference bytes, source hash, subject binding and visual QA.
5. No live ESPN authority inferred from exported or historical data.
6. Unreal state never writes to Canon or World Engine automatically.
7. Prototype uses no new required paid subscriptions; do not commit DerivedDataCache, Saved, Intermediate or exported media to the canonical repository.

## Next build gates

- **A — Export:** generate deterministic versioned manifest with canonical commit, source path/sha256, stable location IDs, source status, owner IDs, abstract coordinates, named landmarks and rejected unknown records.
- **B — Ingest:** Unreal Editor verifies pinned manifest and creates idempotent location blockouts in a dedicated `/Game/ScheminPreview/` namespace. Emit asset receipts.
- **C — Spatial fidelity:** separately resolve metric scale, routes and hierarchy through approved Atlas/location controls before promoting terrain and architecture.
- **D — Visual studio:** shared art kits, lighting, cameras, Sequencer tracks, render checks, and provenance-labelled previews.
- **E — Living events:** read-only historical/verified event shadow replays; check event classification, venue resolver, chronology and consequences before scene changes.
- **F — Release:** repeatable CI/data tests, Mac play-mode performance, independent Umpire acceptance, publication packaging, and explicit promotion.

No gate completion may be inferred from merely saving a `.umap` or `.uasset`.

## Repository placement

Keep contracts and approved exporters under the existing `world/atlas/integration/` domain. Keep machine control in `governance/` only after placement review; keep Mac-specific UE assets in the isolated prototype repository or designated large-asset storage. Do not introduce an additional top-level Unreal OS.

## Proof of concept, not fact promotion

Initial pinned prototype evidence: main commit `7afe7ef0fcf24e25d67ca8c85d4e6e36e03a78e3`, source `world/data/locations.json`, 23 records (8 permanent, 12 provisional, 3 interpretive). These counts are snapshot-specific, not permanent world invariants.
