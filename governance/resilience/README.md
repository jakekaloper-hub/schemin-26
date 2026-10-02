# Schemin '26 Resilience — FLA Pattern Harvest V1

**Authority:** The Librarian + The Groundskeeper + The Umpire  
**Status:** ACTIVE shared control  
**Source precedent:** FLA commit `1494d7cb5342c186ac7f7ebfa84d75129ebc6496`  
**Consumers:** Weekly Memo OS, Living Novel, Bullpen project adapter

## Purpose

Prevent interrupted or cross-session Schemin work from being reconstructed from chat memory, repeated unnecessarily, or resumed from stale creative context.

This control adapts three proven FLA patterns into the existing Schemin architecture:

1. durable verified step checkpoints;
2. fresh-operator handoff testing;
3. creative-conditioning coverage / drift evidence.

It does **not** create a new OS, a second task registry, a second canon store, or a paid external dependency.

## Operating sequence

`task orientation → execution-control state → latest valid checkpoint → minimum authority packet → resume → proof`

A checkpoint is reusable only when its recorded inputs still match current authoritative inputs and its output/evidence receipts remain present.

## Authority rules

- `PROJECT_CONTROL_REGISTRY.md` remains top-level project authority.
- `governance/execution-control/TASK_REGISTRY_V1.json` remains task-state authority.
- Domain sources remain authoritative for facts, canon, publication and manuscript acceptance.
- Checkpoints record completed work; they do not promote truth or canon.
- FLA is a pattern donor only and has no authority inside Schemin.
- Chat memory is never sufficient proof that a stage completed.

## Files

- `FLA_PATTERN_HARVEST_V1.md` — research/audit/decision record.
- `PRODUCTION_CHECKPOINT_STANDARD_V1.md` — resumability contract.
- `FRESH_OPERATOR_HANDOFF_GATE_V1.md` — clean-session proof gate.
- `CREATIVE_CONDITIONING_REGISTRY_V1.json` — Memo/Novel conditioning coverage and drift signals.
- `resilience.py` — deterministic validation/resume utilities.
- `checkpoint_cli.py` — repository-native emit/resume path.
- `checkpoints/` — durable checkpoint receipt store.
- `validate_resilience.py` — repository gate.
- `test_resilience.py` — regression suite.
