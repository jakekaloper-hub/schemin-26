from pathlib import Path
import re,json,hashlib
stage=Path(__file__).resolve().parent;base=stage.parent;root=base.parents[4]
sha=lambda b:hashlib.sha256(b).hexdigest()
for item in json.loads((base/'SOURCE_HASHES.json').read_text())['files']:
 assert sha((root/item['path']).read_bytes())==item['sha256'],item['path']
m=json.loads((stage/'SAGA_READING_SOURCE_MAP.json').read_text());a=(stage/'SAGA_READING_ASSEMBLY.md').read_text()
assert sha(a.encode())==m['assembly_sha256']
heads=list(re.finditer(r'^## (.+)$',a,re.M));assert len(heads)==len(m['units'])
for i,(h,u) in enumerate(zip(heads,m['units'])):
 assert u['unit']==i+1 and h.group(1)==f"{i+1}. {u['title']}"
 parts=[]
 for r in u['fragments']:
  file=(base/r['file']).read_bytes();assert sha(file)==r['file_sha256']
  s=file.decode();hs=list(re.finditer(r'^## (.+)$',s,re.M));j=next(j for j,x in enumerate(hs) if x.group(1)==r['heading'])
  b=s[hs[j].end():hs[j+1].start() if j+1<len(hs) else len(s)].strip();assert sha(b.encode())==r['section_sha256']
  if r['start']:b=b[b.index(r['start']):]
  if r['end']:b=b[:b.index(r['end'])]
  b=b.strip();assert sha(b.encode())==r['fragment_sha256'];parts.append(b)
 b='\n\n'.join(parts)
 for e in u['edits']:
  assert e['old'] in b
  b=b.replace(e['old'],e['new'])
 b=re.sub(r'\n{3,}','\n\n',b).strip()
 actual=a[h.end():heads[i+1].start() if i+1<len(heads) else len(a)].strip()
 assert b==actual and sha(b.encode())==u['body_sha256'],u['title']
print(json.dumps({'status':'PASS','retained_sources':16,'units':len(heads),'assembly_sha256':m['assembly_sha256'],'scope':'Source-byte retention and exact editorial replay, not artistic/authority acceptance.'},indent=2))
