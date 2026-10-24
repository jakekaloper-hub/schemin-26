# Week 6 character reference — Pre-Umpire verification handoff

**Disposition: BLOCKED BEFORE INDEPENDENT UMPIRE. DO NOT PROMOTE.**

## Proven
- Commissioner final source: `Schemin_26_Week_6_Memo.pdf`, SHA256 `1d9b1b6915bf4b757a927c33719ab1cbd9f8f8eb93523e8103d3d8e2bd1a61c8`.
- 23 flattened embedded image masters extracted and independently rehashed (23/23); each 1024×1536. 12 unique canonical IDs checked.
- Candidate PDF pages and expected hashes tracked in externally packaged `Week6_Character_Reference_Candidates.zip`. Candidate register exists in this branch.
- This registry is identity-preserving: no original portraits or Character Registry entries changed.

## Attempted binary persistence routes
- Local container `git ls-remote` to GitHub: DNS/network unavailable.
- GitHub integration exposes binary-capable `create_blob`, but cannot read local filesystem bytes directly. No verified path in this session to transfer the locally extracted binary images to the integration.
- Authorized Desktop Commander Mac is online, but the specific Week 6 PDF and extracted ZIP are not present in expected Downloads paths; no binary staging succeeded.

## Mandatory gates still HOLD (in order)
1. Copy original 23 extracted embedded JPEGs (or an approved 12-character selection) **as byte-identical files** into existing `canon/characters/assets` under versioned Week 6 references. Do not commit pointer-only substitutes. Require Git SHA/blob plus fresh SHA-256.
2. Prove clean-context retrieval of actual image bytes from GitHub, with hash equality to the extraction register.
3. Retrieve original approved character portraits and conduct side-by-side identity audit, documenting per-subject anatomy, costume, accessories, and unacceptable deviations. El Niño Week 6 visual is weather-only.
4. Run the actual image renderer with original + preferred Week 6 image bytes attached and correct subject-ID binding. Record input file hashes and returned raster.
5. Run controlled pose/light/multiple-character regression and compare the *pixels*, especially DK's four integrated legs, TDS three attached heads, Slob/ObiWan human forms, and Blood's Belt.
6. Provide a review package for Independent Umpire. Only an authenticated independent review may promote per-character references to ACTIVE.

## Release assertion
Local byte verification is PASSED; source-to-Git portability, reference mounting, pixel fidelity, and independent Umpire are NOT PASSED. Any claim to the contrary is false-green. No promotion is authorized on this evidence.