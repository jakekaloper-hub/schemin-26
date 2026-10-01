import json
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
STATE=ROOT/"state"
TEMPLATES=ROOT/"templates"

class AuthorCouncilBookArchitectureTests(unittest.TestCase):
    def test_open_loop_ledger_tracks_latest_hard_canon_without_future_leakage(self):
        data=json.loads((STATE/"CURRENT_OPEN_LOOP_LEDGER_V1.json").read_text())
        self.assertEqual(data["status"],"CURRENT_THROUGH_HARD_CANON_CHAPTER_III")
        self.assertEqual(data["temporal_cutoff"],"END_OF_WEEK_3_STORY_TIME")
        self.assertTrue(data["loops"])
        for loop in data["loops"]:
            self.assertNotIn("Week 4",loop.get("latest_canon",""))
            self.assertTrue(loop.get("prohibited"))

    def test_open_loop_ids_unique(self):
        data=json.loads((STATE/"CURRENT_OPEN_LOOP_LEDGER_V1.json").read_text())
        ids=[x["id"] for x in data["loops"]]
        self.assertEqual(len(ids),len(set(ids)))

    def test_open_loops_are_prioritized(self):
        data=json.loads((STATE/"CURRENT_OPEN_LOOP_LEDGER_V1.json").read_text())
        allowed={"PRIMARY","SECONDARY","AMBIENT"}
        for loop in data["loops"]:
            self.assertIn(loop["narrative_priority"],allowed)
            self.assertTrue(loop["next_review_trigger"])

    def test_reader_rule_expansion_is_gated(self):
        data=json.loads((STATE/"READER_RULE_LEDGER_V1.json").read_text())
        gate=data["new_rule_gate"]
        self.assertTrue(gate["require_existing_rule_gap"])
        self.assertTrue(gate["require_limitation_or_cost"])
        self.assertTrue(gate["require_reader_need_now"])
        self.assertTrue(gate["require_provenance_authority"])

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

    def test_minimum_pre_prose_gate_rejects_week_job(self):
        text=(TEMPLATES/"MINIMUM_PRE_PROSE_GATE_V1.md").read_text()
        self.assertIn('the chapter job is "cover Week N"',text)
        self.assertIn("What in this scene would still exist if no Contest were occurring today?",text)

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
