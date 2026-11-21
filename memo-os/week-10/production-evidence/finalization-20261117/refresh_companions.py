"""Persist this session's exact-source medical and acquisition-status rechecks.
No medical prediction, claim placement, or roster mutation.
"""
from pathlib import Path
from datetime import datetime,timezone
from copy import deepcopy
import json
E=Path(__file__).resolve().parent;P=E.parents[3]/'memo-os/week-10/preproduction';O=E.parent/'recovery-20261116'
def read(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
now=datetime.now(timezone.utc).isoformat();f=read(P/'facts.json');snapshot=read(P/'final-league-snapshot.json')
# Sources reopened using web tools, not inferred from the current roster tags.
old=read(O/'injury-source-refresh.json');inj=deepcopy(old);inj['checked_at_utc']=now;inj['fresh_roster_reference']='final-league-snapshot.json';inj['method']='Exact official-team, league and dated wire sources reopened in this execution on2026-11-17, with current ESPN/Flaim ownership and slots checked separately.'
for x in inj['facts']:
 if x['player']=='Drake Maye':x.update({'status':'extended_absence_no_confirmed_season_ending_outcome','source_event_publication_date':'2026-11-16','url':'https://www.patriots.com/news/transcript-head-coach-mike-vrabel-press-conference-11-16','additional_source':'https://www.wbur.org/news/2026/11/17/patriots-drake-maye-ankle-injury-germany','supported_copy_limit':'Coach Mike Vrabel did not confirm a season-ending outcome. The team awaits further evaluation; current reports describe an extended absence. Week11 is New England’s bye. Do not manufacture a diagnosis or return date.'})
 if x['player']=='Woody Marks':x.update({'status':'concussion_monday_did_not_practice_week11_game_status_unresolved','source_event_publication_date':'2026-11-16','url':'https://www.houstontexans.com/news/week-11-injury-report-texans-vs-colts','supported_copy_limit':'Official Monday Week11 report lists concussion and did not practice. Thursday game designation is not yet final; do not call him cleared or ruled out for the game.'})
 if x['player']=='Aidan Hutchinson':x.update({'status':'confirmed_season_ending_acl_indirect_dst_exposure','source_event_publication_date':'2026-11-17','supported_copy_limit':'Tuesday team confirmation of ACL tear; exposure here is Lions D/ST, not an individual-defender roster slot.'})
 if x['player']=='Ladd McConkey':x['status']='confirmed_missed_week10_week11_status_unresolved';x['supported_copy_limit']='Official Sunday downgrade ruled him out of the now-completed Monday Week10 game; it does not determine his Week11 status.'
inj['current_copy_disposition']='W10-P34 refreshed with primary-source distinctions; old injury dates remain distinct from current updates. No season-ending Maye claim.'
dump(E/'injury-source-refresh.json',inj)
news=read(P/'sports-news-pass3.json');news['as_of_utc']=now;news['current_reverification']={'source':'../production-evidence/finalization-20261117/injury-source-refresh.json','checked_at_utc':now,'facts':inj['facts'],'current_roster_entries':222,'current_source':'final-league-snapshot.json','week10_scoring_snapshot_entries':224};news['team_readiness']=snapshot['week11_readiness'];news['roster_snapshot']={'scope':'CURRENT_WEEK11','entries':222,'source':'final-league-snapshot.json'};news['mnf']={'scope':'COMPLETED_WEEK10','remaining_starters':0,'final_contributions':f['mnf']['starters']};news['update_order']=['Use current_reverification for injury facts and final-league-snapshot for ownership','Use final Week10 scoring separately from current Week11 lineups','Keep future practice and game availability explicitly uncertain']
for incident in news.get('incidents',[]):
 player=incident.get('player');src=next((x for x in inj['facts'] if x['player']==player),None)
 if src:incident['current_reverification']=src;incident['fact']=src['supported_copy_limit'];incident['classification']=src['status']
# Current Week11 observations replace stale source-text claims of still having to move byes.
f['pass3']['news']['as_of_utc']=now;f['pass3']['news']['incidents']=deepcopy(news['incidents']);f['pass3']['news']['reverification']=inj['facts'];f['pass3']['news']['artifact']='sports-news-pass3.json'
dump(P/'sports-news-pass3.json',news)
# Fresh bounded Flaim availability queries returned15TE,15K,14DST. Store the
# existing twelve-candidate memo-planning subset exactly, not a complete inventory.
a=read(P/'available-slots-pass3.json');a['captured_at_utc']=now;a['source_file']='../production-evidence/finalization-20261117/availability-readback.json';a['required_slots']=snapshot['week11_required_specialist_needs'];a['coverage']={'TE':15,'K':15,'DST':14,'inventory_complete_claim':False,'ordering':'Provider ESPN-wide roster-rate ordering; not Week11 projections.'}
for position,rows in a['shortlist'].items():
 for row in rows:
  row['acquisitionState']='waivers';row['waiverClearsAt']='2026-11-18T08:00:00.000Z'
  if row['id']=='4362081':row['seasonPoints']=73;row['pointsPerGame']=8.11
# David Njoku is no longer provider-IR. Do not carry the old exclusion forward.
a['excluded_returned_entries']['TE']=[x for x in a['excluded_returned_entries']['TE'] if x['id']!='3123076']
a['excluded_returned_entries']['K']=[x for x in a['excluded_returned_entries']['K'] if x['id']!='4258620']
a['excluded_returned_entries']['K'].append({'id':'4258620','name':'Andre Szmyt','team':'CLE','reasons':['Week11 bye'],'current_acquisition_state':'waivers','waiverClearsAt':'2026-11-19T08:00:00.000Z'})
a['availability_limits']=['This is a bounded live planning subset from15TE,15K and14DST rows, not the entire player inventory.','All twelve retained candidates are now on waivers; no immediate add is promised.','Reported clearance2026-11-18T08:00Z is03:00EST, not a guaranteed successful acquisition.','Candidate IDs are absent from all222 current roster entries.','Provider Active is not medical clearance; uncertain health is checked against dated reporting.','Season points and points-per-game are actual league-scored season values, not Week11 projections.','No player is allocated to multiple teams and no claim, bid or roster action was performed.']
owned={str(x['player_id']) for x in snapshot['current_rosters']};assert all(row['id'] not in owned for rows in a['shortlist'].values() for row in rows)
readback={'checked_at_utc':now,'source':'Fresh connected Flaim get_free_agents, explicit offset0, count15 each TE,K,DST, include_inventory_details=true','kind':'Normalized selected-field readback, not raw connector response','returned_counts':{'TE':15,'K':15,'DST':14},'retained_subset':a['shortlist'],'deltas':['All12 retained candidates now waivers; old free-agent subtype replaced','Cameron Dicker seasonPoints73 and pointsPerGame8.11','David Njoku provider Active, old IR exclusion removed','Andre Szmyt currently available on waivers after Seven Deadly Chins drop; CLE bye excludesWeek11 use'],'no_weekly_projection_or_complete_inventory_claim':True}
dump(E/'availability-readback.json',readback);dump(P/'available-slots-pass3.json',a)
f['pass3']['available_slots']={'fact_id':'W11-AVAILABLE-SLOTS','artifact':'available-slots-pass3.json','scope':'Current bounded available-player planning subset; no pickup recommendation, claim, bid or allocation','data':a,'current_required_slots':snapshot['week11_required_specialist_needs']}
dump(P/'facts.json',f)
# Keep operative companion mirrors current without rewriting immutable prior receipts.
aud=read(P/'league-audit-pass3.json');aud['sports_news_companion']={'artifact':'sports-news-pass3.json','as_of_utc':now,'source_receipt':'../production-evidence/finalization-20261117/injury-source-refresh.json'};aud['required_slot_availability_appendix']={'artifact':'available-slots-pass3.json','captured_at_utc':now,'required_slots':a['required_slots']};dump(P/'league-audit-pass3.json',aud)
print(json.dumps({'injury_source_facts':len(inj['facts']),'current_roster_entries':222,'availability_subset':12,'retained_candidates_all_on_waivers':True,'roster_actions_performed':0},indent=2))
