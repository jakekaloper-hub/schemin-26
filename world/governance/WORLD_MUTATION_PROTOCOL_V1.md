# WORLD MUTATION PROTOCOL V1

A durable world change follows:

PROPOSE → PROVENANCE → CLASSIFY → IMPACT → TEST → APPROVE → MUTATE → PROPAGATE → RECEIPT

## Required record
- request_id
- source
- requester
- current_state
- proposed_state
- reason
- canon_class / confidence
- affected entities
- affected locations
- affected routes
- affected Atlas layers
- affected consumers
- migration action
- tests
- rollback
- approval
- result

## Spatial propagation examples
- ROAD CLOSED → Roads/Travel + Encounter + World-State.
- FLOOD → Weather + World-State + Travel; Physical base geography remains unless erosion/terrain change is explicitly approved.
- BUILD BRIDGE → Civil/Institutional + Roads/Travel + Visibility.
- DESTROY BUILDING → Civil + World-State + Historical Memory.
- RENAME LOCATION → all consumer-facing Atlas views while preserving stable ID unless identity itself changes.
- CLEANUP → World-State; historical memory remains.

## Historical backfill
Representative migrations:
- ObiWan coexists with other Jedi.
- Wilson centaur → Arsenal Gorilla Warrior.
- TDS principal body → one body / three serpent heads.
- TDS + Chili cross-divisional coexistence.
- El Niño manifestation law.

No generated image or chat-only inference bypasses this protocol.
