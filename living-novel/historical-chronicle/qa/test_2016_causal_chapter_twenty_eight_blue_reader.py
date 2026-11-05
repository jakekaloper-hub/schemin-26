"""Source-pinned 2016 Chapter XXVIII V2 and twenty-five-part noncanon reader."""
import hashlib
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CH = "THE_SLEEVE_LEFT_UNSTITCHED_BLUE_THAT_DID_NOT_AGREE_CH28_V2_NONCANON.md"
OLD_CH = "THE_SLEEVE_LEFT_UNSTITCHED_CHAPTER_28_NONCANON.md"
READER = "READING_COPY_2016_CAUSAL_CH01_28_TWENTY_FIVE_PARTS_BLUE_WITH_TWO_SHADOWS_NONCANON.md"
PRIOR = "READING_COPY_2016_CAUSAL_CH01_27_TWENTY_FOUR_PARTS_FISH_AND_RIVER_V2_NONCANON.md"
CH_SHA = "97fe018a47056a6f5af487175476bf77e259167b"
OLD_CH_SHA = "47a8475c2029f5b5b8222adfc72d2a4d17760da0"
PRIOR_SHA = "0691e5169697d68b208a28680b0ee04f2707c2fa"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
 "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
 "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
 "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
 "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def rows(text):
    return [(int(i), p, s, int(w)) for i,p,s,w in re.findall(
       r"^\| (\d+) \| \x60([^\x60]+)\x60 \| \x60([0-9a-f]{40})\x60 \| (\d+) \|$", text, re.M)]

def part(text, filename, sha):
    start = "<!-- BEGIN 2016_CAUSAL " + filename + " | git_blob " + sha + " -->"
    end = "<!-- END 2016_CAUSAL " + filename + " -->"
    assert text.count(start) == 1, filename
    assert text.count(end) == 1, filename
    return text.split(start+"\n\n", 1)[1].split("\n\n"+end, 1)[0]

class ChapterTwentyEightV2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = (BASE / CH).read_text()
        cls.prior = (BASE / PRIOR).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.original = (BASE / OLD_CH).read_text()

    def test_01_exact_pinned_new_chapter_sha(self):
        self.assertEqual(blob(BASE / CH), CH_SHA)

    def test_02_preserve_original_chapter_source(self):
        self.assertEqual(blob(BASE / OLD_CH), OLD_CH_SHA)

    def test_03_reader_prior_pin(self):
        self.assertEqual(blob(BASE / PRIOR), PRIOR_SHA)

    def test_04_six_story_movements(self):
        self.assertEqual(re.findall(r"^### ([IVX]+)\. ", self.chapter, re.M), ["I","II","III","IV","V","VI"])

    def test_05_scene_substantial_and_no_phantom_resolutions(self):
        piece = self.chapter.split("### IV. The blue that did not agree with itself",1)[1].split("### V. The commission at the open window",1)[0]
        self.assertEqual(len(("### IV. The blue that did not agree with itself" + piece).split()), 1902)
        self.assertIn("The roll was still a problem", piece)
        self.assertIn("You won't touch the full roll yet", piece)

    def test_06_reader_markers(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 25)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 25)

    def test_07_manifest_rows_and_order(self):
        data = rows(self.reader)
        self.assertEqual(len(data), 25)
        self.assertEqual([i for i,_,_,_ in data], list(range(1,26)))
        self.assertEqual((data[-1][1],data[-1][2],data[-1][3]), (CH,CH_SHA,7831))

    def test_08_all_twenty_five_parts_exact_match(self):
        for i,filename,sha,words in rows(self.reader):
            source = (BASE/filename).read_text()
            with self.subTest(part=i, filename=filename):
                self.assertEqual(blob(BASE/filename),sha)
                self.assertEqual(len(source.split()),words)
                self.assertEqual(part(self.reader,filename,sha),source.rstrip("\n"))

    def test_09_prior_24_embedded_bodies_identical(self):
        for i,filename,sha,_ in rows(self.reader)[:24]:
            with self.subTest(part=i):
                self.assertEqual(part(self.reader,filename,sha),part(self.prior,filename,sha))

    def test_10_total_source_words(self):
        self.assertEqual(sum(w for _,_,_,w in rows(self.reader)),173850)
        self.assertIn("Source component words including metadata: 173850", self.reader)

    def test_11_limited_proposed_owner_and_evidence_firewall(self):
        for expected in ("Sole limited interior viewpoint", "This is NOT an authenticated historical ESPN owner-slot association", "The kiln passage remains closed", "delivery to Esi remains unconfirmed"):
            self.assertIn(expected,self.chapter)
        self.assertIn("NO CANON PROMOTION",self.reader)

    def test_12_closing_continuity(self):
        self.assertIn("Pell leaves for an uncertain three-day hauling job",self.chapter)
        self.assertIn("four paid hours",self.chapter.lower())
        self.assertIn("independent commercial deliveries",self.chapter)
        self.assertIn("The roll was still a problem",self.chapter)

    def test_13_original_story_sequence_not_replaced(self):
        for anchor in ["I'm not holding you.", "What if she asks?", "The dye woman wants the edges of her cart boards marked", "From farther below the ridge came the faint unfinished tune"]:
            self.assertIn(anchor,self.original)
            self.assertIn(anchor,self.chapter)

    def test_14_protected_canon_bytes(self):
        for path,sha in PROTECTED.items():
            with self.subTest(file=path):
                self.assertEqual(blob(ROOT/path),sha)

    def test_15_evidence_archive_unchanged(self):
        archive = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertTrue(archive.exists())
        self.assertEqual(blob(archive), ARCHIVE_SHA)

    def test_16_unapproved_review_and_payment_gates(self):
        self.assertIn("No author-room or Umpire approval",self.chapter)
        self.assertIn("NO MERGE / NO PUBLICATION",self.reader)
        self.assertIn("four paid stoneworks hours", self.reader)
        self.assertIn("delivery to Esi unconfirmed",self.reader)

if __name__ == "__main__":
    unittest.main()
