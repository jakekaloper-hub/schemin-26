import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('reviewed_text', Path(__file__).resolve().parents[1] / 'reviewed_memo_text.py')
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)


class ReviewedTextTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.memos = [{'id': 'week-6', 'sha256': 'a' * 64, 'pageCount': 3}]
        self.packet = {'memoId': 'week-6', 'status': 'REVIEWED_TEXT_COMPANION',
                       'sourcePdfSha256': 'a' * 64, 'sourcePageCount': 3,
                       'pages': [{'physicalPage': 2, 'title': 'Fixture heading',
                                  'text': 'First paragraph.\n\n<script>Literal fixture text.</script>',
                                  'visualDescription': 'A fixture diagram with two boxes.'}]}
        self.packet['pages'][0]['textSha256'] = hashlib.sha256(self.packet['pages'][0]['text'].encode()).hexdigest()
        self.receipt = {'decision': 'ACCEPTED_FOR_TEXT_COMPANION', 'scope': 'TEXT_COMPANION_ONLY',
                        'sourcePdfSha256': 'a' * 64, 'reviewer': 'fixture-reviewer', 'preparedBy': 'fixture-preparer',
                        'acceptedPhysicalPages': [2],
                        'checks': {'textAccuracy': 'PASS', 'readingOrder': 'PASS', 'visualDescription': 'PASS'}}

    def write(self, path, value):
        target = self.root / path; target.parent.mkdir(parents=True, exist_ok=True)
        raw = (json.dumps(value) + '\n').encode(); target.write_bytes(raw)
        return hashlib.sha256(raw).hexdigest()

    def install(self):
        packet_hash = self.write('packet.json', self.packet)
        self.receipt['packetSha256'] = packet_hash
        receipt_hash = self.write('receipt.json', self.receipt)
        self.write(module.REGISTRY, {'schemaVersion': 1, 'accepted': [{
            'packet': 'packet.json', 'packetSha256': packet_hash,
            'reviewReceipt': 'receipt.json', 'reviewReceiptSha256': receipt_hash}]})

    def load(self):
        return module.load_companions(self.root, self.memos, 'b' * 40)

    def test_partial_accepted_companion_preserves_literal_text_and_provenance(self):
        self.install(); result = self.load()['week-6']
        self.assertEqual(list(result), ['2'])
        self.assertEqual(result['2']['text'], self.packet['pages'][0]['text'])
        self.assertEqual(result['2']['sourcePdfSha256'], 'a' * 64)
        self.assertIn('/' + 'b' * 40 + '/receipt.json', result['2']['reviewUrl'])

    def test_empty_allowlist_never_discovers_ocr_directories(self):
        self.write('ocr/packet.json', self.packet)
        self.write(module.REGISTRY, {'schemaVersion': 1, 'accepted': []})
        self.assertEqual(self.load(), {})

    def test_even_allowlisted_raw_ocr_or_unaccepted_receipt_is_rejected(self):
        for target, field, value in [(self.packet, 'status', 'UNREVIEWED_OCR_CANDIDATE'),
                                      (self.receipt, 'decision', 'PENDING'),
                                      (self.receipt, 'reviewer', 'fixture-preparer'),
                                      (self.receipt, 'checks', {})]:
            old = target[field]; target[field] = value
            self.install()
            with self.assertRaises(ValueError): self.load()
            target[field] = old

    def test_edited_packet_or_receipt_cannot_pass_approved_hash(self):
        for filename in ['packet.json', 'receipt.json']:
            self.install(); path = self.root / filename; path.write_text(path.read_text() + ' ')
            with self.assertRaisesRegex(ValueError, 'hash mismatch'): self.load()

    def test_wrong_source_invalid_duplicate_and_unaccepted_pages_fail(self):
        self.install(); self.memos[0]['sha256'] = 'c' * 64
        with self.assertRaisesRegex(ValueError, 'edition mismatch'): self.load()
        self.memos[0]['sha256'] = 'a' * 64
        for number in [0, 4, True]:
            self.packet['pages'][0]['physicalPage'] = number; self.install()
            with self.assertRaises(ValueError): self.load()
        self.packet['pages'][0]['physicalPage'] = 2
        self.packet['pages'].append(dict(self.packet['pages'][0])); self.install()
        with self.assertRaises(ValueError): self.load()

    def test_outside_repository_and_wrong_page_text_hash_fail(self):
        self.install(); registry = json.loads((self.root / module.REGISTRY).read_text())
        registry['accepted'][0]['packet'] = '../packet.json'; self.write(module.REGISTRY, registry)
        with self.assertRaisesRegex(ValueError, 'repository'): self.load()
        self.packet['pages'][0]['text'] = 'Unreviewed edit'; self.install()
        with self.assertRaisesRegex(ValueError, 'text hash'): self.load()

    def test_duplicate_json_keys_are_rejected_even_with_matching_digests(self):
        for filename in [module.REGISTRY, 'packet.json', 'receipt.json']:
            self.install()
            path = self.root / filename
            value = json.loads(path.read_text())
            key = next(iter(value))
            raw = ('{' + json.dumps(key) + ':' + json.dumps(value[key]) + ',' + path.read_text()[1:]).encode()
            path.write_bytes(raw)
            if filename != module.REGISTRY:
                registry = json.loads((self.root / module.REGISTRY).read_text())
                field = 'packetSha256' if filename == 'packet.json' else 'reviewReceiptSha256'
                registry['accepted'][0][field] = hashlib.sha256(raw).hexdigest()
                self.write(module.REGISTRY, registry)
            with self.assertRaisesRegex(ValueError, 'Duplicate JSON key'):
                self.load()

    def test_boolean_schema_or_source_count_is_not_an_integer(self):
        self.install(); registry = json.loads((self.root / module.REGISTRY).read_text())
        registry['schemaVersion'] = True; self.write(module.REGISTRY, registry)
        with self.assertRaises(ValueError): self.load()
        self.memos[0]['pageCount'] = 1; self.packet['sourcePageCount'] = True
        self.install()
        with self.assertRaisesRegex(ValueError, 'source edition mismatch'): self.load()
