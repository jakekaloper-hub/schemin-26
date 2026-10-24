import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from world.engine.civilization_temporal import resolve_seasonal_division_overlay as resolve

class TemporalTests(unittest.TestCase):
    def test_basin_nonexclusive_2026(self):
        p=resolve("REG-CENTRAL-BASIN",2026,5)
        self.assertTrue(p["ok"])
        self.assertGreater(len(p["division_ids"]),1)
        self.assertEqual(p["week_specific_event_status"],"NOT_INFERRED")

    def test_wrong_season_blocked(self):
        self.assertEqual(resolve("REG-CENTRAL-BASIN",2025,5)["code"],"UNVERIFIED_SEASON")

    def test_week_missing_or_invalid_blocked(self):
        for week in (None,0,19,"5"):
            self.assertEqual(resolve("REG-CENTRAL-BASIN",2026,week)["code"],"SEASON_AND_WEEK_REQUIRED")

    def test_region_missing_blocked(self):
        self.assertEqual(resolve("REG-FAKE",2026,5)["code"],"NO_DIVISION_PRESENCE")

if __name__=="__main__":
    unittest.main()
