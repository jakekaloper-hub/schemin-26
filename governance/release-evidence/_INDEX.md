# Release Evidence Control

**Status:** ACTIVE GOVERNANCE UTILITY  
**Purpose:** prevent historical or stale PASS receipts from masquerading as current release evidence.

This directory is not a new operating system. It is a compact machine-readable evidence layer beneath existing release authorities.

## Files

- `registry.json` — system/receipt records.
- `release_evidence.py` — current-applicability resolver.
- `test_release_evidence.py` — stale-receipt and changed-subsystem regression tests.

## Applicability law

A receipt must record:
- exact tested commit SHA;
- branch;
- test suite;
- timestamp;
- result;
- unresolved blockers;
- required check outcomes;
- subsystem anchor path + exact Git blob SHA where repository-local.

Resolver states:
- `CURRENT_HEAD_PASS`
- `CURRENT_SUBSYSTEM_PASS`
- `HISTORICAL_ONLY`
- `HISTORICAL_ONLY_CHANGED_SUBSYSTEM`
- `BLOCKED_CURRENT_EVIDENCE`
- `NOT_PROVEN`

A red required check always outranks a PASS label.

An old PASS may remain applicable after unrelated repository changes only when the controlled subsystem anchor bytes are unchanged.

A changed subsystem invalidates the old receipt for current applicability without deleting its historical value.
