"""Find minimum synthetic supplemental links for resilience to any one edge failure."""
from itertools import combinations
from math import hypot
from world.atlas.spatial.candidate_validation import load_candidate
from world.atlas.spatial.seasonal_network_resilience import components

def evaluate():
    data=load_candidate();sites={x['location_id']:x['xy'] for x in data['anchors']+data['route_intermediates']}
    base=[tuple(sorted((a,b))) for route in data['paths'] for a,b in zip(route['locations'],route['locations'][1:])]
    base=set(base);names=sorted(sites)
    potential=[(a,b) for a,b in combinations(names,2) if (a,b) not in base]
    solutions=[]
    for count in range(len(potential)+1):
        for selection in combinations(potential,count):
            new_edges=base|set(selection)
            if all(len(components(names,new_edges-{edge}))==1 for edge in new_edges):
                solutions.append(selection)
        if solutions:break
    if not solutions:raise ValueError('NO_SINGLE_FAILURE_TOLERANT_NETWORK')
    result=[]
    for solution in solutions:
        result.append({'proposed_links':[{'from':a,'to':b,'synthetic_straight_distance_m':round(hypot(sites[a][0]-sites[b][0],sites[a][1]-sites[b][1]),3),
                                            'engineering_feasible':False,'approved_route':False} for a,b in solution],
                       'survives_any_one_edge_failure':True})
    return {'status':'SYNTHETIC_GRAPH_REDUNDANCY_ONLY','existing_edge_count':len(base),
            'candidate_new_link_count':len(potential),'minimum_added_links':len(solutions[0]),
            'minimum_topological_solutions':result,'acceptance':'HOLD',
            'limitations':['NO_TERRAIN_ROUTE_SURVEY','NO_SEASONAL_COFAILURE_MODEL','NO_APPROVED_NEW_ROAD','GRAPH_OPTIMAL_NOT_FINANCIALLY_OPTIMAL']}
