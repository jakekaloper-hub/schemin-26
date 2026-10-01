# Repository Structure Audit V2

## Librarian ruling

The domain-first repository architecture is fundamentally sound. The project has outgrown the original documentation and placement conventions, not the domain model itself.

**Decision:** retain current top-level domains; do not launch a broad relocation campaign.

## Structural health

### Strong / coherent
- `canon/`
- `data-gateway/`
- `memo-os/`
- `living-novel/`
- `world/`
- `mercer/`
- `bullpen-runtime/`

These have clear semantic ownership even where internal complexity is high.

### Needs governance hardening
- `governance/` vs `docs/governance/`
- `planning/`
- `productions/`
- `chronicles/`
- `bullpen/` vs `bullpen-runtime/`
- cross-cutting support surfaces `data/`, `schemas/`, `skills/`, `docs/`

## Directory-health observations

- `living-novel/`: high density and depth are justified by manuscript, OS, consultants, production, QA and state separation. Do not flatten.
- `world/`: large but internally modular; missing root navigation is the primary defect.
- `chronicles/`: high density, especially proof-of-concept and production lineage. Its role must be explicitly historical/released lineage, not active Novel authority.
- `memo-os/`: high root-file density but strong `_INDEX.md` prevents it from becoming an ungoverned dump.
- `canon/`: strong domain, but multiple overview files must declare `_INDEX.md` as canonical entry.
- `planning/`: active programs can remain while HOLD/active, but require target subsystem + graduation rule.
- `productions/`: keep only exceptional cross-system workspaces; domain-owned production remains within its domain.

## Boundary decisions

### governance/ vs docs/governance/
- `governance/` = executable or machine-enforced cross-system control: registries, validators, gates, contracts, task state.
- `docs/governance/` = human-readable doctrine, source hierarchy, authority explanation and documentation standards.

### living-novel/ vs chronicles/
- `living-novel/` = active Novel OS, manuscript, literary canon, chapter production and QA.
- `chronicles/` = historical/released narrative lineage, legacy/proof-of-concept visual/narrative artifacts. It cannot become current manuscript authority.

### productions/
Use only when work spans domains and no single subsystem owns the production lifecycle. Domain-specific production stays under its owning subsystem.

### planning/
Planning is a lifecycle state, not a permanent subsystem. Every program must declare PROMOTED, CLOSED, HOLD or CANCELLED disposition and a target owner.

### bullpen/ vs bullpen-runtime/
- `bullpen/` = Schemin-specific reviews, decisions, remediation and evidence.
- `bullpen-runtime/` = executable project adapter to canonical Bullpen Core.

## Migration ruling

No P0/P1 file relocation is required for V2 activation. The defects can be closed through canonical entry-point declarations, missing README/index creation, a machine-readable folder registry, placement/lifecycle law, Catalog/Inventory/Session Context reconciliation, and architecture validation in CI.

Root Xcode handoff files are a P2 cleanup opportunity, not an authority risk. Leave them in place during V2 to avoid cosmetic path churn.