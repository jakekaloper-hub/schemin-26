# BULLPEN BOARD — SCHEMIN WORLD / DIVISION INDEX SUMMIT

**Date:** 2026-09-29  
**Status:** WORKING DECISION / PROPOSED ARCHITECTURE  
**Branch:** `world/division-index-foundation-2026-09-29`  
**Authority:** Jake/Commissioner intent + Project Control Registry + Founder Creative Directive + current World Design Principles + Memo OS V5.5

## Executive finding

The current project does not primarily have a "bad map" problem. It has a **layering problem**.

Schemin already contains:
- a coherent physical-world model;
- a political/commonwealth model;
- a character control system;
- a persistent-world requirement in Memo OS V5.5;
- recurring matchup locations;
- a Living Novel world-design doctrine.

What is missing is a canonical intermediate layer connecting those systems:

`PHYSICAL WORLD → DIVISION JURISDICTIONS → OWNER DOMAINS → RECURRING LOCATIONS → WEEKLY ENCOUNTERS`

Without that layer, the map tends to collapse into visually repetitive fantasy geography decorated by team/division labels.

## Board participants / domain views

### Librarian — Canon and provenance
Preserve the existing causal-world material. Do not retcon physical geography merely to make Burgers, Wings and Pizza look different. Any new division identity must be provenance-tagged and must not silently convert editorial imagery into literal geography.

### Cartography — Geography
The physical-world file already gives a usable causal skeleton: northern mountains, upper valleys, central river basin, western tablelands, eastern storm coast, southern wetlands/delta and inner-sea littoral. The division layer should be drawn **over** this geography rather than replacing it.

### Production Design — Material culture
Division differentiation should come from settlement form, construction materials, roads, civic spaces, trade, agriculture, ceremony, heraldry and recurring objects—not merely from banners and color swaps.

### Visual Development — Readability
A viewer should be able to identify a division from an unlabeled environmental frame. This requires silhouette-level distinctions in skyline, road type, terrain, vegetation, architecture, light and material palette.

### Narrative — Story utility
Divisions must create story pressure: travel difficulty, border crossings, rivalry, home-field familiarity, supply, weather exposure, ceremonial obligations and recurring places. They cannot be decorative map quadrants.

### Character Systems — Owner relationship
Owner domains exist **inside** the world and division framework. They are not twelve sovereign mascot kingdoms by default. The current owner character canon remains authoritative.

### Memo OS — Weekly production
V5.5 already requires WORLD_ATLAS + WORLD_STATE_LEDGER + resolved scene locations. The missing Division Index can become the bridge that makes those controls practical during weekly previsualization.

### Novel OS — Long-form continuity
The same geography must support quiet scenes, travel, institutions, ordinary people and deep history—not only matchup spectacle.

### Umpire / QA
Reject:
- literal food landscapes;
- three nearly identical kingdoms differentiated by color;
- owner-themed geography with no physical cause;
- unexplained teleportation;
- recurring landmarks moving between pages;
- weather that ignores adjacent geography;
- temporary matchup scenery promoted to canon without review.

### Closer — Resolution
Adopt a **layered atlas model** and a **Division Index peer to the Character Index**. Do not redesign the physical world. Add the missing league/division layer above it.

## Primary reconciliation

Existing World Design Principles contain an anti-mascot law: no region should exist merely because a team has a matching mascot/name.

Jake's new direction does not require breaking that law.

The resolution is:

**Burgers, Wings and Pizza are not literal food biomes or mascot kingdoms. They are persistent League divisions with territorial, historical, cultural and institutional expression inside a causally coherent world.**

Food identity becomes:
- heraldry;
- ceremonial tradition;
- guild/civic symbolism;
- hospitality/feast culture;
- market identity;
- idiom;
- ritual;
- historical League symbolism.

It does **not** require mountains shaped like burgers, pizza-stone cities, or giant chicken-wing terrain.

