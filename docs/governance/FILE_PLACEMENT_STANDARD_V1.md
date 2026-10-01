# File Placement Standard V1

## Deterministic placement decision

1. If one subsystem exclusively owns the artifact's truth, place it in that subsystem.
2. If it governs multiple systems through executable/machine-enforced control, place it in `governance/`.
3. If it explains architecture/governance/operations for humans, place it in `docs/`.
4. If it is bounded pre-release, remediation or program planning, place it in `planning/` and declare lifecycle disposition.
5. If it is active cross-system production with no natural owning subsystem, place it in `productions/`.
6. If it is released/historical narrative lineage, place it in `chronicles/`.
7. If it is superseded/inactive but provenance matters, place it in `archive/`.
8. If none applies, STOP and require Librarian review. Do not invent a top-level directory.

## Artifact contract

Durable artifacts should be resolvable as:
`DOMAIN + CLASS + AUTHORITY + STATUS + ENTRY RELATIONSHIP`.

Supported classes:
`CONTROL, CANON, RUNTIME, DATA, SCHEMA, PLAN, WORKING_PRODUCTION, RELEASE, EVIDENCE, RESEARCH, DECISION, DERIVED_INDEX, HISTORICAL, ARCHIVED`.

## Planning lifecycle

Every planning program must declare status, owner, target owning subsystem, graduation criteria and terminal disposition.

- PROMOTED: operational outputs move to the owning subsystem; planning history may remain as provenance.
- CLOSED: objective completed without a permanent subsystem; preserve according to archive policy.
- HOLD: remains in planning with an explicit blocker and next gate.
- CANCELLED: archive with disposition.

Planning may never become an indefinite shadow subsystem.

## Archive lifecycle

Archive only when material is superseded, deprecated, season-complete, excluded from normal routing, and still useful for provenance. Never archive the only known copy of unresolved evidence.

Archive records must preserve original path, archive date, reason, superseding authority and provenance.