import json
from pathlib import Path
import unittest
D=Path(__file__).parent
class CoverageTests(unittest.TestCase):
 def test_every_observation_accounted_for(self):
  for y in range(2015,2026):
   d=json.loads((D/f'{y}_FIXTURE_COVERAGE.json').read_text())
   self.assertEqual(d['returned_rows'],sum(len(e['observations']) for e in d['events']))
   self.assertEqual(d['distinct_source_entries'],d['observed_paired_contests']+d['unpaired_rows'])
   self.assertEqual(len({e['event_id'] for e in d['events']}),len(d['events']))
   self.assertFalse(any(e['conflicting_observations'] for e in d['events']))
 def test_multiweek_aggregate_not_two_contests(self):
  d=json.loads((D/'2015_FIXTURE_COVERAGE.json').read_text())
  final=[e for e in d['events'] if e['period']==15 and e['tier']=='WINNERS_BRACKET']
  self.assertEqual(len(final),1);self.assertEqual(final[0]['observed_scoring_weeks'],[16,17])
  self.assertEqual(final[0]['away_score'],211.5)
 def test_unpaired_rows_do_not_count_as_played(self):
  d=json.loads((D/'2022_FIXTURE_COVERAGE.json').read_text())
  self.assertEqual(d['returned_rows'],105);self.assertEqual(d['observed_paired_contests'],99)
  self.assertEqual(d['unpaired_rows'],6)
  self.assertTrue(all(e['away'] is None for e in d['events'] if e['kind']=='UNPAIRED_PROVIDER_ROW'))
 def test_repeat_opponents_different_periods_retained(self):
  d=json.loads((D/'2025_FIXTURE_COVERAGE.json').read_text())
  meetings=[e for e in d['events'] if {e['home_id'],e['away_id']}=={1,8}]
  self.assertGreater(len(meetings),1);self.assertEqual(len({e['period'] for e in meetings}),len(meetings))
 def test_current_finality_not_inferred(self):
  d=json.loads((D/'2026_FIXTURE_COVERAGE.json').read_text())
  self.assertEqual(d['observed_paired_contests'],36)
  self.assertEqual(d['unresolved_finality'],0)
  self.assertTrue(all(e['provider_winner_flag'] in ('HOME','AWAY') for e in d['events'] if e['period']==4))
  self.assertTrue(all(e['superseded_observation']['status'].startswith('PROVISIONAL') for e in d['events'] if e['period']==4))
  obi=next(e for e in d['events'] if e['period']==4 and e['side_b']=='ObiWan Jacoby')
  self.assertEqual((obi['side_a_score'],obi['side_b_score']),(139.67,157.33))
  self.assertEqual(max(e['period'] for e in d['events']),6)
 def test_supported_bye_does_not_promote_other_unpaired_rows(self):
  d=json.loads((D/'2021_FIXTURE_COVERAGE.json').read_text())
  unpaired=[e for e in d['events'] if e['kind']=='UNPAIRED_PROVIDER_ROW']
  self.assertEqual(sum(e['unpaired_status']=='BYE_REPORTED_BY_HISTORICAL_PRESSURE_LEDGER' for e in unpaired),1)
  self.assertEqual(sum(e['unpaired_status'].endswith('NOT_A_PLAYED_CONTEST') for e in unpaired),5)
 def test_display_ties_preserve_declared_winner_without_inventing_tiebreak(self):
  for year,period in [(2017,3),(2018,15)]:
   d=json.loads((D/f'{year}_FIXTURE_COVERAGE.json').read_text())
   flagged=[e for e in d['events'] if e['result_qualification'].startswith('DISPLAY_SCORE_EQUAL')]
   self.assertEqual(len(flagged),1);self.assertEqual(flagged[0]['period'],period)
   self.assertEqual(flagged[0]['winner'],'HOME')
   self.assertEqual(flagged[0]['event_id_authority'],'MISSION_GENERATED_JOIN_KEY_NOT_PROVIDER_FIXTURE_ID')
 def test_no_literary_acceptance_from_presence(self):
  for y in range(2015,2027):
   d=json.loads((D/f'{y}_FIXTURE_COVERAGE.json').read_text())
   self.assertTrue(all(not e['literary_coverage']['accepted_locations'] for e in d['events']))
if __name__=='__main__':unittest.main()
