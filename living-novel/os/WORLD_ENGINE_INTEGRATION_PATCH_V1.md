# LIVING NOVEL OS — WORLD ENGINE INTEGRATION PATCH V1

**Status:** RELEASE CANDIDATE  
**Purpose:** Ensure the Living Novel and Weekly Memo inhabit one geography and one persistent world state.

## 1. Shared identifiers

Novel scenes must use the same:
- location IDs;
- physical-zone IDs;
- division IDs;
- owner-domain records;
- route IDs;
- world-state events

as Memo OS.

A novel-only location may be created only through the same canon-state/provenance process.

## 2. Scene geography contract

Before drafting a scene that materially depends on place, resolve:

```
SCENE_WORLD_STATE
  location_id
  physical_zone_id
  division_id
  owner_domain / jurisdiction
  arrival_route
  entering_state
  season / weather
  visible_landmarks
  known_prior_events
  state_delta_if_any
```

## 3. Travel continuity

Narrative transitions must respect travel class:
- LOCAL
- REGIONAL
- CROSS_DIVISION
- EXPEDITION

Travel time may remain literary rather than numeric, but impossible same-moment relocation is blocked.

## 4. Historical consequence

A location remembers prior canonical events.

Examples at End of Week 3:
- LLC Boardroom retains Week 2 intrusion history.
- Country Club of Jackson retains Week 3 chili humiliation/cleanup requirement.
- Mire Hill retains Week 3 battlefield memory.
- Bridge/Mountain Lake remains a Week 3 decision landmark.

## 5. Novel invention authority

The Founder Directive still permits world invention, but invention must:
- fit the physical atlas;
- receive a stable ID;
- declare canon status;
- preserve provenance;
- avoid retroactive contradiction.

## 6. Character/world separation

The world may shape what a character encounters. It may not redesign the character.

Character canon outranks environmental convenience.

## 7. Memo → Novel handoff

Weekly cycle:

`verified league fact → Memo story treatment → accepted world-state delta → shared World Engine → Novel significance/story architecture`

The Novel may deepen meaning; it cannot silently rewrite the physical event record.

## 8. Regression requirement

A Week 3 scene resolved in Memo OS and Novel OS must point to the same location/state even if prose and page composition differ.

**PHASE 10 NOVEL INTEGRATION: READY FOR CI**


## 9. Venue authority V1.1

Novel scenes translating weekly Encounters must resolve venue through:

`world/encounters/ENCOUNTER_VENUE_RESOLVER_V1.md`

Regular/divisional Encounters use verified home-team environments by default. GOTWs, playoffs and championships use approved neutral sites by default.

The novel may omit the journey, but the travel graph must contain an approved path.

## 10. Inhabitant ontology authority

Before populating a scene, load:

`world/civilization/INHABITANT_ONTOLOGY_V1.md`

A writer may not:
- invent a duck civilization because Duckhook exists;
- invent a race of Belt Keepers or LLC beings;
- make Wilson Look the only gorilla-bodied person if his home society is on-page;
- make Mud Dogs the only sapient swamp canine if his home society is on-page;
- segregate TDS and Chili because their League divisions differ.

El Niño may be the weather event itself only when the scene's world-state record marks `ATMOSPHERIC_MANIFESTATION`.

## 11. Travel graph promotion

`living-novel/os/geography/world_travel_graph_v1.json` is now hydrated from World Engine locations/routes and supports multi-hop path validation.

The prior `SEED_NOT_FULL_MAP` zero-edge state is superseded.
