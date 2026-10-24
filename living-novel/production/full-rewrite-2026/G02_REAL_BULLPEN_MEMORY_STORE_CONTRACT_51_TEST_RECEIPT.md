# G2 — Real Bullpen memoryStore contract verification

Date: 2026-10-18. Branch: `novel/reconstruction-board-gate-20261015` (Draft PR #188).

**Actual source under test:** isolated authenticated checkout of `jakekaloper-hub/bullpen`, `/tmp/bullpen-memory-verify/knowledge/memoryStore.js`, on the connected authorized Mac. Test driver `living-novel/os/qa/bullpen_memory_live_contract.cjs` calls the real Bullpen `createMemoryStore` and `assertMemoryEntry` directly with 7 2026 Week 3 time-filtered World Memory exports.

**Initially failed:** `freshness_days:null` rejected by the actual validator. Corrected `living-novel/os/adapters/bullpen_memory_contract.py` to omit optional freshness_days when not configured; aligned Python test. Rerun reported `contract: PASS`, `entries: 7`; validation, add/get readback, project scope isolation, conflict identification, supersession, freshness/staleness all passed. Rerun Novel OS Python regression suite: **51 tests passed, 0 failed**.

Commands: `BULLPEN_MEMORY_STORE_PATH=/tmp/bullpen-memory-verify/knowledge/memoryStore.js node living-novel/os/qa/bullpen_memory_live_contract.cjs` and `python3 -m unittest discover -s living-novel/os/qa -p 'test_*.py' -q` in isolated `/tmp/schemin-novel-gate` checkout.

**G2 status:** Actual implementation contract compatibility PASS with in-process ephemeral memoryStore. Durable persistent shared Bullpen runtime, authenticated Director invocation, restart recovery, automatic memory synchronization and independent Umpire gate remain unverified, as do full manuscript/world/art G4–G10 release gates. No false-green, no production store mutated.
