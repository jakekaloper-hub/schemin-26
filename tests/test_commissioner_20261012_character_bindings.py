"""October12 bytes are historical evidence, never automatic active-source promotion."""
import hashlib
import json
from pathlib import Path
import unittest
from canon.characters.runtime.reference_authority import request_authority_state
from canon.characters.cccp_resolver import resolve_character

ROOT=Path(__file__).resolve().parents[1]
HISTORY=json.loads((ROOT/"canon/characters/COMMISSIONER_VISUAL_REFERENCE_2026_10_12.json").read_text())

def candidates():
    result={}
    for entry in HISTORY["entries"]:
        cid=resolve_character(entry["team"])["character_id"]
        paths=list((ROOT/"canon/characters/assets"/cid/"primary").glob("COMMISSIONER_2026-10-12.*"))
        if len(paths)!=1:
            raise AssertionError(f"Expected one preserved historical source for {cid}")
        path=paths[0]
        result[cid]={"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
            "asset_id":"repo:"+str(path.relative_to(ROOT)),"source_kind":"HISTORICAL_CANDIDATE",
            "filename":path.name}
    return result

class CommissionerCharacterBindings(unittest.TestCase):
    def test_all_twelve_historical_bytes_match_original_receipts(self):
        cs=candidates()
        self.assertEqual(len(cs),12)
        for entry in HISTORY["entries"]:
            self.assertEqual(cs[resolve_character(entry["team"])["character_id"]]["sha256"],entry["sha256"])
    def test_historical_set_cannot_replace_current_approved_sources(self):
        cs=candidates()
        self.assertEqual(request_authority_state(list(cs),cs)["state"],"GENERATION_BLOCKED")
        self.assertEqual(HISTORY["status"],"HISTORICAL_REFERENCE_ONLY_NOT_ACTIVE_AUTHORITY")
        self.assertFalse(HISTORY["active_source_supersession"])
    def test_cross_owner_and_tampered_bytes_fail_closed(self):
        cs=candidates()
        for cid in cs:
            altered={k:dict(v) for k,v in cs.items()}
            altered[cid]["sha256"]="0"*64
            self.assertEqual(request_authority_state(list(altered),altered)["state"],"GENERATION_BLOCKED")
            other=next(k for k in cs if k!=cid)
            altered[cid]["sha256"]=cs[other]["sha256"]
            self.assertEqual(request_authority_state([cid],{cid:altered[cid]})["state"],"GENERATION_BLOCKED")
    def test_renderer_provider_not_falsely_certified(self):
        caps=json.loads((ROOT/"canon/characters/renderer_capabilities_v1.json").read_text())
        self.assertEqual(caps["status"],"NO_PRODUCTION_ROUTE_PROVEN")
if __name__=="__main__":unittest.main()
