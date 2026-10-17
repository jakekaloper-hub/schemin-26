# CHAR-PORT-002 — bounded recovery readback (2026-10-17)

**Authority:** Schemin '26 current Character Canon / reference_sources_v1.json and Bullpen #133.  
**Task:** `CHAR-PORT-002` on existing Execution Control registry.  
**Disposition:** IN_PROGRESS / PARTIAL GIT STORAGE 2/12 / 10/12 UNRECOVERED IN PRIMARY PATH. **Not a T15 or T16 acceptance.**

## Actions actually performed

1. Read the 12-item Commissioner-approved `canon/characters/reference_sources_v1.json` on `main`.
2. Queried the GitHub Contents endpoint for **all twelve exact** `canon/characters/assets/<CHAR-ID>/primary/` directories on `main` (2026-10-17).
3. Observed actual primary JPEG Git blobs for Austin Byars and Phillip Pitts; Git returned 404 for the other ten *primary directories*.
4. Listed the connected Library. Original named references, including Austin, Wilson, Bobby and Jake, remain indexed with previously recorded source sizes and file handles.
5. Attempted raw-byte materialization of the current Wilson and Austin original file IDs, plus a separately re-uploaded Austin file ID. **All three returned:** `This Project file does not have an authorized raw-byte materialization path.`
6. Attempted GitHub binary read through the connected GitHub blob endpoint; binary content was not returned as UTF-8. No fresh SHA-256 was calculated from retrieved bytes in this execution.

GitHub blobs, prior approval records, and Library metadata are valuable evidence **but are not current end-to-end raw-byte / SHA-256 / renderer-mount proof**. Do not backfill receipts.

## Per-character durable-storage readback

The expected SHA-256 below is copied from the existing controlling reference registry; it was **not recalculated today**. Sizes for all twelve are manifest/Library sizes; the two present binaries additionally match their observed GitHub metadata sizes.

| Immutable character ID | Expected primary filename | GitHub main primary path | Observed Git blob SHA-1 | Registered byte size | Approved expected SHA-256 | Gate |
|---|---|---|---|---:|---|---|
| CHAR-BOBBY-MITCHELL | `17E68E6F-7825-460F-A612-734BE1E2A543.jpeg` | 404 at primary path | — | 558760 | `4ad8693d7f155f2ee99722f87eb74ea99490eebdfe0b30ca2f17f05004e7cf12` | Binary ingestion BLOCKED |
| CHAR-BEN-WHIPPLE | `88B8E56B-8320-4524-8425-134FFAE8FBF5.jpeg` | 404 at primary path | — | 468673 | `c4401f79783637c9e3974f02de20ba5aeb1209e7ed4e0f5620e2bfcce3b270cf` | Binary ingestion BLOCKED |
| CHAR-KEVIN-ZEEK | `4369C44E-C5C8-46E9-B99F-04A97CEBEC13.jpeg` | 404 at primary path | — | 474768 | `df597e71aed77ddf510fd81f3fcd4ee812ac22b8f8e129e276dc5edfbd9dddc1` | Binary ingestion BLOCKED |
| CHAR-MANNING-WELTY | `2FA6D29A-5E4C-4CA1-9790-88BE5E75F14E.jpeg` | 404 at primary path | — | 520546 | `5e43eadf7ea6426ea8ba2c3af80c108714638625db5adc9d5a32492ff84fc965` | Binary ingestion BLOCKED |
| CHAR-DAVID-BABB | `A6F3AA99-CDB1-4265-AB08-3728117089A3.jpeg` | 404 at primary path | — | 413410 | `ce3137d1472d63deb7a026d114d200f338d2461d3d223647f34b473794e1f85b` | Binary ingestion BLOCKED |
| CHAR-ZACH-WILSON | `5B8C182F-FEBF-40A3-8DDA-1B4B62386B10.jpeg` | 404 at primary path | — | 508338 | `c8124a1f1146c0acc65b5e82d1c21289afd6a74a8ac2046895e39794619dcefb` | Binary ingestion BLOCKED |
| CHAR-JAKE-KALOPER | `73B4BF07-22E9-44CA-BCBB-882612DFA9C1.jpeg` | 404 at primary path | — | 765962 | `e9b6690899566864fc9d56b3bc9dbce0e1eb43a2901d23c0949170be4da91e58` | Binary ingestion BLOCKED |
| CHAR-BRANDON-PRYOR | `76344FB3-1974-48D0-AA90-8B231E6008F7.jpeg` | 404 at primary path | — | 767855 | `0bb99794f3a0b9fa1a7f791e17e6885fffcca4b79c824057623bab5c74598cfe` | Binary ingestion BLOCKED |
| CHAR-JORDAN-HOLLINGSHEAD | `0435E914-64B3-4350-8A41-758173DDC98D.jpeg` | 404 at primary path | — | 481355 | `c052e8c74939338517f1b14bbca5f2ea3d57146794f675d065698a44fb1064e8` | Binary ingestion BLOCKED |
| CHAR-WILSON-LOOK | `IMG_7866(1).jpeg` | 404 at primary path | — | 810974 | `d6279c5ca904c20de1e5800490d1fed42aa24c8674d051654b29838291459a10` | Binary ingestion BLOCKED |
| CHAR-PHILLIP-PITTS | `IMG_2178.jpeg` | PRESENT on main | `61065d0ee5dbffb750da9aeea3f64e664f38a1be` | 200005 | `31b9d7be295ba662b1332897ef7c33e2f64e92aeefb2d6abe625c08bac914c0c` | Stored; independent current SHA-256 and renderer mount not proven |
| CHAR-AUSTIN-BYARS | `IMG_2179.jpeg` | PRESENT on main | `aa7e51ab08a31e6595c9c19d5eab67fb107d8dda` | 238145 | `eedfaaf0b2e2dd78a7a32e11aef333cab41278c206b65ec78c4aa4f1fd2c4f76` | Stored; independent current SHA-256 and renderer mount not proven |

