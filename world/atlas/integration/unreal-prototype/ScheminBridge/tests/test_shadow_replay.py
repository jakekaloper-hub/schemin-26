import unittest
from ScheminBridge.shadow_replay import replay
class ShadowReplayTests(unittest.TestCase):
 def test_historical_bridge(self):
  a=replay("EVT-W3-BRIDGE")
  self.assertEqual(a["mode"],"SHADOW_PREVIEW_ONLY")
  self.assertFalse(a["mutates_world_state"])
  self.assertEqual(a["week"],3)
 def test_missing_event_blocked(self):
  with self.assertRaises(ValueError):replay("NOT-AN-EVENT")
 def test_narrative_interpretation_not_world_canon(self):
  with self.assertRaises(ValueError):replay("EVT-W2-LLC-INTRUSION")
