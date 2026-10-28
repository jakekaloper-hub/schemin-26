"""Consume explicitly accepted repository text companions, never raw OCR folders.

The reviewed registry is the publication allowlist. Receipts bind bytes and record
review decisions; this module does not authenticate a person or certify accessibility.
"""
import hashlib
import json
from pathlib import Path
from urllib.parse import quote

REGISTRY = 'productions/audience-site/memo-text/ACCEPTED_COMPANIONS.json'


def load_companions(root, memos, revision):
    root = Path(root).resolve()

    def read(path, expected=None):
        if not isinstance(path, str) or not path:
            raise ValueError('Missing companion artifact path')
        target = (root / path).resolve()
        if not target.is_relative_to(root) or Path(path).is_absolute():
            raise ValueError('Companion artifact must remain in repository')
        raw = target.read_bytes()
        if expected is not None and hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError('Companion artifact hash mismatch')
        def unique_keys(pairs):
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError('Duplicate JSON key in companion artifact')
                result[key] = value
            return result
        return json.loads(raw, object_pairs_hook=unique_keys)

    registry = read(REGISTRY)
    if not isinstance(registry, dict) or type(registry.get('schemaVersion')) is not int or registry.get('schemaVersion') != 1 or not isinstance(registry.get('accepted'), list):
        raise ValueError('Invalid companion acceptance registry')
    editions = {memo['id']: memo for memo in memos}
    result = {}
    for entry in registry['accepted']:
        if not isinstance(entry, dict):
            raise ValueError('Invalid companion registry entry')
        for field in ('packetSha256', 'reviewReceiptSha256'):
            digest = entry.get(field)
            if not isinstance(digest, str) or len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest):
                raise ValueError('Missing exact companion artifact hash')
        packet = read(entry.get('packet'), entry['packetSha256'])
        receipt = read(entry.get('reviewReceipt'), entry['reviewReceiptSha256'])
        if not isinstance(packet, dict) or not isinstance(receipt, dict):
            raise ValueError('Companion packet and receipt must be objects')
        if not isinstance(packet.get('memoId'), str):
            raise ValueError('Invalid companion edition identity')
        memo = editions.get(packet.get('memoId'))
        if not memo or packet.get('status') != 'REVIEWED_TEXT_COMPANION':
            raise ValueError('Unknown edition or unreviewed text packet')
        if (packet.get('sourcePdfSha256') != memo['sha256']
                or type(packet.get('sourcePageCount')) is not int
                or packet.get('sourcePageCount') != memo['pageCount']):
            raise ValueError('Companion source edition mismatch')
        reviewer, preparer = receipt.get('reviewer'), receipt.get('preparedBy')
        if (receipt.get('decision') != 'ACCEPTED_FOR_TEXT_COMPANION'
                or receipt.get('scope') != 'TEXT_COMPANION_ONLY'
                or receipt.get('checks') != {'textAccuracy': 'PASS', 'readingOrder': 'PASS', 'visualDescription': 'PASS'}
                or receipt.get('packetSha256') != entry['packetSha256']
                or receipt.get('sourcePdfSha256') != memo['sha256']
                or not isinstance(reviewer, str) or not reviewer.strip()
                or not isinstance(preparer, str) or not preparer.strip()
                or reviewer.strip().casefold() == preparer.strip().casefold()):
            raise ValueError('Missing independent, exact-byte text acceptance')
        pages = packet.get('pages')
        if not isinstance(pages, list) or not pages:
            raise ValueError('No reviewed companion pages')
        accepted_pages = receipt.get('acceptedPhysicalPages')
        numbers = [page.get('physicalPage') for page in pages if isinstance(page, dict)]
        if (len(numbers) != len(pages) or any(type(n) is not int or not 1 <= n <= memo['pageCount'] for n in numbers)
                or len(set(numbers)) != len(numbers) or not isinstance(accepted_pages, list)
                or any(type(n) is not int for n in accepted_pages) or accepted_pages != sorted(numbers)):
            raise ValueError('Companion physical-page acceptance mismatch')
        if memo['id'] in result:
            raise ValueError('Duplicate accepted companion for edition')
        result[memo['id']] = {}
        for page in pages:
            for field in ('title', 'text', 'visualDescription'):
                if not isinstance(page.get(field), str) or not page[field].strip():
                    raise ValueError('Reviewed page requires title, text and visual description')
            text_hash = hashlib.sha256(page['text'].encode('utf-8')).hexdigest()
            if page.get('textSha256') != text_hash:
                raise ValueError('Reviewed page text hash mismatch')
            result[memo['id']][str(page['physicalPage'])] = {
                'physicalPage': page['physicalPage'], 'title': page['title'], 'text': page['text'],
                'visualDescription': page['visualDescription'], 'textSha256': text_hash,
                'packetSha256': entry['packetSha256'], 'sourcePdfSha256': memo['sha256'],
                'reviewUrl': f'https://github.com/jakekaloper-hub/schemin-26/blob/{revision}/{quote(entry["reviewReceipt"])}',
            }
    return result
