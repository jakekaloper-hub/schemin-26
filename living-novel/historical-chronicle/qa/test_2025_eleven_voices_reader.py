"""Eleven distinct 2025 historical character-POV manuscripts: noncanon source integrity.

Tests protect manuscript and source boundaries. They do NOT authenticate 2025
human owners, approve period geography, prove literary quality, or replace an
independent Authors Council/Umpire approval.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2025/causal-novel"
EVIDENCE = ROOT / "living-novel/historical-chronicle/evidence/2025_FLAIM_TEAM_SLOT_AND_PODIUM_READBACK_2026-11-01_REVIEW_ONLY.md"
READER = BASE / "READING_COPY_2025_ELEVEN_VOICES_NONCANON.md"
PREVIOUS = BASE / "READING_COPY_2025_TEN_VOICES_NONCANON.md"
PREVIOUS_SHA = "ddb10bd2e028410a3240f09fcfcc1a00bd04c314"
CHAPTER = BASE / "THE_ROAD_NO_BANNER_COULD_OWN_WILSON_2025_NONCANON.md"
CHAPTER_SHA = "b737814a6049175ad15ea354cd6e2f44e449f75b"
OLD_2016 = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel/READING_COPY_CAUSAL_CHAPTERS_01_72_NONCANON.md"
OLD_2016_SHA = "8f1dda21ac4962143ba3291cef4d60769197d62f"
PREVIOUS_SOURCE_WORDS = 48669
NEW_SOURCE_WORDS = 5594
TOTAL_SOURCE_WORDS = 54263
WRAPPER = re.compile(r"<!-- BEGIN 2025_VOICE ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n([\s\S]*?)\n\n<!-- END 2025_VOICE ([^\n]+) -->")
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
OTHER_SOURCE = ROOT / "living-novel/production/historical-saga/R53/HISTORICAL_2025_OBIWAN_NONCANON_PILOT.md"


def gitblob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def source_path(name):
    return OTHER_SOURCE if name == OTHER_SOURCE.name else BASE / name


class ElevenVoiceReadingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader = READER.read_text(encoding="utf-8")
        cls.previous = PREVIOUS.read_text(encoding="utf-8")
        cls.chapter = CHAPTER.read_text(encoding="utf-8")
        cls.scene = cls.chapter.split("\n---\n\n### Source, causality, and continuity handoff")[0]
        cls.parts = list(WRAPPER.finditer(cls.reader))
        cls.old_parts = list(WRAPPER.finditer(cls.previous))
        cls.evidence = EVIDENCE.read_text(encoding="utf-8")

    def test_01_eleven_source_wrappers(self):
        self.assertEqual(len(self.parts), 11)

    def test_02_prior_ten_source_reader_immutable(self):
        self.assertEqual(gitblob(PREVIOUS), PREVIOUS_SHA)

    def test_03_source_body_exact_previous_ten(self):
        self.assertEqual(len(self.old_parts), 10)
        for i in range(10):
            with self.subTest(i=i):
                self.assertEqual(self.parts[i].group(0), self.old_parts[i].group(0))

    def test_04_new_chapter_blob_immutable(self):
        self.assertEqual(gitblob(CHAPTER), CHAPTER_SHA)

    def test_05_new_source_exact_embedding(self):
        last = self.parts[10]
        self.assertEqual(last.group(1), CHAPTER.name)
        self.assertEqual(last.group(2), CHAPTER_SHA)
        self.assertEqual(last.group(3), self.chapter.rstrip("\n"))
        self.assertEqual(last.group(4), CHAPTER.name)

    def test_06_prior_ten_sources_source_exact(self):
        for p in self.parts[:10]:
            with self.subTest(name=p.group(1)):
                path = source_path(p.group(1))
                self.assertEqual(gitblob(path), p.group(2))
                self.assertEqual(path.read_text(encoding="utf-8").rstrip("\n"), p.group(3))

    def test_07_eleven_manifest_rows(self):
        manifest = self.reader.split("## Source-exact manifest\n", 1)[1].split("\n---\n", 1)[0]
        rows = re.findall(r"^\| (\d+) \|", manifest, re.M)
        self.assertEqual(rows, [str(i) for i in range(1, 12)])

    def test_08_source_words(self):
        self.assertEqual(len(self.chapter.split()), NEW_SOURCE_WORDS)

    def test_09_total_original_source_words(self):
        self.assertEqual(
            sum(len(source_path(p.group(1)).read_text(encoding="utf-8").split()) for p in self.parts),
            TOTAL_SOURCE_WORDS
        )
        self.assertIn("54263", self.reader)

    def test_10_reader_word_count_includes_wrappers(self):
        self.assertGreater(len(self.reader.split()), TOTAL_SOURCE_WORDS)

    def test_11_eleven_distinct_characters(self):
        owner_ids = re.findall(r"^\| \d+ \| [^|]+ / (CHAR-[A-Z-]+) \|", self.reader, re.M)
        self.assertEqual(len(owner_ids), 11)
        self.assertEqual(len(set(owner_ids)), 11)
        registry = (ROOT / "canon/characters/CHARACTER_REGISTRY.yaml").read_text(encoding="utf-8")
        for owner in owner_ids:
            self.assertIn("id: "+owner, registry)

    def test_12_eleven_part_order_and_termination(self):
        self.assertIn("## Part 10 — Jordan", self.reader)
        self.assertIn("## Part 11 — Wilson", self.reader)
        self.assertLess(self.reader.index("## Part 10 — Jordan"), self.reader.index("## Part 11 — Wilson"))
        self.assertTrue(self.reader.rstrip().endswith("<!-- END_2025_ELEVEN_VOICES_NONCANON -->"))

    def test_13_new_chapter_substantial(self):
        self.assertGreaterEqual(len(self.chapter.split()), 5000)

    def test_14_six_movement_story(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\. ", self.scene, re.M)), 6)

    def test_15_wilson_sole_interiority(self):
        self.assertIn("Principal and sole interior viewpoint: Wilson Look", self.chapter)
        self.assertIn("Principal and sole interior viewpoint Wilson Look", self.chapter)

    def test_16_single_body_four_legged_not_rider(self):
        for cue in ("ONE integrated body", "four-legged", "not a rider and mount", "forefeet", "rear feet"):
            self.assertIn(cue, self.chapter)

    def test_17_competition_grounded(self):
        self.assertIn("| 5 | Baker Moore Purdy | 9–5 | 5 | eliminated |", self.evidence)
        for cue in ("team slot 5", "Baker Moore Purdy", "9–5", "finalRank 5", "eliminated"):
            self.assertIn(cue, self.chapter)

    def test_18_historical_manager_not_authenticated(self):
        self.assertIn("does not authenticate Wilson", self.chapter)
        self.assertIn("PROVISIONAL FICTIONAL ASSOCIATION", self.chapter)
        self.assertIn("not eleven independently verified historical human owner accounts", self.reader)

    def test_19_no_borrowed_institutional_pov(self):
        self.assertIsNone(re.search(r"\b(?:Edrin|Edin|Oren)\b", self.scene))

    def test_20_period_visual_hold_explicit(self):
        self.assertIn("PERIOD CHARACTER AND ATLAS HOLD", self.chapter)
        self.assertIn("2025 is a literary proposal requiring period review", self.chapter)

    def test_21_no_2026_score_backfill(self):
        self.assertIn("no future 2026 results", self.chapter)
        self.assertIn("no invented league result", self.chapter.lower())

    def test_22_failed_test_preserved(self):
        self.assertIn("The first test was made without a wagon and failed", self.chapter)
        self.assertIn("The near edge sank", self.chapter)

    def test_23_one_wagon_not_general_road_open(self):
        self.assertIn("one inspected wagon", self.chapter)
        self.assertIn("The road was not restored", self.chapter)
        self.assertIn("not declared generally open", self.chapter)

    def test_24_jordan_debt_settled_without_false_attribution(self):
        self.assertIn("Jordan carried the money straight", self.chapter)
        self.assertIn("full payment for those particular hours", self.chapter)
        self.assertIn("Jordan had owed it; Jordan had discharged it", self.chapter)

    def test_25_watch_wage_claim_separate(self):
        self.assertIn("the watch's separate wage obligation still awaited", self.chapter)

    def test_26_no_toll_legality_invented(self):
        self.assertIn("no authenticated title", self.chapter)
        self.assertIn("no new legal authority", self.chapter)

    def test_27_three_figures_still_unknown(self):
        self.assertIn("neither their identities nor their intentions had been established", self.chapter)

    def test_28_noncanon_fiction_and_release_gates(self):
        for cue in ("UNAPPROVED SECONDARY-WORLD FICTION", "INDEPENDENT", "FOUNDER-ONLY", "NO MERGE", "NO PUBLICATION"):
            self.assertIn(cue, self.chapter)

    def test_29_separate_2016_72_chapter_reader_immutable(self):
        self.assertEqual(gitblob(OLD_2016), OLD_2016_SHA)

    def test_30_protected_2026_opening_immutable(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(gitblob(ROOT / path), sha)


if __name__ == "__main__":
    unittest.main()
