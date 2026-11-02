"""Technical integrity for six-owner 2025 causal reader; NONCANON and release-held.

This is not an independent authors' assessment, ESPΝ human-manager verification,
Atlas acceptance, Umpire approval, or Founder approval. Each historical team
result comes from the source-pinned 2025 ESPN/Flaim evidence readback.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2025/causal-novel"
READER = BASE / "READING_COPY_2025_SIX_VOICES_NONCANON.md"
READER_SHA = "ebf421a75eb35cdc5fd4aedf5bf54104b5442ec3"
SOURCES = (
    ("living-novel/historical-chronicle/seasons/2025/causal-novel/THE_NARROWEST_DOOR_AUSTIN_2025_NONCANON.md", "ae5d50aca6c1ac4da20fb8ead28554baa5e70613", "CHAR-AUSTIN-BYARS", 5001),
    ("living-novel/production/historical-saga/R53/HISTORICAL_2025_OBIWAN_NONCANON_PILOT.md", "9737fa9b9832de847ee504ed9b87d5e2c404e481", "CHAR-JAKE-KALOPER", 983),
    ("living-novel/historical-chronicle/seasons/2025/causal-novel/THE_COURSE_BENEATH_THE_COURSE_ZACH_2025_NONCANON.md", "112b3890173cbf11879b139bff966cdff83884d4", "CHAR-ZACH-WILSON", 5310),
    ("living-novel/historical-chronicle/seasons/2025/causal-novel/THE_MASKS_THAT_REMAINED_PHILLIP_2025_NONCANON.md", "f96832d3bd23840d2fb1853d17940ac54774531d", "CHAR-PHILLIP-PITTS", 4777),
    ("living-novel/historical-chronicle/seasons/2025/causal-novel/THE_SIXTH_PLACE_AT_THE_TABLE_BEN_2025_NONCANON.md", "9a2b618d498ad97a6343366dcc18ddc409041419", "CHAR-BEN-WHIPPLE", 4495),
    ("living-novel/historical-chronicle/seasons/2025/causal-novel/THE_WINTER_CLAUSE_DAVID_2025_NONCANON.md", "0de993d2cb3865a7d37ce8cb8f1a9c719c37253c", "CHAR-DAVID-BABB", 4487),
)
OLD_2025 = BASE / "READING_COPY_2025_FIVE_VOICES_NONCANON.md"
OLD_2025_SHA = "d82f3696959e0c17f5a751f576417ca6b070f409"
OLD_2016 = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel/READING_COPY_CAUSAL_CHAPTERS_01_72_NONCANON.md"
OLD_2016_SHA = "8f1dda21ac4962143ba3291cef4d60769197d62f"
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
MANIFEST = re.compile(
    r"^\| ([1-6]) \| ([^|]+) \| `([^\n]+?)` \| `([0-9a-f]{40})` \| (\d+) \|$", re.M
)


def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


class SixVoicesReaderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = READER.read_text(encoding="utf-8")
        cls.bodies = [(ROOT / p).read_text(encoding="utf-8") for p, _, _, _ in SOURCES]
        cls.david = cls.bodies[-1]
        cls.wrappers = list(WRAPPER.finditer(cls.text))
        cls.manifest = list(MANIFEST.finditer(cls.text))
        cls.evidence = (
            ROOT / "living-novel/historical-chronicle/evidence/2025_FLAIM_TEAM_SLOT_AND_PODIUM_READBACK_2026-11-01_REVIEW_ONLY.md"
        ).read_text(encoding="utf-8")

    def test_01_source_blobs_pinned(self):
        for path, sha, _, _ in SOURCES:
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), sha)

    def test_02_reader_blob_pinned(self):
        self.assertEqual(git_blob(READER), READER_SHA)

    def test_03_six_wrappers(self):
        self.assertEqual(len(self.wrappers), 6)

    def test_04_six_manifest_rows(self):
        self.assertEqual(len(self.manifest), 6)

    def test_05_manifest_path_owner_sha_words(self):
        for i, (path, sha, owner, count) in enumerate(SOURCES):
            row = self.manifest[i]
            self.assertEqual(int(row.group(1)), i + 1)
            self.assertIn(owner, row.group(2))
            self.assertEqual(row.group(3), path)
            self.assertEqual(row.group(4), sha)
            self.assertEqual(int(row.group(5)), count)

    def test_06_embedded_sources_byte_exact_except_final_newlines(self):
        for i, (path, sha, _, _) in enumerate(SOURCES):
            filename, embedded_sha, body, closing = self.wrappers[i].groups()
            self.assertEqual(filename, Path(path).name)
            self.assertEqual(closing, filename)
            self.assertEqual(embedded_sha, sha)
            self.assertEqual(body, self.bodies[i].rstrip("\n"))

    def test_07_source_word_counts_and_sum(self):
        self.assertEqual(sum(int(row.group(5)) for row in self.manifest), 25053)
        for body, (_, _, _, count) in zip(self.bodies, SOURCES):
            self.assertEqual(len(body.split()), count)

    def test_08_distinct_canonical_principal_owner_ids(self):
        self.assertEqual(len({entry[2] for entry in SOURCES}), 6)
        for _, _, owner, _ in SOURCES:
            self.assertIn(owner, self.text)

    def test_09_david_substantial(self):
        self.assertGreaterEqual(len(self.david.split()), 4000)

    def test_10_david_six_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\. ", self.david, re.M)), 6)

    def test_11_david_only_interior(self):
        self.assertIn("Principal and sole interior viewpoint: David Babb", self.david)
        self.assertIn("no additional character receives interior narration", self.david)

    def test_12_no_retired_pov_in_new_narrative(self):
        narrative = self.david.split("\n---\n\n### Source, continuity and production handoff")[0]
        self.assertIsNone(re.search(r"\b(?:Edrin|Edin|Master Oren)\b", narrative, re.I))

    def test_13_provider_team_slot_supported(self):
        self.assertIn("| 4 | The LLC | 4–10 | 10 | missed_playoffs |", self.evidence)

    def test_14_david_team_anchor_exact(self):
        for phrase in ("team slot 4", "The LLC", "4–10", "finalRank 10", "missed the playoffs"):
            self.assertIn(phrase, self.david)

    def test_15_2025_human_manager_identity_stays_unknown(self):
        for phrase in ("Historical human manager-account identity remains UNKNOWN",
                       "PROVISIONAL FICTIONAL ASSOCIATION"):
            self.assertIn(phrase, self.david)

    def test_16_no_unverified_competition_score(self):
        self.assertIsNone(re.search(r"\b\d{2,3}\.\d{2}\b", self.david))

    def test_17_no_future_2026_outcome_claim(self):
        self.assertIn("no 2026 outcome is implied", self.david)
        self.assertIn("no unverified opponent", self.david.lower())

    def test_18_ben_outcome_still_enters_david_scene(self):
        for phrase in ("Four had voted", "Two had opposed", "seventh place was empty",
                       "the old serving rule"):
            self.assertIn(phrase, self.david)

    def test_19_existing_steward_vote_unreversed(self):
        self.assertIn("The four-to-two vote stands until someone lawfully changes it", self.david)
        self.assertIn("Tessa did not acquire the seventh stool", self.david)

    def test_20_guarantee_bounded_and_uncompleted(self):
        for phrase in ("two nights", "the third night has not been bought",
                       "The square stayed empty through the night"):
            self.assertIn(phrase, self.david)

    def test_21_old_2025_reader_untouched(self):
        self.assertEqual(git_blob(OLD_2025), OLD_2025_SHA)

    def test_22_old_2016_reader_untouched(self):
        self.assertEqual(git_blob(OLD_2016), OLD_2016_SHA)

    def test_23_protected_main_opening_byte_identical(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), sha)

    def test_24_independent_approval_still_held(self):
        for phrase in ("DRAFT / NONCANON", "INDEPENDENT AUTHORS COUNCIL AND UMPIRE HOLD",
                       "FOUNDER ACCEPTANCE HOLD", "not a released novel"):
            self.assertIn(phrase, self.text)

    def test_25_noncannon_causal_reconciliation_not_magic(self):
        self.assertIn("The existing 4–2 steward vote remains", self.text)
        self.assertIn("No shipment, payment, third night, seventh steward", self.david)

    def test_26_exact_six_part_end_marker(self):
        self.assertTrue(self.text.rstrip().endswith("<!-- END_2025_SIX_VOICES_NONCANON -->"))

    def test_27_explicit_period_atlas_and_real_owner_firewalls(self):
        self.assertIn("PERIOD ATLAS HOLD", self.text)
        self.assertIn("no real person's private motives", self.text.lower())

    def test_28_previous_five_voices_first_and_david_last(self):
        self.assertEqual(self.wrappers[0].group(1), "THE_NARROWEST_DOOR_AUSTIN_2025_NONCANON.md")
        self.assertEqual(self.wrappers[-1].group(1), "THE_WINTER_CLAUSE_DAVID_2025_NONCANON.md")


if __name__ == "__main__":
    unittest.main()
