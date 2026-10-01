# TEST REPORT — Character Reference Portability Mission

**Status:** PENDING PR CI
**Date:** 2026-09-30

## Test surfaces prepared
- active character runtime compile;
- `canon/characters/tests/` full discovery;
- Render Adapter candidate regression;
- source-byte audit with explicit expected `SOURCE_BYTES_REQUIRED` exit state;
- 2/6/12 subject-binding synthetic control-plane tests;
- stale alias / identity-lock red team.

## Evidence expectation
A passing control-plane suite proves only fail-closed enforcement. It does **not** prove:
- 12 durable repository binaries exist;
- current raw bytes freshly match approved SHA-256 values;
- a real provider mounted those bytes;
- a real provider deterministically bound multiple subjects.

Those require separate runtime evidence and remain gated.
