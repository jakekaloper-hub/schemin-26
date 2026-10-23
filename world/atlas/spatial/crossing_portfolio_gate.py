"""Exact minimum-cardinality synthetic crossing repair portfolios; no cost claim."""
from itertools import combinations
from world.atlas.spatial.seasonal_crossing_gate import evaluate as seasons
from world.atlas.spatial.seasonal_network_resilience import components
from world.atlas.spatial.candidate_validation import load_candidate

def evaluate():
    fixture=load_candidate();nodes={p['location_id'] for p in fixture['anchors']+fixture['route_intermediates']}
    reports=[]
    for scenario in seasons()['results']:
        if scenario['scenario']!='HIGH_WATER':continue
        open_edges=[(s['from'],s['to']) for s in scenario['segments'] if not s['candidate_channel_contact']]
        closed=[(s['from'],s['to'],s['route_id']) for s in scenario['segments'] if s['candidate_channel_contact']]
        minimal=[]
        for count in range(len(closed)+1):
            for subset in combinations(closed,count):
                edges=open_edges+[(a,b) for a,b,_ in subset]
                if len(components(nodes,edges))==1:
                    minimal.append([{'route_id':route_id,'from':a,'to':b} for a,b,route_id in subset])
            if minimal:break
        if not minimal:raise ValueError('NO_RECOVERY_WITH_CANONICAL_GRAPH')
        reports.append({'variant':scenario['variant'],'corridor_radius_cells':scenario['corridor_radius_cells'],
             'initial_component_count':len(components(nodes,open_edges)),
             'minimum_repairs_for_full_connectivity':len(minimal[0]),
             'all_minimum_portfolios':minimal,'capital_cost_computed':False,
             'approved_infrastructure':False})
    return {'status':'MIN_CARDINALITY_SYNTHETIC_REPAIR_PORTFOLIOS','results':reports,'acceptance':'HOLD',
     'limitations':['NO_CONSTRUCTION_COSTS','NO_APPROVED_BRIDGE_LOCATIONS','NO_VERIFIED_HYDRAULICS','MINIMUM_EDGE_COUNT_NOT_MINIMUM_INVESTMENT']}
