# Schemin '26 — Branch Protection Target

**Document class:** control  
**Authority / owner:** The Umpire + Groundskeeper  
**Version:** 1.0  
**Status:** TARGET CONFIGURATION — ADMIN APPLICATION PENDING  
**Effective date:** 2026-09-27  
**Review trigger:** CI architecture change, snapshot-write redesign, or repository visibility change

## Main branch target

Protect `main` with:

- pull request required before merge;
- at least one successful required status check: **Repository Merge Gate / Schemin Repository Integrity**;
- branch must be up to date before merge when practical;
- no force pushes;
- no branch deletion;
- administrators should follow the rule unless performing documented incident recovery.

Do **not** require subsystem/path-filtered workflows directly. `Data Gateway CI`, `Novel OS CI`, and `Bullpen Runtime CI` are useful specialized signals, but path filters can cause those checks not to exist on unrelated PRs.

The always-on `.github/workflows/repository-merge-gate.yml` is the stable protection surface. It runs:
- canonical-control existence/JSON checks;
- Data Gateway compile + contract suite;
- Novel OS regression suite;
- Bullpen Runtime test suite.

## data/live target

`data/live` is an operational data branch, not a code-development branch.

Purpose:
- hold `data/snapshots/1417621/latest.json`;
- hold `data/snapshots/1417621/manifest.json`;
- accept automated writes only from the validated ESPN snapshot workflow.

Do not route source-code, governance, canon, prompts, production documents, or human feature work to `data/live`.

If branch/ruleset controls are later applied to `data/live`, they must preserve the trusted GitHub Actions write path while blocking general destructive mutation.

## Separation of duties

```text
main
  code + governance + canon + production state
  human-reviewed merge path
  required Repository Merge Gate

data/live
  machine-updated operational ESPN snapshot state
  no application/source changes
  validated scheduled writer only
```

This separation permits strong protection on `main` without giving the scheduled Data Gateway broad bypass authority over the code branch.

## Current limitation

The connected GitHub application does not expose repository-administration mutation for branch protection/rulesets. This document and Issue #11 define the target, but an authorized GitHub admin must apply the repository setting.
