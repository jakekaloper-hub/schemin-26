# SCHEMIN WORLD — LAYERED ATLAS ARCHITECTURE V1

**Status:** PROPOSED / WORKING ARCHITECTURE  
**Purpose:** Make all Schemin visual and narrative locations coexist in one persistent world without reverse-engineering geography from mascots.

## 1. Canonical spatial hierarchy

```
SCHEMIN WORLD
  └─ Principal narrative theater / subcontinent
      ├─ Physical zones
      ├─ Civil jurisdictions and institutions
      ├─ League division overlays
      ├─ Owner domains
      ├─ Settlements / landmarks
      ├─ Roads / waterways / passes
      ├─ Encounter locations
      └─ Sets / interiors / props
```

The hierarchy is additive. Lower layers inherit the constraints of higher layers.

## 2. Five atlas layers

### Layer A — Physical Atlas
Controls:
- elevation;
- watersheds;
- rivers;
- coastlines;
- climate;
- forests;
- wetlands;
- plains;
- storms;
- seasonal movement constraints.

Authority begins with `living-novel/world/PHYSICAL_WORLD.md`.

### Layer B — Civil / Political Atlas
Controls:
- settlements;
- market centers;
- chartered cities;
- estates;
- ports;
- roads;
- bridges;
- Compact institutions;
- tolls;
- ordinary population;
- political jurisdictions.

A civil border may cross a physical zone, but it may not contradict terrain and transport logic.

### Layer C — League / Division Atlas
Controls:
- Burgers;
- Wings;
- Pizza;
- division meeting places;
- divisional traditions;
- League roads/ritual routes where justified;
- shared division heraldry;
- division-specific cultural expression.

These are **League jurisdictions/affiliations**, not automatically sovereign states.

### Layer D — Owner Domain Atlas
Controls for each of the Twelve:
- home base / residence;
- operating territory;
- recurring roads;
- allied or hostile access;
- nearby settlements;
- recurring landmarks;
- visual/environmental associations;
- home Encounter venues.

Owner domain cannot overwrite the physical or civil world simply to match a team name.

### Layer E — Encounter / State Atlas
Controls:
- weekly matchup sites;
- temporary arenas;
- races;
- hunts;
- battlefields;
- ceremonial sites;
- weather events;
- damage;
- road closures;
- captured banners;
- repairs;
- aftermath.

Every Encounter location has a canon state:
- `PERMANENT_CANON`
- `PROVISIONAL_CANON`
- `TEMPORARY_SITE`
- `VISUAL_METAPHOR`
- `SUPERSEDED`

## 3. Existing physical-zone inheritance

The current physical-world model is preserved:
- Northern Spine
- Upper Valleys and Foothills
- Central River Basin
- Western Tablelands
- Eastern Forest and Storm Coast
- Southern Wetlands and Delta
- Inner Sea Littoral

Division borders, owner domains and recurring locations must be mapped onto these or later causally justified subdivisions.

## 4. Coordinate policy

Do not assign false precision.

V1 uses:
- zone;
- region;
- relative direction;
- adjacency;
- route;
- travel class;
- landmark visibility;
- estimated narrative travel band.

Precise mileage/coordinates are optional later and should only be introduced when they improve continuity.

## 5. Travel bands

Suggested production abstraction:
- `LOCAL` — same settlement/domain; minutes to hours
- `REGIONAL` — adjacent region; part of a day to several days
- `CROSS_DIVISION` — multi-region journey; days+
- `EXPEDITION` — difficult terrain/seasonal constraints; story-significant

Transport modifier:
- foot
- horse/mount
- wagon
- river
- sea
- specialized wetland transport
- special established mechanism

The world may refine these bands later. They are continuity controls, not exact gameplay math.

## 6. Horizon continuity

Every exterior visual brief must identify:
- camera direction;
- dominant foreground terrain;
- midground route/settlement;
- background topography;
- persistent landmarks that should or should not be visible.

If a landmark is established on the western horizon of one recurring location, future reverse views must respect that relationship.

## 7. Weather continuity

Weather is a world-state event, not isolated decoration.

Record:
- source region;
- direction of movement;
- affected neighboring regions;
- start/end state;
- flooding/snow/mud/fire consequences;
- road or river effects.

El Niño or other character-linked weather imagery may influence narrative staging, but the wider climate system remains coherent.

## 8. Location record schema

Each persistent place should eventually contain:

```yaml
location_id:
name:
aliases:
canon_status:
atlas_layer:
physical_zone:
division_overlay:
civil_jurisdiction:
owner_domain:
location_type:
terrain:
elevation_band:
water_relationship:
climate:
access_routes:
travel_constraints:
nearby_locations:
visible_landmarks:
architecture:
materials:
vegetation:
recurring_objects:
historical_events:
current_state:
state_last_updated:
source_provenance:
contradictions:
open_questions:
```

## 9. World-state mutation rule

A weekly event may:
- damage;
- flood;
- burn;
- close;
- rebuild;
- rename;
- occupy;
- scar;
- celebrate;
- memorialize;
- abandon;
- restore

a location.

The event must update the location record. The next scene inherits that state unless an explicit recovery event occurred.

## 10. Previsualization resolver

Before final page art, resolve:

1. Where is the scene?
2. Which physical zone contains it?
3. Which division overlay applies?
4. Whose domain, if any, applies?
5. What route brought each principal character there?
6. What is the entering world state?
7. What persistent landmarks/materials belong here?
8. What cannot appear here?
9. What lies beyond the frame?
10. What state changes after the scene?

Unresolved items must be marked; they may not be improvised into canon by the image model.

## 11. Map products

The system should eventually support different map products rather than one overloaded poster:

- Physical World Map
- Civil / Trade Map
- Division Map
- Owner Domain Map
- League Roads / Travel Map
- Weekly Encounter Map
- Historical / Damage-State Map

A publication page may composite these selectively.

## 12. Definition of atlas readiness

Atlas V1 is production-ready when:
- every published recurring location is classified;
- each division has a stable index;
- each owner has a domain relationship;
- all required routes are plausible;
- major landmarks have stable relative geography;
- no published recurring site requires unexplained relocation;
- world-state changes persist;
- blank-map QA can distinguish physical geography from League overlays.
