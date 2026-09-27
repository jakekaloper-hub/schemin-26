# NOVEL OS — PHASE 0 ARCHAEOLOGY & STATE RECONCILIATION

**Status:** ACTIVE / AUTHORITATIVE PHASE-0 RECORD  
**Repository:** `jakekaloper-hub/schemin-26`  
**Canonical long-lived root:** `living-novel/`  
**Current Prologue production workspace:** `chronicles/proof-of-concept/prologue/`  
**Directive:** BULLPEN — NOVEL OS ENGINE ROOM MASTER BUILD, INTEGRATION & PRODUCTION DIRECTIVE  
**Date:** 2026-09-27

## Executive finding

The Novel project is not starting from zero. It already contains a substantial Living Novel architecture and a mature Prologue production system. The principal Phase-0 defect is **state fragmentation and status drift**, not absence of creative infrastructure.

Accordingly, Novel OS must be evolved in place. Do not create a parallel replacement tree that duplicates approved work.

## Root ruling — ADR candidate

1. `living-novel/` remains the canonical long-lived Novel OS / Legendarium root.
2. `chronicles/proof-of-concept/prologue/` remains the active Prologue production workspace while the current production chain is live.
3. Do not mass-migrate Prologue files during OS construction.
4. Novel OS should reference production artifacts through registries/manifests first. Migration is allowed only after lossless mapping, provenance preservation, and regression tests.
5. Existing top-level `canon/`, `data-gateway/`, `schemas/`, `tests/`, and project governance remain upstream/shared Schemin services rather than being copied into Novel OS.

## Existing authoritative foundations

### Living Novel control plane
- `living-novel/MASTER_DIRECTIVE.md` — governing mission, evidence hierarchy, secondary-world doctrine, live-season doctrine.
- `living-novel/NOVEL_OS.md` — early v0.1 architecture. **STATUS STALE:** its PRE-PRODUCTION / Phase A language no longer represents repository reality.
- `living-novel/research/PHASE_A_ARCHAEOLOGY.md` — historical archaeology foundation.
- `living-novel/world/*` — world-system material already exists.
- `living-novel/characters/*` — individual character records already exist.
- `living-novel/qa/*` — editorial/publication gates already exist.

### Cross-project canon/governance
- `canon/SCHEMIN_26_MASTER_CHARACTER_CANON.md` — binding 12-owner character identity and visual continuity authority.
- `docs/governance/AUTHORITY_MATRIX.md` — project authority boundaries.
- `docs/architecture/REPOSITORY_ARCHITECTURE.md` — Schemin repo domain doctrine.
- `skills/schemin-bullpen-execution/SKILL.md` — evidence-backed execution contract.

### Current Prologue literary master
- `chronicles/proof-of-concept/prologue/PROLOGUE_MANUSCRIPT_V4_CONSULTANT_REVISION.md`
  - consultant-revised literary master candidate;
  - temporal lock: after 2026 draft, before Week 1 results;
  - hold for final gate;
  - manuscript-first production rule.

### Current Prologue visual-production chain
The following required artifacts already exist and must be reconciled rather than rebuilt:
- `PROLOGUE_BEAT_AND_VISUAL_MAP_V1.md`
- `PROLOGUE_ART_DIRECTION_BIBLE_V1.md`
- `PROLOGUE_ART_BRIEF_REGISTER_V1.md`
- `PROLOGUE_REFERENCE_PACKET_ARCHITECTURE_V1.md`
- `PROLOGUE_CHARACTER_REFERENCE_RESOLUTION_MATRIX_V1.md`
- `PROLOGUE_CONSECUTIVE_COMPOSITION_PROTOTYPE_V1.md`
- spread-level `production/spread_*/MANUSCRIPT_LOCK.md` records.

## Classification

### CANONICAL / BINDING
- Master Character Canon and explicit Jake-approved corrections.
- Verified league evidence and authoritative project data.
- Founder/Master Directives where not superseded by a later explicit Jake directive.
- Approved visual locks and official references.

