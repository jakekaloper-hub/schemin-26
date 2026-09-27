# SCHEMIN DATA GATEWAY — ACTIVATION FINDING

**Status:** IMPLEMENTATION SOURCE LOCATED
**Date:** 2026-09-26
**Bullpen owners:** Architect + Scout + Umpire

## Finding
The named "Schemin Data Gateway" doctrine is not present in `schemin-26` as a standalone implementation under that name.

However, Fantasy League Artworks already contains the executable primitives and, critically, a purpose-built historical backfill runner:

- `lib/agents/espnAgent.js` — active ESPN Fantasy v3 fetch/parse layer.
- `lib/agents/ingestionAgent.js` — normalization/persistence.
- `scripts/backfill/backfill-historical.js` — multi-season historical ingestion.
- FLA docs describe `espnAgent` as active and capable of league metadata, standings, matchup scores and rosters.

## Historical Runner Capability
`backfill-historical.js`:
- accepts a league DB UUID plus start/end seasons;
- calls `fetchESPNFull(platformId, season, sport)`;
- probes seasons oldest-first;
- normalizes ESPN output into teams + matchups;
- carries historical season information into league brain;
- computes season summaries;
- attempts champion detection.

This means Schemin should **adapt and harden the existing historical runner**, not invent a parallel ESPN stack.

## Critical Umpire Finding
The existing `detectChampion()` function is NOT sufficiently reliable for Chronicle canon.

It chooses the "championship game" as the **highest combined-scoring matchup in the final playoff week**. In a fantasy league with championship and consolation/placement games in the same week, highest combined score does not prove which matchup is the title game.

It also falls back to best regular-season record if playoff evidence is absent. That is acceptable for a product heuristic but NOT acceptable for historical canon.

### Ruling
- `fetchESPNFull`: approved as retrieval primitive subject to source-access success.
- normalized teams/matchups: candidate Recorded History after validation.
- `detectChampion()` output: **QUARANTINED FOR CHRONICLE USE** until bracket/final-placement semantics independently identify the title matchup.
- fallback champion-by-best-record: **PROHIBITED** for Chronicle history.

## Gateway Hardening Contract
Schemin historical retrieval wrapper must add:
1. bounded retries/backoff;
2. raw payload capture before normalization;
3. payload shape validation;
4. provenance metadata;
5. immutable source checksum/hash;
6. explicit stale/failure state;
7. team-count and schedule invariants;
8. duplicate matchup detection;
9. final-placement / playoff-bracket validation independent of score magnitude;
10. no heuristic champion fallback.

Required provenance fields:
- source
- league_id
- season
- fetched_at
- stale
- failure_reason
- raw_payload_hash
- parser_version
- source_repo_commit

## Target Invocation
Historical runner target:
- FLA league UUID: `2489cdd4-7141-45ff-bd0c-7f46c6a0baa9`
- ESPN league ID: `1417621`
- target season: `2025`

The existing runner's documented invocation shape is:
`node scripts/backfill/backfill-historical.js <leagueDbId> [startSeason] [endSeason]`

For the first controlled recovery, constrain both season bounds to 2025.

## Execution Boundary
The connected GitHub tool can inspect and modify repository code but cannot execute the repository's Node process with its local `.env.local` / Supabase credentials. Therefore activation in this chat can harden and stage the runner, but actual ESPN execution requires a runtime where the repo and its authorized environment variables are available.

## Next Engineering Deliverable
Create a Schemin-specific historical extraction mode that:
- calls FLA's retrieval primitive;
- writes immutable raw source;
- writes validated normalized JSON;
- does NOT write narrative canon automatically;
- emits an evidence report for Scout/Umpire approval.

## Board Decision
Do not rebuild ESPN ingestion.
Reuse FLA.
Remove product heuristics from historical canon decisions.
