import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location('multi_roster',ROOT/'living-novel/os/adapters/flaim/build_multi_season_roster_deltas.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class MultiSeasonRosterTests(unittest.TestCase):
 def test_twelve_per_season(self):
  for year in (2019,2020,2021,2022,2023,2024,2025):
   x=m.build(year)
   self.assertEqual([t['historical_team_id'] for t in x['teams']],list(range(1,13)))
 def test_no_invented_transactions_or_divisions(self):
  for year in (2019,2020,2021,2022,2023,2024,2025):
   self.assertTrue(all(t['transaction_type']=='UNKNOWN_UNVERIFIED' and t['season_division'].startswith('UNKNOWN') for t in m.build(year)['teams']))
 def test_roster_set_arithmetic(self):
  for year in (2019,2020,2021,2022,2023,2024,2025):
   for t in m.build(year)['teams']:
    self.assertEqual(t['retained_count']+len(t['departed_ids']),t['week1_count'])
    self.assertEqual(t['retained_count']+len(t['appeared_ids']),t['week14_count'])
 def test_unknown_year_refused(self):
  with self.assertRaises(ValueError):m.build(2018)
if __name__=='__main__':unittest.main()
