# Central Basin Spatial Foundation — Candidate Gate
Status: EXPERIMENTAL / UNPUBLISHED / NO CANON PROMOTION
Authority: Atlas Control Plane V2 and World Engine V1.1 retain all canonical geography. This pilot adds **illustrative metric geometry only**; no real distances or locations are established.

## Baseline
Reuse Mission #175: `world/engine/central_basin_pilot.py`, its original three anchors, and route chains. Source IDs remain authoritative. Preserve `schemin-local-v1` abstract positions unchanged.

## Coordinate proposal
`schemin-local-metric-candidate-v1`: local flat Cartesian metres, X east, Y north, Z up, origin arbitrary. Coordinates and polygons are synthetic *fixtures*, not extrapolations or measurements. No direct projection from `schemin-local-v1` is claimed.

## Gates
G0 existing pilot/source resolved. G1 provenance and approval of any future metric footprint. G2 geometrical validity and ID parity. G3 local drainage and seasonal scenario checks. G4 Memo/Novel/Atlas same-ID parity. G5 independent Umpire QA and approval. G1 and G5 cannot be marked PASS from generated candidate geometry alone.

## Constraints
- Derived fixture may never write `world/data/locations.json`, `routes.json`, `physical_zones.json` or state ledgers.
- Do not use synthetic distances as travel hours or manuscript facts.
- Maintain original three anchors. Speedway and DK Mud Hill are route intermediates, not new mission anchors.
- Hydrology and season fixtures are isolated plausibility tests; not verified geography or observed weather.
- Zero incremental provider spend.

## Later integration
Only after QA: introduce optional geometry field in scene context (preserving existing payloads), add cache invalidation to existing mutation fanout, then optional 3D viewer. No second source of truth.