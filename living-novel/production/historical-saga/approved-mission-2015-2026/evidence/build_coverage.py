"""Reproducible source index; does not grant literary or canon acceptance."""
from pathlib import Path
import json, hashlib, collections, re
ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).resolve().parent
SRC=ROOT/'living-novel/production/full-rewrite-2026/evidence'
def rel(p): return str(p.relative_to(ROOT))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def normalize(d):
 return dict(period=d.get('period',d.get('matchupPeriodId')),home_id=d.get('home_id',d.get('home_team_id')),home=d.get('home',d.get('home_name')),home_score=d.get('hp',d.get('home_points')),away_id=d.get('away_id',d.get('away_team_id')),away=d.get('away',d.get('away_name')),away_score=d.get('ap',d.get('away_points')),winner=d['winner'],tier=d['tier'])
def key(n):
 # Period and raw label fallback keep repeat opponents in different rounds separate.
 return (n['period'],n['home_id'] if n['home_id'] is not None else n['home'],n['away_id'] if n['away_id'] is not None else n['away'],n['tier'])
def dump(name,data): (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
seasons=[]
FINALS=SRC/'G01_2015_2025_FLAIM_VERIFIED_CHAMPIONSHIP_ROUNDS.json'
finals={x['season']:x for x in json.loads(FINALS.read_text())['finals']}
for year in range(2015,2026):
 p=next(SRC.glob(f'G01_{year}_*MATCHUP*.json')); d=json.loads(p.read_text()); groups={}; rows=[]
 if 'rows' in d:
  rows=[(x['week'],normalize(x),f'/rows/{i}') for i,x in enumerate(d['rows'])]
 else:
  rows=[(w['week'],normalize(x),f'/weeks/{i}/matchups/{j}') for i,w in enumerate(d['weeks']) for j,x in enumerate(w['matchups'])]
 for week,n,ptr in rows:
  k=key(n)
  if k not in groups: groups[k]={'record':n,'observations':[],'conflict':False}
  g=groups[k];g['conflict'] |= n!=g['record'];g['observations'].append({'scoring_week':week,'source_pointer':ptr})
 events=[]
 for i,g in enumerate(groups.values(),1):
  n=g['record'];paired=n['home'] is not None and n['away'] is not None
  weeks=sorted({x['scoring_week'] for x in g['observations']})
  legacy=[]
  if year in (2015,2016):
   for w in weeks:
    candidate=ROOT/f'living-novel/historical-chronicle/seasons/{year}/weeks/W{w:02d}.md'
    if candidate.exists(): legacy.append({'path':rel(candidate),'status':'EXISTING_DRAFT_REQUIRES_EVENT_AND_LITERARY_REVIEW'})
   if n['tier']!='NONE':
    candidate=ROOT/f'living-novel/historical-chronicle/seasons/{year}/POSTSEASON.md'
    if candidate.exists():legacy.append({'path':rel(candidate),'status':'CANDIDATE_REFERENCE_NOT_PROOF_OF_COVERAGE'})
  events.append({'event_id':f'ESPN1417621-{year}-P{n["period"]:02d}-E{i:03d}','season':year,'kind':'PAIRED_CONTEST' if paired else 'UNPAIRED_PROVIDER_ROW','phase':'REGULAR_SEASON' if n['tier']=='NONE' else 'POSTSEASON','source_path':rel(p),'source_sha256':sha(p),'evidence_kind':'REPOSITORY_PROVIDER_TRANSCRIPTION_NOT_RAW_PROVIDER_BYTES','observations':g['observations'],'observed_scoring_weeks':weeks,'aggregate_repeated':len(weeks)>1,'conflicting_observations':g['conflict'],**n,'event_id_authority':'MISSION_GENERATED_JOIN_KEY_NOT_PROVIDER_FIXTURE_ID','result_qualification':'DISPLAY_SCORE_EQUAL_WITH_DECLARED_WINNER_NO_TIEBREAK_EVIDENCE' if paired and n['home_score']==n['away_score'] and n['winner'] in ('HOME','AWAY') else 'PRESERVE_SOURCE_WINNER','owner_time_binding':{'status':'UNKNOWN','source':'living-novel/history/OWNER_LINEAGE.md','rule':'Team slot or label is not owner identity; no historical principal POV attribution licensed.'},'unpaired_status':None if paired else 'NO_OPPONENT_IN_SOURCE_BYE_CANDIDATE_NOT_A_PLAYED_CONTEST','literary_coverage':{'status':'UNACCEPTED','accepted_locations':[],'existing_candidates':legacy}})
 for e in events:
  if year==2021 and e['home_id']==5 and e['period']==15 and e['kind']=='UNPAIRED_PROVIDER_ROW':
   e['unpaired_status']='BYE_REPORTED_BY_HISTORICAL_PRESSURE_LEDGER'
   e['bye_support']={'path':'living-novel/history/HISTORICAL_PRESSURE_LEDGER.md','section':'2021 — decisive final','statement':'Dewars White Label advanced from a bye','evidence_level':'REPOSITORY_HISTORICAL_SYNTHESIS_NOT_RAW_BRACKET'}
 paired=[e for e in events if e['kind']=='PAIRED_CONTEST'];reg=[e for e in paired if e['phase']=='REGULAR_SEASON'];post=[e for e in paired if e['phase']=='POSTSEASON'];unpaired=[e for e in events if e['kind']!='PAIRED_CONTEST']
 summary={'season':year,'source_path':rel(p),'returned_rows':len(rows),'distinct_source_entries':len(events),'duplicate_display_rows':len(rows)-len(events),'observed_paired_contests':len(paired),'regular_season_contests':len(reg),'postseason_contests':len(post),'unpaired_rows':len(unpaired),'postseason_tiers_paired':dict(collections.Counter(e['tier'] for e in post)),'regular_scoring_weeks':sorted({w for e in reg for w in e['observed_scoring_weeks']}),'postseason_scoring_weeks':sorted({w for e in post for w in e['observed_scoring_weeks']}),'denominator_scope':'OBSERVED_PAIRED_SOURCE_CONTESTS; full historical schedule completeness not independently certified','accepted_literary_coverage':0,'coverage_status':'UNACCEPTED_NOT_UNWRITTEN','missing_data':['Historical owner binding','Historical division and venue binding','Raw provider bytes not supplied by these transcriptions','Independent schedule/bracket completeness reconciliation'],'title_outcome':{'source_path':rel(FINALS),'source_sha256':sha(FINALS),'record':finals[year],'meaning':'Historical team label and slot only; not verified present-owner title'},'events':events}
 seasons.append({k:v for k,v in summary.items() if k!='events'});dump(f'{year}_FIXTURE_COVERAGE.json',summary)
# Current season: only cited repository observations, not a live refresh.
current=[]
def add(week,a,ap,b,bp,source,winner=None,home_known=False,final=True):
 p=ROOT/source; current.append({'event_id':f'ESPN1417621-2026-P{week:02d}-E{sum(x["period"]==week for x in current)+1:03d}','event_id_authority':'MISSION_GENERATED_JOIN_KEY_NOT_PROVIDER_FIXTURE_ID','season':2026,'period':week,'phase':'REGULAR_SEASON','kind':'PAIRED_CONTEST','side_a':a,'side_a_score':float(ap),'side_b':b,'side_b_score':float(bp),'home_side':'A' if home_known else 'UNRESOLVED_FROM_THIS_SOURCE','winner':winner,'finality':'REPOSITORY_DECIDED_RECEIPT' if final else 'PROVISIONAL_UNDECIDED','source_path':source,'source_sha256':sha(p),'evidence_kind':'REPOSITORY_TRANSCRIPTION_NOT_LIVE_REFRESH','owner_time_binding':{'status':'CURRENT_CANON_REQUIRES_SCENE_PACKET','source':'canon/characters/CHARACTER_REGISTRY.yaml'},'literary_coverage':{'status':'RECONCILE_EXISTING_MANUSCRIPT','accepted_locations':[]}})
p='living-novel/weekly-ledger/2026_WEEK_01_EVIDENCE_AND_SIGNIFICANCE.md'
for line in (ROOT/p).read_text().splitlines():
 m=re.match(r'\| (.+) def\. (.+) \| ([\d.]+)–([\d.]+) \|',line)
 if m: a,b,ap,bp=m.groups();add(1,a,ap,b,bp,p,winner=a)
p='living-novel/weekly-ledger/2026_WEEK_02_EVIDENCE_AND_SIGNIFICANCE.md'
for line in (ROOT/p).read_text().split('## State after')[0].splitlines():
 m=re.match(r'- (.+) ([\d.]+) def\. (.+) ([\d.]+) —',line)
 if m:a,ap,b,bp=m.groups();add(2,a,ap,b,bp,p,winner=a)
p='memo-os/week-3/WEEK_3_FINAL_EVIDENCE_SNAPSHOT_06.md'
for line in (ROOT/p).read_text().splitlines():
 m=re.match(r'- (.+) ([\d.]+) - (.+) ([\d.]+); winner (.+)\.',line)
 if m:a,ap,b,bp,w=m.groups();add(3,a,ap,b,bp,p,winner=w)
p='living-novel/production/week-04-05/WEEK_04_05_FLAIM_FACT_SNAPSHOT_2026-10-14.json'
for x in json.loads((ROOT/p).read_text())['w4']:
 add(4,x['home'],x['home_points'],x['away'],x['away_points'],p,winner=x['winner'],home_known=True)
 current[-1]['provider_winner_flag']=x['provider_winner_flag']
 current[-1]['superseded_observation']={'path':'memo-os/week-4/publication-readiness/WEEK_04_DETERMINISTIC_DATA.json','status':'PROVISIONAL_UNDECIDED_SUPERSEDED_BY_OCT14_DECIDED_RECEIPT'}
 current[-1]['corroboration']='living-novel/production/chapter-04/PROVIDER_FINALITY_RECHECK_2026-10-14.md'
p='memo-os/week-5/production-evidence/WEEK_5_SIX_PAYOFF_FINAL_RESULT_BANNER_LOCK_2026-10-13.json'
for x in json.loads((ROOT/p).read_text())['pages']:add(5,x['home']['name'],x['home']['score'],x['away']['name'],x['away']['score'],p,winner=x['winner'],home_known=True)
p='memo-os/week-6/WEEK_6_FLAIM_REVERIFICATION_AND_HANDOFF_CONVERGENCE_2026-10-20.md'
for line in (ROOT/p).read_text().splitlines():
 m=re.match(r'\| (.+) \| ([\d.]+) \| (.+) \| ([\d.]+) \| (HOME|AWAY) \|',line)
 if m:a,ap,b,bp,w=m.groups();add(6,a,ap,b,bp,p,winner=a if w=='HOME' else b,home_known=True)
s={'season':2026,'observed_paired_contests':len(current),'decided_repository_receipts':sum(e['finality']=='REPOSITORY_DECIDED_RECEIPT' for e in current),'unresolved_finality':sum(e['finality']!='REPOSITORY_DECIDED_RECEIPT' for e in current),'latest_final_repository_cutoff':'2026 Week 6; receipt 2026-10-20','cutoff_limit':'Not live-provider refreshed; Week 4 finality reconciled to Oct14 receipt; W7 source fixtures explicitly UNDECIDED; no season ending or future results licensed','denominator_scope':'OBSERVED_W1_W6_PAIRED_ROWS; not full-season denominator','events':current}
seasons.append({k:v for k,v in s.items() if k!='events'});dump('2026_FIXTURE_COVERAGE.json',s)
dump('SEASON_DENOMINATORS.json',{'baseline_commit':'8fcb77191955f413fe970154d47632770f923055','policy':'Observed evidence denominators are not certified complete schedules. No acceptance inferred from manuscript existence. Unpaired rows retained separately.','seasons':seasons})
# Inventory actual prose and preserve hashes; headings/receipts are not manuscript completion.
inventory=[]
for pattern in ['living-novel/historical-chronicle/seasons/**/*.md','living-novel/production/historical-saga/R53/*.md','living-novel/manuscript/**/*.md','living-novel/production/full-rewrite-2026/manuscript/*.md']:
 for p in ROOT.glob(pattern):
  text=p.read_text();inventory.append({'path':rel(p),'sha256':sha(p),'words_including_headers':len(text.split()),'status':'EXISTING_REQUIRES_AUTHORITY_AND_LITERARY_RECONCILIATION','first_status_lines':[x for x in text.splitlines()[:18] if 'Status' in x or 'NONCANON' in x or 'status' in x]})
dump('EXISTING_TEXT_INVENTORY.json',inventory)
print(json.dumps([{k:v for k,v in s.items() if k in ('season','observed_paired_contests','regular_season_contests','postseason_contests','unpaired_rows','duplicate_display_rows')} for s in seasons],indent=2))
