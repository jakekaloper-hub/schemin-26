# ENVIRONMENT REFERENCE PACKET STANDARD V1

**Status:** PHASE 2 PRODUCTION CONTROL

## Purpose

Define what counts as a usable environment reference and prevent text descriptions or generated drafts from masquerading as approved renderer-addressable canonical imagery.

## Reference states

### MISSING_APPROVED_VISUAL_REFERENCE
Semantic world truth exists; no approved renderer-addressable image bytes are registered.

### CANDIDATE_REFERENCE_ONLY
A draft/historical environment packet or image may inform review but cannot be mounted as canonical visual authority.

### APPROVED_VISUAL_REFERENCE
Requires:
- stable location ID;
- durable asset URI/path resolvable by production runtime;
- explicit approval/provenance;
- no contradiction with current Location Card;
- reference register entry.

### SUPERSEDED_REFERENCE
Historical only; cannot control new render.

## Required register fields

- location_id
- semantic_reference_status
- visual_reference_status
- approved_reference_uris
- candidate_reference_paths
- blockers
- approval_provenance
- supersedes

## Generation rule

If a workflow requires exact environment-image grounding and visual_reference_status != APPROVED_VISUAL_REFERENCE:

**HUMAN_REVIEW_REQUIRED**

Do not:
- generate a new image and immediately call it canonical;
- use a draft Chronicles packet as approved bytes;
- infer an environment image from a character plate;
- use a Week illustration as a permanent location plate without post-production promotion.

## Semantic-only generation

Text/world packets may still support:
- story planning;
- prose drafting;
- art-direction development;
- layout/previs;
provided the output is not claimed to be visually reference-locked.

## Promotion

A future approved reference must be registered without changing the underlying LOC identity.

**Reference doctrine:** a description is not a mounted reference.
