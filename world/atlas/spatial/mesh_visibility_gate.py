"""Exact triangle intersection against the noncanonical synthetic OBJ terrain."""
from world.atlas.spatial.mesh_export import render_obj
from world.atlas.spatial.cinematic_scene_proof import build
from world.atlas.spatial.terrain_occlusion_gate import elevation

def geometry():
    vertices=[];faces=[]
    for line in render_obj().splitlines():
        if line.startswith('v '):vertices.append(tuple(float(x) for x in line.split()[1:]))
        if line.startswith('f '):faces.append(tuple(int(x)-1 for x in line.split()[1:]))
    return vertices,faces

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def segment_hits_triangle(start,end,a,b,c,eps=1e-8):
    direction=sub(end,start);edge1=sub(b,a);edge2=sub(c,a)
    p=cross(direction,edge2);det=dot(edge1,p)
    if abs(det)<eps:return False
    inv=1/det;t=sub(start,a);u=dot(t,p)*inv
    if u < -eps or u > 1+eps:return False
    q=cross(t,edge1);v=dot(direction,q)*inv
    if v < -eps or u+v > 1+eps:return False
    distance=dot(edge2,q)*inv
    return eps < distance < 1-eps

def audit():
    vertices,faces=geometry();scene=build();checks=[]
    for camera in scene['cameras']:
        landmarks=[]
        for site in scene['landmarks']:
            start=camera['xyz'];end=site['synthetic_xyz']
            hits=sum(segment_hits_triangle(start,end,vertices[i],vertices[j],vertices[k]) for i,j,k in faces)
            # NOTE: a landmark below the ground is not a legitimate visible target.
            ground=elevation_grid_at(end[0],end[1])
            landmarks.append({'location_id':site['location_id'],'triangle_intersections':hits,
                              'mesh_occluded':hits>0,'synthetic_surface_delta_m':round(end[2]-ground,4),
                              'surface_aligned_1m':abs(end[2]-ground)<=1})
        checks.append({'camera_id':camera['id'],'landmarks':landmarks})
    return {'scope':'EXACT_SYNTHETIC_OBJ_TRIANGLES','vertex_count':len(vertices),'triangle_count':len(faces),
            'camera_checks':checks,'acceptance':'HOLD','geographic_certified':False}

def elevation_grid_at(x,y):
    from world.atlas.spatial.landscape_experiment import build_landscape
    return elevation(build_landscape()['heightfield'],x,y)
