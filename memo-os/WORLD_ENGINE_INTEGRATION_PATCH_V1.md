# WEEKLY MEMO OS — WORLD ENGINE INTEGRATION PATCH V1

**Status:** RELEASE CANDIDATE / SUBORDINATE TO MEMO OS V5.5  
**Purpose:** Bind weekly page production to the Schemin World Engine without creating a second Memo OS.

## 1. Resolver gate

Before `STORY_ROOM` may approve a visual page containing an exterior, recurring place, travel transition or physical consequence, the Page Packet must resolve:

- `location_id`
- `physical_zone_id`
- `division_id` when applicable
- `owner_domain_id / character_id` when applicable
- `entering_world_state`
- `route_of_arrival` when travel matters
- `camera_direction`
- `visible_landmarks`
- `forbidden_environment_mutations`
- `post_scene_state_delta`

## 2. Source contract

Use:
- `world/data/physical_zones.json`
- `world/data/divisions.json`
- `world/data/locations.json`
- `world/data/owner_domains.json`
- `world/data/routes.json`
- `world/data/current_world_state.json`

No page may create a parallel location name when an existing location ID applies.

## 3. New-location rule

If no existing location fits, classify the page location as:
- PROVISIONAL_CANON
- TEMPORARY_SITE
- VISUAL_METAPHOR

A provisional location cannot become permanent because generated art repeats it.

## 4. World-state writeback

After Page Lock:
- approved physical consequences are written as proposed state events;
- Umpire/Librarian confirms classification and provenance;
- only then does `current_world_state` advance.

Scores, standings and league facts remain under existing FACT_LOCK.

## 5. Character firewall

World Engine does not alter character identity.

Current hard examples:
- Jake Kaloper: NO championship belt.
- Wilson Look: Arsenal Gorilla Warrior; no centaur/equine anatomy.
- Phillip Pitts: one body with three serpent heads.

Character Control Plane remains authoritative.

## 6. Week 4+ page packet addition

```
WORLD_RESOLUTION
  location_id:
  physical_zone_id:
  division_id:
  owner_character_id:
  route_of_arrival:
  entering_world_state:
  camera_direction:
  visible_landmarks:
  forbidden_mutations:
  post_scene_state_delta:
```

Missing required values = PREVIS BLOCK, not image-model improvisation.

## 7. Regression requirement

Every weekly release must prove:
1. recurring locations did not move;
2. inherited damage/cleanup/weather state is respected;
3. routes and terrain are plausible;
4. division environment is recognizable without labels;
5. newly invented scenery is not silently promoted.

**PHASE 10 MEMO INTEGRATION: READY FOR CI / V5.5 COMPATIBILITY REVIEW**


## 8. Encounter Venue Resolver V1.1

Before Story Room chooses an environment, classify the matchup:
- REGULAR
- DIVISIONAL
- GAME_OF_THE_WEEK
- PLAYOFF
- CHAMPIONSHIP

Then resolve venue from `world/data/encounter_venue_policy.json`.

Rules:
- regular/divisional → verified home-team domain by default;
- GOTW/playoff/championship → approved neutral site by default;
- home/neutral override requires recorded approval;
- if provider home/away is unresolved, venue remains unresolved rather than guessed;
- away side must have an approved route path.

## 9. Inhabitant ontology load

Environment packets must load `world/data/inhabitant_ontology.json` before adding civilians/background inhabitants.

This prevents:
- cloning singular beings into populations;
- isolating peopled-kind owners as unique monsters;
- treating League divisions as species borders;
- erasing TDS/Chili cross-divisional coexistence.

El Niño weather scenes must explicitly mark:
`EMBODIED | ATMOSPHERIC_MANIFESTATION | AMBIGUOUS | ORDINARY_WEATHER`.

## 10. V1.1 world packet

```
WORLD_RESOLUTION
  matchup_class:
  verified_home_team_id:
  venue_mode:
  location_id:
  neutral_override_reason:
  physical_zone_id:
  division_id / division_presence_ids:
  owner_character_id:
  inhabitant_ontology:
  route_of_arrival:
  route_path_valid:
  entering_world_state:
  weather_state:
  el_nino_manifestation_state:
  camera_direction:
  visible_landmarks:
  forbidden_mutations:
  post_scene_state_delta:
```

Missing home/neutral/route resolution = PREVIS BLOCK.
