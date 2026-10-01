import importlib.util
import json
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
VALIDATOR=ROOT/"qa"/"pov_packet_validator.py"
spec=importlib.util.spec_from_file_location("pov_packet_validator",VALIDATOR)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class POVPacketValidatorTests(unittest.TestCase):
    def good(self):
        return {
          "character_id":"jake_kaloper",
          "pov_class":"PRINCIPAL_CHARACTER",
          "story_time_cutoff":"WEEK_2_END",
          "real_owner_derived":True,
          "real_owner_boundary_note":"Fictional Schemin interiority only.",
          "verified_knowledge":["week2_result"],
          "unknowns":["future_results"],
          "prohibited_knowledge":["week3_outcomes"],
          "fictional_interior_range":["strategic uncertainty"],
          "attention_bias":["trade leverage","resource position"]
        }

    def test_valid_packet_passes(self):
        self.assertEqual(mod.validate_pov_packet(self.good()),[])

    def test_principal_packet_requires_real_owner_firewall(self):
        p=self.good(); p["real_owner_boundary_note"]=None
        self.assertIn("MISSING_REAL_OWNER_FIREWALL",mod.validate_pov_packet(p))

    def test_attention_bias_required(self):
        p=self.good(); p["attention_bias"]=[]
        self.assertIn("MISSING_ATTENTION_BIAS",mod.validate_pov_packet(p))

    def test_principal_interior_range_required(self):
        p=self.good(); p["fictional_interior_range"]=[]
        self.assertIn("MISSING_FICTIONAL_INTERIOR_RANGE",mod.validate_pov_packet(p))

    def test_missing_cutoff_blocks(self):
        p=self.good(); p["story_time_cutoff"]=None
        self.assertIn("MISSING_STORY_TIME_CUTOFF",mod.validate_pov_packet(p))

if __name__=="__main__":
    unittest.main(verbosity=2)
