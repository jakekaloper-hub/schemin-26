# Schemin '26 — Bullpen Second-Line Platform Audit

**Document class:** review  
**Authority / owner:** Bullpen — Architect, Librarian, Groundskeeper, Warden, Umpire; Closer synthesis  
**Version:** 1.0  
**Status:** ACTIVE REVIEW — PR #12  
**Created:** 2026-09-27  
**Review trigger:** PR #12 head change, merge, post-merge ESPN persistence proof, or visibility disposition

## Mandate

Review and challenge the Librarian-led repository integrity sweep, verify its claims against live GitHub state, identify defects the first pass missed, and repair the Schemin '26 operating platform where evidence supports a safe change.

## Executive assessment

The Librarian sweep was directionally correct and materially valuable, but its report became stale while the remediation branch continued evolving. Bullpen therefore re-baselined the actual PR rather than treating the earlier report as authoritative.

At second-line audit start:
- PR #12 had grown from the earlier 18-commit / 16-file checkpoint to 40 commits / 26 files;
- PR #12 was draft;
- current `main` was still `49194258ef60c3d467d6f1cdf9926c1a4cc84cc5`;
- the remediation branch had introduced a dedicated `data/live` operational branch design and additional Data Gateway hardening.

## What Librarian got right

1. `schemin-26` is the canonical project repository.
2. External FLA capability is upstream/reusable, not alternate Schemin truth.
3. V5.4/V5.3 needed to supersede the stale top-level V5.2-RC navigation wording.
4. Certification-only PRs #7–#9 were stale and safe to close without merging.
5. The original ESPN persistence workflow had a real first-write defect: pre-stage `git diff` ignored untracked snapshots.
6. The repository-public/private-material boundary is unresolved and materially important.
7. The exact official `Week 2 memo.pdf` must not be replaced by a similarly named later/test artifact.
8. A final PASS would have been premature.

## Additional defects Bullpen found

### BPA-001 — Librarian report drift

**Severity:** P1 process integrity

The remediation branch continued changing after the Librarian checkpoint. The earlier report no longer described the actual PR head.

**Repair:** this second-line audit re-baselines against the current PR and requires audit refresh after material head changes.

### BPA-002 — degraded-state persistence was not actually executable

**Severity:** P1 data reliability

The redesigned workflow wrote snapshots to `data/live`, but it attempted the ESPN refresh before hydrating the last-known-good snapshot from that branch. On a network/contract failure, the Python process therefore had no local LKG to mark stale.

That contradicted the documented contract:
`preserve last-good payload → mark stale/failure metadata → persist degraded state → workflow remains red`.

**Repair:** `.github/workflows/espn-cold-standby.yml` now hydrates `latest.json` and `manifest.json` from `data/live` before the refresh attempt. Regression coverage requires hydration to occur before refresh.

### BPA-003 — executable runtime and mirror documentation disagreed

**Severity:** P2 truth/documentation

`OPERATIONAL_PATCH_v1.0.md` initially instructed the runtime to try configured mirrors while later admitting the committed implementation did not support mirrors.

**Repair:** the executable contract is now stated consistently as:

`direct ESPN → validation → data/live snapshot → degraded LKG on failure`.

Mirrors remain an architectural extension point only.

### BPA-004 — payload validation was structurally too weak

**Severity:** P1 data integrity

The gateway previously accepted:
- an empty schedule as long as the key existed;
- duplicate team IDs;
- zero-player team rosters.

These states are structurally present but not acceptable canonical league payloads.

**Repair:** validation now requires:
- exactly 12 teams;
- unique non-missing team IDs;
- non-empty schedule;
- settings/status object types;
- present non-empty roster entries per team;
- roster entries not exceeding settings-derived capacity.

Regression tests cover each new rejection case while retaining legitimate 17–19 roster variance.

### BPA-005 — branch protection had no stable required check

**Severity:** P1 governance/CI

Subsystem workflows are path-filtered and therefore unsuitable as the sole required checks for `main`; absent checks can make protection brittle.

**Repair:** added `.github/workflows/repository-merge-gate.yml`, an always-on gate that runs:
- canonical control-surface validation;
- Data Gateway compile + contract tests;
- Novel OS regression suite;
- Bullpen Runtime tests.

First clean version of the gate passed on both push and PR events. A deliberate intermediate failure caused by commit sequencing was detected, then the corrected fixture head passed.

### BPA-006 — main/data write responsibilities were coupled

**Severity:** P1 architecture

Direct scheduled snapshot commits to `main` conflicted with strong branch protection.

**Repair:** operational league-state churn is isolated to `data/live`; source/governance/canon/production state remains on `main`.

Target branch-control architecture is documented in:
`docs/governance/BRANCH_PROTECTION_TARGET_V1.md`.

## Current target architecture

```text
ESPN
  ↓
scheduled GitHub Action
  ↓
hydrate LKG from data/live
  ↓
fetch + validate
  ├─ success → fresh snapshot
  └─ failure → preserve LKG + stale/failure metadata
  ↓
persist operational state to data/live
  ↓
consumers resolve data/live + recompute freshness at read time

main
  code / governance / canon / production state
  ↓
PR
  ↓
Repository Merge Gate
  ↓
protected merge
```

## CI evidence

Observed during this second-line audit:

- Data Gateway CI — repeated green runs on the remediation branch after hardening.
- Bullpen Runtime CI — green on current remediation progression.
- Repository Merge Gate:
  - first clean implementation: PASS;
  - one intermediate push failed because new validation landed before fixture update;
  - corrected current-head push: PASS;
  - PR-head gate reran after the corrected fixture and is the merge signal to watch.

The intermediate failure is retained as useful evidence that the new gate catches real cross-subsystem incompatibility.

## Security posture

The repository is still reported by GitHub as public.

Bullpen agrees with the Warden gate: do not merge operational snapshot persistence until one of these is explicit:
1. repository becomes private; or
2. a reviewed/redacted public snapshot contract is approved.

Because the project mandate is that all Schemin '26 activity lives in this repository, **private repository visibility is the simpler and safer target architecture**. This audit does not mutate repository visibility because the connected application does not expose repository-administration controls and the disposition should remain explicit.

## Branch protection posture

The architecture problem is solved but the GitHub setting is not yet applied.

Recommended `main` protection:
- PR required;
- required check: **Repository Merge Gate / Schemin Repository Integrity**;
- no force pushes;
- no branch deletion;
- admin bypass only for documented recovery.

`data/live` remains the operational writer branch and must never become a second source-code branch.

## Remaining blockers

### P1
- repository visibility/private-material disposition (Issue #10);
- post-merge operational proof that the scheduled job creates/updates `data/live:data/snapshots/1417621/latest.json` and degraded-state behavior is executable.

### P2
- branch-protection target must be applied by an authorized GitHub admin (Issue #11);
- exact original V5.1 Data Hardening Patch remains unrecovered;
- official published `Week 2 memo.pdf` remains absent from GitHub;
- arbitrary developer-local workspace state remains outside this GitHub-only attestation.

## Bullpen / Closer verdict

**CONDITIONAL PASS — PLATFORM ARCHITECTURE HARDENED, RELEASE GATES STILL OPEN.**

PR #12 is substantially stronger than at the Librarian checkpoint. The platform now has:
- clear repository authority;
- stronger truth contracts;
- a separated operational data plane;
- real degraded-state semantics;
- stronger ESPN payload validation;
- always-on merge-gate CI;
- an actionable branch-protection target;
- durable provenance/audit records.

Do not call the sweep fully closed until the visibility decision is resolved and a post-merge ESPN run proves the operational data plane end to end.
