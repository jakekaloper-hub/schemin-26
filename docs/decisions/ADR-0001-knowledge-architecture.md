# ADR-0001 — Adopt Librarian-Governed Knowledge Architecture

**Status:** Accepted  
**Date:** 2026-09-25  
**Decision owners:** Schemin Executive Control + Librarian stewardship

## Context

Schemin '26 grew through multiple ChatGPT threads, generated artifacts, operating patches, and a separate Fantasy League Artworks repository. The project accumulated strong doctrine but risked knowledge fragmentation, authority ambiguity, and repeated reconstruction from conversation memory.

## Decision

Schemin '26 will use a lightweight Librarian-governed knowledge architecture:

- GitHub is the durable project memory.
- `PROJECT_CONTROL_REGISTRY.md` is the top-level control entry point.
- `docs/CATALOG.md` maps knowledge areas.
- `docs/INVENTORY.md` registers durable documents.
- `docs/SESSION_CONTEXT.md` routes new sessions to the minimum relevant context.
- Material architectural decisions receive ADRs.
- Every major subsystem maintains a local index.
- Superseded material moves to archive or is explicitly marked historical.
- FLA remains an upstream reusable specialist/platform source, not Schemin's current league-state database.

## Alternatives rejected

### Rely primarily on ChatGPT memory / threads
Rejected because routing, provenance, and version control are weak across long-running work.

### Copy FLA's full documentation bureaucracy
Rejected because Schemin '26 is smaller and should preserve context economy.

### One giant master Markdown file
Rejected because it creates merge conflicts, unclear authority, and poor task-specific retrieval.

## Consequences

Positive:
- faster session startup;
- better provenance;
- less cross-domain confusion;
- cleaner postseason handoff;
- reduced dependence on any one conversation.

Cost:
- indexes and inventory require maintenance;
- material decisions require same-session documentation discipline.
