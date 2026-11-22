# Raster Integrity Preflight — November 22, 2026

**State: implemented and locally tested; NOT image generation, character QA, editorial acceptance, or publication authorization.**

## Existing pipeline and ownership

The canonical `CHRONICLE_SPREAD_PIPELINE` still declares `art_job → characterVisionGate → composition → renderGate → final_qa`. These gates may not be replaced by a generic PNG dimensions check. `src/raster-preflight.js` is a replaceable, deterministic **technical inspection helper** for already-produced PNG bytes.

Its explicit inputs are the trusted root, relative asset path, independently recorded expected SHA-256, and contract dimensions (default **1080 × 1920** for portrait page masters). Before it returns `RASTER_PREFLIGHT_PASSED`, it checks:
- in-root regular file with no symlink/traversal and a bounded file size;
- exact PNG SHA-256 matches the caller's separately sourced expected hash;
- PNG signature, chunk lengths, CRC32, IHDR, IDAT, IEND and actual zlib scanline completeness;
- the expected pixel width and height, 8-bit non-interlaced standard grayscale/RGB/RGBA encodings.

Unsupported or ambiguous formats fail closed. The result ALWAYS declares `character_qa_approved:false`, `editorial_qa_approved:false`, and `publication_eligible:false`. It cannot certify subject identity, textual accuracy, visual composition, reference bindings or canonical geography.

## Test-first implementation and real source inspection

- Test was first run before implementation and failed with missing source module.
- **5/5 new raster-preflight tests PASS:** exact normal PNG, wrong geometry, changed hash / broken PNG, unsafe/missing/symlink paths, forged IHDR-only content.
- Entire `bullpen-runtime` suite after implementation: **33/33 PASS**.
- Existing Week 9 storyboard PNG `memo-os/week-9/storyboards/W09_GOTW_PAGE_TURN_P05_PHONE.png` from the authorized local Schemin worktree was inspected as a **technical-only** real-file canary: **390 × 1100**, original file SHA-256 `34dc1b1eb8e80c809277ebf21b558877b7e2e79fff825513b1291a52cc757533`, 119,068 bytes. Technical raster integrity PASSED; all publication/character flags remain false.
- When checked against the **default current 1080 × 1920 portrait contract**, this real historical storyboard correctly returned `RASTER_PREFLIGHT_BLOCKED / GEOMETRY_MISMATCH`. It is not a certified finished page. Computing the inspection digest from the file itself proves repeatable current-byte inspection, **not prior approval**; in a production packet, `expectedSha256` must come from an independent authoritative asset receipt.

## Remaining true production gaps

Real image-generation workers, externally authenticated invocation, explicit character-source attachment/slot-binding, independent visual inspection, page-lock receipts, and whole-issue release remain unresolved. Do not install this technical preflight in place of any independent gate or promote `art_job` as PASSED by itself.
