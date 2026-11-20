"""Chapter XLII source-exact, exclusivity, preservation, and consequential-artifact checks.

Author-side regressions only. Successful tests cannot substitute for independent approval.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CHAPTER = "THE_STAGE_BENEATH_THE_SHORT_AWNING_CHAPTER_42_NONCANON.md"
READER = "READING_COPY_CAUSAL_CHAPTERS_01_42_NONCANON.md"
PREVIOUS = "READING_COPY_CAUSAL_CHAPTERS_01_41_NONCANON.md"
CHAPTER_SHA = "6294ffee1d478a493091a532451cdbb9f867f917"
READER_SHA = "92b280d66d5be876411bfa35f9f6b45e319d5519"
PREVIOUS_SHA = "14ce93a324f62cf00307625c486bdbc17e4dd5f4"
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

def rows(text):
    return [(int(n), name, sha, int(words)) for n, name, sha, words in re.findall(
        r"^\| (\d+) \| `([^`]+)` \| `([0-9a-f]{40})` \| (\d+) \|$", text, re.M)]

def extract(reader, name, sha):
    start = f"<!-- BEGIN 2016_CAUSAL {name} | git_blob {sha} -->"
    end = f"<!-- END 2016_CAUSAL {name} -->"
    assert reader.count(start) == reader.count(end) == 1
    return reader.split(start, 1)[1].split(end, 1)[0].strip()

class FortyTwoChapterReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CHAPTER).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.previous = (BASE / PREVIOUS).read_text()
        cls.manifest = rows(cls.reader)
        cls.prior_manifest = rows(cls.previous)
        cls.prose = cls.chapter.split("### I.", 1)[1].split("\n---\n", 1)[0]

    def test_01_manifest_order_and_current_word_count(self):
        self.assertEqual([n for n, *_ in self.manifest], list(range(1, 43)))
        self.assertEqual(self.manifest[-1], (42, CHAPTER, CHAPTER_SHA, 8180))

    def test_02_reader_has_exactly_42_begin_and_end_markers(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 42)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 42)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_03_all_42_source_texts_exact(self):
        for number, name, sha, words in self.manifest:
            with self.subTest(chapter=number):
                source = (BASE / name).read_text()
                self.assertEqual(extract(self.reader, name, sha), source.strip())
                self.assertEqual(len(source.split()), words)

    def test_04_all_42_git_blobs_match_manifest(self):
        for number, name, sha, _ in self.manifest:
            with self.subTest(chapter=number):
                self.assertEqual(git_blob(BASE / name), sha)

    def test_05_prior_reader_frozen_and_embedded_sources_unchanged(self):
        self.assertEqual(git_blob(BASE / PREVIOUS), PREVIOUS_SHA)
        self.assertEqual(self.manifest[:41], self.prior_manifest)
        for n, name, sha, _ in self.prior_manifest:
            with self.subTest(chapter=n):
                self.assertEqual(extract(self.reader, name, sha), extract(self.previous, name, sha))

    def test_06_new_reader_and_chapter_pinned(self):
        self.assertEqual(git_blob(BASE / READER), READER_SHA)
        self.assertEqual(git_blob(BASE / CHAPTER), CHAPTER_SHA)

    def test_07_substantial_six_movement_fiction_not_outline(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\.", self.chapter, re.M)), 6)
        self.assertGreaterEqual(len(self.chapter.split()), 8000)
        self.assertGreaterEqual(len(self.reader.split()), 245000)
        self.assertGreater(len(self.prose.split()), 7000)

    def test_08_one_permitted_interior_focalizer_only(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.chapter)
        self.assertIn("CHAR-JAKE-KALOPER", self.chapter)
        self.assertNotRegex(self.prose, r"\b(?:Edrin|Edin)\b")

    def test_09_continuity_from_41(self):
        for token in ("Sela", "Hessa", "Ina", "apprentice", "six", "twenty-one-night",
                      "cart", "donkey", "awing", "red sky"):
            if token == "awing":
                token = "awning"
            self.assertIn(token, self.chapter)

    def test_10_new_nonprocedural_artistic_conflict(self):
        for token in ("Nella", "Tam", "Meric", "Eren", "king", "turnips",
                      "red sky", "three stones", "upright board"):
            self.assertIn(token, self.prose)

    def test_11_merics_separation_not_undoing_ina_departure(self):
        self.assertIn("I'm leaving the shop", self.prose)
        self.assertIn("two unfinished orders", self.chapter)
        self.assertIn("Tomorrow is a separate agreement", self.prose)

    def test_12_no_exploitative_contract_for_children(self):
        self.assertIn("Nor in a child playing without being hired", self.prose)
        self.assertIn("I'm the person telling it", self.prose)

    def test_13_fictitious_fire_never_promoted_to_fact(self):
        self.assertIn("I have never seen the fire", self.prose)
        self.assertIn("this red is a guess", self.prose)
        self.assertNotIn("the distant fire was extinguished", self.prose)

    def test_14_water_and_shelter_not_declared_safe(self):
        self.assertIn("I cannot tell you whether the track's water is sound", self.prose)
        self.assertNotIn("certified safe", self.prose)
        self.assertIn("no public refuge is created", self.chapter.lower())

    def test_15_unresolved_inherited_lore_loops_persist(self):
        for marker in ("Hessa's missing sister", "second horse", "Esi's letter",
                       "escaped bird", "kiln passage", "eight departed"):
            self.assertIn(marker, self.chapter)

    def test_16_no_competitive_facts_in_prose(self):
        self.assertNotIn("ESPN", self.prose)
        self.assertNotIn("Flaim", self.prose)
        self.assertNotRegex(self.prose, r"\b(?:Week [0-9]+|playoff|championship)\b")

    def test_17_protected_2026_main_manuscript_blobs(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), sha)

    def test_18_historical_2016_evidence_archive_preserved(self):
        f = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(git_blob(f), ARCHIVE_SHA)

    def test_19_no_canon_or_merge_promotion(self):
        self.assertTrue(self.chapter.startswith("# The Stage Beneath the Short Awning"))
        self.assertTrue(self.reader.startswith("# 2016 Commonwealth — Causal Novel Reading Copy, Chapters I–XLII"))
        for token in ("NONCANON / INDEPENDENT EDITORIAL HOLD", "UNAUTHENTICATED",
                      "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            self.assertIn(token, self.chapter)

    def test_20_reader_maintains_editorial_boundary(self):
        self.assertIn("independent Authors Council/Umpire review", self.reader)
        self.assertIn("Neither the official 2016 Historical Chronicle nor protected", self.reader)
        self.assertEqual(self.reader.count("<!-- END_CAUSAL_READING_COPY -->"), 1)

    def test_21_meric_name_not_previous_tavin_identity(self):
        self.assertIn("Meric", self.prose)
        self.assertNotIn("Tavin", self.prose)

if __name__ == "__main__":
    unittest.main()
