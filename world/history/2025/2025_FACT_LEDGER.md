# PRO SCHEMIN' — 2025 FACT LEDGER

**Status:** ACTIVE / RECONSTRUCTION PASS 1
**League:** ESPN 1417621
**Season:** 2025
**Owners:** Scout (facts) + Librarian (identity/provenance)
**Narrative access:** PARTIAL — 2025 final podium directly verified; other historical events remain gated

## Evidence Classes
- **A — Direct record:** exact fact is present in an authoritative retrieved artifact/data row.
- **B — Dataset existence verified:** source proves underlying records exist, but this ledger has not yet materialized the exact row/value.
- **C — Corroborated secondary:** supported by multiple retained historical sources but not yet underlying record.
- **D — Unverified lead:** useful retrieval target only; cannot enter Chronicle history.

## Source Registry

### S1 — FLA 2025 Post-Season Audit
Repo: `jakekaloper-hub/fantasy-league-artworks`
Path: `docs/ops/handoffs/PRO_SCHEMIN_SEASON_AUDIT_2025.md`
Authority: historical Bullpen audit generated 2026-04-26.

Directly establishes:
- Pro Schemin' / ESPN 1417621.
- season 2025.
- 17 weeks including regular season + playoffs.
- 12 teams.
- 204/204 team-week snapshots existed.
- 126 league storylines existed across 10 types; 22 labeled legendary by the old system.
- 17 weekly narratives existed.
- old narrative system identified arc candidates around The Immortal, Baker Moore Purdy and The LLC.

**Constraint:** automated storyline labels and old narrative rhetoric are NOT factual canon.

### S2 — Audit generation script
Repo: `jakekaloper-hub/fantasy-league-artworks`
Path: `scripts/postSeasonAudit.js`

Directly establishes:
- internal league UUID `2489cdd4-7141-45ff-bd0c-7f46c6a0baa9`.
- `SEASON = 2025`.
- source database tables queried included `weekly_deliverables`, `matchup_artworks`, `league_storylines`, `team_weekly_snapshots`, `agent_jobs`, `weekly_runs`.
- snapshot query in the audit was COUNT-ONLY.

**Critical implication:** S1's 204-snapshot count proves dataset completeness at audit time, but does not expose individual team-week facts in the retained Markdown.

### S3 — Connected ESPN historical standings (2026-10-10 verification)
Provider: authenticated Flaim Fantasy connector, `get_league_info` and `get_standings` for ESPN football league `1417621`, season `2025`.
Returned: `seasonPhase=season_complete`, `seasonComplete=true`; `outcomeConfidence=explicit` for the verified podium.
- `The Immortal`: `finalRank=1`, `championshipWon=true`, `playoffOutcome=champion`.
- `ObiWan Jacoby`: `finalRank=2`, `playoffOutcome=runner_up`.
- `Three Dreaded Snake`: `finalRank=3`, `playoffOutcome=eliminated`, `outcomeConfidence=explicit`.
**Caution:** regular-season `rank` is NOT the postseason `finalRank`. This source does not directly verify semifinal scores, owner aliases, prior-year events, or keeper costs. Tool execution provenance is documented in the PR #130 V4R2 Atlas/historical source matrix and Bullpen #117.

## Pass-1 Locked Facts

| Fact | Class | Source | Chronicle eligibility |
|---|---|---|---|
| League is Pro Schemin', ESPN 1417621 | A | S1/S2 | yes |
| 2025 first: The Immortal; second: ObiWan Jacoby; third: Three Dreaded Snake | A | S3 explicit finalRank fields | yes, podium order only |
| 2025 season represented 12 teams | A | S1/S2 | yes |
| 17 weeks represented regular season + playoffs | A | S1/S2 | yes |
| 204 team-week snapshots existed | A for existence / B for contents | S1/S2 | existence only |
| 126 machine-detected storylines existed | A | S1 | metadata only |
| 22 storylines were labeled 'legendary' by old engine | A | S1 | label is not historical truth |
| Full weekly narrative coverage existed | A | S1 | provenance only |
| The Immortal had an '8-game arc' in old narrative analysis | D as sporting fact | S1 | NO until underlying events recovered |
| Baker Moore Purdy had a 'luck variance' arc | D as sporting fact | S1 | NO |
| The LLC had a 'snake-bite' narrative | D as sporting fact | S1 | NO |

## Required Materialization
Before 2025 can become Chronicle history, recover or independently verify:
1. 12 historical team identities and owners.
2. week-by-week matchup scores.
3. regular-season standings.
4. playoff bracket and results.
5. champion / runner-up / third. **CLOSED for 2025 via S3.**
6. scoring highs/lows.
7. streaks.
8. significant transactions/trades if retained.
9. historical team-name changes within/between seasons.
10. exact events behind any old storyline selected for reuse.

## Known High-Value Leads — NOT YET LOCKED
2025 podium is now directly sourced from S3 and promoted above. Semifinal details, owner alias mappings, and other historical leads remain unverified by S3. Scout must recover supporting evidence rather than copying remembered values into the historical record.

## Scout Ruling
2025 is **partially fact-materialized**. Postseason podium outcomes are source-locked through S3. Detailed historical fiction beyond the podium remains blocked pending underlying event evidence.

## Librarian Ruling
Do not back-project 2026 team names into 2025. Historical aliases must be resolved season-specifically before manuscript use.

## Beat Writer Gate
CLOSED.

The Beat Writer may use the S3-verified podium in appropriate preseason framing. Detailed canonical 2025 historical scenes beyond those outcomes still require Scout + Librarian event packets.
