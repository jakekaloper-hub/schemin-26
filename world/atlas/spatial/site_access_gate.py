"""Synthetic route slope and site-access audit, never canonical travel proof."""
from math import hypot
from world.atlas.spatial.candidate_validation import load_candidate
from world.atlas.spatial.landscape_experiment import build_landscape
from world.atlas.spatial.terrain_occlusion_gate import elevation


def evaluate(samples=32,grade_limit=0.08):
    if samples<2 or grade_limit<=0:raise ValueError('INVALID_AUDIT_PARAMETERS')
    fixture=load_candidate();grid=build_landscape()['heightfield']
    points={p['location_id']:p['xy'] for p in fixture['anchors']+fixture['route_intermediates']}
    segments=[]
    for route in fixture['paths']:
        for origin,destination in zip(route['locations'],route['locations'][1:]):
            a,b=points[origin],points[destination]
            distance=hypot(b[0]-a[0],b[1]-a[1]); step=distance/samples
            heights=[elevation(grid,a[0]+(b[0]-a[0])*k/samples,a[1]+(b[1]-a[1])*k/samples) for k in range(samples+1)]
            if step<=0 or any(v is None for v in heights):raise ValueError('INVALID_ROUTE_GEOMETRY')
            grades=[abs(v-u)/step for u,v in zip(heights,heights[1:])]
            segments.append({'route_id':route['route_id'],'from':origin,'to':destination,
                             'synthetic_straight_line_length_m':round(distance,3),
                             'peak_absolute_grade':round(max(grades),6),
                             'exceeds_review_grade_limit':max(grades)>grade_limit,
                             'requires_crossing_review':True,'route_feasible_approved':False})
    sites=[]
    for loc in fixture['anchors']+fixture['route_intermediates']:
        x,y=loc['xy'];center=elevation(grid,x,y)
        surrounding=[elevation(grid,x+dx,y+dy) for dx,dy in ((-25,0),(25,0),(0,-25),(0,25))]
        if any(v is None for v in surrounding):raise ValueError('SITE_NEAR_UNMODELED_EDGE')
        sites.append({'location_id':loc['location_id'],
                      'max_local_grade_candidate':round(max(abs(v-center)/25 for v in surrounding),6),
                      'foundation_type':'UNVERIFIED','site_certified':False})
    return {'status':'SITE_AND_ROUTE_SCREEN_ONLY','segments':segments,'sites':sites,
            'review_grade_limit':grade_limit,'acceptance':'HOLD',
            'limitations':['STRAIGHT_LINE_PATHS_NOT_ENGINEERED_ROADS','CROSSING_LOCATIONS_UNVERIFIED','SYNTHETIC_METRIC_DISTANCE_NOT_CANON']}
