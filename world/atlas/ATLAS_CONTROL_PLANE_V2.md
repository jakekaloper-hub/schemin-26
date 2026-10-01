# ATLAS CONTROL PLANE V2

**Status:** RELEASE CANDIDATE
**Parent:** Universe OS V1.2
**Purpose:** spatial representation, topology and QA over one authoritative world model.

## Core law
The Atlas Control Plane does not create a second geography database. It compiles spatial views from canonical Universe/World data.

## Governing layers
1. Physical Atlas.
2. Civil / Institutional Atlas.
3. Division Atlas.
4. Owner Domain Atlas.
5. Roads & Travel Atlas.
6. Encounter Atlas.
7. World-State Atlas.
8. Weather Atlas.
9. Horizon / Visibility Atlas.

The Phase 1 candidate layer remains editorial-only and hidden by default.

## Responsibilities
- containment and adjacency;
- route/travel topology;
- hydrology relationships when known;
- location layer membership;
- visibility/horizon relationships when known;
- map products;
- spatial QA;
- scene-previs spatial context.

## Non-responsibilities
Atlas does not own:
- principal visual/body canon;
- fantasy scoring/standings;
- prose voice;
- candidate promotion;
- generated names;
- world mutations.

## Existing Location Control Plane
The current `world/location-control-plane/` compiler remains the location-card/consumer adapter. Atlas V2 supplies spatial truth to it; it is not replaced.

## Coordinate policy
Schemin-local coordinates remain abstract and non-metric. No Earth lat/long or exact mileage is implied.

## Maturity
V1.2 requires abstract topology and stable IDs. Structured geometry / GeoJSON / Turf / MapLibre remain later optional tooling and may never outrank world data.

**ATLAS V2 RELEASE GATE: PENDING ACCEPTANCE SUITE**
