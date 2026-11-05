"""2025 fifteen-part source-exact, twelve-owner proposed historical reader.

Deterministic source/POV/continuity tests. These DO NOT verify historical
manager accounts, period Atlas geography, literary quality or Umpire approval.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2025/causal-novel"
OLD = BASE / "READING_COPY_2025_TWELVE_VOICES_FOURTEEN_PARTS_NONCANON.md"
NEW = BASE / "READING_COPY_2025_TWELVE_VOICES_FIFTEEN_PARTS_NONCANON.md"
CHAPTER = BASE / "THE_DAY_THE_POT_WENT_COLD_BEN_DAVID_2025_NONCANON.md"
PILOT = ROOT / "living-novel/production/historical-saga/R53/HISTORICAL_2025_OBIWAN_NONCANON_PILOT.md"
PRIOR_2016 = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel/READING_COPY_CAUSAL_CHAPTERS_01_72_NONCANON.md"
EVIDENCE = ROOT / "living-novel/historical-chronicle/evidence/2025_FLAIM_TEAM_SLOT_AND_PODIUM_READBACK_2026-11-01_REVIEW_ONLY.md"
WRAPPER = re.compile(
    r"<!-- BEGIN 2025_VOICE ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n"
    r"([\s\S]*?)\n\n<!-- END 2025_VOICE ([^\n]+) -->"
)
OLD_BLOB = "e36aba8693804e77a0db5dde57172f3d17658f43"
CHAPTER_BLOB = "862d0a9dab9a546a1e110fbc45c474d174b127c3"
PRIOR_2016_BLOB = "8f1dda21ac4962143ba3291cef4d60769197d62f"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def source_path(name: str) -> Path:
    return PILOT if name == PILOT.name else BASE / name

class TwelveOwnerFifteenPartReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old = OLD.read_text(encoding="utf-8")
        cls.reader = NEW.read_text(encoding="utf-8")
        cls.chapter = CHAPTER.read_text(encoding="utf-8")
        cls.old_parts = list(WRAPPER.finditer(cls.old))
        cls.parts = list(WRAPPER.finditer(cls.reader))
        cls.scene = cls.chapter.split("\n---\n\n### Source and editorial handoff", 1)[0]
        cls.evidence = EVIDENCE.read_text(encoding="utf-8")

    def test_01_preserves_prior_reader_blob(self):
        self.assertEqual(git_blob(OLD), OLD_BLOB)

    def test_02_new_source_pinned(self):
        self.assertEqual(git_blob(CHAPTER), CHAPTER_BLOB)

    def test_03_fifteen_wrappers_and_fourteen_predecessors(self):
        self.assertEqual((len(self.old_parts), len(self.parts)), (14, 15))

    def test_04_existing_fourteen_wrappers_source_exact(self):
        for i, p in enumerate(self.old_parts):
            with self.subTest(part=i+1):
                self.assertEqual(p.group(0), self.parts[i].group(0))

    def test_05_new_wrapper_matches_chapter_bytes(self):
        p = self.parts[-1]
        self.assertEqual(p.group(1), CHAPTER.name)
        self.assertEqual(p.group(2), CHAPTER_BLOB)
        self.assertEqual(p.group(3), self.chapter.rstrip("\n"))
        self.assertEqual(p.group(4), CHAPTER.name)

    def test_06_every_wrapped_source_matches_on_disk(self):
        for p in self.parts:
            f = source_path(p.group(1))
            with self.subTest(source=f.name):
                self.assertTrue(f.is_file())
                self.assertEqual(git_blob(f), p.group(2))
                self.assertEqual(f.read_text(encoding="utf-8").rstrip("\n"), p.group(3))

    def test_07_words_sum_to_source_manifest(self):
        self.assertEqual(sum(len(source_path(p.group(1)).read_text(encoding="utf-8").split()) for p in self.parts), 76132)

    def test_08_new_chapter_words_counted_including_handoff(self):
        self.assertEqual(len(self.chapter.split()), 5919)

    def test_09_manifest_explicit_about_editorial_metadata(self):
        self.assertIn("76132 across 15 chapter sources", self.reader)
        self.assertIn("including chapter metadata", self.reader)

    def test_10_manifest_order_fifteen(self):
        m = self.reader.split("## Source-exact manifest\n", 1)[1].split("\n---\n", 1)[0]
        self.assertEqual(re.findall(r"^\| (\d+) \|", m, re.M), [str(i) for i in range(1, 16)])

    def test_11_unique_pov_owner_ids_remain_twelve(self):
        m = self.reader.split("## Source-exact manifest\n", 1)[1].split("\n---\n", 1)[0]
        rows = re.findall(r"^\| \d+ \| ([^\n]+)", m, re.M)
        ids = [re.findall(r"CHAR-[A-Z-]+", row.split(" | ")[0]) for row in rows]
        self.assertEqual(len(ids), 15)
        self.assertEqual(len({x for group in ids for x in group}), 12)
        self.assertEqual(ids[-1], ["CHAR-BEN-WHIPPLE", "CHAR-DAVID-BABB"])

    def test_12_six_movements_alternating_limited_pov(self):
        moves = re.findall(r"^### ([IVX]+)\. ([^\n]+) — (Ben|David)$", self.scene, re.M)
        self.assertEqual([m[0] for m in moves], ["I", "II", "III", "IV", "V", "VI"])
        self.assertEqual([m[2] for m in moves], ["Ben", "David", "Ben", "David", "Ben", "David"])

    def test_13_substantial_new_prose(self):
        self.assertGreater(len(self.scene.split()), 5000)

    def test_14_no_extra_interior_owner_or_retired_pov(self):
        self.assertIsNone(re.search(r"\b(?:Edrin|Edin|Oren)\b", self.scene))
        self.assertIn("Only Ben and David possess interior viewpoint", self.chapter)

    def test_15_prior_six_stewards_vote_four_to_two_acknowledged(self):
        self.assertIn("four-to-two serving rule", self.chapter)
        self.assertIn("Four admitted the worker-elected candidate", self.scene)

    def test_16_worker_election_and_seventh_steward_not_a_gift(self):
        self.assertIn("Tessa refused to let the stewards appoint her", self.scene)
        self.assertIn("Tessa had been chosen by a majority of the eleven", self.scene)

    def test_17_new_vote_has_consequential_opposition(self):
        self.assertIn("Three favored it. Four opposed.", self.scene)
        self.assertIn("Tessa was among the four.", self.scene)

    def test_18_narrower_countermotion_passes(self):
        self.assertIn("The amended motion carried five to two.", self.scene)
        self.assertIn("The unserved would be counted publicly", self.scene)

    def test_19_old_priority_not_retconned(self):
        self.assertIn("The original serving priority had not been rewritten", self.scene)

    def test_20_partial_pell_contract_kept_distinct_from_kevin_gift(self):
        self.assertIn("The gift did not complete Pell's sale.", self.scene)
        self.assertIn("accepted partial load", self.chapter)

    def test_21_david_payment_occurs_for_accepted_quantity(self):
        self.assertIn("The first actual transfer from David's pledged reserve", self.scene)
        self.assertIn("FULLY DISCHARGED", self.scene)

    def test_22_future_pledges_not_counted_as_existing_grain(self):
        self.assertIn("EXPECTED BUT NOT COMMITTED", self.scene)
        self.assertIn("they had never arrived", self.scene)

    def test_23_no_grain_or_food_made_from_votes(self):
        self.assertIn("Will it make more supper?", self.scene)
        self.assertIn("The two missing grain pledges did not reappear.", self.scene)

    def test_24_human_owner_account_bridge_stays_unknown(self):
        self.assertIn("do not independently verify the human managers", self.chapter)
        self.assertTrue(EVIDENCE.is_file())
        self.assertIn("Seven Deadly Chins", self.evidence)
        self.assertIn("The LLC", self.evidence)

    def test_25_noncannon_review_holds_stated(self):
        self.assertIn("DRAFT / NONCANON", self.chapter)
        self.assertIn("No merge, canon promotion, publication", self.chapter)
        self.assertIn("Critical independent editorial challenges", self.chapter)

    def test_26_protected_2026_hard_opening_unchanged(self):
        for p, sha in PROTECTED.items():
            with self.subTest(path=p):
                self.assertEqual(git_blob(ROOT / p), sha)

    def test_27_2016_source_preserved(self):
        self.assertEqual(git_blob(PRIOR_2016), PRIOR_2016_BLOB)

    def test_28_distinct_terminal_edition_markers(self):
        self.assertTrue(self.old.rstrip().endswith("<!-- END_2025_TWELVE_VOICES_FOURTEEN_PARTS_NONCANON -->"))
        self.assertTrue(self.reader.rstrip().endswith("<!-- END_2025_TWELVE_VOICES_FIFTEEN_PARTS_NONCANON -->"))

    def test_29_no_revision_of_protected_old_edition(self):
        self.assertIn("standalone fourteen-part edition remains unchanged", self.reader)
        self.assertIn("not a developmentally accepted or fully temporally aligned novel", self.reader)

    def test_30_source_part_order_exact(self):
        self.assertEqual([p.group(1) for p in self.old_parts], [p.group(1) for p in self.parts[:-1]])

if __name__ == "__main__":
    unittest.main()
