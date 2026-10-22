"""Synthetic grade audit; all distances are candidate-only, never canonical travel times."""
from __future__ import annotations
from math import hypot
from world.atlas.spatial.landscape_experiment import build_landscape
from world.atlas.spatial.candidate_validation import load_candidate

def route_grade_report(n=33,step_m=50):
    landscape=build_landscape(n=n,step_m=step_m)
    grid=landscape["heightfield"]
    extent=(n-1)*step_m
    src=load_candidate()
    positions={i["location_id"]:i["xy"] for i in src["anchors"]+src["route_intermediates"]}
    def elevation(x,y):
        if not 0<=x<=extent or not 0<=y<=extent: raise ValueError("OUTSIDE_TERRAIN")
        u,v=x/step_m,y/step_m
        i,j=min(int(u),n-2),min(int(v),n-2)
        a,b=u-i,v-j
        return grid[j][i]*(1-a)*(1-b)+grid[j][i+1]*a*(1-b)+grid[j+1][i]*(1-a)*b+grid[j+1][i+1]*a*b
    results=[]
    for route in src["paths"]:
        stops=route["locations"]
        segments=[]
        for start,end in zip(stops,stops[1:]):
            x0,y0=positions[start];x1,y1=positions[end]
            length=hypot(x1-x0,y1-y0)
            if length<=0:raise ValueError("DEGENERATE_ROUTE")
            # Sample at no more than half-grid spacing.
            samples=max(2,int(length/(step_m/2))+1)
            values=[elevation(x0+(x1-x0)*k/samples,y0+(y1-y0)*k/samples) for k in range(samples+1)]
            max_grade=max(abs(b-a)/(length/samples) for a,b in zip(values,values[1:]))
            segments.append({"from":start,"to":end,"synthetic_length_m":round(length,2),"maximum_sampled_grade":round(max_grade,5)})
        results.append({"route_id":route["route_id"],"segments":segments})
    return {"status":"SYNTHETIC_NOT_CANON","routes":results,"limits":["NOT_ROUTE_CERTIFICATION","NOT_CANONICAL_DISTANCE","NO_BRIDGE_OR_SOIL_MODEL"]}
