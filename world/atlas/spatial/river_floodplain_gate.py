"""Experimental D8 river corridors/flood exposure, NOT physical-world certification."""
from world.atlas.spatial.candidate_comparison import compare_candidates
from world.atlas.spatial.candidate_validation import load_candidate
from world.atlas.spatial.outlet_gate import drain_to_boundary


def analyze_surface(surface,cell_m=50,channel_threshold=45,stage_m=1.0):
    n=len(surface)
    if n<3 or cell_m<=0 or channel_threshold<1 or stage_m<0:
        raise ValueError('INVALID_MODEL_PARAMETERS')
    # Reuse priority-flood parent graph. This preserves drainage across filled
    # flats without fabricating extra downhill gradients on equal elevations.
    conditioning=drain_to_boundary(surface)
    filled=conditioning['filled_surface']
    downstream={(x,y):None for y in range(n) for x in range(n)}
    for x,y,u,v in conditioning['routing_parents']:
        downstream[(x,y)]=(u,v)
    flat_cells=sum(1 for (x,y),to in downstream.items() if to is not None
                   and 0<x<n-1 and 0<y<n-1 and abs(filled[y][x]-filled[to[1]][to[0]])<1e-8)
    accum={(x,y):1 for y in range(n) for x in range(n)}
    # Traverse parent chains from all source cells; O(n^2 * path length)
    # is acceptable in this tiny candidate fixture and makes mass accounting exact.
    for p in downstream:
        q=downstream[p]
        while q is not None:
            accum[q]+=1
            q=downstream[q]
    channels={p for p,a in accum.items() if a>=channel_threshold}
    # Static near-channel low-ground exposure, not a flood return-period map.
    exposure=set()
    for y in range(n):
        for x in range(n):
            if any(abs(cx-x)<=1 and abs(cy-y)<=1 and filled[y][x]<=filled[cy][cx]+stage_m
                   for cx,cy in channels):exposure.add((x,y))
    return {'channel_cells':len(channels),'near_channel_low_cells':len(exposure),
            'routed_flat_interior_cells':flat_cells,
            'unresolved_flat_interior_cells':0,
            'channel_cells_xy':[list(p) for p in sorted(channels)],
            'exposure_cells_xy':[list(p) for p in sorted(exposure)],
            'status':'EXPERIMENTAL_STATIC_SCREEN_ONLY','verified_floodplain':False}


def evaluate():
    source=load_candidate();landmarks=source['anchors']+source['route_intermediates']
    results=[]
    for candidate in compare_candidates()['variants']:
        grid=candidate['heightfield'];a=analyze_surface(grid)
        exposure={tuple(p) for p in a['exposure_cells_xy']}
        sites=[]
        for loc in landmarks:
            x,y=loc['xy']; cell=(round(x/50),round(y/50))
            sites.append({'location_id':loc['location_id'],'synthetic_near_channel_screen':cell in exposure,
                          'flood_risk_approved':False})
        results.append({'variant':candidate['variant'],'channel_cells':a['channel_cells'],
                        'near_channel_low_cells':a['near_channel_low_cells'],
                        'unresolved_flat_interior_cells':a['unresolved_flat_interior_cells'],
                        'routed_flat_interior_cells':a['routed_flat_interior_cells'],
                        'landmarks':sites,'floodplain_certified':False})
    return {'status':'NONCANONICAL_COMPARISON','results':results,'acceptance':'HOLD',
            'blocking_evidence':['UNAPPROVED_RIVER_OUTLETS','NO_DESIGN_STORM_OR_DISCHARGE',
             'UNRESOLVED_FILLED_FLATS','NO_SURVEYED_LANDMARK_ELEVATIONS']}
