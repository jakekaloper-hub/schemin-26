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

    def test_dk_character_positive_anatomy_not_negated_in_visual_packet(self):
        p=build_packet("LOC-DK-HIGHLAND-STRONGHOLD")
        self.assertEqual(p["character"]["principal_character_ids"], ["CHAR-WILSON-LOOK"])
        # Environmental context must never self-authorize character renders:
        self.assertFalse(p["civilization_context"]["character_rendering_allowed"])
        self.assertEqual(p["character"]["reference_status"], "CHARACTER_REFERENCE_GATE_SEPARATE")
        forbidden=set(p["character"]["negative_locks"])
        required_negative={"NO_GENERIC_BIPEDAL_GORILLA","NO_HORSE_HEADED_CENTAUR",
                           "NO_RIDER_MOUNT_SUBSTITUTE","NO_TWO_CREATURE_SUBSTITUTE",
                           "NO_ARSENAL_IDENTITY_OMISSION"}
        self.assertTrue(required_negative.issubset(forbidden))
        self.assertNotIn("NO_CENTAUR_ANATOMY", forbidden)
        for valid_positive in ("ARSENAL_GORILLA_CENTAUR_WARRIOR",
                               "ONE_INTEGRATED_GORILLA_EQUINE_BODY",
                               "FOUR_LEGGED_CENTAUR_LOWER_BODY"):
            self.assertNotIn(valid_positive, forbidden)
        self.assertIn("Gorilla Centaur Warrior", p["world"]["world_state"][0])

    def test_invalid_location_rejected(self):
        with self.assertRaises(ValueError):
            build_packet("LOC-NONEXISTENT")

    def test_broken_context_rejected(self):
        with patch("world.engine.civilization_consumers.resolve_scene_context",return_value={"ok":False,"code":"BROKEN"}):
            with self.assertRaisesRegex(ValueError,"unresolved civilization context"):
                build_packet("LOC-LEAGUE-CHAMBER")

if __name__=="__main__":
    unittest.main()
