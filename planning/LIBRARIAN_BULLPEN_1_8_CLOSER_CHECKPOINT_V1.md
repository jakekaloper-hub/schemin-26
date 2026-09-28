# Schemin '26 — Librarian/Bullpen 1–8 Cleanup Closer Checkpoint V1

**Document class:** review
**Authority / owner:** The Closer
**Version:** 1.0
**Status:** FINAL-CI PENDING at creation
**Effective date:** 2026-09-28
**Branch:** `chore/librarian-deprecation-canon-lock-2026-09-28`
**PR:** #15

## Executive objective

Turn the repository-contamination discovery into a permanent learning system:

**approval/correction → authority update → contamination search → fix → regression guard → archive/history disposition → Closer certification**

## Step 1 — Librarian / Repository Memory Architecture

### Audit
Initial cleanup branch contained 439 tracked files. Complexity was concentrated in:
- `chronicles/`: 171 files
- `living-novel/`: 141 files

### Finding
Authority could not safely be inferred from age, filenames, or directory position.

### Fix
Added:
- `docs/governance/REPOSITORY_MEMORY_ARCHITECTURE_V1.md`
- `planning/ACTIVE_AUTHORITY_GRAPH_V1.md`

Established:
- ACTIVE PLANE
- ARCHIVE PLANE
- GIT HISTORY PLANE
- nine-state artifact classification model

### Polish
Explicit cross-PR rule prevents PR #15 from duplicating PR #12 governance work.

### Checkpoint
**PASS**

---

## Step 2 — Character QA / Canon as Executable Authority

### Audit
All 12 Chronicle character packets, master canon, reference layer, Memo OS packets and machine identity registry were compared to the Commissioner-approved plate.

### Bugs found
- Slob/Jordan used retired `Frat-Bro Berserker` as competing title.
- Wilson mixed title and body-form identity.
- Duckhook packet appended team identity to character title.
- Ben/Chins retained retired `Blue-Collar Spoiler` and question-mark variants in active surfaces.
- character packets did not consistently point at one visual-lock control.

### Fix
Approved active titles normalized to:
1. The Trade Jedi
2. The Predator Board
3. Win Ugly
4. Hostile Takeover
5. The Philosopher-Warrior — Arsenal Centaur body-form lock
6. The Podium Shadow
7. The Chili Outlaw
8. The Weather System
9. The Belt Keeper
10. Swamp-Born Menace
11. King of the Impossible Lie
12. The People's Champ

Added/updated:
- master visual canon lock
- master character canon
- reference layer
- all 12 render packets
- active Flaim identity registry
- Memo OS character enforcement
- Week 3 packet register
- Living Novel character/QA surfaces

### Regression
`tests/test_character_canon_lock.py` verifies:
- exact 12-title map;
- one active registry;
- all 12 character packets;
- Wilson title/body-form split;
- Jake NO BELT;
- approved visual-lock checksum.

### Remaining blocker
Issue #14: exact approved plate image bytes still need repository-native materialization.

### Checkpoint
**CONDITIONAL PASS — semantic/machine canon locked; binary plate materialization open**

---

## Step 3 — Architect + Umpire / Competing Authority

### Audit
High-risk duplicate/current-looking artifacts were dependency-checked.

### Bugs found
- `world/canon/SCHEMIN_26_MASTER_CHARACTER_CANON_V1_1.md` declared itself CANONICAL/BINDING while carrying retired character titles.
- root `XCODE_CHATGPT_HANDOFF.md` and `XCODE_HANDOFF_PRO_SCHEMIN_WORLD.md` declared themselves ACTIVE while embedding stale instructions.
- second Flaim identity registry duplicated current identity authority and preserved historical aliases.

### Fix
Quarantined:
- legacy canon → `archive/legacy-canon/`
- legacy handoffs → `archive/legacy-handoffs/`
- duplicate identity registry → `archive/identity-history/`

Removed their former active paths.

### Regression
Repository Memory CI verifies:
- retired active paths do not exist;
- only one active master canon exists;
- only one active Flaim identity registry exists;
- quarantine records are explicitly historical.

### Checkpoint
**PASS**

---

## Step 4 — Groundskeeper / Enforceable Cleanup

### Audit
Manual cleanup alone would be reversible by future contributors or agents.

### Fix
Added:
- `tests/test_repository_memory_hygiene.py`
- `.github/workflows/repository-memory-ci.yml`

Checks cover:
- active-path quarantine decisions;
- archive banners/status;
- authority graph/memory controls;
- temporal lineage;
- Mercer firewall;
- manuscript lineage;
- archive-index truth.

