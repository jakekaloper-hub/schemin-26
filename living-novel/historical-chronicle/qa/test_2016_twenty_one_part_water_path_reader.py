"""2016 twenty-one-part source exact reader regression (noncanon)."""
import unittest,hashlib,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
D=ROOT/"living-novel/historical-chronicle/seasons/2016/causal-novel"
OLD=D/"READING_COPY_2016_CAUSAL_CH01_23_TWENTY_PARTS_BLANKET_AT_THRESHOLD_V2_NONCANON.md";NEW=D/"READING_COPY_2016_CAUSAL_CH01_24_TWENTY_ONE_PARTS_LOWER_WATER_PATH_V2_NONCANON.md";CH=D/"THE_THINGS_SHE_CAME_BACK_FOR_THE_LOWER_WATER_PATH_CH24_V2_NONCANON.md";ORIG=D/"THE_THINGS_SHE_CAME_BACK_FOR_CHAPTER_24_NONCANON.md"
def blob(p):
    b=p.read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def rows(s):
    t=chr(96)
    patt=r"^\| (\d+) \| "+t+r"([^"+t+r"]+)"+t+r" \| "+t+r"([a-f0-9]{40})"+t+r" \| (\d+) \|$"
    return [(int(n),f,sha,int(w)) for n,f,sha,w in re.findall(patt,s,re.M)]
def body(s,f,sha):
    return s.split("<!-- BEGIN 2016_CAUSAL "+f+" | git_blob "+sha+" -->\n\n",1)[1].split("\n\n<!-- END 2016_CAUSAL "+f+" -->",1)[0]
class Test21Part(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old=OLD.read_text();cls.new=NEW.read_text();cls.ch=CH.read_text()
        cls.prev=rows(cls.old);cls.curr=rows(cls.new)
    def test_01_parent_reader_sha(self):
        self.assertEqual(blob(OLD),"f3faa9969b5969665d9295d28c6a3751c4f91585")
    def test_02_original_chapter_sha(self):
        self.assertEqual(blob(ORIG),"f767d79d9cd2ae6fdd58129ea96fbe0a73713461")
    def test_03_manifest_21(self):
        self.assertEqual([r[0] for r in self.curr],list(range(1,22)))
    def test_04_prev_rows(self):
        self.assertEqual(self.prev,self.curr[:20])
    def test_05_all_blob_and_word_checks(self):
        for n,f,sha,w in self.curr:
            with self.subTest(n=n):
                p=D/f
                self.assertEqual(blob(p),sha)
                self.assertEqual(len(p.read_text().split()),w)
    def test_06_all_source_exact(self):
        for n,f,sha,w in self.curr:
            with self.subTest(n=n):
                self.assertEqual(body(self.new,f,sha),(D/f).read_text().rstrip("\n"))
    def test_07_prior_components(self):
        for n,f,sha,w in self.prev:
            with self.subTest(n=n):self.assertEqual(body(self.old,f,sha),body(self.new,f,sha))
    def test_08_word_totals(self):
        self.assertEqual(sum(r[3] for r in self.curr),144561)
        self.assertIn("Source words including chapter metadata: 144561",self.new)
    def test_09_v2_scene(self):
        self.assertEqual(len(self.ch.split()),7930)
        self.assertTrue(self.ch.index("### IV. The terms of absence")<self.ch.index("### V. The lower water path")<self.ch.index("### VI. What remained in the room"))
    def test_10_preserved_work(self):
        self.assertIn("It was Sola.",self.ch)
        self.assertIn("I told you I was never staying.",self.ch)
        self.assertIn("I'd have to open it to know.",self.ch)
    def test_11_protected_canon(self):
        protected={"PROLOGUE_DRAFT_V1.md":"5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0","CHAPTER_01_THE_FIRST_ANSWER.md":"26a17f05eb0565e7648c29add03ee9580ec933c3","CHAPTER_02_WHAT_COMES_BACK.md":"30fcf23a3eb8872fa0fb4dff029fe30044141121","CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md":"49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc"}
        for f,sha in protected.items():
            with self.subTest(f=f):self.assertEqual(blob(ROOT/"living-novel/manuscript"/f),sha)
    def test_12_archive_and_release(self):
        self.assertEqual(blob(ROOT/"living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"),"6dbec1fe2537139f3a97c6a78250e2bae082a518")
        for k in ("NONCANON","NO MERGE","NO PUBLICATION","NO CANON PROMOTION","FOUNDER-ONLY"):
            self.assertIn(k,self.new)
