# Local Character Source-Byte Recovery — November 22, 2026

**Disposition: PARTIAL PRIVATE CUSTODY; PHASE 1 STILL HOLD.** This is an evidence checkpoint, not Canon promotion or renderer approval.

## Authorized zero-incremental-cost source search

The user's authorized Mac was searched by **exact source filename** against the 12 existing Commissioner-approved primary JPEG records in `planning/character-native-render/PHASE_1_SOURCE_BYTE_PORTABILITY_MATRIX_2026-10-01.json`. Only byte-for-byte SHA-256 matches with the approved hashes and file sizes were accepted.

- 12 current original-source records evaluated.
- **4/12** identical original JPEG sources found locally: CHAR-MANNING-WELTY, CHAR-BRANDON-PRYOR, CHAR-PHILLIP-PITTS, CHAR-AUSTIN-BYARS.
- **8/12** original sources not found through the indexed-file search; this is not proof they are absent from every possible authorized storage surface.
- A subsequent size-first, hash-confirming local search inspected **8,076 JPEG/PNG/WebP images** in the authorized AI workspace, Desktop and Downloads (excluding dependency caches and Git internals), with **zero matching-size candidate files for those eight expected originals**. This widens the documented search scope but **does not prove global absence** or justify reconstructing missing references.
- A fresh ChatGPT Library image-metadata listing found **12/12** original named records. An authorized original-byte materialization request for one of the eight still returned `This Project file does not have an authorized raw-byte materialization path.` Metadata presence is **not** binary custody; no authorization boundary was bypassed.
- The four matching originals were copied into a *local-only*, user-controlled, private character-source vault. Their repository-relative canonical paths are retained *inside the vault*, not this public repository.
- A new independent process ran the existing `canon/characters/runtime/primary_source_audit.py` over the private vault: **4 PRIMARY_BYTES_VERIFIED, 8 SOURCE_BYTES_REQUIRED, 0 PRIMARY_BYTES_MISMATCH**.
- A separate disposable-copy audit verified that **one-byte corruption and cross-character file substitution both produce `GENERATION_BLOCKED`**. The original four private source files were freshly rehashed before and after and remained unchanged; the private receipt is retained in the local vault. This proves the **4/12** fail-closed custody test only, not complete twelve-source recovery.
- The private vault retains a local receipt with exact SHA-256s; binaries and absolute user paths were intentionally excluded from this public candidate.

## Unchanged non-negotiable gates

- The 12/12 clean-context portability requirement is **not** met. Public GitHub has not received any of the private image bytes.
- Per-character primary asset binding, renderer attachment, output identity and independent final-raster QA are **not** proven.
- The verified four may support further **private source custody** integration experiments but do not authorize generating those characters.
- No supplementary lineup crop, inferred appearance, or generated image substitutes for missing original bytes.
- Existing `PHASE_1_SOURCE_BYTE_PORTABILITY_HOLD_2026-10-01.md` remains the controlling historical root blocker; this checkpoint records partial remediation without supersession.

## Next exact gate

Obtain the remaining eight original source files through already-authorized paths, perform 12/12 independent fresh-byte SHA verification in durable private custody, prove clean-context re-retrieval and corruption/swap rejection, and only then request independent Umpire review. Source files must not be silently committed to the public repository.

**Release status: HOLD.**