### Bug found during polish
Initial widened workflow path edit duplicated YAML path entries.

### Fix
Workflow rewritten cleanly with one deduplicated trigger set.

### Checkpoint
**PASS subject to final-head CI**

---

## Step 5 — Memo OS / Novel OS / Mercer / Temporal Hygiene

### Audit
Subsystems each contained freshness/version concepts, but there was no cross-subsystem temporal contract.

### Risk
Historical roster, manuscript, weekly, or decision state could be retrieved as current.

### Fix
Added:
- `docs/governance/SUBSYSTEM_TEMPORAL_LINEAGE_CONTRACT_V1.md`

Updated:
- `mercer/OPERATING_CONTRACT.md`
- `living-novel/README.md`

Rules:
- mutable state declares time/period and state class;
- V4 is current Prologue production parent unless superseded;
- old Mercer recommendations are Decision Journal history, not standing instructions;
- PRE_FACT/live snapshots are chronological receipts, not perpetual truth.

### Regression
Repository Memory CI verifies temporal contract exposure.

### Checkpoint
**PASS**

---

## Step 6 — Warden / Retrieval + Privacy

### Audit
Targeted current-tree scan reviewed:
- common committed-secret indicators;
- runtime API credential handling;
- Mercer-private leakage into public creative material.

### Finding
No obvious hard-coded credential was found in the targeted scan.

`renderer_transport.py` consumes `RUNPOD_API_KEY` from runtime environment.

### Real bug found
`PROLOGUE_PRESEASON_EVIDENCE_AND_EMOTIONAL_SPINE.md` imported Mercer grades/judgments into public Chronicle evidence.

### Fix
Removed Mercer grades/private valuation conclusions while preserving public ESPN/draft facts.
Added explicit firewall language.
Normalized character titles in the same evidence packet.

### Regression
Repository Memory CI bans reintroduction of specific Mercer-grade/judgment language while allowing the firewall warning itself.

### Artifact
`planning/WARDEN_RETRIEVAL_PRIVACY_AUDIT_V1.md`

### Checkpoint
**PASS WITH CONTINUING MONITORING**

---

## Step 7 — Historian / Safe Historical Plane

### Audit
Manuscript V1–V3 are valuable lineage and should remain path-stable because manifests/production records refer to them.

### Bugs found
- `PROLOGUE_MANUSCRIPT_V1.md` incorrectly labeled itself “Manuscript V2.”
- V1–V3 did not clearly state that they were superseded historical manuscripts.
- `archive/_INDEX.md` falsely said no files had been intentionally archived.

### Fix
- corrected V1 heading;
- V1–V3 marked **SUPERSEDED HISTORICAL MANUSCRIPT — DO NOT USE AS CURRENT PRODUCTION PARENT**;
- V4 explicitly marked current production parent, not final publication;
- archive index updated to current archive groups;
- added `planning/HISTORIAN_ARCHIVE_MAP_V1.md`.

### Regression
Repository Memory CI verifies:
- V1 identity;
- V1–V3 historical status;
- V4 production-parent status;
- active archive index.

### Checkpoint
**PASS**

---

## Step 8 — The Closer / Integration

### Audit
Current-head CI is required. Prior-green commits do not certify a later head.

### First current-head result
- Bullpen Runtime CI — PASS
- Novel OS CI — PASS
- Character Canon CI — FAIL
- Repository Memory CI — FAIL

### Bugs found by CI
1. Character test still expected the duplicate identity registry intentionally removed in Step 3.
2. Warden test banned the phrase `Mercer grade` even inside the new firewall warning.

### Fix
- Character CI now expects exactly one active identity registry.
- Warden test bans actual imported Mercer-grade/judgment patterns while allowing the firewall warning.

### Final certification rule
Final verdict may be issued only after:
- Character Canon CI = PASS
- Repository Memory CI = PASS
- Novel OS CI = PASS
- Bullpen Runtime CI = PASS

## Open blockers outside the 1–8 code cleanup

1. Issue #14 — materialize exact Commissioner-approved visual plate bytes in Git.
2. PR #12 governance/data-plane work remains separate and must be reconciled before merge ordering is finalized.
3. Repository visibility/private-data governance remains a separate release concern.
4. Repository-wide file-by-file classification is not complete; this pass eliminated the highest-risk active contaminants and installed controls for continuing tranches.
5. Official Week 2 published PDF remains an unresolved recovery item.
6. Original V5.1 hardening patch remains unrecovered.

## Closer posture at document creation

**CONDITIONAL PASS — fixes complete; final-head CI rerun pending.**
