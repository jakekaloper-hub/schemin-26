"""2016 18-part source-exact developmental reader — Chapter XXI V2, noncanon."""
from __future__ import annotations
import hashlib
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
D=ROOT/"living-novel/historical-chronicle/seasons/2016/causal-novel"
OLD=D/"READING_COPY_2016_CAUSAL_CH01_20_SEVENTEEN_PARTS_MARA_DEPARTURE_NONCANON.md"
NEW=D/"READING_COPY_2016_CAUSAL_CH01_21_EIGHTEEN_PARTS_BLANK_LEAF_V2_NONCANON.md"
CH=D/"THE_BOOK_THAT_WALKED_OUT_PRICE_OF_A_BLANK_LEAF_CH21_V2_NONCANON.md"
ORIGINAL=D/"THE_BOOK_THAT_WALKED_OUT_CHAPTER_21_NONCANON.md"

def blob(data:bytes)->str:
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\\x00"+data).hexdigest()

def rows(text:str):
    return [(int(n),f,h,int(words)) for n,f,h,words in re.findall(
        r"^\\| (\\d+) \\| \\x60([^\\x60]+)\\x60 \\| \\x60([a-f0-9]{40})\\x60 \\| (\\d+) \\|$",text,re.M)]

def embedded(text:str,filename:str,source_sha:str)->str:
    return text.split(f"<!-- BEGIN 2016_CAUSAL {filename} | git_blob {source_sha} -->\\n\\n",1)[1].split(
        f"\\n\\n<!-- END 2016_CAUSAL {filename} -->",1)[0]

class ChapterXXIEighteenPartReader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old=OLD.read_text()
        cls.new=NEW.read_text()
        cls.chapter=CH.read_text()
        cls.original=ORIGINAL.read_text()
        cls.prev_rows=rows(cls.old)
        cls.rows=rows(cls.new)

    def test_01_reader_previous_blob_pinned(self):
        self.assertEqual(blob(OLD.read_bytes()),"5f47a961ca4cecd8000b8c104722bb41beff076c")

    def test_02_manifest_sequence(self):
        self.assertEqual([n for n,*_ in self.rows],list(range(1,19)))

    def test_03_old_manifest_unchanged(self):
        self.assertEqual(self.rows[:17],self.prev_rows)

    def test_04_original_chapter_remains_untouched(self):
        self.assertEqual(blob(ORIGINAL.read_bytes()),"6badbdcaa4bad10313cb5de6ccbca8711c24a4e4")

    def test_05_all_source_hashes_and_counts(self):
        for n,f,h,word_count in self.rows:
            with self.subTest(part=n):
                raw=(D/f).read_bytes()
                self.assertEqual(blob(raw),h)
                self.assertEqual(len(raw.decode().split()),word_count)

    def test_06_all_reader_bodies_exact(self):
        for n,f,h,word_count in self.rows:
            with self.subTest(part=n):
                self.assertEqual(embedded(self.new,f,h),(D/f).read_text().rstrip("\\n"))

    def test_07_previous_seventeen_bodies_exact(self):
        for n,f,h,w in self.prev_rows:
            with self.subTest(part=n):
                self.assertEqual(embedded(self.new,f,h),embedded(self.old,f,h))

    def test_08_total_source_words(self):
        self.assertEqual(sum(row[3] for row in self.rows),119925)
        self.assertIn("Source words including chapter metadata: 119925",self.new)

    def test_09_revised_chapter_words_and_new_scene(self):
        self.assertEqual(len(self.chapter.split()),8041)
        self.assertIn("#### The price of a blank leaf",self.chapter)
        self.assertIn("Nell states:",self.chapter)

    def test_10_material_payment_not_full_settlement(self):
        self.assertIn('"One delivered," she said. "One waiting. Write it that way."',self.chapter)
        self.assertIn("Not the whole of what Nell says she's owed.",self.chapter)

    def test_11_esi_decides_independently(self):
        self.assertIn('"You may take them," Esi replied.',self.chapter)
        self.assertIn("Esi put the new page beside the witness statements",self.chapter)

    def test_12_maraless_shelter_and_ledger_unchanged(self):
        self.assertIn("Mara's wagon had been gone for three hours",self.chapter)
        self.assertIn("The larger bound book was gone.",self.chapter)
        self.assertIn("The private file with the missing claimant's original mark was elsewhere",self.chapter)

    def test_13_owner_pov_and_metadata_firewall(self):
        self.assertIn("Sole limited interior viewpoint: proposed fictional Jake",self.chapter)
        self.assertIn("not authenticated 2016 ESPN facts",self.chapter)
        self.assertIn("No new historical ESPN fact",self.chapter)

    def test_14_editorial_and_release_holds(self):
        self.assertIn("NONCANON",self.new)
        self.assertIn("NO MERGE",self.new)
        self.assertIn("NO PUBLICATION",self.new)
        self.assertIn("independent literary",self.new.lower())

    def test_15_protected_hard_canon(self):
        expected={
            "PROLOGUE_DRAFT_V1.md":"5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
            "CHAPTER_01_THE_FIRST_ANSWER.md":"26a17f05eb0565e7648c29add03ee9580ec933c3",
            "CHAPTER_02_WHAT_COMES_BACK.md":"30fcf23a3eb8872fa0fb4dff029fe30044141121",
            "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md":"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
        }
        for f,sha in expected.items():
            with self.subTest(f=f):
                self.assertEqual(blob((ROOT/"living-novel/manuscript"/f).read_bytes()),sha)

    def test_16_frozen_historical_evidence(self):
        p=ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(blob(p.read_bytes()),"6dbec1fe2537139f3a97c6a78250e2bae082a518")

    def test_17_reader_is_developmental_only(self):
        self.assertIn("18-Part Developmental Reading",self.new)
        self.assertIn("FOUNDER-ONLY CANON AND PUBLICATION GATE",self.new)
        self.assertIn("Historical manager-slot authentication",self.new)

if __name__=="__main__":
    unittest.main()
