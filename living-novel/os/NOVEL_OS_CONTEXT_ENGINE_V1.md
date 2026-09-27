# NOVEL OS CONTEXT ENGINE V1
**Status:** PHASE-1 BASELINE
## Goal
Supply the smallest sufficient authoritative context for a task. Never dump the full manuscript/world by default.
## Context Pack envelope
pack_id; task; temporal_scope; authority_cutoff; required_entities; source_records; canon_assertions; current_state; manuscript_anchors; conflicts; unknowns; freshness; token_budget; retrieval_log.
## Pack types
CHARACTER_CONTEXT_PACK — identity, state, relationships, knowledge, visual locks.
SCENE_CONTEXT_PACK — manuscript anchors, participants, location, time, promises, required facts.
CHAPTER_CONTEXT_PACK — arc state, prior/next dependencies, style constraints.
LOCATION_CONTEXT_PACK — geography, travel, materiality, history, inhabitants.
CONTINUITY_CONTEXT_PACK — assertions and state necessary to test a candidate.
VISUAL_CONTEXT_PACK — manuscript beat + character packets + environment/object refs + art grammar.
HISTORICAL_CONTEXT_PACK — verified historical evidence + confidence/contestation.
STYLE_CONTEXT_PACK — current literary doctrine and approved prose anchors.
WEEKLY_EVENT_CONTEXT_PACK — verified league event, freshness, historical context, affected entities.
## Retrieval rule
Authority and temporal relevance outrank semantic similarity. Conflicts and unknowns must be included, not hidden.
## Output rule
Every pack exposes provenance sufficient for the downstream agent and validator to explain why material was included.
