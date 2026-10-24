"""Compare hypothetical basin surfaces under the same historical topology; no canon promotion."""
from math import sin,pi,hypot
from world.atlas.spatial.landscape_experiment import build_landscape
from world.atlas.spatial.historical_constraints import build_historical_constraints
from world.atlas.spatial.candidate_validation import load_candidate


def compare_candidates(n=33, step_m=50):
    constraints=build_historical_constraints()
    data=load_candidate()
    anchors={x['location_id']:x['xy'] for x in data['anchors']+data['route_intermediates']}
    baseline=build_landscape(n=n,step_m=step_m)
    if constraints['region_id']!='REG-CENTRAL-BASIN':raise ValueError('WRONG_REGION')
    variants=[]
    for kind in ('baseline','west-ridge','central-valley'):
        surface=[]
        for j,row in enumerate(baseline['heightfield']):
            out=[]
            for i,z in enumerate(row):
                x=i/(n-1)
                relief=0 if kind=='baseline' else (9*(1-x)**2 if kind=='west-ridge' else -5*sin(pi*x)**2)
                out.append(round(z+relief,4))
            surface.append(out)
        def z_at(pt):
            x,y=pt[0]/step_m,pt[1]/step_m
            i,j=min(int(x),n-2),min(int(y),n-2)
            u,v=x-i,y-j
            return (1-v)*((1-u)*surface[j][i]+u*surface[j][i+1])+v*((1-u)*surface[j+1][i]+u*surface[j+1][i+1])
        segments=[]
        for route in data['paths']:
            stops=route['locations']
            for a,b in zip(stops,stops[1:]):
                p,q=anchors[a],anchors[b]
                distance=hypot(q[0]-p[0],q[1]-p[1])
                sampled=[z_at([p[0]+(q[0]-p[0])*k/16,p[1]+(q[1]-p[1])*k/16]) for k in range(17)]
                peak=max(abs(y-x)/(distance/16) for x,y in zip(sampled,sampled[1:]))
                segments.append({'route_id':route['route_id'],'from':a,'to':b,'candidate_max_grade':round(peak,5)})
        variants.append({'variant':kind,'min_elevation':min(map(min,surface)),'max_elevation':max(map(max,surface)),
                         'candidate_segments':segments,'heightfield':surface,
                         'historical_ids_preserved':True,'coordinate_approval':False})
    return {'status':'COMPARATIVE_SYNTHETIC_CANDIDATES','constraints_status':constraints['status'],
            'note':'No generated heightfield is historical evidence or hydrologically certified',
            'variants':variants}
