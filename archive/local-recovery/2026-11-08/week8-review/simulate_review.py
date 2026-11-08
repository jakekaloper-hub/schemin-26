import json,pathlib,collections,hashlib
root=pathlib.Path.home()/'Developer/ai/schemin-visual-local'
d=json.loads((root/'week8-review/week8_packets.json').read_text())
repo=root/'repo'
routes=json.loads((repo/'world/data/routes.json').read_text())['routes']
g=collections.defaultdict(list)
for r in routes:
 seq=[r['from']]+([r['via_location_id']] if r.get('via_location_id') else r.get('via_location_ids',[]))+[r['to']]
 for a,b in zip(seq,seq[1:]):g[a].append(b);g[b].append(a)
domains={x['team_id']:x for x in json.loads((repo/'world/data/owner_domains.json').read_text())['domains']}
cases={}
for p in d['packets']:
 k=p['story']
 if k in cases:continue
 src=domains[p['away_team_id']]['primary_location_id'];dest=p['location_id'];seen={src};q=collections.deque([src])
 while q:
  v=q.popleft()
  for n in g[v]:
   if n not in seen:seen.add(n);q.append(n)
 cases[k]={'route_connected':dest in seen,'packets':len([x for x in d['packets'] if x['story']==k])}
checks={'all_12_reference_hashes_match':all(x['hash_verified'] for x in d['references'].values()),'all_6_route_graph_connected':all(x['route_connected'] for x in cases.values()),'all_28_canvas_correct':all(x['canvas']==[1080,1920] for x in d['packets']),'all_6_have_overture':all(any(x['story']==k and x['layout'].startswith('two equal') for x in d['packets']) for k in cases),'all_6_have_dual_outcome':all(any(x['story']==k and 'A home wins' in x['result_branch'] for x in d['packets']) for k in cases)}
blocks=['GOTW neutral-site formal admission not proven','Week 4-7 entering World State not reconstructed','No authenticated independent Steward / Fact Lock','Reference crop hashes pass but render mount not proven','No final ESPN winner certification','No actual visual raster QA or Founder final approval']
report={'review_type':'LOCAL_SIMULATED_BULLPEN_REVIEW_NOT_AUTHENTICATED_INDEPENDENT_UMPIRE','checks':checks,'matchups':cases,'blocking_items':blocks,'disposition':'CONDITIONAL_PREPRODUCTION_PASS; RELEASE_BLOCKED','approval':'NOT GRANTED'}
(root/'week8-review/simulated_umpire_report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
