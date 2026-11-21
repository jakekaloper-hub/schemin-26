# The Road to Seven — Week 12–14 Future Forks

**Executed in FFHub's actual Playoff Machine on November 18, 2026, league 1417621.** The 20 captured UI scenarios select one winner in each of ten distinct remaining Weeks 12–14 fixtures, while all other games remain simulated. 10,000 Monte Carlo simulations per scenario, ESPN Head to Head, 7 berths, Week 10 final baseline. Distinct from the November 17 research and the November 18 Week 11 experiment batch. These are what-if qualification *estimates*, not a forecast of a specific game's winner, and they do not incorporate NFL injuries or rosters.

## Week 12 — first divisional pass

| Fixture | If first team wins: their odds | If second team wins: their odds | First team leverage | Second team leverage |
|---|---:|---:|---:|---:|
| D0nkey K0ng vs ObiWan Jacoby | 99.48% | 51.36% | 13.48 pp | 35.33 pp |
| Mud Dogs vs Three Dreaded Snake | 0.07% | 13.83% | 0.07 pp | 10.89 pp |
| Red Leopards vs Dr. Duckhook | 71.37% | 97.01% | 37.03 pp | 20.17 pp |
| El Niño vs Seven Deadly Chins | 96.37% | 96.37% | 21.83 pp | 23.57 pp |

## Week 13 — control of the cut line

| Fixture | If first team wins: their odds | If second team wins: their odds | First team leverage | Second team leverage |
|---|---:|---:|---:|---:|
| Three Dreaded Snake vs D0nkey K0ng | 19.25% | 97.96% | 14.32 pp | 13.00 pp |
| The Chili Cheesers vs Red Leopards | 57.36% | 70.21% | 35.79 pp | 39.50 pp |
| Slob on my Dobb vs Dr. Duckhook | 99.76% | 96.48% | 3.81 pp | 12.45 pp |
| El Niño vs His Majesty's Blood | 96.48% | 96.22% | 17.53 pp | 15.93 pp |

## Week 14 — final-week doors

| Fixture | If first team wins: their odds | If second team wins: their odds | First team leverage | Second team leverage |
|---|---:|---:|---:|---:|
| Mud Dogs vs D0nkey K0ng | 0.13% | 95.93% | 0.13 pp | 13.82 pp |
| El Niño vs The LLC | 97.17% | 51.90% | 18.56 pp | 35.89 pp |

## Editorial consequences

**The real knife-edge is Week 13 Red vs Chili.** Holding that game alone fixed while simulating the others shifts Red's qualification estimate from 30.71% on a loss to 70.21% on a win, a 39.50-point swing. Chili moves 21.57% on a loss to 57.36% on a win, a 35.79-point swing. This makes their shared page (#7 vs #8) a **future rematch with two different possible endings**, but neither ending has occurred.

**Week 12 ObiWan vs DK** is a major Burgers gate: ObiWan 51.36% if winning compared with 16.03% if losing (35.33 pp). DK remains favored in either conditional state (99.48% after win vs 86.00% after loss). The league is heavily shaped by that earlier rematch, not only Week 11 vs Chili.

**Week 12 Red vs Duckhook** is similarly consequential (Red 71.37% after win vs 34.34% after loss). **Week 14 LLC vs Niño** is another late gate: The LLC 51.90% with win vs 16.01% with loss.

**Mud** remains mathematically alive under exact witness scenarios, even though a single Week 12/14 loss scenario reports 0.00% qualifying. This simulated zero is not the proof; the mathematical qualification requirements from the original packet remain controlling. A loss before reaching Week 14 would already end Mud's path under the original binary-outcome math.

**Burgers division guarantees are exact, not inferred from these samples:** DK can secure Burgers by beating ObiWan Week 12 and Snake Week 13. ObiWan's win-out plus one additional DK loss outside their rematch also establishes an exact Burgers path. These guarantees belong to the independent witness/rules layer, not to the FFHub simulation probability column.

## Verification & provenance

- Current site <https://theffhub.com/PlayoffTool?site=espn&leagueId=1417621&userId=&s2=&swid=>; real UI selected winners. Each game tested both possibilities; full twelve-team odds table recorded for every run.
- Ten distinct actual future league games; 20 hypothetical outcomes; every captured output accounts for seven berth probabilities totaling 700%. Browser closed following capture.
- Full source JSON kept on connected Mac under `Documents/Schemin-26/Road-to-Seven/evidence-2026-11-18/ffhub-week12-14-future-forks.json`, SHA-256 `ccadd5dd46d9080539aca1e15a9b8c26afb3ae1ec305ed0023838902dbb17c80`.
- Compact all-12-team outcome summaries: [future-fork machine-readable output](FFHUB_FUTURE_FORKS_2026-11-18.json).
- Additional output distributions reflect sampling variation even when fixtures are unchanged. Do not publish as exact odds, mathematically determined seeds, title odds, or game predictions.
