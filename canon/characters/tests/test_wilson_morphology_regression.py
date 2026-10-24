import unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/"canon/characters"))
from cccp_resolver import resolve_character

class WilsonMorphologyRegression(unittest.TestCase):
    def test_current_identity(self):
        r=resolve_character("Wilson Look")
        self.assertEqual(r["status"],"CURRENT_CANON_RESOLVED")
        self.assertEqual(r["identity"],"Arsenal Gorilla Centaur Warrior")
        # Anatomy is owned by the approved registry, not the name resolver API.
        registry=(ROOT/"canon/characters/CHARACTER_REGISTRY.yaml").read_text()
        row=next(line for line in registry.splitlines() if "id: CHAR-WILSON-LOOK," in line)
        self.assertIn("FOUR-LEGGED CENTAUR LOWER BODY",row)
        self.assertIn("ONE BODY",row)

    def test_arsenal_centaur_is_not_retired_alias(self):
        r=resolve_character("Arsenal Centaur")
        self.assertEqual(r["status"],"CURRENT_CANON_RESOLVED")
        self.assertNotEqual(r.get("input_state"),"SUPERSEDED_ALIAS")

    def test_week4_temporal_canon(self):
        t=(ROOT/"memo-os/week-4/WEEK_4_TEMPORAL_CANON_RECEIPT_V1.md").read_text()
        self.assertIn("Arsenal Gorilla Centaur Warrior",t)
        self.assertNotIn("centaur/equine form RETIRED",t)
        self.assertNotIn("centaur rejected",t)

    def test_registry_rejects_wrong_reconstructions(self):
        t=(ROOT/"canon/characters/CHARACTER_REGISTRY.yaml").read_text()
        self.assertIn("FOUR-LEGGED CENTAUR LOWER BODY",t)
        self.assertIn("generic bipedal gorilla",t)
        self.assertIn("horse-headed centaur",t)

if __name__=="__main__": unittest.main()
