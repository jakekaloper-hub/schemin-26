# Schemin '26 Execution Control V1

This directory is the project adapter for Bullpen's Unified Execution Control Plane.

## Canonical execution state

`TASK_REGISTRY_V1.json` is the normalized machine-readable state for active/materially useful work. It does **not** replace domain authority. Every task points to a controlling `source_authority` and, where available, evidence receipts/tests.

## Initial migrated scope

Only live/current work is seeded:
- Character Reference Portability;
- Week 4 Weekly Memo;
- Living Novel next causal story gate.

Historical checklists are not imported merely because they exist.

## Query path

`request → Task Orientation → registry resolution → dependency/blocker check → domain authority → action → evidence → transition → roll-up → next`

## Completion law

A task marked COMPLETE must contain acceptance criteria and PASS evidence. Documentation alone does not satisfy execution unless the task's acceptance contract is itself a documentation deliverable.

## State vocabulary

`NOT_STARTED / READY / IN_PROGRESS / BLOCKED / WAITING_EXTERNAL / DEFERRED / VERIFYING / COMPLETE / SUPERSEDED / CANCELLED / REOPENED`
