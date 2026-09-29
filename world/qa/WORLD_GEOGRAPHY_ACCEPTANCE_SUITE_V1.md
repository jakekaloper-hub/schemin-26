# WORLD GEOGRAPHY & DIVISION ACCEPTANCE SUITE V1

**Status:** PROPOSED QA CONTRACT  
**Scope:** World Atlas, Division Index, owner domains and weekly matchup locations.

## Blocking tests

### GEO-01 — Physical causality
PASS when terrain, water, climate and settlement relationships follow the existing physical-world logic.
FAIL when a division theme overrides causality.

### GEO-02 — Layer separation
PASS when physical, civil, division, owner and Encounter layers can be independently identified.
FAIL when a team/division label is treated as the physical-world definition.

### GEO-03 — Division distinctness
PASS when Burgers/Wings/Pizza are distinguishable without text labels in representative environment briefs.
FAIL when differentiation is predominantly banner color or food props.

### GEO-04 — Food semantic accuracy
PASS when:
- Burgers = burgers;
- Wings = chicken wings;
- Pizza = pizza.
FAIL on silent substitution of Wings into generic avian/angelic imagery.

### GEO-05 — Anti-literal-food
PASS when food identity is cultural/heraldic.
FAIL when terrain/architecture becomes novelty food sculpture without explicit approved story reason.

### GEO-06 — Owner inheritance
PASS when each owner domain respects the division and physical atlas while preserving character canon.
FAIL when owner/team mascot reverse-engineers geography.

### GEO-07 — Recurring-location stability
PASS when a recurring place maintains zone, adjacency, landmarks, materials and route relationships.
FAIL when it teleports or changes biome without an event.

### GEO-08 — World-state persistence
PASS when damage/weather/occupation/repair persists until changed.
FAIL on unexplained reset.

### GEO-09 — Travel plausibility
PASS when scene transitions have a plausible route/transport class.
FAIL on plot-speed relocation across blocked terrain.

### GEO-10 — Horizon continuity
PASS when established visible landmarks and cardinal relationships are stable.
FAIL when major geography moves for composition convenience.

### GEO-11 — Weather propagation
PASS when significant weather has coherent regional effects.
FAIL when adjacent scenes ignore a major weather event without explanation.

### GEO-12 — Location canon status
PASS when every new visual location is PERMANENT_CANON, PROVISIONAL_CANON, TEMPORARY_SITE, VISUAL_METAPHOR or SUPERSEDED.
FAIL when generated scenery silently enters canon.

### GEO-13 — Stranger test
PASS when an outside reader can infer how people move, live and build in the place without fantasy-football knowledge.
FAIL when scenery only makes sense as a team-name joke.

### GEO-14 — Repetition test
PASS when divisions and recurring regions have differentiated composition/material/environment grammars.
FAIL when three territories are the same medieval landscape with palette swaps.

### GEO-15 — Previs completeness
PASS when every major page packet resolves world location, entering state, owner/domain relationship, route, camera direction, F/M/B and post-scene state.
FAIL when image generation is asked to invent these independently.

## Promotion gate

A World Map or Division Map may be labeled `CANONICAL V1` only after:
- GEO-01 through GEO-15 pass;
- release-artifact provenance is reconciled;
- Division Indexes are complete enough for unlabeled-environment tests;
- owner domains are mapped;
- recurring Week 1–3 locations are classified;
- Umpire signs off independently from the producing role.
