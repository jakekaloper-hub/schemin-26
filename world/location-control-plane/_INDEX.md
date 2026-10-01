# LOCATION CONTROL PLANE / ATLAS PHASE 2 — INDEX

**Status:** RELEASE CANDIDATE / PRODUCTION QA PENDING
**Scope:** Homeland, Settlement & Location Card Production

## Read order

1. PHASE_2_WORK_PLAN.md
2. AUTHORITY_AND_CONSUMER_MATRIX_V1.md
3. LOCATION_CONTROL_PLANE_ARCHITECTURE_V1.md
4. SETTLEMENT_AND_INSTITUTION_HIERARCHY_V1.md
5. ATLAS_VISUAL_HIERARCHY_SPECIFICATION_V1.md
6. ENVIRONMENT_REFERENCE_PACKET_STANDARD_V1.md
7. schemas/homeland-card.schema.json
8. schemas/location-card.schema.json
9. schemas/world-packet.schema.json
10. registries/HOMELAND_CARD_REGISTRY.json
11. registries/LOCATION_CARD_REGISTRY.json
12. registries/PARENT_SUBLOCATION_REGISTRY.json
13. registries/LOCATION_REFERENCE_REGISTRY.json
14. compiler/location_control_plane.py
15. adapters/memo_adapter.py
16. adapters/novel_adapter.py
17. qa/PHASE_2_SCENARIO_MATRIX_V1.md
18. qa/test_location_control_plane.py

## Production assets

- 12 Homeland Cards under homelands/{CHAR-ID}/CARD.json
- 23 Location Cards under locations/{LOC-ID}/CARD.json

## Authority boundary

This control plane is derived infrastructure.

It does not supersede:
- World Engine V1.1;
- Character Canon;
- League Data Gateway;
- Memo OS;
- Novel OS.

It makes their location-relevant truth addressable.

## Current visual-reference posture

Semantic location grounding: available for all 23 active locations.

Approved renderer-addressable environment reference bytes: not yet registered for any active location under this Phase 2 control plane.

Therefore exact visual-reference-required generation must block with HUMAN_REVIEW_REQUIRED until approved environment references are registered.

## Candidate firewall

The 48 Phase 1 CAND-* records remain editorial only.

Active resolver accepts LOC-* only.

## Promotion

This index becomes ACTIVE only after:
- structural audit;
- Location Control Plane test suite pass;
- World Engine CI pass;
- Umpire acceptance;
- Closer release approval;
- merge to main.
