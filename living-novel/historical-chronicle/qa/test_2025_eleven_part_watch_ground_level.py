"""Regression proof for a NONCANON 2025 eleven-part developmental reading.

Tests prove text/source identity and limited negative safeguards. They are
not historical-owner authentication, independent literary/Umpire approval
or permission to promote canon.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2025/causal-novel"
CHAPTER = BASE / "THE_WATCH_AT_GROUND_LEVEL_KEVIN_JORDAN_2025_DEVELOPMENTAL_NONCANON.md"
READER = BASE / "READING_COPY_2025_TWELVE_VOICES_ELEVEN_PARTS_WATCH_GROUND_LEVEL_NONCANON.md"
OLD = BASE / "READING_COPY_2025_TWELVE_VOICES_TWELVE_PARTS_TRIPLE_INTEGRATION_NONCANON.md"
KEVIN = BASE / "THE_WATCH_THAT_WENT_DARK_KEVIN_2025_NONCANON.md"
JORDAN = BASE / "THE_BELL_BELOW_THE_FLOOR_JORDAN_2025_NONCANON.md"
WILSON = BASE / "THE_ROAD_NO_BANNER_COULD_OWN_WILSON_2025_NONCANON.md"
READER_2016 = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel/READING_COPY_CAUSAL_CHAPTERS_01_72_NONCANON.md"

CHAPTER_BLOB = "e822af02abd44ecb0ec8a4d739a717f79bbc170b"
READER_BLOB = "3eb4a3c424ba243dc0cb10c81dcf82a7695c6a7e"
OLD_BLOB = "0510c40d3e33d1dde6720e8196ca87f23afd5bbf"
KEVIN_BLOB = "c4e75354fba5bc8d21719a9bcbc0661197467b2f"
JORDAN_BLOB = "e65886fe766c3ba13f07e0cc63d4ebc13560629e"
WILSON_BLOB = "b737814a6049175ad15ea354cd6e2f44e449f75b"
READER_2016_BLOB = "8f1dda21ac4962143ba3291cef4d60769197d62f"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
WRAP = re.compile(
    r"<!-- BEGIN 2025_VOICE ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n"
    r"([\s\S]*?)\n\n<!-- END 2025_VOICE ([^\n]+) -->"
)
ROW = re.compile(
    r"^\| (\d+) \| ([^|]+) \| " + chr(96) +
    r"([^" + chr(96) + r"]+)" + chr(96) +
    r" \| " + chr(96) + r"([0-9a-f]{40})" + chr(96) +
    r" \| (\d+) \|$", re.M
)


def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


class GroundLevelDevelopmentalIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = CHAPTER.read_text(encoding="utf-8")
        cls.reader = READER.read_text(encoding="utf-8")
        cls.old = OLD.read_text(encoding="utf-8")
        cls.story = cls.chapter.split("### Production/source boundary", 1)[0]
        cls.original_wrappers = list(WRAP.finditer(cls.old))
        cls.wrappers = list(WRAP.finditer(cls.reader))
        manifest = cls.reader.split("## Source-exact composition manifest\n", 1)[1].split("\n---\n", 1)[0]
        cls.rows = ROW.findall(manifest)

    def test_01_prior_reader_preserved(self):
        self.assertEqual(git_blob(OLD), OLD_BLOB)

    def test_02_original_kevin_preserved(self):
        self.assertEqual(git_blob(KEVIN), KEVIN_BLOB)

    def test_03_original_jordan_preserved(self):
        self.assertEqual(git_blob(JORDAN), JORDAN_BLOB)

    def test_04_new_chapter_source_blob(self):
        self.assertEqual(git_blob(CHAPTER), CHAPTER_BLOB)

    def test_05_new_assembled_reader_blob(self):
        self.assertEqual(git_blob(READER), READER_BLOB)

    def test_06_following_wilson_source_preserved(self):
        self.assertEqual(git_blob(WILSON), WILSON_BLOB)

    def test_07_separate_2016_reader_preserved(self):
        self.assertEqual(git_blob(READER_2016), READER_2016_BLOB)

    def test_08_protected_2026_prologue_and_three_chapters(self):
        for path, expected_sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), expected_sha)

    def test_09_twelve_parts_become_eleven(self):
        self.assertEqual(len(self.original_wrappers), 12)
        self.assertEqual(len(self.wrappers), 11)
        self.assertEqual(re.findall(r"^## Part (\d+) —", self.reader, re.M),
                         [str(i) for i in range(1, 12)])

    def test_10_ten_retained_wrappers_are_byte_identical(self):
        old_kept = self.original_wrappers[:5] + self.original_wrappers[7:]
        new_kept = self.wrappers[:5] + self.wrappers[6:]
        self.assertEqual(len(old_kept), 10)
        for old, new in zip(old_kept, new_kept):
            with self.subTest(source=old.group(1)):
                self.assertEqual(old.group(0), new.group(0))

    def test_11_every_wrapper_matches_its_actual_git_source(self):
        for match in self.wrappers:
            source = BASE / match.group(1)
            with self.subTest(source=source.name):
                self.assertEqual(match.group(1), match.group(4))
                self.assertTrue(source.is_file())
                self.assertEqual(git_blob(source), match.group(2))
                self.assertEqual(source.read_text(encoding="utf-8").rstrip("\n"), match.group(3))

    def test_12_manifest_has_eleven_source_rows(self):
        self.assertEqual(len(self.rows), 11)

    def test_13_manifest_rows_correspond_to_wrapper_order(self):
        for i, row in enumerate(self.rows):
            with self.subTest(index=i):
                self.assertEqual(int(row[0]), i + 1)
                self.assertEqual(row[2].split("/")[-1], self.wrappers[i].group(1))
                self.assertEqual(row[3], self.wrappers[i].group(2))

    def test_14_manifest_words_are_source_exact(self):
        for row in self.rows:
            with self.subTest(source=row[2]):
                self.assertEqual(int(row[4]), len((ROOT / row[2]).read_text(encoding="utf-8").split()))

    def test_15_total_words_and_developmental_delta(self):
        self.assertEqual(len(self.chapter.split()), 5222)
        self.assertEqual(sum(int(row[4]) for row in self.rows), 59000)
        self.assertEqual(66528 - 59000, 7528)

    def test_16_twelve_registered_character_ids_survive(self):
        ids = {x for row in self.rows for x in re.findall(r"CHAR-[A-Z-]+", row[1])}
        self.assertEqual(len(ids), 12)

    def test_17_two_owners_alternate_six_limited_movements(self):
        movements = re.findall(r"^### ([IVX]+)\. [^\n]+ — (Kevin|Jordan)$", self.story, re.M)
        self.assertEqual(movements, [
            ("I", "Kevin"), ("II", "Jordan"), ("III", "Kevin"),
            ("IV", "Jordan"), ("V", "Kevin"), ("VI", "Jordan"),
        ])
        self.assertEqual(self.wrappers[5].group(1), CHAPTER.name)

    def test_18_retired_and_nonowner_principal_narration_excluded(self):
        self.assertIsNone(re.search(r"\b(?:Edrin|Edin|Oren)\b", self.story))
        self.assertNotRegex(self.story, r"^### [IVX]+\. [^\n]+ — (Ossa|Renn|Hal|Nera)$")

    def test_19_historical_team_slot_results_are_bounded(self):
        for phrase in ("slot 2", "Red Leopards", "6–8", "finalRank 11",
                       "slot 3", "Slob on my Dobb", "4–10", "finalRank 8"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.chapter)

    def test_20_real_manager_ownership_not_claimed(self):
        self.assertIn("UNKNOWN / NOT AUTHENTICATED", self.chapter)
        self.assertIn("provisional", self.chapter.lower())
        self.assertIn("not claims about either real person's actions", self.chapter)

    def test_21_watch_is_dismantled_but_roof_legs_stay(self):
        self.assertIn("floor/screen timber", self.chapter)
        self.assertIn("structural legs/roof remain", self.chapter)
        self.assertIn("watch becomes unstaffable above ground", self.chapter)

    def test_22_one_small_kitchen_hearth_not_two_nights_certified(self):
        self.assertIn("one small kitchen hearth", self.chapter)
        self.assertIn("one night only", self.chapter)
        self.assertIn("two-night conditional guarantee is not certified fulfilled", self.chapter)

    def test_23_second_wagon_still_waiting_for_wilson(self):
        self.assertIn("second wagon remains stranded", self.chapter)
        self.assertIn("Wilson's following chapter", self.chapter)
        self.assertIn("One eventually moves", self.chapter)

    def test_24_jordan_debt_and_watch_wages_do_not_vanish(self):
        self.assertIn("two-hour debt remains unpaid by Jordan", self.chapter)
        self.assertIn("watch\x27s separate unresolved paid-hours procedure", self.chapter)
        self.assertIn("not silently extinguished", self.chapter)

    def test_25_actual_connected_scene_with_consequence(self):
        self.assertGreater(len(self.story.split()), 4600)
        self.assertIn('"I took the floor out of the watch."', self.story)
        self.assertIn('"And I put a barrel where he turned."', self.story)
        self.assertIn('"Both approaches hold," she said.', self.story)

    def test_26_atlas_fiction_and_future_period_firewalls(self):
        self.assertIn("proposed secondary-world fiction", self.chapter)
        self.assertIn("No road, settlement, or route ID is certified", self.chapter)
        self.assertNotRegex(self.story, r"\b2026\s+(?:Week|championship|playoffs|final)")

    def test_27_independent_and_founder_gates_open(self):
        self.assertIn("Independent Authors Council", self.chapter)
        self.assertIn("FOUNDER", self.chapter)
        self.assertIn("NONCANON", self.reader)
        self.assertIn("independent literary", self.reader)

    def test_28_terminal_reading_manifest(self):
        self.assertTrue(self.reader.rstrip().endswith(
            "<!-- END_2025_TWELVE_VOICES_ELEVEN_PARTS_WATCH_GROUND_LEVEL_NONCANON -->"
        ))
        self.assertEqual(self.wrappers[6].group(1), WILSON.name)


if __name__ == "__main__":
    unittest.main()
