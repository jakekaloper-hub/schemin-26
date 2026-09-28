# Schemin '26 — Enforcement Plane

**Authority:** Bullpen / Librarian / Umpire / Warden / Groundskeeper / The Closer  
**Version:** 1.0  
**Status:** ACTIVE FEATURE — dependent on PR #15 until merged  
**Effective date:** 2026-09-28

## Purpose

Convert approved Schemin '26 truth and Librarian audit findings into machine-enforced repository behavior.

## Load order

1. `SCHEMIN_POLICY_REGISTRY_V1.json`
2. `CANON_ASSERTIONS_V1.json`
3. `EXCEPTION_MODEL_V1.md`
4. `EXCEPTIONS_V1.json`
5. `RELEASE_MANIFEST_CONTRACT_V1.md`
6. `RELEASE_REGISTRY_V1.json`
7. `validate.py`
8. `POLICY_COVERAGE_MATRIX_V1.md`

## Enforcement modes

- **MERGE** — protects repository correctness.
- **RELEASE** — adds release/publication requirements on top of merge safety.
- **AUDIT** — evaluates non-blocking integration/debt policies.

## Severity

- **BLOCK** — failure blocks merge and release.
- **RELEASE_BLOCK** — warning during merge, failure during release.
- **WARN** — visible audit signal; never silently certified as complete.

## Aggregate CI

`.github/workflows/enforcement-plane-ci.yml`

The aggregate gate runs:
- Enforcement kernel tests;
- Character Canon regression;
- Repository Memory regression;
- Novel OS regression;
- Bullpen Runtime regression;
- merge enforcement;
- release enforcement.

## Current external dependency

DATA-001 remains WARN/AUDIT until PR #12's hardened Data Gateway is reconciled into the canonical branch. After the following exist and pass:
- `data-gateway/check_snapshot_health.py`
- `tests/test_data_gateway_snapshot_contract.py`
- `.github/workflows/data-gateway-ci.yml`
- ESPN workflow persistence to `data/live`
- `snapshot_age_seconds` freshness contract

the policy should be promoted from WARN/AUDIT to BLOCK/MERGE after integration testing.

## Prime rule

Jake approves truth once. Librarian records it. Bullpen enforces it. CI prevents regression. Archive preserves history.
