# NOVEL OS DATA MODEL V1
**Status:** PHASE-1 BASELINE
## Common envelope
Every structured record SHOULD expose:
`id, type, status, authority, source_ids, provenance, temporal_scope, effective_from, effective_to, supersedes, confidence, created_at, updated_at, approval`.
## Principal entities
### SourceRecord
Immutable evidence pointer; source kind; locator; checksum/version; observed_at; freshness; extraction notes.
### CanonAssertion
subject; predicate; value; authority_class; source_ids; confidence; temporal scope; supersession; approval.
### CharacterState
owner_id; canonical_character_id; current_team_id; physical/visual locks; motives; knowledge; relationships; possessions; location; emotional state; arc state.
### WorldEntity
entity_type; names/aliases; geography; material properties; institutional relationships; world rules; temporal validity.
### NarrativeState
manuscript_id; scene_id; beat_id; POV; revelations; motifs; foreshadowing; mysteries; callbacks; consequences; open threads.
### PromiseRecord
origin; type; characters; promise; importance; status; expected_horizon; payoff; source_ids.
### ManuscriptVersion
id; parent_id; path; semantic status; authoring role; reason; changes; canon implications; approval.
### VisualAssetRecord
asset/ref ID; owners; canonical references; manuscript/beat anchors; brief; composition; generation adapter; QA results; approval; visual-canon status.
### WorkflowRun
command; inputs; routed roles; tools; state; outputs; gates; failures; retries; timestamps.
### DecisionRecord
ADR ID; issue; options; disagreements; Closer resolution; evidence; supersession.
## Authority classes
SOURCE_EVIDENCE; VERIFIED_LEAGUE_FACT; HISTORICAL_RECORD; CHARACTER_CANON; WORLD_CANON; VISUAL_CANON; MANUSCRIPT_CANON; INTERPRETATION; PROPOSED_CANON; ORACLE; EXPERIMENT.
## Mutation rule
Only an approved mutation transaction may change authoritative state. Mutation must record previous value, proposed value, evidence, validator results, approver and effective time.
