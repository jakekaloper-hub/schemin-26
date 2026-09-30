# CHARACTER LOCK EXECUTION RECEIPT — 2026-09-30 TRANCHE 2

## Recovery
Repository evidence `R4_SOURCE_BYTE_HASH_RECEIPT_2026-09-29.md` proves the exact twelve Commissioner source bytes were present in an execution container on 2026-09-29 and matched the registered SHA-256 values 12/12. Therefore SOURCE_IDENTITY_BYTES=PASS historically.

This does NOT prove current durable persistence. Current Project raw-byte materialization remains denied for the twelve registered assets and the Characters.docx recovery path. R1 remains BLOCKED on durable renderer-addressable ingestion/fresh-context retrieval.

## Security hardening
Generation eligibility changed from an unauthenticated SHA-256 of public claims to HMAC-authenticated claims with an injected trusted signing key. Claims remain request-, Character-ID-, asset-hash-, renderer-route-, policy-version-, expiry- and nonce-bound. Adapter supports consumed-nonce replay rejection and reports renderer_invoked.

This repairs the identified forgeability defect in the draft implementation but does not establish R6 PASS until executable Character Lock tests run and all real character-bearing renderer routes are proven unable to bypass the adapter.

## CI observation
GitHub Actions run 36730637847 on PR #32 head 82f9b90d34dfc33b70c1cb77b5da38da92dbf144 completed SUCCESS. Its Bullpen Runtime CI executed 10 Node tests and passed 10/10.

The workflow does NOT execute `canon/characters/tests/*.py`. Therefore:
- Bullpen Runtime CI = PASS.
- Character Lock Python CI = NOT OBSERVED / HOLD.
- R6 = NOT PASS.

## Sanitation
Twelve individual migration contracts and a 12-row acceptance matrix exist. Archaeology confirms high-risk stale material requiring classification/quarantine rather than blind deletion.

## Current promotion
INCIDENT OPEN / GENERATION BLOCKED.
Waiver attempt #4 remains prohibited.
