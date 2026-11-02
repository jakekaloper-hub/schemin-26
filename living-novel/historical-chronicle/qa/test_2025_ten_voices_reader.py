"""Ten-voice 2025 noncanon reader: source-exact and negative continuity guards.

Passing tests establish document integrity, not owner authentication, period
Atlas authority, independent editorial acceptance or release.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2025/causal-novel"
READER = BASE / "READING_COPY_2025_TEN_VOICES_NONCANON.md"
PREVIOUS = BASE / "READING_COPY_2025_NINE_VOICES_NONCANON.md"
PREVIOUS_SHA = "43aea9a2c59001e311b1b77d5f009d1ac03d8752"
CHAPTER = BASE / "THE_BELL_BELOW_THE_FLOOR_JORDAN_2025_NONCANON.md"
CHAPTER_SHA = "e65886fe766c3ba13f07e0cc63d4ebc13560629e"
EVIDENCE = ROOT / "living-novel/historical-chronicle/evidence/2025_FLAIM_TEAM_SLOT_AND_PODIUM_READBACK_2026-11-01_REVIEW_ONLY.md"
WRAPPER = re.compile(r"<!-- BEGIN 2025_VOICE ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n([\s\S]*?)\n\n<!-- END 2025_VOICE ([^\n]+) -->")
SOURCES = [
    ("THE_NARROWEST_DOOR_AUSTIN_2025_NONCANON.md", "ae5d50aca6c1ac4da20fb8ead28554baa5e70613", "CHAR-AUSTIN-BYARS", 5001),
    ("HISTORICAL_2025_OBIWAN_NONCANON_PILOT.md", "9737fa9b9832de847ee504ed9b87d5e2c404e481", "CHAR-JAKE-KALOPER", 983),
    ("THE_COURSE_BENEATH_THE_COURSE_ZACH_2025_NONCANON.md", "112b3890173cbf11879b139bff966cdff83884d4", "CHAR-ZACH-WILSON", 5310),
    ("THE_MASKS_THAT_REMAINED_PHILLIP_2025_NONCANON.md", "f96832d3bd23840d2fb1853d17940ac54774531d", "CHAR-PHILLIP-PITTS", 4777),
    ("THE_SIXTH_PLACE_AT_THE_TABLE_BEN_2025_NONCANON.md", "9a2b618d498ad97a6343366dcc18ddc409041419", "CHAR-BEN-WHIPPLE", 4495),
    ("THE_WINTER_CLAUSE_DAVID_2025_NONCANON.md", "0de993d2cb3865a7d37ce8cb8f1a9c719c37253c", "CHAR-DAVID-BABB", 4487),
    ("THE_FIRST_LOAD_BRANDON_2025_NONCANON.md", "2cce2e20c426a1e1820d738cebf89c7d815e8458", "CHAR-BRANDON-PRYOR", 5448),
    ("THE_BANK_THAT_KEPT_ITS_NAME_BOBBY_2025_NONCANON.md", "80a288faa262fff2f4227240431fd9405a85c021", "CHAR-BOBBY-MITCHELL", 5418),
    ("THE_WATCH_THAT_WENT_DARK_KEVIN_2025_NONCANON.md", "c4e75354fba5bc8d21719a9bcbc0661197467b2f", "CHAR-KEVIN-ZEEK", 6155),
    ("THE_BELL_BELOW_THE_FLOOR_JORDAN_2025_NONCANON.md", CHAPTER_SHA, "CHAR-JORDAN-HOLLINGSHEAD", 6595),
]
OTHER_SOURCE = ROOT / "living-novel/production/historical-saga/R53/HISTORICAL_2025_OBIWAN_NONCANON_PILOT.md"
OLD_2016 = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel/READING_COPY_CAUSAL_CHAPTERS_01_72_NONCANON.md"
OLD_2016_SHA = "8f1dda21ac4962143ba3291cef4d60769197d62f"
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def gitblob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def source_path(name):
    return OTHER_SOURCE if name == OTHER_SOURCE.name else BASE / name

class TenVoiceReadingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader = READER.read_text(encoding="utf-8")
        cls.chapter = CHAPTER.read_text(encoding="utf-8")
        cls.chapter_body = cls.chapter.split("\n---\n\n### Source, causality, and continuity handoff")[0]
        cls.parts = list(WRAPPER.finditer(cls.reader))
        cls.evidence = EVIDENCE.read_text(encoding="utf-8")

    def test_01_ten_source_wrappers(self):
        self.assertEqual(len(self.parts), 10)

    def test_02_source_git_blob_pins(self):
        for name, sha, _, _ in SOURCES:
            with self.subTest(name=name):
                self.assertEqual(gitblob(source_path(name)), sha)

    def test_03_every_source_embedded_exactly(self):
        for i, (name, sha, _, _) in enumerate(SOURCES):
            with self.subTest(name=name):
                p = self.parts[i]
                self.assertEqual((p.group(1), p.group(2), p.group(4)), (name, sha, name))
                self.assertEqual(p.group(3), source_path(name).read_text(encoding="utf-8").rstrip("\n"))

    def test_04_source_word_counts(self):
        for name, _, _, words in SOURCES:
            with self.subTest(name=name):
                self.assertEqual(len(source_path(name).read_text(encoding="utf-8").split()), words)

    def test_05_source_sum(self):
        self.assertEqual(sum(e[3] for e in SOURCES), 48669)

    def test_06_reader_total_distinct_from_wrappers(self):
        self.assertIn("48669", self.reader)
        self.assertGreater(len(self.reader.split()), 48669)

    def test_07_manifest_pins_and_word_counts(self):
        for i, (name, sha, owner, words) in enumerate(SOURCES, 1):
            with self.subTest(name=name):
                self.assertIn("| "+str(i)+" |", self.reader)
                self.assertIn(chr(96)+sha+chr(96)+" | "+str(words)+" |", self.reader)
                self.assertIn(owner, self.reader)

    def test_08_ten_distinct_registered_characters(self):
        owners = [row[2] for row in SOURCES]
        self.assertEqual(len(set(owners)), 10)
        registry = (ROOT / "canon/characters/CHARACTER_REGISTRY.yaml").read_text(encoding="utf-8")
        for owner in owners:
            self.assertIn("id: "+owner, registry)

    def test_09_jordan_substantial(self):
        self.assertGreaterEqual(len(self.chapter.split()), 6000)

    def test_10_six_movement_arc(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\. ", self.chapter, re.M)), 6)

    def test_11_jordan_principal_only(self):
        self.assertIn("Principal and sole interior viewpoint: Jordan Hollingshead", self.chapter)
        self.assertIn("Jordan alone has interior access", self.chapter)

    def test_12_current_character_cues(self):
        for cue in ("horns", "beard", "battered", "metal bat", "pit bull", "Slob"):
            self.assertIn(cue, self.chapter)

    def test_13_no_institutional_pov_in_prose(self):
        self.assertIsNone(re.search(r"\b(Edrin|Edin|Oren)\b", self.chapter_body))

    def test_14_grounded_2025_team_slot(self):
        self.assertIn("| 3 | Slob on my Dobb | 4–10 | 8 | missed_playoffs |", self.evidence)
        for cue in ("team slot 3", "4–10", "finalRank 8", "missed_playoffs"):
            self.assertIn(cue, self.chapter)

    def test_15_human_manager_authentication_unavailable(self):
        self.assertIn("does NOT authenticate Jordan Hollingshead", self.chapter)
        self.assertIn("PROVISIONAL FICTIONAL ASSOCIATION", self.chapter)
        self.assertIn("not ten independently verified historical human owner accounts", self.reader)

    def test_16_older_reader_frozen(self):
        self.assertEqual(gitblob(PREVIOUS), PREVIOUS_SHA)

    def test_17_2016_seventy_two_reader_frozen(self):
        self.assertEqual(gitblob(OLD_2016), OLD_2016_SHA)

    def test_18_protected_opening_frozen(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(gitblob(ROOT / path), sha)

    def test_19_closed_reader_assembly(self):
        self.assertTrue(self.reader.rstrip().endswith("<!-- END_2025_TEN_VOICES_NONCANON -->"))

    def test_20_watch_floor_not_magically_restored(self):
        self.assertIn("Its bell still lay at ground level", self.chapter)
        self.assertIn("The road did not become safe", self.chapter)

    def test_21_barrel_causes_material_harm(self):
        self.assertIn("The barrel moved", self.chapter)
        self.assertIn("blocked a road", self.chapter)
        self.assertIn("wheel pin", self.chapter)

    def test_22_relay_fails_in_rain(self):
        self.assertIn("Their first trial failed", self.chapter)
        self.assertIn("rain", self.chapter)
        self.assertIn("the signal had failed", self.chapter.lower())

    def test_23_no_false_road_security(self):
        self.assertIn("one cart", self.chapter.lower())
        self.assertIn("The second wagon stayed", self.chapter)
        self.assertIn("No permanent guard", self.chapter)

    def test_24_financial_cost_not_disguised(self):
        self.assertIn("Two hours are unpaid", self.chapter)
        self.assertIn("the debt discharged", self.chapter)

    def test_25_unknown_figures_not_named_enemies(self):
        self.assertIn("three figures reported earlier remained unidentified", self.chapter)
        self.assertIn("unknown", self.chapter.lower())

    def test_26_no_future_2026_knowledge(self):
        self.assertIn("no 2026 future results", self.chapter.lower())

    def test_27_geography_and_release_holds(self):
        for cue in ("UNAPPROVED SECONDARY-WORLD", "PERIOD ATLAS HOLD", "INDEPENDENT", "FOUNDER-ONLY"):
            self.assertIn(cue, self.chapter)

    def test_28_parts_ordered_and_tenth_present(self):
        self.assertIn("## Part 10 — Jordan / CHAR-JORDAN-HOLLINGSHEAD", self.reader)
        self.assertLess(self.reader.index("## Part 9 — Kevin"), self.reader.index("## Part 10 — Jordan"))

if __name__ == "__main__":
    unittest.main()
