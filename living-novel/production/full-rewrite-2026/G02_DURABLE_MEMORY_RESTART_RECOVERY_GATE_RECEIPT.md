# G2 — Bullpen Durable Memory Restart/Resume Integration Receipt

Date: 2026-10-18. PR #188, branch `novel/reconstruction-board-gate-20261015`.

Added `living-novel/os/qa/bullpen_durable_memory_gate.mjs`. In an isolated temporary directory, the gate obtains seven time-filtered 2026 Week-3 World Memory export entries using the existing Novel adapter, validates each with the **actual** `jakekaloper-hub/bullpen` `knowledge/memoryStore.js` loaded from local authorized read-only clone, and executes the `schemin-26/bullpen-runtime` actual `BullpenRuntime`, `FileJobStore`, `FileArtifactStore`.

First execution deliberately blocks at missing second-stage worker, after preserving completed first-stage artifact. Second execution supplies readback worker and independent test gate, uses `resume:true`, loads artifact from file and checks every exported entry against actual memoryStore key resolution. It verifies first stage invoked once, second stage passes, and a freshly constructed `FileJobStore` reloads the passed state and both persisted artifacts. Temporary directory cleaned after test.

Observed JSON: `result: PASS`, 7 entries, `artifact_sha256:960ed5086a8ce97eea09b49b919d3008aea76717e556e035aebc22f415fb33ed`, `restart_recovery:true`, `resume_without_replay:true`, `actual_bullpen_contract:true`, `temporary_store_only:true`, `authenticated_director_runtime:false`.

Additional actual authorized Mac runs: **51/51 Novel OS Python tests passed** and **24/24 bullpen-runtime Node tests passed**.

**Gate verdict:** in-process integration, file-backed artifact durability and simulated process-restart through fresh store instance verified on isolated repository checkout; no authenticated independent Bullpen Director, production shared memory server, autonomous scheduling, manuscript acceptance or G10 release. Explicit no-false-green constraint maintained.
