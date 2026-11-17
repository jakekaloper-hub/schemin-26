"""Finalize existing Week 10 facts and editorial copy from captured provider evidence.
No artwork, roster changes, Atlas promotion, merge, or publication is performed.
"""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal,ROUND_HALF_UP
from copy import deepcopy
from collections import Counter
import json,hashlib,re
E=Path(__file__).resolve().parent;R=E.parents[3];P=R/'memo-os/week-10/preproduction'
def read(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def key(i):return f'T{int(i):02d}'
def money(x):return float(Decimal(str(x)).quantize(Decimal('.01'),rounding=ROUND_HALF_UP))
NOW=datetime.now(timezone.utc).isoformat()
a=read(E/'espn-period-10.json');b=read(E/'espn-period-11.json');f=read(P/'facts.json')
old=read(P/'current-league-pass3.json');teams={t['id']:t for t in b['teams']}
names={int(k[1:]):v['name'].strip() for k,v in f['teams'].items()}
# Connected Flaim observations transcribed from successful reads in this execution;
# these are normalized observations, not falsely described as raw connector bytes.
flaim_scores={7:93.70,5:156.67,2:147.82,9:189.08,6:82.78,11:146.22,10:113.62,3:179.29,12:127.67,8:208.76,1:166.53,4:203.96}
flaim_order=[3,9,5,8,12,11,2,7,4,1,6,10]
flaim_pf={3:1599.99,9:1450.03,5:1411.82,8:1451.95,12:1452.15,11:1356.62,2:1404.51,7:1384.79,4:1449.25,1:1384.51,6:1279.46,10:1181.35}
flaim_fixtures=[(3,9),(6,2),(10,11),(1,7),(5,8),(12,4)]
slotnames={0:'QB',2:'RB',4:'WR',5:'WR/TE',6:'TE',16:'D/ST',17:'K',20:'Bench',21:'IR',23:'FLEX'}
posnames={1:'QB',2:'RB',3:'WR',4:'TE',5:'K',16:'D/ST'}
club={}
for t in a['teams']:
 previously={int(x['playerId']):x for x in old[f"roster{t['id']}"]['data']['roster']}
 for en in t['roster']['entries']:
  pl=en['playerPoolEntry']['player'];prev=previously.get(pl['id'])
  if prev and prev.get('proTeam'):club[pl['proTeamId']]=prev['proTeam']
assert set(club.values()).issuperset({'ATL','CLE','GB','LAR','NE','SEA'})
games=[];players_by_team={};rosters10=[];rosters11=[]
for d,output in [(a,rosters10),(b,rosters11)]:
 for t in d['teams']:
  for en in t['roster']['entries']:
   pl=en['playerPoolEntry']['player']
   output.append({'team_id':t['id'],'team_name':names[t['id']],'player_id':pl['id'],'name':pl['fullName'],'position':posnames.get(pl['defaultPositionId'],str(pl['defaultPositionId'])),'lineup_slot_id':en['lineupSlotId'],'lineup_slot':slotnames.get(en['lineupSlotId'],str(en['lineupSlotId'])),'eligible_slot_ids':pl['eligibleSlots'],'pro_team_id':pl['proTeamId'],'pro_team':club.get(pl['proTeamId']),'injury_status':pl.get('injuryStatus'),'last_news_date':pl.get('lastNewsDate')})
assert len(rosters10)==224 and len(rosters11)==222
for m in a['schedule']:
 if m['matchupPeriodId']!=10:continue
 assert m['winner'] in ('HOME','AWAY','TIE')
 g={'provider_id':m['id'],'provider_winner':m['winner'],'status':'FINAL'}
 for side in ('home','away'):
  x=m[side];tid=x['teamId'];entries=x['rosterForCurrentScoringPeriod']['entries'];pts=money(x['totalPoints'])
  starter_sum=money(sum(en['playerPoolEntry'].get('appliedStatTotal',0) for en in entries if en['lineupSlotId'] not in (20,21)))
  assert pts==starter_sum==flaim_scores[tid],(tid,pts,starter_sum)
  g[side]={'team_id':tid,'name':names[tid],'points':pts}
  players_by_team[tid]=[{'player_id':en['playerId'],'name':en['playerPoolEntry']['player']['fullName'],'slot':slotnames.get(en['lineupSlotId'],str(en['lineupSlotId'])),'started':en['lineupSlotId'] not in (20,21),'points':money(en['playerPoolEntry'].get('appliedStatTotal',0)),'position':posnames.get(en['playerPoolEntry']['player']['defaultPositionId'])} for en in entries]
 winner=g['home'] if m['winner']=='HOME' else g['away'];loser=g['away'] if m['winner']=='HOME' else g['home']
 g['winner_id']=winner['team_id'];g['loser_id']=loser['team_id'];g['margin']=money(winner['points']-loser['points']);games.append(g)
assert len(games)==6 and all(g['provider_winner']=='AWAY' for g in games)
standings=[]
for tid,t in teams.items():
 rec=t['record']['overall'];assert rec['wins']+rec['losses']+rec['ties']==10
 assert money(rec['pointsFor'])==flaim_pf[tid]
 standings.append({'team_id':tid,'name':names[tid],'division_id':t['divisionId'],'division':f['teams'][key(tid)]['division'],'wins':rec['wins'],'losses':rec['losses'],'ties':rec['ties'],'points_for':money(rec['pointsFor']),'points_against':money(rec['pointsAgainst']),'official_seed':t['playoffSeed']})
standings.sort(key=lambda s:s['official_seed']);assert [s['team_id'] for s in standings]==flaim_order
fixtures=[{'home_id':m['home']['teamId'],'away_id':m['away']['teamId'],'home':names[m['home']['teamId']],'away':names[m['away']['teamId']],'winner':m['winner']} for m in b['schedule'] if m['matchupPeriodId']==11]
assert [(x['home_id'],x['away_id']) for x in fixtures]==flaim_fixtures and all(x['winner']=='UNDECIDED' for x in fixtures)
status_counts=dict(Counter(x['status'] for x in old['transactions']['data']['transactions']))
assert status_counts=={'complete':29,'failed':7,'pending':3,'canceled':2}
bye={'ATL','CLE','GB','LAR','NE','SEA'};readiness=[];needs=[]
for tid in sorted(teams):
 owned=[x for x in rosters11 if x['team_id']==tid];available=[x for x in owned if x['pro_team'] not in bye and x['lineup_slot_id']!=21 and (x['injury_status'] or '').upper() not in ('IR','OUT','DOUBTFUL','SUSPENSION')]
 uncovered=[]
 for sid,label in ((0,'QB'),(2,'RB'),(4,'WR'),(6,'TE'),(16,'D/ST'),(17,'K')):
  required=2 if sid in (2,4) else 1
  eligible=[x for x in available if sid in x['eligible_slot_ids']]
  if len(eligible)<required:uncovered.append({'position':label,'uncovered_count':required-len(eligible),'eligible_owned_names':[x['name'] for x in eligible]})
 # Memo's required-specialist coverage is distinct from uncertain RB/WR health.
 for x in uncovered:
  if x['position'] in ('TE','D/ST','K'):needs.append({'team_id':tid,'team':names[tid],'position':x['position'],'uncovered_count':x['uncovered_count']})
 readiness.append({'id':tid,'name':names[tid],'snapshot':{'type':'current','scoring_period':11,'captured_at_utc':NOW},'players':owned,'week11_bye_current_starters':[x['name'] for x in owned if x['pro_team'] in bye and x['lineup_slot_id'] not in (20,21)],'week11_bye_all_rostered':[x['name'] for x in owned if x['pro_team'] in bye],'flagged_players':[x for x in owned if x['injury_status'] and x['injury_status'].upper() not in ('ACTIVE','NORMAL')],'uncovered_required_position_counts':uncovered,'limits':'Provider tags and owned eligibility do not certify medical clearance or a future starting lineup.'})
oldids={(x['team_id'],x['player_id']):x for x in rosters10};newids={(x['team_id'],x['player_id']):x for x in rosters11}
delta={'removed':[oldids[k] for k in oldids.keys()-newids.keys()],'added':[newids[k] for k in newids.keys()-oldids.keys()]}
prior=[(m['matchupPeriodId'],m[s]['teamId'],money(m[s]['totalPoints'])) for m in a['schedule'] if 1<=m['matchupPeriodId']<10 for s in ('home','away')]
assert len(prior)==108 and not any(x[2]>=200 for x in prior)
snapshot={'schema':'schemin.week10.final.v1','captured_at_utc':NOW,'source':'Connected Flaim refresh and explicit Week10 reads, corroborated by separately captured ESPN periods10 and11','league_id':1417621,'season':2026,'week':10,'all_six_decided':True,'games':games,'standings_through_week':10,'standings':standings,'week11_fixtures':fixtures,'week10_roster_entry_count':len(rosters10),'current_roster_entry_count':len(rosters11),'week10_rosters':rosters10,'current_rosters':rosters11,'week10_players':players_by_team,'roster_delta_since_week10':delta,'week11_readiness':readiness,'week11_required_specialist_needs':needs,'week11_bye_teams':sorted(bye),'transaction_window':{'week':10,'statuses':status_counts,'returned_rows':41,'truncated':False,'completed':29,'pending_rows_have_completed_outcomes':True},'provider_receipts':[read(E/'espn-period-10-receipt.json'),read(E/'espn-period-11-receipt.json')],'flaim_crosscheck':{'scores':12,'standings':12,'week11_pairs':6,'completed_transactions':29,'current_team12_roster':18},'first_200_scope':{'prior_team_week_observations':108,'prior_200_count':0,'first_two_final_200_teams':[8,4],'scope':'2026 season only, not all time'}}
dump(P/'final-league-snapshot.json',snapshot)
dump(E/'flaim-crosscheck.json',{'captured_at_utc':NOW,'kind':'Normalized observation readback, not raw connector bytes','scores':flaim_scores,'provider_winners':['AWAY']*6,'official_seed_order':flaim_order,'points_for':flaim_pf,'week11_pairs':flaim_fixtures,'transaction_counts':status_counts,'corroboration':'All asserted observations match captured ESPN payloads; transaction counts separately match fresh Flaim week10/count100 response.'})
# Update the canonical fact bundle while retaining entering-week historical columns.
f['captured_at_utc']=NOW;f['packet_id']='S26-W10-FINAL-FACTS-20261117'
f['sources']['SFINAL']={'kind':'FLAIM_ESPN_FINAL_CROSSCHECK','file':'final-league-snapshot.json','captured_at_utc':NOW,'receipts':'../production-evidence/finalization-20261117/'}
f['scopes']['W10_FINAL']='Provider-decided Week10 outcomes at this capture, subject only to subsequent official stat correction.'
f['scopes']['W10_LIVE']='Historical pre-final capture only; not an active render authority.'
f['scopes']['FINAL_SCORING_FORM']='Editorial 70/30 formula using official points through ten games and final Week10 scoring; not provider seeding.'
f['scopes']['CURRENT_ROSTER_SLOTS']='Current Week11 fantasy roster/slots, 222 entries; separate from 224-entry Week10 scoring snapshot; not medical clearance.'
f['scope_sources'].update({'W10_FINAL':['SFINAL'],'FINAL_SCORING_FORM':['SFINAL'],'CURRENT_ROSTER_SLOTS':['SFINAL'],'W11_FIXTURES':['SFINAL']})
f['field_scopes'].update({'teams.current_points':'W10_FINAL','teams.scorers':'W10_FINAL','games.final_winner':'W10_FINAL','teams.post_week10_official_record':'W10_FINAL','teams.post_week10_official_seed':'W10_FINAL','teams.post_week10_official_points_for':'W10_FINAL'})
for s in standings:
 tid=s['team_id'];t=f['teams'][key(tid)];t.update({'current_points':flaim_scores[tid],'final_points':flaim_scores[tid],'post_week10_official_record':{'w':s['wins'],'l':s['losses'],'t':s['ties']},'post_week10_official_seed':s['official_seed'],'post_week10_official_points_for':s['points_for'],'post_week10_official_points_against':s['points_against'],'scorers':{str(x['player_id']):[x['name'],x['slot'],x['points']] for x in players_by_team[tid] if x['started']}})
 own=[x for x in rosters11 if x['team_id']==tid];t['reserve_slots']={label:[x['name'] for x in own if x['lineup_slot']==label] for label in ('Bench','IR')};t['reserve_occupancy']={k:len(v) for k,v in t['reserve_slots'].items()};t['reserve_scope']='CURRENT_WEEK11'
 outcomes=[]
 for m in sorted((m for m in a['schedule'] if m['matchupPeriodId']<=10 and tid in (m['home']['teamId'],m['away']['teamId'])),key=lambda m:m['matchupPeriodId']):
  outcomes.append('T' if m['winner']=='TIE' else ('W' if m[m['winner'].lower()]['teamId']==tid else 'L'))
 count=0
 for x in reversed(outcomes):
  if x!=outcomes[-1]:break
  count+=1
 t['post_week10_streak']=outcomes[-1]+str(count);t['last_five_completed_through10']=''.join(outcomes[-5:])
for x,g in zip(f['games'],games):
 assert x['home']==key(g['home']['team_id']) and x['away']==key(g['away']['team_id'])
 x.update({'scope':'W10_FINAL','source':'SFINAL','current_score':[g['home']['points'],g['away']['points']],'final_score':[g['home']['points'],g['away']['points']],'away_lead':g['margin'],'provider_winner':g['provider_winner'],'final_winner':key(g['winner_id']),'remaining_starter_fact_ids':[],'scheduled_starters_complete':True,'overtake':None})
f['mnf']['scope']='COMPLETED_WEEK10_MNF';f['mnf']['remaining_starter_count']=0;f['mnf']['game_completed']=True
for x in f['mnf']['starters']:
 tid=int(x['team'][1:]);x['final_points']=next(y['points'] for y in players_by_team[tid] if str(y['player_id'])==x['player_id']);x['points_at_capture']=x['final_points'];x['capture_scope']='W10_FINAL'
f['history_200'].update({'current_scope':'W10_FINAL','source':'SFINAL','claim_limit':'First two 200-point performances in the 2026 season through completed Week10; not an all-time claim.'})
form=[]
for s in standings:
 tid=s['team_id'];ppg=Decimal(str(s['points_for']))/10;v=Decimal('.7')*ppg+Decimal('.3')*Decimal(str(flaim_scores[tid]));form.append([key(tid),float(ppg),float(v),float(v.quantize(Decimal('.01'),rounding=ROUND_HALF_UP))])
form.sort(key=lambda x:(-x[2],-flaim_scores[int(x[0][1:])],x[0]))
formobj={'fact_id':'W10-SCORING-FORM','scope':'FINAL_SCORING_FORM','source_inputs':['SFINAL'],'formula':'0.70 * (official_points_for_through10 / 10) + 0.30 * final_week10_points','display_rounding':'2 decimals, half up; sort unrounded','row_fields':['team','season_ppg_through10','unrounded_form','display_form'],'rows':form,'not_playoff_seeding':True}
f['scoring_form']=formobj;f['provisional_scoring_form']=dict(formobj,compatibility_alias='Legacy selector retained; its values are FINAL_SCORING_FORM, not provisional.')
f['official_records']={'fact_id':'W10-OFFICIAL-RECORDS','scope':'W10_FINAL','records':{key(s['team_id']):{'w':s['wins'],'l':s['losses'],'t':s['ties']} for s in standings},'six_four_group':[key(s['team_id']) for s in standings if s['wins']==6 and s['losses']==4]}
f['conditional_records']={'fact_id':'W10-CONDITIONAL-RECORDS','scope':'HISTORICAL_FORECAST_SUPERSEDED','baseline_condition':'Previous all-leads-hold forecast is now resolved by official outcomes. Use official_records.','baseline':deepcopy(f['official_records']['records']),'six_four_group':f['official_records']['six_four_group'],'alternatives':{},'active_source':'/official_records'}
f['derived']['scope']='W10_FINAL'
for x in f['derived']['starting_position_leaders'].values():
 candidates=[(tid,p) for tid,ps in players_by_team.items() for p in ps if p['started'] and p['position']==next((k for k,v in f['derived']['starting_position_leaders'].items() if v is x),None)]
 if candidates:
  tid,p=max(candidates,key=lambda z:z[1]['points']);x.update({'team':key(tid),'player_id':str(p['player_id']),'player':p['name'],'points':p['points'],'points_selector':f"/teams/{key(tid)}/scorers/{p['player_id']}/2"})
for x in f['bench_observations'].values():x['scope']='W10_FINAL_NONSCORING_BENCH'
f['derived']['reserve_occupancy']={key(tid):deepcopy(f['teams'][key(tid)]['reserve_occupancy']) for tid in teams}
f['finality']={'all_six_decided':True,'scope':'W10_PROVIDER_FINAL','captured_at_utc':NOW,'source':'SFINAL','stat_correction_policy':'Reopen affected bindings if ESPN later corrects a posted result.','week11_outcomes_decided':False}
f['current_recheck']={'captured_at_utc':NOW,'source_receipt':'final-league-snapshot.json','all_six_winner_fields':'AWAY','week10_scoring_roster_entries':224,'current_roster_entries':222,'standings_scope':'OFFICIAL_THROUGH_WEEK10','publication_fact_finality':True}
f['release_constraints']=['Week10 results and standings are provider-final at this capture; honor later official corrections.','Week11 remains future and undecided; lineup and medical availability are timestamped reports, not guarantees.','Actual generated artwork and founder publication approval are separate from backend data readiness.','Fantasy reserve placement is not a diagnosis.','Completed transactions exclude failed/canceled and duplicate lifecycle records.','Scoring-form index is editorial, not official playoff seeding.']
f['pass3'].update({'captured_at_utc':NOW,'scope':'FINAL_WEEK10_AND_CURRENT_WEEK11_RECHECK','current_source':'final-league-snapshot.json','all_week10_outcomes_undecided':False,'all_week10_outcomes_decided':True})
f['pass3']['readiness']={'fact_id':'W11-READINESS','captured_at_utc':NOW,'teams':readiness,'required_specialist_needs':needs,'source':'final-league-snapshot.json','scope':'CURRENT_WEEK11_NOT_FINAL_LINEUP'}
f['pass3']['remaining_schedule']=[{'week':m['matchupPeriodId'],'home_team_id':m['home']['teamId'],'away_team_id':m['away']['teamId'],'home_name':names[m['home']['teamId']],'away_name':names[m['away']['teamId']],'same_division':teams[m['home']['teamId']]['divisionId']==teams[m['away']['teamId']]['divisionId'],'provider_winner':m['winner']} for m in b['schedule'] if 11<=m['matchupPeriodId']<=14]
f['pass3']['available_slots']['scope']='Historical candidate availability is not current acquisition evidence; use fresh specialist needs. No candidate names appear in final memo copy.'
f['pass3']['available_slots']['current_required_slots']=needs
f['pass3']['week11_gotw']['audit']['decision_status']='Week11 fixture confirmed, both teams official6–4; editorial preview has no selected winner.'
for k in ('recommended_primary','major_coheadliner'):
 g=f['pass3']['week11_gotw']['audit'][k]
 for field in ('basis','creative_angle'):
  g[field]=g.get(field,'').replace('conditional6–4','official6–4').replace('Conditional6–4','Official6–4').replace('live200-point','final200-point').replace('potential fourth-straight-win','fourth-straight-win')
 g['week10_final_combined_points']=g.pop('week10_live_combined_points',g.get('week10_final_combined_points'))
 g['current_starter_week11_bye_exposure']={names[tid]:next(x for x in readiness if x['id']==tid)['week11_bye_current_starters'] for tid in (g['away_team_id'],g['home_team_id'])}
dump(P/'facts.json',f)
print(json.dumps({'final_games':6,'standings_through':10,'scoring_roster':224,'current_roster':222,'specialist_needs':needs,'form':form,'roster_delta':delta},ensure_ascii=False,indent=2))
