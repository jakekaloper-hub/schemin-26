# ADR-003 — REPOSITORY-NATIVE STATE FIRST
**Status:** ACCEPTED
## Decision
Novel OS v1 stores authoritative structured records as schema-validated repository files. Databases, vector stores and knowledge graphs may be introduced as derived indexes after the fixtures stabilize.
## Board record
Toolsmith preferred an early database/graph. Librarian preferred Git-native durable state. Continuity required structure regardless of storage. The Closer selected schema-first repository state because it is portable, reviewable, recoverable and avoids premature vendor/storage lock-in.
