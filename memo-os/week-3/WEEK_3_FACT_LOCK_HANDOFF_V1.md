# Week 3 Fact-Lock Handoff V1
**Trigger:** Flaim/ESPN authoritatively marks Week 3 complete and final state is stable.

## Close sequence
1. Final Flaim matchup refresh for Week 3.
2. Canonical ESPN/Schemin Data Gateway cross-check and freshness/provenance review.
3. Final player-detail retrieval for all six matchups.
4. Verify all six provider statuses and winners.
5. Lock final scores.
6. Refresh post-Week-3 standings, W-L, PF/PA and division context.
7. Recompute deterministic derived fields: margins, high/low score, closest/largest margin, streak/record claims used.
8. Resolve lineup/transaction consequences only where evidence supports causality.
9. Record discrepancies; resolve by source hierarchy rather than story preference.
10. Write immutable `WEEK_3_FACT_LOCK_V1` with provenance and calculation evidence.
11. Run FACT_LOCK QA.
12. Only on PASS release downstream result-dependent production.

## Downstream release
FACT_LOCK_PASS → select conditional branches → macro-story/cover thesis → final manuscript → final page allocation → visual beats/compositions → CHARACTER_PACKET_LOCK + reference-attached art → deterministic data composite → page QA gates → PAGE_LOCK → full-issue audit → final QA ledger → PDF assembly → render audit → PUBLICATION_APPROVAL.

## Still prohibited before PASS
No final endings, cover thesis, final standings prose, Week 4 stakes/GOTW, result-dependent hero art, or publication certification.

## Failure behavior
If Flaim and canonical ESPN disagree, preserve both observations, mark the field unresolved, investigate provenance/freshness and keep dependent production blocked. Never select the value that produces the better story.
