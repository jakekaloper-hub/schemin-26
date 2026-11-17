"""Recompute retained possibility witnesses from the official Week10 baseline.
These are constructive existence proofs, not forecast probabilities or official seeds.
"""
from pathlib import Path
from copy import deepcopy
from itertools import combinations
from datetime import datetime,timezone
import json
E=Path(__file__).resolve().parent;P=E.parents[3]/'memo-os/week-10/preproduction'
def read(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
snapshot=read(P/'final-league-snapshot.json');raw=read(E/'espn-period-11.json');old=read(P/'playoff-witnesses-pass3.json')
base={x['team_id']:x for x in snapshot['standings']};division={i:s['division'] for i,s in base.items()}
played=[]
for g in raw['schedule']:
 if 1<=g['matchupPeriodId']<=10:
  h,a=g['home']['teamId'],g['away']['teamId'];assert g['winner'] in ('HOME','AWAY','TIE')
  played.append({'week':g['matchupPeriodId'],'home_team_id':h,'away_team_id':a,'winner_team_id':None if g['winner']=='TIE' else g[g['winner'].lower()]['teamId']})
remaining={(x['matchupPeriodId'],x['home']['teamId'],x['away']['teamId']) for x in raw['schedule'] if 11<=x['matchupPeriodId']<=14}
assert len(remaining)==24

def recalc(witness):
 future=witness['winners'];assert {(x['week'],x['home_team_id'],x['away_team_id']) for x in future}==remaining
 records={i:{'team':s['name'],'wins':s['wins'],'losses':s['losses'],'ties':s['ties'],'pf':s['points_for'],'pa':s['points_against'],'division_wins':0,'division_ties':0} for i,s in base.items()}
 allgames=played+future
 for g in allgames:
  h,a,w=g['home_team_id'],g['away_team_id'],g['winner_team_id'];assert w in (h,a,None)
  if division[h]==division[a]:
   if w is None:records[h]['division_ties']+=1;records[a]['division_ties']+=1
   else:records[w]['division_wins']+=1
  if g['week']>=11:
   assert w is not None
   l=a if w==h else h;records[w]['wins']+=1;records[l]['losses']+=1
   records[w]['pf']+=150;records[w]['pa']+=100;records[l]['pf']+=100;records[l]['pa']+=150
 for x in records.values():x['pf']=round(x['pf'],2);x['pa']=round(x['pa'],2)
 def choose(pool):
  best=max(records[i]['wins']+.5*records[i]['ties'] for i in pool);group=[i for i in pool if records[i]['wins']+.5*records[i]['ties']==best]
  if len(group)==1:return group[0]
  counts=[sum({g['home_team_id'],g['away_team_id']}=={i,j} for g in allgames) for i,j in combinations(group,2)]
  if counts and min(counts)>0 and len(set(counts))==1:
   pct={i:sum((1 if g['winner_team_id']==i else .5 if g['winner_team_id'] is None else 0) for g in allgames if i in (g['home_team_id'],g['away_team_id']) and g['home_team_id'] in group and g['away_team_id'] in group) for i in group}
   high=max(pct.values());group=[i for i in group if pct[i]==high]
  high=max(records[i]['pf'] for i in group);group=[i for i in group if records[i]['pf']==high]
  if len(group)>1 and len({division[i] for i in group})==1:
   high=max(records[i]['division_wins']+.5*records[i]['division_ties'] for i in group);group=[i for i in group if records[i]['division_wins']+.5*records[i]['division_ties']==high]
  if len(group)>1:
   high=max(records[i]['pa'] for i in group);group=[i for i in group if records[i]['pa']==high]
  assert len(group)==1,('Unresolved coin flip cannot certify witness',group)
  return group[0]
 def rank(pool):
  ordered=[];left=list(pool)
  while left:
   win=choose(left);ordered.append(win);left.remove(win)
  return ordered
 winners={d:choose([i for i in base if division[i]==d]) for d in sorted(set(division.values()))}
 seeds=rank(list(winners.values()))+rank([i for i in base if i not in winners.values()])[:4]
 return {'winners':future,'final_records':records,'division_winners':winners,'qualified_team_ids':seeds,'illustrative_score_rule':'Each future winner scores150 and loser100 only to construct a possible outcome; never a forecast, recommendation, or probability.'}
result={'scope':'OFFICIAL_W10_BASELINE; FUTURE_W11_W14_HYPOTHETICAL_WITNESSES','captured_at_utc':datetime.now(timezone.utc).isoformat(),'method':'Replayed all25 retained schedule-consistent witnesses from final Week10 records and PF/PA, resolving division winners and four shared places with equal-schedule H2H, PF, same-division record, PA. No coinflip needed. Existing official current seeds are separately provider-sourced.','sources':['final-league-snapshot.json','https://support.espn.com/hc/en-us/articles/47190901074708-H2H-Points-League-Playoff-Seeding-Tiebreakers'],'team_status':{}}
bank=[recalc(v[k]) for v in old['team_status'].values() for k in ('qualification_witness','nonqualification_witness')]+[recalc(old['mud_division_witness'])]
result['prior_witness_repairs']=[]
for tid in sorted(base):
 q=recalc(old['team_status'][str(tid)]['qualification_witness']);n=recalc(old['team_status'][str(tid)]['nonqualification_witness'])
 if tid not in q['qualified_team_ids']:
  result['prior_witness_repairs'].append({'team_id':tid,'type':'qualification','reason':'Old selected witness no longer qualifies under final baseline and explicit tie replay.'})
  q=next(x for x in bank if tid in x['qualified_team_ids'])
 if tid in n['qualified_team_ids']:
  result['prior_witness_repairs'].append({'team_id':tid,'type':'nonqualification','reason':'Old selected witness now qualifies under final baseline and explicit tie replay; replaced by another fully replayed retained witness.'})
  n=next(x for x in bank if tid not in x['qualified_team_ids'])
 assert tid in q['qualified_team_ids'];assert tid not in n['qualified_team_ids']
 result['team_status'][str(tid)]={'name':base[tid]['name'],'clinched':False,'eliminated':False,'status':'Alive, not clinched; constructive qualification and nonqualification witnesses verified from official Week10 results.','qualification_witness':q,'nonqualification_witness':n}
result['mud_division_witness']=recalc(old['mud_division_witness']);assert result['mud_division_witness']['division_winners']['Burgers']==10
result['mud_next_loss_proof']={'max_wins_after_another_loss':5,'six_teams_already_with_six_wins':[x['team_id'] for x in base.values() if x['wins']>=6],'seventh_team_lower_bound':'Red Leopards and The Chili Cheesers each have five wins and play each other in Week13: at least one must finish with six wins, or both have at least five wins plus a tie. Either outranks a five-win/nine-loss Mud Dogs record.','division_title_impossible_at_five':'D0nkey K0ng already has six wins in Burgers.','conclusion':'A further loss eliminates Mud Dogs under the seven-berth rules. A6–8 division-title witness exists if Mud Dogs wins all four remaining games.'}
assert len(result['mud_next_loss_proof']['six_teams_already_with_six_wins'])==6
result['witnesses_passed']=25;result['probabilities_claimed']=False
dump(P/'playoff-witnesses-final.json',result)
f=read(P/'facts.json');f['pass3']['playoffs']={'fact_id':'W10-PLAYOFF-MATH','scope':'OFFICIAL_W10_BASELINE_DERIVED_MATH','rules':f['rules'],'team_status':[{'team_id':int(k),'name':v['name'],'clinched':v['clinched'],'eliminated':v['eliminated']} for k,v in result['team_status'].items()],'all12_alive':True,'none_clinched':True,'witness_file':'playoff-witnesses-final.json','witnesses_passed':25,'mud_next_loss_eliminates':True,'provider_outcomes_not_inferred_from_null':True};dump(P/'facts.json',f)
print(json.dumps({'witnesses_passed':25,'all12_alive':True,'none_clinched':True,'mud_winout_route':result['mud_division_witness']['division_winners'],'next_loss_eliminates_mud':True},indent=2))
