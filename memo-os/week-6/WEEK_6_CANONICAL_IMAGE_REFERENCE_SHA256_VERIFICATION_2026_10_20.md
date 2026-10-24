# Canonical Image Asset Byte Integrity / Reference-Binding Gate — 2026-10-20
**Source:** canonical Oct18 12-character lineup manifest, draft PR #222. **Procedure:** fetch all 12 individual image files using GitHub fetch_file encoding=base64; decode PNG bytes in-process and run SHA-256; compare against published manifest crop_sha256. Original bytes are not stored in this Markdown. 

| Character ID | Fetched PNG bytes | Calculated SHA-256 | Manifest match |
|---|---:|---|---|
| CHAR-JAKE-KALOPER | 320465 | `fe8ce76e267c4c0d8985b2f108b7384d928d3515704d93a20808480c438777e8` | PASS |
| CHAR-WILSON-LOOK | 336378 | `3404ccc361a218c42bb0f7ee65ebe90d2b4076c1240125300e93ca05df2a772f` | PASS |
| CHAR-PHILLIP-PITTS | 331140 | `0c6d6ee2cdd1c1f77c58cda2e5e25c0b482943279e433b16e14aa1277e201a65` | PASS |
| CHAR-AUSTIN-BYARS | 328843 | `e5600122b9a4c85684f968b17b27edafa0b75e9e161ad02ead8329e97794bce3` | PASS |
| CHAR-BRANDON-PRYOR | 230390 | `f12df5e269823726ffa99833d6207d5747f8ab2cfdeaa5c171fa5e8acf82093e` | PASS |
| CHAR-JORDAN-HOLLINGSHEAD | 237136 | `5b3ad2add4a73e224a666379920a53cd9d217afd11b39d9babad99ee17c1e515` | PASS |
| CHAR-ZACH-WILSON | 225523 | `c0ac1b3314c32b8e85c82045268c21a0d9c52525c2fd8ad869aaff449b4cf36a` | PASS |
| CHAR-KEVIN-ZEEK | 245679 | `53bcf61c8514173a35caf7fc3d8b65f4c04a28ac7f0d2e182cc1cce014621e3b` | PASS |
| CHAR-BOBBY-MITCHELL | 324719 | `d88f6ffdde967d0dee2ec350f0d9314f2e8b4da4dd9b8d8d1890bc28d6fae736` | PASS |
| CHAR-BEN-WHIPPLE | 313601 | `0cb352849ff671488948b2d5eea60f49f1e3aa6ee974369e34bc85afcb3abc2f` | PASS |
| CHAR-DAVID-BABB | 280004 | `f7fa692603289275c819dec2e5e1e09ea69bf33309c1bea1da0151a026b8f340` | PASS |
| CHAR-MANNING-WELTY | 322217 | `d9b7cf1c1ea18e8f4b615cb71471909dbede1cd8ebd4518e71e9437af7b05f04` | PASS |

**RESULT:** 12/12 exact byte-hash matches. This newly closes **REPOSITORY SOURCE INTEGRITY**. This does NOT mean image-reference media objects have been accepted by a particular image-generation provider. Provider mount requires a returned asset identifier/usable URL (not a guessed GitHub link), confirmation that the model receives it, and actual resulting likeness QA. No image rendering was performed.

**Camera packet regression:** every one of 23 current pre-render folios already includes an individualized `CINEMATOGRAPHY / UNIT-STILLS LAYER`, introduced in commit `722903b9b7b35e2cc54a5c5070528abe9e48161f`. The cover's camera direction depends on Blackwater II's actual accepted still, not an invented camera match. This is internal Masi-*informed* analysis only, not personal review by Frank Masi.

**Remaining real gate:** provider binding receipt for first two characters `CHAR-KEVIN-ZEEK` and `CHAR-WILSON-LOOK`; enforce the integrated gorilla-centaur (four attached equine legs), character QA, scene visual proof and independent Umpire acceptance at generation time. Source integrity is passed; binding remains HOLD pending actual accepted provider reference inputs.
