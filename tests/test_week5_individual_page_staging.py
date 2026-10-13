"""Week 5 controlled pre-generation acceptance: source contracts, not art certification."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEEK5 = ROOT / "memo-os" / "week-5"
MANIFEST = WEEK5 / "PUBLICATION_PAGE_MANIFEST.json"
ASSETS = WEEK5 / "production-evidence" / "WEEK_5_CHARACTER_SOURCE_ASSET_RECEIPTS_2026-10-13.json"
SCORES = WEEK5 / "production-evidence" / "WEEK_5_12_TEAM_STARTER_SUM_AND_WEEK6_FIXTURES_2026-10-13.json"

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_exactly_32_existing_source_pages_and_no_pagination_promotion():
    d = read_json(MANIFEST)
    pages = d["pages"]
    assert [r["page_id"] for r in pages] == [f"P{i:03d}" for i in range(1, 33)]
    assert all(r["state"] == "CONTRACTED_PARTIAL" for r in pages)
    assert all(r["render_eligible"] is False for r in pages)
    assert len({r["packet_path"] for r in pages}) == 32

def test_each_source_page_has_exactly_one_isolated_handoff():
    d = read_json(MANIFEST)
    for r in d["pages"]:
        pid = r["page_id"]
        path = ROOT / r["packet_path"]
        assert path.is_file(), f"{pid}: page packet missing"
        s = path.read_text(encoding="utf-8")
        needle = "## Page-isolated generator staging — 2026-10-13" if 4 <= int(pid[1:]) <= 27 else "## Page-isolated editorial production staging — 2026-10-13"
        assert s.count(needle) == 1, f"{pid}: handoff duplicated/missing"
        assert "render_eligible=true" not in s
        if 4 <= int(pid[1:]) <= 27:
            assert "## Integrated full-page narrative manuscript" in s, f"{pid}: missing scene-specific source manuscript"
            assert "Visual coordination from approved page brief" in s, f"{pid}: missing shot-to-prose specification"

def test_owner_source_paths_are_12_distinct_originals_and_not_false_render_proofs():
    d = read_json(ASSETS)
    a = d["assets"]
    assert len(a) == 12
    assert len({x["character_id"] for x in a}) == 12
    assert len({x["path"] for x in a}) == 12
    assert d["renderer_mount_state"] == "NOT_PROVEN"
    assert d["subject_binding_state"] == "NOT_PROVEN"
    assert d["render_permission"] == "HOLD"
    for x in a:
        p = ROOT / x["path"]
        assert p.is_file(), x["character_id"]
        assert p.stat().st_size == x["bytes"], x["character_id"]
        assert len(x["git_blob_sha1"]) == 40
        assert x["raw_sha256"] is None
        assert x["renderer_mount_receipt"] is None

def test_provisional_week5_starter_evidence_does_not_promote_a_winner():
    d = read_json(SCORES)
    assert len(d["teams"]) == 12
    assert len(d["matchups"]) == 6
    assert len(d["week6_fixtures"]) == 6
    assert all(m["winner"] == "UNDECIDED" for m in d["matchups"])
    assert all(x["starter_count"] == 10 and x["delta"] == 0 and x["period_status"] == "PROVISIONAL" for x in d["teams"])
    assert d["official_settlement"] == "HOLD"

def test_pitty_data_is_deliberately_deferred_without_blocking_other_briefs():
    p = (WEEK5 / "pages" / "P030-pittys-book" / "PAGE_PACKET.md").read_text(encoding="utf-8")
    assert "PITTY_INPUT_DEFERRED_TO_2026-10-14" in p
    assert "do not manufacture any entry" in p.lower()

def test_known_post_mnf_stale_page_headers_are_reconciled():
    for slug, banned in [
        ("P012-chili-nino-overture", "130.40"),
        ("P015-chili-nino-payoff", "130.40"),
        ("P016-duck-dk-overture", "119.34"),
        ("P020-chins-slob-overture", "168.76"),
        ("P023-chins-slob-payoff", "100.20"),
        ("P024-red-obi-overture", "81.20"),
    ]:
        s = (WEEK5 / "pages" / slug / "PAGE_PACKET.md").read_text(encoding="utf-8")
        assert banned not in s, f"{slug} still contains stale provisional number"
    for slug in ["P026-red-obi-escalation", "P027-red-obi-payoff"]:
        s = (WEEK5 / "pages" / slug / "PAGE_PACKET.md").read_text(encoding="utf-8")
        assert "fourteen catches" not in s
        assert "seventeen" in s
