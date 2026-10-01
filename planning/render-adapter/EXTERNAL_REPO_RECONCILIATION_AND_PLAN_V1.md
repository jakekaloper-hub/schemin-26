# External Repository Reconciliation + Integration Plan V1

**Status:** RESEARCH / PLAN / TEST COMPLETE FOR CONTRACT LAYER  
**Date:** 2026-09-30  
**Production dependencies installed:** NONE

## 1. Reconciliation findings

### Existing Schemin capability that must be reused
- Memo OS V5.5 already owns full-issue previsualization, page packets and page-state gates.
- Week 4 already has Issue Previs Board + Page Packet Register.
- Character Control Plane v2 already has typed records, asset references, immutable render contracts, QA and fail-closed `render_ready`; it remains RELEASE_CANDIDATE / NOT ACTIVE because durable canonical image bytes are not yet portable.
- World Engine V1.1 + Location Control Plane already own geography and world packets.
- Phase 3 environment references already provide 23 renderer-addressable structural plates.
- Chronicle/Living Novel already own historical/narrative continuity.
- Interactive Atlas already exists as a read-only canonical visualization.

### Therefore not selected
- no AIComicBuilder-style second storyboard database;
- no TimelineJS history database;
- no OpenStoryline script authority;
- no Remotion-owned story state;
- no Vizzu-owned league state;
- no Albino-derived reader implementation.

## 2. Character integration research

**Pattern source:** AIComicBuilder.

Adopt as pattern:
- explicit mounted reference assets;
- multi-view/turnaround coverage when human-approved;
- reference-to-character assignment validation;
- downstream generation must not reinterpret identity.

Existing upstream blocker:
- CCP G1 durable bytes + fresh-context renderer injection smoke test.

Decision:
- do not create new character sheets until canonical source bytes are durable and renderer injection is proven;
- when/if turnaround sheets are created, they are candidate supplemental assets until identity QA + Jake approval promotes them.

Test target:
- every depicted character packet must be ACTIVE, render-ready and contain renderer-addressable reference assets.

## 3. Data Story integration research

**Pattern source:** Vizzu.

Candidate use:
- Pittsy's Book cumulative results;
- standings progression;
- weekly scoring arcs;
- H2H history;
- FAAB/waiver spend.

Contract law:
- deterministic read-only payload;
- source receipts;
- explicit field definitions/units;
- DO_NOT_INFER missing values;
- data renderer may animate perspective, not alter values.

First future spike:
- use one closed historical dataset, not live Week 4 production;
- compare manual graphic time, value parity and mobile readability;
- only then decide whether Vizzu itself is needed.

## 4. Motion integration research

**Pattern sources:** Remotion + OpenStoryline + VoiceStudio.

Capability decomposition:
- deterministic composition/rendering role: Remotion-like;
- conversational revision/session role: OpenStoryline-like;
- optional narration/dubbing role: VoiceStudio-like.

No dependency decision has been made.

Before any install:
1. verify local Mac runtime/hardware fit;
2. review Remotion license eligibility;
3. review OpenStoryline service/model credential surface;
4. review VoiceStudio AGPL + model licenses + voice consent;
5. prove the same Render Request can feed a stub renderer;
6. define artifact storage/provenance/rollback;
7. measure whether motion is valuable enough to justify operating cost.

## 5. Timeline / interactive reader

TimelineJS3 remains reference-only. Albino interaction patterns remain learn-only.

Reason: Schemin already owns Chronicle history and an Interactive Atlas. Reader enhancement is not the highest current bottleneck.

## 6. Acceptance result for this strengthen cycle

PASS if:
- external research is reconciled against existing systems instead of duplicating them;
- one shared request shape covers Character-Grounded Static, Data Story and Motion;
- fail-closed tests prove authority cannot be mutated;
- no external dependency is installed or marked active;
- future work is sequenced behind existing CCP/World/Memo gates.

Current result: **contract-layer PASS; production integration NOT AUTHORIZED.**
