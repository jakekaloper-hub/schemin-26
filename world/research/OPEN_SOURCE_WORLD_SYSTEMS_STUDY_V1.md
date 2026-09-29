# OPEN-SOURCE WORLD SYSTEMS STUDY V1

**Status:** COMPLETE — PHASE 1 STUDY  
**Date:** 2026-09-29  
**Purpose:** Extract transferable architecture patterns for Schemin World Engine V1 without importing another project's world, aesthetics or canon.

## Repositories reviewed

### Azgaar/Fantasy-Map-Generator
Evidence reviewed:
- repository metadata;
- README;
- LICENSE.

Relevant findings:
- mature fantasy map editor/generator;
- explicit future architecture separating:
  - world data and styles;
  - procedural generators;
  - interactive editors/controllers;
  - renderers/views;
- README states renderers should be pure visualization and should not mutate world data;
- editors perform controlled mutations of world state;
- project is MIT-licensed.

Schemin conclusion:
**ADOPT PATTERN.**
Use a strict boundary:
`WORLD DATA → CONTROLLED MUTATION → RENDERING`.
Do not let generated art or map rendering become the source of canon.

### Mindwerks/worldengine
Evidence reviewed:
- repository metadata;
- README;
- LICENSE.

Relevant findings:
- generates world data through staged physical simulation;
- algorithm explicitly models plate effects, precipitation, rain shadow, erosion, humidity, terrain permeability and biomes;
- output is stored as reusable world data and can be rendered into multiple map types;
- supports interoperability and machine-readable persistence;
- MIT-licensed.

Schemin conclusion:
**ADAPT PATTERN.**
Do not procedurally regenerate Schemin. Borrow the causal discipline:
physical geography → climate → ecology → movement constraints → settlement logic.
Use simulation thinking as QA, not as an authority that overrides canon.

### MapLibre GL JS
Evidence reviewed:
- repository metadata;
- README;
- LICENSE.

Relevant findings:
- open-source browser/webview mapping library;
- vector-map rendering;
- style-driven layered map display;
- BSD-style licensing with included upstream notices.

Schemin conclusion:
**FUTURE IMPLEMENTATION CANDIDATE.**
Useful for the eventual interactive Schemin Atlas/app because the same world data can be displayed through selectable layers.
Do not make MapLibre a Phase 1 dependency; stabilize our ontology/data first.

### Turf.js
Evidence reviewed:
- repository metadata;
- README;
- LICENSE.

Relevant findings:
- modular JavaScript geospatial engine;
- operates with GeoJSON;
- supports spatial analysis and geometry helpers;
- runs client- or server-side;
- MIT-licensed.

Schemin conclusion:
**ADAPT / LIKELY ADOPT LATER.**
Use for executable geography QA once minimal geometry exists:
- contains;
- intersects;
- adjacency;
- proximity;
- route plausibility;
- rough distance bands.
Do not introduce false cartographic precision solely to enable GIS.

### inkle/ink
Evidence reviewed:
- repository metadata;
- README;
- LICENSE.

Relevant findings:
- narrative engine separates authored narrative logic from the surrounding game/UI;
- compiles narrative into a runtime representation;
- runtime retains story state and choices;
- explicitly designed to slot into a larger application rather than own the entire application;
- MIT-licensed.

Schemin conclusion:
**ADAPT PATTERN.**
Do not convert the novel into interactive fiction.
Borrow the principle of persistent narrative state:
facts/events mutate state; later scenes inherit that state.

## Cross-repository synthesis

The strongest shared architecture is:

```
AUTHORITATIVE DATA
      ↓
DOMAIN RULES
      ↓
CONTROLLED MUTATIONS
      ↓
PERSISTENT STATE
      ↓
MULTIPLE RENDERERS / CONSUMERS
```

For Schemin:

```
CANON + LEAGUE FACTS + PHYSICAL WORLD
                ↓
         WORLD ENGINE RULES
                ↓
       APPROVED STATE MUTATIONS
                ↓
          WORLD STATE LEDGER
                ↓
  ┌─────────────┼─────────────┐
  │             │             │
MEMO OS      NOVEL OS       ATLAS
  │             │             │
  └─────────────┴─────────────┘
                ↓
               QA
```

## Architecture rules adopted from the study

1. **World data is authoritative; renderers are not.**
2. **Generated or edited visual output never silently mutates canon.**
3. **Mutations must be explicit, typed and provenance-bearing.**
4. **Physical-world causality precedes cultural decoration.**
5. **One persistent state should feed multiple outputs.**
6. **Spatial validation should become executable when geometry is mature enough.**
7. **Narrative consequences must persist as state instead of relying on prose memory.**
8. **Interoperability is valuable: world data should remain portable JSON/YAML/GeoJSON rather than trapped in one renderer.**

## Rejected approaches

- random procedural generation as world authority;
- image-first world design;
- renderer-owned geography;
- giant one-off map files with no underlying data model;
- premature graph database;
- precise GIS coordinates before continuity needs them;
- branching-player-choice mechanics for the Living Novel.

## Licensing disposition

Based on repository license files reviewed:
- Azgaar/Fantasy-Map-Generator — MIT
- Mindwerks/worldengine — MIT
- Turf.js — MIT
- inkle/ink — MIT
- MapLibre GL JS — BSD-style license with upstream notices

Current recommendation is to adopt **architectural patterns first**, not copy implementation code. If code is later imported, preserve required notices and perform a focused dependency/license review at that time.

## Gate 1 result

**PASS**

The study resolves the Phase 1 questions:
- authoritative data lives outside renderers;
- controlled mutations alter state;
- persistent state is shared;
- spatial QA can later use geometry tooling;
- narrative continuity should inherit state;
- rendering can remain replaceable.

Next authorized phase:

**PHASE 2 — SOURCE & LOCATION EXCAVATION**
