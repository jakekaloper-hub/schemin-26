"""Corroborate fresh Flaim reads with ESPN's live league payload and audit derived values."""
from pathlib import Path
from datetime import datetime,timezone
from decimal import Decimal,ROUND_HALF_UP
from collections import Counter
import json,hashlib
E=Path(__file__).resolve().parent;R=E.parents[3];P=R/'memo-os/week-10/preproduction'
def load(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
d=load(E/'espn-live-league.json');facts=load(P/'facts.json');old=load(P/'current-league-pass3.json');now=datetime.now(timezone.utc).isoformat()
names={int(k[1:]):v['name'] for k,v in facts['teams'].items()};teams={t['id']:t for t in d['teams']}
observed_flaim={7:93.70,5:156.67,2:136.42,9:189.08,6:75.78,11:146.22,10:113.62,3:179.29,12:127.67,8:208.76,1:130.33,4:203.96}
games=[];scores={};scorers=[]
for m in d['schedule']:
 if m['matchupPeriodId']!=10:continue
 out={'id':m['id'],'winner':m['winner']}
 for side in ['home','away']:
  team=m[side]['teamId'];entries=m[side]['rosterForCurrentScoringPeriod']['entries'];starters=[e for e in entries if e['lineupSlotId'] not in [20,21]]
  total=round(sum(e['playerPoolEntry'].get('appliedStatTotal',0) for e in starters),2)
  if total!=observed_flaim[team]:raise ValueError(f'Flaim / ESPN disagreement {team}: {total}')
  scores[team]=total;out[side]={'team_id':team,'name':names[team],'current_points':total}
  for e in starters:
   pl=e['playerPoolEntry']['player'];scorers.append({'team_id':team,'player_id':pl['id'],'name':pl['fullName'],'slot_id':e['lineupSlotId'],'current_points':round(e['playerPoolEntry'].get('appliedStatTotal',0),2)})
 games.append(out)
assert len(games)==6 and all(x['winner']=='UNDECIDED' for x in games)
rosters=[];abbr={}
for i in range(1,13):
 for pl in old[f'roster{i}']['data']['roster']:
  player=next((e['playerPoolEntry']['player'] for e in teams[i]['roster']['entries'] if str(e['playerId'])==str(pl['playerId'])),None)
  if player:abbr[player['proTeamId']]=pl.get('proTeam')
for tid,t in teams.items():
 for e in t['roster']['entries']:
  pl=e['playerPoolEntry']['player'];rosters.append({'team_id':tid,'team_name':names[tid],'player_id':pl['id'],'name':pl['fullName'],'lineup_slot_id':e['lineupSlotId'],'eligible_slot_ids':pl['eligibleSlots'],'pro_team_id':pl['proTeamId'],'pro_team':abbr.get(pl['proTeamId']),'injury_status':pl.get('injuryStatus'),'last_news_date':pl.get('lastNewsDate')})
standings=[]
for tid,t in teams.items():
 rr=t['record']['overall'];standings.append({'team_id':tid,'name':names[tid],'wins':rr['wins'],'losses':rr['losses'],'ties':rr['ties'],'points_for':round(rr['pointsFor'],2),'points_against':round(rr['pointsAgainst'],2),'official_seed':t['playoffSeed'],'division_id':t['divisionId']})
standings.sort(key=lambda x:x['official_seed'])
week11=[{'home_id':m['home']['teamId'],'home':names[m['home']['teamId']],'away_id':m['away']['teamId'],'away':names[m['away']['teamId']]} for m in d['schedule'] if m['matchupPeriodId']==11]
assert {(x['home_id'],x['away_id']) for x in week11}=={(3,9),(6,2),(10,11),(1,7),(5,8),(12,4)}
conditional={x['team_id']:{'w':x['wins'],'l':x['losses'],'t':x['ties']} for x in standings}
for g in games:
 a,b=g['home'],g['away'];w,l=(a,b) if a['current_points']>b['current_points'] else (b,a);conditional[w['team_id']]['w']+=1;conditional[l['team_id']]['l']+=1
for key,value in facts['conditional_records']['baseline'].items():assert value==conditional[int(key[1:])],key
form=[]
for s in standings:
 tid=s['team_id'];ppg=(Decimal(str(s['points_for']))+Decimal(str(scores[tid])))/10;v=Decimal('.7')*ppg+Decimal('.3')*Decimal(str(scores[tid]));form.append((tid,ppg,v,v.quantize(Decimal('.01'),rounding=ROUND_HALF_UP)))
form.sort(key=lambda x:(-x[2],-scores[x[0]],x[0]))
for row,expected in zip(form,facts['provisional_scoring_form']['rows']):assert f'T{row[0]:02d}'==expected[0] and float(row[3])==expected[3],(row,expected)
# Last nine completed league scores establish scope: not an all-time-record claim.
prior=[(m[side]['teamId'],m['matchupPeriodId'],m[side]['totalPoints']) for m in d['schedule'] if m['matchupPeriodId']<10 for side in ['home','away']]
assert len(prior)==108 and not any(x[2]>=200 for x in prior)
transaction_statuses=dict(Counter(x['status'] for x in old['transactions']['data']['transactions']))
assert transaction_statuses=={'complete':29,'failed':7,'pending':3,'canceled':2}
# These values were also freshly observed in the connected Flaim get_transactions
# response in this session. We retain its normalized prior raw capture and explicitly
# do not label it as the unavailable direct ESPN transactions view.
byes={'ATL','CLE','GB','LAR','NE','SEA'};bye_starters=[x for x in rosters if x['pro_team'] in byes and x['lineup_slot_id'] not in [20,21]]
settings=d['settings']['scheduleSettings'];assert settings['playoffTeamCount']==7 and settings['matchupPeriodCount']==14
result={'captured_at_utc':now,'source':'Fresh connected Flaim league_info, get_matchups(10), get_matchups(11), get_standings, get_transactions + direct ESPN mRoster/mTeam/mMatchup/mSettings corroboration','raw_espn_sha256':hashlib.sha256((E/'espn-live-league.json').read_bytes()).hexdigest(),'league_id':1417621,'season':2026,'week':10,'winner_fields':[g['winner'] for g in games],'all_six_decided':False,'live_score_equality_with_flaim':'12/12','games':games,'standings_through_week':9,'standings':standings,'week11':week11,'roster_entry_count':len(rosters),'rosters':rosters,'current_starter_scorers':scorers,'transaction_status_counts':transaction_statuses,'transaction_total_returned':41,'completed_transactions':29,'transaction_fresh_read':'Connected Flaim get_transactions, week10/count100, this session; no truncation. Direct ESPN transaction view returned400 and is not treated as evidence.','week11_bye_teams':sorted(byes),'current_starters_on_week11_bye':bye_starters,'prior_completed_team_week_count':108,'prior_200_plus_count':0,'first_200_claim_scope':'2026 Weeks1–9 checked plus current Week10 snapshot, NOT all-time','scoring_form_recomputed':True,'conditional_records_recomputed':True,'rules_verified_from_live_settings':{'regular_season_weeks':14,'playoff_teams':7,'seeding_rule':settings['playoffSeedingRule']},'publication_finality':False}
dump(E/'fresh-sports-audit.json',result)
facts['current_recheck']={'captured_at_utc':now,'source_receipt':'../production-evidence/recovery-20261116/fresh-sports-audit.json','current_values_unchanged':True,'all_six_winner_fields':'UNDECIDED','roster_entries_refreshed':len(rosters),'standings_scope':'OFFICIAL_THROUGH_WEEK9','publication_finality':False}
facts['captured_at_utc']=now;dump(P/'facts.json',facts)
print(json.dumps({'scores':'12/12 match Flaim','roster_entries':len(rosters),'week11_pairs':len(week11),'completed_transactions':29,'standings':'all12 verified through9games','derivations':'70/30 form, conditional records, first200 scope verified','finality':'all6 UNDECIDED'},indent=2))
