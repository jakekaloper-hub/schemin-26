"""Audit local synthetic basin against continental receiving-zone hypotheses."""
from world.atlas.spatial.continental_constraint_gate import validate
from world.atlas.spatial.candidate_comparison import compare_candidates
from world.atlas.spatial.outlet_gate import drain_to_boundary


def inspect():
    macro=validate()
    relations={(e['upstream'],e['downstream']) for e in macro['edges']}
    if ('REG-UPPER-VALLEYS','REG-CENTRAL-BASIN') not in relations or ('REG-CENTRAL-BASIN','REG-SOUTHERN-WETLANDS') not in relations:
        raise ValueError('MISSING_UPSTREAM_DOWNSTREAM_CONSTRAINT')
    rows=[]
    for v in compare_candidates()['variants']:
        z=v['heightfield']; n=len(z)
        routing=drain_to_boundary(z)
        parents={(x,y):(a,b) for x,y,a,b in routing['routing_parents']}
        terminals={tuple(p) for p in routing['terminal_boundary_cells']}
        basin={}
        for y in range(n):
            for x in range(n):
                p=(x,y)
                while p in parents:p=parents[p]
                basin[p]=basin.get(p,0)+1
        south=sum(c for (x,y),c in basin.items() if y==0)
        other=n*n-south
        rows.append({'variant':v['variant'],'cells':n*n,'hypothetical_south_receiving_cells':south,
                     'unresolved_other_edge_receiving_cells':other,'south_receiving_fraction':round(south/(n*n),6),
                     'has_unvalidated_other_edge_discharge':other>0,
                     'all_terminal_roots_identified':set(basin)==terminals,
                     'source_region':'REG-UPPER-VALLEYS','target_region':'REG-SOUTHERN-WETLANDS',
                     'geographically_approved':False})
    return {'phase':'P1','status':'CONTINENTAL_LOCAL_AUDIT_ONLY','results':rows,
            'acceptance':'HOLD','note':'Open grid edges are synthetic; other-edge discharge is not an approved coastline or river outlet.'}
