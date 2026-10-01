# R3 — SHA-Bound Release Evidence Receipt

**Mission:** Lunsford × Ezzell External Audit Remediation  
**Gate:** R3 — SHA-Bound Release Evidence  
**Status:** PASS  
**PR:** #56

## Defect

Historical green release/acceptance prose could remain visible after a subsystem advanced to a newer blocked/red state. Memo V5.6 demonstrated the failure class: an older engineering PASS coexisted with a current-head Acceptance CI failure.

## Implementation

R3 adds a compact governance utility under `governance/release-evidence/`:
- machine-readable release/acceptance registry;
- exact tested commit SHA;
- branch;
- execution timestamp;
- test suite;
- required-check conclusions;
- unresolved blockers;
- subsystem anchor path + exact Git blob SHA;
- current-applicability resolver.

Resolver behavior:
- exact tested commit + unchanged subsystem + green required checks → `CURRENT_HEAD_PASS`;
- later unrelated repository commits + unchanged subsystem → `CURRENT_SUBSYSTEM_PASS`;
- changed subsystem bytes → `HISTORICAL_ONLY_CHANGED_SUBSYSTEM`;
- explicit historical receipt → `HISTORICAL_ONLY`;
- any required red check → `BLOCKED_CURRENT_EVIDENCE` regardless of a PASS label.

## Applied systems

- Memo OS V5.5 — ACTIVE pass evidence.
- Memo OS V5.6 — RELEASE CANDIDATE / current blocking evidence.
- Character R2 generation enforcement — ACTIVE safety-boundary pass.
- Character production — explicit BLOCKED receipt.
- Universe OS V1.2 — RELEASED / ACTIVE pass evidence.

## Test receipt

Release Evidence CI run: `36811355793`  
Job: `110206887238`

Result: **7/7 PASS + registry validation PASS for 5 systems**.

Adversarial coverage:
- old green + same subsystem bytes;
- old green + changed subsystem bytes;
- red required check overriding PASS;
- explicit historical pass;
- exact-head pass;
- explicit blocked receipt;
- no false ACTIVE status in the real registry.

Project Mission CI and Bullpen Runtime CI also passed on the R3 PR head.

## Umpire ruling

**R3 PASS.**

Historical evidence remains preserved, but release applicability is now machine-resolved rather than inferred from optimistic/stale prose.
