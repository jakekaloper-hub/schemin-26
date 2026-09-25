# Schemin '26

Canonical operating repository for the 2026 Pro Schemin' Football League project.

This repository is the durable source of truth for:
- Weekly Memo OS
- Bullpen operating authority and reviews
- Jack Mercer AI GM
- Schemin Data Gateway / ESPN reliability
- Character and team canon
- Production prompts and schemas
- QA, tests, and decision records

## Start here

For substantial project work, begin with:

1. `PROJECT_CONTROL_REGISTRY.md`
2. `docs/governance/SOURCE_OF_TRUTH.md`
3. the controlling document for the subsystem being changed

The full artifact migration and known recovery items are recorded in `MIGRATION_LEDGER.md`.

## Repository relationship

`schemin-26` is intentionally separate from `fantasy-league-artworks`.

Fantasy League Artworks (FLA) remains the reusable platform / creative-engineering system.
Schemin '26 contains league-specific operating rules, data contracts, canon, workflows, and outputs.

FLA may be referenced as an upstream capability source. Schemin '26 should not silently modify FLA.

## Canonical league

- ESPN league ID: `1417621`
- Season: `2026`
- Teams: `12`
- Scoring: PPR, H2H Points
- Regular season: 14 weeks
- Playoff teams: 7

## Core systems

- `memo-os/` — V5 / V5.2-RC Weekly Memo production doctrine and gold-standard runbooks
- `data-gateway/` — ESPN acquisition, validation, fallback, snapshot, and freshness policy
- `canon/` — binding team/owner/character continuity
- `mercer/` — Jack Mercer Front Office and GM operating contract
- `bullpen/` — Schemin/FLA Bullpen reviews, orchestration, and governance evidence
- `docs/governance/` — source hierarchy and authority boundaries
- `schemas/` — machine-readable data contracts
- `tests/` — regression targets and future executable acceptance tests

## Operating rule

When ChatGPT, Jack Mercer, the Weekly Memo OS, or Bullpen performs work for Schemin '26:

1. Read the relevant repository contract.
2. Prefer verified league data over remembered state.
3. Preserve character/team canon.
4. Record material operating changes in version control.
5. Do not overwrite a gold-standard artifact without an explicit revision path.
6. Never present stale data as live.
7. Do not treat file existence as release certification.
