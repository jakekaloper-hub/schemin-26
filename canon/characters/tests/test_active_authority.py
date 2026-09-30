import unittest
from canon.characters.cccp_resolver import resolve_character

class Authority(unittest.TestCase):
    def test_wilson_centaur_is_retired_only(self):
        r=resolve_character("Arsenal Centaur")
        self.assertEqual(r["character_id"],"CHAR-WILSON-LOOK")
        self.assertEqual(r.get("input_state"),"SUPERSEDED_ALIAS")
        self.assertIn("Retired identity cannot seed render",r.get("warning",""))

    def test_wilson_current_identity(self):
        r=resolve_character("Arsenal Gorilla Warrior")
        self.assertEqual(r["status"],"CURRENT_CANON_RESOLVED")
        self.assertEqual(r["character_id"],"CHAR-WILSON-LOOK")

    def test_alias_does_not_change_byars_identity(self):
        for q in ["The Immortal","That's Fantasy","His Majesty's Blood"]:
            self.assertEqual(resolve_character(q)["character_id"],"CHAR-AUSTIN-BYARS")

    def test_alias_does_not_create_jordan_character(self):
        for q in ["Fart Star","Win Ugly","Slob on my Dobb"]:
            self.assertEqual(resolve_character(q)["character_id"],"CHAR-JORDAN-HOLLINGSHEAD")

if __name__=="__main__": unittest.main()
