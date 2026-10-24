"""Drainage-basin audit for comparative synthetic grids, without canon inference."""
from world.atlas.spatial.candidate_comparison import compare_candidates


def audit_watersheds():
    comparison = compare_candidates()
    outcomes = []
    for candidate in comparison['variants']:
        z=candidate['heightfield']; n=len(z)
        flow={}
        for y in range(n):
            for x in range(n):
                adj=[(u,v) for v in range(max(0,y-1),min(n,y+2)) for u in range(max(0,x-1),min(n,x+2)) if (u,v)!=(x,y)]
                lower=[p for p in adj if z[p[1]][p[0]]<z[y][x]]
                flow[(x,y)]=min(lower,key=lambda p:(z[p[1]][p[0]],p[1],p[0])) if lower else None
        def destination(point):
            seen=set()
            while flow[point] is not None:
                if point in seen: raise ValueError('CYCLIC_DRAINAGE')
                seen.add(point);point=flow[point]
            return point
        catchments={}
        for point in flow:
            target=destination(point)
            catchments[target]=catchments.get(target,0)+1
        interior={p:c for p,c in catchments.items() if 0<p[0]<n-1 and 0<p[1]<n-1}
        outlets={p:c for p,c in catchments.items() if p not in interior}
        outcomes.append({'variant':candidate['variant'],'catchment_cells':sum(catchments.values()),
                         'outlet_catchments':len(outlets),'interior_sinks':len(interior),
                         'unresolved_interior_cells':sum(interior.values()),
                         'boundary_model_approved':False,'hydrology_accepted':False})
    return {'status':'DIAGNOSTIC_ONLY','results':outcomes,'physical_acceptance':'HOLD'}
