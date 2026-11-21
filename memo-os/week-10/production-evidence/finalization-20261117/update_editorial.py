"""Apply final-result deltas to the existing approved-direction Week10 page bodies.
Preserve full narratives, canonical references, reading order and physical scenes.
"""
from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import json,re
E=Path(__file__).resolve().parent;P=E.parents[3]/'memo-os/week-10/preproduction'
def read(n):return json.loads((P/n).read_text())
def dump(n,x):(P/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
NOW=datetime.now(timezone.utc).isoformat();f=read('facts.json');s=read('final-league-snapshot.json');i=read('issue-previs.json');bs=read('illustrated-page-briefs.json');cards=read('storycards.json');pages={p['page_id']:p for p in i['pages']}
byid={x['team_id']:x for x in s['standings']};names={tid:x['name'] for tid,x in byid.items()}
def record(tid):
 r=byid[tid];return f"{r['wins']}–{r['losses']}"+(f"–{r['ties']}" if r['ties'] else '')
def copy(pid,**kwargs):pages[pid]['draft_copy'].update(kwargs)
def body(pid,text):copy(pid,body=text)
copy('W10-P01',callouts=[{'label':'HIS MAJESTY’S BLOOD','value':'208.76 · FINAL'},{'label':'THE LLC','value':'203.96 · FINAL'}])
body('W10-P02',pages['W10-P02']['draft_copy']['body'].replace('With four regular-season games remaining after this one','With four regular-season games now remaining'))
body('W10-P03',pages['W10-P03']['draft_copy']['body'].replace("Tonight's remaining starters can still move the board. When those numbers settle, the next week will ask each of us what we have left to field.","The numbers have settled, and six teams now share 6–4 records. The next week will ask each of us what we have left to field."))
copy('W10-P03',deck='Commissioner’s note • After Week 10')
copy('W10-P04',deck='Final Week 10 results • All six outcomes posted',body='Monday night is complete, and all six Week 10 outcomes are official. His Majesty’s Blood and The LLC clear two hundred; six teams finish the week at 6–4. These are the final scores, not projections.',rows=[{'home_team':g['home']['name'],'home_points':f"{g['home']['points']:.2f}",'away_team':g['away']['name'],'away_points':f"{g['away']['points']:.2f}",'status':'FINAL'} for g in s['games']])
body('W10-P10',pages['W10-P10']['draft_copy']['body'].replace('El Niño laughs somewhere inside the moving cloud','El Niño laughs across the rain-swept court').replace('and the old semifinal comes back in full:','and the 2022 semifinal comes back in full:'))
body('W10-P17',"The last tail lamp disappears into reeds. Mud Dogs stands under his own sign beside empty stands and flooded racing scars, watching a postcard for Cancún flutter against the post. It is a taunt, not a ticket: at 2–8, a narrow division-title route still exists. Another loss closes it. For now, Slob on my Dobb has delivered the beer, and Mud Dogs has been left with the silence after a truck.")
copy('W10-P18',body="Christian McCaffrey’s 52.60 powers Slob on my Dobb. His Majesty’s Blood receives 113.86 from Brock Purdy, Chuba Hubbard and Jaxon Smith-Njigba; The LLC gets 103.66 from Joe Burrow, Isaiah Likely and Parker Washington. Jahmyr Gibbs answers with 47.40 for Dr. Duckhook. El Niño wins with George Pickens’ 44.50 unused on the bench. Derrick Henry and Mark Andrews add 36.20 on Monday, but ObiWan Jacoby still finishes 37.43 behind The LLC.")
for row in pages['W10-P18']['draft_copy']['rows']:
 row['category']=row['category'].replace('current overall starter lead','overall starter lead')
body('W10-P24',"ObiWan Jacoby holds the inner arch as the remaining guns converge. Smoke from the destroyed emplacement blows in the same direction as the flags; the one surviving battery still fires. He has made two choices, earned two real moments, and still faces an enemy whose resources outlast them. The LLC’s 203.96 withstands the late response. ObiWan Jacoby reaches 166.53, but the gap remains 37.43. The defense is heroic. The result belongs to the visitor.")
needs={}
for n in s['week11_required_specialist_needs']:needs.setdefault(n['team'],[]).append(n['position'])
copy('W10-P25',deck='Week 11 • Seven uncovered required positions',body='Six NFL clubs are on bye. The refreshed rosters still leave six Schemin teams without owned coverage at seven required specialist positions. Managers have already moved other bye-week players; these are the gaps that remain, not a replay of Monday’s starting lineups. Fantasy reserve placement remains separate from an injury diagnosis.',rows=[{'team':name,'need':' + '.join(v)} for name,v in needs.items()])
for co in pages['W10-P26']['draft_copy']['callouts']:
 co['body']=co['body'].replace('ObiWan completed','ObiWan Jacoby completed')
 if 'tonight' in co.get('heading',''):
  co['heading']='The defense that closed the week';co['body']='Three Dreaded Snake added Ravens D/ST for Bengals D/ST on November 11. Baltimore’s defense supplied 7.00 on Monday; Three Dreaded Snake finished with 82.78.'
copy('W10-P27',headline='TWELVE TEAMS. TEN POSTED RESULTS.',deck='Official standings after Week 10',body='Six teams share 6–4 records, with Slob on my Dobb first in the provider’s seeding and first in total points. Red Leopards and The Chili Cheesers follow at 5–5. Equal records do not mean interchangeable seeds: the order below preserves ESPN’s posted table, including the division and tiebreak structure.',rows=[{'seed':t['official_seed'],'team':t['name'],'record':record(t['team_id']),'points_for':f"{t['points_for']:.2f}"} for t in s['standings']])
pages['W10-P27']['title']='TWELVE TEAMS. TEN POSTED RESULTS.'
copy('W10-P28',body='Six teams now share 6–4 records. Pizza contains three of them; Wings two; Burgers one. The same record creates different pressure in each division. Week 11 is the final crossover before Weeks 12–14 bring division opponents back together.',callouts=[{'label':'BURGERS','heading':'D0nkey K0ng has separation','body':'D0nkey K0ng stands at 6–4. ObiWan Jacoby and Three Dreaded Snake are 4–6; Mud Dogs is 2–8 and must win out to preserve a route.'},{'label':'PIZZA','heading':'Three leaders on the same step','body':'El Niño, His Majesty’s Blood and Seven Deadly Chins are all 6–4. The LLC’s 203.96 victory lifts its record to 4–6, with the divisional return still ahead.'},{'label':'WINGS','heading':'The cushion has narrowed','body':'Dr. Duckhook and Slob on my Dobb are 6–4. Red Leopards and The Chili Cheesers are both 5–5. One crossover remains before the four meet division rivals again.'}])
copy('W10-P29',deck='Final Week 10 scoring index • Not playoff seeding',body='Slob on my Dobb leads the final scoring-form index, followed by His Majesty’s Blood and The LLC. The established formula weights season points per game through ten games at 70% and Week 10 at 30%. It measures points already produced. Week 11 injuries and byes belong beside the outlook, not hidden inside a changed formula.',rows=[{'rank':rank,'team':f['teams'][tid]['name'],'index':f'{display:.2f}'} for rank,(tid,ppg,raw,display) in enumerate(f['scoring_form']['rows'],1)])
copy('W10-P30',body='All twelve teams still have a route, and none has clinched. At 2–8, Mud Dogs can still win Burgers at 6–8 through a specific set of results. A further loss eliminates that possibility and the remaining shared-place route. Four games remain: one crossover, then three divisional rounds.',callouts=[{'heading':'SEVEN BERTHS','body':'Three division winners and four shared places.'},{'heading':'MUD DOGS’ NEXT TEST','body':'A Week 11 loss to Seven Deadly Chins eliminates Mud Dogs. Winning keeps a narrow, help-dependent route alive.'}])
copy('W10-P31',deck='Week 11 • Head-to-head now. Divisions next.',body='His Majesty’s Blood at D0nkey K0ng and El Niño at Slob on my Dobb pair four 6–4 contenders in the top-seed race. Red Leopards at Three Dreaded Snake and The Chili Cheesers at ObiWan Jacoby are bubble swings, with the 4–6 hosts needing to stop losing ground. The LLC visits Dr. Duckhook: recovery pressure for the visitor, top-seed contention for the host. Those are pressure games, not automatic eliminators. A loss to Seven Deadly Chins does eliminate Mud Dogs. Head-to-head can decide ties; three divisional rounds follow.')
implications=['6–4 vs 6–4 • Top-seed race','5–5 vs 4–6 • Bubble leverage','6–4 vs 2–8 • A loss eliminates Mud Dogs','5–5 vs 4–6 • Bubble leverage','6–4 vs 6–4 • Top-seed race','4–6 vs 6–4 • Recovery versus top-seed contention']
for row,implication in zip(pages['W10-P31']['draft_copy']['rows'],implications):row['implication']=implication
pages['W10-P31']['week11_implications_source']='../production-evidence/finalization-20261117/week11-implications-audit.json'

copy('W10-P34',body='Dr. Duckhook’s Drake Maye faces an extended absence, but New England has not confirmed a season-ending outcome. Mud Dogs’ Woody Marks missed Monday’s practice with a concussion ahead of Thursday. The Chili Cheesers awaits Brock Bowers’ day-to-day ankle decision. Three Dreaded Snake monitors A.J. Brown’s hamstring exit. Aidan Hutchinson’s confirmed season-ending ACL loss affects His Majesty’s Blood through Lions D/ST. The LLC’s Michael Wilson is out for the season from his November 8 neck injury. ObiWan Jacoby’s Puka Nacua cannot return before Week 15; Red Leopards’ Lamar Jackson has no fixed return date.')
copy('W10-P35',deck='Week 11 preview • His Majesty’s Blood at D0nkey K0ng',body='Two commanding Sundays lead toward the same crossing, with both teams now 6–4. In their verified 2025 Week 9 meeting, D0nkey K0ng’s franchise won 179.68–111.42. That memory gives this visit an edge. His Majesty’s Blood has already moved its bye-week starters; D0nkey K0ng’s current lineup still shows Bijan Robinson and Denzel Boston on byes. One more test comes before division games return.')
# Exact official result treatments appear only on the six matchup payoff pages.
finales=['W10-P07','W10-P10','W10-P14','W10-P17','W10-P21','W10-P24']
for pid,g in zip(finales,s['games']):
 winner=g['away'];loser=g['home'];result={'status':'FINAL','winner':winner['name'],'winner_points':f"{winner['points']:.2f}",'loser':loser['name'],'loser_points':f"{loser['points']:.2f}",'winner_record':record(winner['team_id']),'loser_record':record(loser['team_id']),'margin':f"{g['margin']:.2f}",'source':'SFINAL'}
 pages[pid]['draft_copy']['result']=result
# All matchup pages select the now-confirmed branch while preserving setup/escalation.
for idx,m in enumerate(cards['matchups']):
 g=s['games'][idx];m.update({'status':'FINAL_RESULTS_SOURCE_BOUND','source_score_state':'ALL_WEEK10_PROVIDER_WINNERS_DECIDED','provider_finality_pending':False,'current_points':{'home':g['home']['points'],'away':g['away']['points']},'current_leader':g['away']['name'],'final_winner':g['away']['name'],'margin':g['margin'],'mnf_remaining':[],'selected_branch':'holding','result_source':'SFINAL'})
 for anchor in m.get('football_anchors',[]):
  pointer=anchor.get('selector')
  if pointer:
   v=f
   for part in pointer.strip('/').split('/'):v=v[int(part)] if isinstance(v,list) else v[part]
   anchor['points']=v
 for p in [x for x in pages.values() if x['source_card_id']==m['id']]:
  p['selected_branch']='holding';p['copy_status']='FINAL_RESULT_NARRATIVE_INPUT';p['result_source']='SFINAL'
  if isinstance(p.get('score_module'),dict):p['score_module']['label']='FINAL';p['score_module']['scope']='W10_FINAL'
  if isinstance(p.get('sports_receipt'),dict):
   receipt=p['sports_receipt'];receipt['status']='W10_FINAL';bits=[]
   for field in receipt.get('fields',[]):
    v=f
    for part in field['points_selector'].strip('/').split('/'):v=v[int(part)] if isinstance(v,list) else v[part]
    field['points']=v;bits.append(f"{field['player']} {v:.2f}")
   receipt['text']='; '.join(bits)+'.';receipt['source']='SFINAL'
   if p['page_id'] in finales:p['draft_copy']['football_context']=receipt['text']
# Update the independent factual field snapshots, not only the visible paragraphs.
for p in pages.values():
 if p['page_id']=='W10-P32':continue
 if p['page_id']=='W10-P27':p['fact_dependencies']=['/official_records']+[f'/teams/T{tid:02d}/post_week10_official_seed' for tid in sorted(byid)]+[f'/teams/T{tid:02d}/post_week10_official_points_for' for tid in sorted(byid)]
 if p['page_id']=='W10-P28':p['fact_dependencies']=['/divisions','/official_records','/pass3/remaining_schedule']
 if p['page_id']=='W10-P31':p['fact_dependencies']=['/week11','/week11_implications','/official_records','/pass3/playoffs']
 if p['page_id']=='W10-P29':p['fact_dependencies']=['/scoring_form','/pass3/readiness']
 if p['page_id']=='W10-P33':p['fact_dependencies']=['/week11','/pass3/readiness','/teams/T03/post_week10_official_points_for']
 bindings=[]
 # Rebuild pointer-bearing dependencies; retain historic context bindings.
 selectors=[x for x in p.get('fact_dependencies',[]) if x.startswith('/')]
 for oldbind in p.get('deterministic_data_fields',[]):
  selector=oldbind.get('selector')
  if selector and selector.startswith('/historical_context/') and selector not in selectors:selectors.append(selector)
 if p['source_card_id'].startswith('W10-M'):
  index=int(p['source_card_id'][-2:])-1
  if f'/games/{index}' not in selectors:selectors.insert(0,f'/games/{index}')
 for selector in selectors:
  v=f
  for part in selector.strip('/').split('/'):v=v[int(part)] if isinstance(v,list) else v[part.replace('~1','/').replace('~0','~')]
  bindings.append({'selector':selector,'artifact':'facts.json','snapshot_value':deepcopy(v),'policy':'Exact source-bound value. Week10 final; future availability/fixtures retain their own timestamp and scope.','source_capture_utc':NOW})
 p['deterministic_data_fields']=bindings;p['fact_lock_receipts']=[{'capture_utc':NOW,'scope':'W10_PROVIDER_FINAL_WITH_CURRENT_WEEK11_COMPANION','final_fact_lock':True,'source':'final-league-snapshot.json','reason':'All six Week10 winners decided and scores/standings independently corroborated with Flaim. Week11 outcomes remain undecided.'}]
 p['holds']=['Actual generated page likeness, full-copy typography and 1080×1920 pixel review','Jake’s final visual and publication acceptance']
 p['forbidden_mutations']=[x for x in p.get('forbidden_mutations',[]) if x not in ('FINAL winner labels',)]
 p['draft_copy_template']=deepcopy(p['draft_copy']);p['copy_budget']['body_actual_words']=len(p['draft_copy']['body'].split())
 p['source_finality']='W10_PROVIDER_FINAL';p['finality']='Week10 results are final. Week11 remains an explicitly future preview. Actual artwork/publication acceptance is not claimed.'
 p['backend_readiness']='READY_FOR_REQUESTED_INDIVIDUAL_FOLIO_GENERATION'
 if p['draft_copy'].get('headline'):p['title']=p['draft_copy']['headline']
 bpage=next(x for x in bs['pages'] if x['page_id']==p['page_id']);bpage['fact_bindings']=deepcopy(bindings);bpage['finality']=p['finality']
# Remove awkward duplicated expansions without abbreviating canonical names.
def cleanup(x):
 if isinstance(x,str):
  x=x.replace('THE The LLC','THE LLC').replace('The The LLC','The LLC')
  for name in ('Red Leopards','Mud Dogs','The Chili Cheesers','Seven Deadly Chins'):x=x.replace(name+"'s",name+'’').replace(name+'’s',name+'’')
  return x
 if isinstance(x,list):return [cleanup(v) for v in x]
 if isinstance(x,dict):return {k:cleanup(v) for k,v in x.items()}
 return x
for p in pages.values():p['draft_copy']=cleanup(p['draft_copy'])
i['final_fact_lock']=True;i['sports_snapshot_utc']=NOW;i['status']='FINAL_RESULTS_FULL_FOLIO_BACKEND_READY';i['source_finality']='W10_PROVIDER_FINAL';i['publication_approved']=False;i['art_generated']=False
cards['status']='FINAL_RESULTS_SOURCE_BOUND';cards['source_snapshot_utc']=NOW
# Keep prior captures as history, and supply current audit entry points.
audit=read('league-audit-pass3.json');audit.update({'prepared_at_utc':NOW,'consumer_status':'FINAL_WEEK10_AUDIT_COMPATIBILITY_PATH','current_source':'final-league-snapshot.json','main_findings':['All six Week10 games are provider-decided; twelve scores and standings verified.','Six teams share6–4 records. Official standings preserve provider seed order.','All12 remain alive and none clinched, proven with replayed final-baseline witnesses.','A further Mud Dogs loss eliminates them; a win-out6–8 division-title witness remains.','Week10 scoring uses224 frozen roster entries; current Week11 planning uses222 entries.','29 completed Week10 transactions; historical lifecycle requests are not additional moves.'],'week10_live':{'scope':'W10_FINAL','games':s['games']},'mnf_remaining_starters':[],'standings_and_status':s['standings'],'remaining_schedule':f['pass3']['remaining_schedule'],'elimination':f['pass3']['playoffs'],'rosters':s['week11_readiness'],'week11_gotw':f['pass3']['week11_gotw']['audit'],'release_gates':{'backend_ready':True,'week10_finality':True,'rendered_pixels_reviewed':False,'publication_approved':False}})
dump('issue-previs.json',i);dump('illustrated-page-briefs.json',bs);dump('storycards.json',cards);dump('league-audit-pass3.json',audit)
print(json.dumps({'pages_updated':len(i['recommended_reading_order']),'official_result_payoffs':6,'standings_through':10,'names_expanded':True,'canonical_scene_changes':'Only cloud-laugh ambiguity removed; physical scenes and image references preserved.'},indent=2))
