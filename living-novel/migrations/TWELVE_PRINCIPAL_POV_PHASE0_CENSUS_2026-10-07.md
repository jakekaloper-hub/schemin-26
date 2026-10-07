# Twelve-Principal POV Migration — Phase 0 Census Update

**Captured:** 2026-10-07  
**Status:** INITIAL CENSUS / NOT CLOSED  
**Controlling work:** Issue #129; PR #130; `living-novel/migrations/TWELVE_PRINCIPAL_POV_MIGRATION_PROGRAM_V1.md`  
**Purpose:** Record the first evidence-backed dependency set and production blockers before drafting a migration transaction.

## Search method and limits

The census used the repository's GitHub code search on the default branch for `Edrin`, `Edin`, `Archive POV`, and `Chapter 01 Edrin`, then opened the task registry, POV constitution, project control registry, migration program, and Chapter IV PR metadata.

This is a **bounded initial census**, not an exhaustive whole-tree proof. The connector's code search returns ranked excerpts, not a complete file inventory; therefore Phase 0 remains open until the repository-native search/validator is run against the exact migration branch and hard-canon set.

## Confirmed active dependencies to migrate or supersede

| Artifact | Current dependency | Required treatment |
|---|---|---|
| `living-novel/os/NOVEL_POV_CONSTITUTION_V1.md` | Licenses Archive POV and states Edrin remains a major viewpoint | Supersede through governed V2 transaction; preserve V1 as history |
| `living-novel/os/NOVEL_CAUSAL_CHAPTER_ARCHITECTURE_V1.md` | Archive-role language assigns verification/history functions to Edrin/Oren | Update so institutions and records remain world objects, never POV licenses |
| `living-novel/world/AUTHOR_ROOM_UNIVERSE_HYDRATION_STANDARD_V1.md` | Knowledge boundary refers to Edrin/Oren; also says El Niño is never POV | Retain knowledge limits; remove narrator entitlement only through approved change |
| `living-novel/whole-book/CHARACTER_POV_TEMPORAL_STATE_MATRIX_V1.md` | Edrin has a primary institutional-POV row; Twelve principals have uneven state depth | Convert to 12 principal rows and define per-character readiness; do not equalize by fiat |
| `living-novel/narrative/CHAPTER_01_ARCHITECTURE.md` | Explicitly reopens with Edrin for continuity | Replace continuity bridge with licensed principal-owned causality |
| `living-novel/narrative/CHAPTER_02_ARCHITECTURE.md` | Edrin remains a connective observer | Replace connective narration or retain only as a historical architecture record |
| `living-novel/manuscript/PROLOGUE_DRAFT_V1.md` | Edrin/Oren and Archive carry the opening frame | Back-migrate under the exact-byte canon process |
| `living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md` | Edrin sees, knows, interprets, and bridges events | Back-migrate without altering verified outcomes or silently reopening canon |
| `living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md` | Edrin remains embodied narrator/observer | Back-migrate with knowledge and scene-owner checks |
| `living-novel/os/state/CURRENT_OPEN_LOOP_LEDGER_V1.json` | Open-loop entities include Edrin/Oren/Archive | Preserve institutional loops; detach them from mandatory viewpoint |
| `living-novel/narrative/CHAPTER_03_UNIVERSE_HYDRATION_PACKET_V1.md` | Recommends Wilson POV plus possible later Edrin institutional POV | Keep Wilson-owned Chapter III scene; remove future Edrin bridge assumption |
| `living-novel/production/chapter-03/CHAPTER_03_DOSSIER_V2.md` | Explicitly rejects Edrin as bridge for Chapter III | Preserve as precedent; reconcile template language only where needed |

## Hard-canon and historical boundary

The project control registry states the Prologue, Chapters I–III are **HARD MANUSCRIPT CANON / CLOSED**. The migration may not rewrite their active bytes by an ordinary document edit. They remain the governing text until each has an approved exact-byte migration transaction. Existing audits, consultant rounds, cross-examinations, and release receipts are historical evidence; retain them and add supersession records rather than retroactively changing what their authors reviewed.

The prior Full Seven engagement's conclusions that Edrin was a licensed POV and not the default camera are not authority for the new Commissioner-directed retirement. The current migration is a superseding mandate and requires its own Full Seven architecture review under the active Author Council program.

## Reusable evidence and precedents

- Chapter III's approved Wilson-limited packet and manuscript demonstrate that a principal can own the scene while institutional verification occurs inside that scene.
- The active book architecture already rejects source-week/chapter equivalence and allows omitted outcomes to remain in shared evidence/state.
- Prior Author Council records explicitly identify the risk of Edrin as a narrative monopoly and of a uniform observational tone; carry these as regression risks, not as a claim that the new system has passed.
- PR #128 is a reviewed Chapter IV soft-manuscript/canon-proposal candidate. Its body states a fresh provider-finality revalidation is still required; do not promote it or use memo publication as a substitute.
- The official Week 4 Memo pair is publication evidence and editorial framing. It is not authoritative league-stat or provider-finality evidence.

## Special unresolved dependency

Manning / El Niño remains a migration blocker. Current authorities describe El Niño as a storm and prohibit El Niño itself from becoming a POV. Do not invent a thirteenth narrator, grant weather omniscience, or assume the storm is Manning's consciousness. The Character Director and World Architect must resolve a licensed Twelve-principal path using existing canon, with Umpire review, before a path is authored. Until then that path is visibly blocked.

## Week 4 evidence snapshot — corroboration only

On 2026-10-07 at 16:44 UTC, the connected Flaim ESPN feed for Pro Schemin' Football League, 2026, matchup period 4 returned six winner fields and totals matching the published Week 4 Memo and PR #128 evidence freeze:

| Winner | Opponent | Provider-returned total |
|---|---|---:|
| ObiWan Jacoby | D0nkey K0ng | 157.33–139.67 |
| Three Dreaded Snake | Mud Dogs | 149.84–126.98 |
| Red Leopards | Dr. Duckhook | 164.08–128.36 |
| Slob on my Dobb | The Chili Cheesers | 190.72–139.96 |
| His Majesty's Blood | The LLC | 177.32–138.87 |
| El Niño | Seven Deadly Chins | 170.62–106.20 |

This response exposes matchup winner fields but no explicit aggregate `DECIDED`/provider-finality status. It therefore corroborates values and pairings only; PR #128's explicit provider-finality gate remains open pending its required deterministic revalidation receipt.

## Execution-control reconciliation

The current `governance/execution-control/TASK_REGISTRY_V1.json` contains 17 tasks and no task for Issue #129 / PR #130's Twelve-POV migration. It does contain the separate Novel continuation task (`NOVEL-NEXT-002`), which remains `NOT_STARTED` and depends on `MEMO-W4-002`; the latter is `WAITING_EXTERNAL`. This migration therefore needs a normalized execution-control entry before its status can be called complete.

## Phase 0 disposition

**HOLD / CONTINUE.** The first known dependency set and hard-canon boundaries are recorded. Phase 0 cannot be closed until an exact-branch full-tree scan confirms all active dependencies, distinguishes historical evidence from active prose/templates, and reconciles the migration into the normalized execution registry. No manuscript canon has been changed by this census.
