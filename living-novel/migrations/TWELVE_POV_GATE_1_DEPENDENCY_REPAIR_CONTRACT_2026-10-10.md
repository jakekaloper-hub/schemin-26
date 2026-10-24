# Twelve-principal POV — Gate 1 Dependency Inventory and Repair Contract
**Mission:** Bullpen #117 / Schemin #129 / PR #130
**Date:** 2026-10-10
**Status:** PARTIAL DISCOVERY — ACTIVE DEPENDENCIES VERIFIED; FULL CENSUS AND IMPLEMENTATION BLOCKED
**Authority:** Proposal on `novel/12-principal-pov-migration` only. No alteration to hard-canon manuscript bytes.

## Branch readback
- Existing migration program at `living-novel/migrations/TWELVE_PRINCIPAL_POV_MIGRATION_PROGRAM_V1.md` retrieved from branch `novel/12-principal-pov-migration`, not current `main`.
- Existing `living-novel/os/NOVEL_POV_CONSTITUTION_V1.md` on this branch still licenses Archive POV and Bounded Witness POV, and specifically states "Edrin remains a canonical major viewpoint." Until V2 is approved, the old license remains.
- Existing migration program proposes phases 0–8, with special Manning/El Niño gate; it is not itself the finished migration.

## Evidence-backed dependency slices
| Source | Observed dependency | Classification | Action | Gate |
|---|---|---|---|---|
| `living-novel/os/NOVEL_POV_CONSTITUTION_V1.md` | Edrin Archive POV and non-Twelve witness licenses | Active OS authority | SUPERSEDE with V2, retain historical V1 for provenance | Constitution approval + automated validator |
| `living-novel/manuscript/PROLOGUE_DRAFT_V1.md` | Edrin receives on-page action/dialogue and narrator focus | Hard-canon manuscript | REBUILD/REASSIGN at scene level, not word replacement | Founder approves exact resulting manuscript bytes |
| `living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md` | Listed by migration program as an active dependency; passages not yet exhaustively inspected | Hard-canon manuscript | INSPECT then classify scene-by-scene | Canon proposal |
| `living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md` | Edrin action/perception explicitly found | Hard-canon manuscript | REBUILD/REASSIGN or DELETE only after causal-function mapping | Founder approves exact resulting manuscript bytes |
| `living-novel/narrative/CHAPTER_01_ARCHITECTURE.md` | Explicit "Open again with Edrin" direction | Active or stale planning instructions; authority to reconcile | SUPERSEDE with twelve-only chapter plan; preserve historical source | Read order and routing QA |
| `living-novel/narrative/CHAPTER_02_ARCHITECTURE.md` | Edrin connective observer and institutional limited POV | Active or stale planning instructions; authority to reconcile | SUPERSEDE with twelve-only chapter plan; preserve historical source | Read order and routing QA |
| `living-novel/os/NOVEL_CAUSAL_CHAPTER_ARCHITECTURE_V1.md` | Allows Edrin/Oren archive function | Active architecture | Move functions to licensed principal POV / in-world artifact or supporting dialogue | Architecture and leakage review |
| `living-novel/qa/CHAPTER_01_EDITORIAL_AUDIT.md` | Historic favorable Edrin assessment | Historical QA | RETAIN as historical evidence; mark superseded only where existing governance supports | No retroactive erasure |
| `living-novel/qa/PROLOGUE_DRAFT_V1_EDITORIAL_AUDIT.md` | Documents Edrin/Oren spine | Historical QA | RETAIN as provenance | No retroactive erasure |

This is a **sampled, not complete repository-wide hit inventory**. Do not report Phase 0 100% pass.

## Execution order (same existing migration program)
1. Expand census across current active trees and PR branch, including case/alias variants `Edrin`, `Edin`, `Oren`, `Archive POV`, `Bounded Witness POV`, `institutional POV`; distinguish history from routing authority.
2. Build scene-level function transfers: scene ID / current narrator / causal necessity / licensed principal candidate / knowledge justification / event and timeline / artifact substitution / conflict / QA owner.
3. Run real Full Seven *published-method* analyses on the actual manuscript, not theoretical author simulation; reconcile with Beat Writer / World Architect.
4. Prepare V2 constitution as a **proposal** with `principal_pov_id` licensed only to the Twelve; explicitly gate elemental El Niño path.
5. Add executable tests against V2 registry and scene manifests; fixture rejects Edrin, Oren, witness and anonymous narrator assignments; fixture accepts 12 licensed IDs only.
6. Draft Prologue replacement and chapter repairs on a review branch; show scene-level diffs; do not auto-promote any changed hard canon.
7. Umpire separately audits POV knowledge, continuity, literary coherence, and source evidence before Founder canon transaction.

## Minimum test contract (not yet executed)
- No active `principal_pov_id` outside the twelve-ID authoritative registry.
- No `principal_pov_id` null for story scenes (explicit bounded documents are not narrator scenes).
- All 12 principal manifests present and chronologically routable.
- Per-scene `knowledge_before + acquired` must support viewpoint claims.
- Multi-view event repeats require nonduplicate consequence, knowledge, or price.
- The exact historical canon blobs remain unchanged until explicit approval.
- El Niño/Manning gate cannot silently pass on generic omniscient prose.

## Status
**IMPLEMENTED:** A branch-local, evidence-backed dependency and repair contract.
**TESTED:** GitHub write/readback only, if independently confirmed.
**NOT IMPLEMENTED:** full census, V2 rewrite, principal scene repair, all twelve manifests, automated QA, literary review.
**NOT PROMOTED:** canon. **NO AUTHENTICATED DIRECTOR CONSULTATION CLAIMED.**
