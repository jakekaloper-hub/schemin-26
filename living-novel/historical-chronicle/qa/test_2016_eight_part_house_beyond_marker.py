"""Mechanical source-exact checks: 2016 developmental Chapters I–XI eight-part book."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/"living-novel/historical-chronicle/seasons/2016/causal-novel"
EIGHT=BASE/"READING_COPY_2016_CAUSAL_CH01_11_EIGHT_PARTS_HOUSE_BEYOND_MARKER_NONCANON.md"
SEVEN=BASE/"READING_COPY_2016_CAUSAL_CH01_10_SEVEN_PARTS_SOUND_FACE_V2_NONCANON.md"
XI=BASE/"THE_HOUSE_BEYOND_THE_MARKER_CHAPTER_11_NONCANON.md"
EIGHT_SHA="737789cff129d4bf5409c8ba5d1fc1ab85cfdb26"
SEVEN_SHA="59a7f7d37068853330d85732963315f2a16cfdc4"
XI_SHA="94c81b98a9dc9d308a8d2d4801e7482a1a170f74"
WRAP=re.compile(r"<!-- BEGIN 2016_CAUSAL ([^\n]+) \| git_blob ([0-9a-f]{40}) -->\n\n([\s\S]*?)\n\n<!-- END 2016_CAUSAL ([^\n]+) -->")
ROW=re.compile(r"^\| (\d+) \| `([^`]+)` \| `([0-9a-f]{40})` \| (\d+) \|$",re.M)
PROTECTED={
"living-novel/manuscript/PROLOGUE_DRAFT_V1.md":"5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
"living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md":"26a17f05eb0565e7648c29add03ee9580ec933c3",
"living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md":"30fcf23a3eb8872fa0fb4dff029fe30044141121",
"living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md":"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc"
}
def blob(p):
    data=p.read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

class EightPartHouseBeyondMarker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.book=EIGHT.read_text(encoding="utf-8")
        cls.earlier=SEVEN.read_text(encoding="utf-8")
        cls.wraps=WRAP.findall(cls.book)
        cls.oldwraps=WRAP.findall(cls.earlier)
        cls.rows=ROW.findall(cls.book.split("## Part 1 —",1)[0])

    def test_01_edition_pinned(self): self.assertEqual(blob(EIGHT),EIGHT_SHA)
    def test_02_prior_edition_pinned(self): self.assertEqual(blob(SEVEN),SEVEN_SHA)
    def test_03_xi_original_pinned(self): self.assertEqual(blob(XI),XI_SHA)

    def test_04_eight_source_exact_bodies_and_manifest(self):
        self.assertEqual(len(self.wraps),8)
        self.assertEqual(len(self.rows),8)
        for idx,(wrap,row) in enumerate(zip(self.wraps,self.rows),1):
            with self.subTest(part=idx):
                name,sha,body,end=wrap
                self.assertEqual(end,name)
                self.assertEqual((int(row[0]),row[1],row[2]),(idx,name,sha))
                data=(BASE/name).read_text(encoding="utf-8")
                self.assertEqual(blob(BASE/name),sha)
                self.assertEqual(body,data.rstrip("\n"))
                self.assertEqual(int(row[3]),len(data.split()))

    def test_05_first_seven_exactly_preserved(self): self.assertEqual(self.wraps[:7],self.oldwraps)

    def test_06_eighth_part_is_unmodified_xi(self):
        self.assertEqual(self.wraps[7][0],XI.name)
        self.assertEqual(self.wraps[7][1],XI_SHA)
        self.assertEqual(self.wraps[7][2],XI.read_text(encoding="utf-8").rstrip("\n"))

    def test_07_source_word_math(self):
        words=sum(int(r[3]) for r in self.rows)
        self.assertEqual(words,48813)
        self.assertIn("48813",self.book)
        self.assertEqual(int(self.rows[-1][3]),5490)

    def test_08_water_jars_reconcile_with_next_morning(self):
        self.assertLess(self.book.index("The water jars need carrying"),self.book.index("By the time Jake had carried the second water jar"))

    def test_09_departure_does_not_resolve_claimant(self):
        for phrase in ["old woman's family", "is not reidentified as claimant", "message unopened", "east-room chest unretrieved"]:
            self.assertIn(phrase.lower(),self.book.lower())

    def test_10_exclusive_owner_pov(self):
        self.assertIn("CHAR-JAKE-KALOPER",self.book)
        self.assertNotRegex(self.book,r"(?m)^### (?:Edrin|Edin|Oren)\b")

    def test_11_no_canon_promotion(self):
        for phrase in ["NONCANON","NO MERGE","NO PUBLICATION","NO CANON PROMOTION","UMPIRE HOLD","FOUNDER-ONLY"]:
            self.assertIn(phrase,self.book)

    def test_12_protected_main_contract(self):
        for name,sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(blob(ROOT/name),sha)

if __name__=="__main__":
    unittest.main()
