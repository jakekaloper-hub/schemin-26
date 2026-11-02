"""Source-identity and firewall checks for the noncanonical 2025 13-part development reader.

Passing assertions protect bytes and known facts; they DO NOT constitute literary
quality, historic owner-account verification, Atlas signoff or independent Umpire review.
"""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2025/causal-novel"
CHAPTER = BASE / "THE_WATER_UNDER_THE_BOARDS_ZACH_PHILLIP_2025_DEVELOPMENTAL_NONCANON.md"
READER = BASE / "READING_COPY_2025_TWELVE_VOICES_THIRTEEN_PARTS_DUAL_COMPRESSION_NONCANON.md"
OLD = BASE / "READING_COPY_2025_TWELVE_VOICES_FOURTEEN_PARTS_COMPRESSED_OPENING_NONCANON.md"
ZACH_ORIGINAL = BASE / "THE_COURSE_BENEATH_THE_COURSE_ZACH_2025_NONCANON.md"
PHILLIP_ORIGINAL = BASE / "THE_MASKS_THAT_REMAINED_PHILLIP_2025_NONCANON.md"
READER_2016 = ROOT / "living-novel/historical-chronicle/seasons/2016/causal-novel/READING_COPY_CAUSAL_CHAPTERS_01_72_NONCANON.md"
CHAPTER_BLOB = "dfec5b800b468081805058f33e65f35da49e57bb"
READER_BLOB = "fe6e4056c951323aba19b302c67897bda96d59b9"
OLD_BLOB = "7d9ca508d925493723478d02e0afc97d2276bdd9"
ZACH_BLOB = "112b3890173cbf11879b139bff966cdff83884d4"
PHILLIP_BLOB = "f96832d3bd23840d2fb1853d17940ac54774531d"
OLD_2016_BLOB = "8f1dda21ac4962143ba3291cef4d60769197d62f"
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
MANIFEST_ROW = re.compile(
    r"^\| (\d+) \| ([^|]+) \| " + chr(96) +
    r"([^" + chr(96) + r"]+)" + chr(96) +
    r" \| " + chr(96) + r"([0-9a-f]{40})" + chr(96) +
    r" \| (\d+) \|$", re.M
)

def blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

