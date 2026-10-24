# Week 4 Page Packet Register

**Status:** SCHEMA FROZEN / RESULT FIELDS OPEN  
**Authority:** Groundskeeper

Every final page must contain:

**Story authority binding (required before any other production check):**
- `story_authority_id`
- `story_authority_hash`
- `story_authority_receipt`
- `story_authority_state = CURRENT`

If the controlling story treatment changes, any dependent packet becomes **`PAGE_PACKET_STALE / REBUILD_REQUIRED`** even when its schema, character references, world fields and composition are otherwise valid.

No packet may be compiled from a superseded branch or a fixed page plan that predates current story authority.


- page number;
- page purpose;
- story beat;
- factual source fields;
- character IDs;
- canonical reference assets;
- current character state;
- venue;
- geography;
- entering world state;
- composition;
- foreground/midground/background;
- text hierarchy;
- headline;
- supporting copy;
- score/stat slots;
- visual objects;
- negative constraints;
- known drift risks;
- rejection criteria;
- mobile readability target;
- previous-page relationship;
- next-page relationship.

## Mandatory character rejection criteria

### D0nkey K0ng
PASS only if one integrated **centaur-bodied Arsenal Gorilla Warrior**:
- gorilla-warrior upper identity;
- four-legged centaur/equine lower body.

FAIL:
- bipedal gorilla;
- human-torso centaur;
- legacy Arsenal Centaur;
- generic beast.

### ObiWan
- Trade Jedi;
- no championship belt.

### TDS
- one body;
- exactly three serpent heads.

### HMB
- Belt Keeper identity preserved;
- belt ownership independent of weekly outcome.

## Deterministic-data rule

Scores, records, rankings, betting arithmetic, standings and other critical text must be composed deterministically, not trusted to image-model raster text.


## Story-authority precedence

Production resolves story authority in this order:
1. latest explicit Commissioner instruction;
2. latest matchup-specific amendment;
3. latest Story Room / Author Council approved treatment;
4. latest World / Atlas decision;
5. current Week 4 consequence register;
6. current page manifest;
7. older planning;
8. historical publication.

**Newer + more specific beats older + more general.** Conflicts require a recorded reconciliation decision; they may not be silently blended.
