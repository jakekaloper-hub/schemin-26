#!/usr/bin/env python3
"""Fail-closed read-only Atlas expansion and photo-library cross-PR handshake.

This test reads PR324 checked-in evidence; optionally validates the *existing*
PR253 external checkout without copying or promoting any image. It does not
access other live ChatGPT conversations or private asset stores.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(ok: bool, reason: str):
    if not ok:
        raise AssertionError(reason)


def local_validate():
    cross = read(HERE / "CROSS_PR_324_325_CANDIDATE_RECONCILIATION_V1.json")
    handoff = read(HERE / "PARALLEL_PHOTO_LIBRARY_HANDOFF_V1.json")
    original = read(ROOT / "world/data/atlas_location_candidates.json")["candidates"]
    active = read(ROOT / "world/data/locations.json")["locations"]
    pinned = read(HERE / "ISLAND_TOPOLOGY_PINNED_SOURCE_V1.json")
    lineup = read(ROOT / "canon/characters/APPROVED_LINEUP_2026_10_18.json")["individuals"]
    source_new = {
        item["id"]: item for item in original
        if "Founder location-expansion directive 2026-11-20" in item.get("source_provenance", [])
    }
    rows = cross["rows"]
    counts = cross["counts"]
    ids = [row["pr325_id"] for row in rows]
    require(len(source_new) == 40 and len(rows) == 44, "Cross-PR candidate baseline drift")
    require(len(ids) == len(set(ids)) == 44, "Cross-PR source ID duplicates")
    require(not set(ids).intersection(source_new), "Candidate ID collision missed")
    require(all(row["equivalence_status"] == "UNDECIDED_NOT_DISTINCT_NOT_DUPLICATE"
                and row["canon_promotion_allowed"] is False for row in rows),
            "Unreviewed cross-PR site declared resolved or promoted")
    active_ids = {l["id"] for l in active}
    island_ids = {n["id"] for n in pinned["node_records"]}
    anchored = 0
    for row in rows:
        anchor = row["pr325_anchor"]
        same = row["pr324_same_anchor_options"]
        expect = [x for x in source_new.values() if anchor in x.get("related_active_location_ids", [])]
        require([x["id"] for x in same] == [x["id"] for x in expect],
                f"Cross-branch same-parent list is stale: {row['pr325_id']}")
        require(all(x["name"] == source_new[x["id"]]["working_name"] for x in same),
                f"Cross-branch paired names drifted: {row['pr325_id']}")
        if anchor.startswith("POST-NODE:"):
            require(anchor[10:] in island_ids and not same,
                    f"Unconfirmed new offshore anchor: {row['pr325_id']}")
        else:
            require(anchor in active_ids, f"Unknown native LOC parent: {row['pr325_id']}")
        anchored += bool(same)
    require(counts["pr325_entries_with_pr324_same_approved_parent"] == anchored == 34,
            "Shared-parent count drift")
    require(counts["pr325_entries_other_or_island"] == 10
            and counts["exact_id_overlap"] == 0 and counts["approved_new_site_count"] == 0,
            "Cross-PR counts or decision status cannot be trusted")
    visual = handoff["known_existing_library"]
    require(visual["pr"] == 253 and visual["manifest"] == "docs/visual/manifest.json",
            "Existing CVI authority replaced by parallel library")
    require(visual["existing_entries"] == len(lineup) == 12,
            "Existing lineup/visual bridge missing owner")
    require(handoff["status"] == "READ_ONLY_PARALLEL_HANDOFF__NO_MEDIA_INGEST__NO_PUBLICATION"
            and handoff["adapter_contract"]["media_file_copying"] is False
            and handoff["adapter_contract"]["automatic_image_authority_upgrade"] is False,
            "Atlas bridge moved media or implicitly promoted artwork")
    require(all(p["character_id"].startswith("CHAR-") and
                p["home_location_id"] in active_ids and
                len(p["crop_sha256"]) == 64 for p in lineup),
            "Canonical lineup lost original site or digest")
    return {"status": "PASS_PLANNING_ONLY", "pr325_candidate_review_rows": 44,
            "same_parent_review_cases": anchored, "unmatched_or_island_cases": 10,
            "approved_new_LOC": 0, "known_CVI_assets": len(lineup),
            "media_bytes_copied": 0, "CVI_external_bytes_verified": False}


def check_external_visual_library(visual_repo_root: Path):
    handoff = read(HERE / "PARALLEL_PHOTO_LIBRARY_HANDOFF_V1.json")
    source = read(ROOT / "canon/characters/APPROVED_LINEUP_2026_10_18.json")
    root = visual_repo_root.resolve(strict=True)
    manifest_path = (root / handoff["known_existing_library"]["manifest"]).resolve(strict=True)
    require(manifest_path.is_relative_to(root), "Unsafe manifest location")
    manifest = read(manifest_path)
    rows = manifest["assets"]
    expect = {x["character_id"]: x for x in source["individuals"]}
    require(len(rows) == len(expect) == 12 and len({r["id"] for r in rows}) == 12,
            "CVI list membership mismatched")
    verified = []
    for row in rows:
        sid = row["id"]
        original = expect.get(sid)
        require(original is not None, f"Noncanonical character asset: {sid}")
        require(row["asset_path"] == original["crop"] and
                row["expected_sha256"] == original["crop_sha256"] and
                row["location_id"] == original["home_location_id"],
                f"CVI character/LOC/crop provenance drift: {sid}")
        require(row["visibility"] == "internal" and "HOLD" in row["approval"],
                f"Unauthorized public image promotion: {sid}")
        relative = Path(row["asset_path"])
        require(not relative.is_absolute() and ".." not in relative.parts and
                "\\" not in row["asset_path"], f"Unsafe photo path: {sid}")
        path = (root / relative).resolve(strict=True)
        require(path.is_relative_to(root), f"Escaping photo path: {sid}")
        content = path.read_bytes()
        require(content.startswith(bytes.fromhex("89504e470d0a1a0a")),
                f"Image not PNG: {sid}")
        require(hashlib.sha256(content).hexdigest() == row["expected_sha256"],
                f"Image checksum drift: {sid}")
        verified.append(sid)
    return {"status": "PASS_READ_ONLY_PR253_BYTE_VERIFICATION_NOT_RENDER_RELEASE",
            "character_assets": len(verified), "verified_sha256": len(verified),
            "published_images": 0, "asset_files_copied": 0,
            "source_library_branch": handoff["known_existing_library"]["branch"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--external-visual-repo", type=Path, default=None,
                        help="Existing checked-out PR253 root (read only); never copies media.")
    args = parser.parse_args()
    print(json.dumps(local_validate(), sort_keys=True))
    if args.external_visual_repo:
        print(json.dumps(check_external_visual_library(args.external_visual_repo), sort_keys=True))
