# Frank Masi — Motion Picture Unit-Stills Reference V1

**Status:** PROPOSED / IMPLEMENTED ON FEATURE BRANCH / NOT PROMOTED
**Owner:** Existing Cinematography Director; no new director, OS, or personal affiliation.
**Applies to:** Weekly Memo OS, Novel OS illustration briefs, promotion art, future cinematic adaptations.
**Priority:** Tier 1 reference for story-bearing single-frame imagery; advisory, never above Commissioner intent, verified sports facts, character canon, Atlas, or release gates.

## Documented external evidence (not a personal endorsement)

- The Society of Camera Operators lists Frank Masi as its **2020 Lifetime Achievement — Still Photographer** honoree: https://socawards.com/2020-soc-awards/
- In a 2020 first-person interview Masi describes decades of motion picture unit-stills practice, action-film work, a preference for composing through the viewfinder rather than cropping afterward, and the importance of developing an individual visual style: https://www.blackrapid.com/blackrapid-spotlight-frank-masi/
- A published industry interview describes Masi's challenge of working close to principal motion-picture photography where lighting designed for the principal camera may not work from an offset stills-camera position. This is contextual source evidence, not a Schemin-specific recommendation: https://www.yahoo.com/entertainment/still-photographers-movie-sets-adapt-154025861.html
- External research is a reference only. Neither Masi nor the SOC has worked with, reviewed, authorized, or endorsed Schemin '26.

## Bullpen-derived translations (NOT attributed to Masi)

1. **Decisive instant:** the author identifies a specific verifiable or explicitly fictionalized action beat. Prefer a meaningful in-progress instant to an unfocused action tableau.
2. **Viewfinder-first composition:** decide crop, optical axis, character occupancy, and text-safe margins before rendering. Do not depend on destructive downstream cropping to rescue layout.
3. **Lighting-aware position:** verify facial readability, silhouette, obstruction, flare, and world-motivated light from the proposed virtual camera, rather than assuming a light setup works from any angle.
4. **Invisible witness:** choose an in-world plausible observational position unless expressive/cinematic subjectivity is deliberately stated.
5. **Sequence coherence:** ensure the frame's visual state is consistent with adjacent panels, action timing, and continuity.
6. **One-image readability:** the visual must communicate subject, relationship, moment, and intended emotion without needing factual captions, while approved type remains deterministic and separate.

## Routing and thresholds

- **Tier 1 / mandatory desk consultation:** covers, decisive matchup beats, action, character turning points, scene-to-trailer key art, single-panel cinematic climaxes.
- **Tier 2 / situational:** portraits, environment establishing stills, quieter dialogue, marketing assets.
- **Tier 3 / optional:** tabular standings, purely typographic or statistical layouts.
- Tier 1 means **mandatory review**, not Masi's personal involvement and not automatic approval. The existing Cinematography Director owns shot selection. The Art Director integrates typography and design. Character Canon and Atlas owners retain hard vetoes. The independent Umpire owns final audit with existing release authorities.

## Input contract (additive to existing packets)

Use existing Memo OS visual briefs / NovelVisualJob; *do not replace* their schemas. Where supported place these keys under an additive `unit_stills_review` object or equivalent metadata:

```yaml
unit_stills_review:
  reference_id: frank-masi-unit-stills-v1
  consultation_tier: 1
  beat_id: REQUIRED
  beat_evidence_class: FACT|JAKE_CONTEXT|INFERENCE|STORY|FICTIONALIZATION
  decisive_instant: REQUIRED
  emotional_objective: REQUIRED
  camera_role: REQUIRED
  camera_position_and_axis: REQUIRED
  virtual_shot_scale_and_perspective: REQUIRED
  foreground_midground_background: REQUIRED
  motivated_light_and_shadow_check: REQUIRED
  character_pose_silhouette_readability: REQUIRED
  action_and_occlusion_check: REQUIRED
  text_safe_region: REQUIRED
  atlas_location_and_horizon_lock: REQUIRED
  character_reference_and_negative_locks: REQUIRED_IF_CHARACTER
  continuity_in_out: REQUIRED
  alternative_composition_reason: OPTIONAL
  reviewer: REQUIRED
  review_status: PASS|REVISE|BLOCK|NOT_RUN
  evidence_links: []
```

No numeric focal-length prescription without an explicit artistic/technical rationale. A 'camera' does not authorize new terrain, wardrobe, props, owner identity, game outcome, or league evidence.

## Mandatory checks

**MS-01 — authority:** packet carries current story fact status and resolves to current authoritative production controls.
**MS-02 — instant:** subject/action/emotion are identifiable without caption.
**MS-03 — optics:** camera axis, subject occupancy, obstructions and text-safe regions are feasible for intended aspect ratio.
**MS-04 — illumination:** light plausibly originates in scene; key action/identity remain legible.
**MS-05 — hard canon:** immutable character source, body locks, Atlas horizon, route, object states pass existing checks.
**MS-06 — continuity:** predecessor and next-page story/camera progression are coherent.
**MS-07 — comparison:** for a controlled Tier-1 validation, compare current packet to enriched packet with same canon/beat/aspect ratio and score storytelling, mobile hierarchy, character accuracy, geographic accuracy, and typography room.
**MS-08 — provenance:** human review and output receipts required before describing a comparison or production render as tested.
**MS-09 — no attribution:** never imply Masi's participation or approval.

Failure of MS-05 is BLOCK regardless of photographic quality. Absent actual renderer reference binding remains an existing character-production HOLD, not something this desk may bypass.

## Existing integration surfaces

- `memo-os/WEEK_3_EXTERNAL_PRODUCTION_ADVISORY_PASS_V1.md`: historical prior advisory approach, not replaced.
- `memo-os/WEEK_3_BULLPEN_PREPRODUCTION_WAR_ROOM_MASTER_PROMPT_V1.md`: existing Cinematography Director role.
- `memo-os/week-3/WEEK_3_DAILIES_QA_BOARD_V1.md`: QA questions extended conceptually, not retroactively rewritten.
- `world/production/VISUAL_WORLD_PACKET_SCHEMA_V2.md`: authoritative geography and horizon constraints.
- `living-novel/os/VISUAL_RENDERER_ADAPTER_CONTRACT_V1.md`: use existing `camera_spec`, `lighting_spec`, `composition_map`, locks and `qa_contract`; do not change required renderer contract.
- `PROJECT_CONTROL_REGISTRY.md`: top-level authority and unchanged release blockers.

## Simulated preflight review — NOT a render test

Use an approved existing matchup scene as a comparison fixture only after current page packet, character bytes/reference route, and Atlas location are resolved. Evaluate baseline and enriched compositions with identical story/canon conditions; capture prompts, rendered artifacts and independent QA receipts. Do not invent PASS results.

## Promotion gate

Feature-branch documentation is not production activation. Require schema/packet integration evidence, automated validators where applicable, actual A/B render receipts, Umpire signoff and current release control before merge/promotion. Any failing or unavailable gate is HOLD.
