"""Sensitivity of synthetic route/channel contacts to threshold and corridor width."""
from math import hypot,floor
from world.atlas.spatial.candidate_comparison import compare_candidates
from world.atlas.spatial.candidate_validation import load_candidate
from world.atlas.spatial.river_floodplain_gate import analyze_surface

THRESHOLDS=(10,25,45,70)
WIDTH_CELLS=(0,1,2)

def evaluate(thresholds=THRESHOLDS,widths=WIDTH_CELLS):
    if not thresholds or not widths or any(x<1 for x in thresholds) or any(x<0 for x in widths):
        raise ValueError('INVALID_SENSITIVITY_SETTINGS')
    source=load_candidate();positions={p['location_id']:p['xy'] for p in source['anchors']+source['route_intermediates']}
    results=[]
    for variant in compare_candidates()['variants']:
        grid=variant['heightfield'];n=len(grid)
        for threshold in thresholds:
            channels={tuple(p) for p in analyze_surface(grid,channel_threshold=threshold)['channel_cells_xy']}
            for width in widths:
                hits=[]
                for path in source['paths']:
                    for a,b in zip(path['locations'],path['locations'][1:]):
                        p,q=positions[a],positions[b];distance=hypot(q[0]-p[0],q[1]-p[1]);steps=max(2,int(distance/5)+1)
                        closest=set()
                        for k in range(steps+1):
                            t=k/steps;x=p[0]+(q[0]-p[0])*t;y=p[1]+(q[1]-p[1])*t
                            cx=min(n-1,floor(x/50));cy=min(n-1,floor(y/50))
                            if any(abs(cx-i)<=width and abs(cy-j)<=width for i,j in channels):closest.add((cx,cy))
                        hits.append({'route_id':path['route_id'],'from':a,'to':b,'contact':bool(closest)})
                results.append({'variant':variant['variant'],'accumulation_threshold':threshold,'corridor_half_width_cells':width,
                                'segments_with_contact':sum(int(h['contact']) for h in hits),'route_segments':hits})
    return {'status':'SENSITIVITY_ONLY_NOT_RIVER_CERTIFICATION','results':results,
            'assumed_cell_size_m':50,'scale_authority':'SYNTHETIC_ONLY','approval':'HOLD'}
