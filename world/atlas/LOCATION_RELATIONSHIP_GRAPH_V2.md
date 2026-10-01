# LOCATION RELATIONSHIP GRAPH V2

The Atlas Control Plane owns the spatial relationship view over Universe world data.

## Relationship families
Containment: CONTAINS / WITHIN  
Physical adjacency: ADJACENT_TO  
Movement: ROAD_TO / PASS_TO / CAUSEWAY_TO / RIVER_TO / SEA_ROUTE_TO  
Hydrology: UPSTREAM_OF / DOWNSTREAM_OF / FLOODS_FROM  
Visibility: VISIBLE_FROM  
Civil/economic: TRADES_WITH / SERVES / SUPPLIED_BY  
Social/history: SHARES_POPULATION_WITH / RIVALS / HISTORICALLY_LINKED_TO  
League access: NEUTRAL_ACCESS_TO

## Derivation
Current route edges are generated directly from `world/data/routes.json`, including via stops. Physical-region adjacency is inherited from `physical_zones.json`. Location containment is inherited from `locations.json`.

No invented exact mileage is introduced.

## Known open layers
Hydrologic direction and horizon visibility remain sparse until evidence exists. Their absence is preferable to invented precision.

## Canonical checks
- Bridge at Mountain Lake belongs to actual route chains.
- Southern Speedway is a via node on Basin Market Road.
- Country Club is connected through Delta Causeway / Jackson Levee logic.
- TDS–Chili Shared March remains explicitly cross-divisional.
- all home anchors inherit route access through V1.1 validation.

**GATE 3 DESIGN: PASS / EXECUTABLE GRAPH CREATED**
