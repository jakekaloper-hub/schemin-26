"""Chapter XXV NONCANON source-exact reader integrity and physical-departure regressions.
Invoked by the existing Novel OS CI historical chapter reader discovery step.
Mechanical verification only, NOT independent Author Council/Atlas/Umpire acceptance.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_MILE_BEYOND_THE_WEIGH_STONES_CHAPTER_25_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_25_NONCANON.md"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_01_24_NONCANON.md"
CHAPTER_SHA = "90de3e31f6b729ca33636c74551caf9865a84256"
READER_SHA = "7e2bd8b000523441785eacf34bb741f58530b5f1"
PREVIOUS_SHA = "a05be29bb470c9b27c3a2c33469fe3ee79249931"
HISTORICAL_ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23aeb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\\0" + data).hexdigest()

def rows(doc):
    return [(int(n), name, sha, int(words)) for n,name,sha,words in re.findall(
        r"^\\| (\\d+) \\| \\x60([^\\x60]+)\\x60 \\| \\x60([a-f0-9]{40})\\x60 \\| (\\d+) \\|$", doc, re.M)]

def passage(doc, name, sha):
    start = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    end = f"<!-- END 2016_CAUSAL {name} -->"
    assert doc.count(start) == 1 and doc.count(end) == 1, name
    return doc.split(start, 1)[1].split(end, 1)[0].strip()

class TwentyFiveChapterReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text(encoding="utf-8")
        cls.reader = (BASE / READER).read_text(encoding="utf-8")
        cls.old = (BASE / PREVIOUS).read_text(encoding="utf-8")
        cls.manifest = rows(cls.reader)
        cls.old_manifest = rows(cls.old)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\\n---\\n", 1)[0]

    def test_01_manifest_is_ordered_and_source_marked(self):
        self.assertEqual([row[0] for row in self.manifest], list(range(1, 26)))
        self.assertEqual(self.manifest[-1][1:], (CHAPTER, CHAPTER_SHA, len(self.chapter.split())))
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 25)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 25)

    def test_02_source_exact_assembly_of_all_25(self):
        for n, name, sha, words in self.manifest:
            with self.subTest(chapter=n):
                src = (BASE / name).read_text(encoding="utf-8")
                self.assertEqual(passage(self.reader, name, sha), src.strip())
                self.assertEqual(len(src.split()), words)

    def test_03_manifest_blobs_match_source_bytes(self):
        for n, name, sha, _ in self.manifest:
            with self.subTest(chapter=n):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_04_prior_reader_remains_immutable(self):
        self.assertEqual(git_blob(BASE / PREVIOUS), PREVIOUS_SHA)
        self.assertEqual(self.old_manifest, self.manifest[:24])

    def test_05_all_24_previous_passages_are_unchanged(self):
        for n, name, sha, _ in self.old_manifest:
            with self.subTest(chapter=n):
                self.assertEqual(passage(self.reader, name, sha), passage(self.old, name, sha))

    def test_06_substantial_five_movement_fiction_and_handoff(self):
        self.assertGreaterEqual(len(self.chapter.split()), 5500)
        self.assertEqual(len(re.findall(r"^### [IVX]+\\.", self.chapter, re.M)), 5)
        self.assertIn("### Editorial handoff", self.chapter)
        self.assertIn("The Mile Beyond the Weigh-Stones", self.chapter)

    def test_07_exclusive_owner_pov_and_real_world_firewall(self):
        self.assertIn("Sole limited interior viewpoint", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER / PRINCIPAL_CHARACTER", self.chapter)
        self.assertIn("NOT an authenticated historical ESPN owner-slot association", self.chapter)
        for name in ("Edrin", "Edin", "Oren"):
            self.assertNotIn(name, self.prose)

    def test_08_departure_and_real_arrival_are_observed(self):
        for phrase in ("The weigh-stones began to slip backward",
                       "They reached the outer yard in dusk",
                       "You took the season", "No hours had been entered",
                       "He had left"):
            self.assertIn(phrase, self.prose)

    def test_09_wage_and_transport_costs_not_invented_as_paid_employment(self):
        for phrase in ("Jake paid it from what remained", "No one had offered him road wages",
                       "no new paid work hours or wages are awarded",
                       "the kiln passage is temporarily closed"):
            self.assertIn(phrase, self.chapter)

    def test_10_other_people_complete_independent_work(self):
        for phrase in ("The daughter rolled her cord and walked away",
                       "She named it", "The driver paid the rest",
                       "the younger porter", "Esi and the young porter"):
            self.assertIn(phrase, self.chapter)

    def test_11_unrelated_sola_and_clog_not_conflated(self):
        self.assertIn("Sola had taken both of her own clogs", self.prose)
        self.assertIn("The third leaf of the screen was still unbought", self.prose)
        self.assertIn("The unknown clog remained at the shelter", self.prose)

    def test_12_private_claimant_and_missing_ledger_remain_open(self):
        self.assertIn("The ledger's missing leaves and the thief's identity were still unknown", self.prose)
        self.assertIn("The private claimant file and the separate sealed message had not been opened", self.prose)
        self.assertIn("the suspected cover might already have left the west store", self.prose)

    def test_13_retained_historical_archive_byte_fingerprint(self):
        archive = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(git_blob(archive), HISTORICAL_ARCHIVE_SHA)

    def test_14_protected_hard_manuscripts_byte_fingerprints(self):
        for path, expected in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), expected)

    def test_15_complete_reader_markers_and_release_hold(self):
        self.assertEqual(git_blob(BASE / CHAPTER), CHAPTER_SHA)
        self.assertEqual(git_blob(BASE / READER), READER_SHA)
        self.assertGreaterEqual(len(self.reader.split()), 134000)
        self.assertIn("Twenty-five fully assembled", self.reader)
        self.assertIn("<!-- END_CAUSAL_READING_COPY -->", self.reader)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)
        self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD", self.chapter)
        self.assertIn("no founder-only promotion, merge or publication", self.chapter.lower())

if __name__ == "__main__":
    unittest.main()
