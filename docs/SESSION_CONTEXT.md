# Schemin '26 Session Context Router

**Authority:** The Librarian (CKO)  
**Version:** 1.0  
**Purpose:** Route a new ChatGPT / engineering session to the minimum authoritative context required.

## Session-start rule

Do not load the entire repository by default.

For substantial work:
1. Read `PROJECT_CONTROL_REGISTRY.md`.
2. Match the request to one row below.
3. Load the listed 2–4 documents.
4. Expand only when the task crosses domains or a source conflict appears.

## Routing map

| Intent | Load first |
|---|---|
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