### CURRENT PRODUCTION AUTHORITY
- V4 Consultant Revision as current Prologue literary master candidate pending final gate.
- Prologue Beat & Visual Map V1.
- Art Direction Bible V1.
- Art Brief Register V1.
- Reference Packet Architecture V1.
- Character Reference Resolution Matrix V1.
- Existing spread manuscript locks where traceable to V4.

### STALE BUT HISTORICALLY USEFUL
- `living-novel/NOVEL_OS.md` status declaration claiming PRE-PRODUCTION / Phase A only.
- Earlier manuscript versions where V4 explicitly descends from/supersedes them.
- Earlier production approaches rejected by later reset/corrective directives.

### MUST NOT BE SILENTLY PROMOTED
- hypotheses in archaeology/world documents explicitly marked non-canon;
- generated prose not accepted through a canon gate;
- generated images not explicitly accepted into visual canon;
- future-season outcomes;
- unsupported historical reconstruction.

## Phase-0 conflict register

### C-001 — OS status drift
**Conflict:** Living Novel OS says pre-production while Prologue has advanced through V4 and visual production.  
**Resolution:** update OS state model in Phase 1; preserve old file history but replace stale operational status.

### C-002 — project-root naming
**Conflict:** human shorthand refers to Schem'26/novel; repository currently organizes novel work under `living-novel/` plus Prologue production under `chronicles/`.  
**Resolution:** treat `living-novel/` as canonical Novel OS root. Do not invent a new duplicate `novel/` tree solely to match shorthand.

### C-003 — duplicated canon risk
**Conflict:** novel-specific canon, top-level Schemin canon, and production reference files can diverge.  
**Resolution:** Phase 1 must implement authority pointers/registries; shared Schemin canon is referenced, not copied.

### C-004 — approved production vs proof-of-concept path
**Conflict:** mature/approved Prologue work lives under a directory named `proof-of-concept`.  
**Resolution:** path name does not determine authority. Authority comes from artifact status and provenance. Defer physical migration until after integration tests.

### C-005 — manuscript/version ambiguity
**Conflict:** multiple Prologue manuscript generations and spread locks coexist.  
**Resolution:** build an explicit manuscript lineage manifest and map every production spread to its manuscript anchor before any further automated production.

## Missing OS capabilities confirmed by archaeology

The repository has strong doctrine and production artifacts, but Novel OS still needs a unified machine-operable layer for:
- artifact registry and authority resolution;
- source/provenance registry;
- canon mutation protocol;
- manuscript lineage;
- structured narrative state;
- context-pack builder;
- agent routing contracts;
- story-promise ledger;
- deterministic continuity validators;
- semantic Guardian interface;
- workflow state machine;
- approval gates;
- plugin/tool capability registry;
- evaluation fixtures and regression harness;
- live-season-to-narrative transaction;
- unified visual-production adapter contract;
- recovery / last-known-good state;
- operator commands.

## Phase-1 build order

1. System Architecture V1.
2. Data Model V1.
3. Canon Protocol V1.
4. Repository Spec V1 — **in-place architecture, no duplicate tree**.
5. Context Engine V1.
6. Agent Registry V1.
7. Artifact/authority manifest.
8. Manuscript lineage manifest.
9. Prologue production manifest linking V4 → beats → briefs → references → spreads.
10. Acceptance tests before core-engine implementation.

## Production-preservation rule

OS engineering must not block or reset current Prologue production. The Prologue is the integration fixture. New OS components should wrap, index, validate, and route the current production chain before attempting to replace any part of it.

## Phase-0 gate

**PASS WITH REQUIRED RECONCILIATION.**

Evidence demonstrates sufficient existing foundation to enter Phase 1. Phase 1 is authorized to build the missing operating layer in place. No wholesale restructure is authorized.
