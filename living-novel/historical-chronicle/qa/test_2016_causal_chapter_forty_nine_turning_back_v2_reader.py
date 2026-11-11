"""Chapter XLIX V2 original fiction, source/POV locks, and 46-part reader regression."""
import hashlib
import importlib.util
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
QA = Path(__file__).parent
ORIGINAL = "THE_SHORE_THAT_KEPT_NO_FOOTPRINTS_CHAPTER_49_NONCANON.md"
SCENE = "THE_SHORE_THAT_KEPT_NO_FOOTPRINTS_THE_PRICE_OF_TURNING_BACK_CH49_V2_SCENE_NONCANON.md"
CHAPTER = "THE_SHORE_THAT_KEPT_NO_FOOTPRINTS_THE_PRICE_OF_TURNING_BACK_CH49_V2_NONCANON.md"
ORIGINAL_SHA = "a7640f47d11313582cdf137b1ce9bda177536960"
SCENE_SHA = "17ed4d95e8428d40bcabf75f661b2bf7b26f5d86"
CHAPTER_SHA = "584da699eaf7747600142f00cc041551fc5958c3"
PRIOR_WORDS = 347780
TOTAL_WORDS = 355259

def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def movements(text):
    return [m.group(1).strip() for m in re.finditer(r"(?ms)^### [IVX]+\. [^\n]+\n(.*?)(?=^### [IVX]+\.|^---\n|\Z)", text)]

def module():
    spec = importlib.util.spec_from_file_location("reader_46", QA / "build_2016_causal_46_part_turning_back_reader.py")
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

class ChapterXLIXTurningBack(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = (BASE / ORIGINAL).read_text(encoding="utf-8")
        cls.scene = (BASE / SCENE).read_text(encoding="utf-8")
        cls.new = (BASE / CHAPTER).read_text(encoding="utf-8")
        cls.builder = module()
        cls.prior = cls.builder.prior_reader()
        cls.reader = cls.builder.build_from_repo()

    def test_01_source_chapter_pinned(self):
        self.assertEqual(blob((BASE / ORIGINAL).read_bytes()), ORIGINAL_SHA)

    def test_02_scene_blob_pinned(self):
        self.assertEqual(blob((BASE / SCENE).read_bytes()), SCENE_SHA)

    def test_03_revised_chapter_blob_pinned(self):
        self.assertEqual(blob((BASE / CHAPTER).read_bytes()), CHAPTER_SHA)

    def test_04_new_scene_is_substantial_original_prose(self):
        self.assertEqual(len(self.scene.split()), 2108)
        self.assertGreaterEqual(len(self.scene.split()), 2000)

    def test_05_revised_chapter_count(self):
        self.assertEqual(len(self.old.split()), 5253)
        self.assertEqual(len(self.new.split()), 7479)

    def test_06_seven_ordered_movements(self):
        self.assertEqual(re.findall(r"(?m)^### ([IVX]+)\.", self.new),
                         ["I", "II", "III", "IV", "V", "VI", "VII"])

    def test_07_six_original_movement_bodies_preserved(self):
        original = movements(self.old)
        revised = movements(self.new)
        self.assertEqual(len(original), 6)
        self.assertEqual(len(revised), 7)
        self.assertEqual(original, revised[:5] + [revised[6]])

    def test_08_scene_embedded_once(self):
        self.assertEqual(self.new.count(self.scene.strip()), 1)

    def test_09_prior_manifest_45_parts(self):
        rows = self.builder.rows(self.prior)
        self.assertEqual([r[0] for r in rows], list(range(1, 46)))
        self.assertEqual(sum(r[3] for r in rows), PRIOR_WORDS)

    def test_10_reader_46_part_manifest(self):
        rows = self.builder.rows(self.reader)
        self.assertEqual([r[0] for r in rows], list(range(1, 47)))
        self.assertEqual(rows[-1], (46, CHAPTER, CHAPTER_SHA, 7479))
        self.assertEqual(sum(r[3] for r in rows), TOTAL_WORDS)

    def test_11_46_marker_pairs(self):
        self.assertEqual(self.reader.count(self.builder.BEGIN), 46)
        self.assertEqual(self.reader.count(self.builder.END), 46)
        self.assertEqual(self.reader.count(self.builder.TERMINAL), 1)

    def test_12_preceding_45_sections_unchanged(self):
        prior_body = self.prior[self.prior.index(self.builder.BEGIN):self.prior.index(self.builder.TERMINAL)].rstrip()
        start = f"{self.builder.BEGIN}{CHAPTER} | git_blob {CHAPTER_SHA} -->"
        assembled_body = self.reader[self.reader.index(self.builder.BEGIN):self.reader.index(start)].rstrip()
        self.assertEqual(prior_body, assembled_body)

    def test_13_chapter_embedded_byte_exact(self):
        start = f"{self.builder.BEGIN}{CHAPTER} | git_blob {CHAPTER_SHA} -->"
        end = f"{self.builder.END}{CHAPTER} -->"
        self.assertEqual(self.reader.split(start + "\n\n", 1)[1].split("\n\n" + end, 1)[0], self.new.rstrip("\n"))

    def test_14_source_mutation_fails_closed(self):
        with self.assertRaises(ValueError):
            self.builder.build(self.prior, self.new + "x")

    def test_15_corrupt_predecessor_word_count_fails_closed(self):
        with self.assertRaises(ValueError):
            self.builder.build(self.prior.replace("347780", "999999", 1), self.new)

    def test_16_missing_predecessor_marker_fails_closed(self):
        with self.assertRaises(ValueError):
            self.builder.build(self.prior.replace(self.builder.BEGIN, "", 1), self.new)

    def test_17_only_proposed_canonical_jake_interior(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.new)
        for prohibited in ("Edrin", "Edin", "the cart woman secretly knew", "Hessa secretly believed"):
            self.assertNotIn(prohibited, self.scene)

    def test_18_no_invented_esports_score_or_history(self):
        for phrase in ("ESPN", "Flaim", "final score", "standings", "playoffs"):
            self.assertNotIn(phrase, self.scene)
        self.assertIn("NOT provider-authenticated", self.new)

    def test_19_2016_historical_archive_pinned(self):
        archive = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(blob(archive.read_bytes()), "6dbec1fe2537139f3a97c6a78250e2bae082a518")

    def test_20_protected_2026_canon_pinned(self):
        protected = {
         "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
         "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
         "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
         "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
        }
        for name, sha in protected.items():
            with self.subTest(name=name):
                self.assertEqual(blob((ROOT / "living-novel/manuscript" / name).read_bytes()), sha)

    def test_21_boy_boot_bargain_and_jake_debt_remain_distinct(self):
        for phrase in ("I don't hire boots", "What if he pays you in work?", "Pell", "Four coins", "The boy", "Hessa"):
            self.assertIn(phrase, self.scene)
        self.assertIn("Hessa's sister and the eight others had not been found.", self.new)

    def test_22_explicit_noncanonical_release_holds(self):
        for phrase in ("NONCANON", "INDEPENDENT EDITORIAL HOLD", "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            self.assertIn(phrase, self.new)
        self.assertNotIn("CANON RELEASE APPROVED", self.new)

if __name__ == "__main__":
    unittest.main()
