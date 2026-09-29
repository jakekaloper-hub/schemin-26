# SCHEMIN '26 WORLD ENGINE — EXECUTION ROADMAP TO V1

**Status:** ACTIVE EXECUTION ROADMAP  
**Date:** 2026-09-29  
**Branch:** `world/division-index-foundation-2026-09-29`  
**Program:** Schemin World / Division Index / Persistent Atlas  
**Authority:** Commissioner intent → Project Control Registry → Founder Creative Directive → World Design Principles → Memo OS V5.5 → this roadmap

---

# 0. Mission

Complete a production-ready **Schemin World Engine V1** that makes the following coexist coherently:

- physical world;
- civil/political world;
- Burgers / Wings / Pizza divisions;
- owner domains;
- recurring locations;
- weekly Encounter sites;
- persistent world-state consequences;
- Memo OS;
- Living Novel;
- visual production;
- QA and release governance.

The finished system must make geography, continuity, travel, culture, architecture, world state and visual identity **deterministic enough to guide production without flattening creativity**.

Core doctrine:

> The world determines the image.  
> The image does not determine the world.

---

# 1. Definition of Complete

Schemin World Engine V1 is complete only when all of the following are true:

1. all known Week 1–3 recurring locations are inventoried and canon-classified;
2. the seven-zone physical world is reconciled with League divisions;
3. Burgers, Wings and Pizza each have approved Division Index V1 records;
4. all twelve owners have domain relationships and recurring home/route/location anchors;
5. a persistent Location Registry exists;
6. a World State Ledger records durable weekly consequences;
7. travel/adjacency/horizon/weather rules exist;
8. map/atlas data can be rendered in multiple layers;
9. Memo OS V5.5 can resolve world location/state before page generation;
10. Novel OS can inherit the same geography and world state;
11. a representative Week 1–3 regression suite passes;
12. a canonical Atlas V1 is produced only after QA passes;
13. source/provenance and canon-state rules are enforced;
14. all production-facing systems consume one shared world model rather than independently inventing geography.

---

# 2. Program Governance

## Executive authority
- **Jake / Commissioner** — Founder intent, approval of major lore promotions, final V1 acceptance.
- **Closer** — cross-domain synthesis and gate resolution.
- **Umpire / QA** — independent veto authority on canon, geography and continuity defects.

## Bullpen domain owners
- **Librarian** — provenance, source hierarchy, canon promotion.
- **Cartography** — physical geography, routes, borders, spatial continuity.
- **Architect / Systems** — schemas, state model, world resolver, integrations.
- **Visual Development** — environment fingerprints, material/architectural differentiation.
- **Production Design** — buildings, roads, objects, settlement grammar.
- **Narrative Room** — story utility, travel consequence, cultural coherence.
- **Character Room** — owner/domain integration without character drift.
- **Memo OS** — weekly preproduction integration.
- **Novel OS** — long-form continuity integration.
- **Research Desk** — open-source architecture study and pattern extraction.

## Canon states
Every field is one of:
- `LOCKED_CANON`
- `INTERPRETIVE_CANON`
- `PROPOSED_LORE`
- `OPEN_TERRITORY`
- `SUPERSEDED`

Generated concept art cannot promote canon state.

---

# 3. Current Completed Foundation

The following work already exists on this branch and should be treated as **completed inputs**, not restarted:

- `bullpen/SCHEMIN_WORLD_DIVISION_BOARD_MEETING_2026-09-29.md`
- `world/foundation/SCHEMIN_WORLD_ATLAS_ARCHITECTURE_V1.md`
- `world/divisions/DIVISION_INDEX_SCHEMA_V1.md`
- `world/qa/WORLD_GEOGRAPHY_ACCEPTANCE_SUITE_V1.md`

These establish:
- five-layer atlas architecture;
- Division Index schema;
- food semantic locks;
- geographic QA;
- world/state separation.

---

# 4. Execution Sequence

The program runs through **12 phases**.

No downstream phase may silently bypass an upstream gate.

---

# PHASE 1 — OPEN-SOURCE WORLD SYSTEMS STUDY

## Goal
Extract transferable architecture patterns from mature open-source systems before deep implementation.

## Repositories
Study, at minimum:
- Azgaar/Fantasy-Map-Generator
- Mindwerks/worldengine
- maplibre/maplibre-gl-js
- Turfjs/turf
- inkle/ink

Optional secondary references:
- Logseq
- Neo4j
- Gephi

