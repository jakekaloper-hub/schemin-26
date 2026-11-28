# ROUTE, TRAVEL, HORIZON & WEATHER MODEL V1

**Status:** INTERPRETIVE CANON / WORLD ENGINE V1.1

## Travel classes

- **LOCAL:** same settlement/domain network.
- **REGIONAL:** adjacent physical regions or established regional corridor.
- **CROSS_DIVISION:** League-cultural boundary crossing; may still be geographically ordinary.
- **EXPEDITION:** difficult mountain/wetland/seasonal passage.

These are narrative continuity bands, not exact mileage.

## Governing travel graph

The old Novel OS geography seed is superseded operationally.

`living-novel/os/geography/world_travel_graph_v1.json`

now carries approved nodes/edges derived from:
- `world/data/locations.json`
- `world/data/routes.json`

Status must not regress to `SEED_NOT_FULL_MAP`.

## Route law

A recurring/home/neutral location must:
1. touch an approved route; or
2. be explicitly isolated with a specialized access rule.

A traveler may use a multi-hop route chain. Novel OS validates a minimum feasible path rather than requiring every journey to be one direct edge.

## Terrain-path law — Founder directive, 28 November 2026

All terrestrial travel paths are unpaved and follow their Atlas physical zone. No asphalt or concrete paved roads, painted lanes, or generic modern highway guardrails. Vehicles, where explicitly permitted, do not imply a paved road. Existing bridges, docks, quays and other separately established crossing structures retain their identities. Natural exposed stone is terrain, not paving.

- **REG-NORTHERN-SPINE:** Exposed natural rock, scree and worn mountain trails; snow or ice when season and elevation warrant.
- **REG-UPPER-VALLEYS:** Compacted earth, gravel, forest leaf litter, pasture tracks and natural fieldstone exposed in the ground.
- **REG-CENTRAL-BASIN:** Worn alluvial earth, clay or gravel tracks; seasonal mud and ruts where supported by weather and drainage.
- **REG-WESTERN-TABLELANDS:** Dry dusty earth, broken rock and grassland tracks; localized mud only when rainfall supports it.
- **REG-EASTERN-STORM-COAST:** Wet forest earth, roots, gravel and exposed bedrock; rain washouts and natural drainage.
- **REG-SOUTHERN-WETLANDS:** Raised earthen causeways, muddy tracks and established timber crossings where required; respect floodwater and boat access.
- **REG-INNER-SEA-LITTORAL:** Compacted coastal earth, sand, gravel and exposed stone; retain established quays and bridge structures as distinct from road surfacing.

These are visual/material constraints, not new route edges, permissions, exact surface surveys or geographic placements. An unresolved segment must remain unplaced. See `memo-os/week-12/W12_FOUNDER_TERRAIN_PATH_CORRECTION_2026-11-28.json`.

## Home-host travel law

For ordinary matchups:
- home team remains at/within home environment;
- away side must have an approved route chain to the venue;
- lack of path blocks production.

The journey need not appear in prose or art.

## Neutral-event travel law

GOTW/playoff/championship neutral sites must be reachable from both participants through the approved graph.

Neutral does not mean teleportation.

## TDS + Chili coexistence

The Shared March is an explicit cross-divisional route/social corridor:
- TDS remains Burgers;
- Chili remains Wings;
- shared residence/social space is permitted.

This proves divisions do not act as biological or residential walls.

## Horizon law

Exterior briefs record:
- camera direction;
- foreground terrain;
- midground road/settlement;
- background topography;
- stable landmark visibility.

## Weather law

Weather propagates through regions and watersheds.

El Niño has a special approved dual mode:
- embodied Weather System; or
- explicitly resolved atmospheric manifestation.

Ordinary storms remain ordinary unless tagged otherwise.

## Minimum-time doctrine

Machine graph `min_hours` values are conservative narrative lower bounds used to reject impossible same-moment travel.

They are not canonical exact durations.

**V1.1 ROUTE/TRAVEL GATE: ACTIVE**
