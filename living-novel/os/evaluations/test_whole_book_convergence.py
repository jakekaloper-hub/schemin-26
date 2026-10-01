import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
WHOLE = ROOT / "whole-book"
REPO = ROOT.parent

class WholeBookConvergenceTests(unittest.TestCase):
    def text(self, name):
        return (WHOLE / name).read_text()

    def test_hard_canon_chapter3_is_only_current_chapter3_authority(self):
        matrix = self.text("WHOLE_BOOK_SOURCE_AUTHORITY_MATRIX_V1.md")
        self.assertIn("CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md", matrix)
        self.assertIn("CHAPTER_03_THE_PRICE_OF_ATTENTION_V3.md", matrix)
        self.assertIn("SUPERSEDED AS A MERGE UNIT", matrix)
        self.assertNotIn("living-novel/manuscript/v3/SCHEMIN_26_CURRENT_MASTER_MANUSCRIPT_V3.md | ACTIVE", matrix)

    def test_continuation_contract_blocks_week_equals_chapter(self):
        text = self.text("LIVE_NOVEL_CONTINUATION_CONTRACT_V1.md")
        self.assertIn("Never default to “Week N chapter.”", text)
        self.assertIn("Chapter IV remains unauthorized", text)
        self.assertIn("Week 4 outcome remains UNKNOWN", text)

    def test_memo_translation_treats_week3_as_source_evidence(self):
        text = self.text("MEMO_TO_NOVEL_TRANSLATION_REGISTER_V1.md")
        self.assertIn("HARD-CANON CHAPTER III SOURCE EVIDENCE", text)
        self.assertIn("causal aftermath, not recap", text)

    def test_world_hydration_preserves_mire_hill_non_sovereignty(self):
        text = self.text("WORLD_ATLAS_NARRATIVE_HYDRATION_REGISTER_V1.md")
        self.assertIn("standard below summit", text)
        self.assertIn("summit remains unclaimed", text)
        self.assertIn("social interpretation, not territorial law", text)

    def test_index_rejects_pr61_v3_manuscript_as_authority(self):
        text = self.text("_INDEX.md")
        self.assertIn("manuscript/v3/", text)
        self.assertIn("not current authority", text)
        self.assertIn("CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md", text)

    def test_publication_manifest_still_indexes_current_chapter3(self):
        manifest = json.loads((REPO / "governance" / "publication-manifest" / "PUBLICATION_MANIFEST_V1.json").read_text())
        ch3 = next(x for x in manifest["publications"] if x["publication_id"] == "novel.2026.chapter-03")
        self.assertEqual(ch3["canonical_artifact"], "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md")
        self.assertEqual(ch3["release_state"], "CANON_CLOSED")

if __name__ == "__main__":
    unittest.main(verbosity=2)
