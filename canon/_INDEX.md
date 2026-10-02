# Canon — Index

**Authority:** Character Canon / explicit commissioner-approved changes

## Load order

1. latest explicit Commissioner-approved character correction recorded in current canon
2. `SCHEMIN_26_MASTER_CHARACTER_CANON.md`
3. `characters/CHARACTER_REGISTRY.yaml`
4. `CHARACTER_REFERENCE_LAYER_V1.md`
5. `league.json`
6. `character-control-plane-v2/README.md` — **release-candidate architecture only; NOT active runtime authority until release gates close**

## Governing rule

```text
OWNER
→ CANONICAL CHARACTER
→ CURRENT ESPN TEAM NAME
```

Team names can change. Character identity does not change unless explicitly approved.

The current master character canon plus current owner-scoped registry/reference controls are binding for visual production.

## Current high-risk corrections

- Wilson Look / Donkey Kong: **Arsenal Gorilla Centaur Warrior**, Commissioner-corrected 2026-10-02. ONE BODY: gorilla head/upper warrior identity + four-legged centaur lower body + Arsenal supporter identity. The 2026-09-29 `centaur retired` interpretation was erroneous and is superseded.
- Phillip Pitts / Three Dreaded Snake: **one reptilian humanoid body with exactly three serpent heads**.
- Jake Kaloper / ObiWan Jacoby: **The Trade Jedi — NO championship belt**.
- Brandon Pryor / Chili Cheesers: **The Chili Outlaw + The Dark Horse**.
- Team renames do not redesign characters.

## Character Control Plane v2

`character-control-plane-v2/` is the typed successor architecture. Current status: **RELEASE_CANDIDATE / NOT ACTIVE**.

It may be used for migration, testing, shadow reconciliation and release preparation, but no consumer may treat it as promoted runtime authority until its R15 release conditions and Commissioner promotion are satisfied.


## Fail-closed character generation boundary

The executable enforcement layer under `canon/characters/runtime/` is **ACTIVE as a safety boundary** once present on `main`.

It does **not** promote Character Control Plane v2 and does **not** mean character rendering is production-ready.

For any character-bearing generation, semantic canon resolution alone is insufficient. Production requires:

`APPROVED ASSET → VERIFIED HASH → MOUNT RECEIPT → SUBJECT BINDING → CAPABILITY VERIFIED → SIGNED GENERATION_ELIGIBLE → GOVERNED RENDER → OUTPUT INSTANCE → INDEPENDENT CHARACTER QA`

If any element is absent, generation state is `GENERATION_BLOCKED`.

Current exact-reference durable retrieval and real provider subject-binding evidence remain separate production gates.


## Character source-byte portability mission

Current fail-closed evidence surfaces:
- `characters/reference_sources_v1.json` — 12 approved source expectations and durable target paths.
- `characters/renderer_capabilities_v1.json` — provider capability evidence; unproven routes remain blocked.
- `characters/runtime/source_byte_integrity.py` — exact repository-byte SHA-256 / Git-blob verification.
- `characters/*/REFERENCE_MANIFEST.yaml` — owner-scoped portability state.
- `characters/runtime/reference_mount.py` — request-bound mount + subject-binding receipt contract.

**Current corrected disposition (2026-10-01 Librarian reconciliation):** source acquisition is **not** the missing Commissioner input. Recovery evidence records 12/12 uploaded raw bytes materialized, 12/12 current approved hashes resolved, and 12/12 identity mappings resolved. The open gates are **durable fresh-context binary retrieval / durable asset ingestion** and **deterministic provider reference-to-subject binding**. Do not request another bulk re-upload of the Twelve merely to address those transport/runtime gates. See `../bullpen/LIBRARIAN_THREAD_CLOSEOUT_CHARACTER_PORTABILITY_2026-10-01.md`.
