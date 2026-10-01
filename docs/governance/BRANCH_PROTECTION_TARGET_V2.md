# Schemin ’26 — Main Branch Protection Target V2

**Status:** TARGET / PLATFORM-ADMIN APPLICATION REQUIRED  
**Branch:** `main`  
**Required check:** `Repository Merge Gate / gate`

## Objective

Make the existing Schemin control plane technically enforceable at the Git boundary without requiring every subsystem suite on every documentation change.

The repository-level merge gate is path-scoped and reuses existing domain acceptance suites.

## Required GitHub settings

For `main`:

- Require a pull request before merging: **ON**
- Required approving reviews: **0** (solo-operator velocity; automated independent gates remain mandatory)
- Require status checks to pass before merging: **ON**
- Required check: **Repository Merge Gate / gate**
- Require branches to be up to date before merging: **ON**
- Allow force pushes: **OFF**
- Allow deletions: **OFF**
- Enforce for administrators / bypass actors where the GitHub plan permits: **ON**
- Do not permit a red required check to be bypassed as routine operating practice.

## Path-scoped gate behavior

The single required check routes changes into existing suites:

- project mission/control → Mission validator
- Data Gateway → Data Gateway contract + persistence tests
- character runtime / CCCP integration → Character Lock suite
- Novel OS → Novel OS regression
- Memo OS → V5.5 + Week 4 preproduction acceptance
- World/Atlas/Universe → World acceptance suites
- release evidence → Release Evidence CI logic
- Bullpen runtime → Bullpen runtime tests
- docs-only changes with no controlled subsystem impact → merge-gate planner test only

## Administrative boundary

The connected ChatGPT GitHub application can create branches, files, pull requests, CI workflows and merges, but does not expose repository-administration mutation for branch protection/rulesets.

Therefore this target is not considered ACTIVE merely because this file or the merge-gate workflow exists.

R4 closes only when a readback of GitHub branch protection shows the required check and pull-request rule are actually enforced.
