"""Noncanonical 2025 Austin–Phillip V4 assembled-manuscript mechanical regression suite.
Passing tests do not imply independent literature, Atlas or Umpire acceptance.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"living-novel/historical-chronicle/seasons/2025/causal-novel"
CHAPTER=BASE/"THE_SEATS_THAT_COULD_BE_EMPTY_AUSTIN_PHILLIP_2025_DEVELOPMENTAL_V2_NONCANON.md"
READER=BASE/"READING_COPY_2025_TWELVE_VOICES_ELEVEN_PARTS_AUSTIN_PHILLIP_REVISION_V4_NONCANON.md"
PREVIOUS=BASE/"READING_COPY_2025_TWELVE_VOICES_ELEVEN_PARTS_WILSON_COMPRESSION_V3_NONCANON.md"
ORIGINAL=BASE/"THE_ROOM_WITHOUT_A_STAGE_AUSTIN_PHILLIP_2025_NONCANON.md"
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
    content=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(content)).encode()+b"\x00"+content).hexdigest()

class AustinPhillipV4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter=CHAPTER.read_text(encoding="utf-8")
        cls.reader=READER.read_text(encoding="utf-8")
        cls.previous=PREVIOUS.read_text(encoding="utf-8")
        cls.parts=list(WRAP.finditer(cls.reader))
        cls.oldparts=list(WRAP.finditer(cls.previous))
        cls.rows=ROW.findall(cls.reader.split("## Part 1 —",1)[0])

    def test_01_pinned_chapter_and_reader(self):
        self.assertEqual(blob(CHAPTER),"40616ead56c9f10d94ce122caaa05493db3db924")
        self.assertEqual(blob(READER),"b3ff6735553912ce4c89b5f825767592d6f6180a")
        self.assertEqual(blob(PREVIOUS),"bf47f2bc09bd31500487409fd220a4e818fd1671")
        self.assertEqual(blob(ORIGINAL),"feb66c8f68d83aa9c9b4b6c2e6e7cc755103b116")

    def test_02_protected_2026_opening(self):
        for p,sha in PROTECTED.items():
            with self.subTest(p=p): self.assertEqual(blob(ROOT/p),sha)

    def test_03_exact_source_wrappers(self):
        self.assertEqual(len(self.parts),11)
        self.assertEqual(len(self.rows),11)
        for n,(w,row) in enumerate(zip(self.parts,self.rows),1):
            slot,_,name,sha,words=row
            source=BASE/name
            with self.subTest(part=n):
                self.assertEqual(int(slot),n)
                self.assertEqual(w.group(1),name)
                self.assertEqual(w.group(4),name)
                self.assertEqual(w.group(2),sha)
                self.assertEqual(blob(source),sha)
                self.assertEqual(w.group(3),source.read_text(encoding="utf-8").rstrip("\n"))
                self.assertEqual(len(source.read_text(encoding="utf-8").split()),int(words))

    def test_04_ten_other_wrappers_unchanged(self):
        self.assertEqual(len(self.oldparts),11)
        self.assertEqual([w.group(0) for i,w in enumerate(self.parts) if i!=9],
                         [w.group(0) for i,w in enumerate(self.oldparts) if i!=9])

    def test_05_part_ten_only_replacement(self):
        self.assertEqual(self.parts[9].group(1),CHAPTER.name)
        self.assertEqual(sum(w.group(1)==CHAPTER.name for w in self.parts),1)
        self.assertNotEqual(self.parts[9].group(1),self.oldparts[9].group(1))

    def test_06_word_totals(self):
        self.assertEqual(len(self.chapter.split()),5390)
        self.assertEqual(sum(int(row[4]) for row in self.rows),63935)
        self.assertIn("63935 source words",self.reader)

    def test_07_twelve_exclusive_owner_ids(self):
        ids=set(re.findall(r"CHAR-[A-Z0-9-]+"," ".join(r[1] for r in self.rows)))
        self.assertEqual(ids,OWNERS)

    def test_08_six_alternating_pov_movements(self):
        prose=self.chapter.split("### Production and source boundary",1)[0]
        self.assertEqual(re.findall(r"^### ([IVX]+)\. ",prose,re.M),["I","II","III","IV","V","VI"])
        self.assertIn("Austin → Phillip → Austin → Phillip → Austin → Phillip",self.chapter)

    def test_09_material_household_cost(self):
        lower=self.chapter.lower()
        for p in ["the west gallery was closed","take the amount from the household reserve",
                  "there were no funds left beside the shutter-irons entry"]:
            self.assertIn(p,lower)

    def test_10_tangible_troupe_cost(self):
        lower=self.chapter.lower()
        for p in ["the carpenter began unfastening the back",
                  "the other debts remained exactly where they had been",
                  "three people who had been promised their wages tonight",
                  "we cannot take the planned route tomorrow"]:
            self.assertIn(p,lower)

    def test_11_audience_can_refuse(self):
        lower=self.chapter.lower()
        for p in ["can i leave?","yes.","whoever wants warmth without a play",
                  "eleven people had chosen to sit"]:
            self.assertIn(p,lower)

    def test_12_three_heads_one_body(self):
        self.assertIn("one bodily being with exactly three serpent heads",self.chapter)
        self.assertIn("The three directions belonged to one attention",self.chapter)

    def test_13_evidence_and_atlas_firewall(self):
        self.assertIn("provisional, not authenticated",self.chapter)
        self.assertIn("no period Atlas location is established",self.chapter)
        self.assertIn("No new game, score, trade",self.chapter)

    def test_14_noncanon_release_hold(self):
        self.assertIn("NONCANON",self.chapter)
        self.assertIn("independent Authors Council",self.chapter)
        self.assertIn("NO MERGE / NO PUBLICATION / NO CANON PROMOTION",self.chapter)

if __name__=="__main__":
    unittest.main()
