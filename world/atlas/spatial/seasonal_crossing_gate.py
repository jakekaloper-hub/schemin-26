"""Seasonal crossing candidates, explicitly uncalibrated and not infrastructure approvals."""
from world.atlas.spatial.crossing_infrastructure_gate import classify

SCENARIOS=(('DRY',0),('WET',1),('HIGH_WATER',2))

def evaluate():
    source=classify();rows=[]
    for model in source['results']:
        for name,severity in SCENARIOS:
            segments=[]
            for s in model['segments']:
                contact=s['corridor_contacts_high_penalty']>0
                # Exposure ratings are strictly ordinal scenario assumptions.
                risk=severity+(1 if contact else 0)
                candidates=(['ELEVATED_BRIDGE_REVIEW','DETOUR_REVIEW'] if severity==2 and contact
                    else ['BRIDGE_REVIEW','FORD_REVIEW','CAUSEWAY_REVIEW','DETOUR_REVIEW'] if contact
                    else ['NO_CROSSING_IDENTIFIED','DRAINAGE_REVIEW'])
                segments.append({'route_id':s['route_id'],'from':s['from'],'to':s['to'],
                    'candidate_channel_contact':contact,'scenario_risk_index':risk,
                    'possible_review_options':candidates,'ford_certified':False,
                    'passability_approved':False,'infrastructure_type_selected':None})
            rows.append({'variant':model['variant'],'corridor_radius_cells':model['corridor_radius_cells'],
                        'scenario':name,'scenario_severity_ordinal':severity,'segments':segments})
    return {'status':'UNCALIBRATED_SEASONAL_SCENARIO_SCREEN','results':rows,
            'approval':'HOLD','limitations':['NO_MEASURED_DEPTH_OR_VELOCITY','NO_RETURN_PERIOD','NO_HISTORICAL_BRIDGE_SITE','NO_APPROVED_SEASONAL_CLOSURE']}
