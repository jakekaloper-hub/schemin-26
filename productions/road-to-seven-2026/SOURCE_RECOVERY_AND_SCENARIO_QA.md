# Road to Seven — Original FFHub recovery and source-to-folio audit

**Audit executed 2026-11-18.** Historical research cutoff **final through Week 10, entering Week 11**. This is an audit of the preserved November 17 experiment, not a newly run FFHub simulation.

## Provenance
- User-supplied Library briefing: `Schemin_26_Week_10_Playoff_Briefing.md` — SHA-256 `2acf94ada97fbba5d2a36b4e2e605590b8a4af98954717ed4c3845c3190ac943`.
- User Library JSON: `Schemin_26_Week_10_Playoff_Scenarios.json` — SHA-256 `4277a19a6940ff3b8000beee072a1567c7843075fca04770c59ff49d67930f86`.
- Protected JSON schema: `schemin.playoff_scenario_packet.v1`. Raw 611 KB scenario source intentionally kept private and **not committed** to this repository.
- Website originally run: `https://theffhub.com/PlayoffTool?site=espn&leagueId=1417621&userId=&s2=&swid=`.
- Original vendor settings: ESPN, Head to Head, seven berths, 10,000 samples, historical scoring average/standard deviation, no player projections or NFL bye model.
- Official provider source: operative final Week 10 snapshot on `memo-week10-preproduction-20261116`.
- Native exact witnesses: `memo-os/week-10/preproduction/playoff-witnesses-final.json` on that production branch, independent of FFHub percentages.

## Direct checks performed against raw JSON
1. League 1417621, season 2026, through Week 10, 12 unique teams and 60 completed games verified against source shape.
2. Exactly **20 saved runs**: 18 named scenarios, one initial baseline, one restored baseline.
3. All 20 raw tables contain **12 named teams each**; per-run probability mass sums to **700.00%**, equivalent to seven playoff berths across 10,000 simulated seasons.
4. All 12 `team_povs` baseline, Week 11 win and Week 11 loss estimates agree with the corresponding saved `vendor_experiment.runs[*].totals` within 0.01 percentage points.
5. All 12 win/loss leverage values agree with arithmetic differences.
6. Eleven retained Week 11-loss qualification witnesses exist; Mud Dogs is the only team reported mathematically eliminated by a Week 11 loss under the documented binary-outcome, no-overrides scope.
7. Original-versus-restored baseline differences reach **1.03 percentage points** (largest: The LLC), with mean absolute drift **0.355 pp**. This is simulation sampling drift, not a standings change.
8. Exact 2^24 enumeration and special constructed witnesses are retained as source evidence; this audit does not claim to have freshly re-enumerated every completion.

**Result:** All executed source-consistency checks PASS. This is NOT an approval of vendor model calibration, exact-solver correctness beyond the checked witness contract, or the final visuals.

## Verified team matrix — seed order (percentages are vendor estimates)
| Seed | Team | Record | Baseline | W11 win | W11 loss | Win–loss spread |
|---:|---|---:|---:|---:|---:|---:|
| 1 | Slob on my Dobb | 6–4 | 98.65% | 99.82% | 96.08% | 3.74 pp |
| 2 | El Niño | 6–4 | 87.22% | 96.71% | 83.71% | 13.00 pp |
| 3 | D0nkey K0ng | 6–4 | 92.88% | 98.93% | 88.11% | 10.82 pp |
| 4 | His Majesty's Blood | 6–4 | 88.06% | 95.79% | 79.25% | 16.54 pp |
| 5 | Dr. Duckhook | 6–4 | 87.20% | 96.89% | 79.99% | 16.90 pp |
| 6 | Seven Deadly Chins | 6–4 | 81.28% | 88.61% | 61.18% | 27.43 pp |
| 7 | Red Leopards | 5–5 | 50.35% | 64.16% | 27.61% | 36.55 pp |
| 8 | The Chili Cheesers | 5–5 | 38.10% | 58.17% | 21.09% | 37.08 pp |
| 9 | The LLC | 4–6 | 33.62% | 50.59% | 16.40% | 34.19 pp |
| 10 | ObiWan Jacoby | 4–6 | 32.72% | 51.68% | 13.38% | 38.30 pp |
| 11 | Three Dreaded Snake | 4–6 | 9.91% | 22.57% | 2.33% | 20.24 pp |
| 12 | Mud Dogs | 2–8 | 0.01% | 0.03% | 0.00% | 0.03 pp |

**Important distinctions:** official seed order is NOT vendor percentage order. A 0.00% sampled outcome is not an exact elimination proof; The LLC 100.00% conditional win-out sample is NOT a mathematical guarantee. Nine final wins guarantee qualification, eight alone does not under this source's rules.

## Special scenario highlights already captured
- ObiWan win-out: FFHub 99.79% conditional estimate, legal 8–6 miss still possible.
- Three Dreaded Snake win-out: 99.36% estimate, legal 8–6 miss still possible.
- The LLC win-out: 100.00% sample estimate, but explicit legal 8–6 miss exists.
- Mud Dogs win-out: 4.54% estimate, outside results still needed.
- Mud's specific four-way 6–8 Burgers division route and separately verified 6–8 wildcard path are described in the briefing and retained exact evidence.
- DK defeating both ObiWan W12 and Snake W13 guarantees Burgers; ObiWan sweep plus one extra DK loss outside their head-to-head guarantees Burgers; Red sweep guarantees Wings.

## Readiness and next consumer
- All seven `folios/RT7-P0x/PAGE_PACKET.md` files now bind the historical source, verified teams and selected Atlas locations; the six paired pages carry baseline and conditional vendor estimates.
- Retained FFHub snapshot already began **after Week 10 finalized**, per its own metadata. An additional FFHub live run without a changed cutoff would be a distinct stochastic experiment, not correction of a pre-finalized source.
- The website's shell returned HTTP 200 on the connected Mac on Nov 18, but no new JS-driven FFHub simulation was executed or captured; do not claim fresh odds.
- Inklings literary drafts, Atlas character/reference audits, Creative rendering and independent Umpire review are separate gates. No PNGs were generated.

## Bullpen authority
Creator: project-local editorial/production pass. Counterweight: Analyst validates evidence class; Scout validates official facts; Librarian preserves provenance; Atlas checks persistent geography; Umpire independently audits actual finished work. No independent role signed off merely by creation of this document.
