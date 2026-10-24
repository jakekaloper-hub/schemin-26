"""Synthetic review fixtures, never real editorial/reviewer approval evidence."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import fitz
from PIL import Image, ImageDraw, ImageFont
TOOLS = Path(__file__).resolve().parents[1] / 'tools'
sys.path.insert(0, str(TOOLS))
from inspect_pdf_copy import inspect_pdf_copy


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


@unittest.skipUnless(shutil.which('tesseract'), 'actual PDF OCR requires Tesseract')
class PDFCopyPipeline(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.manifest_path = self.root / 'manifest.json'
        pages = []
        doc = fitz.open()
        for n in (1, 2):
            asset = self.root / f'p{n}.png'
            text = f'CLEAR COPY {n}'
            image = Image.new('RGB', (1024, 1536), 'white')
            ImageDraw.Draw(image).text((50, 50), text, fill='black', font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 48))
            image.save(asset)
            spec = self.root / f'spec{n}.json'
            spec.write_text(json.dumps({'synthetic_fixture_copy': text}))
            receipt = self.root / f'receipt{n}.json'
            receipt.write_text(json.dumps({'status': 'CANDIDATE_NOT_APPROVED',
                'visual_text_independently_verified': False, 'output_sha256': digest(asset),
                'spec_sha256': digest(spec), 'dimensions': [1024,1536],
                'source_text_regions': [{'box':[40,40,900,100], 'rendered_lines':[text]}]}))
            sheet = doc.new_page(width=512, height=768)
            sheet.insert_image(sheet.rect, filename=str(asset))
            pages.append({'slot': n, 'printed_page': n, 'status': 'ACCEPTED',
                'asset_path': asset.name, 'asset_sha256': digest(asset),
                'editorial_spec_path': spec.name, 'editorial_receipt_path': receipt.name,
                'role':'EDITORIAL', 'mobile_qa':'PASS', 'technical_acceptance':'PASS',
                'publication_fidelity':'PASS', 'narrative_job':'synthetic test only'})
        self.pdf = self.root / 'issue.pdf'
        doc.save(self.pdf); doc.close()
        self.manifest = {'artifact_stage':'ISSUE_PACKAGE', 'publication_state':'REVIEW',
                         'expected_pages':2, 'pages':pages, 'pdf_path':'issue.pdf',
                         'published_artifact_sha256':digest(self.pdf)}

    def inspect(self):
        return inspect_pdf_copy(self.manifest, self.manifest_path)

    def cli(self):
        self.manifest_path.write_text(json.dumps(self.manifest))
        result = subprocess.run([sys.executable, str(TOOLS.parent/'tests'/'validate_artifacts.py'), str(self.manifest_path)], capture_output=True, text=True)
        return result, json.loads(result.stdout)

    def test_full_pipeline_real_pdf_positive_without_claiming_approval(self):
        result, report = self.cli()
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        observed = report['pdf_copy_diagnostics']
        self.assertTrue(observed['all_pages_observed'])
        self.assertFalse(observed['independent_acceptance'])
        self.assertEqual(observed['pages'][0]['observation']['regions'][0]['observed_text'], 'CLEAR COPY 1')

    def test_changed_copy_receipt_fails_pipeline(self):
        path = self.root/'receipt1.json'
        receipt = json.loads(path.read_text())
        receipt['source_text_regions'][0]['rendered_lines'] = ['DIFFERENT COPY']
        path.write_text(json.dumps(receipt))
        result, report = self.cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('observed editorial text differs', str(report['errors']))

    def test_overlay_fails_even_with_updated_pdf_hash(self):
        with fitz.open(self.pdf) as doc:
            doc[0].draw_rect(fitz.Rect(0,0,300,80), fill=(1,1,1))
            doc.saveIncr()
        self.manifest['published_artifact_sha256'] = digest(self.pdf)
        self.assertIn('rendered pixels differ', str(self.inspect()['errors']))

    def test_missing_receipt_is_explicit_coverage_gap(self):
        del self.manifest['pages'][0]['editorial_receipt_path']
        report = self.inspect()
        self.assertFalse(report['all_pages_observed'])
        self.assertEqual(report['pages'][0]['region_comparison'], 'NOT_RUN_NO_EDITORIAL_RECEIPT')

    def test_released_pipeline_still_requires_real_evidence(self):
        self.manifest['publication_state']='RELEASED'
        result, report = self.cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('provider receipt required', str(report['errors']))
        self.assertIn('Umpire', str(report['errors']))

    def test_wrong_spec_blocks_before_ocr(self):
        (self.root/'spec1.json').write_text('changed')
        with patch('inspect_pdf_copy.observe') as observe:
            report=self.inspect()
        self.assertIn('source spec hash mismatch',str(report['errors']))
        self.assertEqual(observe.call_count,1) # only unaffected second page

    def test_wrong_pdf_hash_blocks_observation(self):
        self.manifest['published_artifact_sha256']='0'*64
        self.assertIn('PDF hash mismatch', str(self.inspect()['errors']))

    def test_receipt_shape_failure_is_diagnostic(self):
        (self.root/'receipt1.json').write_text('[]')
        report=self.inspect()
        self.assertIn('receipt/master hash mismatch',str(report['errors']))
        self.assertEqual(report['pages'][0]['region_comparison'],'FAILED')

    def test_receipt_path_cannot_escape_release_directory(self):
        self.manifest['pages'][0]['editorial_receipt_path']='../outside.json'
        self.assertIn('path escapes release directory',str(self.inspect()['errors']))

    def test_failed_ocr_returns_diagnostic_not_success(self):
        with patch('inspect_pdf_copy.observe',side_effect=subprocess.CalledProcessError(1,'tesseract')):
            report=self.inspect()
        self.assertEqual(len(report['errors']),2)
        self.assertFalse(report['all_pages_observed'])
