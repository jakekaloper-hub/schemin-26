# Schemas — Cross-System Machine Contracts

**Authority:** owning subsystem / Data / architecture authority

Purpose: shared machine-readable schemas whose scope crosses or supports subsystem boundaries.

Subsystem-private schemas may stay inside their owning subsystem when that improves cohesion. This folder must not become a generic home for unrelated JSON.

## Active shared schemas

- `production-checkpoint.schema.json` — evidence-backed resumability contract for long-running Memo/Novel production stages.
