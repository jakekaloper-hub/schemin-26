"""Deterministic landmark projections from shared experimental geometry; NOT visual QA."""
import math
from world.atlas.spatial.cinematic_scene_proof import build

def project(camera,point):
    origin=camera['xyz'];target=camera['look_at']
    delta=[target[i]-origin[i] for i in range(3)];dist=math.sqrt(sum(x*x for x in delta))
    forward=[x/dist for x in delta]
    right=[forward[1],-forward[0],0.]
    n=math.hypot(right[0],right[1]);right=[x/n for x in right]
    up=[right[1]*forward[2]-right[2]*forward[1],right[2]*forward[0]-right[0]*forward[2],right[0]*forward[1]-right[1]*forward[0]]
    offset=[point[i]-origin[i] for i in range(3)]
    depth=sum(offset[i]*forward[i] for i in range(3))
    if depth<=0:return {'in_front':False,'uv':None}
    uv=[round(sum(offset[i]*axis[i] for i in range(3))/depth,6) for axis in (right,up)]
    return {'in_front':True,'uv':uv,'in_reference_frame':all(abs(x)<=1 for x in uv)}

def audit():
    pack=build()
    views=[]
    for camera in pack['cameras']:
        points=[{'location_id':p['location_id'],**project(camera,p['synthetic_xyz'])} for p in pack['landmarks']]
        views.append({'camera_id':camera['id'],'mesh_sha256':pack['mesh_sha256'],'projections':points})
    return {'scope':'SYNTHETIC_CAMERA_PROJECTION','views':views,'approval':'NOT_CANON_NOT_INDEPENDENTLY_VISUALLY_REVIEWED',
            'limitations':['NO_OCCLUSION_RAYTRACE','NO_HISTORICALLY_APPROVED_LANDMARK_FOOTPRINT','NO_VIEWER_ACCEPTANCE']}
