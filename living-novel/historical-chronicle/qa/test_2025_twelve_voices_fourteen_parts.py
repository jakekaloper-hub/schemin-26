"""2025 fourteen-part source-exact noncanonical historical reader.

Mechanical integrity checks, NOT independent author review, period Atlas
approval, historical manager identity verification or canon acceptance.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2025/causal-novel"
OLD = BASE / "READING_COPY_2025_TWELVE_VOICES_THIRTEEN_PARTS_NONCANON.md"
NEW = BASE / "READING_COPY_2025_TWELVE_VOICES_FOURTEEN_PARTS_NONCANON.md"
CHAPTER = BASE / "THE_ROOM_WITHOUT_A_STAGE_AUSTIN_PHILLIP_2025_NONCANON.md"
PILOT = ROOT / "living-novel/production/historical-saga/R53/HISTORICAL_2025_OBIWAN_NONCANON_PILOT.md"
PRIOR_2016 = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel/READING_COPY_CAUSAL_CHAPTERS_01_72_NONCANON.md"
EVIDENCE = ROOT / "living-novel/historical-chronicle/evidence/2025_FLAIM_TEAM_SLOT_AND_PODIUM_READBACK_2026-11-01_REVIEW_ONLY.md"
HISTORY = ROOT / "living-novel/history/PLAYOFF_MATCHUP_EVIDENCE_2022_2025.json"
WRAPPER = re.compile(r"<!-- BEGIN 2025_VOICE ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n([\s\S]*?)\n\n<!-- END 2025_VOICE ([^\n]+) -->")
OLD_BLOB = "9237ec57f7dc45c13a726bcdf2369788dcae0de4"
CHAPTER_BLOB = "feb66c8f68d83aa9c9b4b6c2e6e7cc755103b116"
PRIOR_2016_BLOB = "8f1dda21ac4962143ba3291cef4d60769197d62f"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def source_path(filename):
    return PILOT if filename == PILOT.name else BASE / filename

class TwelveOwnerFourteenPartReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = OLD.read_text(encoding="utf-8")
        cls.reader = NEW.read_text(encoding="utf-8")
        cls.chapter = CHAPTER.read_text(encoding="utf-8")
        cls.old_parts = list(WRAPPER.finditer(cls.old))
        cls.parts = list(WRAPPER.finditer(cls.reader))
        cls.scene = cls.chapter.split("\n---\n\n### Source, continuity, and editorial handoff", 1)[0]
        cls.evidence = EVIDENCE.read_text(encoding="utf-8")

    def test_01_previous_reader_exact_git_blob(self):
        self.assertEqual(git_blob(OLD), OLD_BLOB)

    def test_02_new_chapter_exact_git_blob(self):
        self.assertEqual(git_blob(CHAPTER), CHAPTER_BLOB)

    def test_03_thirteen_plus_one_wrappers(self):
        self.assertEqual(len(self.old_parts), 13)
        self.assertEqual(len(self.parts), 14)

    def test_04_previous_thirteen_wrappers_byte_exact(self):
        for index, part in enumerate(self.old_parts):
            with self.subTest(part=index + 1):
                self.assertEqual(part.group(0), self.parts[index].group(0))

    def test_05_new_wrapper_source_and_content(self):
        p = self.parts[-1]
        self.assertEqual(p.group(1), CHAPTER.name)
        self.assertEqual(p.group(2), CHAPTER_BLOB)
        self.assertEqual(p.group(3), self.chapter.rstrip("\n"))
        self.assertEqual(p.group(4), CHAPTER.name)

    def test_06_all_fourteen_embedded_sources_match_disk(self):
        for p in self.parts:
            f = source_path(p.group(1))
            with self.subTest(source=f.name):
                self.assertTrue(f.is_file())
                self.assertEqual(git_blob(f), p.group(2))
                self.assertEqual(f.read_text(encoding="utf-8").rstrip("\n"), p.group(3))

    def test_07_source_word_sum(self):
        self.assertEqual(sum(len(source_path(p.group(1)).read_text(encoding="utf-8").split()) for p in self.parts), 70213)

    def test_08_new_chapter_word_count(self):
        self.assertEqual(len(self.chapter.split()), 4770)

    def test_09_reader_declares_correct_manifest_total(self):
        self.assertIn("70213 across 14 chapter sources", self.reader)

    def test_10_manifest_has_ordered_fourteen(self):
        m = self.reader.split("## Source-exact manifest\n", 1)[1].split("\n---\n", 1)[0]
        self.assertEqual(re.findall(r"^\| (\d+) \|", m, re.M), [str(i) for i in range(1, 15)])

    def test_11_twelve_unique_registered_pov_ids(self):
        rows = re.findall(r"^\| \d+ \| ([^\n]+)", self.reader, re.M)
        ids = [re.findall(r"CHAR-[A-Z-]+", row.split(" | ")[0]) for row in rows]
        self.assertEqual(len(ids), 14)
        unique = {v for row in ids for v in row}
        self.assertEqual(len(unique), 12)
        self.assertEqual(ids[-1], ["CHAR-AUSTIN-BYARS", "CHAR-PHILLIP-PITTS"])
        reg = (ROOT / "canon/characters/CHARACTER_REGISTRY.yaml").read_text(encoding="utf-8")
        for id_ in unique:
            self.assertIn("id: " + id_, reg)

    def test_12_four_movement_pov_sequence(self):
        movement = re.findall(r"^### ([IVX]+)\. ([^\n]+) — ([^\n]+)$", self.scene, re.M)
        self.assertEqual([m[0] for m in movement], ["I", "II", "III", "IV"])
        self.assertEqual([m[2] for m in movement], ["Austin", "Phillip", "Austin", "Phillip"])

    def test_13_substantial_narrative_not_just_handoff(self):
        self.assertGreater(len(self.scene.split()), 4200)

    def test_14_exclusive_principal_pov_and_no_retired_narrator(self):
        self.assertIn("Two and only two registered owner-character limited viewpoints", self.chapter)
        self.assertIsNone(re.search(r"\b(?:Edrin|Edin|Oren)\b", self.scene))

    def test_15_phillip_is_single_three_headed_character(self):
        self.assertIn("one-bodied three-headed", self.chapter)
        self.assertIn("a single unwillingness", self.scene)
        self.assertIn("not a debate among three judges", self.scene)

    def test_16_belt_held_only_by_austin(self):
        self.assertIn("championship Belt", self.chapter)
        self.assertIn("the Belt", self.scene)
        self.assertIn("Austin", self.scene)
        self.assertNotIn("Jake put on the Belt", self.scene)

    def test_17_historical_standings_are_season_correct(self):
        self.assertIn("| 6 | Three Dreaded Snake | 10–4 | 3 | eliminated |", self.evidence)
        self.assertIn("| 8 | The Immortal | 9–5 | 1 | champion |", self.evidence)
        self.assertTrue(HISTORY.is_file())

    def test_18_only_verified_bracket_anchors(self):
        self.assertIn("one hundred fifty-three and twenty hundredths", self.scene)
        self.assertIn("one hundred seventy-four and thirty-eight hundredths", self.scene)
        self.assertIn("one hundred nine and fifty-six hundredths", self.scene)
        self.assertIn("one hundred sixty-one and seven hundredths", self.scene)

    def test_19_provisional_historical_owner_attribution(self):
        self.assertIn("do not authenticate historical human account owners", self.chapter)
        self.assertIn("remains provisional", self.chapter)

    def test_20_shelter_promise_not_retconned(self):
        self.assertIn("Thirty-six sleeping places", self.scene)
        self.assertIn("The first night's lodging had been accounted for", self.scene)
        self.assertIn("*subsequent unspecified night*", self.chapter)

    def test_21_mask_and_chair_continuity(self):
        for phrase in ("thirteenth mask", "shorter third-place chair", "The new handle held"):
            self.assertIn(phrase, self.scene)

    def test_22_not_a_free_unlimited_shelter_or_accepted_route(self):
        self.assertIn("second night as a separate household expense", self.scene)
        self.assertIn("does **not** establish a period Atlas route", self.chapter)

    def test_23_authors_self_review_not_independent(self):
        self.assertIn("producer self-critique, not independent review", self.chapter)
        self.assertIn("independent Umpire acceptance are unverified", self.chapter)

    def test_24_no_canon_merge_publishing(self):
        for phrase in ("DRAFT / NONCANON", "NO MERGE", "NO CANON PROMOTION", "NO PUBLICATION", "FOUNDER-ONLY"):
            self.assertIn(phrase, self.chapter)

    def test_25_2026_hard_opening_untouched(self):
        for p, sha in PROTECTED.items():
            with self.subTest(path=p):
                self.assertEqual(git_blob(ROOT / p), sha)

    def test_26_2016_causal_reader_untouched(self):
        self.assertEqual(git_blob(PRIOR_2016), PRIOR_2016_BLOB)

    def test_27_previous_reader_still_has_original_terminal(self):
        self.assertTrue(self.old.rstrip().endswith("<!-- END_2025_TWELVE_VOICES_THIRTEEN_PARTS_NONCANON -->"))

    def test_28_new_reader_has_distinct_terminal(self):
        self.assertTrue(self.reader.rstrip().endswith("<!-- END_2025_TWELVE_VOICES_FOURTEEN_PARTS_NONCANON -->"))

    def test_29_fourteenth_part_is_preserved_as_source_not_autocanon(self):
        self.assertIn("not a developmentally accepted or fully temporally aligned novel", self.reader)
        self.assertIn("INDEPENDENT AUTHORS COUNCIL AND UMPIRE HOLD", self.reader)

    def test_30_previous_thirteen_chapter_order_preserved(self):
        self.assertEqual([x.group(1) for x in self.old_parts], [x.group(1) for x in self.parts[:-1]])

if __name__ == "__main__":
    unittest.main()
