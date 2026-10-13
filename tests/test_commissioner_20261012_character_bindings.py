"""Current approved binary identity bindings, not proof of production image-provider execution."""
import hashlib
import json
import pathlib
import subprocess
import unittest
from canon.characters.runtime.reference_authority import request_authority_state
from canon.characters.runtime.source_byte_integrity import verify_source_bytes

ROOT=pathlib.Path(__file__).resolve().parents[1]
REG=json.loads((ROOT/'canon/characters/reference_sources_v1.json').read_text())

def candidates():
    return {e['character_id']:{
        'sha256':hashlib.sha256((ROOT/e['repository_path']).read_bytes()).hexdigest(),
        'asset_id':'repo:'+e['repository_path'],
        'source_kind':'COMMISSIONER_APPROVED_PRIMARY',
        'filename':e['source_filename'],
    } for e in REG['entries']}

class CommissionerCharacterBindings(unittest.TestCase):
    def test_all_twelve_source_bytes_and_git_objects(self):
        self.assertEqual(verify_source_bytes(ROOT,REG)['pass_count'],12)
        for e in REG['entries']:
            p=ROOT/e['repository_path']
            git=subprocess.check_output(['git','-C',str(ROOT),'hash-object',str(p)],text=True).strip()
            self.assertEqual(git,e['commissioner_upload_2026_10_12']['git_blob_sha'])
    def test_all_twelve_current_authority_bindings(self):
        cs=candidates()
        self.assertEqual(request_authority_state(list(cs),cs)['state'],'REFERENCE_AUTHORITY_RESOLVED')
    def test_cross_owner_and_tampered_bytes_fail_closed(self):
        cs=candidates()
        for cid in cs:
            altered={k:dict(v) for k,v in cs.items()}
            altered[cid]['sha256']='0'*64
            self.assertEqual(request_authority_state(list(altered),altered)['state'],'GENERATION_BLOCKED')
            other=next(k for k in cs if k!=cid)
            altered[cid]['sha256']=cs[other]['sha256']
            self.assertEqual(request_authority_state(list(altered),altered)['state'],'GENERATION_BLOCKED')
    def test_renderer_provider_not_falsely_certified(self):
        caps=json.loads((ROOT/'canon/characters/renderer_capabilities_v1.json').read_text())
        self.assertEqual(caps['status'],'NO_PRODUCTION_ROUTE_PROVEN')
if __name__=='__main__':unittest.main()
