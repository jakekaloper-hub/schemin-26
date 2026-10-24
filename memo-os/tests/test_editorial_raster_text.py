import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image, ImageDraw, ImageFont

PATH = Path(__file__).resolve().parents[1] / 'tools' / 'compare_editorial_raster_text.py'
spec = importlib.util.spec_from_file_location('raster_text', PATH)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class RasterTextDiagnostics(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.png = self.root / 'page.png'
        image = Image.new('RGB', (1024, 1536), 'white')
        ImageDraw.Draw(image).text((50, 50), 'CLEAR COPY 123', fill='black',
                                  font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 48))
        image.save(self.png)
        self.receipt = self.root / 'render.json'
        self.data = {'output_sha256': hashlib.sha256(self.png.read_bytes()).hexdigest(),
                     'dimensions': [1024, 1536], 'source_text_regions': [
                         {'box': [40, 40, 900, 100], 'rendered_lines': ['CLEAR COPY 123']}]}
        self.write()

    def write(self):
        self.receipt.write_text(json.dumps(self.data))

    @unittest.skipUnless(shutil.which('tesseract'), 'tesseract required for actual pixel extraction')
    def test_real_pixels_positive_and_changed_expected_copy(self):
        result = m.observe(self.png, self.receipt)
        self.assertTrue(result['all_regions_exact_match'], result)
        self.assertFalse(result['independent_visual_acceptance'])
        self.data['source_text_regions'][0]['rendered_lines'] = ['CLEAR COPY 999']
        self.write()
        result = m.observe(self.png, self.receipt)
        self.assertFalse(result['all_regions_exact_match'])
        self.assertEqual(result['regions'][0]['observed_text'], 'CLEAR COPY 123')

    def test_wrong_artifact_blocks_before_ocr(self):
        self.png.write_bytes(b'changed')
        with patch.object(m.subprocess, 'run') as run:
            with self.assertRaisesRegex(ValueError, 'bound'):
                m.observe(self.png, self.receipt)
            run.assert_not_called()

    def test_region_cannot_escape_raster(self):
        self.data['source_text_regions'][0]['box'] = [-1, 0, 10, 10]
        self.write()
        with patch.object(m.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, stdout='fixture\n')):
            with self.assertRaisesRegex(ValueError, 'outside'):
                m.observe(self.png, self.receipt)

    def test_no_whitespace_or_punctuation_normalization(self):
        with patch.object(m.subprocess, 'run', side_effect=[
            subprocess.CompletedProcess([], 0, stdout='fixture\n'),
            subprocess.CompletedProcess([], 0, stdout=b'CLEAR  COPY 123!\n')]):
            result = m.observe(self.png, self.receipt)
        self.assertFalse(result['all_regions_exact_match'])

    def test_ocr_failure_propagates_without_success_receipt(self):
        with patch.object(m.subprocess, 'run', side_effect=subprocess.CalledProcessError(1, 'tesseract')):
            with self.assertRaises(subprocess.CalledProcessError):
                m.observe(self.png, self.receipt)
