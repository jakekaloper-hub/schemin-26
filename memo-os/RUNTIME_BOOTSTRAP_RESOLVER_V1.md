# Weekly Memo OS — Runtime Bootstrap Resolver V1

**Status:** V5.6 RC dependency  
**Purpose:** prevent stale chat assumptions, historical fixtures or superseded controls from becoming live production state.

Every substantial Weekly Memo invocation begins:

```text
READ PROJECT CONTROL REGISTRY
→ RESOLVE CURRENT WEEKLY MEMO OS
→ RESOLVE CURRENT PRODUCTION CYCLE
→ RESOLVE CHARACTER AUTHORITY
→ RESOLVE WORLD ENGINE
→ RESOLVE DATA/FRESHNESS AUTHORITY
→ READ PERSISTED CHECKPOINTS
→ READ OPEN DEFECTS
→ BUILD/REFRESH DEPENDENCY GRAPH
→ IDENTIFY NEXT READY WORK
```

## Bootstrap receipt

```yaml
run_id:
resolved_at:
control_registry_version:
weekly_memo_os:
subagent_orchestration:
bullpen_control:
world_engine:
character_authority:
data_snapshot:
production_cycle:
release_state:
latest_valid_checkpoint:
next_ready_dependency:
open_blockers:
superseded_inputs_rejected:
```

## Rules

- Repository/runtime authority supersedes conversational assumptions.
- Historical Week 2/Week 3 acceptance fixtures cannot become current production state.
- Hard-coded mutable character appearances cannot override current canon.
- UNKNOWN is not silently promoted.
- A stale checkpoint is rejected when newer persisted evidence exists.
- Current production is discovered, not embedded permanently in orchestration prompts.
