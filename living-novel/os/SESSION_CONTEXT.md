# Living Novel Session Context Router

**Authority:** Novel OS + The Librarian / Umpire  
**Version:** 1.0  
**Purpose:** Route Novel work to the smallest authoritative packet needed before prose, continuity, canon, or visual work.

## Start rule

Do **not** load the full `living-novel/` tree.

1. Match the task against `TASK_CONTEXT_MATRIX_V1.json`, then resolve existing Novel work in `../../governance/execution-control/TASK_REGISTRY_V1.json` before creating a new chapter/program task.
2. Load the returned sources, capped at four initial files. The Whole-Book Source Authority Matrix is pinned as controlling context and cannot be truncated by the ceiling.
3. For any manuscript-changing work, obey the current whole-book source/authority matrix.
4. Expand only when a material evidence gap, contradiction, failed gate, or cross-domain dependency appears.
5. A source week is evidence; it does not automatically define a chapter.

## Common routes

| Intent | Start here |
|---|---|
| Current Novel state | `README.md`, `MASTER_DIRECTIVE.md`, `whole-book/WHOLE_BOOK_SOURCE_AUTHORITY_MATRIX_V1.md` |
| Plan/write a chapter | Minimum Pre-Prose Gate, Causal Chapter Architecture, Open Loop Ledger |
| POV / character work | POV Constitution, Open Loop Ledger, current Character Canon |
| Canon/release | Canon Protocol, Whole-Book Source Authority, Project Control Registry |
| Live league event → story | Phase 7 Live Season Engine, Data Gateway, Open Loop Ledger |
| Continuity/history | Phase 4 Continuity Intelligence, Open Loop Ledger, Whole-Book Source Authority |
| World/geography | Physical World, Atlas Control Plane, Location Control Plane integration |
| Visual storytelling | Phase 6 Visual Engine, current Character Canon, Location Control Plane |
| Author Council | External Advisory Council, advisory integration patch, Whole-Book Source Authority |

## Context economy

Novel quality is not improved by loading every historical plan, superseded manuscript, consultant dossier, and QA receipt into every session. Current authority should be loaded first; historical evidence is pulled only when the task needs it.
