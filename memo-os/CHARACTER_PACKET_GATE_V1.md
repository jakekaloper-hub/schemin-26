# Weekly Memo OS — Character Packet Gate V1

**Status:** V5.6 RC dependency  
**Authority:** existing character canon + temporal-canon controls

## Gate input
For every continuity-critical visual containing a league owner/character:

OWNER → CANONICAL CHARACTER → CURRENT DISPLAY TEAM → TEMPORAL CANON → APPROVED VISUAL REFERENCES.

## Pre-render receipt

```yaml
owner_id:
owner_name:
current_team_name:
character_id:
character_name:
canon_version:
effective_date:
reference_assets:
continuity_overlay:
required_identity_anchors:
prohibited_mutations:
special_invariants:
status: PASS | BLOCKED
```

## Final-raster QA
PASS requires:
- owner match;
- correct species/body architecture;
- recognizable silhouette;
- correct face/head construction;
- correct body mass;
- active wardrobe/material language;
- required props/companions;
- continuity state;
- retired design absent;
- cross-character contamination absent;
- prohibited mutation absent;
- thumbnail recognizability.

## Failure behavior
Any hard mismatch = PAGE_REJECT / regenerate or repair.

Prompt correctness cannot override a wrong final raster.

## Rename rule
A team rename changes display metadata, not character identity, unless explicit Commissioner canon changes the character.


## October 18, 2026 lineup approval — mandatory presentation reference

For any owner-character page, resolve the owner to immutable CHAR-* ID and attach the current Commissioner-approved comparative appearance baseline:
canon/characters/APPROVED_LINEUP_2026_10_18.json and the matching derived subject record under canon/characters/lineup_2026_10_18/.

This exact lineup is approved for all twelve character appearances including the hooded red-eyed black-armored His Majesty's Blood correction. It does not authorize substitution of a September primary JPEG with a supplementary PNG, actual image provider binding, or publication without existing gates.

- The visual compositor compares each character against the exact owner crop hash and negative rules, not generic prose.
- Physical morphology preserves required limb/head counts and companions; numerical dimensions remain unmeasured.
- Venue, terrain and travel remain governed by world/location-control-plane and existing location IDs, not artwork backdrops.
- Historical poster captions are not fantasy league results, scores or roster facts.
- DK historical bipedal source remains hard-blocked by active VISUAL_REFERENCE_AUTHORITY_V1.json conflict. A new four-legged depiction is not automatically a versioned replacement primary.
- Umpire final-raster checks (C1/T15/T16), source attachment, and per-subject identity binding remain independent prerequisites.

**Status:** appearance approved; generation/publication gates HOLD until actual provider evidence and independent visual QA.

## October 18 operational visual-context bridge
The existing compile_memo_location_packet adapter now actually resolves current Commissioner lineup visual rules, physical anatomy and verified homeland anchors, and build_visual_world_packet adds actual owner-specific physical/negative locks. READY_FOR_SEMANTIC_QA never grants character image-generation eligibility. Nameplate-trimmed panels remain ISOLATION_QA_HOLD and never substitute for an approved primary source. Actual Memo production/release still requires native binding and independent C1/T15/T16 generated-output evidence. See canon/characters/lineup_2026_10_18/OPERATIONAL_CONVERGENCE_REVIEW_2026_10_18.md.
