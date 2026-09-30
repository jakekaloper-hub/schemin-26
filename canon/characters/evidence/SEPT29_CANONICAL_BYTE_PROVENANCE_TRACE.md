# SEPT29 CANONICAL BYTE PROVENANCE TRACE

date: 2026-09-30
status: PARTIALLY_RECONSTRUCTED_FROM_REPOSITORY_EVIDENCE

## Proven chain
1. Commit `97786aa18db584eabbd150900e97432849b13b5e` at 2026-09-29T17:22:58Z recorded "Recovery A normalize CCP v2 governance and evidence".
2. Commit `58d8c0f14ef37bc5ff52af94d18a6e4874561c5d` at 2026-09-29T17:23:37Z, 39 seconds later, added `evidence/R4_SOURCE_BYTE_HASH_RECEIPT_2026-09-29.md`.
3. That receipt states exact source bytes were present under `/mnt/data` in the active execution container and SHA-256 matched the Commissioner Reference Register 12/12.
4. Commit `9961f1bc242fa4930d2807360f128af8b7a31311` at 2026-09-29T17:23:41Z recorded Recovery A PASS while explicitly retaining dependency holds.

## What the repository does NOT prove
The receipt does not identify the exact /mnt/data filenames, mount provider, conversation ID, Project/Library origin, extraction process, or a durable asset URI. No image binaries were committed with the receipt. Therefore those details remain UNKNOWN and must not be inferred.

## Current recovery result
- Historical source identity bytes: PROVEN / SHA PASS 12_OF_12.
- Durable canonical storage: NOT PROVEN.
- Fresh-context retrieval: NOT PROVEN.
- Renderer addressability: NOT PROVEN.
- Reference mount: NOT PROVEN.

## Incident conclusion
Current unavailability cannot be interpreted as evidence that the Commissioner failed to supply canon. The observed defect is loss of durable renderer-addressable persistence after successful source-byte verification.
