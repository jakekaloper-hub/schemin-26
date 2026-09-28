# PRO SCHEMIN' TRANSACTION INTELLIGENCE V1
**Source:** Flaim → ESPN 1417621, 2026.
## Observed volume
Week 1: 12 transaction rows — 6 adds, 3 waivers, 1 trade proposal/decline lifecycle row, 1 trade-uphold row, 1 trade row; at least 1 failed-status row.
Week 2: 29 rows — 18 adds, 9 waivers, 1 trade-uphold, 1 trade; at least 4 failed-status rows.
Week 3 retrieval: 44 rows — 12 adds, 29 waivers, 1 trade-uphold, 1 trade, 1 trade proposal; at least 10 failed-status rows.
## Contested-asset proof
Week 3 Eddy Pineiro: Team 3 completed a $6 FAAB waiver; Team 1 has a failed $1 claim for the same player. This is evidence of competing acquisition attempts, not evidence of motive or emotion.
Other observed Week-3 examples include Dr. Duckhook/Team 12 completing an $11 Baker Mayfield waiver, Team 8 completing a $3 Oronde Gadsden waiver, Team 6 completing a $2 Keon Coleman waiver, and failed claims with explicit bid values.
## Normalization rules
Preserve transaction_id, status, timestamp/date, week, team_ids, players_added, players_dropped and faab_bid. PENDING, FAILED and COMPLETE are distinct states. A failed bid is never normalized as ownership. Duplicate provider lifecycle rows must be de-duplicated at story-event level while retaining provenance.
## Literary boundary
Repeated bidding can support a factual behavioral pattern only after sufficient observations. It cannot by itself establish recklessness, desperation, hatred, confidence or betrayal.
