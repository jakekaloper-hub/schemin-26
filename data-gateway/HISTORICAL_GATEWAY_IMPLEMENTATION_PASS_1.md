# HISTORICAL GATEWAY IMPLEMENTATION — PASS 1

**Status:** STAGED IN FLA
**Date:** 2026-09-26
**Owners:** Architect + Scout + Umpire

## Implementation
Added to Fantasy League Artworks:

`scripts/chronicle/extract-pro-schemin-history.js`

FLA commit:
`e9d0549dcbc6862aca27d6d75a2c9cb5698e6c16`

## What It Does
- reuses FLA's active `espnAgent.fetchESPNFull`;
- does not mutate Supabase;
- does not generate narrative;
- preserves the fetched ESPN-layer object as an immutable JSON artifact;
- computes SHA-256 provenance;
- writes explicit fetch-failure metadata;
- validates league ID / season / team IDs / duplicate pairings / full-slate pairing counts;
- writes normalized evidence separately;
- keeps `canon_write_permitted: false`;
- leaves champion and runner-up UNRESOLVED.

## What It Explicitly Refuses
- highest-total-score final-week = championship heuristic;
- best-record = champion fallback;
- automatic Chronicle canon writes;
- silent substitution of current team names for historical names.

## Execution
From an authorized FLA runtime:

`node scripts/chronicle/extract-pro-schemin-history.js 1417621 2025 <output-dir>`

Expected evidence bundle:
- immutable `espn-1417621-2025-raw-<hash>.json`
- `PROVENANCE.json`
- `VALIDATED_EVIDENCE.json`

On fetch failure:
- `FETCH_FAILURE.json`

## Remaining QA Before Canon
1. execute against ESPN-capable environment;
2. inspect validation output;
3. independently resolve playoff bracket/final placement;
4. reconcile historical names to owner identities;
5. only then populate Schemin 2025 Fact Ledger.

## Umpire Status
Implementation path: PASS.
Live source execution: PENDING.
Historical canon unlock: NO.
