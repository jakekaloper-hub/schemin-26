# MEMO STORY INTELLIGENCE -> NOVEL SEASON STATE CONTRACT V1
**Status:** ENFORCED HANDOFF CONTRACT
**Direction:** Memo OS reports operational evidence; Novel OS decides narrative persistence.

## Required input fields
- evidence_id
- owner_id / canonical team identity
- observed team alias
- event_type
- fact
- source / provenance
- evidence_confidence
- became_true_at
- knowable_at
- verification_status
- uncertainty
- memo_week

## Novel ingestion output
- owner-season-state fact_id
- causal_classification
- prior_state reference
- consequence
- new_state
- narrative_significance
- prose_visibility
- resolution_status
- eligible_book_time
- retroactive_use_prohibited
- persistent_object links
- story_promise links

## Hard gates
1. UNVERIFIED evidence cannot mutate canonical Novel state.
2. knowable_at later than target Book Time => TEMPORAL_VIOLATION.
3. Memo interpretation is never silently promoted to fact.
4. Owner/team alias changes cannot mutate canonical character identity.
5. Mercer/private GM material is rejected from public Novel ingestion.
6. NO_MATERIAL_CHANGE is valid and preserves prior active state.
7. W3 unresolved outcomes remain branches until Fact Lock.

## Ownership
Memo OS owns WHAT HAPPENED operationally.
Novel OS owns WHAT PERSISTS narratively.
Neither overwrites the other's source record.
