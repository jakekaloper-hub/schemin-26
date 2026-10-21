#!/usr/bin/env python3
"""Memo OS pre-render editorial fact and story-room guardrails.

This validates evidence contracts, NOT authenticity of external providers or
independent human editorial approval. No new canon is created.
"""
import argparse
import datetime as dt
import json
import re

SHA = re.compile(r"^[0-9a-f]{64}$")
KINDS = {"NFL_NEWS", "ESPN_TRANSACTION", "WAIVER_CLAIM", "PLAYER_PERFORMANCE", "BENCH_COMPARISON", "TRADE", "UPCOMING_MATCHUP"}

def timestamp(s):
    if not isinstance(s, str):
        return None
    try:
        x = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
        return x if x.tzinfo is not None else None
    except ValueError:
        return None

def validate_sports(packet):
    errors = []
    cutoff = timestamp(packet.get("editorial_cutoff"))
    if cutoff is None:
        errors.append("editorial cutoff must be timezone-aware ISO8601")
    claims = packet.get("claims")
    if not isinstance(claims, list) or not claims:
        return errors + ["sports claims required"]
    seen = set()
    for i, claim in enumerate(claims, 1):
        prefix = f"claim {i}"
        if not isinstance(claim, dict):
            errors.append(f"{prefix}: invalid claim")
            continue
        cid = claim.get("claim_id")
        if not isinstance(cid, str) or not cid.strip() or cid in seen:
            errors.append(f"{prefix}: missing or duplicate claim ID")
        seen.add(cid)
        kind = claim.get("kind")
        if kind not in KINDS:
            errors.append(f"{prefix}: unsupported kind")
        if not isinstance(claim.get("source_provider"), str) or not claim["source_provider"].strip():
            errors.append(f"{prefix}: missing source provider")
        if not isinstance(claim.get("source_reference"), str) or not claim["source_reference"].strip():
            errors.append(f"{prefix}: missing source reference")
        fetched = timestamp(claim.get("retrieved_at"))
        event = timestamp(claim.get("event_at"))
        if fetched is None or event is None:
            errors.append(f"{prefix}: event and retrieval timestamps required")
        if cutoff and ((fetched and fetched > cutoff) or (event and event > cutoff)):
            errors.append(f"{prefix}: information after editorial cutoff")
        if not SHA.fullmatch(str(claim.get("source_sha256", ""))):
            errors.append(f"{prefix}: missing source SHA256")
        if kind in {"WAIVER_CLAIM", "ESPN_TRANSACTION", "TRADE"} and claim.get("transaction_status") != "COMPLETED":
            errors.append(f"{prefix}: transaction not completed")
        if kind == "BENCH_COMPARISON":
            if claim.get("lineup_placement") != "BENCH":
                errors.append(f"{prefix}: bench placement not verified")
            if claim.get("changes_result") is True and claim.get("eligibility_verified") is not True:
                errors.append(f"{prefix}: hypothetical result requires eligibility verification")
        if kind == "NFL_NEWS" and claim.get("medical_claim") and claim.get("news_verification") != "CONTEMPORARY_SOURCE":
            errors.append(f"{prefix}: medical news requires contemporary source verification")
        if not isinstance(claim.get("text"), str) or not claim["text"].strip():
            errors.append(f"{prefix}: editorial claim text missing")
    return errors

def validate_story(packet):
    errors = []
    if packet.get("status") not in {"CANDIDATE", "EDITORIAL_LOCKED"}:
        errors.append("story status invalid")
    for key in ("matchup_id", "home_team_id", "away_team_id", "location_id", "premise", "setup", "escalation", "payoff", "camera_axis", "environment_continuity", "manuscript_sha256"):
        if not isinstance(packet.get(key), str) or not packet[key].strip():
            errors.append(f"story missing {key}")
    if not SHA.fullmatch(str(packet.get("manuscript_sha256", ""))):
        errors.append("story manuscript hash invalid")
    if packet.get("home_team_id") == packet.get("away_team_id"):
        errors.append("story matchup teams must differ")
    if packet.get("location_authority") not in {"ESTABLISHED", "CANDIDATE"}:
        errors.append("location authority invalid")
    if packet.get("character_reference_status") != "VERIFIED":
        errors.append("BLOCKED_BY_CHARACTER_REFERENCE_PIPELINE")
    if packet.get("result_status") != "FINAL":
        errors.append("story factual result not final")
    return errors

def main():
    p = argparse.ArgumentParser()
    p.add_argument("packet")
    p.add_argument("--kind", choices=["sports", "story"], required=True)
    a = p.parse_args()
    data = json.load(open(a.packet, encoding="utf-8"))
    errors = validate_sports(data) if a.kind == "sports" else validate_story(data)
    print(json.dumps({"verdict": "FAIL" if errors else "PASS", "errors": errors}, indent=2))
    return bool(errors)

if __name__ == "__main__":
    raise SystemExit(main())
