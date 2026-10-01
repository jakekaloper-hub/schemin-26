import importlib.util
import json
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]
VALIDATOR=ROOT/"qa"/"pov_packet_validator.py"
PACKET=REPO/"living-novel"/"production"/"chapter-03"/"CHAPTER_03_POV_PACKET_WILSON_V1.json"
GATE=REPO/"living-novel"/"production"/"chapter-03"/"CHAPTER_03_MINIMUM_PRE_PROSE_GATE_V1.md"
RECON=REPO/"living-novel"/"production"/"chapter-03"/"CHAPTER_03_TARGETED_PANEL_RECONCILIATION_V1.md"

spec=importlib.util.spec_from_file_location("pov_packet_validator",VALIDATOR)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class Chapter03MinimumGateTests(unittest.TestCase):
    def test_wilson_packet_passes_fail_closed_validator(self):
        packet=json.loads(PACKET.read_text())
        self.assertEqual(mod.validate_pov_packet(packet),[])

    def test_gate_is_causal_not_weekly(self):
        text=GATE.read_text()
        self.assertIn("Movement II",text)
        self.assertIn("summit standard",text.lower())
        self.assertIn("Off-page",text)
        self.assertIn("does **not** owe foreground scenes",text)

    def test_current_dk_identity_is_locked(self):
        packet=json.loads(PACKET.read_text())
        self.assertIn("Arsenal Gorilla Warrior",packet["canonical_character"])
        self.assertTrue(any("centaur" in x.lower() for x in packet["vocabulary_register_constraints"]))

    def test_future_results_are_firewalled(self):
        packet=json.loads(PACKET.read_text())
        self.assertTrue(any("Week 4 result" in x for x in packet["unknowns"]))
        self.assertTrue(any("Future league outcomes" in x for x in packet["prohibited_knowledge"]))

    def test_panel_closes_minimum_gate_only(self):
        text=RECON.read_text()
        self.assertIn("MINIMUM PRE-PROSE GATE CLOSED",text)
        self.assertIn("Hydrate **Chapter Dossier V2**",text)
        self.assertIn("Do not draft prose until",text)

if __name__=="__main__":
    unittest.main(verbosity=2)
