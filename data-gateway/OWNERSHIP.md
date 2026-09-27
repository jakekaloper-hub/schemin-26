# SCHEMIN '26 — DATA GATEWAY OWNERSHIP

**Status:** BINDING
**Effective:** 2026-09-26

## Repository Boundary
`jakekaloper-hub/schemin-26` is the authoritative home for all Schemin '26 project-specific:
- historical ESPN extraction;
- Chronicle evidence contracts;
- provenance and validation;
- historical fact ledgers;
- canon admission;
- continuity;
- Week 3+ Chronicle production.

`jakekaloper-hub/fantasy-league-artworks` is an upstream/reference implementation only. Schemin may reuse architectural patterns or connect through an adapter, but Schemin-specific production logic must live here.

## Authoritative Extractor
`data-gateway/chronicle/extract-pro-schemin-history.js`

The extractor is adapter-driven so Schemin does not require its core Chronicle evidence logic to live inside FLA.

Adapter contract:
`fetchHistoricalLeague(leagueId, season) -> { leagueData, teams, rawMatchups }`

## Migration Ruling
The previously added FLA file:
`scripts/chronicle/extract-pro-schemin-history.js`
is **NON-AUTHORITATIVE / SUPERSEDED** for the Schemin '26 project.

Its commit remains repository history, but future Bullpen instructions must not treat that path as the Schemin implementation source.

## Dependency Rule
Schemin may:
- consume FLA's ESPN adapter;
- copy/reimplement stable generic parsing contracts when appropriate;
- use FLA as evidence/reference.

Schemin must not:
- require Chronicle governance to be stored in FLA;
- let FLA narrative heuristics determine Schemin canon;
- make FLA the source of truth for Schemin-specific history or character continuity.

## Bullpen Routing
For this project, default write target is `jakekaloper-hub/schemin-26`.

Writing to another repo requires one of:
1. explicit Jake instruction;
2. a generic upstream fix that properly belongs to that repo;
3. an integration change required at the upstream boundary.

Even then, Schemin-specific authority remains here.

## Umpire Rule
If duplicate implementations exist, the `schemin-26` implementation wins for this project unless Jake explicitly changes repository ownership.
