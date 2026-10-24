> **Historical candidate record (October 12–13):** Preserved for provenance, not current source or release authority. Current approved character registry, visual-reference authority and October 18 lineup prevail; older source supersession and 32-page planning claims below are not reactivated. Current release status resolves through `governance/publication-manifest/PUBLICATION_MANIFEST_V1.json`.

# Week 5 — Playoff Probability and Monte Carlo Integration Contract
**Status:** SOURCE-RECOVERY COMPLETE FOR GITHUB TREE / MODEL RUNTIME NOT VERIFIED / ANALYTICS PUBLICATION HOLD.
**Authority:** Existing Week 5 Issue #146, Memo OS V5.5, League Data Gateway and existing playoff context work. Additive Memo consumer contract, NOT a new mathematics OS.

## Discovery receipts (2026-10-12)
- Inspected recursive trees of `jakekaloper-hub/schemin-26` on `main` (1,633 entries) and `week5-unified-preproduction-20261012` (1,716 entries), plus `jakekaloper-hub/bullpen` main (1,581 entries). Searches for monte/math/simulation/playoff/probability/forecast produced **no identifiable executable Monte Carlo or playoff simulator source** in those tracked trees. This does not prove none exists in another repo, private runtime, unpublished code, or connected service.
- `bullpen/runtime/intelAdapters/analytics.js` is production intelligence for writing/agent jobs and narrative coverage, **not** a fantasy playoff simulator.
- `memo-os/week-3/WEEK_3_OFFICIAL_PREPRODUCTION_PAGE_PLAN_V2_REFERENCE_LOCKED.md` contains mention of playoff odds, not executable simulation.
- `living-novel/history/PLAYOFF_ARCHAEOLOGY.md` contains verified 2022–2025 postseason history, **not** a 2026 forecast.
- Current Week 5 intake `WEEK_5_UNIFIED_PREPRODUCTION_CONTROL_BOARD_2026-10-12.md` marks outcomes PROVISIONAL and all Fact Locks blocked. Do not convert this into official standings or playoff percentages.

## Domain ownership / Bullpen execution
**Scout + Data Gateway:** confirm ESPN league 1417621 rules and 2026 12-team schedule, the 7-playoff-team qualification/seeding/tiebreak criteria, actual completed games, W-L, PF/PA, standings and matchup forecasts, remaining schedule, byes and divisions. Do not assume 7 playoff teams means seven seeded by overall record without verifying division winner rules and tie-breaks.
**Mathematics/Analytics owner via existing Bullpen registry:** identify *actual* model implementation/version, code path, simulation entry point, run configuration and evidence; do not impersonate a Director or claim a model ran without invocation receipt.
**Architect:** find and reuse the existing league probabilistic calculation system or authorized deployed service before building any fallback; avoid duplicate Monte Carlo engines.
**Beat Writer:** translate vetted probability shifts into stakes, story arcs and historically grounded commentary without confusing a model estimate for fact.
**Groundskeeper/Visual:** fit tables/cards into existing physical-page architecture without silently adding pages.
**Umpire:** challenge assumptions, reproducibility, schedule coverage, seed behavior, data freeze, and presentation confidence.

## Required forecast model contract — when existing engine is located
- All 12 teams, 14 regular-season weeks, exactly the remaining unplayed fixtures, matching official home/away schedule; six games each week (or precisely as schedule warrants); no independently generated opponents.
- Capture **season snapshot ID**, source/provider, as-of time and timezone, official game state, roster/projection timestamp, team-name/ID map, schedule hash, league-settings hash and tiebreak version.
- Monte Carlo scenarios must preserve schedule correlations; each trial produces jointly coherent league outcomes. Each team ends with wins + losses + ties = 14 (subject to league-specific exceptions), and remaining wins sum consistently across all simulated fixtures.
- Use documented, evidence-backed per-team weekly point distributions, injury/bye and opponent covariance assumptions or independently modelled game probabilities; no arbitrary constant win probabilities.
- Explicit RNG seed, reproducible run, simulation count, uncertainty bands / Monte Carlo sampling error, input/model sensitivity and seed stability. Test standings reconstruction and known deterministic scenarios before publishing.
- Apply verified ESPN playoffs qualification and seed rules, tie resolution and divisions on **every** trial, not merely after averaging results. Allocate exactly 7 berths per scenario (unless actual rules differ).
- Output (P(playoffs)), (P(first-round bye)) only if valid under 7-team bracket settings, (P(division title)), (P(top seed)), estimated win distribution and (P(championship)) only if a separate post-season matchup model is validated.
- Elimination/clinched statuses require formal mathematical proof against all permissible outcomes and tiebreaks; 0%/100% rounding alone is not proof.
- Head-to-head swing analysis, remaining-schedule difficulty, projected seed ranges, likely qualification threshold, and weekly probability **delta** require previous comparable snapshots and clear methodology.
- Historical seasons may guide priors with validated mapping, but do not manufacture league history, treat 2025 standings as 2026, or let narrative canon control math.

## Publication plan (no unapproved page-count change)
- **P003 Scoreboard:** compact league state: verified W-L, games remaining, plus highest-impact playoff leverage game **only if model certified**.
- **P028 Power Rankings:** separate *editorial ranking* from *model playoff probability*; side-by-side narrow playoff percentage chip if credible, no sorting by odds unless explicitly approved.
- **P029 State of the Realm:** primary home for all twelve team's playoff probabilities, projected seed ranges and mathematically established clinch/elimination / bubble status; optional top 5 swing movers and schedule difficulty after validation.
- **P030 Pitty's Book:** house betting odds and receipts remain **separate** from Monte Carlo probabilities. Model estimates are not sportsbook prices or picks; no conflation or fabricated implied value.
- **P032 Final Word:** narrative stakes supported by verified ranges; no claim of fate, prophecy or guaranteed berth.
- Consider a dedicated playoff race page only through the existing publication manifest change-review gate after legibility testing. Current provisional length remains 32.

## Analytics gate / controls
`MATH_ENGINE_LOCATED` → `CONFIG_VERIFIED` → `LEAGUE_SETTINGS_LOCK` → `ESPN_FACT_LOCK` → `MODEL_REPRODUCIBILITY_TEST` → `FORECAST_QA` → `DATA_EXPORT` → `PAGE_HYDRATION` → `MOBILE_QA` → `INDEPENDENT_UMPIRE`.
If any required control is missing, do not typeset numeric playoff percentages. A clearly labeled descriptive "Playoff Picture — model awaiting verification" planning note may remain internal, but never print invented probabilities in the league issue.
Data gateway receipt and model receipts are required; old or stale projections fail the freshness gate.

## No false green
As of this inspection: `MATH_ENGINE_LOCATED=UNVERIFIED`, `RUN_EXECUTED=NO`, `PLAYOFF_ODDS_GENERATED=NO`, `FORECAST_PUBLICATION_ELIGIBLE=NO`. This document authorizes source-gated integration into Week 5 Memo, not an independently certified simulation or approval.
