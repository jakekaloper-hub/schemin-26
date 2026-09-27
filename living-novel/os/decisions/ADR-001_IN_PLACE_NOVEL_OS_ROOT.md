# ADR-001 — IN-PLACE NOVEL OS ROOT
**Status:** ACCEPTED
## Decision
Use `living-novel/` as the canonical long-lived Novel OS root. Retain the active Prologue workspace at `chronicles/proof-of-concept/prologue/` during integration.
## Why
The repository already contains substantial authoritative work in both locations. Creating a fresh `novel/` or `novel-os/` tree would duplicate truth and increase drift risk.
## Consequences
- Novel OS adds an `living-novel/os/` control layer.
- Shared Schemin services remain upstream and referenced.
- Prologue artifacts are indexed through manifests before any physical migration.
- Migration requires explicit tested procedure and rollback.
