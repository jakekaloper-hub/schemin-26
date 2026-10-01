import json
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
STATE=ROOT/"state"
TEMPLATES=ROOT/"templates"

class AuthorCouncilBookArchitectureTests(unittest.TestCase):
    def test_open_loop_ledger_is_frozen_through_week2(self):
        data=json.loads((STATE/"CURRENT_OPEN_LOOP_LEDGER_V1.json").read_text())
        self.assertEqual(data["temporal_cutoff"],"END_OF_WEEK_2_STORY_TIME")
        self.assertTrue(data["loops"])
        for loop in data["loops"]:
            self.assertNotIn("Week 3",loop.get("latest_canon",""))
            self.assertTrue(loop.get("prohibited"))

    def test_open_loop_ids_unique(self):
        data=json.loads((STATE/"CURRENT_OPEN_LOOP_LEDGER_V1.json").read_text())
        ids=[x["id"] for x in data["loops"]]
        self.assertEqual(len(ids),len(set(ids)))

    def test_reader_rules_are_scoped_not_universal(self):
        data=json.loads((STATE/"READER_RULE_LEDGER_V1.json").read_text())
        ids=[x["id"] for x in data["rules"]]
        self.assertEqual(len(ids),len(set(ids)))
        for rule in data["rules"]:
            self.assertTrue(rule["scope"])
            self.assertIn("ambiguity",rule)

    def test_pov_template_fail_closed_fields_exist(self):
        p=json.loads((TEMPLATES/"POV_PACKET_TEMPLATE_V1.json").read_text())
        for field in [
            "story_time_cutoff","verified_knowledge","unknowns","prohibited_knowledge",
            "fictional_interior_range","attention_bias","real_owner_boundary_note"
        ]:
            self.assertIn(field,p)
        self.assertIn("blocks",p["validator_rule"])

    def test_chapter_dossier_contains_anti_recap_gate(self):
        text=(TEMPLATES/"CHAPTER_DOSSIER_V2.md").read_text()
        self.assertIn("Would this chapter still exist if the fantasy Week label were removed?",text)
        self.assertIn("omitted verified events",text)
        self.assertIn("independent world pressure",text)

    def test_book_architecture_is_condition_based(self):
        text=(ROOT/"NOVEL_BOOK_ARCHITECTURE_V2.md").read_text()
        self.assertIn("movements follow story-state transitions, not fantasy Week numbers",text)
        self.assertIn("Anti-oracle rule",text)
        self.assertNotIn("Week 4 —",text)

if __name__=="__main__":
    unittest.main(verbosity=2)
