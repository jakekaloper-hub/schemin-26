"""Source-exact Chapter XXVII V2 and 24-part developmental 2016 reader; NONCANON."""
import hashlib
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
NEW = "READING_COPY_2016_CAUSAL_CH01_27_TWENTY_FOUR_PARTS_FISH_AND_RIVER_V2_NONCANON.md"
OLD = "READING_COPY_2016_CAUSAL_CH01_26_TWENTY_THREE_PARTS_OPEN_DOOR_NONCANON.md"
CH27V2 = "THE_ROOM_WITH_NO_HIGH_SEAT_THE_FISH_THAT_WOULD_NOT_DROWN_CH27_V2_NONCANON.md"
CH27OLD = "THE_ROOM_WITH_NO_HIGH_SEAT_CHAPTER_27_NONCANON.md"
CH26 = "THE_BOARD_AT_THE_OPEN_DOOR_CHAPTER_26_NONCANON.md"
CH28 = "THE_SLEEVE_LEFT_UNSTITCHED_CHAPTER_28_NONCANON.md"
OLD_READER_SHA = "d88eecbe5395064348bca0cf0c660b2a2461435d"
OLD_CH27_SHA = "d451e61332ce6da3911cf77957596b09edcaecdf"
CH26_SHA = "5957266328b8035684c59a1e8c0501f657e05d59"
NEW_CH27_SHA = "b2f469370281a5368b2469c2cacb7766a2f1e607"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def rows(text):
    return [(int(n), name, sha, int(w)) for n, name, sha, w in re.findall(
        r"^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([0-9a-f]{40})\x60 \| (\d+) \|$", text, re.M)]

def embedded(text, name, sha):
    start = "<!-- BEGIN 2016_CAUSAL " + name + " | git_blob " + sha + " -->"
    end = "<!-- END 2016_CAUSAL " + name + " -->"
    assert text.count(start) == text.count(end) == 1, name
    return text.split(start, 1)[1].split(end, 1)[0].strip()

class ChapterTwentySevenFishReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader = (BASE / NEW).read_text()
        cls.prior = (BASE / OLD).read_text()
        cls.v2 = (BASE / CH27V2).read_text()
        cls.original = (BASE / CH27OLD).read_text()
        cls.chapter26 = (BASE / CH26).read_text()
        cls.chapter28 = (BASE / CH28).read_text()
        cls.manifest = rows(cls.reader)
        cls.old_manifest = rows(cls.prior)

    def test_01_ordered_manifest(self):
        self.assertEqual([n for n, _, _, _ in self.manifest], list(range(1, 25)))
        self.assertEqual(len(self.old_manifest), 23)
        self.assertEqual(self.manifest[-1][1], CH27V2)

    def test_02_each_embedded_component_source_exact(self):
        for n, name, sha, words in self.manifest:
            with self.subTest(part=n):
                s = (BASE / name).read_text()
                self.assertEqual(embedded(self.reader, name, sha), s.strip())
                self.assertEqual(len(s.split()), words)

    def test_03_all_manifest_git_blob_hashes(self):
        for n, name, sha, _ in self.manifest:
            with self.subTest(part=n):
                self.assertEqual(blob(BASE / name), sha)

    def test_04_prior_reader_blob_preserved(self):
        self.assertEqual(blob(BASE / OLD), OLD_READER_SHA)
        self.assertEqual(self.manifest[:23], self.old_manifest)

    def test_05_all_prior_twenty_three_bodies_preserved(self):
        for n, name, sha, _ in self.old_manifest:
            with self.subTest(part=n):
                self.assertEqual(embedded(self.reader, name, sha),
                                 embedded(self.prior, name, sha))

    def test_06_original_chapter27_not_rewritten(self):
        self.assertEqual(blob(BASE / CH27OLD), OLD_CH27_SHA)
        self.assertEqual(self.v2.split("### VI.", 1)[0].strip(),
                         self.original.split("\n---\n\n### Editorial handoff", 1)[0].strip())

    def test_07_new_chapter_v2_blob_pinned(self):
        self.assertEqual(blob(BASE / CH27V2), NEW_CH27_SHA)
        self.assertEqual(self.manifest[-1][2], NEW_CH27_SHA)

    def test_08_fiction_adds_cultural_performance_not_a_score(self):
        self.assertIn("### VI. The fish that would not drown", self.v2)
        self.assertIn("a prince bought a river", self.v2)
        self.assertIn("the fish had gone wherever fish went", self.v2)
        self.assertIn("Iri", self.v2)

    def test_09_letter_not_certified_delivered(self):
        self.assertIn("The letter was no longer on Jake's shelf", self.v2)
        self.assertIn("It had not reached Esi", self.v2)
        self.assertIn("the letter's arrival at Esi is **NOT CONFIRMED**", self.reader)

    def test_10_wage_and_safety_timeline_still_unresolved(self):
        self.assertIn("Four hours, if you work all four", self.chapter26)
        self.assertIn("He had been paid for four hours", self.chapter26)
        self.assertIn("Nothing for you this morning", self.v2)
        self.assertIn("The kiln crossing was dark", self.v2)
        self.assertIn("Vessa retains kiln-safety authority", self.reader)

    def test_11_next_chapter_inherits_same_state(self):
        self.assertIn("Story-time follows Chapter XXVII", self.chapter28)
        self.assertIn("delivery to Esi remains unconfirmed", self.chapter28)
        self.assertIn("The kiln passage remains closed", self.chapter28)

    def test_12_2016_competition_evidence_unchanged(self):
        path = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(blob(path), ARCHIVE_SHA)

    def test_13_protected_2026_hard_canon_unchanged(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(blob(ROOT / path), sha)

    def test_14_assembled_counts_and_noncanon_gate(self):
        self.assertEqual(sum(w for _, _, _, w in self.manifest), 166019)
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 24)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 24)
        self.assertIn("NO CANON PROMOTION", self.reader)
        self.assertIn("INDEPENDENT AUTHORS COUNCIL", self.reader)
        self.assertIn("historical 2016 owner identity remains unverified", self.reader.lower())

if __name__ == "__main__":
    unittest.main()
