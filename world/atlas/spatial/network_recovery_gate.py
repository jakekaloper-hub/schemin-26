"""Synthetic alternative-route recovery after hypothetical high-water closures."""
from world.atlas.spatial.seasonal_network_resilience import evaluate as network
from world.atlas.spatial.wide_corridor_route_gate import evaluate as routes

def evaluate():
    route_index={(v['variant'],v['corridor_radius_cells']):v for v in routes()['results']}
    output=[]
    for row in network()['results']:
        if row['season']!='HIGH_WATER':continue
        candidate=route_index[(row['variant'],row['radius_cells'])]
        recovered=[]
        for s in candidate['segments']:
            clean=[o for o in s['options'] if o['corridor_contacts']==0]
            baseline=s['options'][0]['candidate_length']
            if clean:
                best=min(clean,key=lambda o:(o['candidate_length'],o['penalty']))
                status='EXPERIMENTAL_DETOUR_CANDIDATE'
                extra=round(best['candidate_length']-baseline,3)
            else:
                status='CROSSING_INFRASTRUCTURE_OR_UNMODELED_ROUTE_REQUIRED'
                extra=None
            recovered.append({'route_id':s['route_id'],'from':s['from'],'to':s['to'],
                              'recovery_status':status,'candidate_detour_extra_m':extra,
                              'historical_detour_approved':False})
        output.append({'variant':row['variant'],'radius_cells':row['radius_cells'],
                       'base_network_connected':row['all_landmarks_connected'],
                       'segment_recovery':recovered,'full_network_recovery_certified':False})
    return {'status':'SYNTHETIC_MITIGATION_DIAGNOSTIC_ONLY','results':output,'acceptance':'HOLD',
            'limitations':['NO_SURVEYED_ALTERNATE_ROADS','NO_VALIDATED_WATERWAY_GEOMETRY','NO_APPROVED_TRAVEL_TIME']}
