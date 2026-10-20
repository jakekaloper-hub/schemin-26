import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("video_intelligence", Path(__file__).resolve().parents[1] / "bullpen-runtime" / "video_intelligence.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class VideoIdTests(unittest.TestCase):
    def test_short_link(self):
        self.assertEqual(module.video_id("https://youtu.be/vFMnz75y5y4?is=abc"), "vFMnz75y5y4")
    def test_watch_link(self):
        self.assertEqual(module.video_id("https://www.youtube.com/watch?v=vFMnz75y5y4"), "vFMnz75y5y4")
    def test_reject_foreign_domain(self):
        with self.assertRaises(ValueError):
            module.video_id("https://youtube.com.evil.example/watch?v=vFMnz75y5y4")
    def test_reject_bad_id(self):
        with self.assertRaises(ValueError):
            module.video_id("https://youtu.be/abc")
if __name__ == "__main__":
    unittest.main()
