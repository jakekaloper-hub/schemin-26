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
        for valid_positive in ("ARSENAL_GORILLA_WARRIOR",
                               "ONE_BODY_GORILLA_CENTAUR_FOUR_LEGS"):
            self.assertNotIn(valid_positive, forbidden)
        self.assertIn("Gorilla Centaur Warrior", p["world"]["world_state"][0])

    def test_all_twelve_owner_packets_preserve_positive_identity(self):
        """Fail if owner-specific body locks are accidentally turned into negatives."""
        import json
        domains=json.loads((ROOT/"world/data/owner_domains.json").read_text())["domains"]
        for domain in domains:
            with self.subTest(character=domain["character_id"]):
                packet=build_packet(domain["primary_location_id"])
                character=packet["character"]
                self.assertIn(domain["character_id"], character["principal_character_ids"])
                self.assertEqual(character["reference_status"],"CHARACTER_REFERENCE_GATE_SEPARATE")
                self.assertFalse(packet["civilization_context"]["character_rendering_allowed"])
                positive=[x for x in domain["canon_guard"] if not x.startswith("NO_")]
                negative=[x for x in domain["canon_guard"] if x.startswith("NO_")]
                self.assertTrue(set(positive).issubset(set(character["body_locks"])))
                self.assertTrue(set(negative).issubset(set(character["negative_locks"])))
                self.assertFalse(set(positive) & set(character["negative_locks"]))

    def test_specific_historic_drifts_are_never_negative_character_locks(self):
        cases={
            "LOC-TDS-WATERFALL-TEMPLE":("ONE_BODY_THREE_SERPENT_HEADS",[]),
            "LOC-BELT-KEEPER-KEEP":("CHAMPIONSHIP_BELT",[]),
            "LOC-CHILI-STABLE":("DARK_HORSE",[]),
            "LOC-TRADE-JEDI-MOUNTAIN-BASE":(None,["NO_CHAMPIONSHIP_BELT"]),
            "LOC-DK-HIGHLAND-STRONGHOLD":("ONE_BODY_GORILLA_CENTAUR_FOUR_LEGS",["NO_GENERIC_BIPEDAL_GORILLA"]),
        }
        for lid,(positive,negatives) in cases.items():
            with self.subTest(location=lid):
                packet=build_packet(lid)["character"]
                if positive is not None:
                    self.assertIn(positive,packet["body_locks"])
                    self.assertNotIn(positive,packet["negative_locks"])
                for bad in negatives:
                    self.assertIn(bad,packet["negative_locks"])

    def test_invalid_location_rejected(self):
        with self.assertRaises(ValueError):
            build_packet("LOC-NONEXISTENT")

    def test_broken_context_rejected(self):
        with patch("world.engine.civilization_consumers.resolve_scene_context",return_value={"ok":False,"code":"BROKEN"}):
            with self.assertRaisesRegex(ValueError,"unresolved civilization context"):
                build_packet("LOC-LEAGUE-CHAMBER")

if __name__=="__main__":
    unittest.main()
