# Schemin '26 Documentation Catalog

**Authority:** The Librarian (CKO), adapted from the FLA Bullpen knowledge model  
**Version:** 2.0  
**Created:** 2026-09-25  
**Review cadence:** Monthly during season; at every major architecture change; postseason closeout

## Directive

This catalog is the card catalog for Schemin '26.

A durable project cannot depend on remembering which chat, PDF, or Markdown file contains the controlling rule. Every durable knowledge area must be represented here, routed through `docs/SESSION_CONTEXT.md`, and registered in `docs/INVENTORY.md`.

The repository should remain deliberately smaller than FLA. We adopt the Librarian's **discipline**, not FLA's full organizational weight.

## Knowledge areas

| Area | Primary index / entry point | Authority |
|---|---|---|
| Project control | `PROJECT_CONTROL_REGISTRY.md` | SCK / Executive Control |
| Session routing | `docs/SESSION_CONTEXT.md` | Librarian |
| Task orientation | `governance/task-orientation/TASK_CONTEXT_MATRIX_V1.json` | Librarian + SCK |
| Production resilience | `governance/resilience/README.md` | Librarian + Groundskeeper + Umpire |
| Checkpoint runtime | `governance/resilience/checkpoint_cli.py` | Groundskeeper + Umpire |
| Execution control | `governance/execution-control/TASK_REGISTRY_V1.json` | Bullpen Execution Control + domain authorities |
| Repository architecture | `docs/architecture/REPOSITORY_ARCHITECTURE_V2.md` | Librarian + Architect |
| Folder placement registry | `governance/repository-architecture/FOLDER_DOMAIN_REGISTRY_V2.json` | Librarian + Architect |
| Living Novel routing | `living-novel/os/SESSION_CONTEXT.md` | Novel OS + Librarian / Umpire |
| Source hierarchy | `docs/governance/SOURCE_OF_TRUTH.md` | Governance / Data |
| Authority boundaries | `docs/governance/AUTHORITY_MATRIX.md` | Executive Control |
| Weekly Memo OS | `memo-os/_INDEX.md` | Weekly Memo OS |
| Jack Mercer | `mercer/_INDEX.md` | Mercer |
| ESPN / league truth | `data-gateway/_INDEX.md` | Data Gateway |
| Character canon | `canon/_INDEX.md` | Character Canon |
| Bullpen / specialist review | `bullpen/_INDEX.md` | Bullpen / Librarian |
| Prompt registry | `prompts/README.md` | Owning subsystem |
| Schemas | `schemas/README.md` | Data / owning subsystem |
| Tests / acceptance | `tests/README.md` | QA / owning subsystem |
| Decisions | `docs/decisions/` | Librarian records; relevant authority decides |
| Publication manifest | `governance/publication-manifest/_INDEX.md` | Derived identity index; owning release systems remain authoritative |
| Planning lifecycle | `planning/README.md` | Groundskeeper + owning program |
| World / Atlas | `world/README.md` | World Engine / Atlas Control Plane |
| Chronicles / historical narrative | `chronicles/README.md` | Librarian + owning historical publication |
| Cross-system productions | `productions/README.md` | Owning production authority |
| Roadmap | `planning/ROADMAP.md` | Executive Control |
| Archive | `archive/_INDEX.md` | Librarian |

## Catalog rules

1. A new durable subsystem gets an index, owner, source-of-truth declaration, and review cadence.
2. A superseded document is archived or clearly marked; it is not silently deleted.
3. Exact migrated source artifacts are preserved separately from synthesized control documents.
4. Current state and historical evidence are never mixed without labels.
5. Chat history may supply context, but durable decisions must be written into Git.
6. Every major operating change updates the relevant index, inventory, and decision record in the same work cycle.
