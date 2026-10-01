import hashlib
import json
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]

CH=REPO/"living-novel"/"manuscript"/"CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md"
FINAL=REPO/"living-novel"/"qa"/"CHAPTER_03_FINAL_CANON_GATE_V1.md"
RECEIPT=REPO/"living-novel"/"qa"/"CHAPTER_03_CANON_RELEASE_RECEIPT_V1.md"
LOOPS=REPO/"living-novel"/"os"/"state"/"CURRENT_OPEN_LOOP_LEDGER_V1.json"
RULES=REPO/"living-novel"/"os"/"state"/"READER_RULE_LEDGER_V1.json"
WORLD=REPO/"world"/"data"/"current_world_state.json"
MEMORY=REPO/"world"/"data"/"world_memory.json"
MANIFEST=REPO/"governance"/"publication-manifest"/"PUBLICATION_MANIFEST_V1.json"
NEXT=REPO/"living-novel"/"production"/"NEXT_CAUSAL_STORY_GATE_V1.md"

def git_blob_sha(path):
    data=path.read_bytes()
    payload=b"blob "+str(len(data)).encode()+b"\0"+data
    return hashlib.sha1(payload).hexdigest()

class Chapter03CanonCloseoutTests(unittest.TestCase):
    def test_approved_manuscript_bytes_are_exact(self):
        self.assertEqual(git_blob_sha(CH),"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc")

    def test_final_gate_and_receipt_exist(self):
        self.assertIn("HARD MANUSCRIPT CANON / CLOSED",FINAL.read_text())
        self.assertIn("Promotion PR:** #77",RECEIPT.read_text())

    def test_open_loops_transacted(self):
        data=json.loads(LOOPS.read_text())
        self.assertEqual(data["status"],"CURRENT_THROUGH_HARD_CANON_CHAPTER_III")
        self.assertEqual(data["temporal_cutoff"],"END_OF_WEEK_3_STORY_TIME")
        by={x["id"]:x for x in data["loops"]}
        self.assertEqual(by["OL-004"]["state"],"PARTIALLY_PAID")
        self.assertIn("sole 3-0",by["OL-004"]["latest_canon"])
        self.assertIn("OL-009",by)

    def test_reader_rule_is_scoped(self):
        data=json.loads(RULES.read_text())
        rule=next(x for x in data["rules"] if x["id"]=="RR-006")
        self.assertIn("neutral Encounter ground",rule["rule"])
        self.assertIn("supported scope",rule["ambiguity"])

    def test_mire_hill_state_preserves_non_sovereignty(self):
        data=json.loads(WORLD.read_text())
        state=data["locations"]["LOC-DK-MUD-HILL"]
        self.assertTrue(any("standard placed below summit" in x for x in state))
        self.assertTrue(any("summit remains unclaimed" in x for x in state))

    def test_world_memory_separates_social_interpretation(self):
        data=json.loads(MEMORY.read_text())
        event=next(x for x in data["events"] if x["event_id"]=="EVT-W3-MIRE-HILL")
        self.assertTrue(any("crown/ownership imagery" in x for x in event["social_effect"]))
        self.assertTrue(any("distinct from sovereignty" in x for x in event["institutional_effect"]))

    def test_publication_manifest_consumes_novel_authority(self):
        data=json.loads(MANIFEST.read_text())
        ch3=next(x for x in data["publications"] if x["publication_id"]=="novel.2026.chapter-03")
        self.assertEqual(ch3["release_state"],"CANON_CLOSED")
        self.assertEqual(ch3["source_interval"]["kind"],"chapter_causal_interval")
        self.assertIn("living-novel/qa/CHAPTER_03_FINAL_CANON_GATE_V1.md",ch3["authority_refs"])

    def test_next_story_stops_at_live_event_gate(self):
        text=NEXT.read_text()
        self.assertIn("HOLD — LIVE EVENT EVIDENCE NOT YET CLOSED",text)
        self.assertIn("No Chapter IV story architecture is authorized yet",text)

if __name__=="__main__":
    unittest.main(verbosity=2)
