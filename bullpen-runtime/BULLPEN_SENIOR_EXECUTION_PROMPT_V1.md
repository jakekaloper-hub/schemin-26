# BULLPEN SENIOR EXECUTION PROMPT — RUNTIME V1 → PRODUCTION CANARY
**Version:** 1.0
**Decision owner:** Closer
**Mission:** Convert the existing Bullpen Runtime V1 kernel into a truthful, resumable production harness and prove it on one Chronicle spread.

## Operating principle
Do not simulate labor. Do not award PASS from prose. Every claimed action must resolve to an invocation, artifact, test result, or explicit BLOCKED state with evidence.

## Authority
Treat the existing `bullpen-runtime/` implementation as the starting codebase, not as finished architecture. Preserve Schemin canon/data authority and GitHub provenance. Production truth outranks presentation.

## Board assignments
- **Architect / Setup Man:** runtime contracts, persistence, retry/revision state machine, CLI.
- **Librarian:** append-only artifact/job manifests, provenance, SHA/content identity.
- **Pitching Coach:** worker adapter contract for model/agent execution.
- **Visual Development:** image-job adapter contract; no fake image completion.
- **Umpire:** independent gates, fail-closed semantics, tests.
- **Closer:** integration acceptance only after executable evidence.

## Phase 1 — Harden the kernel
Implement:
1. filesystem/GitHub-compatible artifact-store abstraction;
2. durable JSON job manifests capable of resume;
3. bounded retry and revision routing;
4. worker/gate invocation records including timestamps, attempt, input/output artifact IDs and error;
5. deterministic terminal states: PASSED / FAILED / BLOCKED;
6. CLI entry point to start or resume a job;
7. schema validation where practical without creating dependency bloat.

No worker may self-certify its own output.

## Phase 2 — Real adapter boundary
Create explicit adapters for:
- agent/model worker invocation;
- image generation;
- visual inspection/QA;
- GitHub artifact publication.

If credentials/tooling are unavailable in repository CI, adapter must return BLOCKED with a machine-readable reason. Never substitute mock success in production mode.

Mocks are allowed only in tests and must be unmistakably named.

## Phase 3 — Test suite
Prove at minimum:
- happy path;
- missing worker blocks;
- missing artifact blocks;
- gate rejection fails;
- bounded retry succeeds after revision;
- retry exhaustion fails;
- persisted job resumes without replaying passed stages;
- creator cannot satisfy its own independent gate;
- production adapter unavailable => BLOCKED, not PASS.

## Phase 4 — CI proof
Run tests through GitHub Actions. Capture workflow/run/job evidence. Do not call Runtime V1 production-ready until CI is green.

## Phase 5 — Chronicle canary
Only after green CI, prepare one real Prologue spread job using the locked manuscript/canon/source packet.
The canary must create:
- immutable source packet;
- exact manuscript slice;
- spread specification;
- actual generated image artifact if an image worker is available;
- visual/character QA result;
- composed spread if composition tooling exists;
- final Umpire/Closer result.

If any external production adapter is unavailable, stop the canary at BLOCKED and identify the exact missing capability. That outcome is preferable to fabricated completion.

## Acceptance criteria
Runtime is accepted only when:
- state survives process boundaries;
- every stage is traceable;
- every artifact has provenance;
- gates are independent;
- retries are bounded;
- CI proves core behavior;
- the canary demonstrates the production boundary truthfully.

## Execution behavior
Think first, then implement. Review code after implementation. Fix discovered defects before reporting. Commit durable work to `jakekaloper-hub/schemin-26`. Report exact paths, commit SHAs, test/workflow evidence, and any genuine blocker.

**Do not stop at a plan. Execute until a real external dependency prevents further progress.**
