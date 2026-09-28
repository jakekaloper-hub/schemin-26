# Schemin '26 — Enforcement Exception Model V1

**Document class:** control
**Authority / owner:** Umpire + Warden
**Version:** 1.0
**Status:** ACTIVE
**Effective date:** 2026-09-28

## Rule

An exception does not weaken a policy globally. It permits one explicit, reviewable scope.

All active exceptions live in:

`governance/enforcement/EXCEPTIONS_V1.json`

Required fields:
- `exception_id`
- `policy_id`
- `scope_glob`
- `reason`
- `approved_by` (non-empty list)
- `approved_at` (ISO-8601 timestamp)
- `status: ACTIVE`
- at least one of `expires_at` or `review_trigger`

## Approval classes

- `NONE` — policy cannot be excepted.
- `EXPLICIT_COMMISSIONER_ONLY` — must include `Jake / Commissioner`.
- `COMMISSIONER_RELEASE_OVERRIDE` — must include `Jake / Commissioner`.
- `DECLASSIFICATION_REQUIRED` — must include both `Warden` and `Jake / Commissioner`.
- `GOVERNED_EXCEPTION` — must name at least one accountable approver and review trigger/expiry.

## Scope

`scope_glob` is matched against the repository-relative path or validator-defined scope string. Exceptions must be as narrow as practical.

Examples:
- `archive/legacy-canon/**`
- `chronicles/proof-of-concept/prologue/EXPERIMENT.md`
- `release:memo-os/week-4/FINAL.md`

## Anti-bypass

Inline comments, filename suffixes, TODOs, “temporary” prose, or test skips are not valid exceptions.

Expired exceptions fail enforcement until removed or explicitly renewed.