## Tasks
1. read repository architecture/docs;
2. isolate relevant subsystem patterns;
3. classify each finding:
   - ADOPT PATTERN
   - ADAPT PATTERN
   - REJECT
   - FUTURE CONSIDERATION
4. identify licensing constraints;
5. identify what belongs in Schemin now vs later;
6. produce one reference architecture synthesis.

## Deliverables
- `world/research/OPEN_SOURCE_WORLD_SYSTEMS_STUDY_V1.md`
- `world/research/WORLD_ENGINE_PATTERN_ADOPTION_MATRIX_V1.md`

## Gate 1
Pass when the team can explain:
- what data is authoritative;
- what generation may mutate;
- what rendering may not mutate;
- how spatial QA can become testable;
- how persistent narrative state should propagate.

---

# PHASE 2 — SOURCE & LOCATION EXCAVATION

## Goal
Recover the world that already exists before inventing new geography.

## Tasks
1. inventory all Week 1–3 location evidence;
2. inventory repository world/location references;
3. reconcile official Week 2 and Week 3 publication identities;
4. extract:
   - locations;
   - roads;
   - bridges;
   - waterways;
   - mountains;
   - swamps;
   - clubs;
   - headquarters;
   - raceways;
   - battlefields;
   - halls;
   - recurring skyline landmarks;
5. classify each:
   - PERMANENT_CANON
   - PROVISIONAL_CANON
   - TEMPORARY_SITE
   - VISUAL_METAPHOR
   - SUPERSEDED
6. capture source/provenance and first appearance.

## Deliverables
- `world/canon/PUBLISHED_LOCATION_REGISTER_V1.md`
- `world/canon/LOCATION_PROVENANCE_LEDGER_V1.md`
- `world/qa/WEEK3_RELEASE_ARTIFACT_RECONCILIATION.md`

## Gate 2
No new permanent geography until all known locations are classified.

---

# PHASE 3 — WORLD DATA MODEL

## Goal
Turn the existing world architecture into a persistent machine-readable model.

## Tasks
1. define canonical schemas for:
   - region;
   - division;
   - owner domain;
   - location;
   - route;
   - landmark;
   - event;
   - state mutation;
   - provenance;
2. decide YAML/JSON split;
3. assign stable IDs;
4. define alias/rename behavior;
5. define temporal fields;
6. define state inheritance rules;
7. define canon-state promotion workflow.

## Deliverables
- `schemas/world-region.schema.json`
- `schemas/world-division.schema.json`
- `schemas/world-location.schema.json`
- `schemas/world-route.schema.json`
- `schemas/world-state-event.schema.json`
- `world/data/README.md`

## Gate 3
Schemas validate representative Week 1–3 records without inventing unsupported facts.

---

# PHASE 4 — PHYSICAL ATLAS NORMALIZATION

## Goal
Convert the seven-zone physical world into explicit spatial constraints.

## Tasks
1. normalize:
   - Northern Spine;
   - Upper Valleys/Foothills;
   - Central River Basin;
   - Western Tablelands;
   - Eastern Forest/Storm Coast;
   - Southern Wetlands/Delta;
   - Inner Sea Littoral;
2. define adjacency;
3. define elevation relationships;
4. define watershed flow;
5. define climate relationships;
6. define travel barriers;
7. define dominant route classes;
8. define horizon-scale landmarks;
9. keep precision relative, not false-coordinate exact.

## Deliverables
- `world/atlas/PHYSICAL_ATLAS_V1.md`
- `world/data/physical_zones.yaml`
- `world/data/physical_adjacency.yaml`

## Gate 4
GEO-01, GEO-09, GEO-10 and GEO-11 pass on representative cases.

---

# PHASE 5 — DIVISION GENESIS

## Goal
Build Burgers, Wings and Pizza as League-cultural jurisdictions inside the existing world.

## Order
1. Burgers Division Index V1
2. Wings Division Index V1
3. Pizza Division Index V1

## Tasks per division
Complete:
- spatial footprint;
- environmental fingerprint;
- settlement pattern;
- architecture;
- materials;
- economy;
- food-symbol integration;
- League ritual;
- history;
- member owner relationships;
- recurring locations;
- ordinary civilian life;
- anti-drift rules;
- unlabeled visual grammar tests.

## Semantic locks
- Burgers = hamburgers/burgers
- Wings = chicken wings
- Pizza = pizza

Food symbolism is cultural/heraldic, not novelty terrain.

