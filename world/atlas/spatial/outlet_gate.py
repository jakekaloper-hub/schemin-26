"""Experimental priority-flood drainage: outlet choice is hypothetical, not canon."""
import heapq
from world.atlas.spatial.candidate_comparison import compare_candidates


def drain_to_boundary(grid):
    n=len(grid)
    if n<3 or any(len(row)!=n for row in grid):raise ValueError('INVALID_GRID')
    visited=set();heap=[];filled=[[None]*n for _ in range(n)];parent={}
    for y in range(n):
        for x in range(n):
            if x in (0,n-1) or y in (0,n-1):
                filled[y][x]=grid[y][x]
                heapq.heappush(heap,(grid[y][x],y,x))
                visited.add((x,y));parent[(x,y)]=None
    while heap:
        z,y,x=heapq.heappop(heap)
        for yy in range(max(0,y-1),min(n,y+2)):
            for xx in range(max(0,x-1),min(n,x+2)):
                if (xx,yy) in visited:continue
                visited.add((xx,yy))
                f=max(z,grid[yy][xx])
                filled[yy][xx]=f
                parent[(xx,yy)]=(x,y)
                heapq.heappush(heap,(f,yy,xx))
    raised=sum(1 for y in range(n) for x in range(n) if filled[y][x]>grid[y][x]+1e-9)
    for cell in parent:
        seen=set();p=cell
        while parent[p] is not None:
            if p in seen:raise ValueError('FLOW_CYCLE')
            seen.add(p);p=parent[p]
        if p[0] not in (0,n-1) and p[1] not in (0,n-1):raise ValueError('INTERNAL_OUTLET')
    return {'raised_cells':raised,'boundary_outlets':len({p for p,v in parent.items() if v is None}),
            'all_cells_boundary_reachable':len(parent)==n*n,
            'interior_terminal_sinks':0,'filled_surface':filled,
            'status':'SYNTHETIC_HYDROLOGICAL_CONDITIONING_NOT_CANON'}


def audit():
    variants=compare_candidates()['variants']
    rows=[]
    for v in variants:
        a=drain_to_boundary(v['heightfield'])
        rows.append({'variant':v['variant'],'raised_cells':a['raised_cells'],
                     'interior_terminal_sinks':a['interior_terminal_sinks'],
                     'boundary_reachable':a['all_cells_boundary_reachable']})
    return {'results':rows,'acceptance':'EXPERIMENTAL_ONLY',
            'outlet_geography_approved':False,'note':'Open-boundary conditioning is algorithmic; coastal/river outlet positions not independently verified.'}
