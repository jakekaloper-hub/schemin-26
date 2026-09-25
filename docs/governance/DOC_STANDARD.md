# Schemin '26 Documentation Standard

**Authority:** The Librarian (CKO)  
**Version:** 1.0

## Required metadata for new durable documents

Whenever practical, durable operating documents should state:

- title;
- authority / owner;
- version;
- status;
- created or effective date;
- review cadence or review trigger;
- supersedes / superseded-by relationship where applicable.

## Document classes

Use one dominant class:

- **control** — tells the project what governs;
- **runbook** — tells operators how to execute;
- **reference** — factual lookup;
- **canon** — identity / continuity source;
- **schema** — machine-readable contract;
- **prompt** — versioned execution instruction;
- **decision / ADR** — records a consequential choice and rationale;
- **review** — point-in-time audit or board assessment;
- **historical** — preserved evidence no longer controlling.

## Active vs historical

A historical review may remain valuable without remaining controlling.

Never infer authority from filename age or detail. Use explicit status and the control registry.

## Versioning

- Preserve meaningful prior versions.
- Prefer a new version or explicit supersession over silent overwrite of controlling doctrine.
- Small factual corrections may update in place when they do not alter policy.
- Material policy changes require a decision record.

## Closure discipline

A material workstream is not complete until:
1. implementation/artifact exists;
2. relevant index and inventory are current;
3. material decision is recorded;
4. superseded guidance is labeled;
5. session router still points to the correct controlling docs.
