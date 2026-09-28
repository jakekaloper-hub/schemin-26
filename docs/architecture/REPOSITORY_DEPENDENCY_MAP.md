# Schemin '26 — Repository Dependency Map

**Document class:** control / reference  
**Authority / owner:** The Architect + The Librarian  
**Version:** 1.0  
**Status:** ACTIVE  
**Effective date:** 2026-09-27  
**Review trigger:** new repository dependency, platform extraction, or project split

## Canonical repository

`jakekaloper-hub/schemin-26`

This repository owns all durable Schemin '26 project state: league-specific governance, canon, evidence, production systems, weekly state, Mercer controls, Novel OS, Memo OS, Data Gateway, QA evidence, and release decisions.

## Explicit GitHub relationship

`jakekaloper-hub/fantasy-league-artworks` is the only other GitHub repository explicitly referenced by the current Schemin tree as a reusable upstream platform / creative-engineering source.

Dependency direction:

```text
fantasy-league-artworks  -- reusable capability / upstream reference -->
schemin-26               -- league-specific configuration, evidence, canon, production, release authority
```

A reusable FLA defect may be fixed upstream, but the Schemin requirement and resulting upstream commit/PR reference must be recorded in `schemin-26`.

## Bullpen

Schemin-specific Bullpen authority/evidence lives in:
- `bullpen/`
- `bullpen-runtime/`

The reusable external Bullpen repository/tooling may be consulted when available, but it is not a required canonical storage location for Schemin project state unless a future ADR explicitly establishes such a dependency.

## External evidence/tool dependencies

These are services/providers, not alternate sources of project ownership:

- ESPN fantasy endpoint — primary live league evidence when successfully validated.
- Flaim — evidence/intelligence adapter; cannot override Schemin canon or Commissioner release authority.
- External visual/render transports — replaceable Novel OS execution dependencies; output becomes durable only when registered in Schemin.
- ChatGPT/plugins — execution surfaces; conversation state is convenience context, not durable project state.

## Anti-drift rule

No external repository or tool becomes authoritative for a Schemin domain merely because it contains a newer copy. Authority follows `PROJECT_CONTROL_REGISTRY.md`, `docs/governance/SOURCE_OF_TRUTH.md`, and explicit subsystem controls.
