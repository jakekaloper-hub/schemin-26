# G1H — Historical Depth Layer, 2015–2026: Drafts, Expectations, Roster Evolution and Character Arcs

**Status:** SOURCE RETRIEVAL IN PROGRESS / AUTHOR ROOM DESIGN; graft onto existing historical Chronicle, Author Context, Flaim adapter, Novel OS, Universe OS. NOT a new operating system, a set of retrospective invented owner psychologies, or a verified trade ledger.

## New source proof obtained live
- `evidence/G01_2015_2026_DRAFT_HISTORY_PROVIDER_PICKS.json`: exact provider-placed selections for all 12 years. Pick totals 2015–2023 204/year, 2024 203, 2025 202, 2026 204 (total 2,445). Keeper flags returned 2022–2026, not 2015–2021. Zero keeper flags does not imply zero manually designated keepers if provider omitted them.
- `evidence/G01_2022_RED_WEEKLY_ROSTER_SNAPSHOTS.json`: 2022 Red team slot 2, Weeks 1/4/8/14/16 roster snapshots, 17/17/17/19/19 players. Distinct snapshots allow acquisition/departure *observations* only; league transaction endpoint explicitly reports `ESPN_SEASON_NOT_SUPPORTED` for 2022. Do not label differences as trades or waiver claims.
- Historical weekly matchup evidence 2015–2025 already present; 2026 current only up to actual evidence cutoff. Historical team slot lineage is not proven private owner continuity.

## Evidence vs model vs fiction
| Desired depth | Reliable source | Derivation allowed | Must NOT claim |
|---|---|---|---|
| Draft board, round/position, keeper | Flaim ESPN pick metadata, historical selections | Team draft capital distribution, keeper-round exposure, source pick grade | 'ESPN gave Grade A' unless real report retrieved |
| Preseason expectations | Preseason forecasts/projections if timestamped archive recoverable | EX ANTE model with ONLY draft/preseason metadata available before W1 | Using season-end champion as preseason expectation |
| Draft grade | Picks, draft capital, contemporary player projections/ADP *only if recoverable at vintage cutoff* | Named formula and dated benchmark; otherwise **composition profile**, not performance grade | Invented industry rank/ADP or hindsight grade mislabeled as ex ante |
| In-season roster identity | Historical week roster snapshots and known draft player IDs | Roster delta with prior/next presence, starters/bench, rising/falling roles | A trade, waiver, injury, or reason inferred from change alone |
| Trades, adds/drops, keeper deals | 2026 structured transactions when within supported provider window; historical independent receipts if located | Proposed narrative pressure / UNKNOWN provenance | Fabricated historical trade participants, offer, price or dates |
| Weekly rivalry | Actual historic matchups/results, standings by season, rank | Trajectory and pressure arcs; reader knows final outcome, characters only as-of-week events | A prediction or thought as owner fact |
| Universe reaction | Approved Atlas World Memory, event source, existing history | Period-tagged creative proposals for civic economy and character arcs | Retroactive 2026 physical map/appearance |
| Narrative scripts | Character/Novel OS, period-safe source and manuscript | Creative scenes, dialogue, point-of-view constraints | Unapproved manuscripts treated as hard canon |

## Proposed historical Depth Packet per season and per team
`season, evidence_cutoff_week, historical_team_id, historical_team_name, owner_identity_status, draft_picks[], keeper_flags[], draft_profile, preseason_model_status, provenance_cutoff, expected_rank_confidence, known_weekly_matchups[], records_as_of_week, roster_snapshots[], roster_deltas[], transaction_attribution_unknown, independent_story_pressure, competing_character_knowledge, period_world_state, manuscript_refs, open_loops, source_sha, fictionalization_status`.

Two linked uses: (a) a complete **2015–2026 Author Room season writers' dossier** that tracks all twelve historical team slots with an overarching season arc; (b) an **as-of-scene character packet** limiting knowledge to earlier evidence and verified owner attribution. The 2026 novel is current-time culmination, not proof that the same characters participated in earlier periods.

## Draft grade methodology (must not fake certainty)
1. Freeze evidence at **draft completion / before Week 1**.
2. Resolve each selected `playerId`, overall pick and `isKeeper`; ensure 12-team draft order and keeper pick count have no unexplained gaps.
3. If vintage ADP/projections are available with source timestamps preceding draft: derive `value_over_consensus = consensus_expected_pick - actual_pick`, calibrate replacement-level value, keeper opportunity cost and positional balance. Rank all 12 historical teams on repeatable index and print model provenance.
4. If vintage ADP/projections absent: **do not issue A–F performance grades**; output descriptive roster composition, keeper concentration, role/position coverage. A hindsight efficiency grade is a separately named retrospective outcome, never preseason expectation.
5. Draft retrospectives may compare projected vs actual points after the season ends, but label them **POSTSEASON RETROSPECTIVE**, exclude from in-time scenes and author preseason knowledge.
6. A team with missing historical draft selections is `INCOMPLETE_PROVIDER_DRAFT`; never repair a 2024 203-pick board into 204 fictitious picks.

## Roster story mechanics
- Collect bounded historical `get_roster(year, team_id, week)` snapshots across each season. Store player IDs, lineup slots, visibility timestamp/period, provider limitations.
- `appeared = ids_at_week_b - ids_at_week_a`; `departed = ids_at_week_a - ids_at_week_b`; `role_changed = same_id and lineupSlot changed`.
- Label `OBSERVED_ROSTER_DELTA`, never `CONFIRMED_TRADE`; missing intermediate weeks and IR/bench/status mechanics are confounders.
- Link confirmed same-week score impact if provider points are available; historical roster player stats may contain season totals and **must not be misrepresented as week points**.
- For 2026 supported transactions, use exact official transaction events where available and respect limit/count/window completeness constraints.

## Twelve-season novel application
**Preseason:** draft and keeper choices establish each historical team's *available assets*, expectations only through genuinely dated contemporaneous projections or clearly proposed fictional reputations.
**Weeks 1–regular season:** matchups + current-as-of-week roster shape drive turning points; plot response must not see later victories.
**Mid-season:** roster entry/exit is a mystery of changed resources, not evidence of a trade. Compose character-driven hypotheses but never call a particular acquisition certified.
**Playoffs:** score/bracket results determine transitions, not earlier knowledge.
**Aftermath and forward inheritance:** World Memory may preserve social meanings and artifacts only once approved; a current owner can encounter recovered records of historical teams without inventing firsthand 2015–2025 ownership.

## Gate ownership and implement-now tasks
- **Scout/Flaim:** full historical draft archive and season/week standings/roster snapshots, zero inferred transaction labels, provenance/availability receipts.
- **Architect/Librarian:** immutable source depth joins in the existing read-only Author Context service, tests for cutoff and source constraints.
- **ConsultEngine + Beat Writer:** propose season-wide pre/during/post narrative structure, positive and negative arcs for all historical participants, separate supported evidence from invented motives.
- **Universe/Atlas:** contextualize historical consequences by period-specific site state, reject modern-world backfill.
- **Umpire:** independent source and semantic checks; block A–F grades and claimed trades without evidence.

**Current acceptance:** Source draft selection retrieval for 12 years and one 2022 five-snapshot proof COMMITTED. Whole-league historical rosters, historical dated ADP/preseason forecasts, reliable trades before 2026, model grade calibration, actual authenticated Bullpen memory joins, and independent Umpire PASS are **NOT COMPLETED**.
