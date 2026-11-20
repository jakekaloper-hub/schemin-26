"""Chapter XL: noncanonical source-exact 2016 reader and historical/canon negative locks."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_HOUSE_MADE_FROM_A_ROAD_CHAPTER_40_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_40_NONCANON.md"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_01_39_NONCANON.md"
CHAPTER_SHA = "d5a4e6778c705b5f3e655071e04a67892ef22b95"
READER_SHA = "ecc93dfe2100ed68f9aa49e59c0427fc2dbf6295"
PREVIOUS_SHA = "15165b0e6e98f1a0d274a02fa2d613ad1ea048ac"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}


def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def manifest_rows(text):
    return [(int(n), name, sha, int(words)) for n, name, sha, words in re.findall(
        r"^\| (\d+) \| `([^`]+)` \| `([a-f0-9]{40})` \| (\d+) \|$", text, re.M)]


def extract(reader, name, sha):
    opening = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    closing = f"<!-- END 2016_CAUSAL {name} -->"
    assert reader.count(opening) == reader.count(closing) == 1
    return reader.split(opening, 1)[1].split(closing, 1)[0].strip()


class FortyChapterReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.previous = (BASE / PREVIOUS).read_text()
        cls.manifest = manifest_rows(cls.reader)
        cls.old_manifest = manifest_rows(cls.previous)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_manifest_exact_40(self):
        self.assertEqual([n for n, *_ in self.manifest], list(range(1, 41)))
        self.assertEqual(self.manifest[-1], (40, CHAPTER, CHAPTER_SHA, len(self.chapter.split())))

    def test_02_reader_has_40_exact_markers(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 40)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 40)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_03_all_40_sections_source_exact(self):
        for n, name, sha, words in self.manifest:
            with self.subTest(chapter=n):
                source = (BASE / name).read_text()
                self.assertEqual(extract(self.reader, name, sha), source.strip())
                self.assertEqual(len(source.split()), words)

    def test_04_git_blob_integrity_all_40(self):
        for n, name, sha, _ in self.manifest:
            with self.subTest(chapter=n):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_05_previous_39_immutable(self):
        self.assertEqual(git_blob(BASE / PREVIOUS), PREVIOUS_SHA)
        self.assertEqual(self.manifest[:39], self.old_manifest)
        for n, name, sha, _ in self.old_manifest:
            with self.subTest(chapter=n):
                self.assertEqual(extract(self.reader, name, sha), extract(self.previous, name, sha))

    def test_06_new_reader_blob_exact(self):
        self.assertEqual(git_blob(BASE / READER), READER_SHA)

    def test_07_six_movement_substantial_novel_prose(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\.", self.chapter, re.M)), 6)
        self.assertGreaterEqual(len(self.chapter.split()), 6000)
        self.assertGreaterEqual(len(self.reader.split()), 229000)

    def test_08_exclusive_allowed_principal_pov(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertNotRegex(self.prose, r"\b(?:Edrin|Edin|Oren)\b")

    def test_09_narrative_turn_changes_housing_and_cart(self):
        for token in ("Twenty-one nights", "one side", "wheels and axle", "apprentice"):
            self.assertIn(token, self.chapter)
        self.assertIn("A room with witnesses", self.prose)

    def test_10_safety_and_historical_nonfinality(self):
        self.assertIn("local water safety remain unverified", self.chapter)
        self.assertNotIn("safe to drink now", self.prose)
        self.assertNotIn("the missing freight was found", self.prose)

    def test_11_old_world_state_still_visible(self):
        for token in ("Fara's inherited awning", "Mael and Pell", "Esi letter",
                      "distant fire", "eight others departed", "kiln passage is closed"):
            self.assertIn(token, self.chapter)

    def test_12_no_unverified_league_facts_in_prose(self):
        self.assertNotIn("ESPN", self.prose)
        self.assertNotIn("Flaim", self.prose)
        self.assertNotRegex(self.prose, r"\b(?:Week [0-9]+|playoff|championship)\b")
        self.assertIn("UNAUTHENTICATED", self.chapter)

    def test_13_protected_hard_canon_blobs(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), sha)

    def test_14_historical_evidence_archive_unchanged(self):
        source = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(git_blob(source), ARCHIVE_SHA)

    def test_15_draft_and_founder_only_hold(self):
        self.assertTrue(self.chapter.startswith("# The House Made from a Road"))
        self.assertTrue(self.reader.startswith("# 2016 Commonwealth — Causal Novel Reading Copy, Chapters I–XL"))
        self.assertIn("NONCANON / INDEPENDENT EDITORIAL HOLD", self.chapter)
        for gate in ("NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            self.assertIn(gate, self.chapter)

    def test_16_agent_choices_not_protagonist_commands(self):
        for token in ("Hessa", "Ina", "Fara", "boat-cover maker", "the apprentice"):
            self.assertIn(token, self.prose)
        self.assertIn("Carry it. Not the decision.", self.prose)

    def test_17_private_shelter_not_new_law(self):
        self.assertIn("not a permanent settlement or legal charter", self.chapter)
        self.assertIn("No official shelter law", self.chapter)
        self.assertIn("a rumor of a refuge", self.prose)


if __name__ == "__main__":
    unittest.main()
