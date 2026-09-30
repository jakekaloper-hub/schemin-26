#!/usr/bin/env python3
"""Validate and normalize Flaim fantasy-league evidence receipts.

Flaim is an authorized read-only provider adapter, not an independent Schemin
source of truth. This adapter accepts the legacy Week-4 receipt and the
period-aware receipt contract introduced in CP8.
"""
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

EXPECTED_LEAGUE_ID="1417621"
EXPECTED_SEASON=2026
EXPECTED_TEAMS=12

class FlaimContractError(ValueError): pass

def _parse_iso(value:str)->datetime:
    if not value: raise FlaimContractError("captured_at missing")
    parsed=datetime.fromisoformat(value.replace("Z","+00:00"))
    if parsed.tzinfo is None: parsed=parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)

def snapshot_age_seconds(captured_at:str,now:datetime|None=None)->int:
    captured=_parse_iso(captured_at); current=now or datetime.now(timezone.utc)
    if current.tzinfo is None: current=current.replace(tzinfo=timezone.utc)
    return max(0,int((current.astimezone(timezone.utc)-captured).total_seconds()))

def _matchup_block(data):
    # CP8 canonical shape.
    if "matchups" in data:
        block=data["matchups"] or {}
        if not isinstance(block,dict): raise FlaimContractError("matchups must be object")
        week=block.get("matchup_period")
        rows=block.get("rows") or []
        return week,rows
    # Backward-compatible legacy Week-4 evidence.
    return 4,data.get("week4_matchups") or []

def validate_capture(data:dict[str,Any])->None:
    errors=[]
    if data.get("provider")!="flaim": errors.append("provider must be flaim")
    if data.get("upstream_platform")!="espn": errors.append("upstream_platform must be espn")
    league=data.get("league") or {}
    if str(league.get("league_id"))!=EXPECTED_LEAGUE_ID: errors.append("wrong league id")
    if int(league.get("season",0))!=EXPECTED_SEASON: errors.append("wrong season")
    if int(league.get("team_count",0))!=EXPECTED_TEAMS: errors.append("expected 12 teams")
    teams=league.get("teams") or []
    if len(teams)!=EXPECTED_TEAMS: errors.append("league teams must contain 12 rows")
    ids=[str(t.get("team_id")) for t in teams]
    if len(ids)!=len(set(ids)): errors.append("duplicate league team ids")
    if any(not str(t.get("team_name","")).strip() for t in teams): errors.append("empty league team name")
    standings=data.get("standings") or []
    if len(standings)!=EXPECTED_TEAMS: errors.append("standings must contain 12 rows")
    if {str(s.get("team_id")) for s in standings}!=set(ids): errors.append("standings team set does not match league team set")
    week,rows=_matchup_block(data)
    if not isinstance(week,int) or week<1: errors.append("invalid matchup period")
    if len(rows)!=6: errors.append("matchup period must contain exactly 6 matchups")
    mids=[]
    for m in rows:
        home=str((m.get("home") or {}).get("team_id")); away=str((m.get("away") or {}).get("team_id"))
        if home==away: errors.append("matchup cannot contain same team twice")
        mids.extend([home,away])
    if sorted(mids)!=sorted(ids): errors.append("matchup team set must contain each team exactly once")
    rosters=data.get("rosters") or []
    if len(rosters)!=EXPECTED_TEAMS: errors.append("rosters must contain 12 team snapshots")
    if {str(r.get("team_id")) for r in rosters}!=set(ids): errors.append("roster team set does not match league team set")
    for r in rosters:
        if (r.get("snapshot") or {}).get("type")!="current": errors.append(f"roster {r.get('team_id')} is not current snapshot")
        if not r.get("players"): errors.append(f"roster {r.get('team_id')} has no players")
    tx=data.get("transactions") or {}; txrows=tx.get("rows") or []
    if int(tx.get("count",-1))!=len(txrows): errors.append("transaction count does not equal row count")
    if tx.get("source") not in {"mTransactions2","mTransactions2_with_activity_trade_details","activity_feed"}:
        errors.append("unknown ESPN transaction source")
    _parse_iso(str(data.get("captured_at","")))
    if errors: raise FlaimContractError("; ".join(errors))

def normalize_capture(data:dict[str,Any],*,now:datetime|None=None,slo_seconds:int=3600)->dict[str,Any]:
    validate_capture(data)
    age=snapshot_age_seconds(data["captured_at"],now=now)
    week,matchups=_matchup_block(data); tx=data["transactions"]
    return {
      "meta":{"league_id":int(data["league"]["league_id"]),"season":int(data["league"]["season"]),
              "source":"flaim-espn-adapter","captured_at":data["captured_at"],
              "snapshot_age_seconds":age,"stale":age>slo_seconds,
              "freshness_slo_seconds":slo_seconds,"failure_reason":None,
              "provider_limitations":data.get("limitations",[])},
      "league":data["league"],"standings":data["standings"],
      "matchup_period":week,"matchups":matchups,"rosters":data["rosters"],
      "transactions":{**tx,"exact_trade_assets_complete":not bool((tx.get("limitations") or {}).get("structured_details_incomplete"))}
    }

def normalize_lkg(data:dict[str,Any],*,failure_reason:str,now:datetime|None=None)->dict[str,Any]:
    """Fallback is usable only after the stored receipt validates; it is always stale."""
    out=normalize_capture(data,now=now)
    out["meta"]["stale"]=True
    out["meta"]["failure_reason"]=failure_reason
    out["meta"]["source"]="flaim-espn-adapter-lkg"
    return out

def main():
    p=argparse.ArgumentParser(); p.add_argument("capture",type=Path); p.add_argument("--slo-seconds",type=int,default=3600); p.add_argument("--output",type=Path)
    a=p.parse_args(); data=json.loads(a.capture.read_text()); normalized=normalize_capture(data,slo_seconds=a.slo_seconds)
    payload=json.dumps(normalized,indent=2)+"\n"
    if a.output: a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(payload)
    else: print(payload,end="")
if __name__=="__main__": main()
