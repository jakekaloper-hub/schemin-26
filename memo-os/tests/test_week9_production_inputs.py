"""Offline input tests. All constructed scores below are SYNTHETIC, not league facts."""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[2]
WEEK=ROOT/'memo-os/week-9'
MODULE=WEEK/'prepare_production_inputs.py'

class ProductionInputTests(unittest.TestCase):
 def setUp(self):
  self.assertTrue(MODULE.is_file(), 'Executable handoff not implemented')
  spec=importlib.util.spec_from_file_location('week9_production_inputs', MODULE)
  self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
  self.issue=json.loads((WEEK/'WEEK_9_COMPLETE_ISSUE_PREVIS_2026-11-08.json').read_text())
  self.cards=json.loads((WEEK/'WEEK_9_SPORTS_STORY_CARDS_2026-11-08.json').read_text())
 def fixture(self):
  matches=[];rows=[]
  slots=['QB','RB','RB','WR','WR','TE','FLEX','D/ST','K','WR/TE']
  for card in self.cards['cards']:
   match={'matchupPeriodId':9,'winner':'HOME'}
   for side,points in [('home',100),('away',90)]:
    team=card[side];match[side]={'teamId':team['teamId'],'teamName':team['name'],'currentPoints':points,'totalPoints':points}
    for i,slot in enumerate(slots):rows.append({'fantasy_team_id':team['teamId'],'player_id':str(team['teamId']*100+i),'name':'SYNTHETIC PLAYER '+str(i),'lineup_slot':slot,'points':points/10,'started':True})
   matches.append(match)
  return {'request':{'league_id':'1417621','season_year':2026,'week':9},'recorded_at_utc':'2026-11-09T19:35:00+00:00','representation':'SYNTHETIC_TEST_FIXTURE_ONLY','matchups_response':{'success':True,'data':{'leagueId':'1417621','seasonYear':2026,'currentScoringPeriod':9,'matchupPeriod':9,'matchups':matches}},'lineup_evidence':{'league_id':'1417621','season_year':2026,'week':9,'recorded_at_utc':'2026-11-09T19:35:00+00:00','source_ref':'SYNTHETIC_TEST_LINEUP','rows':rows}}
 def run_candidate(self,s):return self.m.reconcile(self.issue,self.cards,s)
 def test_undecided_never_proposes_winners(self):
  s=self.fixture();s['matchups_response']['data']['matchups'][0]['winner']='UNDECIDED'
  r=self.run_candidate(s);self.assertEqual(r['status'],'WAITING_PROVIDER_FINALITY');self.assertEqual(r['page_updates'],[])
 def test_zero_placeholder_is_not_final_score(self):
  s=self.fixture();s['matchups_response']['data']['matchups'][0]['home']['totalPoints']=0
  self.assertEqual(self.run_candidate(s)['status'],'INVALID_SOURCE')
 def test_explicit_week9_survives_current_week_rollover(self):
  s=self.fixture();s['matchups_response']['data']['currentScoringPeriod']=10
  self.assertEqual(self.run_candidate(s)['status'],'RECONCILED_CANDIDATE_NOT_ACCEPTED')
 def test_wrong_week_season_or_league_rejected(self):
  for key,value in [('week',10),('season_year',2025),('league_id','1')]:
   s=self.fixture();s['request'][key]=value
   self.assertEqual(self.run_candidate(s)['status'],'INVALID_SOURCE',key)
 def test_swapped_host_and_partial_or_duplicate_fixture_rejected(self):
  for mode in ['swap','partial','duplicate']:
   s=self.fixture();ms=s['matchups_response']['data']['matchups']
   if mode=='swap':ms[0]['home'],ms[0]['away']=ms[0]['away'],ms[0]['home']
   elif mode=='partial':ms.pop()
   else:ms[-1]=copy.deepcopy(ms[0])
   self.assertEqual(self.run_candidate(s)['status'],'INVALID_SOURCE',mode)
 def test_nonfinite_and_bool_scores_rejected(self):
  for value in [float('nan'),float('inf'),True,None]:
   s=self.fixture();s['matchups_response']['data']['matchups'][0]['home']['totalPoints']=value
   self.assertEqual(self.run_candidate(s)['status'],'INVALID_SOURCE')
 def test_provider_winner_conflict_rejected(self):
  s=self.fixture();s['matchups_response']['data']['matchups'][0]['winner']='AWAY'
  self.assertEqual(self.run_candidate(s)['status'],'INVALID_SOURCE')
 def test_tie_needs_actual_tiebreak_review(self):
  s=self.fixture();m=s['matchups_response']['data']['matchups'][0];m['away']['totalPoints']=100;m['away']['currentPoints']=100
  self.assertEqual(self.run_candidate(s)['status'],'TIEBREAK_REVIEW_REQUIRED')
 def test_missing_lineups_or_sums_never_pass(self):
  s=self.fixture();s.pop('lineup_evidence');self.assertEqual(self.run_candidate(s)['status'],'WAITING_LINEUP_EVIDENCE')
  s=self.fixture();s['lineup_evidence']['rows'][0]['points']=11
  self.assertEqual(self.run_candidate(s)['status'],'LINEUP_RECONCILIATION_REQUIRED')
 def test_bench_or_duplicate_player_not_counted_as_starter(self):
  for mode in ['bench','duplicate']:
   s=self.fixture();rs=s['lineup_evidence']['rows']
   if mode=='bench':rs[0]['lineup_slot']='BENCH'
   else:rs[1]['player_id']=rs[0]['player_id']
   self.assertEqual(self.run_candidate(s)['status'],'LINEUP_RECONCILIATION_REQUIRED')
 def test_stale_lineups_and_stale_snapshot_rejected(self):
  s=self.fixture();s['recorded_at_utc']='2026-11-08T12:00:00Z';self.assertEqual(self.run_candidate(s)['status'],'INVALID_SOURCE')
  s=self.fixture();s['lineup_evidence']['recorded_at_utc']='2026-11-08T12:00:00Z';self.assertEqual(self.run_candidate(s)['status'],'LINEUP_RECONCILIATION_REQUIRED')
 def test_exact_endings_are_proposals_and_originals_do_not_mutate(self):
  before=json.dumps(self.issue,sort_keys=True);s=self.fixture();r=self.run_candidate(s)
  self.assertEqual(r['status'],'RECONCILED_CANDIDATE_NOT_ACCEPTED');self.assertEqual(len(r['results']),6)
  endings=[p for p in r['page_updates'] if p.get('body_proposal')];self.assertEqual(len(endings),6)
  for p in endings:
   old=next(x for x in self.issue['pages'] if x['page_id']==p['page_id']);self.assertEqual(p['body_proposal'],old['editorial_copy']['conditional_narratives']['home_win'])
  self.assertFalse(r['source_accepted']);self.assertFalse(r['render_authorized']);self.assertFalse(r['release_approved']);self.assertEqual(before,json.dumps(self.issue,sort_keys=True))
 def test_away_endings_and_idempotent_output(self):
  s=self.fixture()
  for m in s['matchups_response']['data']['matchups']:
   m['winner']='AWAY'
   for side,pts in [('home',90),('away',100)]:
    m[side].update(totalPoints=pts,currentPoints=pts)
    for r in s['lineup_evidence']['rows']:
     if r['fantasy_team_id']==m[side]['teamId']:r['points']=pts/10
  a=self.run_candidate(s);b=self.run_candidate(s);self.assertEqual(a,b)
  self.assertTrue(all(p['branch_proposal']=='away_win' for p in a['page_updates']))
 def test_missing_ending_discards_all_partial_proposals(self):
  final=next(p for p in self.issue['pages'] if p['page_id']=='W09-P21');final['editorial_copy']['conditional_narratives'].pop('home_win')
  r=self.run_candidate(self.fixture());self.assertEqual(r['status'],'INVALID_SOURCE');self.assertEqual(r['page_updates'],[]);self.assertEqual(r['results'],[])
 def test_one_page_kit_contains_only_its_subjects_and_no_scores(self):
  with tempfile.TemporaryDirectory() as td:
   d=self.m.export_page_kit(ROOT,self.issue,'W09-P05',Path(td)/'kit')
   self.assertEqual(d['exact_cast'],['CHAR-ZACH-WILSON','CHAR-JAKE-KALOPER']);self.assertEqual(len(d['reference_files']),2)
   for asset in d['reference_files']:
    data=(Path(td)/'kit'/asset['file']).read_bytes();self.assertEqual(hashlib.sha256(data).hexdigest(),asset['sha256'])
   text=(Path(td)/'kit'/'COPY.txt').read_text();self.assertNotIn('148.76',text);self.assertNotIn('UNDECIDED',text)
   self.assertFalse(d['renderer_binding_proven']);self.assertFalse(d['artwork_generated']);self.assertEqual(d['canvas'],[1080,1920])
 def test_absorbed_pages_and_preexisting_destination_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   with self.assertRaises(ValueError):self.m.export_page_kit(ROOT,self.issue,'W09-P04',Path(td)/'kit')
   with self.assertRaises(FileExistsError):self.m.export_page_kit(ROOT,self.issue,'W09-P05',Path(td))
 def test_changed_asset_digest_rejected_before_export(self):
  p=next(p for p in self.issue['pages'] if p['page_id']=='W09-P05');p['reference_assets'][0]['selected_visual_reference']['sha256']='0'*64
  with tempfile.TemporaryDirectory() as td:
   with self.assertRaises(ValueError):self.m.export_page_kit(ROOT,self.issue,'W09-P05',Path(td)/'kit')
   self.assertFalse((Path(td)/'kit').exists())

if __name__=='__main__':unittest.main()
