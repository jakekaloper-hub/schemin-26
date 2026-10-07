# Twelve-Principal POV Migration — Phase 0 Census Update

**Captured:** 2026-10-07  
**Status:** PHASE 0 PASS — EXACT-BRANCH TEXT CENSUS COMPLETE  
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

On 2026-10-07 at 16:43 UTC, the connected Flaim ESPN feed for Pro Schemin' Football League, 2026, matchup period 4 returned six winner fields and totals matching the published Week 4 Memo and PR #128 evidence freeze:

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

## Exact-branch full-tree scan and classification

**Scan target:** PR branch `novel/12-principal-pov-migration`, head `68be03df45d0f558c7cd8b26fcc2c56efef2ba79`.  
**Method:** `git grep -l -I -i -E '\\b(Edrin|Edin|Edrin Vale)\\b|archive[ -]?pov|institutional[ -]?pov|bounded witness[ -]?pov|anonymous omniscient|neutral narrator' HEAD --` against every tracked text blob in the exact branch.  
**Result:** 31 files matched; all matches are classified below. Binary image/PDF assets are not text-searchable and are outside this narrator-dependency census.

### Active dependencies to migrate or supersede (9)

- `living-novel/os/NOVEL_POV_CONSTITUTION_V1.md`
- `living-novel/os/NOVEL_CAUSAL_CHAPTER_ARCHITECTURE_V1.md`
- `living-novel/os/NOVEL_SCORE_ARTIFACT_FOREGROUNDING_DOCTRINE_V1.md` — retain its anti-pattern as guidance, but label/remove named narrator examples in the V2 rewrite.
- `living-novel/os/state/CURRENT_OPEN_LOOP_LEDGER_V1.json`
- `living-novel/whole-book/CHARACTER_POV_TEMPORAL_STATE_MATRIX_V1.md`
- `living-novel/world/AUTHOR_ROOM_UNIVERSE_HYDRATION_STANDARD_V1.md`
- `living-novel/narrative/CHAPTER_01_ARCHITECTURE.md`
- `living-novel/narrative/CHAPTER_02_ARCHITECTURE.md`
- `living-novel/narrative/CHAPTER_03_UNIVERSE_HYDRATION_PACKET_V1.md` — future Edrin bridge language must be superseded; retain as Chapter III production provenance.

### Closed hard-canon manuscript requiring governed migration (3)

- `living-novel/manuscript/PROLOGUE_DRAFT_V1.md`
- `living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md`
- `living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md`

These remain hard canon until exact-byte migration approval transactions replace them.

### Historical evidence to retain without retroactive edits (14)

- `living-novel/qa/CHAPTER_01_EDITORIAL_AUDIT.md`
- `living-novel/qa/PROLOGUE_DRAFT_V1_EDITORIAL_AUDIT.md`
- `living-novel/consultants/author-council/engagements/NOVEL-AUTHOR-CONSULT-2026-10-01-001/00_EVIDENCE_FREEZE.md`
- `living-novel/consultants/author-council/engagements/NOVEL-AUTHOR-CONSULT-2026-10-01-001/BULLPEN_CROSS_EXAMINATION_R1.md`
- `living-novel/consultants/author-council/engagements/NOVEL-AUTHOR-CONSULT-2026-10-01-001/IMPLEMENTATION_DECISION.md`
- `living-novel/consultants/author-council/engagements/NOVEL-AUTHOR-CONSULT-2026-10-01-001/ROUND_1_RECONCILIATION.md`
- `living-novel/consultants/author-council/engagements/NOVEL-AUTHOR-CONSULT-2026-10-01-001/round-1/GEORGE_RR_MARTIN_R1.md`
- `living-novel/consultants/author-council/engagements/NOVEL-AUTHOR-CONSULT-2026-10-01-001/round-1/JOE_ABERCROMBIE_R1.md`
- `living-novel/consultants/author-council/engagements/NOVEL-AUTHOR-CONSULT-2026-10-01-001/round-1/URSULA_K_LE_GUIN_R1.md`
- `living-novel/consultants/author-council/engagements/NOVEL-AUTHOR-CONSULT-2026-10-01-001/round-2/URSULA_K_LE_GUIN_R2.md`
- `living-novel/production/chapter-03/CHAPTER_03_DOSSIER_V2.md`
- `living-novel/production/chapter-03/CHAPTER_03_MINIMUM_PRE_PROSE_GATE_V1.md`
- `living-novel/production/chapter-03/CHAPTER_03_POV_PACKET_WILSON_V1.json`
- `living-novel/production/chapter-03/consultant-review/URSULA_K_LE_GUIN_CH3_GATE_REVIEW.md`

These are evidence of earlier decisions and closed Chapter III work, not current narrator licenses. Preserve them; add supersession references where a future operator could mistake a historical recommendation for current law.

### Expected migration records and non-Novel hit (5)

- `living-novel/migrations/TWELVE_PRINCIPAL_POV_MIGRATION_PROGRAM_V1.md`
- `living-novel/migrations/TWELVE_PRINCIPAL_POV_PHASE0_CENSUS_2026-10-07.md`
- `living-novel/migrations/TWELVE_PRINCIPAL_POV_SEVEN_LENS_CHALLENGE_2026-10-07.md`

These name Edrin solely as the migration target or as review context. They are not active POV dependencies. The task-registry hit is the migration alias `retire Edrin`, not a license. The remaining hit, `memo-os/week-4/WEEK_4_PERSONALIZED_INTELLIGENCE_AMENDMENT_LLC_HMB_CASINO_2026-10-02.md`, uses “institutional POV” as a Memo editorial lens and is outside Novel narrator authority.

**Reconciliation:** 9 active system/architecture dependencies + 3 closed hard-canon manuscripts + 14 historical evidence files + 3 expected migration records + 2 non-narrative/control hits = 31 classified files.

## Phase 0 disposition

**PASS.** The exact-branch tracked-text census is complete, all 31 hit files are classified, the migration's hard-canon boundary is recorded, and `NOVEL-POV-MIG-001` is now present in Execution Control. No hard manuscript canon has been changed by the census.