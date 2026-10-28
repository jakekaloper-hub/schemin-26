import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

spec = importlib.util.spec_from_file_location('memo_text_candidates', Path(__file__).resolve().parents[1] / 'build_memo_text_candidates.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CandidateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'archive/edition.pdf'
        self.source.parent.mkdir()
        self.source.write_bytes(b'%PDF-fixture')
        self.manifest = {'files': [{'week': 6, 'archive_path': 'archive/edition.pdf',
                                   'sha256': module.digest(self.source), 'size_bytes': self.source.stat().st_size,
                                   'pages': 2}]}
        self.calls = []

    def runner(self, command, **kwargs):
        self.calls.append(command)
        if command[0] == 'pdfinfo':
            return SimpleNamespace(stdout='Pages: 2\n')
        if command[0] == 'pdftoppm':
            Path(command[-1]).with_suffix('.png').write_bytes(b'page pixels ' + command[2].encode())
        if command[0] == 'tesseract':
            Path(command[2]).with_suffix('.txt').write_text('<script>alert(1)</script>\nUncertain 138.O6')
        return SimpleNamespace(stdout='')

    def build(self, pages=None, output=None):
        return module.build_candidates(self.root, self.manifest, 'a' * 40, 6,
                                       pages or [2, 1], output or self.root / 'candidate', self.runner)

    def test_physical_pages_hashes_and_unreviewed_state(self):
        packet = self.build()
        self.assertFalse(packet['publication_eligible'])
        self.assertEqual([p['physical_page'] for p in packet['pages']], [1, 2])
        for page in packet['pages']:
            self.assertFalse(page['reviewed'])
            self.assertEqual(page['candidate_text_sha256'], module.digest(self.root / 'candidate' / page['candidate_text']))
        document = (self.root / 'candidate/review.html').read_text()
        self.assertNotIn('<script>alert', document)
        self.assertIn('&lt;script&gt;', document)
        self.assertIn('Unreviewed OCR', document)

    def test_wrong_source_bytes_never_reach_ocr(self):
        self.source.write_bytes(b'%PDF-tampered')
        with self.assertRaisesRegex(ValueError, 'hash or size'):
            self.build()
        self.assertFalse(self.calls)

    def test_invalid_page_selection_rejected(self):
        for pages in ([0], [3], [1, 1], [True]):
            with self.subTest(pages=pages), self.assertRaisesRegex(ValueError, 'physical page'):
                self.build(pages)
        self.assertTrue(all(call[0] == 'pdfinfo' for call in self.calls))

    def test_no_public_output_or_existing_packet_overwrite(self):
        for name in ('src', 'dist'):
            with self.assertRaisesRegex(ValueError, 'outside public'):
                self.build(output=self.root / 'productions/audience-site' / name / 'ocr')
        self.build()
        with self.assertRaisesRegex(ValueError, 'empty'):
            self.build()

    def test_pdf_count_mismatch_rejected(self):
        self.manifest['files'][0]['pages'] = 3
        with self.assertRaisesRegex(ValueError, 'page count'):
            self.build()

    def test_source_change_during_capture_rejects_packet(self):
        def change(command, **kwargs):
            result = self.runner(command, **kwargs)
            if command[0] == 'tesseract':
                self.source.write_bytes(b'%PDF-changed while processing')
            return result
        with self.assertRaisesRegex(ValueError, 'changed during OCR'):
            module.build_candidates(self.root, self.manifest, 'a' * 40, 6, [1], self.root / 'changed', change)
        self.assertFalse((self.root / 'changed/candidate.json').exists())

    def test_failed_ocr_does_not_create_acceptance_receipt(self):
        def fail(command, **kwargs):
            if command[0] == 'tesseract':
                raise RuntimeError('OCR unavailable')
            return self.runner(command, **kwargs)
        with self.assertRaisesRegex(RuntimeError, 'unavailable'):
            module.build_candidates(self.root, self.manifest, 'a' * 40, 6, [1], self.root / 'failed', fail)
        self.assertFalse((self.root / 'failed/candidate.json').exists())


if __name__ == '__main__':
    unittest.main()
