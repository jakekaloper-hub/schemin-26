"""Source-exact seven-owner 2025 NONCANON reader. Technical integrity only; not independent review."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2025/causal-novel"
READER = BASE / "READING_COPY_2025_SEVEN_VOICES_NONCANON.md"
READER_SHA = "301a302241e7e54cf05ba1f8d154bfff1dc18007"
SOURCES = [
  [
    "living-novel/historical-chronicle/seasons/2025/causal-novel/THE_NARROWEST_DOOR_AUSTIN_2025_NONCANON.md",
    "ae5d50aca6c1ac4da20fb8ead28554baa5e70613",
    "CHAR-AUSTIN-BYARS",
    5001
  ],
  [
    "living-novel/production/historical-saga/R53/HISTORICAL_2025_OBIWAN_NONCANON_PILOT.md",
    "9737fa9b9832de847ee504ed9b87d5e2c404e481",
    "CHAR-JAKE-KALOPER",
    983
  ],
  [
    "living-novel/historical-chronicle/seasons/2025/causal-novel/THE_COURSE_BENEATH_THE_COURSE_ZACH_2025_NONCANON.md",
    "112b3890173cbf11879b139bff966cdff83884d4",
    "CHAR-ZACH-WILSON",
    5310
  ],
  [
    "living-novel/historical-chronicle/seasons/2025/causal-novel/THE_MASKS_THAT_REMAINED_PHILLIP_2025_NONCANON.md",
    "f96832d3bd23840d2fb1853d17940ac54774531d",
    "CHAR-PHILLIP-PITTS",
    4777
  ],
  [
    "living-novel/historical-chronicle/seasons/2025/causal-novel/THE_SIXTH_PLACE_AT_THE_TABLE_BEN_2025_NONCANON.md",
    "9a2b618d498ad97a6343366dcc18ddc409041419",
    "CHAR-BEN-WHIPPLE",
    4495
  ],
  [
    "living-novel/historical-chronicle/seasons/2025/causal-novel/THE_WINTER_CLAUSE_DAVID_2025_NONCANON.md",
    "0de993d2cb3865a7d37ce8cb8f1a9c719c37253c",
    "CHAR-DAVID-BABB",
    4487
  ],
  [
    "living-novel/historical-chronicle/seasons/2025/causal-novel/THE_FIRST_LOAD_BRANDON_2025_NONCANON.md",
    "2cce2e20c426a1e1820d738cebf89c7d815e8458",
    "CHAR-BRANDON-PRYOR",
    5448
  ]
]
OLD_SIX = BASE / "READING_COPY_2025_SIX_VOICES_NONCANON.md"
OLD_SIX_SHA = "ebf421a75eb35cdc5fd4aedf5bf54104b5442ec3"
OLD_2016 = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel/READING_COPY_CAUSAL_CHAPTERS_01_72_NONCANON.md"
OLD_2016_SHA = "8f1dda21ac4962143ba3291cef4d60769197d62f"
PROTECTED = {
  "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
  "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
  "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
  "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
WRAP = re.compile(r"<!-- BEGIN 2025_VOICE ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n([\s\S]*?)\n\n<!-- END 2025_VOICE ([^\n]+) -->")
ROW = re.compile(r"^\| ([1-7]) \| ([^|]+) \| `([^\n]+?)` \| `([0-9a-f]{40})` \| (\d+) \|$", re.M)


def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


class SevenVoicesReaderTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = READER.read_text(encoding="utf-8")
        cls.bodies = [(ROOT / x[0]).read_text(encoding="utf-8") for x in SOURCES]
        cls.brandon = cls.bodies[-1]
        cls.rows = list(ROW.finditer(cls.text))
        cls.wraps = list(WRAP.finditer(cls.text))
        cls.evidence = (ROOT / "living-novel/historical-chronicle/evidence/2025_FLAIM_TEAM_SLOT_AND_PODIUM_READBACK_2026-11-01_REVIEW_ONLY.md").read_text(encoding="utf-8")

    def test_01_reader_sha_pinned(self):
        self.assertEqual(git_blob(READER), READER_SHA)

    def test_02_source_shas_pinned(self):
        for path, sha, owner, words in SOURCES:
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), sha)

    def test_03_exactly_seven_wrappers(self):
        self.assertEqual(len(self.wraps), 7)

    def test_04_exactly_seven_manifest_rows(self):
        self.assertEqual(len(self.rows), 7)

    def test_05_manifest_order_and_bodies(self):
        for i, (path, sha, owner, words) in enumerate(SOURCES):
            row, wrap = self.rows[i], self.wraps[i]
            with self.subTest(i=i):
                self.assertEqual(int(row.group(1)), i+1)
                self.assertIn(owner, row.group(2))
                self.assertEqual(row.group(3), path)
                self.assertEqual(row.group(4), sha)
                self.assertEqual(int(row.group(5)), words)
                fname = Path(path).name
                self.assertEqual(wrap.group(1), fname)
                self.assertEqual(wrap.group(2), sha)
                self.assertEqual(wrap.group(4), fname)
                self.assertEqual(wrap.group(3), self.bodies[i].rstrip("\n"))

    def test_06_all_original_source_word_counts(self):
        for body, (_, _, owner, words) in zip(self.bodies, SOURCES):
            with self.subTest(owner=owner):
                self.assertEqual(len(body.split()), words)

    def test_07_total_words_count_metadata(self):
        self.assertEqual(sum(entry[3] for entry in SOURCES), 30501)
        self.assertIn("30501", self.text)

    def test_08_seven_unique_canonical_owner_ids(self):
        self.assertEqual(len({entry[2] for entry in SOURCES}), 7)

    def test_09_new_brandon_chapter_substantial(self):
        self.assertGreaterEqual(len(self.brandon.split()), 4500)

    def test_10_six_narrative_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\. ", self.brandon, re.M)), 6)

    def test_11_no_nonowner_interior_claim(self):
        self.assertIn("Principal and sole interior viewpoint: Brandon Pryor", self.brandon)
        self.assertIn("there is no nonowner interior narration", self.brandon)

    def test_12_no_retired_narrator(self):
        narrative = self.brandon.split("\n---\n\n### Source, causality, and continuity handoff")[0]
        self.assertIsNone(re.search(r"\b(?:Edrin|Edin|Master Oren)\b", narrative, re.I))

    def test_13_2025_slot_seven_verified_by_archived_evidence(self):
        self.assertIn("| 7 | The Chili Cheesers [source has trailing space] | 6–8 | 7 | eliminated |", self.evidence)

    def test_14_brandon_fact_bound(self):
        for token in ("team slot 7", "The Chili Cheesers", "6–8", "finalRank 7", "eliminated"):
            self.assertIn(token, self.brandon)

    def test_15_historical_manager_still_unknown(self):
        self.assertIn("manager-account ID is UNKNOWN", self.brandon)
        self.assertIn("PROVISIONAL FICTIONAL ASSOCIATION", self.brandon)

    def test_16_period_atlas_and_owner_firewalls(self):
        self.assertIn("PERIOD ATLAS HOLD", self.brandon)
        self.assertIn("not ESPN transactions or authenticated Atlas facts", self.brandon)
        self.assertIn("Real owners' private motives", self.text)

    def test_17_first_load_precedes_receipt_in_new_chapter(self):
        self.assertLess(self.brandon.index("The first load had not been delivered"), self.brandon.index("Iva set aside the sodden pieces"))

    def test_18_delivery_explicitly_partial(self):
        self.assertIn("partial, witnessed wood acceptance", self.text)
        self.assertIn("does not manufacture a full two-night delivery", self.text)

    def test_19_no_third_night_or_worker_vote_promotion(self):
        self.assertIn("the 4–2 vote stands", self.brandon)
        self.assertIn("David has not funded a third night", self.brandon)
        self.assertIn("Tessa's work column is not wages", self.brandon)

    def test_20_independent_author_and_umpire_hold(self):
        for token in ("DRAFT / NONCANON", "INDEPENDENT AUTHORS COUNCIL AND UMPIRE HOLD", "FOUNDER ACCEPTANCE HOLD"):
            self.assertIn(token, self.text)

    def test_21_old_six_voice_reader_unchanged(self):
        self.assertEqual(git_blob(OLD_SIX), OLD_SIX_SHA)

    def test_22_old_2016_reader_unchanged(self):
        self.assertEqual(git_blob(OLD_2016), OLD_2016_SHA)

    def test_23_hard_2026_opening_unchanged(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), sha)

    def test_24_last_owner_brandon(self):
        self.assertEqual(self.wraps[-1].group(1), "THE_FIRST_LOAD_BRANDON_2025_NONCANON.md")

    def test_25_preserved_prior_six_in_order(self):
        self.assertEqual([Path(x[0]).name for x in SOURCES[:6]], [wrap.group(1) for wrap in self.wraps[:6]])

    def test_26_end_marker(self):
        self.assertTrue(self.text.rstrip().endswith("<!-- END_2025_SEVEN_VOICES_NONCANON -->"))

    def test_27_no_2026_outcome_causality(self):
        self.assertIn("before any 2026 league outcome", self.brandon)
        self.assertIn("No new live ESPN query", self.text)

    def test_28_canonical_companion_not_backdated(self):
        self.assertIn("The Dark Horse's canonical 2026 companion identity is not denied", self.brandon)

    def test_29_reader_not_canon_or_published(self):
        self.assertIn("not a released novel", self.text)
        self.assertIn("All civilian, political, market, legal and geographic developments are PROPOSED SECONDARY-WORLD FICTION", self.text)


if __name__ == "__main__":
    unittest.main()
