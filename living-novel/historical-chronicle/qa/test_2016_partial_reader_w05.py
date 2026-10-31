"""Six-part source-exact 2016 NONCANON partial reader verification."""
from pathlib import Path
import hashlib
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016"
READER = BASE / "READING_COPY_PROLOGUE_W01_W05_PARTIAL_NONCANON.md"
PARTS = [
    ("PROLOGUE.md", "d372cd61c97d698ea34f2f41e7d762775fcdc379"),
    ("weeks/W01.md", "728693dd68e8ec314294d55fc1be263af6df7a60"),
    ("weeks/W02.md", "a2c179164dc529a34d92479b1c8a93f37acb10dd"),
    ("weeks/W03.md", "f515d2e46486f599906fd43cb98232585427ba0c"),
    ("weeks/W04.md", "c04700fe674489a5e0aac8f73ce4ddae9ba564eb"),
    ("weeks/W05.md", "bab0fe58cd46e77950d59fe0359a92efb78bd1ae"),
]


def blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


class ReaderThroughWeekFive2016(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = READER.read_text(encoding="utf-8")

    def test_01_six_ordered_nonduplicated_parts(self):
        markers = [f"<!-- BEGIN 2016 {path} | git_blob {sha} -->" for path, sha in PARTS]
        self.assertEqual([self.text.count(x) for x in markers], [1] * 6)
        self.assertEqual([self.text.index(x) for x in markers],
                         sorted(self.text.index(x) for x in markers))

    def test_02_six_end_markers(self):
        for path, _ in PARTS:
            self.assertEqual(self.text.count(f"<!-- END 2016 {path} -->"), 1)

    def test_03_exact_component_git_blob_shas(self):
        for path, sha in PARTS:
            with self.subTest(path=path):
                self.assertEqual(blob((BASE / path).read_bytes()), sha)

    def test_04_verbatim_body_assembly(self):
        for path, sha in PARTS:
            with self.subTest(path=path):
                start = f"<!-- BEGIN 2016 {path} | git_blob {sha} -->\n\n"
                stop = f"\n\n<!-- END 2016 {path} -->"
                self.assertIn(start, self.text)
                fragment = self.text.split(start, 1)[1].split(stop, 1)[0]
                self.assertEqual(fragment, (BASE / path).read_text(encoding="utf-8").rstrip())

    def test_05_substantial_reading_copy_not_metadata_only(self):
        self.assertGreaterEqual(len(self.text.split()), 20000)
        self.assertEqual(self.text.count("<!-- BEGIN 2016 "), 6)

    def test_06_no_full_season_or_canon_promotion(self):
        for token in ("PARTIAL READING COPY", "NONCANON", "Weeks 6–13",
                      "No Founder, independent Author Council or Umpire approval"):
            self.assertIn(token.lower(), self.text.lower())

    def test_07_protected_2026_manuscript_not_assembled(self):
        for name in ("CHAPTER_01_THE_FIRST_ANSWER", "CHAPTER_02_WHAT_COMES_BACK",
                     "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM"):
            self.assertNotIn(name, self.text)


if __name__ == "__main__":
    unittest.main()
