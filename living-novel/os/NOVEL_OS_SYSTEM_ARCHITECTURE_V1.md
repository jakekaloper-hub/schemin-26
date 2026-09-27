# NOVEL OS SYSTEM ARCHITECTURE V1
**Status:** PHASE-1 BASELINE
## Purpose
Novel OS is the in-place operating layer for the Pro Schemin' Legendarium. It coordinates existing Schemin evidence, canon, manuscript, world, character and visual-production assets without duplicating their authority.
## Architecture
### 1. Evidence plane
Upstream/shared: verified league data, historical records, Weekly Memo evidence, screenshots, commissioner evidence, approved references. Evidence is immutable/provenance-preserved.
### 2. Authority plane
Resolves SOURCE_EVIDENCE, LEAGUE_FACT, CHARACTER_CANON, WORLD_CANON, VISUAL_CANON, MANUSCRIPT_CANON, PROPOSED_CANON, ORACLE and EXPERIMENT. Authority is explicit and versioned.
### 3. State plane
Tracks current character/world/narrative/object/location/knowledge/promise/manuscript state.
### 4. Retrieval plane
Builds bounded task-specific Context Packs with source IDs, authority, temporal scope and freshness.
### 5. Orchestration plane
Routes commands to the minimum required Bullpen roles and tools. Creator and final gatekeeper remain separate.
### 6. Production plane
Literary pipeline and visual pipeline operate against the same authority/state services.
### 7. Validation plane
Deterministic validators run before semantic Guardian review. Failed gates cannot self-certify.
### 8. Persistence plane
Accepted mutations update registries/state/changelogs; rejected experiments remain non-canon.
## Core transaction
INTENT → ROUTE → RETRIEVE → EXECUTE → VALIDATE → CLOSER → HUMAN/CANON GATE → PERSIST.
## Live-season transaction
EVENT → VERIFY → SIGNIFICANCE → CONSEQUENCE → WORLD TRANSLATION → STORY DESIGN → PRODUCTION → QA → CANON PROPOSAL → APPROVAL → STATE.
## Visual transaction
MANUSCRIPT ANCHOR → BEAT → VISUAL VALUE → CANON/REFERENCE RESOLUTION → BRIEF → COMPOSITION → GENERATION → CHARACTER QA → VISUAL QA → APPROVAL.
## Hard boundaries
- Generated content has zero canon authority by default.
- Team names never control owner visual identity.
- Oracle Time never mutates Book Time without verified event ingestion.
- Stale/missing evidence is exposed, never guessed.
- Existing approved Prologue artifacts are wrapped by manifests before any migration.
