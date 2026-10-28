"""Regression checks for forward-only native memo PNG dimensions."""
import importlib.util
import struct
import tempfile
import unittest
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("native_png_contract", HERE / "native_png_contract.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def sample_png(width, height):
    def chunk(kind, payload):
        return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xffffffff)
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    scanlines = (b"\x00" + b"\x11\x22\x33" * width) * height
    return mod.SIGNATURE + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(scanlines)) + chunk(b"IEND", b"")

class NativePNGContractTest(unittest.TestCase):
    def check(self, data):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "page.png"
            path.write_bytes(data)
            return mod.validate_png(path)

    def test_native_dimensions_pass(self):
        self.assertEqual(self.check(sample_png(1080, 1920))["status"], "STRUCTURAL_PASS_VISUAL_QA_REQUIRED")

    def test_legacy_dimensions_block(self):
        with self.assertRaisesRegex(mod.NativePNGError, "WRONG_NATIVE_DIMENSIONS"):
            self.check(sample_png(1024, 1536))

    def test_wrong_aspect_ratio_block(self):
        with self.assertRaises(mod.NativePNGError):
            self.check(sample_png(1080, 1350))

    def test_corrupt_bytes_block(self):
        with self.assertRaises(mod.NativePNGError):
            self.check(b"not a PNG")

    def test_trailing_bytes_block(self):
        with self.assertRaises(mod.NativePNGError):
            self.check(sample_png(1080, 1920) + b"BAD")

if __name__ == "__main__":
    unittest.main()
