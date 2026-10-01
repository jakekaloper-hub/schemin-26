# WORLD MUTATION PROTOCOL V1

**Status:** PHASE 9 CANDIDATE

A world change must be proposed, sourced, classified, impact-analyzed, tested, approved, applied, propagated and receipted.

## Required fields
REQUEST_ID
SOURCE
CURRENT_STATE
PROPOSED_STATE
RATIONALE
CANON_CLASS
CANON_CONFIDENCE
AFFECTED_ENTITIES
AFFECTED_LOCATIONS
AFFECTED_ROUTES
AFFECTED_ATLAS_LAYERS
AFFECTED_SYSTEMS
MIGRATION_ID
TESTS
ROLLBACK
APPROVAL
RESULT

## Spatial propagation
ROAD CLOSED → Roads/Travel + Encounter + World-State.
FLOOD → Weather + World-State + Roads/Travel + affected Civil layer.
BUILD BRIDGE → Civil + Roads/Travel + Visibility.
DESTROY BUILDING → Civil + World-State + Memory.
RENAME LOCATION → every consumer-facing Atlas view and all references.

No renderer or prose artifact can perform a mutation by itself.
