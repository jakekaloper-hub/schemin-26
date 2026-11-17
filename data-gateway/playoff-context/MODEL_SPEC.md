# Model Spec — V1.1

## Evidence and input

DESCRIPTIVE score comparisons, PROBABILISTIC forecasts, EXACT proofs and
UNRESOLVED status remain distinct. Editorial inference is downstream. This
model covers regular-season qualification and seeds, not championship odds.

The runner requires a final matchup per team in every completed week and an
unstarted fixture per team in every remaining week. It reconciles W/L/T and
PF/PA against standings; validates finite numbers, league/season/cutoff, team
identity and freshness; rejects live/final scores after the cutoff. An observed
SLOT_POINTS rule permits a provider-resolved equal score.

Provider H2H_RECORD and playoff-edit status cannot be overruled by config.
Schemin's 14-week season, seven berths, division membership and three automatic
division berths have identified canonical/approved-publication sources. The
trailing tie waterfall is conditional on ESPN's documented default.

## Scoring model

The weekly runner ignores all provider projections, including historical
projections fetched after games ended. Team mean is:

`w × (0.60 × season mean + 0.40 × last-three mean) + (1 − w) × league mean`

where `w = min(0.80, 0.35 + 0.10 × completed games)`.

Standard deviation is the larger of 12 points and observed population standard
deviation. With fewer than five scores, it is blended equally with the league
deviation. Independent Normal scores determine winners and the same PF/PA
increments. The distribution is unbounded. Injuries, lineups, roster changes,
NFL byes and opponent covariance are absent.

Default main run: 10,000 trials. Conditional branch: 2,000 trials. Every run
records seed, counts and input/rules/source hashes. Conditional win/loss runs
preserve unforced-game random streams and correctly condition the score draws.
Leverage is signed, never converted to positive through absolute value.

## Qualification

Supported modes are explicit OVERALL/POINTS_FOR and
DIVISION_WINNERS_PLUS_WILDCARDS/H2H_RECORD. Unsupported rules hold the forecast.
The ESPN mode selects and seeds division champions first. Remaining seeds use
winning percentage, then H2H only when every tied pair played equally often,
then PF, division win percentage, PA and a seeded random decision. The process
restarts after each awarded seed. The complete outcome ledger must reproduce
records. The implementation is original; official references are in seeding.py.

## Exact status and uncertainty

Strict record-point bounds, including half-wins for ties, can prove statuses
for explicit overall qualification. Division status remains UNKNOWN/UNRESOLVED.
A sampled 0%/100% is never a clinch/elimination proof. Wilson 95% intervals
measure Monte Carlo sampling variation only and retain a positive upper bound
at zero observed successes. Model and rule uncertainty are additional.

## Actual Week 10 disposition

All twelve observed ESPN seeds were reproduced from sixty final games. The
unchanged scoring model was checked on 42 past matchups in Weeks 4–10, using
strictly earlier scores. Brier loss was 0.2669438272 versus the 50/50 baseline
0.25; log loss was 0.7339592157 versus 0.6931471806. Lower is better. This sparse
same-league diagnostic establishes neither general inferiority nor external
calibration. No parameters were tuned against these 42 games.

The runner therefore keeps editorial_probability_eligible=false. Memo uses a
descriptive-field allowlist to withhold probabilities, simulated seeds/wins and
leverage. Future promotion needs improved evidence and independent acceptance;
more simulations alone do not fix model accuracy.
