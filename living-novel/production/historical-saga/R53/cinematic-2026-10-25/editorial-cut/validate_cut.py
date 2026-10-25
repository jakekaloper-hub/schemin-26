from pathlib import Path
import json,re,hashlib
stage=Path(__file__).resolve().parent;base=stage.parent;root=base.parents[4]
sha=lambda b:hashlib.sha256(b).hexdigest()
for item in json.loads((base/'SOURCE_HASHES.json').read_text())['files']:
 assert sha((root/item['path']).read_bytes())==item['sha256'],item['path']
m=json.loads((stage/'CUT_MANIFEST.json').read_text())
assert sha((base/'principal-convergence/SAGA_READING_ASSEMBLY.md').read_bytes())==m['source_assembly_sha256']
cut=(stage/'EDITORIAL_CUT.md').read_text();assert sha(cut.encode())==m['cut_sha256']
heads=list(re.finditer(r'^## (.+)$',cut,re.M));assert len(heads)==len(m['parts'])==3
words=0
for i,p in enumerate(m['parts']):
 raw=(stage/p['file']).read_bytes();assert sha(raw)==p['file_sha256']
 body=re.search(r'^## Cut\s*\n(.*?)(?=^## |\Z)',raw.decode(),re.M|re.S).group(1).strip()
 actual=cut[heads[i].end():heads[i+1].start() if i+1<len(heads) else len(cut)].strip()
 assert body==actual and sha(body.encode())==p['cut_body_sha256']
 assert heads[i].group(1)==p['heading'] and len(body.split())==p['body_words']
 words+=p['body_words']
ids=[x['source_unit'] for x in m['units']];assert sorted(ids)==list(range(1,51))
assert all(x['status'] in ['compressed','omitted','retained'] and x['reason'] for x in m['units'])
omitted=[x['source_unit'] for x in m['units'] if x['status']=='omitted'];assert omitted==[5,27,29,31,34,35,44,49]
for x in m['units']:
 if x['status']!='omitted':
  part=next(p for p in m['parts'] if p['file'].startswith('PART_'+x['part']+('_' if x['part']=='I' else '.')))
  body=(stage/part['file']).read_text()
  assert x['new_beat_anchor'].lower() in body.lower(),x
print(json.dumps({'status':'PASS','unchanged_authority_sources':16,'source_units_accounted':50,'compressed':42,'omitted':8,'parts':3,'body_words':words,'total_words':len(cut.split()),'cut_sha256':m['cut_sha256'],'scope':'Hash/body/map validation only; prose compression is independently reviewed, not byte-equivalent to source.'},indent=2))
