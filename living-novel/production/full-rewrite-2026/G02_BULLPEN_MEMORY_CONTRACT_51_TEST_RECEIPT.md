# G2 — Bullpen Memory Contract Integration Receipt

Date: 2026-10-18. The actual canonical Bullpen `knowledge/memoryStore.js` and `governance/BULLPEN_MEMORY_ARCHITECTURE.md` were read from `jakekaloper-hub/bullpen` before implementation. Their required fields include id, scope, source, owner, observed_at; provenance, freshness, supersession, status and conflict semantics.

Added `living-novel/os/adapters/bullpen_memory_contract.py`, a read-only export of existing time-filtered World Memory events to Bullpen-contract-compatible entries. It preserves source paths, project scope, confidence and event time and expressly labels each event as WORLD_EVENT_NOT_PERSONAL_MEMORY. No external memoryStore state is mutated, no new OS or database created, and no actual authenticated Director invocation is claimed.

Added `living-novel/os/qa/test_bullpen_memory_contract.py`: required field coverage, prohibition on future event export to a 2022 scene, and personal-knowledge misattribution prevention. Actual Mac isolated checkout verification: `python3 -m unittest discover -s living-novel/os/qa -p 'test_*.py' -q` -> **51 tests passed**.

**Limitations:** Export compatibility only; actual persistent Bullpen MCP/runtime writer, memory readback, freshness/conflict engine exercise, historical owner identity, period divisions, whole-novel literary/visual canon and independent G10 release remain unverified or incomplete. The original dirty Mac checkout was not modified.
