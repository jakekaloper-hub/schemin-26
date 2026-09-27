# NOVEL OS ADOPTION DECISIONS
**Status:** PHASE-2 CLOSER RULING

## Board disagreement
**Toolsmith:** favors a database/knowledge-graph service early for structured state.
**Librarian:** favors repository-native files first because they preserve portability, reviewability and provenance.
**Continuity Director:** wants structured records immediately, independent of storage engine.
**Closer ruling:** define strict schemas and repository-native JSON first. Introduce a database/index as a derived acceleration layer only after fixtures prove the data model. Git remains recoverable authority; indexes are rebuildable.

**Visual Director:** favors multiple generation providers for model diversity.
**Canon Guardian:** warns that provider diversity increases reference drift.
**Closer ruling:** one adapter contract, multiple optional providers. Visual Canon Gate remains provider-independent.

## Phase-2 decisions
1. ADAPT deterministic continuity patterns from CanonKit/Novel-OS.
2. ADAPT acceptance-only memory mutation from Novel Studio AI.
3. ADAPT promise/forget-risk tracking from NovelForge-style systems.
4. LEARN from LoreWeave evidence-linked graph/RAG architecture; no code copying.
5. Keep GitHub as durable operating record for v1.
6. Keep plugins as replaceable adapters.
7. Do not install additional SaaS for v1 core.
8. Implement core engine in small dependency-light Python modules + JSON schemas so CI and local execution remain portable.
