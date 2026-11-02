"""Source-integrity regressions for a NONCANON 2025 Wilson dispatch bridge.

Automated structural/provenance guards cannot establish historical manager
ownership, literary excellence, physical engineering or independent Umpire approval.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2025/causal-novel"
PREVIOUS = BASE / "READING_COPY_2025_TWELVE_VOICES_ELEVEN_PARTS_WATCH_GROUND_LEVEL_NONCANON.md"
READER = BASE / "READING_COPY_2025_TWELVE_VOICES_TWELVE_PARTS_DISPATCH_BRIDGE_NONCANON.md"
CHAPTER = BASE / "THE_TWO_WORDS_THAT_TRAVELED_WILSON_2025_DEVELOPMENTAL_NONCANON.md"
WILSON_OLD = BASE / "THE_ROAD_NO_BANNER_COULD_OWN_WILSON_2025_NONCANON.md"
JAKE = BASE / "THE_MAP_OF_UNPAID_MILES_JAKE_2025_NONCANON.md"
READER_2016 = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel/READING_COPY_CAUSAL_CHAPTERS_01_72_NONCANON.md"

PREVIOUS_SHA = "3eb4a3c424ba243dc0cb10c81dcf82a7695c6a7e"
CHAPTER_SHA = "dcddddd05ed4b4b151b11b856fbc01e77aa58dc6"
READER_SHA = "df153f16717f77b7b9c760441c331a7445786c99"
WILSON_OLD_SHA = "b737814a6049175ad15ea354cd6e2f44e449f75b"
JAKE_SHA = "3821bc1c3a99bcca5b6419e50ebee6e260dc3234"
READER_2016_SHA = "8f1dda21ac4962143ba3291cef4d60769197d62f"

PROTECTED = {
 "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
 "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
 "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
 "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

WRAP = re.compile(
 r"<!-- BEGIN 2025_VOICE ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n"
 r"([\s\S]*?)\n\n<!-- END 2025_VOICE ([^\n]+) -->"
)
ROW = re.compile(
 r"^\| (\d+) \| ([^|]+) \| `([^`]+)` \| `([0-9a-f]{40})` \| (\d+) \|$", re.M
)
OWNERS = {
 "CHAR-AUSTIN-BYARS", "CHAR-JAKE-KALOPER", "CHAR-ZACH-WILSON",
 "CHAR-PHILLIP-PITTS", "CHAR-BEN-WHIPPLE", "CHAR-DAVID-BABB",
 "CHAR-BRANDON-PRYOR", "CHAR-BOBBY-MITCHELL", "CHAR-KEVIN-ZEEK",
 "CHAR-JORDAN-HOLLINGSHEAD", "CHAR-WILSON-LOOK", "CHAR-MANNING-WELTY",
}

def blob(path):
 data = path.read_bytes()
 return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()

def wordcount(text):
 return len(text.split())

class WilsonDispatchBridge(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.chapter = CHAPTER.read_text(encoding="utf-8")
  cls.reader = READER.read_text(encoding="utf-8")
  cls.previous = PREVIOUS.read_text(encoding="utf-8")
  cls.new_wrap = list(WRAP.finditer(cls.reader))
  cls.old_wrap = list(WRAP.finditer(cls.previous))
  manifest = cls.reader.split("## Source-exact composition manifest\n", 1)[1].split("\n---\n", 1)[0]
  cls.rows = ROW.findall(manifest)
  cls.story = cls.chapter.split("## Source, chronology and integration receipt", 1)[0]

 def test_01_previous_reader_immutable(self):
  self.assertEqual(blob(PREVIOUS), PREVIOUS_SHA)

 def test_02_new_wilson_chapter_blob(self):
  self.assertEqual(blob(CHAPTER), CHAPTER_SHA)

 def test_03_new_reader_blob(self):
  self.assertEqual(blob(READER), READER_SHA)

 def test_04_existing_wilson_source_immutable(self):
  self.assertEqual(blob(WILSON_OLD), WILSON_OLD_SHA)

 def test_05_later_jake_source_immutable(self):
  self.assertEqual(blob(JAKE), JAKE_SHA)

 def test_06_separate_2016_reader_immutable(self):
  self.assertEqual(blob(READER_2016), READER_2016_SHA)

 def test_07_protected_prologue_and_chapters_immutable(self):
  for path, sha in PROTECTED.items():
   with self.subTest(path=path):
    self.assertEqual(blob(ROOT / path), sha)

 def test_08_old_and_new_wrapper_counts(self):
  self.assertEqual(len(self.old_wrap), 11)
  self.assertEqual(len(self.new_wrap), 12)

 def test_09_part_headings_ordered(self):
  self.assertEqual(
   [int(x) for x in re.findall(r"^## Part (\d+) —", self.reader, re.M)],
   list(range(1, 13))
  )

 def test_10_all_previous_source_wrappers_identical(self):
  for i, old in enumerate(self.old_wrap):
   index = i if i < 7 else i + 1
   with self.subTest(index=index):
    self.assertEqual(old.group(0), self.new_wrap[index].group(0))

 def test_11_bridge_is_eighth_wrapper(self):
  self.assertEqual(self.new_wrap[7].group(1), CHAPTER.name)
  self.assertEqual(self.new_wrap[7].group(2), CHAPTER_SHA)
  self.assertEqual(self.new_wrap[7].group(4), CHAPTER.name)

 def test_12_every_wrapper_is_source_exact(self):
  for m in self.new_wrap:
   with self.subTest(source=m.group(1)):
    path = BASE / m.group(1)
    self.assertTrue(path.is_file())
    self.assertEqual(m.group(1), m.group(4))
    self.assertEqual(blob(path), m.group(2))
    self.assertEqual(path.read_text(encoding="utf-8").rstrip("\n"), m.group(3))

 def test_13_manifest_twelve_rows(self):
  self.assertEqual(len(self.rows), 12)

 def test_14_manifest_matches_wrapper_order_and_sha(self):
  for i, row in enumerate(self.rows):
   with self.subTest(index=i):
    self.assertEqual(int(row[0]), i + 1)
    self.assertEqual(Path(row[2]).name, self.new_wrap[i].group(1))
    self.assertEqual(row[3], self.new_wrap[i].group(2))

 def test_15_manifest_individual_word_counts(self):
  for i, row in enumerate(self.rows):
   with self.subTest(index=i):
    self.assertEqual(int(row[4]), wordcount(self.new_wrap[i].group(3)))

 def test_16_source_words_aggregate(self):
  self.assertEqual(sum(int(x[4]) for x in self.rows), 63698)
  self.assertIn("63698 whitespace-delimited source words", self.reader)

 def test_17_new_material_exactly_4698_words(self):
  self.assertEqual(wordcount(self.chapter), 4698)
  self.assertEqual(63698 - 59000, 4698)

 def test_18_all_twelve_owner_character_ids_covered(self):
  rendered = set(re.findall(r"CHAR-[A-Z]+(?:-[A-Z]+)*", " ".join(x[1] for x in self.rows)))
  self.assertEqual(rendered, OWNERS)

 def test_19_exclusive_wilson_movement_viewpoints(self):
  movements = re.findall(r"^### ([IVX]+)\. ([^\n]+)", self.story, re.M)
  self.assertEqual(len(movements), 5)
  self.assertEqual([x[0] for x in movements], ["I", "II", "III", "IV", "V"])
  self.assertEqual(self.chapter.count("Sole interior viewpoint: fictional Wilson Look"), 1)

 def test_20_no_unlicensed_institutional_viewpoints(self):
  self.assertNotRegex(self.story, r"(?im)^### [IVX]+\. .*\b(Edrin|Edin|Oren)\b")

 def test_21_historical_owner_authentication_hold_explicit(self):
  self.assertIn("UNKNOWN / UNAUTHENTICATED", self.chapter)
  self.assertIn("9–5 and fifth place", self.chapter)
  self.assertIn("not biographical", self.chapter)

 def test_22_road_fiction_and_atlas_hold_explicit(self):
  self.assertIn("proposed secondary-world fiction", self.chapter)
  self.assertIn("not approved period Atlas geography", self.chapter)

 def test_23_did_not_assert_second_loaded_wagon_passed(self):
  self.assertIn("SECOND LOADED WAGON HELD", self.story)
  self.assertIn("no second loaded crossing", self.chapter.lower())

 def test_24_failed_brace_and_dispatch_distinction(self):
  self.assertIn("NO CLEARANCE FOR FURTHER LOADED CROSSING", self.story)
  self.assertIn("ONE INSPECTED LOADED WAGON PASSED", self.story)
  self.assertIn("Tarin", self.story)
  self.assertIn("Ossa", self.story)

 def test_25_no_certified_route_to_jake_or_coast(self):
  self.assertIn("No geospatial edge to Jake's hall", self.chapter)
  self.assertIn("the salt harbor", self.chapter)
  self.assertIn("intentionally unknown", self.chapter)

 def test_26_signed_notice_not_road_sovereignty(self):
  self.assertIn("no claim of renewed high watch", self.chapter)
  self.assertIn("no claim of", self.chapter.lower())
  self.assertIn("NO MERGE / NO PUBLICATION / NO CANON PROMOTION", self.chapter)

 def test_27_original_2025_source_chain_preserved(self):
  self.assertEqual(
   [m.group(2) for m in self.old_wrap],
   [m.group(2) for i,m in enumerate(self.new_wrap) if i != 7]
  )

 def test_28_insertion_between_wilson_and_manning(self):
  self.assertIn("ROAD_NO_BANNER", self.new_wrap[6].group(1))
  self.assertIn("TWO_WORDS", self.new_wrap[7].group(1))
  self.assertIn("WEATHER_THAT", self.new_wrap[8].group(1))


if __name__ == "__main__":
 unittest.main()
