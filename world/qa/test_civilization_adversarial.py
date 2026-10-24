"""Adversarial fixtures against civilization and route source drift."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from world.engine import civilization_context as cc
from world.engine.central_basin_pilot import build_central_basin_pilot
from world.engine.universe_resolver import UniverseResolver

class AdversarialTests(unittest.TestCase):
    def test_missing_settlement_fails_closed(self):
        real = cc._load
        def altered(file, key):
            rows = real(file, key)
            if file == "settlements.json":
                return [r for r in rows if r["physical_zone_id"] != "REG-CENTRAL-BASIN"]
            return rows
        with patch.object(cc, "_load", side_effect=altered):
            self.assertEqual(cc.resolve_civilization_context("REG-CENTRAL-BASIN")["error"], "INCOMPLETE_REGION_CONTEXT")

    def test_duplicate_economy_fails_closed(self):
        real = cc._load
        def altered(file, key):
            rows = real(file, key)
            if file == "economies.json":
                return rows + [next(x for x in rows if x["physical_zone_id"] == "REG-CENTRAL-BASIN")]
            return rows
        with patch.object(cc, "_load", side_effect=altered):
            self.assertEqual(cc.resolve_civilization_context("REG-CENTRAL-BASIN")["error"], "INCOMPLETE_REGION_CONTEXT")

    def test_foreign_anchor_fails_closed(self):
        real = cc._load
        def altered(file, key):
            rows = real(file, key)
            if file == "settlements.json":
                import copy
                rows = copy.deepcopy(rows)
                next(x for x in rows if x["physical_zone_id"] == "REG-CENTRAL-BASIN")["anchor_location_ids"].append("LOC-TRADE-JEDI-MOUNTAIN-BASE")
            return rows
        with patch.object(cc, "_load", side_effect=altered):
            self.assertEqual(cc.resolve_civilization_context("REG-CENTRAL-BASIN")["error"], "INVALID_LOCATION_ANCHOR")

    def test_missing_route_fails_pilot(self):
        original = UniverseResolver.how_to_travel
        def altered(self, start, end):
            if start == "LOC-LEAGUE-CHAMBER" and end == "LOC-PITTSYS-BOOK":
                return {"ok": False, "code": "NO_ROUTE"}
            return original(self, start, end)
        with patch.object(UniverseResolver, "how_to_travel", altered):
            self.assertEqual(build_central_basin_pilot()["code"], "UNVERIFIED_ROUTE")

    def test_moved_anchor_fails_pilot(self):
        original = UniverseResolver.__init__
        def altered(self):
            original(self)
            self.loc_by_id["LOC-LEAGUE-ARCHIVE"] = {**self.loc_by_id["LOC-LEAGUE-ARCHIVE"], "physical_zone_id": "REG-NORTHERN-SPINE"}
        with patch.object(UniverseResolver, "__init__", altered):
            self.assertEqual(build_central_basin_pilot()["code"], "INVALID_BASIN_ANCHOR")

if __name__ == "__main__":
    unittest.main()
