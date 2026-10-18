# G2 — Historical Identity Isolation Correction

Date: 2026-10-18. Branch: `novel/reconstruction-board-gate-20261015`, PR #188.

**Finding:** `author_context_reader.author_context` used the present-day 2026 team ID as part of `permitted_team_ids` for scenes in 2026. While assessing historical matchup rows (2015–2025), this implicitly classified all rows involving the matching historical slot as that modern character's personal history. A twelve-character Author Memory packet was therefore susceptible to unsupported owner inheritance.

**Correction:** For rows whose source season is before 2026, permit character-specific matchup attribution **only through explicitly supplied, independently verified historical identity links**. Present 2026 team IDs may apply to 2026 records, but cannot backfill earlier seasons. Public historical rows remain available in `other_public_matchups` as archive information, not owner memories.

**Regression:** New `living-novel/os/qa/test_2026_identity_leak.py` instantiates all twelve current characters' 2026 Week 3 packets and asserts no inherited personal historical matchups, while the public archive remains nonempty. The actual connected Mac isolated checkout executed `python3 -m unittest discover -s living-novel/os/qa -p 'test_*.py' -q`: **59 tests passed** at commit `8dd98d8`.

**Gate:** identity isolation mechanical PASS. G2 authenticated production runtime, owner lineage verification, granular season-scoped identity sources, actual Director consultations, G5–G9 manuscript/visual deliverables and G10 independent review/merge/publication remain uncompleted. This test is not an independent Umpire decision.