### Semantic lock
**WINGS = chicken wings.**  
Any crest, heraldic or food-symbol treatment must read as chicken wings/wing culture rather than generic bird wings unless intentionally specified otherwise.

## Current visual evidence and problem statement

The attached Week 3 memo demonstrates both the strength and the gap:
- early pages show several memorable local environments and story locations;
- the "Three Kingdoms" spread presents Burgers, Wings and Pizza as broad visual territories;
- the later "Six Roads Forward" spread successfully treats matchup locations as destinations connected by routes.

The problem is that the intermediate geography is underdefined, so large-scale maps can become repetitive while local scenes are much richer.

### Provenance caution
The attached Week 3 PDF contains 23 rendered pages, while the current Project Control Registry describes a 21-page Week 3 immutable release. This does not block architecture work, but **page-level imagery must not be promoted to LOCKED CANON until the Librarian reconciles the release artifact identity.**

## Assets to preserve

1. Existing seven-zone physical geography in `living-novel/world/PHYSICAL_WORLD.md`.
2. Causal construction order and anti-mascot law in `living-novel/world/WORLD_DESIGN_PRINCIPLES.md`.
3. Multipolar commonwealth / Compact political model.
4. Character canon and owner→character→team identity law.
5. Memo OS V5.5 WORLD_ATLAS + WORLD_STATE_LEDGER + complete-issue previs requirements.
6. Existing recurring locations and environmental motifs from published memo evidence.
7. Serious-world tone: the world does not wink at the reader.
8. Persistent consequence: damage, travel and history remain visible.

## Missing systems

The board identifies these gaps:

1. **Division Index** — no governing schema for Burgers/Wings/Pizza.
2. **Division-to-physical-world overlay** — no explicit way to map divisions onto the seven-zone physical model.
3. **Owner Domain Register** — character homes/strongholds/routes are not normalized against division geography.
4. **Location Canon Register** — recurring places need permanent/provisional/metaphor states.
5. **Travel & visibility model** — relative distance, routes, passes, waterways and horizon relationships need stable rules.
6. **World-state mutation contract** — weekly events need a deterministic way to alter locations without resetting them.
7. **Environment fingerprint** — each division/region needs enough visual structure to survive label removal.
8. **Cartographic layer model** — physical, political, League/division, owner and weekly-event layers are currently conflated.

## Architecture decision

Adopt five persistent atlas layers:

1. **PHYSICAL ATLAS** — terrain, water, climate, ecology, elevation.
2. **CIVIL/POLITICAL ATLAS** — cities, jurisdictions, trade, roads, institutions.
3. **LEAGUE/DIVISION ATLAS** — Burgers, Wings, Pizza as competition/cultural jurisdictions.
4. **OWNER DOMAIN ATLAS** — the Twelve's residences, operating territories and recurring routes.
5. **ENCOUNTER/STATE ATLAS** — weekly locations, active damage, temporary sites and current-world consequences.

A single rendered map may combine selected layers, but the data model must keep them distinct.

## Board output / next production order

1. Freeze this layered-atlas architecture as the working model.
2. Build Division Index schema.
3. Inventory all published/repository locations and classify them.
4. Reconcile Week 3 release artifact identity.
5. Map existing locations onto physical zones without inventing precise coordinates.
6. Draft Burgers/Wings/Pizza identities as PROPOSED LORE.
7. Test each division with unlabeled environment briefs.
8. Build owner-domain mapping.
9. Create Atlas V1 only after the above passes.
10. Integrate the resulting Division Index + Atlas resolver into Memo OS V5.5 page packets.

## Closer decision

**APPROVED FOR WORKING IMPLEMENTATION.**

This is not a final lore freeze. It is the production architecture within which the detailed worldbuilding should now be performed.

Core doctrine:

> Build the world first.  
> Let divisions inhabit it.  
> Let owners belong to it.  
> Let weekly events alter it.  
> Then let the camera enter it.
