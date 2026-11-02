"""Noncanon 2025 triple-developmental reading: exact-byte and evidence firewalls.

These tests assert source integrity and known constraints only. They do not
constitute literary approval, historical manager authentication, period Atlas
validation, or independent Umpire acceptance.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2025/causal-novel"
CHAPTER = BASE / "WHAT_THE_DOOR_COULD_HOLD_BEN_DAVID_2025_DEVELOPMENTAL_NONCANON.md"
READER = BASE / "READING_COPY_2025_TWELVE_VOICES_TWELVE_PARTS_TRIPLE_INTEGRATION_NONCANON.md"
OLD = BASE / "READING_COPY_2025_TWELVE_VOICES_THIRTEEN_PARTS_DUAL_COMPRESSION_NONCANON.md"
BEN = BASE / "THE_SIXTH_PLACE_AT_THE_TABLE_BEN_2025_NONCANON.md"
DAVID = BASE / "THE_WINTER_CLAUSE_DAVID_2025_NONCANON.md"
BRANDON = BASE / "THE_FIRST_LOAD_BRANDON_2025_NONCANON.md"
READER_2016 = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel/READING_COPY_CAUSAL_CHAPTERS_01_72_NONCANON.md"

CHAPTER_BLOB = "4425ddab9b8c59936c967f41d634439d64da5204"
READER_BLOB = "0510c40d3e33d1dde6720e8196ca87f23afd5bbf"
OLD_BLOB = "fe6e4056c951323aba19b302c67897bda96d59b9"
BEN_BLOB = "9a2b618d498ad97a6343366dcc18ddc409041419"
DAVID_BLOB = "0de993d2cb3865a7d37ce8cb8f1a9c719c37253c"
BRANDON_BLOB = "2cce2e20c426a1e1820d738cebf89c7d815e8458"
OLD_2016_BLOB = "8f1dda21ac4962143ba3291cef4d60769197d62f"

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


class TripleDevelopmentalIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = CHAPTER.read_text(encoding="utf-8")
        cls.reader = READER.read_text(encoding="utf-8")
        cls.old = OLD.read_text(encoding="utf-8")
        cls.story = cls.chapter.split("### Production/source boundary", 1)[0]
        cls.old_wrap = list(WRAP.finditer(cls.old))
        cls.new_wrap = list(WRAP.finditer(cls.reader))
        table = cls.reader.split("## Source-exact composition manifest\n", 1)[1].split("\n---\n", 1)[0]
        cls.rows = ROW.findall(table)

    def test_01_prior_reader_preserved(self):
        self.assertEqual(git_blob(OLD), OLD_BLOB)

    def test_02_original_ben_preserved(self):
        self.assertEqual(git_blob(BEN), BEN_BLOB)

    def test_03_original_david_preserved(self):
        self.assertEqual(git_blob(DAVID), DAVID_BLOB)

    def test_04_following_brandon_preserved(self):
        self.assertEqual(git_blob(BRANDON), BRANDON_BLOB)

    def test_05_new_chapter_blob(self):
        self.assertEqual(git_blob(CHAPTER), CHAPTER_BLOB)

    def test_06_new_reader_blob(self):
        self.assertEqual(git_blob(READER), READER_BLOB)

    def test_07_old_new_wrapper_counts(self):
        self.assertEqual(len(self.old_wrap), 13)
        self.assertEqual(len(self.new_wrap), 12)

    def test_08_retained_wrappers_exactly_preserved(self):
        before = self.old_wrap[:2] + self.old_wrap[4:]
        after = self.new_wrap[:2] + self.new_wrap[3:]
        self.assertEqual(len(before), 11)
        self.assertEqual(len(after), 11)
        for prev, new in zip(before, after):
            with self.subTest(name=prev.group(1)):
                self.assertEqual(prev.group(0), new.group(0))

    def test_09_every_wrapper_exact_to_git_source(self):
        for item in self.new_wrap:
            source = BASE / item.group(1)
            with self.subTest(source=source.name):
                self.assertEqual(item.group(1), item.group(4))
                self.assertTrue(source.is_file())
                self.assertEqual(git_blob(source), item.group(2))
                self.assertEqual(source.read_text(encoding="utf-8").rstrip("\n"), item.group(3))

    def test_10_sequence_is_twelve_parts(self):
        self.assertEqual(re.findall(r"^## Part (\d+) —", self.reader, re.M),
                         [str(i) for i in range(1, 13)])

    def test_11_manifest_order_matches_wrappers(self):
        self.assertEqual(len(self.rows), 12)
        for index, row in enumerate(self.rows):
            with self.subTest(index=index):
                self.assertEqual(int(row[0]), index + 1)
                self.assertEqual(row[2].split("/")[-1], self.new_wrap[index].group(1))
                self.assertEqual(row[3], self.new_wrap[index].group(2))

    def test_12_manifest_words_are_exact(self):
        for row in self.rows:
            source = BASE / row[2].split("/")[-1]
            self.assertEqual(int(row[4]), len(source.read_text(encoding="utf-8").split()))

    def test_13_source_word_count_and_edit_delta(self):
        self.assertEqual(len(self.chapter.split()), 5393)
        self.assertEqual(sum(int(row[4]) for row in self.rows), 66528)
        self.assertEqual(70117 - 66528, 3589)

    def test_14_all_twelve_registered_owner_povs_retained(self):
        ids = {item for row in self.rows for item in re.findall(r"CHAR-[A-Z-]+", row[1])}
        self.assertEqual(len(ids), 12)

    def test_15_new_replacement_at_position_three(self):
        self.assertEqual(self.new_wrap[2].group(1), CHAPTER.name)
        self.assertEqual(set(re.findall(r"CHAR-[A-Z-]+", self.rows[2][1])),
                         {"CHAR-BEN-WHIPPLE", "CHAR-DAVID-BABB"})

    def test_16_six_alternating_owner_movements(self):
        movements = re.findall(r"^### ([IVX]+)\. [^\n]+ — (Ben|David)$", self.story, re.M)
        self.assertEqual(movements, [("I", "Ben"), ("II", "David"),
                                    ("III", "Ben"), ("IV", "David"),
                                    ("V", "Ben"), ("VI", "David")])

    def test_17_no_retired_or_nonowner_narration(self):
        self.assertIsNone(re.search(r"\b(?:Edrin|Edin|Oren)\b", self.story))
        self.assertNotIn("### VII.", self.story)

    def test_18_historical_team_slot_results_precise(self):
        for phrase in ("slot 11", "Seven Deadly Chins", "6–8",
                       "finalRank 6", "slot 4", "The LLC", "4–10", "finalRank 10"):
            self.assertIn(phrase, self.chapter)

    def test_19_manager_ownership_is_not_authenticated(self):
        self.assertIn("UNKNOWN / NOT AUTHENTICATED", self.chapter)
        self.assertIn("provisional", self.chapter.lower())

    def test_20_supply_contract_not_magically_fulfilled(self):
        for phrase in ("two-night personal fuel guarantee",
                       "No delivery, accepted receipt, payment",
                       "signed", "inspection", "third night"):
            self.assertIn(phrase.lower(), self.chapter.lower())

    def test_21_no_automatic_worker_vote(self):
        self.assertIn("4–2", self.chapter)
        self.assertIn("worker-nomination motion", self.chapter)
        self.assertIn("seventh stool", self.chapter.lower())

    def test_22_consequential_prose_not_an_outline(self):
        self.assertGreater(len(self.story.split()), 4450)
        self.assertIn("The boy took the bowl with both hands", self.story)
        self.assertIn("He crossed out the fixtures and passage rights", self.story)

    def test_23_explicit_fiction_and_atlas_firewalls(self):
        self.assertIn("proposed secondary-world fiction", self.chapter)
        self.assertIn("No route ID", self.chapter)
        self.assertNotIn("ATLAS_APPROVED", self.chapter)

    def test_24_prior_2016_reader_untouched(self):
        self.assertEqual(git_blob(READER_2016), OLD_2016_BLOB)

    def test_25_hard_canon_prologue_and_chapters_1_to_3_untouched(self):
        for path, expected_sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), expected_sha)

    def test_26_no_2026_future_outcome_in_story(self):
        self.assertNotRegex(self.story, r"\b2026\s+(?:Week|championship|playoffs|final)")
        self.assertIn("knows no 2026 outcome", self.chapter)

    def test_27_independent_gates_are_not_claimed_passed(self):
        self.assertIn("no independent Authors Council", self.reader)
        self.assertIn("review hold", self.reader.lower())
        self.assertIn("Founder approval", self.chapter)

    def test_28_terminal_manifest_tag_and_following_brandon(self):
        self.assertTrue(self.reader.rstrip().endswith(
            "<!-- END_2025_TWELVE_VOICES_TWELVE_PARTS_TRIPLE_INTEGRATION_NONCANON -->"
        ))
        self.assertEqual(self.new_wrap[3].group(1), BRANDON.name)


if __name__ == "__main__":
    unittest.main()
