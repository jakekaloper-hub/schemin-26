#!/usr/bin/env python3
"""Fail-closed Week 6 cinematic environment candidate validator.

This does NOT claim visual likeness, physics simulation, or final human approval.
"""
from pathlib import Path
import json, hashlib, sys
ROOT=Path(__file__).resolve().parents[2]
CAND=ROOT/"memo-os/week-6/WEEK_6_CINEMATIC_CANDIDATE_REVIEW_V1.json"
REF=ROOT/"world/location-control-plane/registries/LOCATION_REFERENCE_REGISTRY.json"
LOC=ROOT/"world/data/locations.json"
def main():
    cand=json.loads(CAND.read_text())
    refs={r["location_id"]:r for r in json.loads(REF.read_text())["locations"]}
    locs={r["id"]:r for r in json.loads(LOC.read_text())["locations"]}
    assert cand["commissioner_review"]=="DEVELOP_SIX_NOT_FINAL_APPROVE"
    assert cand["cinematic_approval"]=="NONE"
    assert len(cand["locations"])==6
    ids=set()
    for c in cand["locations"]:
        lid=c["location_id"]
        assert lid not in ids
        ids.add(lid)
        assert lid in refs and lid in locs
        assert c["status"]=="CANDIDATE_REVIEW_NOT_APPROVED"
        assert c["zone"]==locs[lid]["physical_zone_id"]
        assert c["structural_reference"] in refs[lid]["approved_structural_reference_uris"]
        plate=ROOT/c["structural_reference"]
        data=plate.read_bytes()
        assert b"NOT CINEMATIC ART" in data and lid.encode() in data
        assert refs[lid]["structural_reference_status"]=="APPROVED_STRUCTURAL_REFERENCE"
        assert refs[lid]["cinematic_reference_status"]=="MISSING_APPROVED_CINEMATIC_REFERENCE"
        assert not refs[lid]["approved_cinematic_reference_uris"]
        assert c["proposed_asset_status"]=="NOT_REGISTERED_NO_APPROVED_CINEMATIC_BYTES"
        assert c["rejected_drift"] and c["cinematic_direction"]
        print(f"{lid} STRUCTURAL_PRESENT SHA256={hashlib.sha256(data).hexdigest()} CINEMATIC_HOLD")
    print("PASS 6/6 metadata, LOC binding, source SVG byte hashes and fail-closed reference states")
    print("NOT TESTED final cinematic asset bytes, scene physics, character raster identity or human approvals")
if __name__=="__main__":
    main()
