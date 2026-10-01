# Repository Architecture V2 Mission Freeze

**Mission:** Schemin '26 Repository Architecture V2 & Placement Governance
**Lead:** The Librarian
**Counterweights:** The Architect, Groundskeeper, Umpire, Closer
**Frozen main:** `d2912d0bff0ecafe1bf0f3bc7717965565b74741`
**Tree:** `9aa8821b441787d10bbb4ca05d08477259a9292d`
**Date:** 2026-10-01

## Scope freeze

This mission begins from the merged Execution Control V1 state. No mass folder migration is authorized.

Initial inventory:
- 1,177 files
- 299 directories
- 1,476 recursive tree entries

Largest domains by file count:
- Living Novel: 274
- World: 261
- Chronicles: 173
- Canon: 155
- Memo OS: 137

## Initial risk findings

1. `docs/architecture/REPOSITORY_ARCHITECTURE.md` materially lags the current repository.
2. `world/` and `chronicles/` have no root human entry point.
3. `governance/` vs `docs/governance/` needs a formal executable-vs-doctrine boundary.
4. `living-novel/`, `chronicles/`, and `productions/` need explicit lifecycle/ownership boundaries.
5. `planning/` contains active execution programs and needs a graduation law.
6. several support domains lack a root navigation contract.
7. `prompts/` is a real first-class top-level domain and must be governed explicitly.

No file move is justified solely by these findings. Placement law and enforcement come first.