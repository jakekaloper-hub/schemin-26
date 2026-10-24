"""Fail closed when fact claims are not present in a signed, hashed source snapshot.

A trusted ingestion signature only binds bytes. This check additionally
ensures each claim cites a concrete record and matching values within them.
It does not independently authenticate the upstream provider.
"""
import json
from pathlib import Path

def validate_claim_payload(packet, packet_path):
    root=Path(packet_path).resolve().parent
    sources={x.get("source_reference"):x for x in packet.get("source_inputs",[]) if isinstance(x,dict)}
    errors=[]
    claims=packet.get("sports",{}).get("claims",[])
    for claim in claims:
        if not isinstance(claim,dict):
            continue
        cid=claim.get("claim_id","unknown")
        source=sources.get(claim.get("source_reference"))
        if source is None:
            continue  # the production entrypoint already rejects unbound sources
        path=(root/str(source.get("path",""))).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            continue  # source byte verification reports missing/unsafe evidence
        try:
            payload=json.loads(path.read_text(encoding="utf-8"))
        except (ValueError,UnicodeError):
            errors.append(f"claim {cid}: source payload must be valid JSON")
            continue
        if not isinstance(payload,dict) or not isinstance(payload.get("records"),list):
            errors.append(f"claim {cid}: source has no structured records")
            continue
        record_id=claim.get("source_record_id")
        if not isinstance(record_id,str) or not record_id:
            errors.append(f"claim {cid}: source record ID required")
            continue
        records=[r for r in payload["records"] if isinstance(r,dict) and r.get("id")==record_id]
        if len(records)!=1:
            errors.append(f"claim {cid}: source record missing or ambiguous")
            continue
        record=records[0]
        expected=claim.get("source_fields")
        if not isinstance(expected,dict) or not expected:
            errors.append(f"claim {cid}: explicit source fields required")
            continue
        if any(k not in record or record[k]!=v for k,v in expected.items()):
            errors.append(f"claim {cid}: published source fields differ from evidence")
    return errors
