from pathlib import Path
from datetime import datetime,timezone
import json
E=Path(__file__).resolve().parent;R=E.parents[3];P=R/'memo-os/week-10/preproduction'
reviews=json.loads((E/'bullpen-review-results.json').read_text());assert reviews['expected']==reviews['returned']==38
fresh=json.loads((E/'fresh-sports-audit.json').read_text());players={x['name']:x for x in fresh['rosters']}
assert players['Patrick Mahomes']['team_id']==11
applied={
 'the_pitching_coach':('APPLIED','W10-P08 camera explicitly shows shallow water curling around the sandbag into existing ruts; no tidal wall.','issue-previs.json#W10-P08'),
 'the_umpire':('APPLIED','W10-P20 explicitly frames both stacked burger layers, open box, separate sideboard cake.','issue-previs.json#W10-P20'),
 'jk_rowling':('APPLIED','W10-P21 camera and continuity explicitly remove candles before cake contact; separate burger untouched.','issue-previs.json#W10-P21'),
 'the_beat_writer':('ADAPTED','The single surviving battery has multiple barrels converging; do not invent another functional emplacement.','issue-previs.json#W10-P24'),
 'the_bookkeeper':('ADAPTED','Wet rope, mud, hand-tied finish, hat location and no belt/property transfer made explicit.','issue-previs.json#W10-P07'),
 'unit_stills':('ADAPTED','No existing image proves a lifted cake. P20 camera now expressly leaves it on the sideboard; the actual lift belongs before P21.','issue-previs.json#W10-P20'),
 'the_gm':('ALREADY_SATISFIED','Scoreboard deck, every row and sports-policy already explicitly state provisional/ESPN finality pending.','issue-previs.json#W10-P04'),
 'character_vfx':('ALREADY_SATISFIED','Unposted and UNDECIDED describe the same current state; live provider confirms six undecided winners.','fresh-sports-audit.json'),
 'vfx_pipeline':('ALREADY_SATISFIED','The scene is labeled a current-leading-score branch, not an official result; request sports-policy and output footer preserve forecast scope.','render-inputs/W10-P24/request.json'),
 'the_groundskeeper':('ALREADY_SATISFIED','P30 states the precise conditional premise, 6–8 division route and loss consequence. Full constructive witnesses are retained in playoff-witnesses-pass3.json; do not invent odds or burden the page with all permutations.','playoff-witnesses-pass3.json'),
 'the_librarian':('ALREADY_SATISFIED','P30 links actual saved constructive playoff witnesses; the page is a concise conditional roadmap, not an exhaustive scenario dump.','playoff-witnesses-pass3.json'),
 'the_commissioner_general':('REJECTED_SOURCE_CONTRADICTION','Fresh ESPN player roster lists Isaiah Likely as TE. The unsupported WR replacement would corrupt the sports page.','fresh-sports-audit.json'),
 'the_clubhouse_manager':('REJECTED_SOURCE_CONTRADICTION','Official published Week 9 physical pages17–19 establish the cookout LAST week; current week10 is birthday retaliation.','precedent-w09-p19.jpg'),
 'george_rr_martin':('REJECTED_SOURCE_CONTRADICTION','Patrick Mahomes is rostered by Seven Deadly Chins (team11), not Red Leopards. Fresh roster was checked directly.','fresh-sports-audit.json'),
 'production_design':('REJECTED_SOURCE_CONTRADICTION','Patrick Mahomes is rostered by Seven Deadly Chins (team11), not The Chili Cheesers.','fresh-sports-audit.json'),
 'the_warden':('REJECTED_SOURCE_CONTRADICTION','Seven Deadly Chins is the registered Ben Whipple identity, with approved hash-verified character crop.','character-byte-recovery.json'),
 'the_agent':('REJECTED_SOURCE_CONTRADICTION','Changing PROVISIONAL to FINAL contradicts six live UNDECIDED winner fields.','fresh-sports-audit.json'),
 'editing':('REJECTED_SOURCE_CONTRADICTION','Changing PROVISIONAL to FINAL contradicts six live UNDECIDED winner fields.','fresh-sports-audit.json'),
 'brandon_sanderson':('REJECTED_FALSE_PREMISE','Every current score is labeled provisional; source-backed current values are not final results. Unresolved values remain blank.','render-inputs/W10-P04/request.json'),
 'jrr_tolkien':('REJECTED_UNSUBSTANTIATED','No differing score is identified; all12 displayed values independently match fresh Flaim and ESPN starter sums.','fresh-sports-audit.json'),
 'performance':('REJECTED_FALSE_PREMISE','The criticized and proposed camera descriptions already describe the same briefing-table composition. Published opening references and current page agree.','render-inputs/W10-P02/request.json')}
rows=[]
for r in reviews['results']:
 assert r['status']=='returned' and isinstance(r['structured']['findings'],list)
 for i,f in enumerate(r['structured']['findings']):
  if r['id'] in applied:status,reason,source=applied[r['id']]
  elif any(x in (f['observation']+' '+f['required_fix']).lower() for x in ['headline','page title']):status,reason,source='REJECTED_CREATIVE_REGRESSION','Metaphorical story titles are intentional and separate from dominant department headings. A location description is not a mandatory story title.','issue-draft.md and published Opening Drive references'
  elif any(x in f['observation'].lower() for x in ['image shows','visual observation','generic burger']):status,reason,source='REJECTED_FABRICATED_OUTPUT_OBSERVATION','No new Week10 raster exists. A style/location reference is not a generated Week10 page, and different page references must not be conflated. Preserve wet rope, mud and approved locations.','render-inputs/manifest.json'
  else:status,reason,source='REJECTED_UNSUBSTANTIATED','The note does not demonstrate a contradiction in the supplied page contract; no unsupported change to canon or creative direction is authorized.','issue-previs.json'
  rows.append({'reviewer_kind':r['kind'],'reviewer_id':r['id'],'finding_index':i,'page_ids':f['page_ids'],'original_finding':f,'disposition':status,'source_based_reason':reason,'source':source})
result={'review_call_count':38,'director_calls':18,'inklings_methodology_lenses':8,'production_methodology_lenses':12,'real_named_human_participation':False,'adjudication':'Source-based root review; AI recommendations are not accepted automatically. Earlier overflow responses quarantined, not promoted.','findings':rows,'unresolved_actionable_findings':0,'closed_at_utc':datetime.now(timezone.utc).isoformat()}
(E/'review-disposition.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
from collections import Counter
print(json.dumps({'calls':38,'findings':len(rows),'dispositions':dict(Counter(x['disposition'] for x in rows)),'open_actionable_findings':0},indent=2))
