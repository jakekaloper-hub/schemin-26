# Repository Architecture

## Purpose

Schemin '26 is the league-specific control plane. FLA is an upstream platform and creative capability source.

## Top-level domains

### `bullpen/`
Cross-functional review authority, board-meeting outputs, audits, escalation rules, and project-wide decisions.

### `memo-os/`
Weekly Memo production system: intake, pre-production, data freeze, writing, art direction, page production, QA, final assembly, and postmortems.

### `mercer/`
Jack Mercer AI GM: roster analysis, trades, waivers, lineup decisions, opponent scouting, keeper/draft-pick economics, and decision journal.

### `data-gateway/`
ESPN ingestion contracts, retries/backoff, validation, last-known-good snapshots, mirror fallback, and freshness metadata.

### `canon/`
Authoritative team names, owner identities, character continuity, rename mapping, visual constraints, and league constants.

### `prompts/`
Versioned production and initiation prompts. Prompts are treated as executable operating assets.

### `schemas/`
Machine-readable contracts for league state, freshness metadata, memo inputs, character canon, and decisions.

### `tests/`
Golden-path, regression, data-contract, and canon-validation tests.

### `docs/`
Architecture decisions, governance, runbooks, and operating manuals.

## Change doctrine

- League-specific changes belong here.
- Reusable platform changes belong in FLA.
- Cross-repo changes should be documented before implementation.
- Breaking changes require a migration note.
