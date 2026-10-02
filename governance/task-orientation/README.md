# Schemin '26 Task Orientation

**Authority:** The Librarian + SCK / Executive Control  
**Runtime owner:** Bullpen Task Orientation V1  
**Purpose:** Reduce pre-planning latency by selecting the minimum authoritative context before execution.

## Fast path

`request → task class → 2–4 controlling sources → domain authority → action → proof`

Use `TASK_CONTEXT_MATRIX_V1.json` before broad repository search. The matrix is intentionally small and routes to existing sources of truth; it is not a new authority layer.

## Rules

1. Initial context is capped at four project sources. **Default project authority sources are pinned first** and cannot be displaced by task-specific sources. Pinned defaults count toward the ceiling; every declared route packet must fit without relying on silent truncation.
2. A matching route is a starting packet, not permission to ignore stronger project authority.
3. Expand only for a material evidence gap, source conflict, failed test, or cross-domain dependency.
4. Do not load entire folders merely because they exist.
5. Do not re-run archaeology already represented in current control/state files.
6. Current `PROJECT_CONTROL_REGISTRY.md` remains the top-level control authority.
7. Novel work immediately delegates to `living-novel/os/TASK_CONTEXT_MATRIX_V1.json`.
8. Bullpen commands and Director identities remain owned by the canonical Bullpen repository.

## Planning economy

The Bullpen planning-depth contract applies:

- quick — at most 1 distinct pre-planning pass;
- standard — at most 2;
- deep/mission — at most 3.

These are ceilings. Compatible research/spec/risk work should be collapsed into one pass rather than serialized.
