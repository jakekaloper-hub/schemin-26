"""Deterministic candidate A* route alternatives; never canonical roads."""
import heapq
from math import hypot
from world.atlas.spatial.candidate_comparison import compare_candidates
from world.atlas.spatial.candidate_validation import load_candidate
from world.atlas.spatial.river_floodplain_gate import analyze_surface

def pathfind(grid, start, end, channel_cells, risk_weight=8):
    n=len(grid)
    a=(round(start[0]/50),round(start[1]/50));b=(round(end[0]/50),round(end[1]/50))
    if any(not(0<=u<n and 0<=v<n) for u,v in (a,b)):raise ValueError('OUT_OF_GRID')
    q=[(0.0,a)];dist={a:0.0};back={};steps=[(u,v) for u in (-1,0,1) for v in (-1,0,1) if u or v]
    while q:
        _,p=heapq.heappop(q)
        if p==b:break
        for dx,dy in steps:
            x,y=p[0]+dx,p[1]+dy
            if not(0<=x<n and 0<=y<n):continue
            nxt=(x,y);length=hypot(dx,dy)*50
            grade=abs(grid[y][x]-grid[p[1]][p[0]])/length
            cost=length*(1+20*grade*grade+risk_weight*(nxt in channel_cells))
            proposal=dist[p]+cost
            if proposal<dist.get(nxt,float('inf'))-1e-8:
                dist[nxt]=proposal;back[nxt]=p
                heapq.heappush(q,(proposal+hypot(b[0]-x,b[1]-y)*50,nxt))
    if b not in dist:raise ValueError('NO_ROUTE')
    route=[b]
    while route[-1]!=a:route.append(back[route[-1]])
    route.reverse()
    return {'grid_cells':route,'channel_contact_cells':sum(p in channel_cells for p in route),
            'length_m_candidate':round(sum(hypot(v[0]-u[0],v[1]-u[1])*50 for u,v in zip(route,route[1:])),3),
            'endpoint_ids_preserved':True,'road_approved':False}

def evaluate():
    source=load_candidate();points={x['location_id']:x['xy'] for x in source['anchors']+source['route_intermediates']}
    results=[]
    for variant in compare_candidates()['variants']:
        channels=set(map(tuple,analyze_surface(variant['heightfield'],channel_threshold=25)['channel_cells_xy']))
        segments=[]
        for route in source['paths']:
            for a,b in zip(route['locations'],route['locations'][1:]):
                options=[]
                for weight in (0,8,25):
                    solution=pathfind(variant['heightfield'],points[a],points[b],channels,weight)
                    options.append({'risk_weight':weight,**solution})
                segments.append({'route_id':route['route_id'],'from':a,'to':b,'alternatives':options})
        results.append({'variant':variant['variant'],'segments':segments})
    return {'status':'SYNTHETIC_ROUTE_ALTERNATIVES_ONLY','results':results,'acceptance':'HOLD',
            'limitations':['NO_APPROVED_RIVER_WIDTH','NO_APPROVED_ROUTE_CENTERLINES','GRID_STEP_50M_IS_SYNTHETIC']}
