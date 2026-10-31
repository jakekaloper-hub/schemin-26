"""Exact-component 2016 partial Chronicle reader verification (NONCANON)."""
from pathlib import Path
import hashlib
import unittest

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "living-novel/historical-chronicle/seasons/2016"
READER = BASE / "READING_COPY_PROLOGUE_W01_W04_PARTIAL_NONCANON.md"
COMPONENTS = [
    ("PROLOGUE.md", "d372cd61c97d698ea34f2f41e7d762775fcdc379"),
    ("weeks/W01.md", "728693dd68e8ec314294d55fc1be263af6df7a60"),
    ("weeks/W02.md", "a2c179164dc529a34d92479b1c8a93f37acb10dd"),
    ("weeks/W03.md", "f515d2e46486f599906fd43cb98232585427ba0c"),
    ("weeks/W04.md", "c04700fe674489a5e0aac8f73ce4ddae9ba564eb"),
]


def blob_sha(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


class PartialReader2016Checks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = READER.read_text(encoding="utf-8")

    def test_five_components_in_order_and_once_each(self):
        positions = []
        for path, sha in COMPONENTS:
            marker = f"<!-- BEGIN 2016 {path} | git_blob {sha} -->"
            self.assertEqual(self.text.count(marker), 1, path)
            self.assertEqual(self.text.count(f"<!-- END 2016 {path} -->"), 1, path)
            positions.append(self.text.index(marker))
        self.assertEqual(positions, sorted(positions))

    def test_exact_source_component_blobs_unchanged(self):
        for path, sha in COMPONENTS:
            with self.subTest(path=path):
                self.assertEqual(blob_sha((BASE / path).read_bytes()), sha)

    def test_assembled_bodies_equal_source_text(self):
        for path, sha in COMPONENTS:
            with self.subTest(path=path):
                start = f"<!-- BEGIN 2016 {path} | git_blob {sha} -->\n\n"
                end = f"\n\n<!-- END 2016 {path} -->"
                self.assertIn(start, self.text)
                body = self.text.split(start, 1)[1].split(end, 1)[0]
                self.assertEqual(body, (BASE / path).read_text(encoding="utf-8").rstrip())

    def test_partial_not_final_season_or_canon(self):
        for marker in ("PARTIAL READING COPY", "NONCANON", "intentionally incomplete",
                       "Weeks 5–13", "No Founder, Author Council or Umpire approval"):
            self.assertIn(marker.lower(), self.text.lower())

    def test_reader_materially_substantial_and_2016_only(self):
        self.assertGreaterEqual(len(self.text.split()), 14000)
        self.assertEqual(self.text.count("<!-- BEGIN 2016 "), 5)

    def test_original_2026_hard_manuscript_not_included(self):
        for name in ("CHAPTER_01_THE_FIRST_ANSWER", "CHAPTER_02_WHAT_COMES_BACK",
                     "CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM"):
            self.assertNotIn(name, self.text)


if __name__ == "__main__":
    unittest.main()
