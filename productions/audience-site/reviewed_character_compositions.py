"""Consume explicitly allowlisted profile art; never grant generation eligibility.

Repository review is the activation boundary. Hashes bind records, not identities;
this consumer does not authenticate a reviewer or mint a runtime eligibility token.
"""
import hashlib
import importlib.util
from io import BytesIO
import json
from pathlib import Path
from urllib.parse import quote
from PIL import Image

REGISTRY = 'productions/audience-site/artwork/ACCEPTED_CHARACTER_COMPOSITIONS.json'
REFERENCE_MODULE = Path(__file__).resolve().parents[2] / 'canon/characters/runtime/reference_authority.py'


def load_compositions(root, output, revision):
    root = Path(root).resolve()
    target = Path(output).resolve() / 'character-compositions'
    if target.is_symlink() or root.is_relative_to(target.resolve()):
        raise ValueError('Composition output cannot alias source repository')
    sources_read = []

    def read(path, expected=None):
        if not isinstance(path, str) or not path or Path(path).is_absolute():
            raise ValueError('Composition requires repository-relative source path')
        source = (root / path).resolve()
        if not source.is_relative_to(root):
            raise ValueError('Composition source escapes repository')
        sources_read.append(source)
        raw = source.read_bytes()
        if expected is not None and (not isinstance(expected, str) or len(expected) != 64
                or any(c not in '0123456789abcdef' for c in expected)
                or hashlib.sha256(raw).hexdigest() != expected):
            raise ValueError('Composition source hash mismatch')
        return raw, source

    def document(path, expected=None):
        def unique(pairs):
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError('Duplicate composition JSON key')
                result[key] = value
            return result
        value = json.loads(read(path, expected)[0], object_pairs_hook=unique)
        if not isinstance(value, dict):
            raise ValueError('Composition record must be an object')
        return value

    registry = document(REGISTRY)
    if type(registry.get('schemaVersion')) is not int or registry['schemaVersion'] != 1 or not isinstance(registry.get('accepted'), list):
        raise ValueError('Invalid composition acceptance registry')
    assets, pending = {}, []
    if registry['accepted']:
        sources = document('canon/characters/reference_sources_v1.json')
        authority = document('canon/characters/VISUAL_REFERENCE_AUTHORITY_V1.json')
        spec = importlib.util.spec_from_file_location('composition_reference_authority', REFERENCE_MODULE)
        resolver = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(resolver)
    for entry in registry['accepted']:
        if not isinstance(entry, dict):
            raise ValueError('Invalid composition allowlist entry')
        for field in ('packetSha256', 'reviewReceiptSha256', 'executionReceiptSha256'):
            if not isinstance(entry.get(field), str) or len(entry[field]) != 64 or any(c not in '0123456789abcdef' for c in entry[field]):
                raise ValueError('Exact composition receipt hash required')
        packet = document(entry.get('packet'), entry['packetSha256'])
        review = document(entry.get('reviewReceipt'), entry['reviewReceiptSha256'])
        execution = document(entry.get('executionReceipt'), entry['executionReceiptSha256'])
        digest = packet.get('assetSha256')
        if not isinstance(digest, str) or len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest):
            raise ValueError('Exact composition image hash required')
        cid = packet.get('characterId')
        if not isinstance(cid, str) or not cid.startswith('CHAR-') or cid in assets:
            raise ValueError('Unknown or duplicate composition character')
        if packet.get('scope') != 'PROFILE_PRESENTATION_ONLY':
            raise ValueError('Composition cannot activate canon or generation')
        reference = packet.get('reference')
        if not isinstance(reference, dict):
            raise ValueError('Composition reference binding required')
        expected = resolver.expected_source(cid, sources)
        if not expected or reference.get('path') != expected.get('repository_path'):
            raise ValueError('Composition must bind current canonical source path')
        read(reference.get('path'), reference.get('sha256'))
        verdict = resolver.validate_reference_candidate(cid, {
            'sha256': reference.get('sha256'), 'asset_id': reference.get('assetId'),
            'source_kind': reference.get('sourceKind'), 'filename': reference.get('filename')}, sources, authority)
        if verdict.get('state') != 'REFERENCE_AUTHORITY_RESOLVED':
            raise ValueError('Composition reference authority unresolved: ' + str(verdict.get('reason')))
        fields = ('requestId', 'route', 'mountReceiptId', 'generationReferenceId', 'subjectBindingId', 'outputInstanceId')
        if any(not isinstance(packet.get(k), str) or not packet[k].strip() for k in fields):
            raise ValueError('Composition requires exact generation execution binding')
        expected_execution = {'request_id':packet['requestId'], 'route':packet['route'],
            'mount_receipt_ids':[packet['mountReceiptId']],
            'generation_reference_ids':[packet['generationReferenceId']],
            'subject_binding_ids':[packet['subjectBindingId']]}
        if (execution.get('state') != 'GENERATION_EXECUTED_PENDING_CHARACTER_QA'
                or execution.get('renderer_invoked') is not True
                or execution.get('output_instance_id') != packet['outputInstanceId']
                or execution.get('execution_receipt') != expected_execution):
            raise ValueError('Composition generation execution not proven')
        for field in ('reviewer', 'preparedBy'):
            if not isinstance(review.get(field), str) or not review[field].strip():
                raise ValueError('Composition independent review identities required')
        if (review['reviewer'].strip().casefold() == review['preparedBy'].strip().casefold()
                or review.get('decision') != 'ACCEPTED_FOR_PROFILE_PRESENTATION'
                or review.get('scope') != packet['scope']
                or review.get('packetSha256') != entry['packetSha256']
                or review.get('executionReceiptSha256') != entry['executionReceiptSha256']
                or review.get('characterId') != cid
                or review.get('outputInstanceId') != packet['outputInstanceId']
                or review.get('assetSha256') != packet.get('assetSha256')
                or review.get('referenceSha256') != reference.get('sha256')
                or review.get('checks') != {'identity':'PASS','sourceBinding':'PASS','composition':'PASS','mobileCrop':'PASS'}):
            raise ValueError('Missing independent artifact-bound composition acceptance')
        raw, source = read(packet.get('assetPath'), packet.get('assetSha256'))
        if source.suffix.lower() not in {'.png', '.webp', '.jpg', '.jpeg'}:
            raise ValueError('Unsupported composition image format')
        with Image.open(BytesIO(raw)) as image:
            image.verify()
        with Image.open(BytesIO(raw)) as image:
            image.load()
            width, height = image.size
        if not isinstance(packet.get('alt'), str) or not packet['alt'].strip():
            raise ValueError('Composition requires reviewed alternative text')
        filename = cid + '-' + packet['assetSha256'] + source.suffix.lower()
        destination = (target / filename).resolve()
        if destination.parent != target.resolve() or destination == source:
            raise ValueError('Composition output must be separate from input')
        if destination.exists() and destination.read_bytes() != raw:
            raise ValueError('Composition output conflicts with existing bytes')
        pending.append((destination, raw))
        assets[cid] = {'file':filename, 'alt':packet['alt'], 'width':width, 'height':height,
            'sha256':packet['assetSha256'], 'reviewUrl':f'https://github.com/jakekaloper-hub/schemin-26/blob/{revision}/{quote(entry["reviewReceipt"])}'}
    # Revocation removes previous generated art, but never unknown/user files.
    # The ownership marker is build bookkeeping, not approval evidence.
    if any(source.is_relative_to(target.resolve()) for source in sources_read):
        raise ValueError('Composition output must be separate from input')
    marker = target / '.generated-compositions.json'
    old = {}
    if target.exists():
        if not target.is_dir() or not marker.is_file() or marker.is_symlink():
            raise ValueError('Composition output conflicts with existing bytes: unmanaged folder')
        old = json.loads(marker.read_text())
        if not isinstance(old, dict):
            raise ValueError('Invalid composition output ownership marker')
        if set(p.name for p in target.iterdir()) != set(old) | {marker.name}:
            raise ValueError('Composition output conflicts with existing bytes: unknown files')
        for filename, expected_hash in old.items():
            path = target / filename
            if (Path(filename).name != filename or path.is_symlink() or not path.is_file()
                    or hashlib.sha256(path.read_bytes()).hexdigest() != expected_hash):
                raise ValueError('Composition output conflicts with existing bytes: changed managed file')
    # All evidence and existing output bytes are checked before any deletion.
    for filename in old:
        (target / filename).unlink()
    if not pending:
        if marker.exists():
            marker.unlink()
            target.rmdir()
        return {'schemaVersion': 1, 'assets': assets}
    target.mkdir(parents=True, exist_ok=True)
    ownership = {}
    for path, raw in pending:
        path.write_bytes(raw)
        ownership[path.name] = hashlib.sha256(raw).hexdigest()
    marker.write_text(json.dumps(ownership, sort_keys=True))
    return {'schemaVersion':1, 'assets':assets}
