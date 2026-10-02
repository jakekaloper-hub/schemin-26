import json
import pathlib
import re

ROOT=pathlib.Path(__file__).resolve().parents[3]

def read(p):
    return (ROOT/p).read_text(encoding="utf-8")

def test_dk_active_spec_is_one_body_gorilla_centaur():
    s=read("canon/characters/CHAR-WILSON-LOOK/T04_CHARACTER_SPEC.md")
    assert "ONE hybrid centaur-bodied gorilla warrior" in s
    assert "FOUR-LEGGED centaur/equine lower body" in s
    assert "Arsenal supporter" in s
    assert "centaur; equine body" not in s

def test_tds_exactly_three_heads_one_body():
    s=read("canon/characters/CHAR-PHILLIP-PITTS/T04_CHARACTER_SPEC.md")
    assert "ONE reptilian humanoid BODY with EXACTLY THREE serpent HEADS" in s
    assert "older instruction saying TDS is single-headed or “never three heads” is STALE" in s

def test_hmb_belt_keeper_not_rename_redesign():
    s=read("canon/characters/CHAR-AUSTIN-BYARS/T04_CHARACTER_SPEC.md")
    assert "CHAMPIONSHIP BELT IDENTITY-CRITICAL" in s
    assert "NO_KING_CROWN" in s
    assert "NO_VAMPIRE_BLOOD_MASCOT" in s

def test_visual_authority_records_outlier_reconciliation():
    a=json.loads(read("canon/characters/VISUAL_REFERENCE_AUTHORITY_V1.json"))
    r=a["outlier_reconciliation_2026_10_02"]
    assert r["status"]=="ACTIVE"
    assert set(r["characters"])=={"CHAR-WILSON-LOOK","CHAR-PHILLIP-PITTS","CHAR-AUSTIN-BYARS"}

def test_week4_receipt_uses_correct_dk():
    s=read("memo-os/week-4/WEEK_4_TEMPORAL_CANON_RECEIPT_V1.md")
    assert "Arsenal Gorilla Centaur Warrior" in s
    assert "FOUR-LEGGED centaur/equine lower body" in s

def test_active_core_files_do_not_reassert_retired_centaur():
    active=[
      "canon/_INDEX.md",
      "canon/CHARACTER_REFERENCE_LAYER_V1.md",
      "memo-os/week-4/WEEK_4_TEMPORAL_CANON_RECEIPT_V1.md",
      "memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_3_CHARACTER_REFERENCE_ENFORCEMENT_PATCH.md",
      "world/divisions/BURGERS_DIVISION_INDEX_V1.md",
      "world/domains/OWNER_DOMAIN_REGISTER_V1.md",
      "canon/characters/CHAR-WILSON-LOOK/T04_CHARACTER_SPEC.md",
    ]
    forbidden=[r"centaur/equine (?:form|design|identity) (?:is )?RETIRED",r"NO centaur",r"centaur anatomy is retired"]
    for p in active:
        s=read(p)
        for pat in forbidden:
            assert not re.search(pat,s,re.I), (p,pat)
