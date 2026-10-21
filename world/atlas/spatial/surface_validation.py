"""Bounded synthetic terrain/footprint/route/season QA. Never canonical geography."""
from __future__ import annotations
from math import hypot, isfinite
from world.atlas.spatial.candidate_validation import load_candidate, validate_candidate

def cross(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def polygon_valid(poly):
    if len(poly)<3 or len(set(map(tuple,poly)))!=len(poly): return False
    area=sum(poly[i][0]*poly[(i+1)%len(poly)][1]-poly[(i+1)%len(poly)][0]*poly[i][1] for i in range(len(poly)))
    if abs(area)<0.001: return False
    # Detect non-adjacent proper edge crossings and collinear overlap.
    def touches(a,b,c,d):
        x1,x2=cross(a,b,c),cross(a,b,d)
        y1,y2=cross(c,d,a),cross(c,d,b)
        return x1*x2<=0 and y1*y2<=0
    n=len(poly)
    for i in range(n):
        for j in range(i+1,n):
            if j==i+1 or (i==0 and j==n-1): continue
            if touches(poly[i],poly[(i+1)%n],poly[j],poly[(j+1)%n]): return False
    return True

def validate_surface(data):
    errors=[]
    grid=data.get("surface",{})
    heights=grid.get("heights",[])
    width=grid.get("width")
    if not isinstance(width,int) or width<2 or not heights or any(not isinstance(row,list) or len(row)!=width or any(type(z) not in (float,int) or not isfinite(z) for z in row) for row in heights):
        return ["INVALID_TERRAIN_GRID"]
    height=len(heights)
    dx=grid.get("step_m")
    if type(dx) not in (int,float) or dx<=0: return ["INVALID_GRID_SCALE"]
    bounds=(0,(width-1)*dx,0,(height-1)*dx)
    def inside(xy):
        return bounds[0]<=xy[0]<=bounds[1] and bounds[2]<=xy[1]<=bounds[3]
    def elevation(xy):
        x,y=xy[0]/dx,xy[1]/dx
        i,j=min(int(x),width-2),min(int(y),height-2)
        u,v=x-i,y-j
        z00,z10=heights[j][i],heights[j][i+1]
        z01,z11=heights[j+1][i],heights[j+1][i+1]
        return z00*(1-u)*(1-v)+z10*u*(1-v)+z01*(1-u)*v+z11*u*v
    features=data.get("footprints",[])
    expected={x["location_id"] for x in load_candidate()["anchors"]+load_candidate()["route_intermediates"]}
    if {f.get("location_id") for f in features}!=expected: errors.append("FOOTPRINT_ID_DRIFT")
    for f in features:
        poly=f.get("ring",[])
        if not polygon_valid(poly): errors.append("INVALID_FOOTPRINT")
        if any(not inside(p) for p in poly): errors.append("FOOTPRINT_OUTSIDE_GRID")
    for route in data.get("route_geometries",[]):
        points=route.get("polyline",[])
        if len(points)<2 or any(not inside(p) for p in points) or any(hypot(b[0]-a[0],b[1]-a[1])==0 for a,b in zip(points,points[1:])):
            errors.append("INVALID_ROUTE_GEOMETRY")
    reference=load_candidate()
    anchors={a["location_id"]:a["xy"] for a in reference["anchors"]+reference["route_intermediates"]}
    routes={r["route_id"]:r for r in reference["paths"]}
    for route in data.get("route_geometries",[]):
        ref=routes.get(route.get("route_id"))
        polyline=route.get("polyline",[])
        if ref and len(polyline)>=2:
            points=[anchors[i] for i in ref["locations"]]
            if len(polyline)!=len(points) or any(hypot(a[0]-b[0],a[1]-b[1])>0.01 for a,b in zip(polyline,points)):
                errors.append("ROUTE_ALIGNMENT_DRIFT")
    if {p["route_id"] for p in data.get("route_geometries",[])}!={p["route_id"] for p in reference["paths"]}: errors.append("ROUTE_ID_DRIFT")
    drains=data.get("drainage",[])
    nodes={n.get("id"):n for n in drains}
    if len(nodes)!=len(drains) or not nodes: errors.append("INVALID_DRAINAGE")
    for n in drains:
        xy=n.get("xy",[])
        if len(xy)!=2 or not inside(xy): errors.append("DRAINAGE_OUTSIDE_GRID");continue
        if abs(n.get("surface_z",-10000)-elevation(xy))>0.01: errors.append("DRAINAGE_ELEVATION_MISMATCH")
        downstream=n.get("downstream")
        if downstream is not None:
            if downstream not in nodes: errors.append("DRAINAGE_MISSING_OUTLET")
            elif n["surface_z"]<=nodes[downstream]["surface_z"]: errors.append("UPHILL_FLOW")
    for source in nodes:
        seen=set()
        point=source
        while point in nodes:
            if point in seen: errors.append("DRAINAGE_CYCLE");break
            seen.add(point)
            point=nodes[point].get("downstream")
            if point is None: break
    seasons=data.get("seasonal_fields",[])
    if {s.get("date") for s in seasons}!={s["date"] for s in reference["scenarios"]}: errors.append("SEASON_DATE_DRIFT")
    if any(s.get("status")!="HYPOTHETICAL" for s in seasons): errors.append("SEASON_AUTHORITY_DRIFT")
    return sorted(set(errors))
