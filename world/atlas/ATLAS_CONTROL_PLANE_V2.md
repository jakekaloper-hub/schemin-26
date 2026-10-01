# ATLAS CONTROL PLANE V2

**Status:** RELEASE CANDIDATE — spatial subsystem of Universe OS V1.2.

## Architectural rule
The Atlas is a family of spatial views over authoritative Universe data. It does not own independent geography.

## Layers
A. Physical  
B. Civil / Institutional  
C. Division overlay  
D. Owner Domain  
E. Roads & Travel  
F. Encounter  
G. World State  
H. Weather  
I. Horizon / Visibility

## Spatial responsibilities
- containment;
- adjacency;
- route topology;
- hydrology relationships;
- travel classes;
- visibility;
- spatial QA;
- deterministic map products.

## Existing active components reused
- Atlas V1;
- Atlas Phase 1 expansion governance;
- Phase 2 Location Control Plane;
- Phase 3 structural environment references;
- Phase 4 Interactive Atlas;
- Phase 5 Weekly World Evolution.

## Invariants
- division layers are nonexclusive overlays;
- owner domains are not sovereign countries by default;
- lower spatial layers inherit upper physical constraints;
- active locations use stable LOC-* IDs;
- rendering cannot mutate geography;
- exact metric/GIS precision is not required for continuity.

## Promotion target
Atlas Control Plane V2 becomes active only with Universe OS V1.2 acceptance.
