import copy, importlib.util, json
from datetime import datetime, timezone
from pathlib import Path
import pytest
ROOT=Path(__file__).parents[1]
def load(name,path):
    s=importlib.util.spec_from_file_location(name,ROOT/path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
flaim=load("cp8_flaim",Path("data-gateway/flaim_adapter.py"))
truth=load("cp8_truth",Path("member-gateway/truth_plane_adapter.py"))
legacy=json.loads((ROOT/"data/provider-receipts/flaim/1417621/2026/week-4/2026-09-29T175654Z.json").read_text())

def period_receipt(week=5):
    d=copy.deepcopy(legacy)
    rows=d.pop("week4_matchups")
    for m in rows: m["matchupPeriodId"]=week
    d["matchups"]={"matchup_period":week,"rows":rows}
    return d

def test_legacy_week4_remains_valid():
    flaim.validate_capture(legacy)
    assert flaim.normalize_capture(legacy,now=datetime(2026,9,29,18,0,tzinfo=timezone.utc))["matchup_period"]==4

def test_period_aware_receipt_is_not_hardcoded_to_week4():
    d=period_receipt(5); flaim.validate_capture(d)
    n=flaim.normalize_capture(d,now=datetime(2026,9,29,18,0,tzinfo=timezone.utc))
    assert n["matchup_period"]==5 and len(n["matchups"])==6

def test_period_aware_receipt_rejects_duplicate_team():
    d=period_receipt(5)
    d["matchups"]["rows"][0]["away"]["team_id"]=d["matchups"]["rows"][0]["home"]["team_id"]
    with pytest.raises(flaim.FlaimContractError): flaim.validate_capture(d)

def test_lkg_is_always_stale_and_reasoned():
    n=flaim.normalize_lkg(legacy,failure_reason="LIVE_PROVIDER_UNAVAILABLE",
        now=datetime(2026,9,29,18,0,tzinfo=timezone.utc))
    assert n["meta"]["stale"] is True
    assert n["meta"]["failure_reason"]=="LIVE_PROVIDER_UNAVAILABLE"
    assert n["meta"]["source"].endswith("-lkg")

def test_lkg_must_still_validate():
    bad=copy.deepcopy(legacy); bad["league"]["league_id"]="999"
    with pytest.raises(flaim.FlaimContractError):
        flaim.normalize_lkg(bad,failure_reason="LIVE_PROVIDER_UNAVAILABLE")

def test_period_truth_packet_preserves_freshness_and_period():
    d=period_receipt(5)
    n=flaim.normalize_capture(d,now=datetime(2026,9,29,18,0,tzinfo=timezone.utc))
    p=truth.from_normalized_data_gateway(n)
    assert p["freshness"]["stale"] is False
    assert p["result"]["matchups"][0]["matchupPeriodId"]==5
