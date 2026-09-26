# Schemin' '26 Novel Engine — Upstream Research Ledger

**Reviewed:** 2026-09-26  
**Authority:** Bullpen Scout + Architect + Librarian  
**Decision record:** `ENGINE_ARCHITECTURE.md`

| Repository | Role | Decision | Schemin' use |
|---|---|---|---|
| jmorenobl/bookwright | Spec-driven authoring + continuity graph | **PRIMARY / ADAPT** | Constitution/bible/outline/manuscript model; pending facts; validation; provenance |
| sheengoa/novelforge | Long-form workbench + auditor | **BORROW** | Severity-based continuity review; deviation log; human arbitration |
| YfengJ/novel-studio-ai | Story memory + character state | **BORROW** | Confirmed memory; graph facts; retrieval context |
| HuangLeijiana/novel-agent | Multi-agent novel pipeline | **REFERENCE** | Specialized roles; reader simulator; refinement stages |
| mushroomfk/long-novel-agent-kit | Durable continuity infrastructure | **BORROW** | Chapter contracts; narrative debts; proposals; snapshots; audit trail |
| mrigankad/Novel-OS | Persistent state + editorial roles | **REFERENCE** | Compare deterministic + LLM validation and provenance design |
| cantus-industries/agentic-writers-room | Human-gated writers' room case study | **REFERENCE** | Generator/verifier separation; accepted-correction write-back |

## Selection rationale

Schemin' already possesses a constitution, bible, editorial gates, timeline and character canon. Therefore the correct upstream is not the repository with the most autonomous agents. It is the architecture that can strengthen **our existing source of truth** while keeping the manuscript auditable and human-controlled.

Bookwright is the primary architectural reference because its plain-text, Git-versioned, spec-driven approach is naturally compatible with Schemin' '26.

## Fork policy

Do not vendor/fork an upstream repository into `schemin-26` until:
1. license is verified,
2. exact modules required are identified,
3. adapter boundary is specified,
4. dependency/security review passes,
5. a proof-of-concept beats the Schemin'-native implementation.

Default mode is **adapt patterns, not copy stacks**.

## Re-evaluation triggers

Re-run upstream review when:
- manuscript exceeds current context strategy,
- continuity tests show repeated misses,
- a local author workbench becomes a priority,
- upstream Bookwright changes its artifact/validation model materially,
- Schemin' moves from one novel to a multi-book series.
