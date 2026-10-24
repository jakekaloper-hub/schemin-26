"""Candidate network connectivity after hypothetical high-water crossing closures."""
from collections import deque
from world.atlas.spatial.seasonal_crossing_gate import evaluate as scenarios
from world.atlas.spatial.candidate_validation import load_candidate


def components(nodes, edges):
    adjacency={n:set() for n in nodes}
    for a,b in edges:
        adjacency[a].add(b);adjacency[b].add(a)
    result=[];unseen=set(nodes)
    while unseen:
        start=min(unseen);visited={start};queue=deque([start]);unseen.remove(start)
        while queue:
            p=queue.popleft()
            for q in sorted(adjacency[p]):
                if q in unseen:unseen.remove(q);visited.add(q);queue.append(q)
        result.append(sorted(visited))
    return sorted(result,key=lambda x:x[0])

def evaluate():
    source=load_candidate();ids={p['location_id'] for p in source['anchors']+source['route_intermediates']}
    rows=[]
    for scenario in scenarios()['results']:
        all_edges=[(s['from'],s['to']) for s in scenario['segments']]
        open_edges=[(s['from'],s['to']) for s in scenario['segments'] if not(scenario['scenario']=='HIGH_WATER' and s['candidate_channel_contact'])]
        groups=components(ids,open_edges)
        rows.append({'variant':scenario['variant'],'radius_cells':scenario['corridor_radius_cells'],'season':scenario['scenario'],
                     'base_route_edges':len(all_edges),'passable_edges_hypothesis':len(open_edges),
                     'closed_edges_hypothesis':len(all_edges)-len(open_edges),
                     'connected_components':groups,'isolated_landmarks':[group[0] for group in groups if len(group)==1],
                     'all_landmarks_connected':len(groups)==1,'verified_real_closure':False})
    return {'status':'SYNTHETIC_NETWORK_RESILIENCE_ONLY','results':rows,'acceptance':'HOLD',
            'limitations':['NO_AUTHORIZED_SEASONAL_ROAD_CLOSURES','NO_VERIFIED_ALTERNATE_ROADS','DETOUR_TIME_NOT_ESTABLISHED']}
