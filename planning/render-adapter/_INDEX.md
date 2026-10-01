# Schemin Render Adapter — Research Candidate

**Status:** RESEARCH_CANDIDATE / NOT ACTIVE  
**Date:** 2026-09-30  
**Authority:** planning only; does not modify PROJECT_CONTROL_REGISTRY.md  
**North star:** `SCHEMIN_26_PROJECT_MISSION.md`

This directory tests whether multiple render surfaces can consume the same governed Schemin inputs without creating another source of truth.

It does **not** install or authorize AIComicBuilder, Vizzu, OpenStoryline, Remotion, VoiceStudio, TimelineJS3, or any other production dependency.

## Candidate artifacts

- `SCHEMIN_RENDER_ADAPTER_CONTRACT_V1_CANDIDATE.md` — architecture and authority contract.
- `render_request_v1.schema.json` — proposed request shape.
- `adapter_profiles_v1.json` — Character-Grounded Static, Data Story, and Motion research profiles.
- `contract_validator.py` — stdlib-only fail-closed contract checker; not a renderer.
- `EXTERNAL_REPO_RECONCILIATION_AND_PLAN_V1.md` — research → plan → test findings.
- `../../tests/test_render_adapter_candidate.py` — executable research acceptance tests.

## Promotion rule

Nothing here becomes ACTIVE because it is present on `main`. Promotion would require a separate decision, evidence from a live Schemin production use, license/security review for any selected dependency, and explicit Project Control Registry integration.
