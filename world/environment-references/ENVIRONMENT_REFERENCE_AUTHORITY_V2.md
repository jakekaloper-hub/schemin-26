# ENVIRONMENT REFERENCE AUTHORITY V2

## Reference states

SEMANTIC:
- RESOLVED_FROM_WORLD_ENGINE

STRUCTURAL:
- MISSING_STRUCTURAL_REFERENCE
- APPROVED_STRUCTURAL_REFERENCE
- SUPERSEDED_STRUCTURAL_REFERENCE

CINEMATIC:
- MISSING_APPROVED_CINEMATIC_REFERENCE
- CANDIDATE_CINEMATIC_REFERENCE
- APPROVED_CINEMATIC_REFERENCE
- SUPERSEDED_CINEMATIC_REFERENCE

## Structural plate contract

A structural plate is an authoritative **diagrammatic identity plate**, not cinematic artwork.

It is generated from current Location Card fields and may be committed because its content is deterministic and reviewable.

It must include:
- location ID and current name;
- zone;
- primary landmark list;
- route/access list;
- current-state warning summary;
- no invented architecture beyond active location/zone data;
- no principal character body depiction.

## Cinematic plate contract

A cinematic plate may add:
- perspective;
- architectural specificity;
- atmospheric depth;
- recurring visual material treatment;
- approved sub-location composition.

It may not add new canon silently.

## Render request requirements

SEMANTIC requirement:
semantic packet sufficient.

STRUCTURAL requirement:
approved structural plate URI required.

CINEMATIC requirement:
approved cinematic reference URI required.

## Failure behavior

Missing requested tier:
HUMAN_REVIEW_REQUIRED.

## Historical images

Released memo images may be candidate evidence.
They do not automatically become the canonical environment plate because:
- they may contain character drift;
- composition may be one-off;
- generated incidental scenery may be noncanonical;
- historical release truth is not identical to reusable renderer reference truth.
