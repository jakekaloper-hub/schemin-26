"""2025 three-voice source-exact reader QA; NOT independent editorial review."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2025/causal-novel"
SOURCES = (
    (BASE / "THE_NARROWEST_DOOR_AUSTIN_2025_NONCANON.md", "ae5d50aca6c1ac4da20fb8ead28554baa5e70613", "CHAR-AUSTIN-BYARS", 5001),
    (ROOT / "living-novel/production/historical-saga/R53/HISTORICAL_2025_OBIWAN_NONCANON_PILOT.md", "9737fa9b9832de847ee504ed9b87d5e2c404e481", "CHAR-JAKE-KALOPER", 983),
    (BASE / "THE_COURSE_BENEATH_THE_COURSE_ZACH_2025_NONCANON.md", "112b3890173cbf11879b139bff966cdff83884d4", "CHAR-ZACH-WILSON", 5310),
)
READER = BASE / "READING_COPY_2025_THREE_VOICES_NONCANON.md"
READER_SHA = "c09df3abe7233b2a1eb7edd84274d5550ed759cb"
PREVIOUS_READER = BASE / "READING_COPY_2025_TWO_VOICES_NONCANON.md"
PREVIOUS_READER_SHA = "3d82eb3a17c23154bee5c6fd4bde601c19fd372b"
PREVIOUS_2016 = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel/READING_COPY_CAUSAL_CHAPTERS_01_72_NONCANON.md"
PREVIOUS_2016_SHA = "8f1dda21ac4962143ba3291cef4d60769197d62f"
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
TICK = chr(96)
MANIFEST = re.compile(
    r"^\| ([123]) \| ([^|]+) \| " + TICK + r"([^\n]+?)" + TICK + r" \| " +
    TICK + r"([0-9a-f]{40})" + TICK + r" \| (\d+) \|$", re.M
)

def git_blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

class ThreeVoices2025SourceReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contents = [path.read_text(encoding="utf-8") for path, _, _, _ in SOURCES]
        cls.reader = READER.read_text(encoding="utf-8")
        cls.wrappers = list(WRAPPER.finditer(cls.reader))
        cls.rows = list(MANIFEST.finditer(cls.reader))
        cls.zach = cls.contents[2]

    def test_01_original_sources_exact_blob(self):
        for path, sha, _, _ in SOURCES:
            with self.subTest(path=path.name):
                self.assertEqual(git_blob(path), sha)

    def test_02_assembled_reader_exact_blob(self):
        self.assertEqual(git_blob(READER), READER_SHA)

    def test_03_exact_three_wrapper_count(self):
        self.assertEqual(len(self.wrappers), 3)

    def test_04_exact_three_manifest_rows(self):
        self.assertEqual(len(self.rows), 3)

    def test_05_source_exact_embedded_bodies(self):
        for i, (path, sha, _, _) in enumerate(SOURCES):
            begin, declared_sha, body, end = self.wrappers[i].groups()
            self.assertEqual(begin, path.name)
            self.assertEqual(end, path.name)
            self.assertEqual(declared_sha, sha)
            self.assertEqual(body.strip("\n"), self.contents[i].rstrip("\n"))

    def test_06_manifest_refs_counts_and_order(self):
        for i, (path, sha, owner, count) in enumerate(SOURCES):
            row = self.rows[i]
            self.assertEqual(int(row.group(1)), i+1)
            self.assertIn(owner, row.group(2))
            self.assertEqual(row.group(3), str(path.relative_to(ROOT)))
            self.assertEqual(row.group(4), sha)
            self.assertEqual(int(row.group(5)), count)

    def test_07_zach_is_substantive(self):
        self.assertEqual(len(self.zach.split()), 5310)
        self.assertEqual(len(re.findall(r"^### [IVX]+\. ", self.zach, re.M)), 6)

    def test_08_distinct_owner_interior(self):
        for _, _, owner, _ in SOURCES:
            self.assertIn(owner, self.reader)
        self.assertIn("sole interior viewpoint", self.zach)

    def test_09_restricted_institutional_pov_absent(self):
        narrative = self.zach.split("\n---\n\n### Source and narrative handoff")[0]
        self.assertIsNone(re.search(r"\b(?:Edrin|Edin|Master Oren)\b", narrative, re.I))

    def test_10_semifinal_score_correct(self):
        self.assertIn("152.20–151.80", self.reader)
        self.assertIn("151.80–152.20", self.zach)

    def test_11_final_score_correct(self):
        self.assertIn("161.07–109.56", self.reader)
        self.assertIn("161.07–109.56", self.zach)

    def test_12_no_false_historical_owner_claim(self):
        for term in ("UNKNOWN", "owner-account", "2025 Atlas"):
            self.assertIn(term, self.zach)
        self.assertIn("historical human-owner account mapping remains UNKNOWN", self.reader)

    def test_13_projected_geography_is_proposed(self):
        for phrase in ("PROPOSED_UNAPPROVED", "not ESPN events", "2025 Atlas locations"):
            self.assertIn(phrase, self.zach)

    def test_14_story_time_after_final(self):
        self.assertIn("after the certified 2025 championship", self.zach.lower())
        self.assertIn("no 2026 knowledge", self.zach)

    def test_15_no_canon_promotion(self):
        for term in ("DRAFT / NONCANON", "FOUNDER ACCEPTANCE HOLD", "independent Umpire"):
            self.assertIn(term, self.reader)
        self.assertIn("No merge/publication/canon promotion", self.reader)

    def test_16_previous_two_voice_reader_preserved(self):
        self.assertEqual(git_blob(PREVIOUS_READER), PREVIOUS_READER_SHA)

    def test_17_previous_2016_reader_preserved(self):
        self.assertEqual(git_blob(PREVIOUS_2016), PREVIOUS_2016_SHA)

    def test_18_protected_hard_canon_preserved(self):
        for name, sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(git_blob(ROOT/name), sha)

    def test_19_material_dramatic_turn(self):
        for phrase in ("The lower practice lane is flooded", "The water's through my threshold",
                       "The permission came back with an argument attached", "A fine green lay broken"):
            self.assertIn(phrase, self.zach)

    def test_20_reader_closes(self):
        self.assertTrue(self.reader.rstrip().endswith("<!-- END_2025_THREE_VOICES_NONCANON -->"))

if __name__ == "__main__":
    unittest.main()
