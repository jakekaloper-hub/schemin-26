# Phase 1 — Exact Source-Byte Portability HOLD Receipt

**Date:** 2026-10-01  
**Phase:** 1 — Exact Source-Byte Portability  
**Gap:** CNR-GAP-001  
**Disposition:** **HOLD — AUTHORIZED RAW-BYTE EXPORT / MATERIALIZATION UNAVAILABLE**  
**Authoritative Director:** The Librarian  
**Counterweights:** The Setup Man, The Warden, The Architect  
**Final acceptance authority:** The Umpire

## Mission result

Phase 1 cannot legitimately PASS.

Bullpen exhausted the currently available zero-incremental-spend source paths and isolated the blocker to one exact transport capability:

> The 12 approved native Project/Library image records remain present and identifiable, but this execution context cannot export or materialize their original raw bytes.

This is **not** a missing-character decision and **not** a source-identification problem.

## What is proven

For all 12 current Commissioner-approved character sources:

- the exact Character ID is known;
- source filename is known;
- original conversation file ID is known;
- persistent Library file ID is known;
- persistent Library record is still present;
- Library metadata reports the expected file size;
- approved expected SHA-256 is recorded;
- canonical target repository path is defined;
- provenance remains Commissioner-supplied;
- no paid provider is required to identify the source.

Library enumeration on 2026-10-01 found **12/12** registered Library IDs.

## What failed

### Original Project/conversation file handles

Raw materialization was attempted for all 12 source file IDs.

Result for **12/12**:

`This Project file does not have an authorized raw-byte materialization path.`

### Persistent Library IDs

Direct raw materialization was also attempted using persistent Library IDs.

Result:

`This Project file does not have an authorized raw-byte materialization path.`

This proves that swapping the opaque identifier form does not bypass the platform authorization boundary.

### Repository target paths

All 12 canonical target paths under:

`canon/characters/assets/<CHARACTER_ID>/primary/<SOURCE_FILE>`

were checked on current `main`.

Result: **0/12 exist**.

Therefore prior hash receipts cannot be converted into clean-context binary retrieval from GitHub.

### Direct Library image read

A direct read of the current Wilson source was tested as an independent route.

Result:

`Native image pixels were unavailable; returned extracted text only.`

The returned text view is not the source binary and cannot support fresh SHA-256 verification.

## Why previous hash evidence is insufficient

The repository contains earlier SHA-256 receipts proving that the Commissioner-supplied bytes were once observed and hashed.

Those receipts remain valid historical evidence.

They do **not** satisfy Phase 1 because Phase 1 explicitly requires:

1. fresh binary retrieval;
2. fresh SHA-256 computation;
3. durable storage;
4. fresh-context re-retrieval;
5. corruption/swap testing against the durable copy.

None of those can be honestly claimed without access to the source bytes.

## Counterweight rulings

### Setup Man
**HOLD.** Metadata-only visibility is not runtime portability.

### Architect
**HOLD.** Creating another metadata registry or derived image store would duplicate authority without solving binary custody.

### Warden
**HOLD.** Substituting a stale composite, generated preview, semantic reconstruction, or prior hash receipt would violate the fail-closed reference boundary.

### Umpire
**HOLD ACCEPTED.** The blocker is sufficiently isolated and no unsupported PASS is permitted.

## Exact irreducible gate

Phase 1 can resume immediately when **one authorized zero-spend path exposes the original raw bytes** for the existing registered files, for example:

- native Library/Project raw-file materialization becomes authorized in this execution context; or
- the same exact source bytes are attached/uploaded through a path that exposes original bytes to the active conversation/runtime; or
- another already-authorized zero-incremental-spend storage surface exposes the exact binaries.

The source identities do **not** need to be rediscovered.

The character designs do **not** need to be recreated.

The expected hashes do **not** need to be guessed.

## Resume command

`/bullpen resume Phase 1 from authorized source-byte materialization — retrieve exact registered bytes → fresh SHA-256 → ingest canonical owner paths → clean-context retrieval → corruption/swap tests → 12/12 acceptance.`

## Downstream state

- Phase 2 design may proceed independently once it treats Phase 1's byte contract as fixed.
- Phase 3 native reference mounting remains **BLOCKED BY PHASE 1**.
- Phases 4–12 that require real character rendering remain blocked transitively.
- No 12-character overview rebuild is authorized.
- No CCP v2 promotion is authorized.
