"""Independent numeric gates for candidate surfaces; deliberately cannot certify canon."""
from math import hypot
from world.atlas.spatial.candidate_comparison import compare_candidates
from world.atlas.spatial.candidate_validation import load_candidate


def evaluate(n=33, step_m=50):
    candidates=compare_candidates(n,step_m)
    source=load_candidate()
    points=source['anchors']+source['route_intermediates']
    results=[]
    for item in candidates['variants']:
        z=item['heightfield']
        sinks=[]; drainage_edges=0
        for j in range(n):
            for i in range(n):
                neighbors=[(x,y) for y in range(max(0,j-1),min(n,j+2)) for x in range(max(0,i-1),min(n,i+2)) if (x,y)!=(i,j)]
                lower=[(x,y) for x,y in neighbors if z[y][x]<z[j][i]]
                if lower: drainage_edges+=1
                else: sinks.append([i,j])
        samples=[]
        for p in points:
            x,y=p['xy'];i,j=int(x/step_m),int(y/step_m)
            if not (0<=i<n and 0<=j<n): raise ValueError('SITE_OUTSIDE_GRID')
            neighbors=[z[a][b] for a in range(max(0,j-1),min(n,j+2)) for b in range(max(0,i-1),min(n,i+2))]
            relief=max(neighbors)-min(neighbors)
            samples.append({'location_id':p['location_id'],'local_relief_m_candidate':round(relief,5),'site_certified':False})
        max_grade=max(s['candidate_max_grade'] for s in item['candidate_segments'])
        results.append({'variant':item['variant'],'candidate_sink_count':len(sinks),
                        'candidate_sinks':sinks,'drainage_edge_count':drainage_edges,
                        'peak_route_grade_candidate':max_grade,'landmark_relief':samples,
                        'grade_review_flag':max_grade>0.08,'hydrology_certified':False,'geometry_approved':False})
    return {'status':'COMPARISON_ONLY_NO_WINNER','region':'REG-CENTRAL-BASIN','results':results,
            'acceptance':'HOLD','blocks':['NO_OUTLET_BOUNDARY_MODEL','NO_FLOODPLAIN_MODEL',
             'NO_SURVEYED_LANDMARK_FOOTPRINTS','NO_APPROVED_SCALE','NO_CINEMATIC_GROUND_TRUTH']}
