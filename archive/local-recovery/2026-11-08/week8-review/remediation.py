import json,pathlib,hashlib,collections
root=pathlib.Path.home()/'Developer/ai/schemin-visual-local'
repo=root/'repo';out=root/'week8-review'
p=json.loads((out/'week8_packets.json').read_text())
state=json.loads((repo/'world/data/current_world_state.json').read_text())
ledger=json.loads((repo/'world/evolution/WORLD_EVOLUTION_LEDGER.json').read_text())
routes=json.loads((repo/'world/data/routes.json').read_text())['routes']
loc={x['id']:x for x in json.loads((repo/'world/data/locations.json').read_text())['locations']}
assert len(p['packets'])==28
assert len(ledger['transactions'])==0
report={'week8_production_readiness':'PREVIS_ONLY','world_state':{'as_of':state['as_of'],'applied_transactions':len(ledger['transactions']),'decision':'BLOCK_WORLD_STATE_PROMOTION'},'gotw':{'venue':'LOC-TDS-CHILI-SHARED-MARCH','registered':True,'neutral_approval':'NOT_VERIFIED','decision':'PROPOSE_ADMISSION_NOT_APPROVED'},'reference_transport':{'crop_hashes_pass':sum(x['hash_verified'] for x in p['references'].values()),'renderer_attachment_receipt':'NOT_VERIFIED','decision':'NO_CHARACTER_GENERATION_AUTHORIZATION'},'visual_proof':{'type':'REFERENCE_BACKED_WIREFRAME','rendered_character_art':False,'full_artifact_qa':'NOT_PERFORMED'},'next_actions':['obtain signed venue exception or neutral pool admission','reconstruct weeks 4-7 from verified events through world evolution engine','mount reference images with renderer subject-binding receipts','independent Fact Lock and final ESPN outcomes','render first actual POV plate and inspect phone-scale raster']}
(out/'remediation_receipt.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
