"""Separate publication observations from binding physical constraints."""
from world.atlas.spatial.memo_archive_grounding import resolve_central_basin_evidence
from world.atlas.spatial.candidate_validation import load_candidate


def build_historical_constraints():
    observations=resolve_central_basin_evidence()['locations']
    source=load_candidate()
    anchors=[x['location_id'] for x in source['anchors']]
    intermediates=[x['location_id'] for x in source['route_intermediates']]
    routes=[{'route_id':r['route_id'],'ordered_location_ids':r['locations'],
             'geometry_approved':False,'metric_distance_approved':False}
            for r in source['paths']]
    return {'status':'EVIDENCE_CONSTRAINED_CANDIDATE_NOT_CANON',
      'region_id':source['region_id'],
      'landmark_ids':anchors+intermediates,
      'historical_observations':observations,
      'route_topology_constraints':routes,
      'physical_requirements':{
        'uplands_feed_central_basin':True,
        'central_basin_drains_towards_southern_lowlands':True,
        'roads_require_viable_grade_and_crossings':True,
        'metric_scale_and_landmark_footprints_approved':False},
      'prohibited_inferences':['ILLUSTRATED_WATERFALL_IMPLIES_PITTSYS_DISTANCE',
        'ARTWORK_LABEL_POSITION_EQUALS_METRIC_COORDINATE',
        'WEEK5_ARTWORK_REVIEW_EQUALS_RELEASE_ACCEPTANCE'],
      'authorization':'RESEARCH_AND_SIMULATION_ONLY'}
