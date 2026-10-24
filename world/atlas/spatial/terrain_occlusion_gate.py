"""Sample synthetic heightfield for camera-to-landmark occlusion; no geographic approval."""
import math
from world.atlas.spatial.landscape_experiment import build_landscape
from world.atlas.spatial.cinematic_scene_proof import build
from world.atlas.spatial.camera_projection_audit import project

def elevation(grid,x,y,step=50):
    n=len(grid);u=x/step;v=y/step
    if not (0<=u<=n-1 and 0<=v<=n-1):return None
    i=min(int(u),n-2);j=min(int(v),n-2);u-=i;v-=j
    return ((1-v)*((1-u)*grid[j][i]+u*grid[j][i+1])+
            v*((1-u)*grid[j+1][i]+u*grid[j+1][i+1]))

def occluded(camera_xyz,point_xyz,grid,samples=256,clearance=0):
    if samples<2:raise ValueError('INSUFFICIENT_SAMPLES')
    for k in range(1,samples):
        t=k/samples;x=camera_xyz[0]+t*(point_xyz[0]-camera_xyz[0]);y=camera_xyz[1]+t*(point_xyz[1]-camera_xyz[1]);z=camera_xyz[2]+t*(point_xyz[2]-camera_xyz[2])
        ground=elevation(grid,x,y)
        if ground is not None and ground+clearance>z:return True
    return False

def audit():
    pack=build();grid=build_landscape()['heightfield']
    rows=[]
    for cam in pack['cameras']:
        items=[]
        for site in pack['landmarks']:
            pos=site['synthetic_xyz'];frame=project(cam,pos)
            items.append({'location_id':site['location_id'],'in_frame':frame.get('in_reference_frame',False),
                          'terrain_occluded':occluded(cam['xyz'],pos,grid),
                          'visibility_certified':False})
        rows.append({'camera_id':cam['id'],'landmarks':items})
    return {'status':'SYNTHETIC_LINE_OF_SIGHT_DIAGNOSTIC','views':rows,
            'approval':'HOLD','limitations':['NO_BUILDINGS_OR_VEGETATION_OCCLUSION','SAMPLED_HEIGHTFIELD_NOT_EXACT_RAY_TRIANGLE','SYNTHETIC_LANDMARK_ELEVATIONS']}
