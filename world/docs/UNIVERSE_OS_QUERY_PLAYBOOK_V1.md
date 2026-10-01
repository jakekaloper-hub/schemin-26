# UNIVERSE OS QUERY PLAYBOOK V1

Canonical production queries:

- `WHERE_IS(entity)`
- `WHO_LIVES(location)`
- `WHAT_KIND(entity)`
- `HOW_TO_TRAVEL(A,B)`
- `WHAT_ROUTES_TOUCH(location)`
- `WHAT_IS_UPSTREAM(location)`
- `WHAT_IS_DOWNSTREAM(location)`
- `WHAT_CAN_BE_SEEN_FROM(location)`
- `WHAT_REGION_CONTAINS(location)`
- `WHAT_ATLAS_LAYERS_CONTAIN(location)`
- `WHAT_HAPPENED(location)`
- `WHAT_STATE(location)`
- `WHAT_MEMORY(location)`
- `WHAT_INSTITUTIONS_NEAR(location)`
- `WHAT_ECONOMY(location)`
- `WHAT_DIVISION_CULTURE(location)`
- `WHAT_CAN_APPEAR_IN_SCENE(location)`
- `WHAT_IS_FORBIDDEN(location)`
- `WHAT_CHANGED_AFTER(event)`
- `WHAT_REFERENCE_CONTROLS(character)`

## Example — ObiWan
Expected truth:
- principal: CHAR-JAKE-KALOPER;
- home: LOC-TRADE-JEDI-MOUNTAIN-BASE;
- region: REG-UPPER-VALLEYS;
- division: DIV-BURGERS;
- inhabitants: other Jedi + non-Jedi humans;
- route: Eastern Ascent → Bridge → basin network;
- forbidden: championship belt; cloning ObiWan's exact identity across other Jedi.

## Example — Country Club of Jackson
Expected truth:
- physical zone: Southern Wetlands;
- Duckhook is singular;
- surrounding population may be mixed ordinary inhabitants;
- Jackson Levee / causeway logic governs access;
- Week 3 chili incident remains historical memory / unresolved cleanup state.

## Cross-consumer rule
Universe OS, Atlas, Memo OS, Novel OS and Art Pipeline must resolve the same IDs and compatible state. A consumer-specific presentation may omit details; it may not fork them.
