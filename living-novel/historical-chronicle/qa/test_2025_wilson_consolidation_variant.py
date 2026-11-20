"""Fail-closed source-integrity checks for alternate 2025 Wilson consolidation.
Technical checks do not certify historical owners, literary quality,
period Atlas, Character Canon, the Umpire, or Founder canon approval.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2025/causal-novel"
CURRENT = BASE / "READING_COPY_2025_TWELVE_VOICES_ELEVEN_PARTS_WILSON_CONSOLIDATED_NONCANON.md"
CHAPTER = BASE / "THE_ROAD_NO_BANNER_COULD_OWN_TWO_TRUE_DISPATCHES_WILSON_2025_INTEGRATED_NONCANON.md"
PREVIOUS = BASE / "READING_COPY_2025_TWELVE_VOICES_TWELVE_PARTS_DISPATCH_BRIDGE_NONCANON.md"
OLD = BASE / "THE_ROAD_NO_BANNER_COULD_OWN_WILSON_2025_NONCANON.md"
DISPATCH = BASE / "THE_TWO_WORDS_THAT_TRAVELED_WILSON_2025_DEVELOPMENTAL_NONCANON.md"
HIST_AUDIT = ROOT / "living-novel/historical-chronicle/seasons/2016/source-audits/FLAIM_ESPN_2016_SLOT_OUTCOME_AND_POV_BINDING_AUDIT_2026-11-02.md"
PINNED = {
    CURRENT: "5e1679d01c16742bc222d8bafc23cde6a73582d4",
    CHAPTER: "57b767cf2d417895db070c24fa7da07892629f62",
    PREVIOUS: "df153f16717f77b7b9c760441c331a7445786c99",
    OLD: "b737814a6049175ad15ea354cd6e2f44e449f75b",
    DISPATCH: "dcddddd05ed4b4b151b11b856fbc01e77aa58dc6",
}
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
WRAP = re.compile(
    r"<!-- BEGIN 2025_VOICE (\S+) \| git_blob ([a-f0-9]{40}) -->\n"
    r"([\s\S]*?)\n<!-- END 2025_VOICE \1 -->"
)
ROW = re.compile(
    r"^\| (\d+) \| ([^|]+) \| \x60([^\x60]+)\x60 \| \x60([a-f0-9]{40})\x60 \| (\d+) \|$",
    re.M,
)
OWNERS = {
    "CHAR-AUSTIN-BYARS", "CHAR-JAKE-KALOPER", "CHAR-ZACH-WILSON",
    "CHAR-PHILLIP-PITTS", "CHAR-BEN-WHIPPLE", "CHAR-DAVID-BABB",
    "CHAR-BRANDON-PRYOR", "CHAR-BOBBY-MITCHELL", "CHAR-KEVIN-ZEEK",
    "CHAR-JORDAN-HOLLINGSHEAD", "CHAR-WILSON-LOOK", "CHAR-MANNING-WELTY",
}

def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()

class WilsonConsolidationVariant(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader = CURRENT.read_text(encoding="utf-8")
        cls.chapter = CHAPTER.read_text(encoding="utf-8")
        cls.previous = PREVIOUS.read_text(encoding="utf-8")
        cls.wraps = list(WRAP.finditer(cls.reader))
        cls.old_wraps = list(WRAP.finditer(cls.previous))
        cls.rows = ROW.findall(cls.reader)
        cls.aud = HIST_AUDIT.read_text(encoding="utf-8")

    def test_01_pinned_source_blobs(self):
        for path, expected in PINNED.items():
            with self.subTest(path=path.name):
                self.assertEqual(git_blob(path), expected)

    def test_02_protected_manuscript_blobs(self):
        for path, expected in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), expected)

    def test_03_part_count(self):
        self.assertEqual(len(self.wraps), 11)
        self.assertEqual(len(self.old_wraps), 12)
        self.assertEqual(len(self.rows), 11)

    def test_04_source_exact_wrappers(self):
        for i, (row, m) in enumerate(zip(self.rows, self.wraps), start=1):
            part, _owner, path, sha, total = row
            with self.subTest(part=i):
                source = ROOT / path
                self.assertEqual(int(part), i)
                self.assertEqual(m.group(1), source.name)
                self.assertEqual(m.group(2), sha)
                self.assertEqual(git_blob(source), sha)
                self.assertEqual(m.group(3).strip(), source.read_text(encoding="utf-8").strip())
                self.assertEqual(len(source.read_text(encoding="utf-8").split()), int(total))

    def test_05_word_count(self):
        self.assertEqual(sum(int(r[4]) for r in self.rows), 61408)
        self.assertIn("61408 whitespace-delimited source words", self.reader)

    def test_06_exclusive_canonical_owners(self):
        seen = set()
        for _index, owner, _path, _sha, _n in self.rows:
            seen.update(re.findall(r"CHAR-[A-Z0-9-]+", owner))
        self.assertEqual(seen, OWNERS)

    def test_07_wilson_one_part(self):
        self.assertEqual(sum("CHAR-WILSON-LOOK" in r[1] for r in self.rows), 1)
        self.assertEqual(sum(CHAPTER.name == r[2].split("/")[-1] for r in self.rows), 1)

    def test_08_one_departure_second_held(self):
        self.assertEqual(self.chapter.count("The procession moved."), 1)
        self.assertIn("The second wagon stayed where it was.", self.chapter)
        self.assertNotIn("stranded second wagon crosses", self.chapter.lower())

    def test_09_qualified_loaded_crossing(self):
        self.assertIn("An empty cart was examined yesterday", self.chapter)
        self.assertIn("ONE INSPECTED LOADED WAGON PASSED", self.chapter)
        self.assertIn("NO CLEARANCE FOR FURTHER LOADED CROSSING", self.chapter)

    def test_10_source_provenance(self):
        self.assertIn(PINNED[OLD], self.chapter)
        self.assertIn(PINNED[DISPATCH], self.chapter)

    def test_11_release_hold_and_owner_authentication(self):
        self.assertIn("DRAFT / NONCANON", self.reader)
        self.assertIn("UNKNOWN / UNAUTHENTICATED", self.chapter)
        self.assertIn("NO MERGE / NO CANON PROMOTION / NO PUBLICATION", self.chapter)

    def test_12_2016_two_austin_slots_not_conflated(self):
        self.assertIn("Austin's Hyena's", self.aud)
        self.assertIn("The Real Austin's Hyenas", self.aud)
        self.assertIn("team slot 1", self.aud)
        self.assertIn("fourth", self.aud)

    def test_13_movement_order(self):
        self.assertEqual(
            re.findall(r"^### ([IVX]+)\. ", self.chapter, re.M),
            ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"],
        )

if __name__ == "__main__":
    unittest.main()
