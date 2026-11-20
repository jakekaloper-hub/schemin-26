"""Chapter LXVIII: source-exact 13-chapter continuation, history, POV and derivative gates."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_LINE_ON_THE_GATE_CHAPTER_68_NONCANON.md"
CHAPTER_SHA = "f57ab546164fd08b0c7dab946a651656e07b2e99"
READER = "READING_COPY_CAUSAL_CHAPTERS_56_68_NONCANON.md"
READER_SHA = "e3e4edca68f02a81c7fc982f7a9b36f1b264aaf6"
PREVIOUS_READER = "READING_COPY_CAUSAL_CHAPTERS_56_67_NONCANON.md"
PREVIOUS_READER_SHA = "b245e52e66807de2c44ede6aa863728387e18459"
FIRST_FIFTY_FIVE = "READING_COPY_CAUSAL_CHAPTERS_01_55_NONCANON.md"
FIRST_FIFTY_FIVE_SHA = "a21bbcbc7268e6523378097aa60d62e1c85bed35"
QA = "CHAPTER_68_SOURCE_EDITORIAL_QA_RECEIPT.md"
HISTORY = "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
HISTORY_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def blob_sha(p):
    raw = p.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()

class ChapterSixtyEight(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text(encoding="utf-8")
        cls.reader = (BASE / READER).read_text(encoding="utf-8")
        cls.previous = (BASE / PREVIOUS_READER).read_text(encoding="utf-8")
        cls.qa = (BASE / QA).read_text(encoding="utf-8")
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_new_chapter_blob(self):
        self.assertEqual(blob_sha(BASE / CHAPTER), CHAPTER_SHA)

    def test_02_new_assembled_reader_blob(self):
        self.assertEqual(blob_sha(BASE / READER), READER_SHA)

    def test_03_previous_reader_blob_preserved(self):
        self.assertEqual(blob_sha(BASE / PREVIOUS_READER), PREVIOUS_READER_SHA)

    def test_04_prior_fifty_five_reader_preserved(self):
        self.assertEqual(blob_sha(BASE / FIRST_FIFTY_FIVE), FIRST_FIFTY_FIVE_SHA)

    def test_05_2016_archive_retained(self):
        self.assertEqual(blob_sha(ROOT / HISTORY), HISTORY_SHA)

    def test_06_protected_prologue_and_chapters_retained(self):
        for file, sha in PROTECTED.items():
            with self.subTest(path=file):
                self.assertEqual(blob_sha(ROOT / file), sha)

    def test_07_frozen_prior_reader_embedded_source_exact(self):
        prefix = self.previous[self.previous.index("## Chapter LVI"):]
        current = self.reader[self.reader.index("## Chapter LVI"):self.reader.index("\n## Chapter LXVIII")]
        self.assertEqual(current.strip(), prefix.strip())

    def test_08_new_wrapper_matches_source_exact(self):
        begin = "<!-- BEGIN 2016_CAUSAL " + CHAPTER + " | git_blob " + CHAPTER_SHA + " -->"
        end = "<!-- END 2016_CAUSAL " + CHAPTER + " -->"
        self.assertEqual(self.reader.count(begin), 1)
        self.assertEqual(self.reader.count(end), 1)
        self.assertEqual(self.reader.split(begin, 1)[1].split(end, 1)[0].strip(), self.chapter.strip())

    def test_09_thirteen_wrappers_only(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 13)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 13)

    def test_10_reader_manifest_new_row(self):
        self.assertIn("| 68 | " + CHAPTER + " | " + CHAPTER_SHA + " | 3805 |", self.reader)

    def test_11_reader_has_thirteen_manifest_rows(self):
        self.assertEqual(len(re.findall(r"^\| (?:5[6-9]|6[0-8]) \| ", self.reader, re.M)), 13)

    def test_12_chapter_word_count(self):
        self.assertEqual(len(self.chapter.split()), 3805)

    def test_13_prose_word_count(self):
        self.assertEqual(len(self.prose.split()), 3389)

    def test_14_reader_word_count(self):
        self.assertEqual(len(self.reader.split()), 65602)

    def test_15_six_narrative_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\.", self.chapter, re.M)), 6)

    def test_16_not_a_canon_release(self):
        self.assertIn("DRAFT / NONCANON / INDEPENDENT EDITORIAL HOLD", self.chapter)
        self.assertIn("NO MERGE / CANON PROMOTION / PUBLICATION", self.qa)

    def test_17_only_proposed_jake_interior(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("68 consecutive Jake-limited historical chapters", self.qa)

    def test_18_no_retired_narrators(self):
        self.assertNotRegex(self.prose, r"\b(?:Edrin|Edin|Oren)\b")

    def test_19_no_fiction_claimed_as_score(self):
        self.assertNotRegex(self.prose, r"\b(?:ESPN|Flaim|touchdown|quarterback|Week [0-9]+)\b")

    def test_20_source_copy_is_unauthorized(self):
        self.assertIn("The mark appeared on Meric's gate before anyone admitted to making it", self.prose)

    def test_21_father_is_not_a_cart_owner_proxy(self):
        self.assertIn("its collar is still with the buyer", self.prose)
        self.assertIn("Nobody has voted to move the six-owner cart", self.prose)

    def test_22_survivor_does_not_claim_route(self):
        self.assertIn("Then I was never on this road", self.prose)
        self.assertIn("I didn't draw this fork", self.prose)

    def test_23_six_strokes_not_verified_positions(self):
        self.assertIn("I never counted six people at its end", self.prose)
        self.assertIn("Those are people", self.prose)

    def test_24_does_not_draw_replacement_route(self):
        self.assertIn("I can't make this my road", self.prose)
        self.assertIn("No. Not on this.", self.prose)

    def test_25_maker_admits_error(self):
        self.assertIn('"I did it," he said.', self.prose)
        self.assertIn("I thought if I put the pieces together", self.prose)

    def test_26_error_preserved_as_attributed_copy(self):
        self.assertIn("This copy records what was on the gate, not where anyone went", self.prose)

    def test_27_error_removed_from_gate(self):
        self.assertIn("You put them there. You take them away", self.prose)
        self.assertIn("no road anybody could follow", self.prose)

    def test_28_father_receives_only_before_separation_memory(self):
        self.assertIn("He helped me once", self.prose)
        self.assertIn("A boot. I had caught it in mud", self.prose)
        self.assertIn("I don't know what happened to him after we parted", self.prose)

    def test_29_no_search_leaves_from_fake_map(self):
        self.assertIn("The group did not depart", self.prose)

    def test_30_returned_traveler_keeps_agency(self):
        self.assertIn("Then shut it to questions", self.prose)

    def test_31_six_missing_not_solved(self):
        self.assertIn("six others were still unlocated", self.prose)
        self.assertIn("neither confirmed deaths nor a certified trail", self.prose)

    def test_32_hessa_no_verified_route_claim(self):
        self.assertIn("Hessa had a copy of an error and not a map", self.prose)

    def test_33_prior_survivor_plot_marked_conditional(self):
        self.assertIn("conditionally follows the unapproved fictional survivor-return", self.chapter)
        self.assertIn("depends entirely on the unapproved survivor return", self.qa)

    def test_34_adversarial_qa_and_umpire_hold(self):
        for phrase in ["Authors Council", "Historical Librarian", "Atlas", "independent Umpire", "structural defect"]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.qa)

    def test_35_not_monolithic_claim(self):
        self.assertIn("A monolithic 68-chapter assembled reader is not claimed", self.reader)

if __name__ == "__main__":
    unittest.main()
