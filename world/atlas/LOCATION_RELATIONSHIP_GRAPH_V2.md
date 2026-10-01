# LOCATION RELATIONSHIP GRAPH V2

**Status:** RELEASE CANDIDATE

Owner: Atlas Control Plane + World Engine + Cartography.

The graph is derived from active LOC and ROUTE records. It does not invent metric geometry.

Required relationship classes include containment, roads, passes, causeways, river/sea routes, visibility, shared population, trade, historic links and neutral access. Only evidence-backed classes may be populated.

Gate rules:
- every major location resolves to a physical region;
- every home anchor touches an approved route or has an explicit isolation rule;
- required neutral venues are reachable;
- shared-space relationships survive division overlays;
- renderer-created adjacency is non-authoritative.
