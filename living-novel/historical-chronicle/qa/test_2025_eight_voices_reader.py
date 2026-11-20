"""Noncanonical 2025 eight-voice source-exact assembly checks. No editorial approval implied."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2025/causal-novel"
READER = BASE / "READING_COPY_2025_EIGHT_VOICES_NONCANON.md"
OLD_SEVEN = BASE / "READING_COPY_2025_SEVEN_VOICES_NONCANON.md"
OLD_SEVEN_SHA = "301a302241e7e54cf05ba1f8d154bfff1dc18007"
CHAPTER = BASE / "THE_BANK_THAT_KEPT_ITS_NAME_BOBBY_2025_NONCANON.md"
CHAPTER_SHA = "80a288faa262fff2f4227240431fd9405a85c021"
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
  ],
  [
    "living-novel/historical-chronicle/seasons/2025/causal-novel/THE_BANK_THAT_KEPT_ITS_NAME_BOBBY_2025_NONCANON.md",
    "80a288faa262fff2f4227240431fd9405a85c021",
    "CHAR-BOBBY-MITCHELL",
    5418
  ]
]
EXPECTED_WORDS = 35919
WRAP = re.compile(r"<!-- BEGIN 2025_VOICE ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n([\s\S]*?)\n\n<!-- END 2025_VOICE ([^\n]+) -->")
PROTECTED = {
  "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
  "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
  "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
  "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
OLD_2016 = "living-novel/historical-chronicle/seasons/2016/causal-novel/READING_COPY_CAUSAL_CHAPTERS_01_72_NONCANON.md"
OLD_2016_SHA = "8f1dda21ac4962143ba3291cef4d60769197d62f"

def blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

class EightVoiceReadingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader = READER.read_text(encoding="utf-8")
        cls.chapter = CHAPTER.read_text(encoding="utf-8")
        cls.wraps = list(WRAP.finditer(cls.reader))
        cls.evidence = (ROOT / "living-novel/historical-chronicle/evidence/2025_FLAIM_TEAM_SLOT_AND_PODIUM_READBACK_2026-11-01_REVIEW_ONLY.md").read_text(encoding="utf-8")

    def test_01_eight_wrappers(self):
        self.assertEqual(len(self.wraps), 8)

    def test_02_all_source_shas(self):
        for path, sha, owner, words in SOURCES:
            with self.subTest(path=path):
                self.assertEqual(blob(ROOT / path), sha)

    def test_03_source_exact_wrappers_and_order(self):
        for i,(path,sha,owner,words) in enumerate(SOURCES):
            m=self.wraps[i]
            with self.subTest(i=i):
                self.assertEqual(m.group(1), Path(path).name)
                self.assertEqual(m.group(2), sha)
                self.assertEqual(m.group(3), (ROOT / path).read_text(encoding="utf-8").rstrip("\n"))
                self.assertEqual(m.group(4), Path(path).name)

    def test_04_manifest_has_every_source(self):
        for i,(path,sha,owner,words) in enumerate(SOURCES,1):
            with self.subTest(i=i):
                row=f"| {i} | "
                self.assertIn(row, self.reader)
                self.assertIn(f"`{path}` | `{sha}` | {words} |", self.reader)

    def test_05_source_word_counts(self):
        for path,sha,owner,words in SOURCES:
            with self.subTest(path=path):
                self.assertEqual(len((ROOT / path).read_text(encoding="utf-8").split()), words)

    def test_06_eight_unique_owner_ids(self):
        self.assertEqual(len({a[2] for a in SOURCES}),8)
        registry=(ROOT / "canon/characters/CHARACTER_REGISTRY.yaml").read_text(encoding="utf-8")
        for _,_,owner,_ in SOURCES:
            with self.subTest(owner=owner):
                self.assertIn("id: "+owner, registry)

    def test_07_total_words(self):
        self.assertEqual(sum(a[3] for a in SOURCES), EXPECTED_WORDS)
        self.assertIn(str(EXPECTED_WORDS), self.reader)

    def test_08_chapter_substantial(self):
        self.assertGreaterEqual(len(self.chapter.split()), 4800)

    def test_09_six_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\. ", self.chapter, re.M)),6)

    def test_10_bobby_exclusive_nonhuman_pov(self):
        self.assertIn("Principal and sole interior viewpoint: Bobby Mitchell",self.chapter)
        self.assertIn("gigantic **quadrupedal**",self.chapter)
        self.assertIn("Bobby alone receives interior access",self.chapter)
        self.assertNotRegex(self.chapter, r"\bBobby (?:said|wrote|read aloud)\b")

    def test_11_no_retired_principal_in_scene(self):
        narrative=self.chapter.split("\n---\n\n### Source, causality, and continuity handoff")[0]
        self.assertIsNone(re.search(r"\b(?:Edrin|Edin|Master Oren)\b",narrative,re.I))

    def test_12_verified_2025_slot_ten(self):
        self.assertIn("| 10 | Mud Dogs | 6–8 | 9 | missed_playoffs |",self.evidence)

    def test_13_chapter_team_fact_boundary(self):
        for s in ("team slot 10","Mud Dogs","6–8","finalRank 9","missed_playoffs"):
            self.assertIn(s,self.chapter)

    def test_14_owner_historical_not_authenticated(self):
        self.assertIn("PROVISIONAL FICTIONAL ASSOCIATION",self.chapter)
        self.assertIn("historical human manager owner IDs",self.chapter)

    def test_15_cross_chapter_temporal_reconciliation(self):
        self.assertIn("proposed partial first fuel acceptance",self.chapter)
        self.assertIn("partial accepted first delivery",self.chapter)
        self.assertIn("David's guarantee has not been legally resolved",self.chapter)

    def test_16_noncanonical_atlas_and_founder_holds(self):
        self.assertIn("UNAPPROVED SECONDARY-WORLD PROPOSALS",self.chapter)
        self.assertIn("PERIOD ATLAS HOLD",self.chapter)
        self.assertIn("FOUNDER-ONLY CANON AND PUBLICATION HOLD",self.chapter)

    def test_17_distinct_environmental_causality(self):
        a=self.chapter.index("The first small collapse")
        b=self.chapter.index("Bobby released the coat.")
        c=self.chapter.index("Fuel for another winter")
        self.assertLess(a,b)
        self.assertLess(b,c)
        self.assertIn("further delaying the kitchen",self.chapter)

    def test_18_previous_seven_reader_preserved(self):
        self.assertEqual(blob(OLD_SEVEN),OLD_SEVEN_SHA)

    def test_19_2016_reader_preserved(self):
        self.assertEqual(blob(ROOT / OLD_2016),OLD_2016_SHA)

    def test_20_protected_2026_hard_canon_preserved(self):
        for path,sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(blob(ROOT / path),sha)

    def test_21_reader_end_marker(self):
        self.assertTrue(self.reader.rstrip().endswith("<!-- END_2025_EIGHT_VOICES_NONCANON -->"))

    def test_22_no_reported_release_or_publication(self):
        self.assertIn("DRAFT / NONCANON",self.reader)
        self.assertIn("INDEPENDENT AUTHORS COUNCIL AND UMPIRE HOLD",self.reader)
        self.assertIn("not a released novel",self.reader)

    def test_23_source_total_measures_metadata_not_prose(self):
        self.assertIn("not the full wrapper word count",self.reader)

    def test_24_after_season_no_2026_result(self):
        self.assertIn("No 2026 league result",self.chapter)
        self.assertIn("No new live ESPN query",self.reader)

if __name__ == "__main__":
    unittest.main()
