"""Synthetic-only positive contract; no real composition approval is created."""
import hashlib
import importlib.util
from pathlib import Path
import json
import tempfile
import unittest
from PIL import Image

spec=importlib.util.spec_from_file_location('composition_consumer',Path(__file__).resolve().parents[1]/'reviewed_character_compositions.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


class CompositionConsumer(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'repo';self.root.mkdir()
        self.output=Path(self.tmp.name)/'out';self.cid='CHAR-FIXTURE'
        self.asset=self.root/'art.png';Image.new('RGB',(64,96),'navy').save(self.asset)
        self.reference=self.root/'reference.png';Image.new('RGB',(32,48),'blue').save(self.reference)
        self.sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
        self.sources={'entries':[{'character_id':self.cid,'approval_state':'APPROVED','expected_sha256':self.sha(self.reference),'repository_path':'reference.png'}]}
        self.authority={}
        # Empty dict would trigger default-loader fallback in existing resolver;
        # retain a populated fixture registry without modifying real canon.
        self.authority={'schema_version':'fixture','source_visual_conflicts':[], 'master_lineup':{'creative_claw_asset_id':'fixture-master', 'name':'master.png'}}
        self.packet={'characterId':self.cid,'scope':'PROFILE_PRESENTATION_ONLY','assetPath':'art.png',
            'assetSha256':self.sha(self.asset),'alt':'Synthetic blue fixture only',
            'reference':{'path':'reference.png','sha256':self.sha(self.reference),'sourceKind':'PRIMARY','filename':'reference.png'},
            'requestId':'fixture-request','route':'fixture-provider','mountReceiptId':'mount1',
            'generationReferenceId':'ref1','subjectBindingId':'subject1','outputInstanceId':'output1'}
        self.execution={'state':'GENERATION_EXECUTED_PENDING_CHARACTER_QA','renderer_invoked':True,'output_instance_id':'output1',
            'execution_receipt':{'request_id':'fixture-request','route':'fixture-provider',
                'mount_receipt_ids':['mount1'],'generation_reference_ids':['ref1'],'subject_binding_ids':['subject1']}}
        self.review={'reviewer':'fixture-independent','preparedBy':'fixture-creator',
            'decision':'ACCEPTED_FOR_PROFILE_PRESENTATION','scope':'PROFILE_PRESENTATION_ONLY',
            'characterId':self.cid,'outputInstanceId':'output1','assetSha256':self.packet['assetSha256'],
            'referenceSha256':self.sha(self.reference),
            'checks':{'identity':'PASS','sourceBinding':'PASS','composition':'PASS','mobileCrop':'PASS'}}

    def write(self,path,data):
        p=self.root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data))
        return self.sha(p)

    def install(self):
        self.write('canon/characters/reference_sources_v1.json',self.sources)
        self.write('canon/characters/VISUAL_REFERENCE_AUTHORITY_V1.json',self.authority)
        ph=self.write('packet.json',self.packet);eh=self.write('execution.json',self.execution)
        self.review.update(packetSha256=ph,executionReceiptSha256=eh)
        rh=self.write('review.json',self.review)
        self.entry={'packet':'packet.json','packetSha256':ph,'executionReceipt':'execution.json',
            'executionReceiptSha256':eh,'reviewReceipt':'review.json','reviewReceiptSha256':rh}
        self.write(m.REGISTRY,{'schemaVersion':1,'accepted':[self.entry]})

    def load(self):return m.load_compositions(self.root,self.output,'a'*40)

    def test_positive_uses_exact_bytes_and_profile_only_catalog(self):
        self.install();asset=self.load()['assets'][self.cid]
        self.assertEqual((self.output/'character-compositions'/asset['file']).read_bytes(),self.asset.read_bytes())
        self.assertEqual((asset['width'],asset['height']),(64,96))
        self.assertNotIn('generation_eligible',asset)

    def test_empty_registry_never_auto_discovers_images(self):
        self.write(m.REGISTRY,{'schemaVersion':1,'accepted':[]})
        self.assertEqual(self.load(),{'schemaVersion':1,'assets':{}})
        self.assertFalse(self.output.exists())

    def test_asset_tamper_rejected(self):
        self.install();self.asset.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'hash mismatch'):self.load()

    def test_reference_tamper_rejected(self):
        self.install();self.reference.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'hash mismatch'):self.load()

    def test_receipt_tamper_rejected(self):
        self.install();self.write('review.json',dict(self.review,reviewer='someone else'))
        with self.assertRaisesRegex(ValueError,'hash mismatch'):self.load()

    def test_self_review_rejected_even_when_rehashed(self):
        self.review['reviewer']=' FIXTURE-CREATOR ';self.install()
        with self.assertRaisesRegex(ValueError,'independent'):self.load()

    def test_runtime_hold_cannot_be_promoted_by_review(self):
        self.execution['state']='GENERATION_BLOCKED';self.install()
        with self.assertRaisesRegex(ValueError,'execution'):self.load()

    def test_swapped_subject_binding_rejected(self):
        self.execution['execution_receipt']['subject_binding_ids']=['other'];self.install()
        with self.assertRaisesRegex(ValueError,'execution'):self.load()

    def test_active_canon_conflict_still_blocks(self):
        self.authority['source_visual_conflicts']=[{'character_id':self.cid,'state':'ACTIVE_CANON_VISUAL_CONFLICT_HOLD',
            'affected_expected_sha256':self.sha(self.reference)}];self.install()
        with self.assertRaisesRegex(ValueError,'authority unresolved'):self.load()

    def test_derived_reference_cannot_seed_composition(self):
        self.packet['reference']['sourceKind']='DERIVED';self.install()
        with self.assertRaisesRegex(ValueError,'authority unresolved'):self.load()

    def test_unknown_character_rejected(self):
        self.packet['characterId']='CHAR-UNKNOWN';self.install()
        with self.assertRaisesRegex(ValueError,'canonical source'):self.load()

    def test_path_escape_rejected_before_output(self):
        self.packet['assetPath']='../outside.png';self.install()
        with self.assertRaisesRegex(ValueError,'escapes'):self.load()
        self.assertFalse(self.output.exists())

    def test_duplicate_character_rejected_before_any_copy(self):
        self.install();self.write(m.REGISTRY,{'schemaVersion':1,'accepted':[self.entry,self.entry]})
        with self.assertRaisesRegex(ValueError,'duplicate'):self.load()
        self.assertFalse(self.output.exists())

    def test_malformed_receipt_object_rejected(self):
        self.install();self.entry['executionReceiptSha256']=self.write('execution.json',[])
        self.write(m.REGISTRY,{'schemaVersion':1,'accepted':[self.entry]})
        with self.assertRaisesRegex(ValueError,'must be an object'):self.load()

    def test_corrupt_raster_rejected_even_when_receipts_match_hash(self):
        self.asset.write_bytes(b'not an image');self.packet['assetSha256']=self.sha(self.asset)
        self.review['assetSha256']=self.packet['assetSha256'];self.install()
        with self.assertRaises(OSError):self.load()
        self.assertFalse(self.output.exists())

    def test_missing_asset_hash_rejected(self):
        del self.packet['assetSha256'];self.install()
        with self.assertRaisesRegex(ValueError,'image hash required'):self.load()

    def test_existing_unrelated_output_is_not_overwritten(self):
        self.install()
        filename=self.cid+'-'+self.packet['assetSha256']+'.png'
        existing=self.output/'character-compositions'/filename
        existing.parent.mkdir(parents=True);existing.write_bytes(b'unrelated')
        with self.assertRaisesRegex(ValueError,'conflicts with existing bytes'):self.load()
        self.assertEqual(existing.read_bytes(),b'unrelated')

    def test_output_cannot_overwrite_source(self):
        filename=self.cid+'-'+self.packet['assetSha256']+'.png'
        source_dir=self.root/'character-compositions';source_dir.mkdir()
        source=source_dir/filename;source.write_bytes(self.asset.read_bytes())
        self.packet['assetPath']='character-compositions/'+filename;self.install()
        before=source.read_bytes()
        with self.assertRaisesRegex(ValueError,'separate from input'):
            m.load_compositions(self.root,self.root,'a'*40)
        self.assertEqual(source.read_bytes(),before)

    def test_revoked_registry_removes_previously_published_art(self):
        self.install();asset=self.load()['assets'][self.cid]
        published=self.output/'character-compositions'/asset['file']
        self.assertTrue(published.exists())
        self.write(m.REGISTRY,{'schemaVersion':1,'accepted':[]})
        self.assertEqual(self.load()['assets'],{})
        self.assertFalse(published.exists())

    def test_same_valid_build_is_idempotent(self):
        self.install();first=self.load();self.assertEqual(self.load(),first)

    def test_symlink_output_target_never_deleted(self):
        self.install();self.output.mkdir()
        (self.output/'character-compositions').symlink_to(self.root,target_is_directory=True)
        with self.assertRaisesRegex(ValueError,'alias'):self.load()
        self.assertTrue(self.asset.exists())

    def test_unknown_file_in_managed_output_blocks_cleanup(self):
        self.install();self.load()
        extra=self.output/'character-compositions'/'user.txt';extra.write_text('retain')
        self.write(m.REGISTRY,{'schemaVersion':1,'accepted':[]})
        with self.assertRaisesRegex(ValueError,'unknown files'):self.load()
        self.assertEqual(extra.read_text(),'retain')
