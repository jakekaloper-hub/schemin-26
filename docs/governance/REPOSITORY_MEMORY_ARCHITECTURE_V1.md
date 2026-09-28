# Schemin '26 — Repository Memory Architecture V1

**Document class:** control
**Authority / owner:** Librarian + Architect + Umpire
**Version:** 1.0
**Status:** ACTIVE — PR #15 cleanup control
**Effective date:** 2026-09-28
**Review trigger:** material authority-chain change, subsystem release, or archive migration

## Objective

Make repository retrieval deterministic by separating current operating truth from historical memory and disposable residue.

## Three-plane memory model

### ACTIVE PLANE
Only material that may directly drive current production, decisioning, generation, validation, or release.

Allowed classifications:
- CANONICAL_CURRENT
- ACTIVE_SUPPORTING

### ARCHIVE PLANE
Material preserved for history, provenance, archaeology, regression research, or supersession lineage.

Allowed classifications:
- SUPERSEDED_REFERENCE
- ARCHIVE_ONLY
- EXPERIMENTAL_NONCANONICAL

Archive material must not compete with active authority.

### GIT HISTORY PLANE
Material with no remaining retrieval value:
- true duplicates;
- incorrect contaminants with no historical value;
- abandoned generated/transient artifacts;
- obsolete handoff residue;
- reproducible dead intermediates.

Deletion from the working tree is permitted after dependency and reference checks because Git history preserves provenance.

## Classification contract

Every materially relevant artifact resolves to exactly one primary state:

1. CANONICAL_CURRENT
2. ACTIVE_SUPPORTING
3. SUPERSEDED_REFERENCE
4. ARCHIVE_ONLY
5. EXPERIMENTAL_NONCANONICAL
6. DUPLICATE
7. INCORRECT_CONTAMINANT
8. GENERATED_TRANSIENT
9. UNRESOLVED

No file may rely on words such as FINAL, MASTER, CANONICAL, OFFICIAL, CURRENT, or APPROVED in its filename as proof of authority.

## Domain authority rules

| Domain | Active entry point / authority | Historical plane | High-risk ambiguity |
|---|---|---|---|
| Project navigation | `PROJECT_CONTROL_REGISTRY.md` on current main; PR #12 separately hardens governance | Git history / superseded governance | PR #12 is not yet merged; do not duplicate its controls here |
| Character canon | `canon/_INDEX.md` → visual lock → master canon → reference layer | retired descriptors / older world canon | duplicate `world/canon` master is contaminant candidate |
| League constants | `canon/league.json` + validated league truth | historical league ledgers | stale roster/team-state files |
| Memo OS | `memo-os/_INDEX.md` + controlling patch chain | old versions / test runs | older patch docs that still appear binding |
| Week production | week-specific active register set | completed weekly evidence / publication archive | stale PRE_FACT packets after Fact Lock |
| Data Gateway | `data-gateway/_INDEX.md` + executable code | historical endpoint/recovery investigations | design claims not implemented in code |
| Living Novel | `living-novel/README.md`, current OS/manifest lineage | superseded manuscripts / experiments | many proof/research artifacts appear operational |
| Chronicles / Prologue | approved/current production manifests + explicit official benchmark docs | proof-of-concept lineage | 171 files; highest volume of retrieval ambiguity |
| Mercer | `mercer/_INDEX.md` + operating contract | dated decisions / historical roster states | temporal facts can masquerade as current |
| Bullpen runtime | `bullpen-runtime/README.md` + executable runtime/tests | old consultation reports | old prompts may look executable |
| Prompts | active domain-owned prompts only | superseded prompts | prompt text is executable governance |
| Tests / schemas | tests supporting current behavior | retired fixtures / frozen historical regression data | tests may encode obsolete truth |
| Generated output | published/approved artifacts only | publication archive | transient output should not remain active |

## Retrieval law

A future agent should retrieve in this order:

1. domain index / project control registry;
2. explicit current authority;
3. active supporting files;
4. archive only when the task is historical;
5. never use Git history or deprecated artifacts as current authority without explicit recovery intent.

## Cross-PR rule

PR #15 must not recreate or overwrite governance work that belongs to PR #12.

If PR #12 contains the future merged standing operating contract, branch-protection target, or repository-integrity controls, PR #15 references those as an upstream merge dependency rather than cloning them.

## Cleanup decision rule

For every candidate:
- Does active production depend on it?
- Is it independently authoritative?
- Does it preserve unique historical/provenance value?
- Could semantic retrieval mistake it for current truth?
- Is there a clearer replacement?
- Are downstream references repairable?

Disposition:
- active + unique → retain;
- historical + unique → archive/isolate;
- duplicate + no unique value → delete;
- wrong + dangerous + no history value → delete;
- unresolved → hold.

## Definition of repository-memory PASS

PASS requires:
- one current authority chain per domain;
- archive/history clearly isolated;
- no high-risk duplicate authority left unclassified;
- current indexes point only to current/supporting material;
- high-value anti-drift checks exist;
- unresolved ambiguity is registered, not hidden.
