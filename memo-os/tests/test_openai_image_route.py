import importlib.util
import io
import pathlib
import sys
import tempfile
import unittest
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location("route", ROOT / "openai_image_route.py")
route = importlib.util.module_from_spec(spec)
spec.loader.exec_module(route)

class OpenAIImageRouteTest(unittest.TestCase):
    def test_explicit_9_16_source_request(self):
        req = route.request_body("test")
        self.assertEqual(req["size"], "1152x2048")
        self.assertEqual(req["output_format"], "png")

    def test_downscale_to_exact_master(self):
        buf = io.BytesIO()
        Image.new("RGB", (1152, 2048), "blue").save(buf, format="PNG")
        with tempfile.TemporaryDirectory() as d:
            result=route.create_master(buf.getvalue(), pathlib.Path(d)/"page.png")
            self.assertEqual(result["status"], "STRUCTURAL_PASS_VISUAL_QA_REQUIRED")

    def test_wrong_source_rejected(self):
        buf = io.BytesIO()
        Image.new("RGB", (1024, 1536), "blue").save(buf, format="PNG")
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError, "OPENAI_SOURCE_DIMENSIONS_UNEXPECTED"):
                route.create_master(buf.getvalue(), pathlib.Path(d)/"page.png")

    def test_no_unapproved_api_cost(self):
        with self.assertRaises(PermissionError):
            route.generate("test", "does-not-exist.png")

if __name__ == "__main__":
    unittest.main()
