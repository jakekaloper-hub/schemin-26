import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location("story",ROOT/"living-novel/os/adapters/build_historical_story_room.py")
story=importlib.util.module_from_spec(spec);spec.loader.exec_module(story)
class HistoricalRoomTests(unittest.TestCase):
 def test_eleven_seasons_have_documented_verified_finals(self):
  a=story.build_all();self.assertEqual([x["season"] for x in a],list(range(2015,2026)))
  self.assertEqual(sum(x["game_row_count"] for x in a),1117)
  self.assertTrue(all(x["championship"]["winner_team_id"] for x in a))
 def test_2017_missing_matchup_ids_are_explicit(self):
  a=story.build(2017)
  self.assertEqual(a["team_identity_coverage"],"PARTIAL_TEAM_ID_SOURCE_GAP")
  self.assertLess(len(a["historical_team_slots"]),12)
 def test_no_season_assumes_historical_owner_division(self):
  for a in story.build_all():
   self.assertTrue(any("Division memberships unknown" in x for x in a["evidence_limits"]))
   self.assertEqual(a["review_status"],"NOT_INDEPENDENTLY_REVIEWED")
 def test_year_boundaries(self):
  for y in (2014,2026):
   with self.assertRaises(ValueError):story.build(y)
if __name__=="__main__":unittest.main()
