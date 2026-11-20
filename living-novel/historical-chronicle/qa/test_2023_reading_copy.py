"""Guard the 2023 NONCANON full regular-season reading copy against source drift.

Technical concordance is not Author Council, Atlas, Umpire or Founder approval.
The copy is a derived reading artifact; original chapter files retain authority.
"""
import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE=Path("living-novel/historical-chronicle/seasons/2023")
READING=ROOT/BASE/"READING_COPY_REGULAR_SEASON_NONCANON.md"
ARCHIVE=ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2023_FULL_WEEKLY_MATCHUPS.json"
CONTINUITY=ROOT/BASE/"CONTINUITY.json"
EXPECTED=[str(BASE/"PROLOGUE.md")]+[str(BASE/"weeks"/f"W{i:02}.md") for i in range(1,15)]
PROTECTED={
 "PROLOGUE_DRAFT_V1.md":"5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
 "CHAPTER_01_THE_FIRST_ANSWER.md":"26a17f05eb0565e7648c29add03ee9580ec933c3",
 "CHAPTER_02_WHAT_COMES_BACK.md":"30fcf23a3eb8872fa0fb4dff029fe30044141121",
 "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md":"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}
SOURCE_SHA="ded119cde5c660f87f197f269b8d6ddd2a11316a"
TAG=re.compile(
    r"<!-- SOURCE_BEGIN (?P<path>\S+) (?P<sha>[0-9a-f]{40}) -->\n\n"
    r"(?P<body>.*?)\n\n<!-- SOURCE_END (?P=path) -->", re.DOTALL,
)

def blob(path):
    data=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

class Test2023ReadingCopy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text=READING.read_text(encoding="utf-8")
        cls.sections=list(TAG.finditer(cls.text))
        cls.cont=json.loads(CONTINUITY.read_text(encoding="utf-8"))
        cls.archive=json.loads(ARCHIVE.read_text(encoding="utf-8"))

    def test_all_fifteen_original_manuscripts_in_source_order(self):
        self.assertEqual(len(self.sections),15)
        self.assertEqual([s.group("path") for s in self.sections], EXPECTED)
        self.assertEqual(self.text.count("<!-- SOURCE_BEGIN "),15)
        self.assertEqual(self.text.count("<!-- SOURCE_END "),15)

    def test_assembled_chapters_byte_equivalent_after_only_trailing_trim(self):
        for section in self.sections:
            with self.subTest(path=section.group("path")):
                source=(ROOT/section.group("path")).read_text(encoding="utf-8")
                self.assertEqual(section.group("body"),source.rstrip())

    def test_every_assembly_header_pins_unchanged_source_sha(self):
        for section in self.sections:
            with self.subTest(path=section.group("path")):
                self.assertEqual(section.group("sha"),blob(ROOT/section.group("path")))
                self.assertIn(f'| `{section.group("path")}` | `{section.group("sha")}` |',self.text)

    def test_noncanonical_boundary_not_cloaked_as_book_one_release(self):
        header=self.text.split("<!-- BEGIN_COMPILED_MANUSCRIPT -->",1)[0]
        for phrase in ("NONCANON","Not canon","not published","Historical human-owner lineage remains unverified",
                       "Postseason NOT VERIFIED / NOT DRAFTED","Source snapshot"):
            self.assertIn(phrase.lower(),header.lower())
        self.assertIn("<!-- END_COMPILED_MANUSCRIPT -->",self.text)

    def test_full_season_84_source_results_without_claiming_postseason(self):
        self.assertEqual(blob(ARCHIVE),SOURCE_SHA)
        self.assertEqual(self.archive["source"],"Flaim ESPN 1417621")
        weeks=self.archive["weeks"][:14]
        self.assertEqual([w["week"] for w in weeks],list(range(1,15)))
        self.assertEqual(sum(len(w["matchups"]) for w in weeks),84)
        c=self.cont
        self.assertEqual(c["matchup_coverage"]["regular_season_matchups_covered"],84)
        self.assertEqual(c["matchup_coverage"]["prose_entries"],84)
        self.assertEqual(c["matchup_coverage"]["postseason"],"NOT_DRAFTED")
        self.assertEqual(c["source"]["owner_identity"],"UNVERIFIED")

    def test_more_than_seventy_thousand_source_words_no_invented_extra_story(self):
        word_counts=[len((ROOT/p).read_text(encoding="utf-8").split()) for p in EXPECTED]
        self.assertGreaterEqual(sum(word_counts),73000)
        self.assertEqual(len(word_counts),15)
        self.assertEqual(self.text.count("<!-- BEGIN_COMPILED_MANUSCRIPT -->"),1)

    def test_compiled_body_boundaries_in_order(self):
        self.assertLess(self.text.index("<!-- BEGIN_COMPILED_MANUSCRIPT -->"),self.sections[0].start())
        self.assertLess(self.sections[-1].end(),self.text.index("<!-- END_COMPILED_MANUSCRIPT -->"))
        self.assertEqual(len({s.group("path") for s in self.sections}),15)

    def test_2026_protected_hard_canon_untouched(self):
        for name,sha in PROTECTED.items():
            with self.subTest(protected=name):
                self.assertEqual(blob(ROOT/"living-novel/manuscript"/name),sha)

if __name__=="__main__":
    unittest.main()
