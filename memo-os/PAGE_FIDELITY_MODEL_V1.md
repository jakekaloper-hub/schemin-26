# Weekly Memo OS — Page Fidelity Model V1

**Status:** V5.6 RC REQUIRED
**Source:** actual Week 2 + Week 3 released page anatomy
**Purpose:** decide whether a new PNG page genuinely belongs to the Schemin publication family.

## Gate structure

A page must pass both:

`TECHNICAL_ACCEPTANCE`
and
`PUBLICATION_FIDELITY`.

No weighted average can allow technical correctness to compensate for failed publication fidelity.

## Ten fidelity dimensions

Each dimension receives PASS / FAIL plus evidence.

### F1 — Scene specificity
PASS when the physical concept is inseparable from the named story.
Auto-fail if team labels can be swapped with unrelated teams and the scene still works.

### F2 — Narrative agent presence
Required character(s), force, institution or world agent must actively participate in the visual story.
Decorative portrait presence is insufficient.

### F3 — Environmental storytelling
At least one location cue and one story-specific prop/callback must communicate narrative before body copy.

### F4 — Editorial-art integration
Headline, score/facts, art and body copy must share one composition.
Flagship pages fail when built as generic hero image + separate report panel.

### F5 — Depth construction
Where concept permits, foreground, midground and background must each carry intentional information.

### F6 — Prop/evidence density
The page must contain concrete physical evidence of the week: receipts, debris, trophies, food, signs, wager slips, office papers, route markers, tools, weather damage, etc.
Props cannot be generic decoration only.

### F7 — World binding
The setting must be physically compatible with the active World/Encounter packet and recognizable through visual cues beyond a caption.

### F8 — Page archetype originality
The page may share publication DNA but cannot mechanically reuse the prior flagship page’s structure.
Repeated template dependence across an issue is a fidelity defect.

### F9 — Visual premise before prose
Independent reviewer must be able to explain the central visual joke/conflict/stake from illustration + headline + primary data without reading the body copy.

### F10 — 390px hierarchy
At phone width, headline, primary subjects, matchup/result/projection state and essential story beat remain legible and visually ordered.

## Benchmark comparison gate

Benchmark pages remain isolated during blank-canvas generation.
After a candidate exists, independent QA compares it against representative Week 2/Week 3 pages for:
- ambition;
- density;
- scene specificity;
- visual storytelling;
- character scale;
- typography confidence;
- physical-world believability;
- editorial finish.

Exact composition similarity is prohibited.
Quality-family similarity is required.

## Negative-control auto-fail

The first V5.6 Week 4 technical fixture is the permanent negative control:
- single generic hero;
- dark lower information panel;
- minimal scene-specific prop language;
- missing opposing matchup agent;
- art and typography adjacent rather than integrated;
- insufficient benchmark-level density.

Any flagship page that materially regresses toward this structure fails F1/F3/F4/F6/F8/F9.

## Page acceptance receipt

```yaml
page_id:
technical_acceptance:
fidelity:
  F1_scene_specificity:
  F2_narrative_agent_presence:
  F3_environmental_storytelling:
  F4_editorial_art_integration:
  F5_depth_construction:
  F6_prop_evidence_density:
  F7_world_binding:
  F8_page_archetype_originality:
  F9_visual_premise_before_prose:
  F10_mobile_hierarchy:
benchmark_comparison:
critical_defects:
real_page_acceptance:
```

REAL_PAGE_ACCEPTANCE is PASS only when technical acceptance and all release-critical fidelity dimensions pass.
