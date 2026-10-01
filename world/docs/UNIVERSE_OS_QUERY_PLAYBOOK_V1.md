# UNIVERSE OS QUERY PLAYBOOK V1

Standard queries:
- WHERE_IS(entity)?
- WHO_LIVES(location)?
- WHAT_KIND(entity)?
- HOW_TO_TRAVEL(A,B)?
- WHAT_ROUTES_TOUCH(location)?
- WHAT_IS_UPSTREAM(location)?
- WHAT_IS_DOWNSTREAM(location)?
- WHAT_CAN_BE_SEEN_FROM(location)?
- WHAT_REGION_CONTAINS(location)?
- WHAT_ATLAS_LAYERS_CONTAIN(location)?
- WHAT_HAPPENED(location)?
- WHAT_STATE(location)?
- WHAT_MEMORY(location)?
- WHAT_INSTITUTIONS_NEAR(location)?
- WHAT_ECONOMY(location)?
- WHAT_DIVISION_CULTURE(location)?
- WHAT_CAN_APPEAR_IN_SCENE(location)?
- WHAT_IS_FORBIDDEN(location)?
- WHAT_CHANGED_AFTER(event)?
- WHAT_REFERENCE_CONTROLS(character)?
- WHAT_NEUTRAL_SITE_CAN_BOTH_TEAMS_REACH(A,B)?

Each result should expose canonical IDs, answer, authority/source, confidence, current state, unresolved fields and consumer warnings.

Examples:
- ObiWan resolves to Trade Jedi Mountain Base in the Upper Valleys, with other Jedi and non-Jedi humans around him.
- Country Club of Jackson resolves to a mixed ordinary estate population; Dr. Duckhook is singular.
- TDS–Chili Shared March permits both Burgers and Wings presence.

Memo, Novel, Atlas and Art must resolve compatible IDs and state.
