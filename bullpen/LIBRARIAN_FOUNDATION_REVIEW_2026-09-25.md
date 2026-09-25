# Schemin '26 — Librarian Foundation Review

**Director:** The Librarian (CKO)  
**Date:** 2026-09-25  
**Scope:** Entire new `schemin-26` repository  
**Purpose:** Establish long-term institutional memory and retrieval discipline.

## Librarian assessment

The migration succeeded in preserving the project's strongest source artifacts, but the initial repository was **artifact-rich and navigation-light**.

The primary risk was not missing intelligence. It was future retrieval failure:

- no dedicated session-intent router;
- no formal knowledge inventory;
- no decision-record system;
- no archive contract;
- no review cadence;
- subsystem folders had entry-point READMEs but no consistent knowledge architecture;
- current and historical review documents could eventually become difficult to distinguish;
- Git could store the information without guaranteeing that future sessions would load the correct information.

## Ruling

Schemin '26 should adopt a **lightweight version of FLA's Librarian discipline**.

Do not reproduce the size of FLA's documentation estate. Preserve these high-value mechanisms:

1. **Card catalog** — one map of knowledge areas.
2. **Inventory** — durable files are registered.
3. **Session router** — each task starts from only the controlling 2–4 docs.
4. **Decision capture** — architectural calls survive chat/session boundaries.
5. **Local subsystem indexes** — each domain declares authority and loading order.
6. **Archive contract** — old evidence remains retrievable without masquerading as current.
7. **Currency cadence** — monthly in-season audit + architecture-change audit.
8. **Postseason promotion** — durable lessons survive; weekly clutter does not become permanent doctrine.

## Current strengths

- Clear five-plane operating architecture.
- Strong Memo OS source material.
- Strong character continuity doctrine.
- Explicit ESPN freshness/fallback policy.
- Mercer now has a durable operating contract.
- FLA boundary is explicit.
- Migration provenance is documented.

## Priority gaps

### P0 — Execution integrity
Doctrine is ahead of executable enforcement. Acceptance rules need machine-visible tests and release evidence.

### P0 — Seasonal truth registry
The repo still needs a structured team/owner/identity registry and an authoritative keeper/draft-pick ledger contract.

### P1 — Data contract implementation
Gateway documentation exists; code/fixtures/health checks need to be made first-class here or explicitly delegated to FLA with a tested interface.

### P1 — Release history
Weekly Memo releases should gain a manifest linking source snapshot, locked pages, QA outcomes, and final PDF.

### P1 — Decision memory
Consequential changes should use ADRs instead of being discoverable only through long audit documents.

### P2 — Postseason lifecycle
A formal 2026 closeout package should decide what becomes permanent for 2027.

## Knowledge-loss tests

The repository should be considered healthy when a fresh session can answer, without prior chat context:

- What governs a Weekly Memo production?
- Is V5.2 permanent or still RC?
- Where does current league truth come from?
- What happens when ESPN is stale?
- Which character belongs to each owner despite team renames?
- Who owns a mixed ESPN + memo problem?
- What documents govern a Mercer trade decision?
- Why is FLA not the Schemin source of current league truth?
- What unresolved migration gaps still exist?
- What should be carried into 2027?

The new catalog, inventory, session router, roadmap, ADR, archive policy and subsystem indexes are designed to make those answers deterministic.

## Librarian conclusion

The repository should be treated as an **institutional operating memory**, not merely a backup folder.

The immediate next phase is not more documentation. It is converting the existing doctrine into **observable execution evidence**: tests, manifests, structured state, and repeatable weekly receipts.
