# LOCATION CONTROL PLANE ARCHITECTURE V1

**Status:** PHASE 2 ARCHITECTURE
**Namespace:** world/location-control-plane/

## 1. Purpose

Provide deterministic, machine-addressable compilation of Schemin location truth for Memo OS, Novel OS and visual production.

## 2. Non-authoritative compiler pattern

The control plane reads:
- world/data/locations.json
- world/data/physical_zones.json
- world/data/divisions.json
- world/data/routes.json
- world/data/owner_domains.json
- world/data/current_world_state.json
- world/data/world_state_events.json
- world/data/landmark_visibility.json
- world/data/weather_regions.json
- world/data/atlas_location_candidates.json

It never mutates these sources during normal packet compilation.

## 3. Directory model

world/location-control-plane/
- _INDEX.md
- AUTHORITY_AND_CONSUMER_MATRIX_V1.md
- schemas/
- registries/
- homelands/{CHAR-ID}/CARD.json
- locations/{LOC-ID}/CARD.json
- compiler/location_control_plane.py
- adapters/memo_adapter.py
- adapters/novel_adapter.py
- qa/test_location_control_plane.py
- qa/PHASE_2_SCENARIO_MATRIX_V1.md

## 4. Resolver contract

### resolve_location(location_id)
Returns:
- CURRENT_LOCATION_RESOLVED;
- HUMAN_REVIEW_REQUIRED / UNKNOWN_LOCATION;
- HUMAN_REVIEW_REQUIRED / CANDIDATE_NOT_ACTIVE.

### resolve_homeland(character_id)
Returns:
- CURRENT_HOMELAND_RESOLVED;
- HUMAN_REVIEW_REQUIRED / UNKNOWN_CHARACTER_DOMAIN.

### resolve_sublocation(handle_id)
Returns a derived landmark handle only.
A handle is not a separate LOC record.

## 5. World Packet compiler

Input:
- location_id;
- character_ids[];
- consumer = MEMO | NOVEL | VISUAL;
- event_class;
- optional sublocation_handle;
- optional home_character_id.

Output:
- authority snapshot;
- location card;
- physical-zone profile;
- division overlay;
- route/access requirements;
- current world state;
- historical event IDs;
- horizon constraints;
- weather-region relationships;
- character/location relationship classes;
- consumer overlay;
- reference status;
- prohibited inventions;
- review blockers.

## 6. Relationship classes

Character vs location:
- HOME_PRIMARY
- HOME_SHARED
- HOME_ASSOCIATED
- AWAY_REACHABLE
- NEUTRAL
- UNKNOWN_RELATIONSHIP

No emotional or psychological interpretation is inferred.

## 7. Sublocation model

Persistent landmarks become addressable handles:

SUB::{LOCATION_ID}::{SLUG}

A handle:
- inherits parent location ID;
- inherits physical zone;
- inherits division relation;
- inherits current world state;
- cannot move independently;
- cannot become canon by generation.

Promotion to a new LOC record requires the Phase 1 unlock framework.

## 8. Reference model

Every active location gets:
- semantic_reference_status;
- visual_reference_status;
- approved_reference_uris[];
- candidate_reference_paths[];
- blockers[].

Default visual status is MISSING_APPROVED_VISUAL_REFERENCE unless a durable approved asset URI is actually registered.

Text description alone is not equivalent to renderer-addressable visual bytes.

## 9. Card generation

Cards are derived snapshots.

Each card records:
- generated_from source paths;
- source schema versions where available;
- compilation version;
- open questions.

Cards may be regenerated when upstream canon changes.

## 10. Candidate firewall

The active resolver only accepts LOC-*.

CAND-* requests return:
HUMAN_REVIEW_REQUIRED / CANDIDATE_NOT_ACTIVE

A future candidate-production adapter may be separate.

## 11. Release boundary

The Location Control Plane is production infrastructure.
It does not change the existing World Engine's authority ranking.

**Architecture doctrine:** sources define reality; packets make reality usable.