For each row, the exact target path is the existing manifest's `repository_path`; no new location scheme was created.

## Important correction to historical blocker

Earlier Bullpen #133 said Austin's primary path was 404 when checked. **That condition is no longer true in the 2026-10-17 main readback.** Phillip Pitts's binary is also present. Do not overwrite or re-upload either binary without hash-authority reconciliation.

## Remaining steps, in dependency order

1. Resolve the ten inaccessible exact approved binary sources from an **authorized source that actually exposes raw bytes**. Existing user-supplied Library identities are known; do not ask for a generic twelve-file re-upload. Try existing durable Git objects/branches, accessible prior conversation backing files, authorized asset connectors or existing recovery artifacts before escalating.
2. For all twelve, read the exact bytes afresh, recompute SHA-256, compare to expected approved hash, record stable Git blob/byte size/locator and fail-closed mismatch behavior. Any divergent encoded export requires explicit Commissioner supersession rather than silent replacement.
3. Demonstrate clean-context retrieval, renderer mount hashes and per-character subject-slot binding using actual supported provider receipts. Native image references alone do not establish deterministic binding.
4. Run C1 per-character crop/QA. Only after C1 PASS expand to multi-character adverse tests, T15 Umpire acceptance and T16 release certification.

## Release and QA verdict

- **IMPLEMENTED:** bounded Git main readback, Library identity lookup and negative raw-byte export tests, recorded here.
- **TESTED:** GitHub 12/12 path probes, three materialization attempts; no successful binary rehash or provider mount test.
- **AUDITED:** evidence-limited review in this run; **independent Umpire NOT invoked/authenticated**.
- **PROMOTED:** nothing. This is a draft review artifact.
- **BLOCKED:** ten raw-byte transports; all twelve current-session hash/mount/subject-binding proofs; T15 and T16.
- **REMAINING_EXTERNAL_INPUT_REQUIRED:** authorized raw-byte-capable retrieval path or tool access for already supplied files, only if internal recovery avenues remain unavailable; **not another generic content upload**.

No character-bearing artwork was generated.
