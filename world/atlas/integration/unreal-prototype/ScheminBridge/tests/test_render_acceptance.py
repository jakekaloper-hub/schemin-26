import json,unittest
from pathlib import Path
from ScheminBridge.render_acceptance import ROOT
class RenderAcceptanceTests(unittest.TestCase):
 def test_no_false_positive(self):
  p=ROOT/"generated/render_acceptance.json"
  if not p.exists():self.skipTest("report not generated")
  d=json.loads(p.read_text())
  if not (ROOT/"generated/rendered_showcase_preview.png").exists():
   self.assertFalse(d["render_verified"])
