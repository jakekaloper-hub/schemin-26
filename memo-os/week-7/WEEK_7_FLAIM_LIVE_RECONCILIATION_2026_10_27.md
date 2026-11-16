# Week 7 — October 27 Live FLAIM Evidence Reconciliation

**Status:** ACTUAL CONNECTOR READ / UNDECIDED PROVIDER RESULT / PREPRODUCTION ONLY.
**League:** ESPN 1417621, 2026 Pro Schemin' Football League. **Read date:** 2026-10-27. Read-only calls: session, league info, Week 7 matchups, Week 8 matchups, standings.

## Week 7 provider scoreboard (currentPoints, not totalPoints)
| Home | Points | Away | Points | Observed leader | Provider winner |
|---|---:|---|---:|---|---|
| Three Dreaded Snake | 141.42 | Dr. Duckhook | 141.74 | Duckhook +0.32 | UNDECIDED |
| D0nkey K0ng | 122.67 | El Niño | 133.75 | El Niño +11.08 | UNDECIDED |
| ObiWan Jacoby | 94.75 | Seven Deadly Chins | 116.60 | Chins +21.85 | UNDECIDED |
| Mud Dogs | 108.72 | The Chili Cheesers | 134.92 | Chili +26.20 | UNDECIDED |
| Red Leopards | 148.53 | His Majesty's Blood | 137.02 | Red +11.51 | UNDECIDED |
| Slob on my Dobb | 155.92 | The LLC | 111.21 | Slob +44.71 | UNDECIDED |

**Critical provider semantics:** ESPN/Flaim `totalPoints` remains 0 on all six; `currentPoints` contains observed scores. All six `winner` values are UNDECIDED. Do not assert certified winner, result or Fact Lock from this snapshot.

## Standings source-state
The live standings read returned twelve teams with W+L = **6** for each team, despite Week 7's observed score completion. The endpoint has not incorporated Week 7 into records. These are pre-Week-7 standings, not Week 7 State of the Realm.

| Reported rank | Team | W–L | Points for |
|---:|---|---|---:|
| 1 | ObiWan Jacoby | 4–2 | 836.47 |
| 2 | His Majesty's Blood | 4–2 | 808.47 |
| 3 | Red Leopards | 3–3 | 853.78 |
| 4 | D0nkey K0ng | 4–2 | 881.03 |
| 5 | Slob on my Dobb | 3–3 | 940.86 |
| 6 | The Chili Cheesers | 3–3 | 879.82 |
| 7 | Dr. Duckhook | 3–3 | 842.12 |
| 8 | Seven Deadly Chins | 3–3 | 815.18 |
| 9 | Three Dreaded Snake | 3–3 | 759.17 |
| 10 | The LLC | 2–4 | 865.61 |
| 11 | El Niño | 2–4 | 837.28 |
| 12 | Mud Dogs | 2–4 | 773.93 |

Do not mislabel ESPN standings rank as editorial Power Rankings or final playoff qualification. Divisional standings require separately sourced division membership and Week 7 finality.

## Week 8 fixtures (provider schedule)
1. Mud Dogs HOME vs Dr. Duckhook AWAY
2. ObiWan Jacoby HOME vs El Niño AWAY
3. D0nkey K0ng HOME vs Seven Deadly Chins AWAY
4. Three Dreaded Snake HOME vs The Chili Cheesers AWAY
5. Slob on my Dobb HOME vs His Majesty's Blood AWAY
6. Red Leopards HOME vs The LLC AWAY

All Week 8 fixtures have UNDECIDED winner and currentPoints 0. The proposed Slob/HMB Game of the Week remains a creative candidate, not Founder-selected Week 8 GOTW.

## Editorial consequences
- Week 7 scoreboard can use `currentPoints` with provisional status.
- Cover's Duckhook 0.32 and Slob's weekly-high 155.92 remain observed but not certified.
- State of Realm and Power Rankings remain on fact/evidence HOLD; do not fabricate seven-game records or movement arrows.
- Six story manuscripts may proceed under Founder-approved fiction direction; fictional physical outcomes are not ESPN records.
- This snapshot does not replace actual player-level contribution or transaction verification.

**No renderer, publication, merge or independent Umpire acceptance.**
