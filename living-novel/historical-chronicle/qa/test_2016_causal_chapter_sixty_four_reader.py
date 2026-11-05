"""2016 historical causal Chapter LXIV: exact nine-chapter reader, continuity, noncanon gates."""
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
    ("THE_HAND_BEHIND_THE_WALL_CHAPTER_64_NONCANON.md", "3edb40570163f6d1144c49f77408075ba2482418", 5640),
)
READER = "READING_COPY_CAUSAL_CHAPTERS_56_64_NONCANON.md"
READER_SHA = "35876dc97fac32ca33984ead06f618dedc5cbedf"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_56_63_NONCANON.md"
PREVIOUS_SHA = "c0555de060eae2c1eafc3b98f97683b9d65076cc"
FIFTY_FIVE = "READING_COPY_CAUSAL_CHAPTERS_01_55_NONCANON.md"
FIFTY_FIVE_SHA = "a21bbcbc7268e6523378097aa60d62e1c85bed35"
QA = "CHAPTER_64_SOURCE_EDITORIAL_QA_RECEIPT.md"
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


class ChapterSixtyFour(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / SOURCES[-1][0]).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.qa = (BASE / QA).read_text()
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_all_nine_source_blob_pins(self):
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

    def test_04_nine_sections(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 9)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 9)

    def test_05_source_manifest_pin_rows(self):
        for number, (filename, sha, words) in enumerate(SOURCES, 56):
            self.assertIn(f"| {number} | {filename} | {sha} | {words} |", self.reader)

    def test_06_chapter_whitespace_words(self):
        self.assertEqual(len(self.chapter.split()), 5640)

    def test_07_prose_whitespace_words(self):
        self.assertEqual(len(self.prose.split()), 5112)

    def test_08_reader_whitespace_words(self):
        self.assertEqual(len(self.reader.split()), 46971)

    def test_09_six_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+[.]", self.chapter, re.M)), 6)

    def test_10_reader_is_continuation_not_canon_monolith(self):
        self.assertIn("A monolithic 64-chapter assembled reader is not claimed", self.reader)
        self.assertIn("DRAFT / INDEPENDENT EDITORIAL HOLD", self.reader)

    def test_11_previous_eight_reader_untouched(self):
        self.assertEqual(blob_sha(BASE / PREVIOUS), PREVIOUS_SHA)

    def test_12_first_55_reader_untouched(self):
        self.assertEqual(blob_sha(BASE / FIFTY_FIVE), FIFTY_FIVE_SHA)

    def test_13_archive_evidence_untouched(self):
        p = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(blob_sha(p), ARCHIVE_SHA)

    def test_14_protected_2026_manuscript_untouched(self):
        for p, sha in PROTECTED.items():
            with self.subTest(path=p):
                self.assertEqual(blob_sha(ROOT / p), sha)

    def test_15_authorized_single_fictional_owner_pov(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("64 consecutive Jake-limited historical chapters", self.qa)

    def test_16_no_retired_or_archival_narrator(self):
        self.assertNotRegex(self.prose, r"\b(?:Edrin|Edin|Oren)\b")

    def test_17_no_unverified_real_matchup_or_score(self):
        self.assertNotRegex(self.prose, r"\b(?:ESPN|Flaim|quarterback|touchdown|Week [0-9]+)\b")

    def test_18_nella_prior_false_performance_preserved(self):
        self.assertIn("Nella returning part of the payment", self.prose)
        self.assertIn("I took it. I returned some. Not all", self.prose)

    def test_19_nella_refused_second_performance(self):
        self.assertIn("Nella refuse a second performance at the bowls", self.prose)

    def test_20_nonhistorical_inner_play_invented(self):
        self.assertIn("Nobody. I made him up", self.prose)
        self.assertIn("The collector counted doors where there were none", self.prose)

    def test_21_no_open_flame_near_recent_burn(self):
        self.assertIn("Nella did not use a lantern", self.prose)
        self.assertIn("not put a new flame under stretched cloth", self.prose)

    def test_22_merics_yard_permission_and_clear_path(self):
        self.assertIn("I haven't agreed to lend you a yard", self.prose)
        self.assertIn("Keep my path clear", self.prose)

    def test_23_ina_owns_borrowed_fabric(self):
        self.assertIn("If you cut this", self.prose)
        self.assertIn("Ina did not require a report on laughter", self.prose)

    def test_24_material_stage_mechanism_causal_failure(self):
        self.assertIn("one side of the pale fabric folded inward", self.prose)
        self.assertIn("the new drilled hole had split", self.prose)

    def test_25_critic_raises_real_past_harm(self):
        self.assertIn("Last time you said people were dead", self.prose)
        self.assertIn("You did not ask us to believe the deaths either", self.prose)

    def test_26_nella_continues_visible_unhidden(self):
        self.assertIn("You can watch the rest being made", self.prose)
        self.assertIn("the audience could see every movement of her hands", self.prose)

    def test_27_comedy_not_a_state_institution(self):
        self.assertIn("there are more doors in this land", self.prose)
        self.assertIn("not an actual institution", self.chapter)

    def test_28_no_magical_absolution(self):
        self.assertIn("The woman walked away without offering forgiveness", self.prose)
        self.assertIn("mixed audience response", self.qa)

    def test_29_audience_leaving_undercuts_easy_victory(self):
        self.assertIn("A few spectators left", self.prose)
        self.assertIn("Nobody told him to stay", self.prose)

    def test_30_fictional_jake_does_not_erase_false_testimony(self):
        self.assertIn("four coins", self.prose)
        self.assertIn("original lie", self.prose)

    def test_31_missing_seven_and_hessa_not_resolved(self):
        self.assertIn("the seven travelers unlocated", self.prose)
        self.assertIn("Hessa remained away and unreachable", self.prose)

    def test_32_warning_is_not_a_verified_route(self):
        self.assertIn("Don't tell anyone it finds Hessa", self.prose)
        self.assertIn("I won't", self.prose)

    def test_33_prior_resources_not_reset(self):
        self.assertIn("the six-owner cart disabled", self.prose)
        self.assertIn("Neris and Dovan injured", self.prose)

    def test_34_poorly_made_stage_still_costs_a_peg(self):
        self.assertIn("You can cut me another tomorrow", self.prose)
        self.assertIn("I won't pay you for today's performance", self.prose)

    def test_35_linen_is_returned_to_ina(self):
        self.assertIn("Wash it here", self.prose)
        self.assertIn("hung the remnant", self.prose)

    def test_36_no_2016_owner_account_auth_claim(self):
        self.assertIn("still user-attested", self.qa)
        self.assertIn("not independently authenticated", self.qa)

    def test_37_author_side_not_independent_review(self):
        for phrase in ("NOT INDEPENDENT REVIEW", "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            self.assertIn(phrase, self.qa)

    def test_38_no_canon_promotion_embedded_in_chapter(self):
        self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD", self.chapter)
        self.assertIn("Protected 2026 Prologue and Chapters I–III remain untouched", self.chapter)

    def test_39_previous_chapter_63_blob_guard(self):
        self.assertEqual(blob_sha(BASE / SOURCES[-2][0]), SOURCES[-2][1])

    def test_40_old_eight_chapter_source_sections_exact_prefix(self):
        old = (BASE / PREVIOUS).read_text()
        delim = "\n## Chapter LVI —"
        self.assertEqual(
            self.reader.split(delim, 1)[1].split("\n\n## Chapter LXIV", 1)[0].strip(),
            old.split(delim, 1)[1].strip(),
        )


if __name__ == "__main__":
    unittest.main()
