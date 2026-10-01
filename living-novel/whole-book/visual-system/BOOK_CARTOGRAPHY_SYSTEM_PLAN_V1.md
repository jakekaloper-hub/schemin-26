# SCHEMIN’ ’26 — BOOK CARTOGRAPHY SYSTEM PLAN V1

**Status:** PREPRODUCTION / ATLAS-DERIVED  
**Spatial authority:** Universe OS V1.2 + Atlas Control Plane V2  
**Cartography law:** the book consumes Atlas truth; it never becomes an independent geography store.

## Map doctrine
The book uses **one cartographic visual language with multiple layer modes**, not unrelated map styles.

Base style:
- hand-drawn engraved/ink relief;
- restrained watercolor/wash for terrain and weather;
- material cues from Archive maps;
- clear labels typeset after rendering;
- no faux GIS precision;
- no invented metric scale;
- abstract orientation consistent with `schemin-local-v1`.

## Layer grammar
Atlas already defines nine layer families. The book expresses them as controlled overlays:

| Atlas layer | Book treatment |
|---|---|
| ATLAS-PHYSICAL | terrain, water, elevation, landform; always foundational |
| ATLAS-CIVIL | settlements, League institutions, Record House/Hall/markets |
| ATLAS-DIVISION | soft cultural hatch/borderless wash; never sovereign boundaries |
| ATLAS-OWNER | owner-domain influence/anchor symbols; no false nations |
| ATLAS-TRAVEL | roads, passes, causeways, sea/river travel |
| ATLAS-ENCOUNTER | resolved event venue markers |
| ATLAS-STATE | damage, repair, closure, active environmental state |
| ATLAS-WEATHER | storms/flood/weather; distinguish El Niño manifestation from ordinary weather |
| ATLAS-HORIZON | what can be seen / visual relationship / distant landmarks |

## Map stack
### M0 — Master World Map
Purpose: answer “Where is everything in relation to everything else?”

Show:
- seven physical regions/zones;
- major hydrology/topography;
- League Chamber / Archive / Hall institutions;
- 12 primary home anchors;
- primary routes;
- selected recurring landmarks.

Hide:
- exact distances;
- unsupported civic boundaries;
- all 48 candidate locations;
- weekly clutter;
- statistics;
- future venues not promoted to canon.

### M1 — Institutional Basin Map
League Chamber, Archive, Hall of Keeping, Pittsy’s Book, Compact Grounds, market/travel connections.
Use early in Chapter I when civic reaction becomes narratively important.

### M2 — Burgers / Upper-to-Wetlands Regional Map
Trade Jedi Mountain Base, Wilson stronghold/Barbershop, TDS Waterfall Temple, Mud Dogs Swamp, bridge, Mire Hill; division overlay only as secondary wash.

### M3 — Wings Regional Map
Red Ruins, Slob foothill/alpine route, Chili Stable, Country Club; emphasize roads and social/economic links.

### M4 — Pizza / Storm-Coast Regional Map
LLC Boardroom + Storm City, Belt Keeper Keep, El Niño/Storm Bowl, Chins Road Commons; emphasize weather/port/basin connections.

### M5 — Roads & Rivalries Map
Travel topology only. Useful as chapter interstitial: Eastern Ascent, Black Cliff, Delta Causeway, Shared March, Upper Basin Connector, etc.

### M6 — Encounter Terrain Maps
Small maps keyed to specific high-value scenes: Southern Wetlands, Mire Hill, Country Club, southern gate/Storm City, alpine wager route.

### M7 — World-Memory Map
Same physical base as M0/M2–M4, with time-coded memory overlays:
- Week 2 LLC intrusion;
- Week 3 Bridge memory;
- Mire Hill scars;
- Country Club chili history;
- Alpine wager receipt;
- Southern Speedway history;
- LLC Storm City weather/protection.

### M8 — Six Roads Forward
End-of-current-manuscript map. Show the six verified upcoming pathways/pressures only. No predicted results.

## Visual distinction between information types
- Geography: black/earth ink + relief.
- Institutions: architectural glyphs.
- Owner domains: emblem/sigil marker + light territorial halo, not hard border.
- Divisions: subtle texture/hatching.
- Routes: line style based on travel class.
- Encounter: numbered seal.
- World memory: translucent scar/repair annotation with date/week.
- Character movement: temporary arrow/route trace only when manuscript explicitly follows movement.
- Narrative importance: composition/label hierarchy, never fake geographic size.

## How many maps is too many?
For the current ~23k-word manuscript:
- 1 master map;
- 3 regional maps;
- 2–4 scene/route maps;
- 1 world-memory map;
- 1 horizon map.

**Recommended current ceiling: ~8–10 distinct map products**, with fragments/crops reused only when they answer a new narrative question.

Do not place a map merely because a location appears.

## Book placement
Front matter:
- M0 master map.

Early body:
- M1 institutional basin only if reader orientation is materially improved.

Chapter II:
- M2 or focused Southern Wetlands route map.
- optional W2 road/attention map.

Chapter III:
- Mire Hill encounter/world-memory inset;
- TDS market/route or LLC storm map only if spatially relevant.

Horizon:
- M8 Six Roads Forward.

Back matter:
- regional M2–M4;
- M5 travel network;
- M7 world-memory composite.

## Map update model
Base maps are stable outputs from active Atlas entities. Weekly changes produce overlay revisions, not redrawn geography.

CHANGE ONCE → rebuild affected Atlas view → rebuild affected book map → QA against stable LOC/ROUTE IDs.

## Production gate
A cartographic brief cannot enter art until:
- all LOC/ROUTE IDs resolve;
- selected Atlas layers are declared;
- unresolved candidates are excluded;
- labels are deterministic;
- no renderer-created geography is accepted as canon.
