"""Verify signed Data Release Steward receipt from a trusted external caller.

This module does not authenticate people or issue signatures. Only an external
identity-authorized steward service may hold the signing key.
"""
import hashlib
import hmac
import json
import os


def verify(envelope):
    if not isinstance(envelope, dict) or set(envelope) != {'payload', 'signature'}:
        raise ValueError('malformed signed Steward envelope')
    key = os.environ.get('MEMO_STEWARD_VERIFICATION_KEY', '').encode()
    principal = os.environ.get('MEMO_TRUSTED_STEWARD_PRINCIPAL', '')
    verifier = os.environ.get('MEMO_TRUSTED_STEWARD_VERIFIER', '')
    if len(key) < 32 or not principal or not verifier:
        raise ValueError('trusted Steward verifier not configured')
    payload = envelope['payload']
    if not isinstance(payload, dict) or not isinstance(envelope['signature'], str):
        raise ValueError('malformed Steward payload')
    mac = hmac.new(key, json.dumps(payload, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(mac, envelope['signature']):
        raise ValueError('Steward receipt signature invalid')
    if payload.get('receiver_id') != principal or payload.get('verification_method') != verifier:
        raise ValueError('Steward trusted identity mismatch')
    return payload
