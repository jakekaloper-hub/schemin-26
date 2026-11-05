"""2025 source-exact sixteen-part developmental bridge; NONCANON.

These tests establish file/reader integrity and bounded narrative facts.
They do not authenticate historical manager IDs, fiction's Atlas geography,
independent literary merit, Umpire signoff or Founder promotion.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2025/causal-novel"
OLD = BASE / "READING_COPY_2025_TWELVE_VOICES_FIFTEEN_PARTS_NONCANON.md"
NEW = BASE / "READING_COPY_2025_TWELVE_VOICES_SIXTEEN_PARTS_DEVELOPMENTAL_NONCANON.md"
CHAPTER = BASE / "THE_NAME_BENEATH_THE_GOLD_AUSTIN_JAKE_2025_NONCANON.md"
PILOT = ROOT / "living-novel/production/historical-saga/R53/HISTORICAL_2025_OBIWAN_NONCANON_PILOT.md"
PREVIOUS_2016 = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel/READING_COPY_CAUSAL_CHAPTERS_01_72_NONCANON.md"

OLD_BLOB = "df42a31981d0017de410eaac3fb83f64454fed38"
CHAPTER_BLOB = "3c920a249aebb8f9b244d5e70027843a00708dad"
NEW_BLOB = "1910482c32d4c02c3b0f2b7f70a517c64e6a6abd"
PRIOR_2016_BLOB = "8f1dda21ac4962143ba3291cef4d60769197d62f"

PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
WRAPPER = re.compile(
    r"<!-- BEGIN 2025_VOICE ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n"
    r"([\s\S]*?)\n\n<!-- END 2025_VOICE ([^\n]+) -->"
)

def blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def source_for(name: str) -> Path:
    return PILOT if name == PILOT.name else BASE / name

class DevelopmentalBridge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = OLD.read_text(encoding="utf-8")
        cls.new = NEW.read_text(encoding="utf-8")
        cls.chapter = CHAPTER.read_text(encoding="utf-8")
        cls.oldwrap = list(WRAPPER.finditer(cls.old))
        cls.wrap = list(WRAPPER.finditer(cls.new))
        cls.story = cls.chapter.split("\n---\n\n### Source, causality", 1)[0]
        cls.manifest = cls.new.split("## Source-exact manifest\n", 1)[1].split("\n---\n", 1)[0]

    def test_01_prior_fifteen_part_edition_immutable(self):
        self.assertEqual(blob(OLD), OLD_BLOB)

    def test_02_exact_new_chapter_blob(self):
        self.assertEqual(blob(CHAPTER), CHAPTER_BLOB)

    def test_03_exact_new_reader_blob(self):
        self.assertEqual(blob(NEW), NEW_BLOB)

    def test_04_full_wrappers_present(self):
        self.assertEqual((len(self.oldwrap), len(self.wrap)), (15, 16))

    def test_05_new_chapter_inserted_at_part_three(self):
        self.assertEqual(self.wrap[2].group(1), CHAPTER.name)
        self.assertEqual(self.wrap[2].group(2), CHAPTER_BLOB)
        self.assertEqual(self.wrap[2].group(3), self.chapter.rstrip("\n"))

    def test_06_every_predecessor_wrapper_unchanged(self):
        for i, old in enumerate(self.oldwrap):
            with self.subTest(old_index=i + 1):
                new_index = i if i < 2 else i + 1
                self.assertEqual(old.group(0), self.wrap[new_index].group(0))

    def test_07_source_sha_and_exact_bytes_for_all(self):
        for wrapper in self.wrap:
            path = source_for(wrapper.group(1))
            with self.subTest(path=path.name):
                self.assertTrue(path.is_file())
                self.assertEqual(wrapper.group(1), wrapper.group(4))
                self.assertEqual(blob(path), wrapper.group(2))
                self.assertEqual(path.read_text(encoding="utf-8").rstrip("\n"), wrapper.group(3))

    def test_08_manifest_sequential_sixteen(self):
        self.assertEqual(re.findall(r"^\| (\d+) \|", self.manifest, re.M),
                         [str(i) for i in range(1, 17)])

    def test_09_manifest_names_match_wrappers(self):
        paths = re.findall(r"^\| \d+ \| .*? \| `([^`]+)` \| `([0-9a-f]{40})`", self.manifest, re.M)
        self.assertEqual(len(paths), 16)
        for i, (path, sha) in enumerate(paths):
            self.assertEqual(path.split("/")[-1], self.wrap[i].group(1))
            self.assertEqual(sha, self.wrap[i].group(2))

    def test_10_sources_sum_to_exact_words(self):
        self.assertEqual(sum(len(source_for(w.group(1)).read_text(encoding="utf-8").split()) for w in self.wrap), 81549)

    def test_11_chapter_source_word_count(self):
        self.assertEqual(len(self.chapter.split()), 5417)

    def test_12_narrative_prose_substantial(self):
        self.assertGreater(len(self.story.split()), 4300)

    def test_13_twelve_registered_owners_no_new_owner(self):
        rows = re.findall(r"^\| \d+ \| ([^|]+) \| `", self.manifest, re.M)
        names = {x for r in rows for x in re.findall(r"CHAR-[A-Z-]+", r)}
        self.assertEqual(len(rows), 16)
        self.assertEqual(len(names), 12)
        self.assertEqual(set(re.findall(r"CHAR-[A-Z-]+", rows[2])), {"CHAR-AUSTIN-BYARS", "CHAR-JAKE-KALOPER"})

    def test_14_only_two_interiors_six_movements(self):
        moves = re.findall(r"^### ([IVX]+)\. ([^\n]+) — (Jake|Austin)$", self.story, re.M)
        self.assertEqual([x[0] for x in moves], ["I", "II", "III", "IV", "V", "VI"])
        self.assertEqual([x[2] for x in moves], ["Jake", "Austin", "Jake", "Austin", "Jake", "Austin"])

    def test_15_no_retired_archive_pov(self):
        self.assertIsNone(re.search(r"\b(?:Edrin|Edin|Oren)\b", self.story))

    def test_16_year_specific_2024_winner_and_loser_name(self):
        self.assertIn("187.52–161.68", self.chapter)
        self.assertIn("The King", self.story)
        self.assertIn("ObiWan Jacoby", self.chapter)

    def test_17_year_specific_2025_result_retained(self):
        self.assertIn("161.07–109.56", self.chapter)
        self.assertIn("The Immortal", self.story)

    def test_18_semifinal_anchor_no_alternative_outcome(self):
        self.assertIn("152.20–151.80", self.chapter)
        self.assertIn("The Immortal", self.chapter)

    def test_19_belt_correct_custody(self):
        self.assertIn("The Belt belongs to Austin", self.chapter)
        self.assertIn("Austin", self.story)

    def test_20_fictional_2025_manager_link_unverified(self):
        self.assertIn("do NOT authenticate period human manager identities", self.chapter)
        self.assertIn("provisional fictional", self.chapter)

    def test_21_no_fictional_hall_claimed_approved_atlas(self):
        self.assertIn("period World/Atlas review", self.chapter)
        self.assertIn("PROPOSED FICTION", self.chapter)

    def test_22_character_opposition_not_easy_agreement(self):
        self.assertIn("patron's money", self.story)
        self.assertIn("defeated man's pride", self.story)
        self.assertIn("the rivalry unresolved", self.chapter)

    def test_23_prior_hard_main_manuscript_preserved(self):
        for path, expected in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(blob(ROOT / path), expected)

    def test_24_2016_seventy_two_reader_preserved(self):
        self.assertEqual(blob(PREVIOUS_2016), PRIOR_2016_BLOB)

    def test_25_old_terminal_marker_remains_unchanged(self):
        self.assertTrue(self.old.rstrip().endswith("<!-- END_2025_TWELVE_VOICES_FIFTEEN_PARTS_NONCANON -->"))
        self.assertTrue(self.new.rstrip().endswith("<!-- END_2025_TWELVE_VOICES_SIXTEEN_PARTS_DEVELOPMENTAL_NONCANON -->"))

    def test_26_not_claiming_accepted_rewrite(self):
        self.assertIn("NOT an accepted comprehensive developmental rewrite", self.new)
        self.assertIn("independently accepted novel", self.new)
        self.assertIn("No merge, canon promotion, deployment", self.chapter)

if __name__ == "__main__":
    unittest.main()
