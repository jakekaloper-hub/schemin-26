# Week 3 Pre-Fact Evidence Register V1
**Status:** LIVE / MUTABLE. This is **not FACT_LOCK**.

## Authority rule
Sunday/Monday Flaim/ESPN captures are evidence snapshots. They may establish what the provider showed at capture time but cannot become final winners, records or derived Week 3 standings until authoritative completion.

## Preserve on meaningful change
- matchup actual scores
- projections
- lineup/start-bench state
- remaining-player exposure
- provider matchup status
- provider scoring corrections
- player scoring totals
- transaction evidence
- standings state/freshness

## Current known production constraints
- All six matchups have remained provider-UNDECIDED in the latest captured checks.
- Monday exposure register identifies active PHI/CHI starters for Mud Dogs, Red Leopards, Seven Deadly Chins and El Niño.
- Negative score deltas are provider corrections unless independently attributed.
- Flaim does not expose a trustworthy second-by-second historical fantasy timeline through the currently used matchup interface; exact scoring-play chronology must not be fabricated.

## Snapshot protocol
For each new meaningful capture record: timestamp/source; previous snapshot; matchup actual-score deltas; projection deltas; player deltas when available; lineup changes; provider-status changes; standings changes; remaining exposure; corrections/limitations.

## Transition condition
Only authoritative Week 3 completion triggers creation of immutable `WEEK_3_FACT_LOCK_V1`. Until then all result-dependent prose, art, cover thesis, final page allocation and Week 4 GOTW remain blocked.
