"""Derived ground-contact placement audit; never modifies historical or canonical coordinates."""
from world.atlas.spatial.candidate_validation import load_candidate
from world.atlas.spatial.terrain_occlusion_gate import elevation
from world.atlas.spatial.landscape_experiment import build_landscape


def reconcile():
    fixture=load_candidate();grid=build_landscape()['heightfield']
    placements=[]
    for landmark in fixture['anchors']+fixture['route_intermediates']:
        x,y=landmark['xy'];ground=elevation(grid,x,y)
        if ground is None:raise ValueError('LANDMARK_OUTSIDE_SYNTHETIC_GRID')
        delta=round(landmark['z']-ground,4)
        placements.append({'location_id':landmark['location_id'], 'xy_candidate':[x,y],
         'original_z_candidate':landmark['z'], 'terrain_ground_z_candidate':round(ground,4),
         'original_vertical_offset_m_candidate':delta,
         'derived_ground_contact_xyz_candidate':[x,y,round(ground,4)],
         'structure_or_platform_height':'UNRESOLVED',
         'original_landmark_geometry_preserved':True,
         'derived_ground_contact_approved':False})
    return {'status':'NONCANONICAL_GROUND_CONTACT_DERIVATION',
            'region_id':'REG-CENTRAL-BASIN','source_fixture_status':fixture['status'],
            'placements':placements,'acceptance':'HOLD',
            'blocked_on':['SITE_FOUNDATION_TYPE_UNVERIFIED','NO_APPROVED_SURVEY_ELEVATIONS','NO_INDEPENDENT_SITE_REVIEW']}
