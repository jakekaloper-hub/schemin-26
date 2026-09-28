# Schemin '26 — Repository Integrity & Sync Sweep

**Document class:** review  
**Authority / owner:** The Librarian; final verdict by The Closer  
**Version:** 0.2 remediation checkpoint  
**Status:** IN PROGRESS — REMEDIATION PR PREPARATION  
**Created:** 2026-09-27  
**Review trigger:** merge/post-merge verification or material new finding  
**Baseline branch:** `main`

## Executive checkpoint

The repository is materially healthier and the single-repository operating model is now explicit. The sweep converted repository ownership, canonical artifacts, CI evidence, drift-prevention procedures, and unresolved risks into durable GitHub state.

The project is not yet eligible for a final PASS because the default branch still needs the ESPN persistence repair merged/proven, repository visibility requires a deliberate disposition, and several non-blocking durability/governance items remain open.

## Baseline

- canonical repository: `jakekaloper-hub/schemin-26`
- baseline main SHA: `49194258ef60c3d467d6f1cdf9926c1a4cc84cc5`
- baseline visibility: **public**
- baseline main protection: **disabled**
- local workspace state: `NOT_ATTESTABLE_FROM_CURRENT_RUNTIME`
- recursive tree at sweep branch checkpoint: **440 files / 138 directories**
- Markdown: 387; JSON: 26; Python: 10; JavaScript: 11; YAML: 5

## Repository authority

Confirmed:
- `schemin-26` is the canonical durable project repository.
- `fantasy-league-artworks` is the only other GitHub repo explicitly referenced in the current tree and remains an upstream reusable platform, not an alternate project home.
- Schemin-specific Bullpen evidence/runtime lives in this repository.
- External tools/providers supply capabilities/evidence; they do not become project truth by recency.

Durable controls added:
- `docs/governance/REPOSITORY_INTEGRITY_SWEEP_CONTROL_V1.md`
- `docs/governance/CROSS_REPO_SOURCE_OF_TRUTH_MATRIX.md`
- `docs/governance/CANONICAL_ARTIFACT_REGISTER.md`
- `docs/architecture/REPOSITORY_DEPENDENCY_MAP.md`
- `docs/ops/REPOSITORY_SYNCHRONIZATION_PLAYBOOK.md`
- `planning/repository_state_manifest_2026-09-27.json`

## Production continuity

Week 3 is not chat-only. `memo-os/week-3/` contains committed evidence, continuity, historical, lineup, Monday exposure/close, character/reference, composition, mobile, Fact Lock, and QA records.

Memo OS control drift was repaired:
- subsystem index already identified V5.4 as controlling hardening and V5.3 as binding character/reference enforcement;
- top-level `PROJECT_CONTROL_REGISTRY.md` and `README.md` were updated on the sweep branch to match that reality.

## CI and test evidence

See `planning/REPOSITORY_SWEEP_CI_EVIDENCE_2026-09-27.md`.

Observed:
- Bullpen Runtime CI — green on baseline main and sweep commits.
- Novel OS CI — multiple recent green main runs.
- Novel OS ZeroGPU Smoke — successful real smoke run at tested commit.
- Data Gateway CI — added during sweep; first run PASS.

## Critical Data Gateway defect and repair

### Finding

The scheduled ESPN workflow successfully fetched and validated league 1417621, but default-branch `data/snapshots/1417621/latest.json` was absent.

The commit step checked:

`git diff --quiet -- data/snapshots/1417621`

before staging. Git diff ignores untracked files, so a first/new snapshot directory could cause a clean exit even though validated snapshot files had just been written.

The writer also omitted required `snapshot_age_seconds` metadata from the documented freshness contract.

### Repair

Sweep branch changes:
- stage the snapshot directory first;
- gate on `git diff --cached --quiet`;
- emit `snapshot_age_seconds: 0` at fresh acquisition;
- refactor writer into testable functions without changing the acquisition contract;
- add atomic-write/freshness/workflow-order regression tests;
- add dedicated `Data Gateway CI`.

Data Gateway CI run 1 / id `36373200079` passed compile and all contract tests.

### Remaining proof

One post-merge scheduled/manual ESPN run must persist the snapshot on the default branch before RIS-009 can close.

## PR hygiene

Closed as superseded/satisfied, without merge:
- PR #7 — certification attempt with failed Novel OS CI
- PR #8 — later successful certification attempt, superseded
- PR #9 — successful certification trigger whose purpose is now satisfied by later main CI history

Preserved open:
- PR #4 Digital Universe R&D — substantive
- PR #6 Commissioner Bot foundation — substantive

## Security and visibility

No obvious committed secrets were found in targeted searches for common credential patterns. This was not a full-history secret-scanner certification.

GitHub reports the repository as public while project governance anticipates private Mercer/sensitive material. Issue #10 tracks the required disposition. No repository-visibility mutation was made autonomously.

## Path / artifact integrity

A targeted audit of high-value indexes/control documents against the recursive tree found two missing referenced artifacts:

1. `SCHEMIN_26_WEEKLY_MEMO_OS_V5_1_DATA_HARDENING_PATCH.md` — already known and intentionally not fabricated.
2. `Week 2 memo.pdf` — Commissioner-designated official publication is referenced but absent from the GitHub tree.

A Library recovery search found similarly named later/test PDFs, but governance explicitly prohibits substituting those for the official published edition. Issue #5 now records the recovery gap.

## Open material risks

P1:
- RIS-001 — public/private-material boundary.
- RIS-009 — ESPN durable snapshot repair requires merge + runtime proof.

P2:
- RIS-002 — branch protection/ruleset design, tracked by Issue #11.
- RIS-005 — local workspace state not attestable here.
- RIS-006 — original V5.1 patch unrecovered.
- RIS-010 — exact official Week 2 PDF absent.

## Closer checkpoint

**CONDITIONAL PASS — REMEDIATION BRANCH READY FOR REVIEW, NOT FINAL SWEEP CLOSURE.**

The repository has a coherent canonical-home model, current production state is durably represented, stale certification PRs are reconciled, CI evidence is materially stronger, a real Data Gateway durability defect has been repaired and regression-tested, and control-document drift has been corrected. Final closure remains gated by merge/post-merge ESPN persistence proof and the explicit visibility decision; branch protection, local-workspace attestation, V5.1 source recovery, and the official Week 2 PDF are tracked non-destructive follow-ups.
