# WORLD MUTATION FANOUT CONTRACT V2

**Doctrine:** CHANGE ONCE → REBUILD MANY.

This contract extends Atlas Phase 5 Weekly World Evolution without replacing it.

## Fanout

### STATE_HISTORY_MUTATION
Authority changes:
- `world/data/current_world_state.json`
- `world/data/world_state_events.json`

Rebuild/review:
- Location Control Plane
- structural environment references where state is surfaced
- Interactive Atlas
- Memo hydration
- Novel hydration
- Universe query caches

### ROUTE_CHANGE
Authority changes:
- `world/data/routes.json`

Rebuild/review:
- Novel travel graph
- route/venue validation
- Location Cards
- Atlas views
- Memo/Novel world packets
- visual packets

### ACTIVE_LOCATION_CHANGE
Authority changes:
- `world/data/locations.json`

Rebuild/review:
- relationship graph
- Location Control Plane
- structural references
- Interactive Atlas
- travel graph
- encounter resolver
- Memo/Novel consumers

### CANDIDATE_PROMOTION
Candidate → active transition requires existing Atlas Phase 1/5 governance and Commissioner approval where required.

Rebuild:
- locations/routes as approved
- candidate store
- relationship graph
- LCP
- environment references
- Interactive Atlas
- venue resolver
- consumer indexes

## Anti-fork law
No downstream consumer is an authorized emergency write target. If a derived view is stale, rebuild it from the authority.
