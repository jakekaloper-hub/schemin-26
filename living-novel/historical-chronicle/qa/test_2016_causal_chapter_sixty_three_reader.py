"""2016 causal Chapter LXIII: source-exact 8-chapter continuation and canon/continuity protections."""
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
    ("THE_PLACE_LEFT_OPEN_CHAPTER_59_NONCANON.md", "9eb451c84168e452971d29d82f7e7d9f14972dfc", 5051),
    ("THE_TRACK_ABOVE_THE_WATER_CHAPTER_60_NONCANON.md", "46cf50294a7e34afe465a5d738e2d66bea48edbe", 5277),
    ("THE_MEASURE_OF_A_SHORE_CHAPTER_61_NONCANON.md", "ddccc87b4a7a0a381d567e700adec17f821d57f4", 5665),
    ("THE_FRAME_ABOVE_THE_ASH_CHAPTER_62_NONCANON.md", "56e058db1178899d476b9487c99c54364199af2f", 5094),
    ("WHERE_THE_RAIN_WENT_CHAPTER_63_NONCANON.md", "5406813aa81203ccb75399b33f57c4a3bdb0d355", 5679),
)
READER = "READING_COPY_CAUSAL_CHAPTERS_56_63_NONCANON.md"
READER_SHA = "c0555de060eae2c1eafc3b98f97683b9d65076cc"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_56_62_NONCANON.md"
PREVIOUS_SHA = "667db1e40dae2cededb446026e785ef40000c64c"
FIFTY_FIVE = "READING_COPY_CAUSAL_CHAPTERS_01_55_NONCANON.md"
FIFTY_FIVE_SHA = "a21bbcbc7268e6523378097aa60d62e1c85bed35"
QA = "CHAPTER_63_SOURCE_EDITORIAL_QA_RECEIPT.md"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def blob_sha(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\\x00" + raw).hexdigest()

class ChapterSixtyThree(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / SOURCES[-1][0]).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.qa = (BASE / QA).read_text()
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\\n---\\n", 1)[0]

    def test_01_all_eight_source_blob_pins(self):
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
                self.assertEqual(self.reader.split(start, 1)[1].split(end, 1)[0].strip(), (BASE / filename).read_text().strip())

    def test_04_eight_sections(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 8)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 8)

    def test_05_pinned_source_manifest(self):
        for number, (filename, sha, words) in enumerate(SOURCES, 56):
            with self.subTest(number=number):
                self.assertIn(f"| {number} | {filename} | {sha} | {words} |", self.reader)

    def test_06_reader_whitespace_word_count(self):
        self.assertEqual(len(self.reader.split()), 41300)

    def test_07_chapter_whitespace_word_count(self):
        self.assertEqual(len(self.chapter.split()), 5679)

    def test_08_narrative_whitespace_word_count(self):
        self.assertEqual(len(self.prose.split()), 5129)

    def test_09_six_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+[.]", self.chapter, re.M)), 6)

    def test_10_no_monolithic_canon_claim(self):
        self.assertIn("A monolithic 63-chapter assembled reader is not claimed", self.reader)
        self.assertIn("DRAFT / INDEPENDENT EDITORIAL HOLD", self.reader)

    def test_11_previous_continuation_preserved(self):
        self.assertEqual(blob_sha(BASE / PREVIOUS), PREVIOUS_SHA)

    def test_12_first_55_reader_preserved(self):
        self.assertEqual(blob_sha(BASE / FIFTY_FIVE), FIFTY_FIVE_SHA)

    def test_13_retired_or_institutional_povs_excluded(self):
        self.assertNotRegex(self.prose, r"\\b(?:Edrin|Edin|Oren)\\b")

    def test_14_no_invented_league_match_result(self):
        self.assertNotRegex(self.prose, r"\\b(?:ESPN|Flaim|quarterback|touchdown|Week [0-9]+)\\b")

    def test_15_only_proposed_registered_interior_pov(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("63 consecutive Jake-limited chapters", self.qa)

    def test_16_not_a_water_sanitation_instruction(self):
        self.assertIn("not Atlas-approved settlements", self.chapter)
        self.assertIn("water-quality certification", self.qa)

    def test_17_first_rain_after_fire(self):
        self.assertIn("Then the rain came", self.prose)
        self.assertIn("the burned meadow", self.prose)

    def test_18_trough_visibly_ash_affected(self):
        self.assertIn("the color of weak ink", self.prose)
        self.assertIn("There's ash in it", self.prose)

    def test_19_fara_has_agency_not_public_office(self):
        self.assertIn("Fara stood beside the dark basin", self.prose)
        self.assertIn("The gesture had no force of law", self.prose)

    def test_20_no_unearned_potable_certification(self):
        self.assertIn("I would not promise what I have not tested", self.prose)
        self.assertIn("no assertion that source or catch is safe", self.qa)

    def test_21_esi_owns_limited_stored_water(self):
        self.assertIn("It isn't a gift from the sky", self.prose)
        self.assertIn("It has my name on it until I choose", self.prose)

    def test_22_esi_water_not_unpaid_wage(self):
        self.assertIn("I didn't send you there for a coin", self.prose)
        self.assertIn("Esi's remaining shelter debt", self.qa)

    def test_23_aven_neris_task_does_not_reconcile(self):
        self.assertIn("Aven remained the man who had returned alone", self.prose)
        self.assertIn("Neris had set a boundary Aven obeyed", self.prose)

    def test_24_hessa_still_unreached(self):
        self.assertIn("Hessa was still beyond their reach", self.prose)
        self.assertIn("To where?", self.prose)

    def test_25_seven_missing_unlocated(self):
        self.assertIn("They remained missing", self.prose)
        self.assertIn("Seven fictional travelers unlocated", self.qa)

    def test_26_map_does_not_claim_unseen_route(self):
        self.assertIn("each line was shorter", self.prose.lower())
        self.assertIn("I won't ask them to swear that a road connects", self.prose)

    def test_27_reed_workers_new_frame_not_destroyed(self):
        self.assertIn("The frame stood", self.prose)
        self.assertIn("reeds are damp", self.qa)

    def test_28_one_credit_not_debt_cleared(self):
        self.assertIn("shelter tally was one mark smaller", self.prose)
        self.assertIn("the rest still owes", self.qa)

    def test_29_water_source_uncertainty_carries(self):
        self.assertIn("The next rain might send another load of ash", self.prose)
        self.assertIn("runoff patterns", self.qa)

    def test_30_prior_2016_archive_unchanged(self):
        archive = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(blob_sha(archive), ARCHIVE_SHA)

    def test_31_protected_main_manuscript_not_modified(self):
        for filename, sha in PROTECTED.items():
            with self.subTest(filename=filename):
                self.assertEqual(blob_sha(ROOT / filename), sha)

    def test_32_self_review_does_not_impersonate_independent(self):
        for phrase in ("NOT INDEPENDENT REVIEW", "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            self.assertIn(phrase, self.qa)

    def test_33_previous_chapter_62_blob_guard(self):
        self.assertEqual(blob_sha(BASE / SOURCES[-2][0]), SOURCES[-2][1])

    def test_34_previous_seven_continuation_sources_are_prefix(self):
        previous = (BASE / PREVIOUS).read_text()
        anchor = "\\n\\n## Chapter LVI — The Price of One Wheel"
        self.assertEqual(self.reader.split(anchor, 1)[1].split("\\n\\n## Chapter LXIII", 1)[0].strip(), previous.split(anchor, 1)[1].strip())

    def test_35_separate_historical_owner_and_sela_hold(self):
        self.assertNotRegex(self.prose, r"\\bSela\\b")
        self.assertIn("Historical owner account authentication remains absent", self.qa)

    def test_36_no_invented_water_institution(self):
        self.assertIn("No new civic authority", self.qa)
        self.assertIn("The gesture had no force of law", self.prose)

    def test_37_consequence_not_reset(self):
        self.assertIn("The rain was over. Its route through the settlement remained", self.prose)

    def test_38_archival_source_fact_deliberately_offpage(self):
        self.assertIn("No 2016 ESPN/Flaim matchup or result", self.chapter)

    def test_39_independent_atlas_and_umpire_holds(self):
        self.assertIn("Atlas review required", self.qa)
        self.assertIn("Independent Umpire:", self.qa)

    def test_40_no_premature_prose_promotion(self):
        self.assertIn("NO MERGE, NO CANON PROMOTION, NO PUBLICATION", self.chapter)

if __name__ == "__main__":
    unittest.main()
