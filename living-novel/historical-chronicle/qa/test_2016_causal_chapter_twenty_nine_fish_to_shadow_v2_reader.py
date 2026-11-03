"""Source-pinned 2016 Chapter XXIX fish-to-shadow V2 and 26-part reader (NONCANON).
Deterministic structure/provenance checks, not literary, Umpire or Founder acceptance.
"""
import hashlib
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel"
CH = "THE_PLAY_WITH_NO_END_THE_FISH_DOES_NOT_GET_ANOTHER_MOUTH_CH29_V2_NONCANON.md"
OLD = "THE_PLAY_WITH_NO_END_CHAPTER_29_NONCANON.md"
READER = "READING_COPY_2016_CAUSAL_CH01_29_TWENTY_SIX_PARTS_FISH_TO_SHADOW_V2_NONCANON.md"
PRIOR = "READING_COPY_2016_CAUSAL_CH01_28_TWENTY_FIVE_PARTS_BLUE_WITH_TWO_SHADOWS_NONCANON.md"
CH_SHA = "d686d653a29d69a7a1c785f68ff848014cdcebef"
OLD_SHA = "815329d6d69dd875929f26e0a4c7974cd77415dd"
PRIOR_SHA = "fa4002fb2ad9a4e8de310711ea93c02d6e7ddc7c"
ARCHIVE_SHA = "6dbec1fe2537139f3a97c6a78250e2bae082a518"
PROTECTED = {
 "living-novel/manuscript/PROLOGUE_DRAFT_V1.md": "5ef240b31a67cf1a3b6c6d8ee723bf39fc7dfaf0",
 "living-novel/manuscript/CHAPTER_01_THE_FIRST_ANSWER.md": "26a17f05eb0565e7648c29add03ee9580ec933c3",
 "living-novel/manuscript/CHAPTER_02_WHAT_COMES_BACK.md": "30fcf23a3eb8872fa0fb4dff029fe30044141121",
 "living-novel/manuscript/CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md": "49e1fd1c20c61e4cf77a22489b7ec3eb3f6656cc",
}

def git_blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

def manifest(text):
    return [(int(n), filename, sha, int(words))
            for n, filename, sha, words in re.findall(
                r"^\| (\d+) \| `([^`]+)` \| `([a-f0-9]{40})` \| (\d+) \|$", text, re.M)]

def body(text, filename, sha):
    start = f"<!-- BEGIN 2016_CAUSAL {filename} | git_blob {sha} -->"
    end = f"<!-- END 2016_CAUSAL {filename} -->"
    assert text.count(start) == 1 and text.count(end) == 1, filename
    return text.split(start + "\n\n", 1)[1].split("\n\n" + end, 1)[0]

