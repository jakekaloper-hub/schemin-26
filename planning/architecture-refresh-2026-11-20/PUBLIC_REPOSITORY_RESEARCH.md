# Cross-OS public repository research (2026-11-20)
**Source-level review, not approved adoption.** All comparisons below are to established project architecture. The existing zero-incremental-spend rule remains controlling.

| Candidate repo | Source-supported pattern | Schemin decision |
| --- | --- | --- |
| [mrdoob/three.js](https://github.com/mrdoob/three.js), MIT | Browser WebGL/WebGPU 3D rendering | Evaluate renderer/fallback test coverage and scene quality for observer site; **do not replace existing graphics** without baseline parity tests |
| [open-telemetry/opentelemetry-js](https://github.com/open-telemetry/opentelemetry-js), Apache-2.0 | Cross-stage traces, metrics and context propagation | Compare to existing Bullpen trace/span correlation; adopt ideas only if source and cost analysis justify them |
| [temporalio/sdk-typescript](https://github.com/temporalio/sdk-typescript), MIT | Durable TypeScript workflows/activities | **Defer** dependency: server/worker overhead and budget remain unproven; use patterns to test resumability in current Bullpen Runtime |
| [colyseus/colyseus](https://github.com/colyseus/colyseus), MIT | Authoritative multiplayer room/state synchronization | **Not now**: current public observer host is source-bound and read-only, not an authenticated multiplayer live-world server |

### Three modeled consultant method lenses
- Jeff Lunsford (strategy): prioritize audience-visible world continuity and user outcomes before infrastructure complexity.
- John Ezzell (enterprise): preserve canonical contracts and implement reversible migration gates with interoperability tests.
- Tim Veil (engineering): benchmark failing paths and verify negative cases, not just green prose or architectural diagrams.

These are analytical applications of documented advisory responsibilities, **not direct quotations, personal participation, endorsement or a live consultant session**. No package has been installed or copied. Review upstream LICENSE, security posture, pinned version and dependencies again before any import.
