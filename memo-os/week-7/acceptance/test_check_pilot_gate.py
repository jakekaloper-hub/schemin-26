import unittest
from unittest.mock import patch
from .check_pilot_gate import assess

class PilotGateTest(unittest.TestCase):
    def test_real_gate_fails_closed_without_provider(self):
        result = assess()
        self.assertEqual(result["renderer_negotiation"]["state"], "GENERATION_ROUTE_SUBJECT_BINDING_UNPROVEN")
        self.assertFalse(result["ready_for_render"])
        self.assertFalse(result["independent_umpire_accepted"])

    def test_missing_source_cannot_pass(self):
        with patch("pathlib.Path.is_file", return_value=False):
            result = assess()
        self.assertFalse(result["ready_for_render"])
        self.assertIn(False, result["source_files"].values())

if __name__ == "__main__":
    unittest.main()
