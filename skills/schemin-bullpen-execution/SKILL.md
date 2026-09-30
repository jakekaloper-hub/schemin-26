---
name: schemin-bullpen-execution
description: Use when Jake asks Bullpen to execute, proceed, work, loop, finish, produce, or complete substantial Schemin work where plans or role-played reviews would be insufficient.
---

# Schemin Bullpen Execution

## Overview
Bullpen is an execution contract, not simulated staffing. A role counts as having acted only when there is evidence: a tool invocation, durable artifact, test result, rendered asset, or explicit BLOCKED state.

**Core principle:** evidence before completion claims.

## Command compilation

Jake is not required to memorize Bullpen commands. Before routing substantial work, interpret broad natural language through the canonical Bullpen command vocabulary and the Schemin adapter at `docs/architecture/BULLPEN_COMMAND_ADAPTER_V2.md`.

Command selection and Director selection are separate: command determines WHEN/HOW; Director routing determines WHO. Explicit constraints such as "planning only", "do not execute", "audit only", or "do not generate" override broad execution language.

If no precise command is recognized, default a broad authorized objective to `run`; use `mission` for an end-to-end outcome with unknown phases; use `incident` for repeated/systemic production failure.

## Required behavior
1. Recover the current objective, authoritative repo state, and applicable canon/data constraints.
2. Think and plan internally; do not stop at the plan when execution is possible.
3. Route work through canonical Bullpen Core to the smallest relevant Director set.
4. Consume the canonical `counterweight_plan`. If it is activated, include its counterweight Directors as challenge participants while preserving the primary Director's authority.
5. Add Schemin project-local roles only after canonical Director routing; project roles never create a 19th Bullpen Director.
6. Execute available work with real tools.
7. Persist durable outputs to the owning repository or requested artifact surface.
8. Independently verify outputs before claiming success.
9. Record counterweight impact when it materially changed, constrained, or validated a decision.
10. Continue through nonblocked phases without asking Jake to approve routine implementation choices.
11. If a required capability is genuinely unavailable, stop exactly there and report BLOCKED with the missing capability and completed evidence.

Do not recreate the 18 Director weakness/counterweight registry inside Schemin. Its canonical source is `jakekaloper-hub/bullpen`.

## Evidence contract

| Claim | Minimum evidence |
|---|---|
| role worked | invocation/result or durable artifact |
| counterweight acted | recorded challenge/review tied to the canonical route |
| counterweight changed decision | before/after decision or explicit constrained/validated outcome |
| code implemented | repository change |
| tests pass | fresh test/CI output |
| image produced | actual image artifact |
| visual QA passed | inspection result against explicit gates |
| PDF complete | actual PDF + render-back/preflight evidence |
| workflow complete | every required gate has evidence |
| blocked | exact missing dependency/capability |

Markdown saying PASS, reviewed, or approved is not evidence by itself.

## Bullpen routing
Use domain authority, not ceremonial attendance:
- **Closer:** synthesis and final integration gate.
- **Architect / Setup Man:** software architecture, runtime, contracts, infrastructure.
- **Librarian:** source hierarchy, provenance, durable knowledge.
- **Scout:** ESPN/data acquisition and freshness.
- **Beat Writer:** narrative manuscript.
- **Visual Development:** Schemin project-local art direction and image production role.
- **Clubhouse Manager:** organizational/capability lifecycle; project character-continuity roles remain Schemin-local.
- **Umpire:** independent QA, contradiction and completion gates.
- Other Bullpen Directors join only when their domain materially affects the task.
- Activated canonical counterweights join as bounded challenge participants, not replacement owners.

Creator and final gatekeeper must be different roles.

## Counterweight challenge behavior

When `counterweight_plan.activated === true`:
- preserve the canonical primary Director;
- surface the declared failure mode;
- use the canonical challenge questions during work;
- apply the canonical PRE / DURING / POST controls;
- record whether the challenge changed, constrained, or validated the result;
- do not count attendance alone as counterweight evidence.

For inactive counterweights, retain the challenge plan but do not add ceremonial participants.

## Production state machine
Use: PENDING → RUNNING → PASSED | FAILED | BLOCKED.

A failed QA gate routes to bounded revision when revision is possible. Missing workers, credentials, tools, source evidence, or required artifacts produce BLOCKED; never convert them into simulated success.

For Chronicle spread production, use:
source_packet → manuscript_slice → spread_spec → art_job → character_visual_QA → composition → render_QA → final_gate.

## Autonomy boundary
Proceed without routine confirmation for reversible implementation choices already inside Jake's stated objective.

Escalate only when:
- authoritative sources materially conflict;
- evidence is insufficient for a factual claim;
- a decision permanently redefines major canon;
- an irreversible external action requires approval;
- multiple fundamentally different creative directions require Jake's authorship.

## Completion response
Report only:
1. what was actually completed;
2. proof: paths, commits, test/run evidence, or artifacts;
3. genuine blockers;
4. the next executable phase if work remains.

Do not present a prompt, roadmap, board meeting, audit document, or future plan as a substitute for the requested deliverable.

## Red flags
- “Bullpen reviewed” without independent evidence.
- “Counterweight reviewed” with no recorded challenge or decision effect.
- Rebuilding the canonical 18-Director counterweight registry inside Schemin.
- Treating a Schemin project role as a new Bullpen Director.
- “Production complete” without the production artifact.
- “Tests pass” without fresh execution output.
- Asking Jake to say “continue” when the next step is already authorized.
- Creating governance documents repeatedly while the requested artifact remains unbuilt.
- Treating a persona as a persistent autonomous agent when no such worker invocation occurred.

If any red flag occurs, correct the claim and return to the last evidence-backed state.
