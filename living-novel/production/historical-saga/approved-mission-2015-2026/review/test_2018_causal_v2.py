"""Regressions for proposed 2018 single-POV causal reader V2.

This check DOES NOT establish human-owner historical identity, real geography,
independent literary acceptance, or permission to promote the candidate.
"""
import hashlib
import json
import re
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent / "manuscript" / "2018-jake-breakwater"
CANDIDATE = ROOT / "THE_NAMES_HE_DID_NOT_KEEP_CAUSAL_READING_CANDIDATE_V2_NONCANON.md"
PREDECESSOR = ROOT / "THE_NAMES_HE_DID_NOT_KEEP_NONCANON.md"
REGISTER = ROOT / "SCENE_REGISTER_CAUSAL_V2.json"
EARLIER_REGISTER = ROOT / "SCENE_REGISTER.json"
REPO = next(p for p in HERE.parents if (p / "living-novel/manuscript/PROLOGUE_DRAFT_V1.md").exists())
PROTECTED = {
    "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
PREDECESSOR_GIT_SHA = "6b8b59368ad10c19e67c52731539aaed321ea9c3"

def git_blob_sha(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

class Test2018CausalV2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = CANDIDATE.read_text(encoding="utf-8")
        cls.story = cls.text[cls.text.index("## I. Half a Voice"):]
        cls.reg = json.loads(REGISTER.read_text(encoding="utf-8"))
        cls.old_reg = json.loads(EARLIER_REGISTER.read_text(encoding="utf-8"))

    def test_protected_canon_sha_matches_current_main_baseline(self):
        for filename, sha in PROTECTED.items():
            with self.subTest(filename=filename):
                self.assertEqual(git_blob_sha(REPO / "living-novel/manuscript" / filename), sha)

    def test_preserves_previous_historical_eight_vignette_version(self):
        self.assertEqual(git_blob_sha(PREDECESSOR), PREDECESSOR_GIT_SHA)
        self.assertEqual(len(self.old_reg["scenes"]), 8)
        self.assertIn("## VIII. The Fourth Return", PREDECESSOR.read_text(encoding="utf-8"))

    def test_four_distinct_causal_movements_and_substantial_prose(self):
        headings = re.findall(r"(?m)^## ([IVX]+)\. (.+)$", self.story)
        self.assertEqual([a for a, _ in headings], ["I", "II", "III", "IV"])
        self.assertEqual([name for _,name in headings],
                         ["Half a Voice", "A Map That Lied Less", "The Empty Chair", "The Sound That Returned"])
        self.assertGreaterEqual(len(self.story.split()), 3800)
        self.assertEqual(len(self.reg["scenes"]), 4)

    def test_exclusive_fictional_jake_principal_pov(self):
        self.assertEqual(self.reg["primary_pov_ids"], ["CHAR-JAKE-KALOPER"])
        self.assertEqual({s["pov_character_id"] for s in self.reg["scenes"]}, {"CHAR-JAKE-KALOPER"})
        self.assertTrue(all(s["pov_class"] == "PRINCIPAL_CHARACTER" for s in self.reg["scenes"]))
        self.assertNotRegex(self.story, r"\b(?:Edrin|Edin|Master Oren)\b")

    def test_all_sixteen_attested_result_ids_are_accounted_for_without_full_coverage_claim(self):
        before = {event for scene in self.old_reg["scenes"] for event in scene["source_event_ids"]}
        exposed = {event for scene in self.reg["scenes"] for event in scene["source_event_ids"]}
        background = set(self.reg["background_unforegrounded_event_ids"])
        self.assertEqual(len(before), 16)
        self.assertEqual(exposed | background, before)
        self.assertFalse(exposed & background)
        self.assertEqual(len(exposed), 11)
        self.assertEqual(len(background), 5)
        self.assertFalse(self.reg["declares_full_matchup_dramatization"])
        self.assertIn("Not all sixteen results are dramatized", self.text)

    def test_period_order_and_knowledge_limits(self):
        groups = []
        for scene in self.reg["scenes"]:
            groups.append([int(re.search(r"-P(\d+)-", event).group(1))
                           for event in scene["source_event_ids"]])
        self.assertEqual(groups, [[4, 5], [8, 9], [10, 11, 12], [13, 14, 15, 16]])
        self.assertNotRegex(self.story, r"\b202[4-9]\b")
        self.assertNotRegex(self.story, r"\b(?:championship|champion's Belt)\b")

    def test_narrative_causality_and_clear_fiction_boundary(self):
        for anchor in ["the bell", "map", "the cart", "keeper", "correction"]:
            self.assertIn(anchor, self.story.lower())
        self.assertIn("NONCANON", self.text)
        self.assertIn("invented proposed staging", self.text)
        self.assertIn("not approved Atlas locations", self.text)
        self.assertIn("no opponent-owner names", self.text.lower())

    def test_release_fails_closed(self):
        self.assertEqual(self.reg["status"], "DRAFT_NONCANON_REVIEW_HOLD")
        self.assertEqual(self.reg["historical_venue"], "PROPOSED_UNAPPROVED")
        self.assertFalse(self.reg["independent_editorial_acceptance"])
        self.assertFalse(self.reg["independent_umpire_acceptance"])
        self.assertFalse(self.reg["founder_canon_promotion"])
        self.assertFalse(self.reg["canonical_merge"])
        self.assertTrue(self.reg["predecessor_retained_unchanged"])

if __name__ == "__main__":
    unittest.main()
