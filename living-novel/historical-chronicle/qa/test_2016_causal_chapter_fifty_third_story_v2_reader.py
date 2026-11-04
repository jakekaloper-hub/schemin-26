"""Chapter L V2 literature, POV, source locks, and 47-part reader regression."""
import hashlib
import importlib.util
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
QA = Path(__file__).parent
ORIGINAL = "THE_NIGHT_BELOW_THE_ROOM_CHAPTER_50_NONCANON.md"
SCENE = "THE_NIGHT_BELOW_THE_ROOM_THE_THIRD_STORY_CH50_V2_SCENE_NONCANON.md"
CHAPTER = "THE_NIGHT_BELOW_THE_ROOM_THE_THIRD_STORY_CH50_V2_NONCANON.md"
ORIGINAL_SHA = "920d3fda6c9f366d9c56e45745b8db117c8e3fa8"
SCENE_SHA = "16f2de7a87bb2f8452e5f0072bc20f3442716b76"
CHAPTER_SHA = "9cbfdd0db15734cfa25b8e9b7dcb55c4aedc04aa"
PRIOR_WORDS = 355259
TOTAL_WORDS = 363594


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def movements(text):
    return [m.group(1).strip() for m in re.finditer(
        r"(?ms)^### [IVX]+\. [^\n]+\n(.*?)(?=^### [IVX]+\.|^---\n|\Z)", text)]


def module():
    spec = importlib.util.spec_from_file_location(
        "reader_47", QA / "build_2016_causal_47_part_third_story_reader.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class ChapterLThirdStory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old_bytes = (BASE / ORIGINAL).read_bytes()
        cls.scene_bytes = (BASE / SCENE).read_bytes()
        cls.new_bytes = (BASE / CHAPTER).read_bytes()
        cls.old = cls.old_bytes.decode("utf-8")
        cls.scene = cls.scene_bytes.decode("utf-8")
        cls.new = cls.new_bytes.decode("utf-8")
        cls.builder = module()
        cls.prior = cls.builder.prior_reader()
        cls.reader = cls.builder.build_from_repo()

    def test_01_original_source_is_pinned(self):
        self.assertEqual(blob(self.old_bytes), ORIGINAL_SHA)

    def test_02_new_scene_is_pinned(self):
        self.assertEqual(blob(self.scene_bytes), SCENE_SHA)

    def test_03_new_chapter_is_pinned(self):
        self.assertEqual(blob(self.new_bytes), CHAPTER_SHA)

    def test_04_substantial_prose(self):
        self.assertEqual(len(self.scene.split()), 2364)
        self.assertGreaterEqual(len(self.scene.split()), 2000)

    def test_05_chapter_word_count(self):
        self.assertEqual(len(self.old.split()), 5637)
        self.assertEqual(len(self.new.split()), 8335)

    def test_06_seven_roman_numbered_movements(self):
        self.assertEqual(re.findall(r"(?m)^### ([IVX]+)\.", self.new),
                         ["I", "II", "III", "IV", "V", "VI", "VII"])

    def test_07_all_six_original_bodies_exactly_preserved(self):
        old, new = movements(self.old), movements(self.new)
        self.assertEqual(len(old), 6)
        self.assertEqual(len(new), 7)
        self.assertEqual(old, new[:5] + [new[6]])

    def test_08_new_scene_is_embedded_once(self):
        embedded = self.scene.rsplit("\n---", 1)[0].strip()
        self.assertEqual(self.new.count(embedded), 1)

    def test_09_predecessor_has_46_manifest_rows(self):
        rows = self.builder.rows(self.prior)
        self.assertEqual([r[0] for r in rows], list(range(1, 47)))
        self.assertEqual(sum(r[3] for r in rows), PRIOR_WORDS)

    def test_10_new_reader_has_47_source_rows(self):
        rows = self.builder.rows(self.reader)
        self.assertEqual([r[0] for r in rows], list(range(1, 48)))
        self.assertEqual(rows[-1], (47, CHAPTER, CHAPTER_SHA, 8335))
        self.assertEqual(sum(r[3] for r in rows), TOTAL_WORDS)

    def test_11_exact_marker_pairs(self):
        self.assertEqual(self.reader.count(self.builder.BEGIN), 47)
        self.assertEqual(self.reader.count(self.builder.END), 47)
        self.assertEqual(self.reader.count(self.builder.TERMINAL), 1)

    def test_12_previous_46_components_unchanged(self):
        old_body = self.prior[self.prior.index(self.builder.BEGIN):
                              self.prior.index(self.builder.TERMINAL)].rstrip()
        start = f"{self.builder.BEGIN}{CHAPTER} | git_blob {CHAPTER_SHA} -->"
        new_body = self.reader[self.reader.index(self.builder.BEGIN):
                               self.reader.index(start)].rstrip()
        self.assertEqual(old_body, new_body)

    def test_13_revised_chapter_embedded_source_exact(self):
        start = f"{self.builder.BEGIN}{CHAPTER} | git_blob {CHAPTER_SHA} -->"
        end = f"{self.builder.END}{CHAPTER} -->"
        extracted = self.reader.split(start + "\n\n", 1)[1].split("\n\n" + end, 1)[0]
        self.assertEqual(extracted, self.new.rstrip("\n"))

    def test_14_corrupt_new_chapter_fails_closed(self):
        with self.assertRaises(ValueError):
            self.builder.build(self.prior, self.new + "x")

    def test_15_corrupt_predecessor_word_total_fails_closed(self):
        with self.assertRaises(ValueError):
            self.builder.build(self.prior.replace("355259", "999999", 1), self.new)

    def test_16_missing_prior_marker_fails_closed(self):
        with self.assertRaises(ValueError):
            self.builder.build(self.prior.replace(self.builder.BEGIN, "", 1), self.new)

    def test_17_pov_only_approved_owner_limited_interior(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake", self.new)
        for prohibited in ("Edrin", "Edin", "Neris secretly knew",
                           "Tovin privately resolved", "Dovan secretly believed"):
            self.assertNotIn(prohibited, self.scene)

    def test_18_no_invented_score_or_owner_authentication(self):
        for phrase in ("ESPN", "Flaim", "final score", "standings", "playoffs"):
            self.assertNotIn(phrase, self.scene)
        self.assertIn("NOT provider-authenticated", self.new)

    def test_19_archive_historical_source_unchanged(self):
        p = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(blob(p.read_bytes()), "6dbec1fe2537139f3a97c6a78250e2bae082a518")

    def test_20_2026_prologue_and_three_chapters_protected(self):
        protected = {
            "PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
            "CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
            "CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
            "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
        }
        for filename, sha in protected.items():
            with self.subTest(filename=filename):
                self.assertEqual(blob((ROOT / "living-novel/manuscript" / filename).read_bytes()), sha)

    def test_21_traveler_choices_and_continuity(self):
        for phrase in ("I am choosing the night", "I would stay tonight",
                       "one night that is possible", "Hessa", "Dovan", "Neris", "Tovin"):
            self.assertIn(phrase, self.scene)
        self.assertIn("One night", self.old)
        self.assertIn("Ina cleared the dry sorting room.", self.new)

    def test_22_release_gate_stays_closed(self):
        for phrase in ("NONCANON", "INDEPENDENT EDITORIAL HOLD",
                       "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION"):
            self.assertIn(phrase, self.new)
        self.assertNotIn("CANON RELEASE APPROVED", self.new)


if __name__ == "__main__":
    unittest.main()
