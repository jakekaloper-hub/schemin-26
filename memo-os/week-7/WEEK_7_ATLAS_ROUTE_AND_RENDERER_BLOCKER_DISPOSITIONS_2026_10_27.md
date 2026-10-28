# Week 7 — Atlas Blocker Closure and Renderer Capability Decision

**Scope:** Existing Memo OS PR #256. **Evidence:** current world location-control authority matrix, `world/data/routes.json` including `via_location_ids`, `PARENT_SUBLOCATION_REGISTRY.json`, existing renderer capability contracts. **No render, publish or merge.**

## Material correction: LLC travel route FOUND
Earlier graph traversal incorrectly treated each route as a direct endpoint-to-endpoint edge and ignored intermediate `via_location_ids`. Recomputed using ordered waypoints:
`LOC-LLC-BOARDROOM` → `LOC-LLC-STORM-CITY` (ROUTE-INNER-SEA-QUAY) → `LOC-LEAGUE-CHAMBER` (ROUTE-PORT-BASIN-CONNECTOR) → `LOC-BRIDGE-MOUNTAIN-LAKE` (ROUTE-UPPER-BASIN-CONNECTOR) → `LOC-SLOB-FOOTHILL-CAMP` (ROUTE-HEARTHROAD, registered VIA node).
**Graph reachability: PASS.** Each segment is INTERPRETIVE_CANON; mode constraints include port/storm gates, river traffic, seasonal mud, ridge traffic. This is not proof of exact travel time or date-specific safe passage.

Red and HMB also reach `LOC-COMPACT-NEUTRAL-GROUNDS` through existing routes and `ROUTE-COMPACT-GROUNDS`. The parent is PROVISIONAL_CANON and contains an open ceremonial field, arbiter pavilion and arrival roads. **No basketball court exists as a registered feature.** Venue acceptance remains HOLD.

## Governed location decisions under actual authority matrix
The Memo OS may stage a home-ground sub-location and visual metaphor; Visual Production may select **allowed** feature handles. Neither may create a new permanent landmark or use an unknown sublocation handle as approved. The control plane requires `HUMAN_REVIEW_REQUIRED` for unknown handle or material upstream conflict.

| Scene | Disposition | Basis / limitation |
|---|---|---|
| TDS waterfall golf | ACCEPTED WITH CONDITIONS (parent only) | Permanent Waterfall Temple and waterfall/temple/dense vegetation handles exist; temporary golf green is NOT an allowed handle. Golf green HOLD |
| DK tower | ACCEPTED WITH CONDITIONS (parent only) | Stronghold parent exists; aperture and centaur fall geometry require physical/scene review |
| ObiWan training | ACCEPTED WITH CONDITIONS (parent only) | Mountain base exists; training courtyard staging must respect approved features |
| Mud/Chili cypress hunt | ACCEPTED WITH CONDITIONS (parent only) | Mud Dogs swamp and raised-ground handle exist; cypress clearing not registered |
| Red/HMB basketball | BLOCKED at subsite | Compact Neutral Grounds is a plausible neutral parent; no registered court |
| Slob/LLC poker | ACCEPTED WITH CONDITIONS (parent/travel) | Slob camp exists and LLC route graph now reaches it; man-cave interior not registered |
| Pittsy jungle book | BLOCKED by upstream conflict | Book machine/published address Central Basin; Founder locked jungle establishment. Do not replace with invented satellite |

These dispositions do not authorize any new scene handle or character-bearing render.

## Renderer capability decision
`canon/characters/renderer_capabilities_v1.json` declares `NO_PRODUCTION_ROUTE_PROVEN`; current renderer lacks mount-hash and deterministic per-subject binding receipts. `NATIVE_RENDER_REFERENCE_BINDING_V1.json` contains historical file handles but documents stale DK morphology and no raw materialization proof. Local October 18 crop bytes SHA256 12/12 PASS, **not** renderer binding. Existing `RENDERER_ADDRESSABLE_ASSET_CONTRACT_V1.md` requires durable asset identity, output hash, reference lineage and inspectable bytes.
**Disposition: BLOCKED** for claimed certified reference-conditioned production; do not weaken contract or pretend a reference handle proves correct subject binding.

## Actual tests (isolated local checkout)
- Location control plane: 15 tests PASS, exit 0.
- Renderer capability evidence: 2 tests PASS, exit 0.
- Previous character provenance 13, scene direction 11, cinematography routing 3, Creative DNA validator PASS.
These are actual code tests, not authenticated independent Umpire review or actual page-image acceptance.

## Packet application
- P005–P007: travel graph source now found for Duckhook; golf-green subsite and renderer binding HOLD.
- P017–P019: Red/HMB neutral-ground approach reachable; basketball-court handle HOLD.
- P020–P022: LLC arrival path FOUND through Hearthroad VIA node; man-cave interior and renderer binding HOLD.
- P025: Pittsy location hard conflict unchanged.
- All other folios remain PLANNED/HOLD until their specific source/visual gates are satisfied.

**IMPLEMENTED:** Corrected travel graph interpretation and explicit location/renderer dispositions.
**TESTED:** 17/17 location/renderer tests; prior suites recorded separately.
**AUDITED:** Existing authority contracts and route waypoints.
**PROMOTED:** Draft PR only.
**BLOCKED:** Unregistered scene subsites, Pittsy conflict, deterministic renderer subject binding, final fact lock, independent Umpire.
**REMAINING:** governed subsite review, real renderer capability evidence, final source QA. No render, publish or merge.
