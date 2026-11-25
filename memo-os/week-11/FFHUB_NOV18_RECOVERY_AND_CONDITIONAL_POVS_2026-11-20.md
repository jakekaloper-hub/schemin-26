# Week 11 — November 18 TheFFHub source recovery and conditional playoff intelligence

**Recovery date:** November 20, 2026 (authorized Mac, existing Road-to-Seven research folder).  
**Original capture:** 2026-11-18T16:45:12.354Z through 2026-11-18T17:05:07.191Z.  
**League:** ESPN `1417621`; season 2026; final input through **Week 10**.  
**Actual capture source:** `https://theffhub.com/PlayoffTool?site=espn&leagueId=1417621&userId=&s2=&swid=`; captured from visible UI in a headless Chromium session, **not authenticated original vendor backend HTTP bytes**.  
**Source preservation:** existing **private** Bullpen [PR #158](https://github.com/jakekaloper-hub/bullpen/pull/158), commit `eca8e1659073255c7f89f6fbf11639e3e28a5d18`, path `projects/schemin-26/evidence/week-11-20261118/`. Private raw originals, SHA-256 manifest, 12-team equality check and all intermediate scenarios are retained for source/Analyst/Umpire review.  
**Status:** `LOCAL_CAPTURE_RECOVERED / BYTE_MANIFEST_VERIFIED / 12_OF_12_SCENARIO_PARITY_PASS / VENDOR_CALIBRATION_NOT_PROVEN / INDEPENDENT_UMPIRE_PENDING`.

## Actual evidence and tests
- `ffhub-summary.json`: original 12-team summary, six Week 11 fixtures, complete four-win-out scenarios, `validation.pass=true`.
- `ffhub-w11-12-live-scenarios.json`: 12 named conditional Week 11 runs, 10,000 simulations per run, selected `Head to Head` tiebreaker, empty capture-errors array.
- `ffhub-4-winout-scenarios.json`: four win-out probes.
- `ffhub-week12-14-future-forks.json` plus `ffhub-week12-14-future-summary.json`: 10 selected division-fork experiments from remaining weeks.
- Validation performed against original local raw bytes: **12/12 teams' baseline, Week 11 victory and Week 11 defeat percentages agree exactly between summary and named raw runs**; matching league ID `1417621`, through Week `10`, 10,000 simulations. No recorded live capture errors. All 5 exact full SHA256 hashes are in protected Bullpen source manifest.

## Dated Week 11 baseline and hypothetical win/loss qualification percentages
| Team | Baseline % | If Week 11 win % | If Week 11 loss % |
|---|---:|---:|---:|
| Slob on my Dobb | 98.48 | 99.74 | 95.89 |
| D0nkey K0ng | 93.31 | 98.66 | 88.55 |
| His Majesty's Blood | 87.62 | 95.17 | 80.10 |
| Dr. Duckhook | 87.55 | 96.40 | 78.90 |
| El Niño | 87.10 | 96.88 | 83.92 |
| Seven Deadly Chins | 82.16 | 88.24 | 61.25 |
| Red Leopards | 50.14 | 64.81 | 27.21 |
| The Chili Cheesers | 38.16 | 58.81 | 20.68 |
| The LLC | 33.41 | 51.78 | 15.61 |
| ObiWan Jacoby | 32.45 | 52.89 | 12.77 |
| Three Dreaded Snake | 9.61 | 22.76 | 2.36 |
| Mud Dogs | 0.01 | 0.07 | 0.00 |

These are **independent stochastic Monte Carlo samples**, not a single controlled paired common-random-number experiment. Scenario differences include sampling drift. This simulation does **not** incorporate NFL player/lineup projections. No baseline/conditional number is an ESPN playoff seed, exact mathematical elimination, guaranteed clinch or a prediction of Week 11's final score. Do not use two-decimal precision as proof of model calibration. The binary fixture/witness proof preserved from November 17 is separate.

## Creative integration and restrictions
- This replaces the prior **source-missing** label for Nov18 with `RECOVERED, SOURCE-BOUND, EDITORIAL-CANDIDATE`. Existing earlier audits correctly reported `NOT_REVERIFIED` *when they were written* and remain immutable historical evidence, not current retrieval status.
- Use these dated values as **pre-Week-11 character circumstances only** with explicit source and "win/loss hypothetical" qualifier, pending independent Analyst/Umpire review.
- After Week 11 ESPN final Monday, November 23, 2026, refresh the league and run new week-specific forecast evidence before claiming "current" playoff percentages. A separate future research capture never authorizes premature island arrival, clinch or mathematically eliminated character.
- Keep protected raw data inside Bullpen; the public Memo repository consumes this sanitized, dated synthesis with a reproducible private source path.
