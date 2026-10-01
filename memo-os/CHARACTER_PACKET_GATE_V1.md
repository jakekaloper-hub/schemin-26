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
