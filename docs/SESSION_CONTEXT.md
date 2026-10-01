# Schemin '26 Session Context Router

**Authority:** The Librarian (CKO)  
**Version:** 1.1  
**Purpose:** Route a new ChatGPT / engineering session to the minimum authoritative context required.

## Machine task-orientation front door

Before broad repository search, classify the request with `governance/task-orientation/TASK_CONTEXT_MATRIX_V1.json`. This is the machine-readable companion to this document and is designed for Bullpen/ChatGPT task orientation.

Initial project context is capped at four sources. After orientation, resolve the request against `governance/execution-control/TASK_REGISTRY_V1.json` before creating a new roadmap/task. Expand only for a material evidence gap, authority conflict, failed test, or cross-domain dependency.

## Session-start rule

Do not load the entire repository by default.

For substantial work:
1. Read `PROJECT_CONTROL_REGISTRY.md`.
2. Match the request to one row below.
3. Load the listed 2–4 documents.
4. Expand only when the task crosses domains or a source conflict appears.

## Global publication identity lock

Whenever a session references the **official/published/league-shared Week 2 memo** or the **Week 2 gold standard**, resolve it to **`Week 2 memo.pdf`**, the 14-page September 23, 2026 illustrated issue with the Red Leopards “SPECIAL DELIVERY” cover. Do not substitute similarly named Week 2 finals, tests, reruns, replays, or RC candidates.


## Repeated-input / trust-recovery rule

Before asking the Commissioner to re-upload or reproduce previously supplied project inputs, reconcile repository truth and search current Project/Library/handoff evidence. A storage, durability, transport, retrieval, or renderer-binding defect must not be presented as missing user input.

For character-reference portability specifically, the Twelve were already re-uploaded and materialized 12/12 in the 2026-10-01 recovery cycle. Future sessions must resume from durable retrieval + C1 reference-binding work, not another bulk-upload request. Load `bullpen/LIBRARIAN_THREAD_CLOSEOUT_CHARACTER_PORTABILITY_2026-10-01.md` when this issue is involved.

## Routing map

| Intent | Load first |
|---|---|
| Task orientation / AI session startup | `governance/task-orientation/TASK_CONTEXT_MATRIX_V1.json`, this router, `PROJECT_CONTROL_REGISTRY.md` |
| Execution control / roadmap / task status / blockers / next | `governance/execution-control/TASK_REGISTRY_V1.json`, `governance/execution-control/README.md`, controlling domain source from the matched task |
| Living Novel / chapter / POV / manuscript / continuity | `living-novel/os/SESSION_CONTEXT.md`, `living-novel/os/TASK_CONTEXT_MATRIX_V1.json`, Whole-Book Source Authority Matrix |
| General Schemin '26 orientation | `PROJECT_CONTROL_REGISTRY.md`, `docs/governance/SOURCE_OF_TRUTH.md`, `planning/ROADMAP.md` |
| Produce or repair Weekly Memo | `memo-os/_INDEX.md`, V5 Studio Patch, V5.2-RC Patch, Master Character Canon |
| Audit Weekly Memo quality | V5.2-RC Patch, Gold-Standard Production Manual, `tests/README.md`, Character Canon |
| ESPN / stale data / roster mismatch | `data-gateway/_INDEX.md`, Operational Patch, ESPN Reliability Patch, freshness schema |
| Trade / waiver / lineup / roster decision | `mercer/_INDEX.md`, Mercer Operating Contract, current validated league state |
| Character artwork / visual identity | `canon/_INDEX.md`, Master Character Canon |
| Bullpen consultation | `bullpen/_INDEX.md`, latest Bullpen review, Authority Matrix |
| FLA integration | `docs/architecture/FLA_INTEGRATION.md`, Authority Matrix, latest Bullpen review |
| Architecture / repo organization | `docs/CATALOG.md`, `docs/INVENTORY.md`, Repository Architecture, latest ADRs |
| New prompt / workflow version | owning subsystem index, `prompts/README.md`, relevant ADR / operating contract |
| Historical question | `docs/INVENTORY.md`, `archive/_INDEX.md`, relevant migration/decision ledger |
| Publication identity / archive / Memo ↔ Novel relationship | `governance/publication-manifest/_INDEX.md`, Publication Manifest V1, Project Control Registry, owning release gate |

## Cross-domain routing

When a request touches multiple domains, SCK coordinates. Domain truth remains with its authority.

Examples:

```text
ESPN discrepancy + Weekly Memo
→ Data Gateway establishes truth
→ SCK coordinates
→ Weekly Memo OS owns publication

Mercer insight + public memo
→ Mercer owns private football analysis
→ firewall review
→ Weekly Memo OS decides publishable use

FLA specialist advice + Schemin workflow
→ FLA Bullpen provides specialist input
→ Schemin authority remains controlling
```

## Context economy standard

A healthy session should usually begin with **2–4 controlling files**, not 20 files and not raw conversation archaeology.
