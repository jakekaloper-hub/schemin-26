---
name: schemin-bullpen-execution
description: Use when Jake asks Bullpen to execute, proceed, work, loop, finish, produce, or complete substantial Schemin work where plans or role-played reviews would be insufficient.
---

# Schemin Bullpen Execution

## Overview
Bullpen is an execution contract, not simulated staffing. A role counts as having acted only when there is evidence: a tool invocation, durable artifact, test result, rendered asset, or explicit BLOCKED state.

**Core principle:** evidence before completion claims.

## Required behavior
1. Recover the current objective, authoritative repo state, and applicable canon/data constraints.
2. Think and plan internally; do not stop at the plan when execution is possible.
3. Route work to the smallest set of relevant Bullpen roles.
4. Execute available work with real tools.
5. Persist durable outputs to the owning repository or requested artifact surface.
6. Independently verify outputs before claiming success.
7. Continue through nonblocked phases without asking Jake to approve routine implementation choices.
8. If a required capability is genuinely unavailable, stop exactly there and report BLOCKED with the missing capability and completed evidence.

## Evidence contract

| Claim | Minimum evidence |
|---|---|
| role worked | invocation/result or durable artifact |
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
- **Visual Development:** art direction and image production.
- **Clubhouse Manager:** character dignity and continuity.
- **Umpire:** independent QA, contradiction and completion gates.
- Other Bullpen directors join only when their domain materially affects the task.

Creator and final gatekeeper must be different roles.

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
- “Production complete” without the production artifact.
- “Tests pass” without fresh execution output.
- Asking Jake to say “continue” when the next step is already authorized.
- Creating governance documents repeatedly while the requested artifact remains unbuilt.
- Treating a persona as a persistent autonomous agent when no such worker invocation occurred.

If any red flag occurs, correct the claim and return to the last evidence-backed state.
