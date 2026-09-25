# Provenance & Approval State Machine

## Content states
DRAFT → FACT_CHECKED → CANON_CHECKED → EDITORIAL_APPROVED → MEDIA_CANDIDATE → MEDIA_APPROVED → RELEASE_CANDIDATE → PUBLISHED

## Hard invariants
- PUBLISHED original editions are immutable.
- A media candidate cannot become MEDIA_APPROVED without source asset IDs, story beat ID and reviewer.
- FACT claims require factual_basis.
- FICTIONALIZED_PRESENTATION cannot be promoted into FACT.
- Character reference changes require Jake.
- Public PUBLISHED transition requires Jake.

## Media candidate record
```
candidate_id
story_beat_id
source_assets[]
provider_adapter
model_version
prompt_version
created_at
rights_notes
identity_check
artifact_check
editorial_check
accessibility_assets
approval_status
reviewer
```

## Rejection reasons
IDENTITY_DRIFT | FACT_ERROR | TEXT_HALLUCINATION | ARTIFACT | CANON_VIOLATION | RIGHTS_UNKNOWN | ACCESSIBILITY_MISSING | PERFORMANCE_BUDGET | EDITORIAL_MISS

## Audit
Never delete rejected candidate metadata from the production ledger; mark rejected and retain enough provenance to avoid repeating failed generation patterns.
