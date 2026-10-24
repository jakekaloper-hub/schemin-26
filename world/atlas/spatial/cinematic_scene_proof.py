"""Reproducible, inspectable noncanonical camera/terrain proof, not a visual signoff."""
import hashlib,json,math
from pathlib import Path
from world.atlas.spatial.mesh_export import render_obj
from world.atlas.spatial.candidate_validation import load_candidate

def build():
    raw=render_obj().encode()
    data=load_candidate()
    anchors=data['anchors']+data['route_intermediates']
    # Multiple real 3D virtual camera coordinates over a *single* immutable mesh.
    cameras=[{'id':'CB-NORTH-LOOK-SOUTH','xyz':[800,1350,145],'look_at':[700,600,20]},
             {'id':'CB-EAST-LOOK-WEST','xyz':[1450,700,130],'look_at':[700,550,20]},
             {'id':'CB-SOUTH-LOOK-NORTH','xyz':[780,-280,115],'look_at':[700,600,20]}]
    for cam in cameras:
        a=cam['xyz'];b=cam['look_at'];dx=b[0]-a[0];dy=b[1]-a[1];dz=b[2]-a[2]
        cam['yaw_deg']=round(math.degrees(math.atan2(dx,dy)),4)
        cam['pitch_deg']=round(math.degrees(math.atan2(dz,math.hypot(dx,dy))),4)
    landmarks=[{'location_id':a['location_id'],'synthetic_xyz':[a['xy'][0],a['xy'][1],a['z']],
                 'coordinate_authority':'EXPERIMENTAL_ONLY'} for a in anchors]
    return {'schema':'SCHEMIN_ENV_REFERENCE_CANDIDATE_V1','approval':'NOT_CANON_NOT_VISUALLY_REVIEWED',
            'mesh_sha256':hashlib.sha256(raw).hexdigest(),'camera_count':len(cameras),
            'cameras':cameras,'landmarks':landmarks,'terrain_units':'SYNTHETIC_METERS_NO_REAL_DISTANCE_CLAIM',
            'render_status':'GEOMETRY_AND_CAMERA_PACKET_ONLY_NO_RENDERED_PLATES',
            'reference_integrity':'ALL_CAMERAS_SHARE_ONE_MESH_HASH_AND_LANDMARK_PACK'}
