"""Fail-closed continent-scale *candidate* topology; never authoritative geometry."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
ZONES=ROOT/'world/data/physical_zones.json'
# Proposed drainage network; not all branches are perennial or proven rivers.
# Coastal direct discharge and dry western catchments deliberately remain open.
CANDIDATE_EDGES=(
 ('REG-NORTHERN-SPINE','REG-UPPER-VALLEYS'),
 ('REG-UPPER-VALLEYS','REG-CENTRAL-BASIN'),
 ('REG-CENTRAL-BASIN','REG-SOUTHERN-WETLANDS'),
 ('REG-SOUTHERN-WETLANDS','REG-INNER-SEA-LITTORAL'),
)

def validate(edges=CANDIDATE_EDGES):
    data=json.loads(ZONES.read_text())
    zones={p['id']:p for p in data['regions']}
    if len(zones)!=7 or data.get('coordinate_space')!='schemin-local-v1 (abstract, non-metric)':
        raise ValueError('CANONICAL_ZONE_AUTHORITY_CHANGED')
    if len(edges)!=len(set(edges)):raise ValueError('DUPLICATE_EDGE')
    parents={}
    for upstream,downstream in edges:
        if upstream not in zones or downstream not in zones:raise ValueError('UNKNOWN_REGION')
        if downstream not in zones[upstream]['adjacent_region_ids']:
            raise ValueError('NONADJACENT_DRAINAGE_CANDIDATE')
        if upstream==downstream:raise ValueError('SELF_DRAINAGE')
        if upstream in parents:raise ValueError('UNSUPPORTED_MULTIPLE_OUTLETS')
        parents[upstream]=downstream
    for start in parents:
        seen=set();p=start
        while p in parents:
            if p in seen:raise ValueError('DRAINAGE_CYCLE')
            seen.add(p);p=parents[p]
    expected={'REG-NORTHERN-SPINE','REG-UPPER-VALLEYS','REG-CENTRAL-BASIN','REG-SOUTHERN-WETLANDS'}
    if not expected.issubset(parents) or any(x!='REG-INNER-SEA-LITTORAL' for x in set(parents.values())-expected):
        raise ValueError('MISSING_MANDATORY_SPINE_TO_SEA_RELATION')
    p='REG-NORTHERN-SPINE'
    while p in parents:p=parents[p]
    if p!='REG-INNER-SEA-LITTORAL':raise ValueError('SPINE_NOT_CONNECTED_TO_SEA')
    return {'authority':'NONCANONICAL_DERIVED_CONSTRAINT','source':'living-novel/world/PHYSICAL_WORLD.md',
            'canonical_zone_source':'world/data/physical_zones.json','coordinates':'NONE',
            'edges':[{'upstream':a,'downstream':b,'status':'GEOGRAPHIC_HYPOTHESIS','distance_m':None} for a,b in edges],
            'unresolved':['EASTERN_DIRECT_COASTAL_OUTLETS','WESTERN_SEASONAL_DRAINAGE','ACTUAL_RIVER_MOUTHS','COASTLINE_GEOMETRY'],
            'acceptance':'CONSTRAINT_VALIDATION_ONLY'}
