# PRO SCHEMIN' 2025 — MATERIALIZATION PLAN

**Status:** ACTIVE
**Owners:** Scout + Architect + Librarian
**Purpose:** Recover exact 2025 historical records from FLA's retained data surfaces without promoting narrative summaries to fact.

## Discovery
FLA contains a public read-only recap data path whose underlying query exposes the exact fields needed for historical reconstruction.

Source implementation:
`jakekaloper-hub/fantasy-league-artworks/api/recap.js`

For a supplied league UUID, season and week, the recap assembly reads:

### team_weekly_snapshots
- team_id
- wins
- losses
- ties
- points_for
- points_against
- standing
- opponent_team_name
- team_score
- opponent_score
- result
- narrative
- season_narrative_summary

### matchup_artworks
Also contains retained:
- winner_team_name
- loser_team_name
- winner_score
- loser_score
- point_differential

### teams
- id
- team_name
- avatar_url

### matchups
- id
- home_team_id
- category-win fields where relevant

Known historical league UUID from the 2025 audit script:
`2489cdd4-7141-45ff-bd0c-7f46c6a0baa9`

## Critical Finding
The historical records were not merely prose. FLA's architecture froze standings and matchup numbers into `team_weekly_snapshots` specifically so narratives remained consistent with referenced numbers.

Therefore the preferred recovery source is:
1. snapshot numeric fields;
2. matchups;
3. teams;
4. retained artwork score fields as corroboration;
5. narrative/storyline text only as leads.

## Extraction Contract
For weeks 1–17, materialize:
```
{
  season,
  week,
  team_id,
  historical_team_name,
  wins,
  losses,
  ties,
  points_for,
  points_against,
  standing,
  opponent_team_name,
  team_score,
  opponent_score,
  result,
  source
}
```

Then derive matchup rows only by pairing reciprocal team snapshots and verifying scores agree.

## Validation Rules
- 12 snapshot rows expected per week.
- 204 rows expected across 17 weeks.
- reciprocal opponent scores must agree.
- W/L result must agree with score comparison except any provider-specific edge cases, which are flagged.
- cumulative record cannot move backward.
- final standings cannot be inferred solely from `standing` during playoff weeks without understanding provider semantics.
- team name must be resolved from historical source, not current 2026 display name.
- playoff classification requires schedule/playoff evidence; do not infer championship solely from final-week standing.

## Current Access Boundary
GitHub source proves the extraction path and schema but does not itself expose production Supabase row contents. No service credentials will be copied into Schemin history files.

Next recovery preference:
1. retained exported historical data in repositories;
2. public FLA recap endpoint if still reachable and season-addressable;
3. canonical ESPN historical endpoint / Schemin Data Gateway;
4. commissioner-provided export only if the first three fail.

## Architect Decision
Do not build a new database or ingestion framework for this. Produce deterministic Markdown/JSON historical artifacts in `schemin-26/world/history/<season>/` after verification.

## Scout Decision
2025 reconstruction is now a data-retrieval problem, not a research-design problem.

## Librarian Decision
Alias map remains provisional until exact historical team names are materialized.

## Umpire Gate
No 2025 literary history until:
- exact rows are recovered or independently re-verified;
- owner/team alias map is locked;
- playoff path is independently validated.
