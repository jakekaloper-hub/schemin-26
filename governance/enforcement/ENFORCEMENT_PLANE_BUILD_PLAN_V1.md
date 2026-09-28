# Schemin '26 — Enforcement Plane Build & Maintenance Plan V1

**Document class:** control / runbook  
**Authority / owner:** Architect + Groundskeeper + Librarian  
**Version:** 1.0  
**Status:** ACTIVE  
**Effective date:** 2026-09-28

## Build loop

Every enforcement unit follows:

**design → implement → test → inspect failure → bug-fix → audit → polish → retest → checkpoint**

Do not advance a unit on an unresolved red gate.

## Completed build units

1. Policy Registry + Enforcement Kernel
2. Authority / Supersession Enforcement
3. Temporal-State Enforcement
4. Mercer Firewall Enforcement
5. Prompt Governance Enforcement
6. Publication / Release Enforcement
7. Governed Exceptions
8. Aggregate Enforcement Orchestrator
9. Coverage Expansion + Adversarial Corruption
10. Closer Certification + durable operating surface

## Future policy admission

When Librarian/Bullpen discovers a material recurring defect:

1. record the defect and source authority;
2. determine BLOCK / RELEASE_BLOCK / WARN;
3. assign policy ID and accountable owner;
4. implement deterministic validator where possible;
5. create positive and corrupt-fixture tests;
6. run aggregate gate;
7. fix false positives without weakening the underlying rule;
8. update coverage matrix and policy registry;
9. Closer certifies the current head.

## Policy promotion

WARN policies may be promoted only after the underlying dependency is executable and tested.

Example:
DATA-001 remains WARN until PR #12 Data Gateway hardening is integrated and operationally verified. It then becomes BLOCK only after:
- code is present;
- contract tests pass;
- aggregate enforcement passes;
- real data/live persistence is proven;
- no repository-visibility/privacy blocker invalidates the data path.

## Exception maintenance

Exceptions are narrow temporary governance records, never inline bypass comments. Expired exceptions fail. Commissioner-only and declassification policies require the specified approvers.

## Release maintenance

RELEASED is a machine state backed by the release registry. FINAL/OFFICIAL filenames alone have zero release authority.

## CI rule

The Schemin Enforcement Gate is intended to become the stable required branch-protection check after PR #12/#15/enforcement reconciliation. Do not require path-filtered subsystem workflows as the only universal gate.
