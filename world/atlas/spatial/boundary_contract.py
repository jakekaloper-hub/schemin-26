"""Classify synthetic basin drainage exits against existing macro watershed law.
This is not evidence of particular real rivers or coastline geometry.
"""
from world.atlas.spatial.candidate_comparison import compare_candidates
from world.atlas.spatial.outlet_gate import drain_to_boundary

BOUNDARY = {'north': 'REG-UPPER-VALLEYS', 'south': 'REG-SOUTHERN-WETLANDS',
            'east': 'REG-EASTERN-STORM-COAST', 'west': 'REG-WESTERN-TABLELANDS'}
RECEIVING = {'REG-SOUTHERN-WETLANDS': 'REG-INNER-SEA-LITTORAL'}

def classify(point,n):
    x,y=point
    if y==0:return 'south'
    if y==n-1:return 'north'
    if x==0:return 'west'
    if x==n-1:return 'east'
    raise ValueError('OUTLET_NOT_ON_BOUNDARY')

def audit_boundary():
    result=[]
    for candidate in compare_candidates()['variants']:
        z=candidate['heightfield'];n=len(z)
        # This existing priority-flood routine establishes boundary-reachability but
        # does not return unique routed mouths. Do not invent a mouth count.
        conditioned=drain_to_boundary(z)
        if not conditioned['all_cells_boundary_reachable']:
            raise ValueError('UNRESOLVED_INTERIOR_DRAINAGE')
        south=[(x,0) for x in range(n)]
        north=[(x,n-1) for x in range(n)]
        result.append({'variant':candidate['variant'],
          'north_boundary_class':BOUNDARY['north'],
          'southern_receiving_zone':BOUNDARY['south'],
          'downstream_regional_relation':RECEIVING,
          'hypothetical_south_edge_cells':len(south),
          'hypothetical_north_edge_cells':len(north),
          'boundary_reachable':True,'verified_river_mouths':0,
          'geographic_boundary_certified':False})
    return {'status':'TOPOLOGICAL_CONTRACT_ONLY','region_id':'REG-CENTRAL-BASIN',
            'outlet_orientation_assumption':'SOUTH_GRID_EDGE_AS_DOWNSTREAM_HYPOTHESIS',
            'results':result,'independent_acceptance':'HOLD'}
