# UNIVERSE OS V1.1 BASELINE SNAPSHOT

**Captured:** 2026-09-30
**Repository:** `jakekaloper-hub/schemin-26`
**Canonical branch:** `main`
**Baseline commit:** `2bbe0047b6aa8df39899fcf1461c360c27f6af4e`
**Purpose:** immutable pre-Universe-OS-V1.2 reconstruction point.

## Controlling releases
- World Engine: **V1.1 — RELEASED / ACTIVE**
- Weekly Memo OS: **V5.5**
- Character Control Plane v2: **RELEASE_CANDIDATE / NOT ACTIVE**
- Character authority: current Character Registry + latest Commissioner corrections
- Living Novel: current canonical main state

## Snapshot artifacts
- `UNIVERSE_OS_V1_1_ENTITY_EXPORT.json`
- `UNIVERSE_OS_V1_1_LOCATION_EXPORT.json`
- `UNIVERSE_OS_V1_1_ROUTE_EXPORT.json`
- `UNIVERSE_OS_V1_1_CHARACTER_EXPORT.json`
- `UNIVERSE_OS_V1_1_WORLD_STATE_EXPORT.json`

## Reconstruction sources
- world/data/physical_zones.json
- world/data/divisions.json
- world/data/owner_domains.json
- world/data/locations.json
- world/data/routes.json
- world/data/inhabitant_ontology.json
- world/data/encounter_venue_policy.json
- world/data/world_state_events.json
- world/data/current_world_state.json
- canon/characters/CHARACTER_REGISTRY.yaml
- living-novel/os/geography/world_travel_graph_v1.json

## Current governing facts captured
- 2026 Burgers: ObiWan Jacoby, D0nkey K0ng, TDS, Mud Dogs.
- 2026 Wings: Red Leopards, Slob, Chili, Duckhook.
- 2026 Pizza: LLC, HMB, El Niño, Seven Chins.
- Wilson Look = Arsenal Gorilla Warrior; centaur is superseded.
- TDS current body lock = one body / three serpent heads.
- ObiWan has no championship Belt.
- ObiWan coexists with other Jedi under the latest Commissioner clarification, which will enter V1.2 through governed migration rather than being silently back-written into this V1.1 snapshot.
- Divisions are nonexclusive League-cultural/home-venue overlays.
- TDS and Chili coexist across division affiliation.
- El Niño supports embodied / atmospheric / ambiguous manifestation under V1.1 world doctrine.
- Travel graph is ACTIVE_WORLD_ENGINE_V1_1 and route-backed.

## Rollback rule
If Universe OS V1.2 introduces a blocking regression, restore the machine records represented by these exports and reset controlling registry authority to World Engine V1.1 until the V1.2 defect is repaired.

## Gate -1 reconstruction test
PASS if:
1. all exported sources parse;
2. the 12 owner/domain records remain recoverable;
3. all current locations/routes remain recoverable;
4. current world-state events remain recoverable;
5. character registry raw authority is preserved;
6. the travel graph can be reconstructed.

**PHASE -1 STATUS: SNAPSHOT CREATED — TEST WITH CI BEFORE PROMOTION.**
