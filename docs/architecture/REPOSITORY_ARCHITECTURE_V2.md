# Schemin '26 Repository Architecture V2

**Status:** ACTIVE CANDIDATE pending acceptance gate
**Authority:** The Librarian + The Architect; final promotion by The Closer

## Principle

Structure follows authority. Files live with the subsystem that owns their truth. Lifecycle folders describe state, not alternate authority.

## Canonical top-level model

```text
schemin-26/
├── README.md
├── SCHEMIN_26_PROJECT_MISSION.md
├── PROJECT_CONTROL_REGISTRY.md
├── MIGRATION_LEDGER.md
├── canon/
├── data-gateway/
├── data/
├── memo-os/
├── living-novel/
├── world/
├── mercer/
├── bullpen/
├── bullpen-runtime/
├── governance/
├── docs/
├── schemas/
├── skills/
├── tests/
├── planning/
├── productions/
├── chronicles/
├── archive/
├── prompts/
└── .github/
```

The machine-readable authority for this list is `governance/repository-architecture/FOLDER_DOMAIN_REGISTRY_V2.json`.

## Domain laws

### Owning domains
`canon/`, `data-gateway/`, `memo-os/`, `living-novel/`, `world/`, and `mercer/` own their domain truth and operational artifacts.

### Cross-system control
`governance/` contains executable or machine-enforced cross-system controls: registries, validators, release gates, policy contracts, task state and machine authority maps.

`docs/governance/` contains human-readable governance doctrine: source hierarchy, authority explanation, documentation standards and operating policy.

### Bullpen
`bullpen/` stores Schemin-specific review, decisions, remediation and evidence. `bullpen-runtime/` contains executable adapters to canonical Bullpen Core. Neither may recreate Bullpen Core inside Schemin.

### Lifecycle surfaces
`planning/` is bounded pre-release/remediation/program work. It must graduate to PROMOTED, CLOSED, HOLD or CANCELLED.

`productions/` is exceptional cross-system working production only when no single subsystem naturally owns the work.

`chronicles/` preserves historical/released narrative lineage and proof-of-concept material. It has no authority over active Living Novel manuscript/canon.

`archive/` contains superseded, deprecated or season-complete material excluded from normal routing but retained for provenance.

### Support surfaces
`data/`, `docs/`, `schemas/`, `skills/`, `tests/`, `prompts/`, and `.github/` support the domain systems without becoming competing domain authorities.

## Entry-point law

Every registered first-class top-level directory except `.github/` must declare one canonical human entry point in the folder registry. Additional README/index files may exist only as supplementary navigation and must not create competing authority.

## Depth and density

No global numeric depth/file-count cap is imposed. High density is acceptable where semantic substructure remains coherent and a canonical entry point exists. Depth becomes a defect only when it creates ambiguous ownership, duplicate authority, or navigation failure.

## New top-level directory rule

A new top-level directory requires Librarian placement review plus an update to the folder registry, Catalog/Inventory where applicable, and architecture tests. If an existing domain can own the artifact, no new top-level directory should be created.

## Current migration ruling

V2 requires no P0/P1 path relocation. Missing entry points, stale architecture documentation and machine enforcement are repaired in place. Root Xcode handoff files are P2 cleanup candidates and remain untouched in V2.