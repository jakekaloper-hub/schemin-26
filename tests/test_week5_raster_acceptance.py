"""Regression tests for Week 5 page-image handoff; never claims final art QA."""
import hashlib
import importlib.util
import json
import struct
import zlib
from pathlib import Path

import pytest

P = Path(__file__).resolve().parents[1] / "memo-os/week-5/runtime/raster_acceptance.py"
spec = importlib.util.spec_from_file_location("raster_acceptance", P)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def _sha(value):
    return hashlib.sha256(value).hexdigest()


def _chunk(name, data):
    return struct.pack(">I", len(data)) + name + data + struct.pack(">I", zlib.crc32(name + data) & 0xffffffff)


def _png(w=1024):
    h = 1536
    hdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    pixels = (b"\x00" + b"\x01\x02\x03" * w) * h
    return mod.PNG_SIGNATURE + _chunk(b"IHDR", hdr) + _chunk(b"IDAT", zlib.compress(pixels)) + _chunk(b"IEND", b"")


@pytest.fixture
def case(tmp_path):
    week = tmp_path / "memo-os/week-5"
    (week / "production-evidence").mkdir(parents=True)
    (week / "pages/P004").mkdir(parents=True)
    (tmp_path / "assets").mkdir()
    a = b"original subject one"
    b = b"original subject two"
    (tmp_path / "assets/a.jpeg").write_bytes(a)
    (tmp_path / "assets/b.jpeg").write_bytes(b)
    rel = "memo-os/week-5/pages/P004/PAGE_PACKET.md"
    packet = tmp_path / rel
    prose = "Original approved words stay fixed."
    packet.write_text("**Narrative copy:**\n\n" + prose + "\n\n**Visual coordination from approved page brief:**")
    image = tmp_path / "SCHEMIN26_W05_P004_GOTW.png"
    image.write_bytes(_png())
    refs = [{"character_id": cid, "raw_sha256": _sha(src)} for cid, src in [("A", a), ("B", b)]]
    rows = [{"page_id": "P004", "packet_path": rel, "expected_flattened_png": image.name}]
    titles = [{"page_id": "P004", "display_header": "His Majesty's Blood at Three Dreaded Snake", "owner_reference_requirements": refs}]
    (week / "PUBLICATION_PAGE_MANIFEST.json").write_text(json.dumps({"pages": rows}))
    (week / "production-evidence/WEEK_5_CHARACTER_AND_TITLE_RENDER_GATES_2026-10-13.json").write_text(json.dumps({"pages": titles}))
    mounts = [{
        "character_id": cid, "original_repo_path": "assets/" + name,
        "mounted_repo_path": "assets/" + name, "subject_binding_id": cid,
        "generation_reference_id": "ref-" + cid,
    } for cid, name in [("A", "a.jpeg"), ("B", "b.jpeg")]]
    receipt = {
        "page_id": "P004", "png_sha256": _sha(image.read_bytes()),
        "visible_primary_header_transcription": titles[0]["display_header"],
        "league_masthead_dominates": False,
        "source_packet_sha256": _sha(packet.read_bytes()),
        "transcribed_editorial_copy": prose,
        "shot_role": mod.GOTW_ROLES["P004"], "editorial_text_area_percent": 70,
        "reference_mounts": mounts,
        "full_res_manual_pixel_review": True,
        "mobile_390px_manual_review": True
    }
    return tmp_path, image, receipt


def _check(case):
    root, image, receipt = case
    return mod.inspect_candidate("P004", image, receipt, root)


def test_matching_candidate_never_becomes_final_approval(case):
    result = _check(case)
    assert result["state"] == "TECHNICAL_CANDIDATE_CHECK_PASSED_PUBLICATION_HOLD"
    assert result["may_publish"] is False


@pytest.mark.parametrize("edit,reason", [
    ({"transcribed_editorial_copy": "Changed prose"}, "MANUSCRIPT_NOT_VERBATIM"),
    ({"visible_primary_header_transcription": "SCHEMIN 26"}, "MAIN_HEADER_NOT_VERIFIED"),
    ({"editorial_text_area_percent": 30}, "OVERTURE_EDITORIAL_RATIO_UNVERIFIED"),
    ({"shot_role": "OVERHEAD_MONUMENTAL_BOARD_AND_SHELTERED_STALLS"}, "GOTW_SCENE_ROLE_MISMATCH"),
])
def test_artifact_contract_rejects_drift(case, edit, reason):
    case[2].update(edit)
    assert _check(case)["reason"] == reason


def test_wrong_dimensions_rejected(case):
    case[1].write_bytes(_png(1023))
    assert _check(case)["reason"] == "INVALID_1024_X_1536_PNG"


def test_wrong_subject_bytes_rejected(case):
    case[2]["reference_mounts"][0]["mounted_repo_path"] = "assets/b.jpeg"
    assert _check(case)["reason"] == "SOURCE_OR_MOUNT_BYTES_WRONG"


def test_missing_review_rejected(case):
    case[2]["full_res_manual_pixel_review"] = False
    assert _check(case)["reason"] == "PIXEL_AND_MOBILE_REVIEW_UNVERIFIED"