class ChapterTwentyNineFishV2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ch = (BASE / CH).read_text()
        cls.old_ch = (BASE / OLD).read_text()
        cls.reader = (BASE / READER).read_text()
        cls.previous = (BASE / PRIOR).read_text()
        cls.rows = manifest(cls.reader)
        cls.prev_rows = manifest(cls.previous)
        cls.scene = "### I. The fish does not get another mouth" + cls.ch.split(
            "### I. The fish does not get another mouth", 1)[1].split(
            "### II. The place where the light stood", 1)[0]
        cls.prose = cls.ch.split("### I.", 1)[1].split(
            "### Editorial handoff", 1)[0]

    def test_01_new_chapter_blob(self):
        self.assertEqual(git_blob(BASE / CH), CH_SHA)

    def test_02_old_chapter_blob_preserved(self):
        self.assertEqual(git_blob(BASE / OLD), OLD_SHA)

    def test_03_previous_reader_blob_preserved(self):
        self.assertEqual(git_blob(BASE / PRIOR), PRIOR_SHA)

    def test_04_six_movements_in_order(self):
        self.assertEqual(re.findall(r"^### ([IVX]+)\. ", self.ch, re.M),
                         ["I", "II", "III", "IV", "V", "VI"])

    def test_05_new_bridge_substantial(self):
        self.assertEqual(len(self.scene.split()), 1902)
        self.assertIn("It ate a crown", self.scene)
        self.assertIn("That corner belongs to the woman", self.scene)
        self.assertIn("The fish has been claimed by its maker", self.scene)

    def test_06_original_drama_still_present(self):
        for s in (
            "The child who had been learning the same high note",
            "The play had reached its second attempt at an ending when Vessa entered",
            "The children had made the door from a piece of wood",
            "After the lamps were raised, the linen became an ordinary sheet",
            "The next part belongs to another night",
        ):
            self.assertIn(s, self.ch)
            self.assertIn(s, self.old_ch)

    def test_07_reader_manifest_sequence(self):
        self.assertEqual([n for n, _, _, _ in self.rows], list(range(1, 27)))
        self.assertEqual(self.rows[-1], (26, CH, CH_SHA, 7806))

    def test_08_reader_marker_balance(self):
        self.assertEqual(self.reader.count("<!-- BEGIN 2016_CAUSAL "), 26)
        self.assertEqual(self.reader.count("<!-- END 2016_CAUSAL "), 26)

    def test_09_all_26_component_hashes_and_bodies(self):
        for n, name, sha, words in self.rows:
            with self.subTest(part=n, name=name):
                source = (BASE / name).read_text()
                self.assertEqual(git_blob(BASE / name), sha)
                self.assertEqual(len(source.split()), words)
                self.assertEqual(body(self.reader, name, sha), source.rstrip("\n"))

    def test_10_all_prior_25_bodies_unchanged(self):
        self.assertEqual(self.rows[:25], self.prev_rows)
        for n, name, sha, _ in self.rows[:25]:
            with self.subTest(part=n):
                self.assertEqual(body(self.reader, name, sha),
                                 body(self.previous, name, sha))

    def test_11_total_manifest_words(self):
        self.assertEqual(sum(w for _, _, _, w in self.rows), 181656)
        self.assertIn("Source component words including metadata: 181656",
                      self.reader)

    def test_12_single_proposed_owner_pov(self):
        self.assertIn("Sole limited interior viewpoint", self.ch)
        self.assertIn("historical 2016 owner slot remains UNAUTHENTICATED", self.ch)
        for prohibited in ("Edrin", "Edin"):
            self.assertNotIn(prohibited, self.prose)

    def test_13_two_theaters_are_distinct(self):
        for anchor in ("The fish has been claimed by its maker",
                       "No lamp touching the cloth",
                       "She had come to collect what was hers",
                       "The children's spoon stood waiting"):
            self.assertIn(anchor, self.scene)
        self.assertIn("Iri's fish story in Chapter XXVII", self.reader)

    def test_14_unresolved_work_and_delivery(self):
        for anchor in ("kiln passage remains closed",
                       "half-paid cart-mark commission is incomplete",
                       "Esi's receipt remains unconfirmed",
                       "four stoneworks hours"):
            self.assertIn(anchor, self.ch)
        self.assertIn("I won't open it for your play", self.ch)
        self.assertIn("Pell's hauling work is uncertain", self.reader)

    def test_15_archive_remains_intact(self):
        archive = ROOT / "living-novel/production/full-rewrite-2026/evidence/G01_2016_FULL_WEEKLY_MATCHUPS.json"
        self.assertEqual(git_blob(archive), ARCHIVE_SHA)

    def test_16_protected_2026_hard_canon(self):
        for path, sha in PROTECTED.items():
            with self.subTest(file=path):
                self.assertEqual(git_blob(ROOT / path), sha)

    def test_17_not_published_or_approved(self):
        self.assertIn("NO MERGE / NO PUBLICATION / NO CANON PROMOTION", self.reader)
        self.assertIn("independent review HOLD", self.ch)
        self.assertIn("FOUNDER-ONLY CANON & PUBLICATION APPROVAL", self.reader)

if __name__ == "__main__":
    unittest.main()
