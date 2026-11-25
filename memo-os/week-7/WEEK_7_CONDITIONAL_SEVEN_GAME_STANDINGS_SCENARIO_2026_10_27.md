# Week 7 — Conditional Seven-Game Standings Scenario (NOT ESPN OFFICIAL)

**Evidence:** FLAIM 2026-10-27, ESPN league 1417621. Six-game provider standings + Week 7 `currentPoints` snapshot. All six provider `winner` fields remained `UNDECIDED`. This document is a deterministic **what-if projection**, not official seven-game standings, a playoff seed order or Fact Lock. Do not publish as the State of the Realm without official confirmation.

## Calculation
For each team, add the observed Week 7 `currentPoints` to six-game `pointsFor`, add the opponent's observed score to `pointsAgainst`, and add one conditional win or loss based solely on the observed point comparison. Two-decimal rounding is display-only. Display order below sorts by conditional wins then PF, **not ESPN tiebreakers or playoff seeds**.

| Team | Conditional W–L | Conditional PF | Conditional PA |
|---|---:|---:|---:|
| Slob on my Dobb | 4–3 | 1096.78 | 969.12 |
| The Chili Cheesers | 4–3 | 1014.74 | 1027.99 |
| D0nkey K0ng | 4–3 | 1003.70 | 941.76 |
| Red Leopards | 4–3 | 1002.31 | 906.88 |
| Dr. Duckhook | 4–3 | 983.86 | 1039.73 |
| His Majesty's Blood | 4–3 | 945.49 | 907.84 |
| Seven Deadly Chins | 4–3 | 931.78 | 934.51 |
| ObiWan Jacoby | 4–3 | 931.22 | 886.99 |
| El Niño | 3–4 | 971.03 | 981.31 |
| Three Dreaded Snake | 3–4 | 900.59 | 966.79 |
| The LLC | 2–5 | 976.82 | 1046.39 |
| Mud Dogs | 2–5 | 882.65 | 1031.66 |

## Division overlay (source: world/atlas/foundation/EXISTING_UNIVERSE_INVENTORY_V1.md)
- **Burgers:** DK 4–3, ObiWan 4–3, TDS 3–4, Mud Dogs 2–5.
- **Wings:** Slob 4–3, Chili 4–3, Red 4–3, Duckhook 4–3.
- **Pizza:** HMB 4–3, Chins 4–3, El Niño 3–4, LLC 2–5.

This is not an authenticated divisional ranking or tie-break resolution. League division identities are cultural overlays, not geographic biomes.

## Required before publication
1. FLAIM/ESPN must report final winner and seven-game standings, or an established Memo OS authority must explicitly permit publication of labeled provisional scenarios.
2. Confirm tie-breaker rules and provider seed ordering; do not substitute points-for sorting as official ranks.
3. Power Rankings must use its own established analytical method and actual previous published rank baseline; no fabricated movement.
4. Preserve this scenario as audit history if ESPN later changes scores or corrections.

**State:** INTELLIGENCE WORKING MODEL / NOT FACT LOCK / NOT RENDER READY.
