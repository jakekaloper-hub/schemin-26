"""Nine-voice noncanonical historical reader: source integrity and negative guards.

Passing tests validate documentary assembly, not historical owner lineage,
period geography, a human independent editorial review, or canon promotion.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2025/causal-novel"
READER = BASE / "READING_COPY_2025_NINE_VOICES_NONCANON.md"
PREVIOUS_READER = BASE / "READING_COPY_2025_EIGHT_VOICES_NONCANON.md"
PREVIOUS_READER_SHA = "17050cca9c3492f960c880186d82af23b84aadd0"
CHAPTER = BASE / "THE_WATCH_THAT_WENT_DARK_KEVIN_2025_NONCANON.md"
CHAPTER_SHA = "c4e75354fba5bc8d21719a9bcbc0661197467b2f"
SOURCES = [
    ("THE_NARROWEST_DOOR_AUSTIN_2025_NONCANON.md", "ae5d50aca6c1ac4da20fb8ead28554baa5e70613", "CHAR-AUSTIN-BYARS", 5001),
    ("HISTORICAL_2025_OBIWAN_NONCANON_PILOT.md", "9737fa9b9832de847ee504ed9b87d5e2c404e481", "CHAR-JAKE-KALOPER", 983),
    ("THE_COURSE_BENEATH_THE_COURSE_ZACH_2025_NONCANON.md", "112b3890173cbf11879b139bff966cdff83884d4", "CHAR-ZACH-WILSON", 5310),
    ("THE_MASKS_THAT_REMAINED_PHILLIP_2025_NONCANON.md", "f96832d3bd23840d2fb1853d17940ac54774531d", "CHAR-PHILLIP-PITTS", 4777),
    ("THE_SIXTH_PLACE_AT_THE_TABLE_BEN_2025_NONCANON.md", "9a2b618d498ad97a6343366dcc18ddc409041419", "CHAR-BEN-WHIPPLE", 4495),
    ("THE_WINTER_CLAUSE_DAVID_2025_NONCANON.md", "0de993d2cb3865a7d37ce8cb8f1a9c719c37253c", "CHAR-DAVID-BABB", 4487),
    ("THE_FIRST_LOAD_BRANDON_2025_NONCANON.md", "2cce2e20c426a1e1820d738cebf89c7d815e8458", "CHAR-BRANDON-PRYOR", 5448),
    ("THE_BANK_THAT_KEPT_ITS_NAME_BOBBY_2025_NONCANON.md", "80a288faa262fff2f4227240431fd9405a85c021", "CHAR-BOBBY-MITCHELL", 5418),
    ("THE_WATCH_THAT_WENT_DARK_KEVIN_2025_NONCANON.md", CHAPTER_SHA, "CHAR-KEVIN-ZEEK", 6155),
]
OTHER_SOURCE = ROOT / "living-novel/production/historical-saga/R53/HISTORICAL_2025_OBIWAN_NONCANON_PILOT.md"
EXPECTED_SOURCE_WORDS = 42074
WRAPPER = re.compile(r"<!-- BEGIN 2025_VOICE ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n([\s\S]*?)\n\n<!-- END 2025_VOICE ([^\n]+) -->")
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
OLD_2016 = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel/READING_COPY_CAUSAL_CHAPTERS_01_72_NONCANON.md"
OLD_2016_SHA = "8f1dda21ac4962143ba3291cef4d60769197d62f"

def gitblob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def source_path(name):
    return OTHER_SOURCE if name == OTHER_SOURCE.name else BASE / name

class NineVoiceReadingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader = READER.read_text(encoding="utf-8")
        cls.chapter = CHAPTER.read_text(encoding="utf-8")
        cls.wrappers = list(WRAPPER.finditer(cls.reader))
        cls.evidence = (ROOT / "living-novel/historical-chronicle/evidence/2025_FLAIM_TEAM_SLOT_AND_PODIUM_READBACK_2026-11-01_REVIEW_ONLY.md").read_text(encoding="utf-8")

    def test_01_nine_complete_wrappers(self):
        self.assertEqual(len(self.wrappers), 9)

    def test_02_source_blob_pins(self):
        for name, sha, _, _ in SOURCES:
            with self.subTest(name=name):
                self.assertEqual(gitblob(source_path(name)), sha)

    def test_03_embedded_chapter_bytes(self):
        for i, (name, sha, _, _) in enumerate(SOURCES):
            w = self.wrappers[i]
            with self.subTest(name=name):
                self.assertEqual(w.group(1), name)
                self.assertEqual(w.group(2), sha)
                self.assertEqual(w.group(3), source_path(name).read_text(encoding="utf-8").rstrip("\n"))
                self.assertEqual(w.group(4), name)

    def test_04_manifest_nine_lines(self):
        for i, (name, sha, _, words) in enumerate(SOURCES, 1):
            with self.subTest(name=name):
                self.assertIn(f"| {i} |", self.reader)
                self.assertIn(f"`{sha}` | {words} |", self.reader)
                self.assertIn(name, self.reader)

    def test_05_source_word_counts(self):
        for name, _, _, words in SOURCES:
            with self.subTest(name=name):
                self.assertEqual(len(source_path(name).read_text(encoding="utf-8").split()), words)

    def test_06_total_original_source_words(self):
        self.assertEqual(sum(s[3] for s in SOURCES), EXPECTED_SOURCE_WORDS)
        self.assertIn(str(EXPECTED_SOURCE_WORDS), self.reader)

    def test_07_nine_unique_registered_owner_characters(self):
        ids = [s[2] for s in SOURCES]
        self.assertEqual(len(set(ids)), 9)
        registry = (ROOT / "canon/characters/CHARACTER_REGISTRY.yaml").read_text(encoding="utf-8")
        for owner in ids:
            with self.subTest(owner=owner):
                self.assertIn("id: " + owner, registry)

    def test_08_new_chapter_is_substantial(self):
        self.assertGreaterEqual(len(self.chapter.split()), 5000)

    def test_09_six_dramatic_movements(self):
        self.assertEqual(len(re.findall(r"^### [IVX]+\. ", self.chapter, re.M)), 6)

    def test_10_kevin_principal_only(self):
        self.assertIn("Principal and sole interior viewpoint: Kevin Zeek", self.chapter)
        self.assertIn("Kevin alone has interior access", self.chapter)
        self.assertIn("CHAR-KEVIN-ZEEK", self.chapter)

    def test_11_correct_feline_morphology(self):
        self.assertIn("anthropomorphic red leopard", self.chapter)
        self.assertIn("black rosettes", self.chapter)
        self.assertIn("claws", self.chapter)

    def test_12_retired_principal_not_reintroduced(self):
        narrative = self.chapter.split("\n---\n\n### Source, causality, and continuity handoff")[0]
        self.assertIsNone(re.search(r"\b(?:Edrin|Edin|Master Oren)\b", narrative, re.I))

    def test_13_2025_team_slot_two_grounded(self):
        self.assertIn("| 2 | Red Leopards | 6–8 | 11 | missed_playoffs |", self.evidence)
        for term in ("team slot 2", "Red Leopards", "6–8", "finalRank 11", "missed_playoffs"):
            self.assertIn(term, self.chapter)

    def test_14_historical_human_manager_unverified(self):
        self.assertIn("does NOT authenticate Kevin Zeek", self.chapter)
        self.assertIn("PROVISIONAL FICTIONAL ASSOCIATION", self.chapter)

    def test_15_reader_keeps_historical_firewall(self):
        self.assertIn("human manager IDs", self.reader)
        self.assertIn("nine independently verified historical human owner accounts", self.reader)

    def test_16_performance_does_not_change_standings(self):
        self.assertIn("No number there could be improved by saving a kitchen", self.chapter)
        self.assertIn("No 2026 event", self.chapter)

    def test_17_material_loss_precedes_delivery(self):
        a = self.chapter.index("The lowering")
        b = self.chapter.index("The fire that had witnesses")
        c = self.chapter.index("An opening without a watcher")
        self.assertLess(a, b)
        self.assertLess(b, c)

    def test_18_public_inspection_limits_gift(self):
        self.assertIn("sound count was entered", self.chapter)
        self.assertIn("small second fire for the coming night", self.chapter)
        self.assertIn("not automatically release Pell", self.chapter)

    def test_19_unelected_workers_remain_unresolved(self):
        self.assertIn("still had no corresponding seat", self.chapter)
        self.assertIn("No one certified that Pell had completed", self.chapter)

    def test_20_unwatched_approach_risk_survives(self):
        self.assertIn("could not safely be reached", self.chapter)
        self.assertIn("explicitly unidentified", self.chapter)
        self.assertIn("watch waited for a new floor", self.chapter)

    def test_21_independent_gates_explicit(self):
        self.assertIn("INDEPENDENT", self.chapter)
        self.assertIn("FOUNDER-ONLY CANON AND PUBLICATION HOLD", self.chapter)
        self.assertIn("NONCANON", self.reader)

    def test_22_old_eight_reader_unchanged(self):
        self.assertEqual(gitblob(PREVIOUS_READER), PREVIOUS_READER_SHA)

    def test_23_old_seventy_two_chapters_unchanged(self):
        self.assertEqual(gitblob(OLD_2016), OLD_2016_SHA)

    def test_24_protected_opening_unchanged(self):
        for path, sha in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(gitblob(ROOT / path), sha)

    def test_25_assembly_closed(self):
        self.assertTrue(self.reader.rstrip().endswith("<!-- END_2025_NINE_VOICES_NONCANON -->"))

    def test_26_no_external_acceptance_claim(self):
        self.assertIn("Neither this assembled document nor its chapter files is released or canon-promoted", self.reader)
        self.assertIn("INDEPENDENT AUTHORS COUNCIL AND UMPIRE HOLD", self.reader)

    def test_27_distinct_original_words_from_reader_words(self):
        self.assertIn("not its complete word count or a narrative-prose-only count", self.reader)
        self.assertGreater(len(self.reader.split()), EXPECTED_SOURCE_WORDS)

    def test_28_source_location_is_noncanonical(self):
        self.assertIn("UNAPPROVED SECONDARY-WORLD PROPOSALS", self.chapter)
        self.assertIn("not certified 2025 Atlas locations", self.chapter)

if __name__ == "__main__":
    unittest.main()
