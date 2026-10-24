"""Classify *candidate* infrastructure needs; no invented canonical bridges."""
from world.atlas.spatial.wide_corridor_route_gate import evaluate as wide_routes
from world.atlas.spatial.site_access_gate import evaluate as site_access


def classify():
    sources=wide_routes()['results'];grades=site_access()['segments']
    grade_index={(s['route_id'],s['from'],s['to']):s['peak_absolute_grade'] for s in grades}
    rows=[]
    for model in sources:
        items=[]
        for segment in model['segments']:
            key=(segment['route_id'],segment['from'],segment['to'])
            grade=grade_index[key]
            preferred=segment['options'][-1]
            contact=preferred['corridor_contacts']>0
            # Existence of contact is not evidence of width, depth, substrate or historic bridge.
            candidates=['BRIDGE','FORD','CAUSEWAY','REROUTE'] if contact else ['NO_DETECTED_CROSSING','REROUTE']
            items.append({'route_id':key[0],'from':key[1],'to':key[2],
                          'peak_grade_straight_candidate':grade,
                          'corridor_contacts_high_penalty':preferred['corridor_contacts'],
                          'candidate_treatments':candidates,
                          'classification':'CROSSING_REVIEW_REQUIRED' if contact else 'NO_CROSSING_DETECTED_AT_THIS_ASSUMPTION',
                          'verified_infrastructure':'NONE','crossing_type_selected':None,
                          'hydraulic_and_foundation_review':'REQUIRED' if contact else 'NOT_TRIGGERED',
                          'historical_approval':False})
        rows.append({'variant':model['variant'],'corridor_radius_cells':model['corridor_radius_cells'],'segments':items})
    return {'status':'SYNTHETIC_INFRASTRUCTURE_FEASIBILITY_SCREEN', 'results':rows,
            'acceptance':'HOLD','blocks':['NO_APPROVED_RIVER_WIDTH_OR_FLOW','NO_CROSSING_FOUNDATIONS','NO_CONFIRMED_HISTORICAL_BRIDGE_SITE','NO_APPROVED_ROUTE_CENTERLINE']}
