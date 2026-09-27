# NOVEL OS REPOSITORY SPEC V1
**Status:** PHASE-1 BASELINE
## Ruling
Novel OS evolves in place under `living-novel/`. Do not create a duplicate top-level novel tree.
## New OS control layer
`living-novel/os/` — architecture, protocols, registries, manifests, schemas and runtime documentation.
## Existing domains retained
`living-novel/characters/` — novel character records.
`living-novel/world/` — world model.
`living-novel/history/` — interpreted/reconstructed history.
`living-novel/manuscript/` — long-lived manuscript publication lineage where applicable.
`living-novel/qa/` — editorial/publication QA.
`living-novel/research/` — archaeology/research.
`living-novel/weekly-ledger/` — live-season evidence/significance records.
## Shared upstream services — reference, do not copy
`/canon`, `/data-gateway`, `/schemas`, `/tests`, `/docs/governance`, `/skills`.
## Active production workspace
`chronicles/proof-of-concept/prologue/` remains the Prologue workspace until a tested migration is approved.
## Planned OS subdomains
`living-novel/os/registries/`
`living-novel/os/manifests/`
`living-novel/os/schemas/`
`living-novel/os/decisions/`
`living-novel/os/evaluations/`
`living-novel/os/fixtures/`
`living-novel/os/runbooks/`
Create only when populated by operational artifacts.
## Naming
Stable architecture: `NOVEL_OS_<SUBSYSTEM>_V#.md`.
ADRs: `ADR-###_<TOPIC>.md`.
Machine records: lowercase snake_case JSON/YAML where implementation requires.
## Migration doctrine
Index first, move later. No path migration without source/destination manifest, checksum/content verification, inbound-reference update, regression test and rollback plan.
