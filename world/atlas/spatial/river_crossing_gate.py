"""Screen synthetic straight-line pilot routes against candidate channel grid cells."""
from math import hypot,floor
from world.atlas.spatial.candidate_comparison import compare_candidates
from world.atlas.spatial.candidate_validation import load_candidate
from world.atlas.spatial.river_floodplain_gate import analyze_surface

def screen(step_m=50):
    if step_m<=0:raise ValueError('INVALID_STEP')
    fixture=load_candidate();points={x['location_id']:x['xy'] for x in fixture['anchors']+fixture['route_intermediates']}
    results=[]
    for surface in compare_candidates()['variants']:
        channels={tuple(p) for p in analyze_surface(surface['heightfield'],cell_m=step_m)['channel_cells_xy']}
        segments=[]
        for route in fixture['paths']:
            for a,b in zip(route['locations'],route['locations'][1:]):
                origin,dest=points[a],points[b]
                distance=hypot(dest[0]-origin[0],dest[1]-origin[1])
                # Dense synthetic grid-cell traversal. This detects corridor contact,
                # not the precise river centerline crossing or bridge structure.
                steps=max(2,int(distance/(step_m/4))+1)
                contacts=set()
                for k in range(steps+1):
                    t=k/steps;x=origin[0]+t*(dest[0]-origin[0]);y=origin[1]+t*(dest[1]-origin[1])
                    cell=(min(floor(x/step_m),len(surface['heightfield'])-1),min(floor(y/step_m),len(surface['heightfield'])-1))
                    if cell in channels:contacts.add(cell)
                segments.append({'route_id':route['route_id'],'from':a,'to':b,
                                 'candidate_channel_contacts':[list(v) for v in sorted(contacts)],
                                 'requires_crossing_design':bool(contacts),
                                 'bridge_ford_causeway_type':'NOT_ESTABLISHED',
                                 'route_infrastructure_approved':False})
        results.append({'variant':surface['variant'],'segments':segments})
    return {'status':'CANDIDATE_CORRIDOR_INTERSECTION_ONLY','results':results,'acceptance':'HOLD',
            'limitations':['RIVER_CHANNELS_SYNTHETIC','NO_WATERWAY_WIDTH_OR_DESIGN_FLOOD','STRAIGHT_LINE_ROUTES_NOT_APPROVED_ROADS','NO_APPROVED_CROSSING_INFRASTRUCTURE']}