class DualDevelopmentalCompression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = CHAPTER.read_text(encoding="utf-8")
        cls.new = READER.read_text(encoding="utf-8")
        cls.old = OLD.read_text(encoding="utf-8")
        cls.newwrap = list(WRAP.finditer(cls.new))
        cls.oldwrap = list(WRAP.finditer(cls.old))
        cls.manifest = cls.new.split("## Source-exact composition manifest\n", 1)[1].split("\n---\n", 1)[0]
        cls.rows = MANIFEST_ROW.findall(cls.manifest)
        cls.story = cls.chapter.split("### Production/source boundary", 1)[0]

    def test_01_prior_fourteen_part_reader_unchanged(self):
        self.assertEqual(blob(OLD), OLD_BLOB)

    def test_02_new_literary_chapter_sha(self):
        self.assertEqual(blob(CHAPTER), CHAPTER_BLOB)

    def test_03_new_reader_sha(self):
        self.assertEqual(blob(READER), READER_BLOB)

    def test_04_original_zach_and_phillip_chapters_unchanged(self):
        self.assertEqual(blob(ZACH_ORIGINAL), ZACH_BLOB)
        self.assertEqual(blob(PHILLIP_ORIGINAL), PHILLIP_BLOB)

    def test_05_old_and_new_wrapper_counts(self):
        self.assertEqual(len(self.oldwrap), 14)
        self.assertEqual(len(self.newwrap), 13)

    def test_06_twelve_prior_wrapper_bodies_byte_exact(self):
        before = [self.oldwrap[0], *self.oldwrap[3:]]
        after = [self.newwrap[0], *self.newwrap[2:]]
        self.assertEqual(len(before), len(after))
        for b, a in zip(before, after):
            with self.subTest(name=b.group(1)):
                self.assertEqual(b.group(0), a.group(0))

    def test_07_all_wrapped_sources_are_exact(self):
        for w in self.newwrap:
            p = BASE / w.group(1)
            with self.subTest(name=p.name):
                self.assertEqual(w.group(1), w.group(4))
                self.assertTrue(p.is_file())
                self.assertEqual(blob(p), w.group(2))
                self.assertEqual(w.group(3), p.read_text(encoding="utf-8").rstrip("\n"))

    def test_08_part_labels_sequential(self):
        self.assertEqual(re.findall(r"^## Part (\d+) —", self.new, re.M),
                         [str(i) for i in range(1, 14)])

    def test_09_manifest_exactly_matches_wrapper_order(self):
        self.assertEqual(len(self.rows), 13)
        for n, row in enumerate(self.rows):
            with self.subTest(n=n):
                self.assertEqual(int(row[0]), n + 1)
                self.assertEqual(row[2].split("/")[-1], self.newwrap[n].group(1))
                self.assertEqual(row[3], self.newwrap[n].group(2))

    def test_10_manifest_word_counts_are_not_estimates(self):
        for row in self.rows:
            self.assertEqual(int(row[4]), len((BASE / row[2].split("/")[-1]).read_text(encoding="utf-8").split()))

    def test_11_source_words_sum_and_compaction(self):
        self.assertEqual(len(self.chapter.split()), 5162)
        self.assertEqual(sum(int(row[4]) for row in self.rows), 70117)
        self.assertEqual(75042 - 70117, 4925)

    def test_12_exactly_twelve_unique_registered_principals(self):
        owners = {owner for row in self.rows for owner in re.findall(r"CHAR-[A-Z-]+", row[1])}
        self.assertEqual(len(owners), 12)
        self.assertEqual(set(re.findall(r"CHAR-[A-Z-]+", self.rows[1][1])),
                         {"CHAR-ZACH-WILSON", "CHAR-PHILLIP-PITTS"})

    def test_13_two_legal_alternating_limited_povs(self):
        mov = re.findall(r"^### ([IVX]+)\. ([^\n]+) — (Zach|Phillip)$", self.story, re.M)
        self.assertEqual([m[0] for m in mov], ["I", "II", "III", "IV", "V", "VI"])
        self.assertEqual([m[2] for m in mov], ["Zach", "Phillip", "Zach", "Phillip", "Zach", "Phillip"])

    def test_14_no_retired_narrator_in_story(self):
        self.assertIsNone(re.search(r"\b(?:Edrin|Edin|Oren)\b", self.story))

    def test_15_source_facts_present_and_bounded(self):
        for val in ("152.20", "151.80", "The Immortal", "Three Dreaded Snake"):
            self.assertIn(val, self.chapter)
        self.assertIn("not authenticated 2025 ESPN manager", self.chapter)
        self.assertIn("historical real manager attribution remains UNKNOWN", self.chapter)

    def test_16_character_morphology_and_prosthetic(self):
        for val in ("white duck", "bucket hat", "driver", "three heads", "one Phillip", "one set of hands"):
            self.assertIn(val.lower(), self.story.lower())

    def test_17_real_material_consequence_not_instant_restoration(self):
        for val in ("The green collapsed", "no stage", "deposit", "damaged", "cottages", "blank"):
            self.assertIn(val.lower(), self.story.lower())

    def test_18_no_authored_atlas_geography_promotion(self):
        self.assertIn("no approved historical Atlas location", self.chapter)
        self.assertIn("provisional", self.new.lower())
        self.assertNotIn("ATLAS_APPROVED", self.chapter)

    def test_19_story_has_substantial_scene_prose(self):
        self.assertGreater(len(self.story.split()), 4600)
        self.assertIn("### VI. An Unpaid Audience — Phillip", self.story)

    def test_20_no_new_factual_transactions_or_2026_results(self):
        self.assertIn("not an ESPN event", self.chapter.lower())
        self.assertIn("all 2026 outcomes", self.chapter)

    def test_21_protected_main_prologue_and_three_chapters(self):
        for name, sha in PROTECTED.items():
            with self.subTest(name=name):
                self.assertEqual(blob(ROOT / name), sha)

    def test_22_2016_full_reader_untouched(self):
        self.assertEqual(blob(READER_2016), OLD_2016_BLOB)

    def test_23_no_auto_promotion_or_review_claim(self):
        self.assertIn("NONCANON / REVIEW HOLD", self.chapter)
        self.assertIn("No independent author, Umpire or Founder approval is inferred", self.new)

    def test_24_terminal_marker_and_end_tag(self):
        self.assertTrue(self.new.rstrip().endswith(
            "<!-- END_2025_TWELVE_VOICES_THIRTEEN_PARTS_DUAL_COMPRESSION_NONCANON -->"))
        self.assertEqual(self.newwrap[1].group(1), CHAPTER.name)

if __name__ == "__main__":
    unittest.main()
