# Week 3 — Ingestion Coverage Gap Audit V1
**Status:** RECOMMENDATIONS ONLY. No permanent Memo OS governance change authorized.

## Finding
The Achane event was promoted because commissioner input triggered targeted verification. Existing Week 3 ingestion was strong on fantasy score, player points, transactions, standings, history and continuity, but it did not guarantee a systematic cross-team join between:
**NFL availability event × fantasy ownership × keeper status × lineup slot × keeper cost/control × current matchup × long-arc consequence.**

That is a genuine coverage gap.

## Similar gaps exposed
1. **Keeper injury/availability join:** Puka Nacua and Nico Collins were unavailable in Week 3; without a league-wide pass their keeper significance could remain buried in roster zeros.
2. **Non-keeper structural QB availability:** TDS Caleb Williams and Mud Jayden Daniels materially affect roster construction but can be missed if only active starters are analyzed.
3. **Bench consequence:** high bench scores are captured by player detail but not automatically promoted when they materially contrast with a weak starter.
4. **Failed-bid consequence:** transactions capture failed claims, but matchup/story packets do not automatically connect the failed bid to the winning claimant or subsequent starting usage.
5. **Injury chronology:** fantasy roster state can show IR/0 without establishing when/why the NFL event occurred. External verification is required.
6. **Long-arc continuity:** an injury/absence needs an explicit continuity-out state so future issues do not silently restore a lost asset.
7. **Trade detail:** ESPN transaction rows may be structurally incomplete; story production must not infer counterparties/assets when trade_sides are absent.

## Proposed OS patch candidates — NOT IMPLEMENTED
### A. TEAM_EVENT_SCAN
Run for all 12 teams during each weekly preproduction window:
roster → keepers → lineup → IR/bench → transactions → external availability verification → prior-week delta.

### B. EVENT_MATERIALITY CLASSIFIER
Classify verified events:
- LEVEL 0 routine/no story value
- LEVEL 1 matchup texture
- LEVEL 2 meaningful weekly consequence
- LEVEL 3 season-arc event
- LEVEL 4 league-history/canon event
This is editorial triage, not an automated truth score.

### C. KEEPER_IMPACT JOIN
For every injury/absence, automatically ask:
keeper? cost? year/control known? starting slot? replacement? future continuity?

### D. START/BENCH CONSEQUENCE PASS
After Sunday and after Monday, compare actual starter points to bench alternatives. Label only the numerical contrast; never infer motive or claim the manager “would have won” until final arithmetic supports it.

### E. TRANSACTION-TO-OUTCOME JOIN
Connect verified adds/waivers/failed bids to Week 3 roster usage and points. Preserve claim order/mechanics uncertainty.

### F. CONTINUITY-OUT WRITER
Any Level 3/4 event must write a future-facing continuity state after Fact Lock.

### G. FINAL EVENT DELTA PASS
Immediately before FACT_LOCK, rerun all 12 team scans to catch Monday injuries, inactive changes, scoring corrections, late transactions and provider result changes.

## Acceptance test proposed
A future blank-canvas test should ask whether the system discovers Achane's event **without commissioner prompting**, correctly resolves him as HMB's Round-15 keeper and starter, verifies the external season-ending injury, separates it from matchup causality, and writes the long-arc continuity state.

Jake approval is required before promoting these recommendations into permanent Memo OS governance.
