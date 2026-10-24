# G2 Relationship and Promise Context — 2026-10-18

Implemented `living-novel/os/adapters/story_continuity_context.py` as a read-only overlay of existing noncanon author room relationship register `R40_TWELVE_OWNER_CROSS_CAUSAL_MAP_V1.json` and existing `living-novel/os/promises/STORY_PROMISE_LEDGER_V1.json`. No new OS or mutable memory database created. Current promise register has **zero records** and is reported empty, not populated with invented obligations.

The relationship adapter accepts a principal ID and scene year/week, admits only edges with explicit year/week temporal anchors at or before cutoff, withholds future or imprecisely dated anchors, separates FACT-labeled source-register claims from PROPOSED options and explicitly disclaims independent verification/personal memory/canon promotion. Year-range anchors are withheld rather than given invented exact weeks.

Added `living-novel/os/qa/test_story_continuity_context.py` containing four tests for W3 future cutoff, W4 eligible register record, empty promise ledger, and unspecified-year-range withholding. Initial regex defect was corrected before acceptance. Authorized isolated Mac checkout ran `python3 -m unittest discover -s living-novel/os/qa -p 'test_*.py' -q`, resulting **63 tests passed, 0 failures**.

G2 remains partial: no authenticated live Bullpen Director access or persistent production write/readback, relationship assertions not independently source-verified, and no real promises extracted/admitted. G5–G10 manuscript, visual review and publication remain blocked pending independent acceptance. No canon promotion, merge or publication is implied.
