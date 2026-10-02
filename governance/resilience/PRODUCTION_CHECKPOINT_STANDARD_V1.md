# Production Checkpoint Standard V1

**Authority:** The Groundskeeper + The Librarian  
**Gatekeeper:** The Umpire  
**Status:** ACTIVE  
**Consumers:** Weekly Memo OS, Living Novel, long-running Schemin production

## Rule

A completed stage may be resumed/skipped only when there is a durable checkpoint proving:

`STAGE + CONTROLLING AUTHORITY + INPUT FINGERPRINTS + OUTPUT DIGESTS + EVIDENCE = REUSABLE WORK`

Task status alone is not sufficient.

## Required checkpoint fields

- checkpoint ID;
- project / workflow / stage;
- owner;
- source authority;
- completed timestamp;
- input fingerprints;
- output artifact digests;
- evidence references;
- invalidation triggers.

Machine contract: `../../schemas/production-checkpoint.schema.json`.

Operational writer/resolver: `checkpoint_cli.py`.
Durable receipts live under `checkpoints/<workflow>/`.

## Resume law

1. Resolve the durable task first.
2. Load candidate checkpoints for that workflow.
3. Recompute/compare current authoritative input fingerprints.
4. Recompute authoritative input digests and verify output artifact digests plus evidence references.
5. Ignore any checkpoint whose inputs changed, whose output is missing/mutated, or whose evidence no longer resolves.
6. Resume after the latest valid completed checkpoint.
7. If no checkpoint is valid, rerun the earliest affected stage only.
8. Never ask Jake to reproduce input merely because a checkpoint or transport path failed; distinguish missing input from missing durable storage.

## Invalidation examples

A checkpoint is invalid when:
- the controlling source is superseded;
- any recorded input fingerprint changes;
- a referenced output disappears;
- required evidence becomes stale against current head;
- character canon changes for a character used by the stage;
- verified league truth materially changes for the stage;
- the Commissioner explicitly reopens or replaces the work.

## Memo OS mapping

Examples of checkpoint-worthy boundaries:
- Fact Lock;
- Temporal/Character/World context load;
- Story Lock / Issue Previs;
- Page Design Packet set;
- approved page master;
- assembled PDF + render audit.

The Memo OS remains authoritative for what each stage means.

## Living Novel mapping

Examples:
- selected causal story unit;
- Minimum Pre-Prose Gate;
- Chapter Dossier;
- consultant/advisory reconciliation when used;
- reviewed manuscript;
- continuity/canon proposal;
- Founder-approved hard canon.

The Novel OS remains authoritative for manuscript/canon state.

## Anti-bureaucracy

Do not checkpoint trivial reads or every sentence/page edit. Checkpoint only stages expensive or consequential enough that repeating them would create material cost, drift, or user correction.


## Operational maturity rule

The checkpoint subsystem is considered operational only when:
- a checkpoint can be emitted by the repository-native CLI;
- the receipt validates against current source/input/output/evidence;
- a later resume resolves that receipt without chat memory;
- mutation/deletion of an input or output causes fail-closed invalidation.

A design document or task status alone does not satisfy this gate.
