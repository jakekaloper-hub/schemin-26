# Schemin '26 — Subsystem Temporal & Lineage Contract V1

**Document class:** control
**Authority / owner:** Librarian + Memo OS + Novel OS + Jack Mercer
**Version:** 1.0
**Status:** ACTIVE — PR #15
**Effective date:** 2026-09-28

## Problem

Schemin '26 contains valuable historical state. Historical state becomes contamination when retrieval cannot distinguish it from current state.

A file is not current because:
- it is easy to find;
- it says FINAL;
- it was once approved;
- it contains the latest data that existed when written.

## Universal mutable-state header

Any new or materially revised artifact containing mutable league, roster, production, manuscript, or decision state should expose:

- **Temporal scope / as-of:** exact week/date/season or historical range;
- **Authority:** subsystem/source that controls the facts;
- **State class:** CURRENT / HISTORICAL / CANDIDATE / SUPERSEDED / PRE_FACT / FACT_LOCKED;
- **Supersession:** newer parent/child or replacement where known;
- **Freshness rule:** for current league state, use Data Gateway metadata rather than document age alone.

## Memo OS

Authority chain remains `memo-os/_INDEX.md`.

Rules:
- OS patches are version lineage, not weekly state.
- Week folders are time-bounded production records.
- PRE_FACT evidence remains historical after Fact Lock; it must never be read as final result state.
- Live snapshots are chronological receipts, not perpetual current state.
- Published artifacts must be distinguished from production candidates/tests.

## Novel / Chronicles

Manuscript lineage:
`V1 → V2_AUDITED → V3_REBUILD → V4_CONSULTANT_REVISION`.

V4 is current production parent unless explicitly superseded.

Earlier manuscripts are valuable historical lineage and should remain recoverable, but no current production brief may silently source prose from V1–V3 when V4 governs.

Proof-of-concept production directives should be treated as dated execution records unless a current manifest explicitly imports them.

## Jack Mercer

Mercer decisions are temporal by definition.

A recommendation must distinguish:
- league-state timestamp / matchup period;
- roster state used;
- injury/news evidence time where relevant;
- keeper/pick ledger version;
- decision timestamp.

Past recommendations belong in the Decision Journal as historical decisions, not current instructions.

No roster, trade, waiver, lineup, or opponent file may be treated as current solely because it lives under `mercer/`.

## Historical league/world material

Historical facts retain their original season/date and evidence class.

TO VERIFY / partially verified historical mappings must never be promoted into current identity or owner continuity.

## Retrieval rule

When a request contains "current", "today", "now", "this week", "live", or a current decision:
1. resolve current Data Gateway / provider state;
2. load current subsystem authority;
3. use dated historical artifacts only as context;
4. state freshness where material.

When a request is historical:
1. allow archive/history retrieval;
2. preserve the original evidence classification;
3. do not back-project current ownership, names, or canon into older periods without proof.
