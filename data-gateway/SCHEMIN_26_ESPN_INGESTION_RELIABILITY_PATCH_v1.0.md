# SCHEMIN '26 — ESPN INGESTION RELIABILITY PATCH v1.0

## Incident

The agent environment could parse an uploaded ESPN league export but could not reliably resolve ESPN's Fantasy read hostname. The failure mode was dangerous because a valid historical snapshot could be mistaken for current league state.

## Root-cause classification

This is **not** a league-ID/parser failure. It is an execution-surface transport failure. ESPN's current read API remains the `lm-api-reads.fantasy.espn.com` v3 host, but an agent/tool runtime may fail DNS, outbound policy, CORS, or upstream availability independently of ESPN itself.

## Reliability design

### Data Acquisition Agent
Owns endpoint construction, timeouts, retries, rate limiting, primary/mirror routing, and response parsing.

### Contract & QA Agent
Rejects malformed/wrong-league payloads before promotion. Current hard contracts: league 1417621, season 2026, 12 teams, 17 roster entries/team, core schedule/settings/status objects.

### Snapshot Custodian
Atomically persists only validated payloads, maintains `latest.json` and provenance metadata, and never lets a failed refresh overwrite last-known-good state.

### Freshness Sentinel
Computes snapshot age and degradation state. It prevents Mercer/Memo OS from calling cached data “live.”

### Recovery Agent
Routes direct ESPN → edge mirror → GitHub cold standby → local last-good snapshot. Escalates only when no validated snapshot exists or freshness exceeds the consuming workflow's SLO.

## Operational states

- **GREEN / LIVE:** direct or mirror refresh validated; `stale=false`.
- **YELLOW / DEGRADED:** network refresh failed; validated snapshot served; `stale=true` and age disclosed.
- **RED / UNAVAILABLE:** no validated current or cached snapshot exists.
- **RED / CONTRACT BREAK:** upstream returned JSON but schema/league contracts failed; retain prior snapshot and alert.

## Required downstream change

Mercer, Weekly Memo OS, Front Office, Trade Center, roster news, opponent scouting, and any future subagent must consume the gateway envelope and propagate freshness metadata. They must never infer freshness merely because data exists.

## Source-informed decisions

Research across current public ESPN-fantasy projects supports the current `lm-api-reads` host, multi-view reads, public-league anonymous access, retries on transient HTTP errors, persistent snapshots, and scheduled refresh/caching. We intentionally combine those patterns rather than depending on any one wrapper library.