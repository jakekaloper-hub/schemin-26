"""Deterministic, NONCANONICAL Central Basin terrain and hydrology experiment.

No additional dependencies. A provisional heightfield is not a world elevation authority.
"""
from __future__ import annotations
from datetime import date
from math import cos, pi, sin, hypot
from world.atlas.spatial.candidate_packet import build_candidate_spatial_packet

def height(x:int,y:int,n:int)->float:
    # Broad southward decline, valley and deterministic two-ridge variation.
    return round(8 + 0.018*y + 7*sin(pi*x/(n-1))**2 +
                 5*cos(2*pi*y/(n-1))**2 + 3*sin(pi*(x+y)/(n-1))**2, 5)

def build_landscape(n:int=33,step_m:int=50,when:str="2026-10-21")->dict:
    if n<9 or n>129 or step_m<=0: raise ValueError("UNSUPPORTED_GRID_PARAMETERS")
    day=date.fromisoformat(when)
    packet=build_candidate_spatial_packet("2026-10-21")
    if not packet["ok"]: raise ValueError("CANON_CONTEXT_UNAVAILABLE")
    z=[[height(i,j,n) for i in range(n)] for j in range(n)]
    downstream={}
    sinks=[]
    for j in range(n):
        for i in range(n):
            neighbors=[(a,b) for b in range(max(0,j-1),min(n,j+2))
                       for a in range(max(0,i-1),min(n,i+2)) if (a,b)!=(i,j)]
            lower=[(a,b) for a,b in neighbors if z[b][a]<z[j][i]]
            if lower:
                # Steepest downhill gradient, fixed tie breaking.
                dest=max(lower,key=lambda q:((z[j][i]-z[q[1]][q[0]])/hypot(q[0]-i,q[1]-j),-q[1],-q[0]))
                downstream[(i,j)]=dest
            else:
                downstream[(i,j)]=None
                sinks.append((i,j))
    accumulation={(i,j):1 for j in range(n) for i in range(n)}
    for i,j in sorted(accumulation,key=lambda p:z[p[1]][p[0]],reverse=True):
        to=downstream[(i,j)]
        if to is not None: accumulation[to]+=accumulation[(i,j)]
    # Temperate illustrative cycle; numeric output carries no weather authority.
    days=(day-date(day.year,1,1)).days
    seasonal_c=round(12+10*sin(2*pi*(days-80)/365.25),3)
    return {"status":"DERIVED_SYNTHETIC_NOT_CANON","world_context_id":packet["shared_candidate_spatial_context"]["context_id"],
      "region_id":"REG-CENTRAL-BASIN","n":n,"step_m":step_m,"heightfield":z,
      "flow_edges":[[i,j,*to] for (i,j),to in sorted(downstream.items()) if to is not None],
      "sinks":[list(p) for p in sinks],"flow_accumulation":[[accumulation[(i,j)] for i in range(n)] for j in range(n)],
      "when":when,"season_temperature_c_hypothetical":seasonal_c,
      "explicit_limitations":["NO_CANONICAL_DISTANCE","NO_REAL_CLIMATE_CLAIM","NO_WATERSHED_APPROVAL","NO_RASTER_REFERENCE_CERTIFICATION"]}
