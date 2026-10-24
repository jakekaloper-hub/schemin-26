import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from world.engine.civilization_consumers import resolve_scene_context
from world.engine.universe_resolver import UniverseResolver

class ConsumerContractTests(unittest.TestCase):
    def test_all_four_share_one_canonical_context(self):
        views = [resolve_scene_context("LOC-LEAGUE-CHAMBER", c) for c in ("memo","novel","atlas","art_environment")]
        self.assertTrue(all(v["ok"] for v in views), views)
        self.assertEqual({v["region_id"] for v in views}, {"REG-CENTRAL-BASIN"})
        self.assertEqual(len({v["context_id"] for v in views}), 1)
        self.assertEqual(len({tuple(v["ordinary_life"]) for v in views}), 1)
        self.assertFalse(views[3]["character_rendering_allowed"])

    def test_unknown_location_fails_all(self):
        for consumer in ("memo","novel","atlas","art_environment"):
            self.assertEqual(resolve_scene_context("LOC-INVENTED", consumer)["code"], "UNKNOWN_LOCATION")

    def test_unknown_consumer_fails(self):
        self.assertEqual(resolve_scene_context("LOC-LEAGUE-CHAMBER", "canon_writer")["code"], "UNKNOWN_CONSUMER")

    def test_resolver_query_is_executable(self):
        view = UniverseResolver().what_civilization_context("LOC-LEAGUE-CHAMBER")
        self.assertTrue(view["ok"])
        self.assertEqual(view["physical_zone_id"], "REG-CENTRAL-BASIN")

    def test_all_canonical_locations_resolve(self):
        r = UniverseResolver()
        for loc in r.locations:
            with self.subTest(loc=loc["id"]):
                self.assertTrue(r.what_civilization_context(loc["id"])["ok"])

if __name__ == "__main__":
    unittest.main()
