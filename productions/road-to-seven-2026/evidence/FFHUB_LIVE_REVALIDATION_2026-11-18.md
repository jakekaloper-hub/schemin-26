# FFHub revalidation — The Road to Seven (November 18, 2026)

**Status:** FRESH UI RUN EXECUTED, SOURCE-SAMPLED / NOT EXACT PLAYOFF PROOF. Recovered original November 17 historical evidence remains preserved separately. Both snapshots are **final through Week 10, entering Week 11** for ESPN league **1417621**.

## Live execution receipt

- Site: https://theffhub.com/PlayoffTool?site=espn&leagueId=1417621&userId=&s2=&swid=
- Capture: 2026-11-18T16:45:12.354Z through 2026-11-18T16:46:53.445Z UTC.
- ESPN selector: ESPN. Playoff tiebreaker selector: **Head to Head**.
- Source engine: **10,000 Monte Carlo samples per displayed run** using season scoring averages and standard deviations, not player projections or NFL byes.
- Browser: isolated single-page headless Chrome session on authorized Mac; browser closed after all runs, no persistent tab growth.
- Executed: **one saved baseline, twelve single-game Week 11 scenario runs (both winners for each of six matchups), and four four-game win-out scenario runs**. Total 17 captured tables. Site-provided results, **not** fabricated or analytically reconstructed odds.
- Capture method: clicked actual named winner buttons, verified success-state selection, recorded all twelve rows of the resulting seed-probability table. Reloaded page between separate games/sweeps to avoid prior selections.
- Snapshot stored privately on the authorized Mac; raw JSON is **not** placed into this repository. Private raw hashes: Week 11 `a7d946da605859df92c8008ade74f24947345367973f73482787edaa8fca1b1b`, sweeps `2b8d6f98aa0f9db4ed3461bc6075c2674a37e084d279c314b9c4020e92423f30`.
- Machine audit: `PASS`, with 0 reported errors; all 12 single-game runs retained 12 teams and exactly seven playoff-berth probability mass.

## All twelve team POVs — official Week 10 seed order

Each `Win W11` value conditions on that team's victory in Week 11, and `Lose W11` conditions on its defeat. All other unselected future games remain simulated. Differences are approximate due to new random draws. November 17 differences in last column are *sampling drift*, not evidence of a real change in standings.

| Official seed | Team | Fresh baseline | Win W11 | Lose W11 | Conditional swing | Change from Nov 17 baseline |
|---:|---|---:|---:|---:|---:|---:|
| 1 | Slob on my Dobb | 98.48% | 99.74% | 95.89% | 3.85 pp | -0.17 pp |
| 2 | El Niño | 87.10% | 96.88% | 83.92% | 12.96 pp | -0.12 pp |
| 3 | D0nkey K0ng | 93.31% | 98.66% | 88.55% | 10.11 pp | +0.43 pp |
| 4 | His Majesty's Blood | 87.62% | 95.17% | 80.10% | 15.07 pp | -0.44 pp |
| 5 | Dr. Duckhook | 87.55% | 96.40% | 78.90% | 17.50 pp | +0.35 pp |
| 6 | Seven Deadly Chins | 82.16% | 88.24% | 61.25% | 26.99 pp | +0.88 pp |
| 7 | Red Leopards | 50.14% | 64.81% | 27.21% | 37.60 pp | -0.21 pp |
| 8 | The Chili Cheesers | 38.16% | 58.81% | 20.68% | 38.13 pp | +0.06 pp |
| 9 | The LLC | 33.41% | 51.78% | 15.61% | 36.17 pp | -0.21 pp |
| 10 | ObiWan Jacoby | 32.45% | 52.89% | 12.77% | 40.12 pp | -0.27 pp |
| 11 | Three Dreaded Snake | 9.61% | 22.76% | 2.36% | 20.40 pp | -0.30 pp |
| 12 | Mud Dogs | 0.01% | 0.07% | 0.00% | 0.07 pp | +0.00 pp |

**Largest outcome dependencies:** ObiWan 40.12 pp; Chili 38.13 pp; Red 37.60 pp; The LLC 36.17 pp. These are high-leverage story beats, not exact clinch tests.

## Four fixed win-out experiments

| Fixed team | Fresh FFHub estimated berth chance | Scenario |
|---|---:|---|
| ObiWan Jacoby | 99.76% | 4 consecutive selected victories |
| Three Dreaded Snake | 99.28% | 4 consecutive selected victories |
| The LLC | 100.00% | 4 consecutive selected victories |
| Mud Dogs | 4.77% | 4 consecutive selected victories |

**Scope caveats:** Even a displayed 100.00% for The LLC is only 10,000 simulated successes, NOT a guaranteed 8–6 berth. Mud Dogs may show 0.00% in a Monte Carlo run but has mathematically constructed survival paths from the November 17 exact evidence. Mud's Week 11 loss-elimination statement rests on independent rules arithmetic, not 0% simulation.

## Folio implication (no creative rewrite required)

- **RT7-P02**: Slob vs El Niño and two strong contenders, neither guaranteed.
- **RT7-P03**: DK vs HMB direct crossover; DK's later divisional qualification route remains important.
- **RT7-P04**: Dr. Duckhook faces LLC; Seven Deadly Chins can mathematically eliminate Mud with a win.
- **RT7-P05**: Red #7 vs Chili #8 — the qualification cutline, now with measured 37.60 / 38.13 pp outcome spreads.
- **RT7-P06**: LLC vs ObiWan #9/#10, both high conditional Week 11 leverage. Their separate win-out estimates remain near certainty *within the vendor sample*, but exact proof is not equivalent.
- **RT7-P07**: Snake's outsider path and Mud's four-required-win route. Mud's conditional 0.00% does not itself prove elimination.

## What this checks and what it cannot

**Verified by execution:** FFHub live site loaded league 1417621, six Week 11 matchups and four divisional final weeks; 16 hypothetical UI scenarios were run and recorded; the outputs align with the November 17 underlying league state and directionally with prior runs.

**Not independently established:** vendor probability calibration, exhaustive future-score model accuracy, an unchanged JSON implementation, or an independent BulIpen Umpire/visual sign-off. Protected legacy source and exact mathematical witnesses remain separate evidence classes.

The original standalone edition is still seven PNGs and is not retroactively modified by a new stochastic sample. Use the dated value with clear attribution if selected for publication.
