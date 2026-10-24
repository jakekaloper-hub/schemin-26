"""Scenario-robust synthetic edge-repair portfolio; no canonical capital investment."""
from itertools import combinations
from world.atlas.spatial.seasonal_crossing_gate import evaluate as seasons
from world.atlas.spatial.seasonal_network_resilience import components
from world.atlas.spatial.candidate_validation import load_candidate

def evaluate():
    fixture=load_candidate();nodes={p['location_id'] for p in fixture['anchors']+fixture['route_intermediates']}
    scenarios=seasons()['results'];all_edges=sorted({(s['route_id'],s['from'],s['to']) for row in scenarios for s in row['segments']})
    portfolios=[]
    for k in range(len(all_edges)+1):
        for subset in combinations(all_edges,k):
            supported=set(subset);passes=True
            for row in scenarios:
                viable=[(s['from'],s['to']) for s in row['segments']
                        if not (row['scenario']=='HIGH_WATER' and s['candidate_channel_contact'])
                        or (s['route_id'],s['from'],s['to']) in supported]
                if len(components(nodes,viable))!=1:passes=False;break
            if passes:portfolios.append([{'route_id':a,'from':b,'to':c} for a,b,c in subset])
        if portfolios:break
    if not portfolios:raise ValueError('NO_ROBUST_PORTFOLIO')
    return {'status':'SYNTHETIC_CROSS_SCENARIO_ROBUST_PORTFOLIO','scenario_count':len(scenarios),
            'edge_count':len(all_edges),'minimum_permanent_repair_count':len(portfolios[0]),
            'minimum_portfolios':portfolios,'approved_investments':False,'acceptance':'HOLD',
            'limitations':['REPAIR_COSTS_UNKNOWN','NO_APPROVED_BRIDGES','SEASONAL_CLOSURES_HYPOTHETICAL','NO_INDEPENDENT_GEOGRAPHIC_APPROVAL']}
