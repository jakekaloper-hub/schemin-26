import importlib.util
import unittest
import tempfile
import json
from unittest.mock import patch
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
class ReceiptFreshnessTests(unittest.TestCase):
    def download_metadata(self, command, **kwargs):
        template = Path(command[command.index("-o") + 1])
        (template.parent / "vFMnz75y5y4.info.json").write_text(json.dumps({"id": self.metadata_id, "title": "fixture"}))

    def test_existing_caption_and_media_files_are_not_new_evidence(self):
        self.metadata_id = "vFMnz75y5y4"
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            (output / "vFMnz75y5y4.en.vtt").write_text("stale transcript")
            (output / "vFMnz75y5y4.mp4").write_bytes(b"stale media")
            with patch.object(module.subprocess, "run", side_effect=self.download_metadata):
                receipt = module.run("https://youtu.be/vFMnz75y5y4", output, allow_media=True)
            self.assertEqual(receipt["status"], "METADATA_ONLY")
            self.assertEqual(receipt["transcript_files"], [])
            self.assertEqual(receipt["media_files"], [])

    def test_wrong_video_metadata_rejected(self):
        self.metadata_id = "different-id"
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(module.subprocess, "run", side_effect=self.download_metadata):
                with self.assertRaisesRegex(RuntimeError, "identity mismatch"):
                    module.run("https://youtu.be/vFMnz75y5y4", directory)
            self.assertFalse((Path(directory) / "receipt.json").exists())

if __name__ == "__main__":
    unittest.main()
