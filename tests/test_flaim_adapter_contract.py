import copy
import importlib.util
import json
import pathlib
import unittest
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
ADAPTER_PATH = ROOT / "data-gateway" / "flaim_adapter.py"
FIXTURE = ROOT / "data/provider-receipts/flaim/1417621/2026/week-4/2026-09-29T175654Z.json"

spec = importlib.util.spec_from_file_location("flaim_adapter", ADAPTER_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class FlaimAdapterContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.capture = json.loads(FIXTURE.read_text())

    def test_current_receipt_validates(self):
        mod.validate_capture(self.capture)

    def test_receipt_shape(self):
        self.assertEqual(len(self.capture["league"]["teams"]), 12)
        self.assertEqual(len(self.capture["standings"]), 12)
        self.assertEqual(len(self.capture["week4_matchups"]), 6)
        self.assertEqual(len(self.capture["rosters"]), 12)
        self.assertEqual(self.capture["transactions"]["count"], 47)

    def test_week4_matchups_cover_each_team_once(self):
        ids = []
        for matchup in self.capture["week4_matchups"]:
            ids.extend([matchup["home"]["team_id"], matchup["away"]["team_id"]])
        self.assertEqual(sorted(ids), [str(i) for i in range(1, 13)])

    def test_normalizer_preserves_transaction_limitation(self):
        now = datetime(2026, 9, 29, 18, 0, tzinfo=timezone.utc)
        normalized = mod.normalize_capture(self.capture, now=now, slo_seconds=3600)
        self.assertFalse(normalized["meta"]["stale"])
        self.assertFalse(normalized["transactions"]["exact_trade_assets_complete"])
        self.assertTrue(
            normalized["transactions"]["limitations"]["structured_details_incomplete"]
        )

    def test_freshness_recomputed_at_read_time(self):
        now = datetime(2026, 9, 29, 20, 0, tzinfo=timezone.utc)
        normalized = mod.normalize_capture(self.capture, now=now, slo_seconds=3600)
        self.assertTrue(normalized["meta"]["stale"])
        self.assertGreater(normalized["meta"]["snapshot_age_seconds"], 3600)

    def test_wrong_league_rejected(self):
        bad = copy.deepcopy(self.capture)
        bad["league"]["league_id"] = "999"
        with self.assertRaises(mod.FlaimContractError):
            mod.validate_capture(bad)

    def test_duplicate_team_matchup_rejected(self):
        bad = copy.deepcopy(self.capture)
        bad["week4_matchups"][0]["away"]["team_id"] = bad["week4_matchups"][0]["home"]["team_id"]
        with self.assertRaises(mod.FlaimContractError):
            mod.validate_capture(bad)

    def test_empty_roster_rejected(self):
        bad = copy.deepcopy(self.capture)
        bad["rosters"][0]["players"] = []
        with self.assertRaises(mod.FlaimContractError):
            mod.validate_capture(bad)


if __name__ == "__main__":
    unittest.main()
