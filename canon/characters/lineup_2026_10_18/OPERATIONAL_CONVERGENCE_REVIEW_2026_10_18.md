# Character canon operational convergence: G0–G7 evidence

**Scope:** Existing Schemin 26 canon, the approved October 18 lineup, and current Memo/Novel/World runtime adapters. No new OS. Approved lineup SHA-256: 24cd6adf9654e598c97a6588afc07603d5adcc40c276eba07e7c86c0d438e7b2.

## G0: post-merge authority
Commissioner-approved lineup merged to main as PR #201, 456a7cd. The master image and original twelve hashed crops remain unchanged; HMB correction present. The old bipedal DK registered source remains quarantined by merged PR #197. Historical primary source hashes are not replaced.

**Governance exception:** PR #201 was merged without a recorded independent GitHub review. This fact is not retrospectively waived by simulated Umpire deliberation.

## G1: candidate-only trimmed portrait derivatives
Twelve additional images were produced from approved pixels using macOS CoreGraphics rectangular selection and PNG re-encoding, without recomposition, inpainting, or regenerated characters. The precise coordinates, master lineage and hashes are in NAMEPLATE_TRIMMED_DERIVATIVES_2026_10_18.json. Two independent regenerations reproduced all twelve PNG hashes (NAMEPLATE_TRIMMED_REPLAY_RECEIPT_2026_10_18.json).

**FAIL-CLOSED ISOLATION LIMIT:** These are not full background-free subjects. Scenery remains, shared title artwork is visible in parts of first-row images, and cropping can remove lower limbs or equipment. All twelve are ISOLATION_QA_HOLD and NOT production reference seeds. The earlier 12 approved panel crops and the approved complete lineup remain the accepted comparison baseline. Further identity-preserving segmentation requires explicit visual QA; no automatic source-version promotion.

## G2/G3: actual existing runtime consumers
The following existing production-facing functions now call the approved visual resolver and expose anatomical constraints and existing spatial anchors:
- Memo LCP: world/location-control-plane/adapters/memo_adapter.py:compile_memo_location_packet
- Novel LCP: world/location-control-plane/adapters/novel_adapter.py:compile_novel_location_packet
- Visual World Packet: world/production/build_visual_world_packet.py:build_packet
- Novel visual compiler: living-novel/os/adapters/comfyui_adapter.py:compile_job when explicit immutable character_ids and location_id are supplied.

All compare authoritative character IDs to actual homeland/location/domain records, reject tampered or unknown identities and mismatched geography, and provide verified appearance only. No new location, distance, body measurement or travel fact is inferred from imagery. Numeric movement, heights and collision geometry remain UNKNOWN.

Character-bearing NovelVisualJob currently returns COMPILED_UNRENDERED_CHARACTER_PROVIDER_QA_HOLD. Environment-only legacy jobs retain their historical behavior. The Memo adapter is a callable LCP entrypoint, not proof that every downstream Memo UI scheduler has adopted it.

## G4: seven canary preparations, zero image outputs
world/location-control-plane/evidence/LINEUP_RUNTIME_CANARY_AUDIT_2026_10_18.json records actual function invocations for A DK; B HMB; C ObiWan; D TDS; E all 12 singles; F an all-owner central scene; G Red Leopards vs DK at the canonical LOC-RED-RUINS venue.

All semantic preparations passed. **Zero external image-generation requests were submitted; zero generated outputs were evaluated.** Existing renderer capability registry reports PROVIDER_CAPABILITY_BLOCKED because it exposes neither mounted-byte hash receipts nor deterministic per-subject binding receipts. Provider-native visual canaries, multi-character identity evaluation, C1, T15, T16 all remain HOLD.

## G5/G6: independent acceptance and release
Run character-provenance, pixel crop, LCP, visual world packet, Novel adapter and World Engine regressions and the full repository merge gate. Require independent authenticated reviewer approval on actual PR changes before merging any safe code/data scope. No simulated director/Umpire comment constitutes such approval.

Safe review candidates: character visual runtime context integration and deterministic cropped assets explicitly classified as QA HOLD. Unsafe for production: all pixel-only derivatives as authoritative clean cutouts; outdated DK primary; provider rendering, C1/T15/T16 and historical JPEG version migration (remaining on draft PR #195).

## Remaining external inputs
1. A supported provider mechanism that can prove genuine owner-specific reference conditioning or Commissioner/Umpire-approved equivalent evidence.
2. Real generated canaries and independent identity/contamination review.
3. Audited background/subject isolation if truly clean full-body refs are required.
4. Authenticated independent PR approval.
