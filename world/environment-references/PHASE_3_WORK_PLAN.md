# ATLAS PHASE 3 — ENVIRONMENT REFERENCE & RENDERER GROUNDING

**Status:** ACTIVE PRODUCTION GATE

## Mission
Convert Phase 2's semantic location addressability into renderer-consumable environment grounding without allowing a generated first draft to define canon.

## Two-tier reference model

### Tier A — APPROVED_STRUCTURAL_REFERENCE
Deterministic, repo-addressable plate derived only from active Location Card / World Engine facts.

May lock:
- location ID/name;
- physical zone;
- persistent landmarks;
- route/access context;
- current-state warnings;
- horizon/visibility constraints;
- forbidden substitutions.

May support:
- previs;
- composition planning;
- environment layout continuity;
- renderer grounding when semantic/structural reference is sufficient.

### Tier B — APPROVED_CINEMATIC_REFERENCE
Human-approved illustrative environment plate with durable bytes and explicit provenance.

May support:
- exact environment-image grounding;
- recurring cinematic visual identity.

Phase 3 does not fabricate Tier B approval.

## Promotion rule
A generated image cannot promote itself.
Cinematic promotion requires:
1. active LOC identity;
2. structural packet;
3. candidate image bytes;
4. Visual Director review;
5. Umpire continuity review;
6. Commissioner approval;
7. registry update.

## Deliverables
- 23 deterministic structural SVG plates;
- structural plate generator;
- tiered environment reference registry;
- reference resolver behavior;
- renderer contract tests;
- Memo/Novel/Visual integration rules;
- CI gate;
- acceptance report and release receipt.

## Hard invariants
- 23 active LOC identities preserved;
- 48 CAND sites untouched;
- no active geography mutation;
- no cinematic reference falsely approved;
- structural plates regenerated deterministically from active cards;
- exact cinematic grounding still blocks when Tier B is required.
