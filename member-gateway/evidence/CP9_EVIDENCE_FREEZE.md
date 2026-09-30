# CP9 Evidence Freeze — Pitts Member Acceptance & Durable Replay

**Status:** PASSED  
**Certified implementation head:** `a9c22c7fa98e918954d874d5546d5f1bd38fae15`

## Exact-head certification
- Member AI Gateway Phase 1 CI — PASS — run 36755929863
- Flaim Adapter CI — PASS — run 36755929869
- Bullpen Runtime CI — PASS — run 36755929734

## Production invariant
A workflow is replayable only when its Warden-approved response packet and terminal
`COMPLETED` state are persisted by the same RunStore `complete()` operation.
Delivery is a separate state and cannot promote an incomplete workflow.

## Repair cycle
GitHub precedent review showed mature idempotency implementations converge on durable
response capture, monotonic completion, replay without re-execution, and fail-closed
handling of incompatible state. Schemin adopted those principles without importing
external code.

## Umpire acceptance
The suite covers:
- Pitts job discovery without Director/Mercer/write exposure;
- fresh execution and understandable stale-data state;
- duplicate replay without re-execution;
- delivery failure followed by replay;
- legacy completed rows without stored response fail closed;
- revoked client cannot receive stored response;
- crash before completion cannot appear replayable;
- completion-before-delivery remains safely replayable;
- incomplete runs cannot be marked delivered;
- arbitrary terminal success transitions are forbidden;
- retained CP1-CP8 Gateway regressions;
- Warden attack tests;
- Flaim Adapter regressions;
- Bullpen Runtime regressions.

## Gate decision
CP9 is frozen **PASSED**. CP10 — Jake/Commissioner Acceptance + Private Isolation is authorized.
No deployment or PR merge is implied by this freeze.
