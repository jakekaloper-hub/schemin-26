"""Noncanonical 2025 14-part compressed opening: source-exact assembly guards.

No technical assertion establishes historical manager ownership, approved fictional
geography, literary excellence or independent Umpire/Founder authorization.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2025/causal-novel"
CHAPTER = BASE / "THE_STONE_THAT_COULD_NOT_WIN_AUSTIN_JAKE_2025_DEVELOPMENTAL_NONCANON.md"
NEW = BASE / "READING_COPY_2025_TWELVE_VOICES_FOURTEEN_PARTS_COMPRESSED_OPENING_NONCANON.md"
OLD = BASE / "READING_COPY_2025_TWELVE_VOICES_SIXTEEN_PARTS_DEVELOPMENTAL_NONCANON.md"
PILOT = ROOT / "living-novel/production/historical-saga/R53/HISTORICAL_2025_OBIWAN_NONCANON_PILOT.md"
PREVIOUS_2016 = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel/READING_COPY_CAUSAL_CHAPTERS_01_72_NONCANON.md"
NEW_CHAPTER_BLOB = "893056edeb514dcea60e1e3a77d34af7620d47b3"
NEW_READER_BLOB = "7d9ca508d925493723478d02e0afc97d2276bdd9"
OLD_READER_BLOB = "1910482c32d4c02c3b0f2b7f70a517c64e6a6abd"
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

def blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def source_for(name):
    return PILOT if name == PILOT.name else BASE / name

class CompressedOpening(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = CHAPTER.read_text(encoding="utf-8")
        cls.new = NEW.read_text(encoding="utf-8")
        cls.old = OLD.read_text(encoding="utf-8")
        cls.wrap = list(WRAPPER.finditer(cls.new))
        cls.oldwrap = list(WRAPPER.finditer(cls.old))
        cls.manifest = cls.new.split("## Source-exact composition manifest\n", 1)[1].split("\n---\n", 1)[0]
        cls.story = cls.chapter.split("### Production/source boundary", 1)[0]

    def test_01_predecessor_edition_immutable(self):
        self.assertEqual(blob(OLD), OLD_READER_BLOB)

    def test_02_new_chapter_digest(self):
        self.assertEqual(blob(CHAPTER), NEW_CHAPTER_BLOB)

    def test_03_new_reader_digest(self):
        self.assertEqual(blob(NEW), NEW_READER_BLOB)

    def test_04_manifest_and_part_counts(self):
        self.assertEqual((len(self.oldwrap), len(self.wrap)), (16, 14))

    def test_05_first_wrapped_chapter_correct(self):
        w = self.wrap[0]
        self.assertEqual(w.group(1), CHAPTER.name)
        self.assertEqual(w.group(2), NEW_CHAPTER_BLOB)
        self.assertEqual(w.group(3), self.chapter.rstrip("\n"))

    def test_06_remaining_thirteen_wrappers_are_exact(self):
        for i, (before, after) in enumerate(zip(self.oldwrap[3:], self.wrap[1:])):
            with self.subTest(chapter=i+2):
                self.assertEqual(before.group(0), after.group(0))

    def test_07_sources_match_git_blobs_and_reader_bytes(self):
        for wrapper in self.wrap:
            path = source_for(wrapper.group(1))
            with self.subTest(path=path.name):
                self.assertTrue(path.is_file())
                self.assertEqual(wrapper.group(1), wrapper.group(4))
                self.assertEqual(blob(path), wrapper.group(2))
                self.assertEqual(path.read_text(encoding="utf-8").rstrip("\n"), wrapper.group(3))

    def test_08_sequential_fourteen_part_labels(self):
        nums = re.findall(r"^## Part (\d+) —", self.new, re.M)
        self.assertEqual(nums, list(map(str, range(1, 15))))

    def test_09_manifest_matches_fourteen_wrappers(self):
        rows = re.findall(r"^\| (\d+) \| ([^|]+) \| \x60([^\x60]+)\x60 \| \x60([0-9a-f]{40})\x60 \| (\d+) \|$", self.manifest, re.M)
        self.assertEqual(len(rows), 14)
        for i, row in enumerate(rows):
            self.assertEqual(row[0], str(i+1))
            self.assertEqual(row[2].split("/")[-1], self.wrap[i].group(1))
            self.assertEqual(row[3], self.wrap[i].group(2))

    def test_10_source_words_recomputed(self):
        self.assertEqual(sum(len(source_for(w.group(1)).read_text(encoding="utf-8").split()) for w in self.wrap), 75042)

    def test_11_new_source_words_and_narrative_minimum(self):
        self.assertEqual(len(self.chapter.split()), 4894)
        self.assertGreater(len(self.story.split()), 4500)

    def test_12_twelve_distinct_registered_owner_views(self):
        rows = re.findall(r"^\| \d+ \| ([^|]+) \| \x60", self.manifest, re.M)
        owners = {v for row in rows for v in re.findall(r"CHAR-[A-Z-]+", row)}
        self.assertEqual(len(owners), 12)
        self.assertEqual(set(re.findall(r"CHAR-[A-Z-]+", rows[0])),
                         {"CHAR-JAKE-KALOPER", "CHAR-AUSTIN-BYARS"})

    def test_13_six_changing_legal_pov_movements(self):
        movements = re.findall(r"^### ([IVX]+)\. ([^\n]+) — (Austin|Jake)$", self.story, re.M)
        self.assertEqual([m[0] for m in movements], ["I", "II", "III", "IV", "V", "VI"])
        self.assertEqual([m[2] for m in movements], ["Austin", "Jake", "Austin", "Jake", "Austin", "Jake"])

    def test_14_no_retired_institutional_pov(self):
        self.assertIsNone(re.search(r"\b(Edrin|Edin|Oren)\b", self.story))

    def test_15_proven_score_anchors(self):
        for score in ("152.20", "151.80", "161.07", "109.56", "187.52", "161.68"):
            self.assertIn(score, self.story)

    def test_16_temporal_names_and_custody(self):
        self.assertIn("The King", self.story)
        self.assertIn("The Immortal", self.story)
        self.assertIn("Austin accepted it", self.story)
        self.assertIn("The current Belt was fastened at Austin's waist", self.story)

    def test_17_edit_has_costly_shared_turning_point(self):
        for detail in ("thirty-six", "patron", "foreman", "ceremonial fund", "rail"):
            self.assertIn(detail, self.story)

    def test_18_period_ownership_not_falsely_verified(self):
        self.assertIn("not independently authenticated", self.chapter)
        self.assertIn("provisional", self.new.lower())
        self.assertIn("NONCANON", self.new)

    def test_19_fictional_hall_does_not_claim_atlas_approval(self):
        self.assertIn("proposed secondary-world fiction", self.chapter)
        self.assertIn("not league events or approved historical geography", self.chapter)

    def test_20_protected_2026_hard_manuscript_untouched(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(blob(ROOT / path), sha)

    def test_21_previous_2016_reader_untouched(self):
        self.assertEqual(blob(PREVIOUS_2016), PRIOR_2016_BLOB)

    def test_22_no_publication_or_independent_approval_claim(self):
        self.assertIn("NOT AN APPROVED REPLACEMENT", self.chapter)
        self.assertIn("No author, Umpire or Founder approval is inferred", self.new)

    def test_23_terminal_markers(self):
        self.assertTrue(self.old.rstrip().endswith(
            "<!-- END_2025_TWELVE_VOICES_SIXTEEN_PARTS_DEVELOPMENTAL_NONCANON -->"))
        self.assertTrue(self.new.rstrip().endswith(
            "<!-- END_2025_TWELVE_VOICES_FOURTEEN_PARTS_COMPRESSED_OPENING_NONCANON -->"))

if __name__ == "__main__":
    unittest.main()