## Deliverables
- `world/divisions/BURGERS_DIVISION_INDEX_V1.md`
- `world/divisions/WINGS_DIVISION_INDEX_V1.md`
- `world/divisions/PIZZA_DIVISION_INDEX_V1.md`

## Gate 5 — Division Differentiation
Each division passes:
- aerial test;
- street test;
- interior test;
- night test;
- weather test;
- artifact test;
- civilian test;
- owner-domain test.

---

# PHASE 6 — OWNER DOMAIN INTEGRATION

## Goal
Place the Twelve inside the world without turning them into twelve mascot kingdoms.

## Tasks
For each owner:
1. assign domain relationship:
   - territorial;
   - institutional;
   - commercial;
   - mobile;
   - martial;
   - mixed;
2. establish residence/stronghold;
3. establish nearest settlement;
4. establish recurring routes;
5. establish home Encounter venue;
6. establish neighboring owners;
7. record division membership;
8. preserve character canon;
9. define visible regional materials/terrain;
10. distinguish owner identity from division identity.

## Deliverables
- `world/domains/OWNER_DOMAIN_REGISTER_V1.md`
- twelve machine-readable owner-domain records

## Gate 6
All twelve pass:
- character canon;
- geography compatibility;
- division inheritance;
- non-mascot geography;
- travel plausibility.

---

# PHASE 7 — ROUTES, TRAVEL, HORIZONS & WEATHER

## Goal
Make scenes physically coexist.

## Tasks
1. build route network;
2. classify:
   - local;
   - regional;
   - cross-division;
   - expedition;
3. connect known locations;
4. define mountain passes;
5. define river/sea travel;
6. define swamp transport;
7. define route closures;
8. define weather propagation;
9. define landmark visibility relationships;
10. define camera-direction continuity.

## Deliverables
- `world/atlas/ROUTE_AND_TRAVEL_MODEL_V1.md`
- `world/data/routes.yaml`
- `world/data/landmark_visibility.yaml`
- `world/data/weather_regions.yaml`

## Gate 7
No known Week 1–3 scene requires unexplained teleportation or impossible adjacency.

---

# PHASE 8 — WORLD STATE LEDGER

## Goal
Make weekly consequences persist.

## State types
- damage;
- flooding;
- fire;
- rebuilding;
- occupation;
- abandonment;
- banner/ownership change;
- route closure;
- memorialization;
- environmental scar;
- reputation-linked public monument/artifact;
- restored condition.

## Tasks
1. define event→mutation contract;
2. backfill approved Week 1–3 consequences;
3. timestamp all mutations;
4. define recovery/reversal events;
5. ensure next-week inheritance;
6. separate temporary scene decoration from persistent state.

## Deliverables
- `world/state/WORLD_STATE_LEDGER_V1.md`
- `world/data/world_state_events.yaml`
- `world/data/current_world_state.yaml`

## Gate 8
Week 1→2→3 regression proves no unexplained environmental reset.

---

# PHASE 9 — SPATIAL QA AUTOMATION

## Goal
Move geographic consistency from prose-only review toward executable checks.

## Research path
Use Turf.js / GeoJSON concepts where useful.

## Tasks
1. define lightweight spatial geometry representation;
2. test:
   - contains;
   - intersects;
   - adjacency;
   - route crossing;
   - nearest location;
   - rough distance band;
3. integrate with existing acceptance suite;
4. avoid overengineering precision.

## Deliverables
- `world/qa/spatial/`
- executable test fixtures
- machine-readable validation report

## Gate 9
Known-good fixtures pass and known-bad fixtures fail.

---

# PHASE 10 — MEMO OS + NOVEL OS INTEGRATION

## Goal
Make both production systems consume the same world state.

## Memo OS tasks
Add resolver requirements to Page Packets:
- location_id;
- physical_zone;
- division_id;
- owner_domain_id;
- entering_state;
- route_of_arrival;
- camera_direction;
- visible_landmarks;
- forbidden_environment mutations;
- post_scene_state_delta.

## Novel OS tasks
Require:
- travel continuity;
- persistent location memory;
- historical consequence;
- same location IDs;
- same owner/division relationships;
- no separate novel-only geography without canon review.

## Deliverables
- `memo-os/WORLD_ENGINE_INTEGRATION_PATCH_V1.md`
- `living-novel/os/WORLD_ENGINE_INTEGRATION_PATCH_V1.md`

## Gate 10
The same Week 3 event resolves to the same place/state in Memo OS and Novel OS.

