"""Adapter from existing Schemin Data Gateway normalized packets to Member Gateway truth packets."""
from typing import Any, Mapping

class TruthPlaneAdapterError(ValueError):
    pass

def from_normalized_data_gateway(normalized: Mapping[str, Any]) -> dict[str, Any]:
    meta = normalized.get("meta") or {}
    required = {"stale","captured_at","snapshot_age_seconds","failure_reason"}
    missing = sorted(required - set(meta.keys()))
    if missing:
        raise TruthPlaneAdapterError("INVALID_DATA_GATEWAY_META:" + ",".join(missing))
    return {
        "result": {
            "league": normalized.get("league"),
            "standings": normalized.get("standings"),
            "matchups": normalized.get("matchups"),
            "rosters": normalized.get("rosters"),
            "transactions": normalized.get("transactions"),
        },
        "freshness": {
            "stale": meta["stale"],
            "fetched_at": meta["captured_at"],
            "snapshot_age_seconds": meta["snapshot_age_seconds"],
            "failure_reason": meta["failure_reason"],
        },
        "provenance": [{
            "authority":"League Data Platform",
            "source":meta.get("source"),
            "captured_at":meta.get("captured_at"),
        }],
        "limitations": list(meta.get("provider_limitations") or []),
        "authority_status":"BULLPEN_ROUTED",
        "qa_status":"DATA_GATEWAY_VALIDATED",
    }
