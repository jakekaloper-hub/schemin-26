# 2025 RECOVERY PASS 3 — SOURCE ACCESS RULING

**Status:** ACTIVE
**Date:** 2026-09-26
**Owners:** Scout + Architect + Umpire

## Objective
Recover exact 2025 sporting records after repository archaeology established the historical corpus but did not expose a clean 204-row export.

## Repository Findings
FLA preserves:
- league UUID `2489cdd4-7141-45ff-bd0c-7f46c6a0baa9`;
- ESPN league ID `1417621`;
- season 2025;
- 17-week corpus;
- 204 team-week snapshot existence;
- 12 historical team-name leads;
- canonical weekly-run metadata;
- the exact database schema/fields required for reconstruction.

It does NOT currently expose a clean committed 204-row numerical snapshot export.

## External Endpoint Verification
Current public technical documentation independently confirms ESPN Fantasy's active read host and relevant views:
- `lm-api-reads.fantasy.espn.com`
- modern 2018+ season path under `/apis/v3/games/ffl/seasons/{season}/segments/0/leagues/{leagueId}`
- `mSchedule` for full-season schedule
- `mStandings` for records/points/final ranks
- `mTeam` for team identity
- `mMatchupScore` / scoreboard views for scores.

Important restriction documented by current community verification: historical-season access may require authenticated ESPN cookies even for leagues that were once publicly readable.

## Bullpen Ruling
Do not scrape random search-index fragments for sporting facts.

The clean recovery target is the canonical ESPN/Data Gateway payload using:
- league: 1417621
- season: 2025
- views: mTeam, mSchedule, mStandings, with matchup score corroboration as needed.

If the historical endpoint returns an authentication barrier in the available runtime, mark ACCESS BLOCKED rather than infer values.

## Data Contract for Accepted 2025 Recovery
A recovered payload must permit:
1. exactly 12 league teams;
2. stable ESPN team IDs;
3. historical display names;
4. full schedule/matchup periods;
5. six unique pairings per standard 12-team H2H week;
6. scores for completed matchups;
7. regular-season records/points;
8. playoff schedule/path;
9. final placement evidence.

## Cross-checks
- historical ESPN team names vs FLA 12-team lead list;
- ESPN matchup scores vs any retained FLA numeric fields;
- championship/playoff outcome vs project-held 2025 podium leads;
- owner mapping vs Character Master;
- rename chronology vs 2026 current names.

## Failure Policy
If direct historical ESPN access is unavailable:
- retain all recovered repository evidence;
- record exact missing source;
- do not unlock Beat Writer;
- next authorized route is an authenticated Data Gateway/commissioner export, not invented reconstruction.

## Current Gate
**SPORTING FACT MATERIALIZATION: OPEN / NOT YET PASSED**
**BEAT WRITER: LOCKED**
