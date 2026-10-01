# V5.6 Current-Main Salvage — Final Acceptance

**Date:** 2026-10-01
**Status:** PASS FOR CONTROL SALVAGE / V5.6 PROMOTION HOLD

## Accepted into current main

The following publication-integrity controls may be merged beneath V5.5:
- Page Production Contract;
- Publication Fidelity Contract;
- Page Fidelity Model;
- Generation Intent Firewall;
- Character Packet Gate;
- Reference Mount Receipt;
- Renderer-Addressable Asset Contract;
- Runtime Bootstrap Resolver;
- World / Encounter Binding.

## Version authority

**V5.5 remains ACTIVE.**
**V5.6 remains RELEASE_CANDIDATE / NOT ACTIVE.**

Merging these controls is not a version promotion.

## Release architecture

The proposed Memo-local release registry is superseded.

Canonical architecture:
- Publication Manifest V1 = derived publication identity / relationships;
- Release Evidence = machine release / acceptance evidence;
- owning Memo release gate = actual publication authorization.

## Exact-byte repair

The recorded Week 4 ObiWan technical fixture was reloaded from its durable Creative Claw asset and independently hashed:

- asset ID: `97a316c2-aa34-46cc-b088-442d0c6868a4`
- byte count: `253543`
- SHA-256: `4aba1fe41e8fc2c1e5ff247d02e7fcc69ffe7a72c7650782f8308fc7c61f654a`

This repairs the fixture identity defect only.

## Remaining promotion blockers

1. Week 4 real-page publication fidelity: **FAIL**.
2. Controlled Week 2 reconstruction under current-main V5.6 candidate: **MISSING**.
3. Exact canonical `Week 2 memo.pdf` bytes for exact-binary comparison: **SOURCE_BYTES_REQUIRED**.
4. Independent release audit: **BLOCKED** on the above.

Accessible repository and Project/Library searches did not expose the canonical Week 2 PDF bytes. Supporting Week 2 evidence and a PNG overview exist, but they are not substitutes for the canonical PDF binary.

## Verification

Receipt-predecessor candidate passed:
- Repository Merge Gate #149 — PASS
- Bullpen Runtime CI #2803 — PASS
- Week 4 Preproduction CI #100 — PASS
- Schemin Project Mission CI #114 — PASS

## Umpire ruling

**PASS FOR SALVAGE / HOLD PROMOTION.**

No current evidence supports V5.6 activation.

## Architect ruling

**PASS.**

The salvage reduces duplication by retiring the proposed Memo-local release registry and reusing current publication/release authority.

## Post-merge disposition

Close PR #38 as superseded by this targeted current-main salvage. Preserve PR #38 only as historical engineering/provenance evidence.
