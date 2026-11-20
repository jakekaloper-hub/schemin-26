"""Source-exact noncanon integrated 2025 Wilson road/dispatch developmental guards.

These checks do NOT certify manager identities, engineering, fiction quality,
period Atlas legality, independent author/Umpire clearance or canon promotion.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2025/causal-novel"
PREVIOUS = BASE / "READING_COPY_2025_TWELVE_VOICES_TWELVE_PARTS_DISPATCH_BRIDGE_NONCANON.md"
READER = BASE / "READING_COPY_2025_TWELVE_VOICES_ELEVEN_PARTS_INTEGRATED_WILSON_NONCANON.md"
CHAPTER = BASE / "THE_ROAD_THAT_SPOKE_IN_TWO_VOICES_WILSON_2025_INTEGRATED_NONCANON.md"
OLD = BASE / "THE_ROAD_NO_BANNER_COULD_OWN_WILSON_2025_NONCANON.md"
BRIDGE = BASE / "THE_TWO_WORDS_THAT_TRAVELED_WILSON_2025_DEVELOPMENTAL_NONCANON.md"
READER_2016 = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel/READING_COPY_CAUSAL_CHAPTERS_01_72_NONCANON.md"

PREVIOUS_SHA = "df153f16717f77b7b9c760441c331a7445786c99"
READER_SHA = "22f438a91aba72f391ae4ec7be5cae3c375230ce"
CHAPTER_SHA = "bdaac1446d87c9ce0e738f6f9bbd632397152251"
OLD_SHA = "b737814a6049175ad15ea354cd6e2f44e449f75b"
BRIDGE_SHA = "dcddddd05ed4b4b151b11b856fbc01e77aa58dc6"
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
ROW = re.compile(r"^\| (\d+) \| ([^|]+) \| `([^`]+)` \| `([0-9a-f]{40})` \| (\d+) \|$", re.M)
OWNERS = {
 "CHAR-AUSTIN-BYARS", "CHAR-JAKE-KALOPER", "CHAR-ZACH-WILSON",
 "CHAR-PHILLIP-PITTS", "CHAR-BEN-WHIPPLE", "CHAR-DAVID-BABB",
 "CHAR-BRANDON-PRYOR", "CHAR-BOBBY-MITCHELL", "CHAR-KEVIN-ZEEK",
 "CHAR-JORDAN-HOLLINGSHEAD", "CHAR-WILSON-LOOK", "CHAR-MANNING-WELTY",
}

def blob(path):
 data=path.read_bytes()
 return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()

def words(text):
 return len(text.split())

class WilsonSingleDepartureDevelopmentalReader(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.chapter=CHAPTER.read_text(encoding="utf-8")
  cls.reader=READER.read_text(encoding="utf-8")
  cls.previous=PREVIOUS.read_text(encoding="utf-8")
  cls.old=OLD.read_text(encoding="utf-8")
  cls.bridge=BRIDGE.read_text(encoding="utf-8")
  cls.wrap=list(WRAP.finditer(cls.reader))
  cls.oldwrap=list(WRAP.finditer(cls.previous))
  cls.rows=ROW.findall(cls.reader.split("| Part | Principal viewpoint",1)[1].split("\n\n**Total:",1)[0])
  cls.story=cls.chapter.split("## Source and editorial receipt",1)[0]

 def test_01_previous_reader_preserved(self):
  self.assertEqual(blob(PREVIOUS),PREVIOUS_SHA)
 def test_02_new_reader_pinned(self):
  self.assertEqual(blob(READER),READER_SHA)
 def test_03_integrated_source_pinned(self):
  self.assertEqual(blob(CHAPTER),CHAPTER_SHA)
 def test_04_original_wilson_sources_immutable(self):
  self.assertEqual(blob(OLD),OLD_SHA)
  self.assertEqual(blob(BRIDGE),BRIDGE_SHA)
 def test_05_2016_full_reader_immutable(self):
  self.assertEqual(blob(READER_2016),READER_2016_SHA)
 def test_06_protected_2026_manuscript_unchanged(self):
  for name,digest in PROTECTED.items():
   with self.subTest(path=name):
    self.assertEqual(blob(ROOT/name),digest)
 def test_07_eleven_assembled_parts(self):
  self.assertEqual(len(self.wrap),11)
  self.assertEqual(len(self.oldwrap),12)
 def test_08_part_headings_consecutive(self):
  self.assertEqual([int(v) for v in re.findall(r"^## Part (\d+) —",self.reader,re.M)],list(range(1,12)))
 def test_09_every_wrapper_matches_git_source(self):
  for m in self.wrap:
   with self.subTest(file=m.group(1)):
    f=BASE/m.group(1)
    self.assertTrue(f.exists())
    self.assertEqual(m.group(1),m.group(4))
    self.assertEqual(blob(f),m.group(2))
    self.assertEqual(f.read_text(encoding="utf-8").rstrip("\n"),m.group(3))
 def test_10_unmodified_ten_wrappers(self):
  expected=[m.group(0) for i,m in enumerate(self.oldwrap) if i not in (6,7)]
  actual=[m.group(0) for i,m in enumerate(self.wrap) if i!=6]
  self.assertEqual(actual,expected)
 def test_11_integrated_replaces_two_slots_once(self):
  self.assertEqual(self.wrap[6].group(1),CHAPTER.name)
  self.assertEqual(self.wrap[6].group(2),CHAPTER_SHA)
  self.assertNotIn(OLD.name,[m.group(1) for m in self.wrap])
  self.assertNotIn(BRIDGE.name,[m.group(1) for m in self.wrap])
 def test_12_manifest_rows_exact(self):
  self.assertEqual(len(self.rows),11)
  for i,row in enumerate(self.rows):
   with self.subTest(index=i):
    self.assertEqual(int(row[0]),i+1)
    self.assertEqual(row[2],self.wrap[i].group(1))
    self.assertEqual(row[3],self.wrap[i].group(2))
    self.assertEqual(int(row[4]),words(self.wrap[i].group(3)))
 def test_13_total_source_words(self):
  self.assertEqual(sum(int(r[4]) for r in self.rows),63738)
  self.assertIn("63738 source words",self.reader)
 def test_14_integrated_chapter_substantial(self):
  self.assertEqual(words(self.chapter),10332)
  self.assertGreater(words(self.chapter),10000)
 def test_15_twelve_canonical_owners_covered(self):
  ids=set(re.findall(r"CHAR-[A-Z]+(?:-[A-Z]+)*"," ".join(x[1] for x in self.rows)))
  self.assertEqual(ids,OWNERS)
 def test_16_eleven_ordered_movement_sections(self):
  self.assertEqual(re.findall(r"^### ([IVX]+)\.",self.story,re.M),
                   ["I","II","III","IV","V","VI","VII","VIII","IX","X","XI"])
 def test_17_one_company_departure_no_intercut_warning(self):
  self.assertEqual(self.story.count("The procession moved."),1)
  self.assertNotIn("### VI. The missing platform",self.story)
  self.assertNotIn("Deliberate story-time intercut:",self.story)
  self.assertNotIn("He did not own the bend. He did not need to.",self.story)
 def test_18_broken_timber_and_single_inspected_crossing(self):
  self.assertIn("The first wagon had gone.",self.story)
  self.assertIn("NO CLEARANCE FOR FURTHER LOADED CROSSING",self.story)
  self.assertIn("SECOND LOADED WAGON HELD",self.story)
 def test_19_material_driver_loss_not_silently_paid(self):
  self.assertIn("### IX. The charge for a lost day",self.story)
  self.assertIn("I want a record of what the delay costs",self.story)
  self.assertIn("He had been offered no compensation",self.story)
 def test_20_no_invented_road_authority(self):
  self.assertIn("Nothing signed here appoints you.",self.story)
  self.assertIn("The disputed toll board remains without legal foundation.",self.chapter)
 def test_21_no_period_manager_identity_certification(self):
  self.assertIn("manager-account identity has **not been authenticated**",self.chapter)
  self.assertIn("no scores or fixtures are invented",self.chapter)
 def test_22_provisional_atlas_and_character_disclaimer(self):
  self.assertIn("period Character Canon approval",self.reader)
  self.assertIn("proposed secondary-world fiction",self.reader)
 def test_23_unknown_silhouettes_not_rebranded_enemy(self):
  self.assertIn("three indistinct figures",self.story)
  self.assertIn("declined a search",self.story)
 def test_24_original_causal_consequences_preserved(self):
  self.assertIn("Jordan's two owed hours are paid by Jordan",self.chapter)
  self.assertIn("The watch's older wage debt",self.story)
  self.assertIn("four agreed wages",self.story)
 def test_25_hard_canon_and_approval_gates_explicit(self):
  self.assertIn("2026 protected Prologue and Chapters I–III stay unmodified",self.chapter)
  self.assertIn("Only genuine historical, Character Canon, Atlas, Authors Council and Umpire reviews",self.chapter)

if __name__=="__main__":
 unittest.main()
