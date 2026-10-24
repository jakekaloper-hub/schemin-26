# WORLD STATE RECONSTRUCTION CONTRACT V1

**Status:** PROTOTYPE CONTRACT — NON-AUTHORITATIVE
**Gate:** G5
**Authority preserved:** World Evolution + authoritative files under `world/data/`

## Purpose
Define deterministic, version-aware reconstruction proof without creating a second world-state store.

## Authority rule
A reconstruction envelope is a **DERIVED RECEIPT / TEST FIXTURE**. It MUST NOT be read as canonical current state and MUST NOT write canonical state. Canon remains:
- `world/data/current_world_state.json`
- `world/data/world_state_events.json`
- `world/evolution/WORLD_EVOLUTION_LEDGER.json`
through the governed World Evolution apply path.

## Envelope V1
Required:
- `contract_version`: `1.0`
- `state_schema_version`
- `events_schema_version`
- `ledger_schema_version`
- `base_state`
- `base_events`
- `base_ledger`
- `source_hashes`
- `transactions`

Each transaction is an existing World Evolution request. Reconstruction applies transactions in declared order using `apply_to_payloads`.

## Integrity
Before replay, canonical JSON serialization of each base payload MUST match its recorded SHA-256. Hash mismatch fails closed.

## Version policy
V1 supports source schema `1.0` only. Unknown contract or source schema versions fail closed with an explicit error. No implicit migration, coercion or best-effort load is permitted.

A future migration must be an explicit function from one named version to another with tests proving the transformation. Unsupported migrations MUST fail without mutation.

## Determinism
Given identical base payloads + hashes + ordered transactions, reconstruction MUST produce byte-equivalent canonical JSON for state/events/ledger.

## Safety
- in-memory only for prototype;
- no canonical writes;
- no renderer dependency;
- no Unreal dependency;
- no network dependency;
- zero incremental spend.

## G5 acceptance
PASS only if the contract defines authority, versions, hashes, replay ordering, deterministic comparison, explicit unsupported-version failure, and no-write behavior.
