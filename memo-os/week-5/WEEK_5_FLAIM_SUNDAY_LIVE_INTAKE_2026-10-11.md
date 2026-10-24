# Week 5 — FLAIM Sunday Live Intake (2026-10-11)

**State:** READ-ONLY PROVIDER SNAPSHOT / PROVISIONAL LIVE / NOT FINAL FACT LOCK / NO WINNERS
**Provider:** Authenticated FLAIM → ESPN, Pro Schemin' Football League, league 1417621, football 2026, scoring/matchup period 5.
**Acquisition:** October 11, 2026, Sunday afternoon. Read time is invocation time; exact timestamp was not provided by the adapter. ESPN league discovery refresh succeeded (6 active ESPN leagues, Schemin confirmed).
**Control:** Existing Issue #146. Preserve earlier October 9 receipt; this is a newer observation, not an immutable ESPN API dump.

## Week 5 live scoring-period points (host → visitor)
**IMPORTANT ESPN semantics:** `totalPoints` returned 0 on both sides despite nonzero `pointsByScoringPeriod['5']`. All provider winner fields are `UNDECIDED`. These figures are **live scoring-period values only**, not verified finished matchup scores.

| Matchup world | Host | Visitor | Live scoring-period points (host — visitor) | Current ESPN projections (host — visitor) | Provider winner |
|---|---|---|---|---|---|
| #1 Champions' Joust | Red Leopards | ObiWan Jacoby | 43.90 — 32.20 | 132.90 — 143.94 | UNDECIDED |
| #2 After the Storm | Slob on my Dobb | Seven Deadly Chins | 26.30 — 109.56 | 119.77 — 182.25 | UNDECIDED |
| #3 Dark Wizard Chess — GOTW | Three Dreaded Snake | His Majesty's Blood | 70.38 — 29.15 | 96.02 — 115.98 | UNDECIDED |
| #4 A Storm Comes to Town | Chili Cheesers | El Niño | 73.40 — 90.70 | 158.71 — 152.49 | UNDECIDED |
| #5 Save the Swamp | Mud Dogs | The LLC | 20.90 — 91.49 | 111.93 — 191.22 | UNDECIDED |
| #6 David vs Goliath | Dr. Duckhook | D0nkey K0ng | 81.95 — 70.64 | 156.27 — 140.60 | UNDECIDED |

## Live starter-level storyline candidates (not final outcomes)
Values below from six authenticated FLAIM `get_matchups(detail=players)` requests, each matched to the same week, live and mutable. Only started players shown.
1. **Joust:** Red — Spencer Shrader 14, Bears D/ST 8.1, Josh Downs 7.7; ObiWan — Packers D/ST 16.9, Jacory Croskey-Merritt 11.7. Both 3–1 entering Week 5; possible clash for the upper standings, no declared favorite/winner.
2. **Mudding:** Chins — Jaylen Warren 22.8, Justin Jefferson 18.1, Emeka Egbuka 17.3, D'Andre Swift 16.6, Tyler Warren 16.6; Slob — Will Reichard 10, Quinshon Judkins 6.4. Dramatic provisional scoring separation; no declared winner.
3. **GOTW chess:** TDS — Bengals D/ST 16.9, Javonte Williams 15.4, Bhayshul Tuten 13.8; HMB — Vikings D/ST 16.9, Mike Gesicki 7.4. Several late game performances may alter narrative and projections.
4. **Storm shootout:** Chili — Christian Watson 34.1, Brock Bowers 16.9, Steelers D/ST 11.7; El Niño — George Pickens 29, Jalen Hurts 17.2, Ka'imi Fairbairn 15. Future scoring may reverse positions. Do not portray El Niño as a sheriff.
5. **Swamp:** LLC — Parker Washington 33.95, Joe Burrow 23.84, Garrett Wilson 18; Mud — Woody Marks 8.3, Jakobi Meyers 5.7. Serious provisional differential; not confirmed land disposition.
6. **David vs Goliath:** Duckhook — Drake Maye 28.8, Rhamondre Stevenson 14.5, Ollie Gordon II 10; DK — Texans D/ST 20.9, Dak Prescott 15.64, MarShawn Lloyd 11.3. Resolved outcome pending.

## Standings entering Week 5 (provider live snapshot)
| Team | W-L | PF |
|---|---|---:|
| Red Leopards | 3–1 | 635.28 |
| ObiWan Jacoby | 3–1 | 558.67 |
| D0nkey K0ng | 3–1 | 620.63 |
| Slob on my Dobb | 2–2 | 662.46 |
| El Niño | 2–2 | 560.72 |
| Chili Cheesers | 2–2 | 571.05 |
| His Majesty's Blood | 2–2 | 558.10 |
| Three Dreaded Snake | 2–2 | 535.77 |
| Mud Dogs | 2–2 | 510.04 |
| The LLC | 1–3 | 534.19 |
| Dr. Duckhook | 1–3 | 524.81 |
| Seven Deadly Chins | 1–3 | 512.94 |

ESPN playoff seed is not a verified final finish, and midseason `madePlayoffs:true` for all teams is not proof of clinching.

## Week 5 transaction intake
Provider: ESPN `mTransactions2`; explicit matchup-period 5 window, **22 rows** returned (October 9 receipt described 18).
**Newer completed activity:**
- October 11 — ObiWan adds Kendre Miller (RB, NO) as a free-agent transaction; no drop recorded.
- October 10 — Duckhook adds Roschon Johnson (RB, CHI), drops Chris Bell.
- October 9 — TDS adds Mike Washington Jr. (RB, LV), drops Kendre Miller.
- October 9 — Duckhook adds Chris Bell, drops Pat Bryant.
Previously observed completed Week 5 waivers:
- LLC bids $51 for Will Shipley, successful.
- Seven Deadly Chins bids $62 Keon Coleman and $32 Dohnte Meyers, successful.
- Chili $5 Jacoby Brissett, successful.
- Duckhook $5 Jaguars D/ST, successful.
**Failed:** HMB bids for Jacoby Brissett ($4), Dohnte Meyers ($6), Keon Coleman ($8), Will Shipley ($19); not acquisitions.
**Unresolved:** TDS Dohnte Meyers waiver is provider-status unknown; do not write as completed.
`count:22` is the returned rows for the Week 5 query, not proof the provider will never add more later. `date_bounds_kind:unavailable`, though period selector is explicit.

## Production integration
- Scout / Data Gateway: preserve data source, period, read date and provisional winner status; next verification after late Sunday/SNF/MNF. Reconcile `totalPoints` discrepancy from individual player/lineup data before Fact Lock.
- Analyst: build player-level scoring swing dossiers with timestamps. Do not interpret partial scores as full-week causal attribution.
- Beat Writer: use the new evidence to refine urgency, stakes and plausible routes, **not final winning POV or result-dependent overtures**. Draft alternative focal notes.
- Groundskeeper: advance six Atlas world packets, visual anchors, mobile multi-panel page design and completeness checklist. No final-result art.
- Librarian: enforce source-plate canon, including DK current hybrid reference and HMB belt.
- Umpire: independently test source semantics and verify late-week finality before releasing result-dependent scenes.

**Read-only FLAIM calls succeeded. No ESPN provider transactions were modified.**
