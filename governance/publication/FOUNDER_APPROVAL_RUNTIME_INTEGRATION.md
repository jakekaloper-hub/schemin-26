# Issue #184 — Founder approval runtime adapter

**Status: CANDIDATE / NOT CONNECTED TO LIVE MEMO PUBLICATION.**

`founder_approval_gate.py` checks Memo V5 issue-state transitions and existing release QA. `founder_approval_runtime.py` provides a signed receipt envelope, integrity-protected JSON checkpoint, and fail-closed transition operation. It does **not** replace the active Memo OS page production or publication controllers.

## Trusted boundary
- `MEMO_APPROVAL_SIGNING_KEY`: at least 32 characters, injected from protected secret management; never included in source, logs or user-controlled execution.
- `MEMO_FOUNDER_PRINCIPAL`: exact principal ID from authenticated identity service.
- `MEMO_TRUSTED_IDENTITY_VERIFIER`: ID of trusted upstream verifier.
- `issue_founder_receipt` MUST be callable only from the trusted backend after actual identity verification. Merely passing a principal/verifier string is NOT authentication.
- The current module uses HMAC integrity but does not implement identity-provider verification, key rotation, anti-replay across state stores, multi-writer locking or trusted provenance for individual QA booleans. Do not enable public release on the strength of this adapter alone.
- Durable file replacement protects against interrupted single-process writes. Production concurrency requires a locked or transactional store and verified issuer authorization.
- Any source plan, QA evidence, final artifact or character reference change must invalidate dependent approvals and re-run owning gates; runtime integrations must enforce this rather than relying on callers to update hashes.

## Tests
`python -m unittest discover -s governance/publication -p 'test_founder_approval_*.py' -v`

Negative cases include direct-release bypass, missing approvals, modified PDF hash, altered persisted state, forged receipt, wrong founder, absent key and release QA failures.

## Remaining production acceptance
1. Identify all actual publication entry points and route transitions through one authenticated service.
2. Integrate verified external identity provider and trusted, non-forgeable approval issuer.
3. Persist receipts and release state in production transaction store with concurrency protection.
4. Bind QA results to independently verified evidence, not caller-controlled Boolean claims.
5. Exercise real publication fixture, interruption recovery and end-to-end bypass attempts.
6. Independent Umpire review and Founder promotion. Keep PR #185 draft until all are evidenced.
