"""2025 measured-service source-exact reading — mechanical and provenance checks only.
PASS does not signify Founder, historical, Atlas, literary, or Umpire acceptance.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"living-novel/historical-chronicle/seasons/2025/causal-novel"
CHAPTER=BASE/"THE_DAY_THE_POT_WENT_COLD_BEN_DAVID_2025_DEVELOPMENTAL_V2_NONCANON.md"
READER=BASE/"READING_COPY_2025_TWELVE_VOICES_ELEVEN_PARTS_MEASURED_SERVICE_V5_NONCANON.md"
PREVIOUS=BASE/"READING_COPY_2025_TWELVE_VOICES_ELEVEN_PARTS_AUSTIN_PHILLIP_REVISION_V4_NONCANON.md"
ORIGINAL=BASE/"THE_DAY_THE_POT_WENT_COLD_BEN_DAVID_2025_NONCANON.md"
WRAP=re.compile(r"<!-- BEGIN 2025_VOICE ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n([\s\S]*?)\n\n<!-- END 2025_VOICE ([^\n]+) -->")
ROW=re.compile(r"^\| (\d+) \| ([^|]+) \| \x60([^\x60]+)\x60 \| \x60([0-9a-f]{40})\x60 \| (\d+) \|$",re.M)
OWNERS={"CHAR-AUSTIN-BYARS","CHAR-JAKE-KALOPER","CHAR-ZACH-WILSON",
"CHAR-PHILLIP-PITTS","CHAR-BEN-WHIPPLE","CHAR-DAVID-BABB",
"CHAR-BRANDON-PRYOR","CHAR-BOBBY-MITCHELL","CHAR-KEVIN-ZEEK",
"CHAR-JORDAN-HOLLINGSHEAD","CHAR-WILSON-LOOK","CHAR-MANNING-WELTY"}
PROTECTED={
"living-novel/manuscript/PROLOGUE_DRAFT_V1.md":"5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
"living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md":"26a17f05eb0565e7648c29add03ee9580ec933c3",
"living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md":"30fcf23a3eb8872fa0fb4dff029fe30044141121",
"living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md":"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc"}

def blob(path):
    data=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\x00"+data).hexdigest()

class MeasuredServiceV5(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter=CHAPTER.read_text(encoding="utf-8")
        cls.reader=READER.read_text(encoding="utf-8")
        cls.previous=PREVIOUS.read_text(encoding="utf-8")
        cls.parts=list(WRAP.finditer(cls.reader))
        cls.prevparts=list(WRAP.finditer(cls.previous))
        cls.rows=ROW.findall(cls.reader.split("## Part 1 —",1)[0])

    def test_01_pinned_edition_and_preserved_original(self):
        self.assertEqual(blob(CHAPTER),"f38bc57bdf828a8fa7607b1717448cf283a6ce24")
        self.assertEqual(blob(READER),"3dbf0047e81174b203a63b80797894d2f9ccfbe6")
        self.assertEqual(blob(PREVIOUS),"b3ff6735553912ce4c89b5f825767592d6f6180a")
        self.assertEqual(blob(ORIGINAL),"862d0a9dab9a546a1e110fbc45c474d174b127c3")

    def test_02_protected_2026_files_unchanged(self):
        for rel,sha in PROTECTED.items():
            with self.subTest(rel=rel): self.assertEqual(blob(ROOT/rel),sha)

    def test_03_exact_eleven_wrappers_and_manifest(self):
        self.assertEqual(len(self.parts),11)
        self.assertEqual(len(self.rows),11)
        for i,(wrap,row) in enumerate(zip(self.parts,self.rows),1):
            slot,_,name,sha,words=row
            source=BASE/name
            with self.subTest(i=i):
                self.assertEqual(int(slot),i)
                self.assertEqual(name,wrap.group(1))
                self.assertEqual(name,wrap.group(4))
                self.assertEqual(sha,wrap.group(2))
                self.assertEqual(blob(source),sha)
                self.assertEqual(wrap.group(3),source.read_text(encoding="utf-8").rstrip("\n"))
                self.assertEqual(len(source.read_text(encoding="utf-8").split()),int(words))

    def test_04_previous_ten_wrappers_identical(self):
        self.assertEqual(len(self.prevparts),11)
        self.assertEqual([p.group(0) for p in self.parts[:10]],
                         [p.group(0) for p in self.prevparts[:10]])

    def test_05_only_part_eleven_is_new(self):
        self.assertEqual(self.parts[10].group(1),CHAPTER.name)
        self.assertNotEqual(self.parts[10].group(1),self.prevparts[10].group(1))
        self.assertEqual(sum(w.group(1)==CHAPTER.name for w in self.parts),1)

    def test_06_source_word_arithmetic(self):
        self.assertEqual(len(self.chapter.split()),7924)
        self.assertEqual(sum(int(row[4]) for row in self.rows),65940)
        self.assertIn("65940 source words",self.reader)

    def test_07_twelve_canonical_owner_ids_only(self):
        ids=set(re.findall(r"CHAR-[A-Z0-9-]+"," ".join(row[1] for row in self.rows)))
        self.assertEqual(ids,OWNERS)

    def test_08_six_ben_david_movements(self):
        main=self.chapter.split("### Source and editorial handoff",1)[0]
        self.assertEqual(re.findall(r"^### ([IVX]+)\. ",main,re.M),["I","II","III","IV","V","VI"])
        self.assertEqual(re.findall(r"^### [IVX]+\. [^\n]+ — ([^\n]+)",main,re.M),
                         ["Ben","David","Ben","David","Ben","David"])

    def test_09_worker_choice_without_celebrity_takeover(self):
        for t in ["I cannot begin by calling their work settled",
                  "He kept his hands on the bucket handle",
                  "Maren nodded once"]:
            self.assertIn(t,self.chapter)

    def test_10_wages_and_service_remain_distinct(self):
        for t in ["The hours were disputed","I am here","she could not take the next turn",
                  "No steward claimed the choice had canceled the arrears"]:
            self.assertIn(t,self.chapter)

    def test_11_actual_serving_not_authorized_serving(self):
        for t in ["Write the quantity authorized","Leave another for those who came too late",
                  "not mark it served until the person received it",
                  "The next bowl was measured"]:
            self.assertIn(t,self.chapter)

    def test_12_financial_and_scarcity_negative_gates(self):
        prose=self.chapter.lower()
        for t in ["accepted quantity","unsettled remainder","two notices",
                  "future grain pledges","does not promise new funds"]:
            self.assertIn(t,prose)

    def test_13_closing_defers_broad_resolution(self):
        self.assertIn("It was supper for some",self.chapter)
        self.assertIn("account of who could answer back",self.chapter)
        self.assertIn("The seventh stool remained occupied",self.chapter)

    def test_14_historical_and_atlas_hold(self):
        t=self.chapter.lower()
        self.assertIn("do not authenticate ben whipple or david babb",t)
        self.assertIn("atlas-unapproved",t)
        self.assertIn("no merge",t)

    def test_15_part10_part11_only_thematic_not_spatial_join(self):
        t=self.reader.lower().split("## part 1 —",1)[0]
        self.assertIn("thematic edit",t)
        self.assertIn("not an approved geographical route",t)
        self.assertIn("ten",t)

    def test_16_independent_and_founder_gates_retained(self):
        prelude=self.reader.split("## Part 1 —",1)[0]
        for t in ["DRAFT / NONCANON","INDEPENDENT AUTHORS COUNCIL","NO PUBLICATION OR CANON PROMOTION",
                  "historical manager accounts"]:
            self.assertIn(t.lower(),prelude.lower())

if __name__=="__main__":
    unittest.main()
