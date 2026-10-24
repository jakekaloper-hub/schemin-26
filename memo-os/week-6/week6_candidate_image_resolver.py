"""Byte-verified preview-only Week 6 environment reference resolver.

Never returns an approved/canonical URI or asserts native generative-model bindings.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / 'memo-os/week-6/WEEK_6_EXACT_PNG_INGESTION_MANIFEST.json'
REGISTRY = ROOT / 'world/location-control-plane/registries/LOCATION_REFERENCE_REGISTRY.json'

class CandidateReferenceError(ValueError):
    pass

def resolve(location_id: str, *, mode: str = 'candidate_preview') -> dict:
    if mode != 'candidate_preview':
        raise CandidateReferenceError('CANONICAL_REFERENCE_UNAPPROVED')
    entries = json.loads(MANIFEST.read_text())['assets']
    matches = [asset for asset in entries if asset['location_id'] == location_id]
    if len(matches) != 1:
        raise CandidateReferenceError('UNKNOWN_OR_DUPLICATE_LOCATION_ID')
    asset = matches[0]
    registry = {item['location_id']:item for item in json.loads(REGISTRY.read_text())['locations']}
    if location_id not in registry or registry[location_id].get('approved_cinematic_reference_uris'):
        raise CandidateReferenceError('REGISTRY_STATE_REQUIRES_REVIEW')
    p = (ROOT / asset['candidate_uri']).resolve()
    base = (ROOT / 'world/environment-references/candidates/week-6' / location_id).resolve()
    if p.parent != base or not p.is_file():
        raise CandidateReferenceError('LOCATION_ASSET_MISSING_OR_MISMAPPED')
    data = p.read_bytes()
    if not data.startswith(bytes.fromhex('89504e470d0a1a0a')):
        raise CandidateReferenceError('INVALID_PNG')
    if hashlib.sha256(data).hexdigest() != asset['sha256'] or len(data) != asset['bytes']:
        raise CandidateReferenceError('SOURCE_HASH_OR_LENGTH_MISMATCH')
    width = int.from_bytes(data[16:20], 'big');height=int.from_bytes(data[20:24], 'big')
    if (width,height) != (asset['width'],asset['height']):
        raise CandidateReferenceError('PNG_DIMENSION_MISMATCH')
    return {'location_id':location_id, 'uri':asset['candidate_uri'], 'sha256':asset['sha256'],
            'width':width,'height':height,'status':'CANDIDATE_PREVIEW_ONLY',
            'canonical_approved':False,'native_renderer_binding_verified':False}
