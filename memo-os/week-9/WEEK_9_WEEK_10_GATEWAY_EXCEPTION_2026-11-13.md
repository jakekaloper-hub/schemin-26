# November 13 — Parsed Gateway Cross-Source Exception (V5.2-RC)

Supplemental source review after merged [PR #310](https://github.com/jakekaloper-hub/schemin-26/pull/310). **Not a Steward acceptance or release certificate.**

GitHub `data/live` manifest shows parsed ESPN snapshot captured **2026-11-13 07:05:41 UTC**, `stale:false` **at capture only**, snapshot blob `7d1645520a609923440c0aa90d6fecab5e3729ec`, manifest blob `f55b1276ef595b8159be5cc504460f581266a02d`. This is not native HTTP response bytes/headers. The Flaim ESPN read occurred later the same day; these are **not simultaneous captures**.

## Domain-specific comparison
| Domain | Preliminary result |
|---|---|
| Weeks 9–11 true team pairings | **18/18 matched** |
| Weeks 9–11 ESPN winner states | **18/18 matched** |
| Week 9 final scores | **6/6 matched** |
| Week 10 live/partial scores | **1/6 matched; 5/6 differed** |
| Week 11 early 0–0 scores | **6/6 matched** |
| Standings seed, W–L and points-for | **12/12 matched** |
| Transaction-event independent parity | **Unavailable in parsed gateway** |
  
For the five Week 10 mismatches, the direct gateway captured all fixtures as 0–0 while the later authenticated Flaim read reported the following **provisional** scoring:

- The Chili Cheesers 36.40–0.00 D0nkey K0ng; gateway 0–0
- Red Leopards 21.72–20.30 El Niño; gateway 0–0
- Three Dreaded Snake 2.00–0.00 Seven Deadly Chins; gateway 0–0
- Dr. Duckhook 0.00–7.30 His Majesty's Blood; gateway 0–0
- ObiWan Jacoby 0.00–30.70 The LLC; gateway 0–0

**Classification:** `SCORE_DOMAIN_ASYNCHRONOUS_MISMATCH`. Do **not** declare all ESPN unavailable; do **not** call stale until source semantics and capture timestamps are resolved. Only the live-score corroboration claim is held. Week 9 final scores, Week 10 fixture identities/winner-state, Week 11 fixture identities and ESPN standings continue to pass preliminary comparison.

## Routing
Return score-coherence validation to upstream source acquisition/reconciliation for timely new timestamped comparative snapshots. No independent Steward RECEIVED/VALIDATED identity, wire-provenance receipt, signed semantics/freshness acceptance, or approved exception exists. `CANONICAL_SNAPSHOT_LOCK` and `FACT_LOCK` **BLOCKED**; downstream ART/COPY/PAGE/release controls **WAITING**. No fictitious staff ACK, no permanent V5.2 promotion, no Mercer. Continue Issue #268; do not open redundant missions.
