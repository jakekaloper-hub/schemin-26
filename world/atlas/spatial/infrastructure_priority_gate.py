"""Rank single-edge hypothetical repairs by restored landmark pairs, not money."""
from itertools import combinations
from world.atlas.spatial.seasonal_crossing_gate import evaluate as seasonal
from world.atlas.spatial.seasonal_network_resilience import components
from world.atlas.spatial.candidate_validation import load_candidate

def connected_pairs(groups):
    return sum(len(g)*(len(g)-1)//2 for g in groups)

def evaluate():
    fixture=load_candidate();nodes={p['location_id'] for p in fixture['anchors']+fixture['route_intermediates']}
    reports=[]
    for row in seasonal()['results']:
        if row['scenario']!='HIGH_WATER':continue
        open_edges=[(x['from'],x['to']) for x in row['segments'] if not x['candidate_channel_contact']]
        closed=[x for x in row['segments'] if x['candidate_channel_contact']]
        before=components(nodes,open_edges);baseline=connected_pairs(before)
        options=[]
        for item in closed:
            edge=(item['from'],item['to']);after=components(nodes,open_edges+[edge]);gain=connected_pairs(after)-baseline
            options.append({'route_id':item['route_id'],'from':edge[0],'to':edge[1],
              'restored_connected_pairs':gain,'remaining_components':len(after),
              'cost_estimate':'NOT_AVAILABLE','infrastructure_type':'UNDETERMINED',
              'historically_approved':False})
        options.sort(key=lambda x:(-x['restored_connected_pairs'],x['route_id'],x['from'],x['to']))
        reports.append({'variant':row['variant'],'corridor_radius_cells':row['corridor_radius_cells'],
          'baseline_components':len(before),'baseline_connected_pairs':baseline,
          'candidate_single_edge_repairs':options,'winner_authorized':False})
    return {'status':'SYNTHETIC_SINGLE_EDGE_CONNECTIVITY_RANKING','results':reports,'acceptance':'HOLD',
       'limitations':['NO_COSTS_OR_CONSTRUCTION_FEASIBILITY','NO_APPROVED_WATERWAY_WIDTH','NO_CANONICAL_BRIDGE_SITE','MULTI_EDGE_BUDGET_OPTIMIZATION_NOT_PERFORMED']}
