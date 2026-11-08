import json, unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/"generated/pie_movement_evidence.json"
class PIEEvidenceTests(unittest.TestCase):
 def test_evidence_cannot_claim_movement(self):
  if not P.exists():self.skipTest("no PIE probe")
  d=json.loads(P.read_text())
  if not d.get("pawn_found") or not d.get("pie_started"):
   self.assertFalse(d.get("movement_verified"))
  if d.get("movement_verified"):
   self.assertTrue(d.get("pawn_found") and d.get("pie_started"))
