# WORLD ENGINE PATTERN ADOPTION MATRIX V1

| Source | Pattern | Decision | Schemin application | Timing |
|---|---|---|---|---|
| Azgaar/FMG | Separate state, generators/editors, renderers | ADOPT | Canon/world data cannot be mutated by visual renderer | NOW |
| Azgaar/FMG | Controlled interactive mutation | ADOPT | World-state change must use explicit mutation records | NOW |
| WorldEngine | Multi-stage physical causality | ADAPT | Test climate/terrain/ecology/settlement coherence | NOW |
| WorldEngine | Procedural generation | REJECT AS AUTHORITY | Never overwrite existing Schemin geography | N/A |
| MapLibre | Layered vector rendering | FUTURE CONSIDERATION | Interactive Physical/Division/Owner/Encounter atlas | AFTER DATA STABILIZES |
| Turf.js | GeoJSON spatial operations | ADAPT | Executable containment/adjacency/route QA | PHASE 9 |
| ink | Persistent runtime state | ADAPT | Week N consequences become inherited Week N+1 state | NOW |
| ink | Branching player choice | REJECT | Real league results, not reader choice, determine future events | N/A |
| Logseq/Neo4j/Gephi | Knowledge graph representation | FUTURE CONSIDERATION | Character↔Location↔Event↔Artifact relationship visualization | POST-V1 IF NEEDED |

## Bullpen implementation verdict

The World Engine V1 should remain **Git-native and schema-first**.

Preferred near-term storage:
- YAML for human-maintained canonical records;
- JSON Schema for validation;
- JSON/GeoJSON where executable consumers require it;
- Markdown for human-readable bibles, indexes and audits.

Do not add a database until:
1. ontology is stable;
2. query volume justifies it;
3. file-native workflows become the bottleneck.
