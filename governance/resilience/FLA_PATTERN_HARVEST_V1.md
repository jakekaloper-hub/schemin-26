# FLA Pattern Harvest V1 — Schemin '26 + Living Novel

**Authority:** Bullpen / The Librarian / The Architect / The Umpire  
**Inspected repository:** `jakekaloper-hub/fantasy-league-artworks`  
**Pinned revision:** `1494d7cb5342c186ac7f7ebfa84d75129ebc6496`  
**Date:** 2026-10-02  
**Decision:** ADAPT selected patterns; do not clone FLA runtime

## Mission

Run the Bullpen lifecycle against FLA as a pattern donor and determine what still improves the current Schemin '26 and Living Novel systems after Task Orientation V1.1, Execution Control V1, Repository Architecture V2, Memo OS V5.5, and the current Novel OS.

## Duplicate check

Already present strongly enough; do not rebuild:
- task/session orientation;
- execution-control registry;
- false-completion detection;
- source/canon authority separation;
- adversarial QA and release gates;
- resumable-state-machine doctrine in Novel OS;
- versioned prompt directory doctrine;
- deterministic evidence and publication receipts.

## ADAPT NOW

### 1. Durable verified production checkpoints

FLA precedent:
- `lib/workflow/stepCheckpoint.js`;
- completed stage output persisted before advance;
- skip/recall on retry;
- lease/recovery semantics for interrupted work.

Schemin adaptation:
- repository/evidence-backed checkpoint records, not Supabase rows;
- each checkpoint binds stage, controlling authority, input fingerprints, output digests and evidence;
- checkpoint reuse fails closed when inputs drift;
- task registry remains the workflow state authority.

Expected improvement:
reduce manual restarts, repeated user input requests, and re-execution of already-proven production stages.

### 2. Fresh-operator handoff gate

FLA precedent:
- Lunsford × Ezzell Gate R7 requires a fresh operator with repository access and no chat memory to recover current authority/state without Jake correction.

Schemin adaptation:
- deterministic fixtures must recover current Memo, character-portability and Novel work from repository truth;
- source authority and next action must be discoverable without conversation history;
- a missing/stale route is a blocking regression.

Expected improvement:
reduce cross-thread state loss and prevent "we already did this" failures.

### 3. Creative-conditioning coverage / drift registry

FLA precedent:
- Voice and Prompt Ledger concept;
- prompt-conditioning coverage matrix;
- drift detection distinguishes output quality from missing conditioning layers.

Schemin adaptation:
- no duplicate prompt engine;
- register the required creative conditioning layers for Weekly Memo and Living Novel;
- validate that every layer points to current authority;
- drift signals guide targeted audit rather than automatically mutating canon.

Expected improvement:
detect creative drift caused by omitted canon/world/POV/evidence conditioning before it becomes a finished artifact.

## REFERENCE / DEFER

### Full-season replay testing

FLA's 17-week full pipeline replay is strong evidence of end-to-end maturity. Schemin should adapt a historical multi-week replay only when enough stable Memo/Novel fixtures exist to avoid encoding provisional creative judgments as tests.

Revisit trigger:
at least two additional completed weekly cycles under the current Memo/Novel architecture.

### Autonomous sentinel/remediation runtime

Useful pattern: typed health signals, shadow mode, allowlists and circuit breakers.

Disposition: DEFER.

Reason:
current project baseline assumes ChatGPT Plus and no incremental paid always-on runtime. Existing CI, Bullpen Verify and repository gates already provide the safer first-party enforcement path.

### Episodic LLM memory

Disposition: REJECT as a source of project truth.

Reason:
Schemin's canon, open-loop, world, task and release state are explicitly repository-backed and provenance-bearing. Opaque agent memory may assist local execution later, but may never replace those stores.

## Acceptance standard

The harvest is successful only if:
1. no second OS or authority plane is created;
2. no production dependency is installed;
3. current Memo/Novel state can be recovered in a fresh session from Git;
4. checkpoint reuse is input-sensitive and evidence-backed;
5. creative-conditioning registry validates against existing authority paths;
6. existing Memo, Novel, orientation, execution-control and repository gates remain green.
