# Weekly Memo OS — Page Production Contract V1

**Status:** V5.6 RC dependency

## Purpose
A compact pre-render contract that turns a page concept into a verifiable production unit.

## Required contract

```yaml
issue_id:
page_id:
page_role:
page_state: PLANNED

narrative_job:
chapter_beat:
reader_takeaway:

fact_dependencies:
fact_lock_receipts:
deterministic_data_fields:

owners_present:
characters_present:
temporal_canon_receipts:
reference_assets:
forbidden_mutations:

encounter:
  venue_id:
  venue_type:
  division_context:
  route_required:
  world_state_in:
  persistent_landmarks:
  provisional_location: false

continuity_in:
continuity_out:

image_tells:
prose_tells:
art_text_ratio:
camera_and_composition:
foreground:
midground:
background:
copy_budget:

adjacent_pages:
rhythm_function:
mobile_risk:

failure_conditions:
required_qa:
manual_approval_required:
```

## State rules

PLANNED → CONTRACTED → READY_FOR_RENDER → GENERATED → QA_PENDING → LOCKED

Any material FACT, canon, or world dependency change reopens only affected pages.

## Hard blocks

A page cannot enter READY_FOR_RENDER when:
- required Fact Lock is missing;
- a required character packet is unresolved;
- encounter geography is unresolved;
- factual text is delegated to uncontrolled image generation;
- mobile copy budget is undefined for a text-heavy page.

## Complementarity test

Every contract must answer:
- What does the image communicate that prose should not repeat?
- What does prose communicate that the image cannot show?

If both answers are materially identical, return to composition/copy.
