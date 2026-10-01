# R4 — Repository Control Remediation Receipt

**Mission:** Lunsford × Ezzell External Audit Remediation  
**Gate:** R4 — Enforce the Control Plane at GitHub  
**Status:** REPOSITORY GATE PASS / PLATFORM ADMIN BLOCKED  
**PR:** #57  
**Admin blocker:** #58

## Implementation

R4 adds one path-scoped repository-level check:

`Repository Merge Gate / gate`

The gate routes material changes into existing acceptance suites rather than running every subsystem test on every documentation edit.

Mapped domains:
- Project Mission / registry
- Data Gateway
- Character runtime
- Novel OS
- Memo OS
- World / Atlas / Universe
- Release Evidence
- Bullpen runtime

## Test receipt

Repository Merge Gate run: `36811720127`  
Job: `110208012916`

Result: **PASS**.

Planner suite: **11/11 PASS**.

Covered:
- docs-only routing;
- Memo;
- World;
- Novel;
- Character;
- Bullpen;
- Data;
- Project Registry;
- Release Evidence;
- Character release-evidence anchor;
- deliberate required-command failure propagation.

Bullpen Runtime CI also passed on PR #57.

## Administrative limitation

At execution time, repository readback showed:

- `main.protected = false`
- required status-check enforcement = off
- no required checks

The connected GitHub application exposes repository content/PR/CI writes but no branch-protection/ruleset mutation. No authorized Desktop Commander device is connected.

Exact target is documented at:

`docs/governance/BRANCH_PROTECTION_TARGET_V2.md`

Durable external-action issue:

**#58 — R4 Admin Gate — enforce main branch protection**

Required target:
- PR required;
- `Repository Merge Gate / gate` required;
- branch up-to-date required;
- force pushes disabled;
- deletion disabled;
- admin/bypass enforcement where plan permits.

## Umpire ruling

**Repository merge-gate implementation: PASS.**

**Platform-enforced branch protection: BLOCKED_EXTERNAL.**

R4 is not fully closed until a GitHub protection readback proves the target is active.

Downstream R5–R7 may be audited/planned and prepared, but must not be represented as fully promoted while this prerequisite remains open.
