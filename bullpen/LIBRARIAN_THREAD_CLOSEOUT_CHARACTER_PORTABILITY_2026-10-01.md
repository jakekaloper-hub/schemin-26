# Librarian Thread Closeout — Character Reference Portability Trust Incident

**Date:** 2026-10-01  
**Authority:** Librarian / Commissioner correction  
**Thread state:** CLOSED  
**Scope:** Character-reference portability, renderer-binding, repeated source-upload requests, and resulting trust failure.

## Why this closeout exists

This thread must not be resumed as if source acquisition were still unresolved.

The Commissioner explicitly stated that the twelve current character references had already been supplied repeatedly, including twice on 2026-10-01. Repository-adjacent recovery evidence independently confirms:

- current uploaded bytes materialized: **12/12**;
- character identity mapping: **12/12**;
- current approved hashes established: **12/12**;
- TDS and His Majesty's Blood matched prior canonical hashes exactly;
- ten re-uploaded files used different encodings/exports and were Commissioner-promoted as the current approved reference bytes;
- a real renderer accepted all twelve supplied references, but the resulting raster was rejected because reference presence did not prove reference-to-subject control.

The assistant repeatedly reverted to an older `SOURCE_BYTES_REQUIRED` framing and asked for the twelve images again. That was a retrieval/state-reconciliation failure and caused loss of user trust in this thread.

## Corrected authoritative distinction

### COMPLETE — do not ask the Commissioner to repeat this work

- 12/12 current character references have been re-uploaded.
- 12/12 uploaded raw bytes were materialized in the recovery cycle.
- 12/12 current approved character hashes were resolved.
- 12/12 character identity mappings were resolved.
- The existing supplied references remain the intended current source set unless the Commissioner explicitly changes canon.

**Operational rule:** Do not request another bulk re-upload of the Twelve merely because durable repository retrieval remains open.

A new upload request is allowed only if:
1. the Commissioner explicitly replaces a canonical reference; or
2. verified storage loss means a specific exact source can no longer be recovered by any authorized existing source.

In case (2), identify the exact missing Character ID/file first. Never issue a generic “upload all twelve again” request.

### OPEN — actual remaining engineering problem

- durable repository/asset-store ingestion of the already-established approved bytes;
- stable durable locators;
- fresh-context retrieval independent of conversation-local state;
- repository-backed SHA/hash/blob receipts;
- renderer mount proof;
- deterministic reference-to-subject binding;
- single-character C1 benchmarks before increasing cardinality;
- independent Character QA;
- multi-character contamination testing;
- later T15 acceptance.

## Renderer incident learning

The first twelve-character renderer proof is diagnostic evidence, not a successful character render.

Observed result:
- renderer reference attachment: OBSERVED;
- reference-to-subject binding: NOT PROVEN;
- first ensemble Character QA: **0/12 PASS**;
- first raster: REJECTED;
- native twelve-character route: NOT AUTHORIZED.

Root cause:

`REFERENCE PRESENCE != REFERENCE CONTROL`

The missing proof chain remains:

`REFERENCE HASH → CHARACTER ID → SUBJECT SLOT → BODY/FACE/FORM LOCK → OUTPUT INSTANCE → QA CROP`

Do not jump from available references directly to another twelve-character generation.

## Correct future resume point

Do not restart discovery.

Do not restart source acquisition.

Do not ask for all twelve references again.

Resume at:

**existing 12/12 materialized approved source bytes → durable asset ingestion/retrieval → fresh-context verification → C1 single-character reference-binding benchmarks → explicit PASS/FAIL evidence → only then increase subject cardinality**

Recommended future command:

`/bullpen resume character-reference portability from verified 12/12 materialized source bytes — close durable retrieval and C1 binding benchmarks; do not request re-upload`

## Trust-recovery operating rule

When a user says work has already been supplied, completed, uploaded, approved, or tested:

1. reconcile current repository truth;
2. search existing Project/Library/handoff evidence;
3. distinguish storage/transport failure from missing user input;
4. do not make the user reproduce work until evidence proves the input itself is actually unavailable.

A transport-layer defect must not be misreported as a Commissioner-input defect.

## Thread disposition

This conversation thread is CLOSED.

No further character-reference production work should continue from this conversational state.

Future work must start from repository/runtime truth plus this Librarian closeout, not from the stale repeated-upload loop.
