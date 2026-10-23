"""Noncanonical terrain and flood sensitivity for supplemental cycle link."""
from math import hypot
from world.atlas.spatial.network_redundancy_gate import evaluate as redundancy
from world.atlas.spatial.candidate_validation import load_candidate
from world.atlas.spatial.candidate_comparison import compare_candidates
from world.atlas.spatial.route_alignment_gate import pathfind
from world.atlas.spatial.river_floodplain_gate import analyze_surface
from world.atlas.spatial.wide_corridor_route_gate import expand

def evaluate():
    fixture=load_candidate();points={x['location_id']:x['xy'] for x in fixture['anchors']+fixture['route_intermediates']}
    proposals=redundancy()['minimum_topological_solutions'];rows=[]
    for candidate in compare_candidates()['variants']:
        grid=candidate['heightfield'];n=len(grid)
        channels=set(map(tuple,analyze_surface(grid,channel_threshold=25)['channel_cells_xy']))
        for radius in (0,1,2):
            unsafe=expand(channels,n,radius)
            for proposal in proposals:
                for link in proposal['proposed_links']:
                    a,b=link['from'],link['to']
                    options=[pathfind(grid,points[a],points[b],unsafe,w) for w in (0,8,25)]
                    maxgrade=[]
                    for opt in options:
                        cells=opt['grid_cells'];grades=[abs(grid[y2][x2]-grid[y1][x1])/(50*hypot(x2-x1,y2-y1)) for (x1,y1),(x2,y2) in zip(cells,cells[1:])]
                        maxgrade.append(round(max(grades,default=0),6))
                    rows.append({'variant':candidate['variant'],'corridor_radius_cells':radius,'from':a,'to':b,
                                 'alternatives':[{'risk_weight':w,'candidate_length_m':o['length_m_candidate'],
                                                  'corridor_contact_cells':o['channel_contact_cells'],
                                                  'max_segment_grade':g,'route_approved':False}
                                                 for w,o,g in zip((0,8,25),options,maxgrade)],
                                 'high_water_redundancy_approved':False})
    return {'status':'SYNTHETIC_BACKUP_LINK_FEASIBILITY_SCREEN','results':rows,'acceptance':'HOLD',
            'limitations':['NO_APPROVED_WATERWAY_WIDTH','NO_CANONICAL_BACKUP_CORRIDOR','NO_SIMULTANEOUS_FAILURE_PROOF','NO_ENGINEERING_SITE_SURVEY']}
