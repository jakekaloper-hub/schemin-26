import unittest
from canon.characters.runtime.local_reference_bundle import prepare_local_reference_bundle

class LocalBundleTests(unittest.TestCase):
    def test_two_subjects_verified_not_render_eligible(self):
        p = prepare_local_reference_bundle(["CHAR-WILSON-LOOK","CHAR-JAKE-KALOPER"])
        self.assertEqual(len(p["records"]),2)
        self.assertFalse(p["renderer_eligible"])
        self.assertTrue(all(not r["provider_binding_proven"] for r in p["records"]))
        self.assertTrue(all(r["original_primary_supersession"] is False for r in p["records"]))
    def test_unknown_character_fails(self):
        with self.assertRaisesRegex(ValueError,"UNKNOWN_CHARACTER_ID"):
            prepare_local_reference_bundle(["CHAR-UNKNOWN"])
    def test_duplicate_character_fails(self):
        with self.assertRaisesRegex(ValueError,"CHARACTER_SET_INVALID"):
            prepare_local_reference_bundle(["CHAR-WILSON-LOOK","CHAR-WILSON-LOOK"])

if __name__=="__main__":
    unittest.main()
