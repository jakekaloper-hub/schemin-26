import sys
import unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from world.production.build_visual_world_packet import build_packet

class VisualPacketTests(unittest.TestCase):
    def test_basin_environment_hydrated(self):
        p=build_packet("LOC-LEAGUE-CHAMBER")
        c=p["civilization_context"]
        self.assertEqual(c["region_id"],"REG-CENTRAL-BASIN")
        self.assertFalse(c["character_rendering_allowed"])
        self.assertEqual(c["authority"],"READ_ONLY_INTERPRETIVE_CONTEXT")

    def test_invalid_location_rejected(self):
        with self.assertRaises(ValueError):
            build_packet("LOC-NONEXISTENT")

    def test_broken_context_rejected(self):
        with patch("world.engine.civilization_consumers.resolve_scene_context",return_value={"ok":False,"code":"BROKEN"}):
            with self.assertRaisesRegex(ValueError,"unresolved civilization context"):
                build_packet("LOC-LEAGUE-CHAMBER")

if __name__=="__main__":
    unittest.main()
