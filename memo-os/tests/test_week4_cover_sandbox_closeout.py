import unittest
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "governance" / "publication-manifest"))
from memo_reference_resolver import resolve_memo_reference

def read(p):
    return (ROOT / p).read_text(encoding="utf-8")

class CloseoutTests(unittest.TestCase):
    def test_latest_memo_is_week3_not_week2():
        p=resolve_memo_reference("latest memo")
        assert p["publication_id"]=="memo.2026.week-03"
        assert p["canonical_artifact"]=="Pro_Schemin_Week_3_Memo_Final.pdf"

    def test_week4_is_unreleased_and_sandbox_cannot_qualify():
        m=json.loads(read("governance/publication-manifest/PUBLICATION_MANIFEST_V1.json"))
        w4=next(x for x in m["publications"] if x["publication_id"]=="memo.2026.week-04")
        assert w4["release_state"]=="BLOCKED"
        assert w4["canonical_artifact"] is None
        close=read("memo-os/week-4/WEEK_4_COVER_SANDBOX_ACCEPTANCE_CLOSEOUT_2026-10-02.md")
        assert "NOT_THE_OFFICIAL_WEEK_4_COVER" in close
        assert "“NOW THE TARGET” is sandbox copy only" in close

    def test_dk_current_authority_defeats_stale_semantics():
        s=read("canon/characters/CHAR-WILSON-LOOK/T04_CHARACTER_SPEC.md")
        assert "Arsenal Gorilla Centaur Warrior" in s
        assert "FOUR-LEGGED centaur/equine lower body" in s
        assert "generic bipedal gorilla" in s
        receipt=read("memo-os/week-4/WEEK_4_TEMPORAL_CANON_RECEIPT_V1.md")
        assert "STALE / SUPERSEDED" in receipt
        assert "Current authority remains **Arsenal Gorilla Centaur Warrior**" in receipt

    def test_tds_current_authority_defeats_single_head():
        s=read("canon/characters/CHAR-PHILLIP-PITTS/T04_CHARACTER_SPEC.md")
        assert "EXACTLY THREE serpent HEADS" in s
        assert "single-headed reptile" in s

    def test_hmb_current_authority_defeats_rename_redesign():
        s=read("canon/characters/CHAR-AUSTIN-BYARS/T04_CHARACTER_SPEC.md")
        assert "CHAMPIONSHIP BELT IDENTITY-CRITICAL" in s
        assert "NO_KING_CROWN" in s
        assert "NO_VAMPIRE_BLOOD_MASCOT" in s

    def test_obiwan_is_beltless():
        i=read("canon/_INDEX.md")
        assert "Trade Jedi — NO championship belt" in i

    def test_cover_learning_is_binding_but_sandbox_story_is_not():
        v=read("memo-os/SCHEMIN_26_WEEKLY_MEMO_OS_V5_5_INTEGRATED_PREPRODUCTION_PATCH.md")
        assert "Cover ≠ matchup opening scene" in v
        assert "Reference controls identity, not staging" in v
        assert "Behavior is continuity" in v
        assert "Actual-pixel QA is mandatory" in v
        assert "Beautiful ≠ PASS" in v
        assert "Sandbox/canon firewall" in v


if __name__ == '__main__':
    unittest.main()
