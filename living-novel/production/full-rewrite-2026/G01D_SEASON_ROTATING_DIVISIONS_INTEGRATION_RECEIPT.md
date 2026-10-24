# G1D — Rotating Historical Divisions, 2015–2026
**Founder ruling:** Team division placements change from season to season. No division assignment persists by assumption. League divisions are identity/jurisdiction overlays, not immutable geographic borders or species maps.

## Investigation (2026-10-17)
- Connected Flaim `get_league_info(league=1417621, season=2022)` exposed basic team IDs/names but **did not expose historical division IDs** in its normalized team records; no verified 2022 division map was recovered through this call.
- `world/data/divisions.json` explicitly scopes membership as `season: 2026` and `member_team_ids_2026`. Burgers/Wings/Pizza geographic culture may persist, but **2026 team membership must not be backdated**.
- `world/divisions/DIVISION_INDEX_SCHEMA_V1.md` already requires “member owners/teams by season.” This is a missing data-binding operation, not grounds to create another division OS.

## Actual code changes
- New read-only `living-novel/os/adapters/season_division_reader.py` returns 2026 source-bound placements but `UNKNOWN_HISTORICAL_DIVISIONS` for 2015–2025 until explicit season-specific evidence is provided; can accept verified period team-to-division references and rejects year mismatch/duplicates.
- New `living-novel/os/qa/test_season_division_reader.py`: five test cases for 2026 map, anti-backdating for eleven years, independent past map acceptance, and invalid evidence controls.
- Executed on isolated Mac checkout: **29 tests passed** (previous 24 plus five); actual resolver readout showed 2015–2025 each UNKNOWN, 2026 all 12 source-bound.

## Season packet integration mandate
Each historical team entry should include `season`, `historical_team_id`, `division_id` (nullable), `division_evidence_source`, `membership_status`, `division_rivalries_as_of_week`. The novel's 2022 season packet should use UNKNOWN division without filling Burgers/Wings/Pizza from current JSON. A division change from season A to B may establish *documented* political/social repositioning in fiction only if both memberships have independent evidence and proposed World Evolution treatment.

## Scout next priority
Retrieve per-season division membership from ESPN native year-specific league settings/team metadata if available, archived FLA raw payloads, existing historic league files, league commissioners' records, or verified interviews; do not estimate membership from a streak of divisional matchups alone (schedule inference is suggestive, not certified). Record `source_year`, `source_sha`, `team_ids`, `division_ids`, names/aliases, and membership completeness. Require all 12 assignments or explicit UNKNOWN slots. Repeat for all 2015–2026 seasons.

## World/Author Room constraints
Historical divisional warfare, home-field, cultural identities and road crossings must reference **period membership**; persistent physical locations need not move merely because team affiliations rotate. Ensure changes in heraldry, customs, alliances and access privileges are intentional author proposals, not mistaken retroactive World State facts.

**Gate verdict:** Historical division time-leak prevention code and five tests PASS; actual 2015–2025 division membership reconstruction remains OPEN. No independent Umpire or publication release.
