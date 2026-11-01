"""2016 causal Chapter LXII: source-exact seven-chapter continuation, protected-canon and continuity guards."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
SOURCES = (
    ("THE_PRICE_OF_ONE_WHEEL_CHAPTER_56_NONCANON.md", "410285ab80b12c4ea9f07840b51bbd7ddc79dfb2", 5178),
    ("THE_BLACK_MEADOW_CHAPTER_57_NONCANON.md", "d2a483e2d6b90e79b9d858525a1e19ae7657648c", 4471),
    ("THE_DISTANCE_A_NAME_COULD_TRAVEL_CHAPTER_58_NONCANON.md", "23a33fe476aa980667060bde07561861b4111959", 4564),
    ("THE_PLACE_LEFT_OPEN_CHAPTER_59_NONCANON.md", "9eb451c84168e452971d29d82a981", 5051),
    ("THE_TRACK_ABOVE_THE_WATER_CHAPTER_60_NONCANON.md", "46cf50294a7e34afe465a5d738e2d66bea48edbe", 5277),
    ("THE_MEASURE_OF_A_SHORE_CHAPTER_61_NONCANON.md", "ddccc87b4a7a0a381d567e700adec17f821d57f4", 5665),
    ("THE_FRAME_ABOVE_THE_ASH_CHAPTER_62_NONCANON.md", "56e058db1178899d476b9487c99c54364199af2f", 5094),
)
READER = "READING_COPY_CAUSAL_CHAPTERS_56_62_NONCANON.md"
READER_SHA = "667db1e40dae2cededb446026e785ef40000c64c"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_56_61_NONCANON.md"
PREVIOUS_SHA = "bf4b36516beb945c4df419829816b8c1ced297f4"
FIFTY_FIVE = "READING_COPY_CAUSAL_CHAPTERS_01_55_NONCANON.md"
FIFTY_FIVE_SHA = "a21bbcbc7268e6523378097aa60d62e1c85bed35"
QA = "CHAPTER_62_SOURCE_EDITORIAL_QA_RECEIPT.md"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}


def blob_sha(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()


class ChapterSixtyTwo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / SOURCES[-1][0]).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.qa = (BASE / QA).read_text()
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_all_source_blob_pins(self):
        for filename, sha, _ in SOURCES:
            with self.subTest(filename=filename):
                self.assertEqual(blob_sha(BASE / filename), sha)

    def test_02_reader_blob_pin(self):
        self.assertEqual(blob_sha(BASE / READER), READER_SHA)

    def test_03_exact_source_delimiters_and_contents(self):
        for filename, sha, _ in SOURCES:
            with self.subTest(filename=filename):
                start = f"<!-- BEGIN 2016_CAUSAL {filename} | git_blob {sha} -->"
                end = f"<!-- END 2016_CAUSAL {filename} -->"
                self.assertEqual(self.reader.count(start), 1)
                self.assertEqual(self.reader.count(end), 1)
                self.assertEqual(
                    self.reader.split(start, 1)[1].split(end, 1)[0].strip(),
                    (BASE / filename).read_text().strip(),
                )

    def test_04_exact_seven_chapter_sections(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 7)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 7)

    def test_05_pinned_manifest(self):
        for chapter_no, (filename, sha, words) in enumerate(SOURCES, start=56):
            with self.subTest(chapter=chapter_no):
                self.assertIn(f"| {chapter_no} | {filename} | {sha} | {words} |", self.reader)

    def test_06_reader_word_count(self):
        self.assertEqual(len(self.reader.split()), 35594)

    def test_07_chapter_word_count(self):
        self.assertEqual(len(self.chapter.split()), 5094)

    def test_08_narrative_word_count(self):
        self.assertEqual(len(self.prose.split()), 4495)

    def test_09_six_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+[.]", self.chapter, re.M)), 6)

    def test_10_reader_scope_noncanon(self):
        self.assertIn("holds only Chapters LVI, LVII, LVIII, LIX, LX, LXI and LXII", self.reader)
        self.assertIn("A monolithic 62-chapter assembled reader is not claimed", self.reader)

    def test_11_previous_continuation_preserved(self):
        self.assertEqual(blob_sha(BASE / PREVIOUS), PREVIOUS_SHA)

    def test_12_prior_55_master_preserved(self):
        self.assertEqual(blob_sha(BASE / FIFTY_FIVE), FIFTY_FIVE_SHA)

    def test_13_no_retired_viewpoint(self):
        self.assertNotRegex(self.prose, r"\b(?:Edrin|Edin|Oren)\b")

    def test_14_no_espn_invented_outcomes(self):
        self.assertNotRegex(self.prose, r"\b(?:ESPN|Flaim|touchdown|quarterback|Week [0-9]+)\b")

    def test_15_single_proposed_registered_pov(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertIn("not as new interior POV carriers", self.chapter)

    def test_16_historical_binding_unverified(self):
        self.assertIn("Historical 2016 owner-to-team authentication is absent", self.chapter)
        self.assertIn("62 consecutive proposed Jake-limited historical chapters", self.qa)

    def test_17_seven_unlocated_remain_unlocated(self):
        self.assertIn("Seven travelers remained unlocated", self.prose)
        self.assertIn("No missing person has been located", self.qa)

    def test_18_reed_worker_survives_and_lost_frame_stays_lost(self):
        self.assertIn("Nothing remained of the wicker frame", self.prose)
        self.assertIn("The reed worker survives", self.qa)

    def test_19_reed_worker_new_frame_smaller(self):
        self.assertIn("That will carry less than half what the other one carried", self.prose)
        self.assertIn("We've made me one small frame", self.prose)

    def test_20_two_stage_wind_test(self):
        self.assertIn("The far corner rose", self.prose)
        self.assertIn("The corner struck its stop-block and held", self.prose)

    def test_21_merics_count_is_verified(self):
        self.assertIn("You were right about the rotten base", self.prose)
        self.assertIn("The count was work", self.prose)

    def test_22_one_coin_wage_separate_from_pole_damage(self):
        self.assertIn("That is for the count. The pole is still broken", self.prose)
        self.assertIn("The split pole remains mine", self.prose)

    def test_23_esi_ledger_reduced_but_not_closed(self):
        self.assertIn("one unit as paid", self.prose)
        self.assertIn("The remaining marks stood plainly beside it", self.prose)
        self.assertIn("not cleared", self.qa)

    def test_24_no_invented_reed_rights_or_law(self):
        self.assertIn("I won't make you a deed for what I've only walked", self.prose)
        self.assertIn("No charitable miracle, landed ownership", self.qa)

    def test_25_unverified_map_arrow_removed(self):
        self.assertIn("That isn't my hand", self.prose)
        self.assertIn("The added arrow was gone", self.prose)

    def test_26_injuries_and_hessa_message_gap_preserved(self):
        self.assertIn("Neris could use only one arm freely", self.prose)
        self.assertIn("Hessa was away; Ilyen had not reached her", self.prose)

    def test_27_six_owner_cart_collar_not_resolved(self):
        self.assertIn("six-owner cart's missing iron collar", self.prose)
        self.assertIn("Tovin had not been forgiven", self.prose)

    def test_28_noncanonical_atlas_and_review_boundary(self):
        self.assertIn("not ESPN/Flaim events, approved Atlas geography", self.chapter)
        self.assertIn("candidate fiction pending Atlas review", self.qa)

    def test_29_archived_historical_league_facts_unchanged(self):
        archive = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(blob_sha(archive), ARCHIVE_SHA)

    def test_30_protected_hard_canon_unmodified(self):
        for filename, sha in PROTECTED.items():
            with self.subTest(filename=filename):
                self.assertEqual(blob_sha(ROOT / filename), sha)

    def test_31_self_review_does_not_impersonate_independent(self):
        for phrase in ("NOT INDEPENDENT REVIEW", "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            self.assertIn(phrase, self.qa)

    def test_32_author_editorial_risks_explicit(self):
        for topic in ("Economics:", "Craft and meteorology:", "Atlas/land:", "Source authenticity:"):
            self.assertIn(topic, self.qa)

    def test_33_previous_source_repair_not_edited(self):
        previous_chapter = BASE / "THE_MEASURE_OF_A_SHORE_CHAPTER_61_NONCANON.md"
        self.assertEqual(blob_sha(previous_chapter), "ddccc87b4a7a0a381d567e700adec17f821d57f4")

    def test_34_scene_not_automatic_week_chapter(self):
        self.assertIn("No 2016 league scoring event enters the foreground", self.chapter)

    def test_35_no_unauthorized_sela_or_missing_rescue(self):
        self.assertNotRegex(self.prose, r"\bSela\b")
        self.assertIn("seven remain unlocated", self.qa.lower())


if __name__ == "__main__":
    unittest.main()