---

# PHASE 11 — ATLAS RENDERING & VISUAL PROTOTYPES

## Goal
Render the world only after underlying data is stable.

## Required atlas products
1. Physical Atlas
2. Civil/Trade Atlas
3. Division Atlas
4. Owner Domain Atlas
5. Roads/Travel Atlas
6. Weekly Encounter Atlas
7. Historical/World-State Atlas

## Tasks
1. define map style;
2. define layer priority;
3. define label rules;
4. define scale behavior;
5. define visual legend;
6. create one unlabeled division test image each;
7. create one owner-domain test per division;
8. create one Week 3 state overlay.

## Deliverables
- `world/atlas/ATLAS_V1.md`
- render specs
- prototype outputs

## Gate 11
All GEO-01 through GEO-15 pass.

---

# PHASE 12 — V1 RELEASE & FREEZE

## Goal
Promote a coherent, tested world system into production.

## Tasks
1. Umpire full audit;
2. Librarian provenance audit;
3. character cross-check;
4. division distinctness audit;
5. world-state regression;
6. route/travel regression;
7. Memo OS integration test;
8. Novel OS integration test;
9. render QA;
10. fix defects;
11. rerun full suite;
12. Closer signoff;
13. Commissioner approval where required;
14. merge branch;
15. publish release receipt.

## Deliverables
- `world/qa/WORLD_ENGINE_V1_ACCEPTANCE_REPORT.md`
- `world/SCHEMIN_WORLD_ENGINE_V1_RELEASE_RECEIPT.md`
- `world/PRO_SCHEMIN_WORLD_BIBLE_V1.md`
- `world/atlas/ATLAS_V1.md`

## Gate 12
**WORLD ENGINE V1 = RELEASED**

---

# 5. Dependency Graph

```
OPEN-SOURCE STUDY
        ↓
SOURCE / LOCATION EXCAVATION
        ↓
WORLD DATA MODEL
        ↓
PHYSICAL ATLAS
        ↓
DIVISION GENESIS
        ↓
OWNER DOMAINS
        ↓
ROUTES / WEATHER / HORIZONS
        ↓
WORLD STATE LEDGER
        ↓
SPATIAL QA
        ↓
MEMO + NOVEL INTEGRATION
        ↓
ATLAS / VISUAL PROTOTYPES
        ↓
FULL ACCEPTANCE
        ↓
V1 RELEASE
```

Parallel work is permitted only when shared dependencies are already resolved.

---

# 6. Build Discipline After Every Phase

Every phase follows:

`PLAN → BUILD → TEST → AUDIT → BUG-FIX → POLISH → RETEST → PROMOTE`

No phase is promoted from "file exists."

Each gate requires evidence.

---

# 7. Explicit Non-Goals

Do not:
- redraw the final map early;
- replace the physical world with random procedural generation;
- literalize food into landscape;
- let generated artwork become canon by repetition;
- create owner mascot kingdoms;
- introduce precise coordinates before continuity needs them;
- rebuild the character system;
- duplicate Memo OS/Novel OS geography;
- adopt Neo4j or heavy infrastructure before the ontology stabilizes;
- silently retcon published artifacts;
- treat an aesthetically pleasing map as proof of geographic coherence.

---

# 8. Completion Metrics

Program completion should be measurable:

- 3/3 Division Indexes approved
- 12/12 owner domains resolved
- 100% known recurring locations classified
- 100% known persistent consequences represented
- 0 unexplained recurring-location relocations
- 0 untracked canon promotions from image generation
- 0 duplicate geography systems between Memo and Novel
- GEO-01…GEO-15 all PASS
- spatial regression suite PASS
- Week 1–3 replay PASS
- one canonical V1 release receipt committed

---

# 9. Immediate Work Queue

The next executable queue is:

1. Phase 1 — Open-source study
2. Phase 2 — location/source excavation
3. Phase 3 — schemas
4. Phase 4 — physical atlas normalization
5. Phase 5 — Burgers Division Index
6. QA + retest
7. Wings Division Index
8. QA + retest
9. Pizza Division Index
10. QA + retest
11. continue through Phases 6–12 without skipping gates

The Bullpen should continue autonomously until a legitimate Founder approval gate or source conflict is reached.

---

# 10. Governing Standard

The success condition is not:

> "We made a cool fantasy map."

It is:

> "Every future Schemin scene, Memo page, novel chapter and world illustration can be placed inside one persistent, causally coherent universe that remembers what happened before."

