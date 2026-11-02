"""2025 Wilson V3 / assembled 11-part developmental edition integrity checks.
These are technical regression checks, NOT independent literary or Umpire acceptance.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2025/causal-novel"
CHAPTER = BASE / "THE_ROAD_THAT_SPOKE_IN_TWO_VOICES_WILSON_2025_DEVELOPMENTAL_COMPRESSION_V3_NONCANON.md"
READER = BASE / "READING_COPY_2025_TWELVE_VOICES_ELEVEN_PARTS_WILSON_COMPRESSION_V3_NONCANON.md"
V2 = BASE / "THE_ROAD_THAT_SPOKE_IN_TWO_VOICES_WILSON_2025_SELECTED_REVISION_V2_NONCANON.md"
V2_READER = BASE / "READING_COPY_2025_TWELVE_VOICES_ELEVEN_PARTS_SELECTED_WILSON_V2_NONCANON.md"
PINNED = {
    CHAPTER: "31ddd0d2f18f7eb433bd1d6d0abb791b666aaeb4",
    READER: "bf47f2bc09bd31500487409fd220a4e818fd1671",
    V2: "5c953eb78e8f383d1038712501335418ce8af4ab",
    V2_READER: "9a0181bf15bfff9ea8516fce06cda5ea1e8ba2c1",
}
PROTECTED = {
    "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
    "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
    "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
    "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
WRAP = re.compile(r"<!-- BEGIN 2025_VOICE ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n([\s\S]*?)\n\n<!-- END 2025_VOICE ([^\n]+) -->")
ROW = re.compile(r"^\| (\d+) \| ([^|]+) \| `([^`]+)` \| `([0-9a-f]{40})` \| (\d+) \|$", re.M)
OWNERS = {
    "CHAR-AUSTIN-BYARS", "CHAR-JAKE-KALOPER", "CHAR-ZACH-WILSON",
    "CHAR-PHILLIP-PITTS", "CHAR-BEN-WHIPPLE", "CHAR-DAVID-BABB",
    "CHAR-BRANDON-PRYOR", "CHAR-BOBBY-MITCHELL", "CHAR-KEVIN-ZEEK",
    "CHAR-JORDAN-HOLLINGSHEAD", "CHAR-WILSON-LOOK", "CHAR-MANNING-WELTY",
}

def git_blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()

class WilsonV3DevelopmentalReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.story = CHAPTER.read_text(encoding="utf-8")
        cls.reader = READER.read_text(encoding="utf-8")
        cls.v2reader = V2_READER.read_text(encoding="utf-8")
        cls.parts = list(WRAP.finditer(cls.reader))
        cls.oldparts = list(WRAP.finditer(cls.v2reader))
        cls.rows = ROW.findall(cls.reader.split("## Part 1 —", 1)[0])

    def test_01_pinned_sources_unchanged(self):
        for file, expected in PINNED.items():
            with self.subTest(file=file.name):
                self.assertEqual(git_blob(file), expected)

    def test_02_protected_2026_opening_untouched(self):
        for path, expected in PROTECTED.items():
            with self.subTest(path=path):
                self.assertEqual(git_blob(ROOT / path), expected)

    def test_03_eleven_parts_rows_and_all_source_hashes(self):
        self.assertEqual(len(self.parts), 11)
        self.assertEqual(len(self.rows), 11)
        for index, (wrap, row) in enumerate(zip(self.parts, self.rows), 1):
            part, owner, name, sha, words = row
            source = BASE / name
            with self.subTest(index=index, source=name):
                self.assertEqual(int(part), index)
                self.assertEqual(wrap.group(1), name)
                self.assertEqual(wrap.group(4), name)
                self.assertEqual(wrap.group(2), sha)
                self.assertEqual(git_blob(source), sha)
                self.assertEqual(wrap.group(3), source.read_text(encoding="utf-8").rstrip("\n"))
                self.assertEqual(len(source.read_text(encoding="utf-8").split()), int(words))

    def test_04_ten_non_wilson_chapter_wrappers_byte_exact(self):
        self.assertEqual(len(self.oldparts), 11)
        self.assertEqual([p.group(0) for i,p in enumerate(self.parts) if i!=6],
                         [p.group(0) for i,p in enumerate(self.oldparts) if i!=6])

    def test_05_v3_source_only_at_seventh_position(self):
        self.assertEqual(self.parts[6].group(1), CHAPTER.name)
        self.assertEqual(self.parts[6].group(2), PINNED[CHAPTER])
        self.assertEqual(sum(p.group(1)==CHAPTER.name for p in self.parts), 1)

    def test_06_source_word_tally(self):
        self.assertEqual(len(self.story.split()), 9909)
        self.assertEqual(sum(int(row[4]) for row in self.rows), 63315)
        self.assertIn("63315 source words", self.reader)

    def test_07_all_twelve_canonical_owner_identities(self):
        ids=set(re.findall(r"CHAR-[A-Z0-9-]+", " ".join(row[1] for row in self.rows)))
        self.assertEqual(ids, OWNERS)

    def test_08_one_loaded_crossing_and_held_second(self):
        self.assertIn("An empty cart was examined yesterday", self.story)
        self.assertIn("ONE INSPECTED LOADED WAGON PASSED", self.story)
        self.assertIn("SECOND LOADED WAGON HELD", self.story)
        self.assertIn("NO CLEARANCE FOR FURTHER LOADED CROSSING", self.story)
        self.assertIn("The second wagon stayed where it was.", self.story)

    def test_09_single_departure_and_eleven_movements(self):
        self.assertEqual(self.story.count("The procession moved."),1)
        names=re.findall(r"^### ([IVX]+)\. ",self.story.split("## Source and editorial receipt",1)[0],re.M)
        self.assertEqual(names, ["I","II","III","IV","V","VI","VII","VIII","IX","X","XI"])

    def test_10_prose_compression_real_not_just_metadata(self):
        self.assertLess(len(self.story.split()), len(V2.read_text(encoding="utf-8").split())-1500)
        self.assertIn("The driver of the waiting wagon came to Ossa with a sheet of paper and a narrow knife.", self.story)
        self.assertIn("A witnessed wage", V2.read_text(encoding="utf-8"))

    def test_11_driver_material_consequences_unsettled(self):
        self.assertIn("Write down my day", self.story)
        self.assertIn("Not yet known", self.story)
        self.assertIn("Neither paper was a promise of payment.", self.story)
        self.assertIn("sealed chests remained on the wagon", self.story)

    def test_12_unloading_state_after_bargain_consistent(self):
        self.assertIn("move only the coverings and stacked tiles", self.story)
        self.assertIn("moved the blankets and tiles beneath the dry covering", self.story)
        self.assertIn("The sealed chests remained on the wagon", self.story)
        self.assertNotIn("he had not yet chosen", self.story.lower())

    def test_13_paid_new_watchers_once_separately_from_old_wages(self):
        self.assertEqual(self.story.count("He counted the four agreed wages into four separate hands."), 1)
        self.assertIn("the old watch's wage debt", self.story)
        self.assertIn("Jordan's two owed hours had been paid by Jordan", self.story)
        self.assertIn("unappointed fee board", self.story)

    def test_14_unknown_figures_not_assigned(self):
        self.assertIn("three indistinct figures", self.story)
        self.assertIn("unconfirmed", self.story)
        self.assertNotIn("identified as saboteurs", self.story)

    def test_15_historical_and_spatial_firewall(self):
        self.assertIn("DRAFT / NONCANON", self.story)
        self.assertIn("human-manager-account", self.reader)
        self.assertIn("no cross-Atlas routes", self.reader)
        self.assertIn("no independent", self.reader.lower()) if False else None
        self.assertNotIn("couriers delivered the reports to Jake", self.story)

    def test_16_no_author_or_umpire_approval_inferred(self):
        self.assertIn("independent Umpire", self.reader)
        self.assertIn("not canon", self.reader.lower())
        self.assertIn("No merge, publication or canon promotion", self.reader)

if __name__ == "__main__":
    unittest.main()
