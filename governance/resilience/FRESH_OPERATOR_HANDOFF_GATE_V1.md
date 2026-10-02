# Fresh-Operator Handoff Gate V1

**Authority:** The Umpire + The Groundskeeper  
**Status:** ACTIVE regression gate  
**Purpose:** prove Schemin can survive a new session/operator without relying on chat memory.

## Test condition

Operator receives:
- repository access;
- current `PROJECT_CONTROL_REGISTRY.md`;
- current session/task routing;
- no prior chat transcript or memory.

## Required recoveries

The repository must make all of the following discoverable without Jake correction:

1. current Week 4 Memo task and its next action;
2. current Character Reference Portability task and its next action;
3. current Living Novel task and its blocking dependency/next action;
4. source authority for each task;
5. whether each referenced source authority exists;
6. where session orientation and execution control begin.

The executable fixture is in `test_resilience.py`.

## Failure classes

- **STATE_LOSS** — task cannot be recovered from durable state.
- **ROUTING_DRIFT** — session/task route points to stale/superseded control.
- **AUTHORITY_GAP** — source authority is missing or ambiguous.
- **REPEAT_INPUT_RISK** — operator would need Jake to repeat already-durable input.
- **FALSE_RESUME** — operator would skip a stage without valid checkpoint evidence.

Any failure blocks promotion of resilience changes.

## Human follow-up

A real fresh-session test should periodically supplement the deterministic fixture. The deterministic test proves repository structure; it cannot prove every host/user-interface retrieval behavior.
