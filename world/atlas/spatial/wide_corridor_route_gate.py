"""Noncanonical route alternatives under explicitly widened synthetic river corridors."""
from world.atlas.spatial.candidate_comparison import compare_candidates
from world.atlas.spatial.candidate_validation import load_candidate
from world.atlas.spatial.river_floodplain_gate import analyze_surface
from world.atlas.spatial.route_alignment_gate import pathfind

def expand(channels,n,radius):
    if radius<0:raise ValueError('NEGATIVE_CORRIDOR_WIDTH')
    return {(x,y) for cx,cy in channels for x in range(max(0,cx-radius),min(n,cx+radius+1))
            for y in range(max(0,cy-radius),min(n,cy+radius+1))}

def evaluate():
    source=load_candidate();sites={v['location_id']:v['xy'] for v in source['anchors']+source['route_intermediates']}
    rows=[]
    for candidate in compare_candidates()['variants']:
        grid=candidate['heightfield'];n=len(grid)
        channels=set(map(tuple,analyze_surface(grid,channel_threshold=25)['channel_cells_xy']))
        for radius in (0,1,2):
            risky=expand(channels,n,radius)
            segments=[]
            for route in source['paths']:
                for a,b in zip(route['locations'],route['locations'][1:]):
                    options=[]
                    for penalty in (0,8,25):
                        answer=pathfind(grid,sites[a],sites[b],risky,penalty)
                        options.append({'penalty':penalty,'corridor_contacts':answer['channel_contact_cells'],
                                        'candidate_length':answer['length_m_candidate'],
                                        'candidate_cells':answer['grid_cells'],'road_approved':False})
                    segments.append({'route_id':route['route_id'],'from':a,'to':b,'options':options,
                                     'mandatory_contact_under_all_penalties':all(o['corridor_contacts']>0 for o in options)})
            rows.append({'variant':candidate['variant'],'corridor_radius_cells':radius,'segments':segments})
    return {'status':'WIDENED_SYNTHETIC_CORRIDOR_ALTERNATIVES','results':rows,'acceptance':'HOLD',
            'limitations':['RIVER_WIDTH_UNVERIFIED','NO_APPROVED_BRIDGE_OR_FORD','LOCAL_GRID_DISTANCE_NOT_CANON']}
