# CANONICAL WORLD ID CONTRACT V1

## Stable namespaces
- `LOC-*` active locations
- `ROUTE-*` active routes
- `REG-*` physical regions
- `DIV-*` League division overlays
- `CHAR-*` principal character identities
- `INST-*` institution entities where used
- `EVT-*` / existing event namespace for world-state events
- `CAND-*` editorial location candidates
- `SUB::LOC-*::*` derived sublocation handles

## Rules
1. Consumers reference canonical IDs; display names are presentation.
2. Rename does not create a new identity by itself.
3. Renderer labels never become IDs.
4. Memo and Novel may not create shadow IDs for an existing canonical object.
5. CAND-* cannot appear in an active resolver as LOC-* without governed promotion.
6. Derived handles must retain parent canonical ID.
7. Legacy aliases resolve to canonical IDs and never become competing authorities.
8. Historical names remain aliases/provenance after rename.

## Failure behavior
Unknown active ID → FAIL CLOSED / HUMAN REVIEW.
