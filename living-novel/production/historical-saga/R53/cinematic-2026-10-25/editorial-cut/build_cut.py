from pathlib import Path
import hashlib,json,re
stage=Path(__file__).resolve().parent;base=stage.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
source=base/'principal-convergence/SAGA_READING_ASSEMBLY.md'
source_hash=sha(source.read_bytes())
text='''# What remains between us — a three-part cinematic treatment

PROPOSED / NONCANON editorial cut. Primary format recommendation: a three-part limited-series development treatment. This is a reading treatment, not a commissioned series, finished screenplay or measured runtime. Dates orient selected history; action, dialogue and civilian institutions remain proposed adaptations. No historical owner gap, future result, held interior voice or formal creative approval is supplied by this cut.

'''
records=[];units=[]
for roman in ['I','II','III']:
 f=stage/('PART_I_WHAT_COMES_BACK.md' if roman=='I' else f'PART_{roman}.md');s=f.read_text()
 match=re.search(r'^## Cut\s*\n(.*?)(?=^## |\Z)',s,re.M|re.S)
 assert match,f
 body=match.group(1).strip()
 title=s.splitlines()[0].removeprefix('# ')
 text+=f'## {title}\n\n{body}\n\n'
 records.append({'file':f.name,'file_sha256':sha(f.read_bytes()),'heading':title,'cut_body_sha256':sha(body.encode()),'body_words':len(body.split())})
 mapping=json.loads((stage/f'PART_{roman}_SOURCE_MAP.json').read_text())
 assert mapping['source_sha256']==source_hash
 for item in mapping['units']:
  units.append(dict(item,part=roman))
assert sorted(u['source_unit'] for u in units)==list(range(1,51))
text=text.rstrip()+'\n'
(stage/'EDITORIAL_CUT.md').write_text(text)
(stage/'CUT_MANIFEST.json').write_text(json.dumps({'status':'PROPOSED_NONCANON','source_assembly_sha256':source_hash,'cut_sha256':sha(text.encode()),'parts':records,'units':units},indent=2)+'\n')
heads=re.findall(r'^## \d+\. (.+)$',source.read_text(),re.M)
table='# Source and omission map — editorial cut\n\nEvery source unit is accounted for. Compression is editorial prose, not byte-equivalent reuse; source fidelity requires the independent review. Omission means not shown here, not canceled in history. Exact part files and reader hashes are in CUT_MANIFEST.json.\n\n| Source unit | Source title | Part | Disposition | New beat | Reason / boundary |\n|---|---|---|---|---|---|\n'
for u in sorted(units,key=lambda x:x['source_unit']):
 n=u['source_unit'];values=[str(n),heads[n-1],u['part'],u['status'],u.get('new_beat_anchor') or '—',u['reason']]
 values=[v.replace('See prose source/omission table','See [Part III source/omission table](PART_III.md#source-compression-and-omission-map)').replace('see prose source/omission table', 'see [Part III source/omission table](PART_III.md#source-compression-and-omission-map)').replace('See prose source/omission table.','See [Part III source/omission table](PART_III.md#source-compression-and-omission-map).') for v in values]
 table+='| '+' | '.join(v.replace('|','/') for v in values)+' |\n'
(stage/'SOURCE_OMISSION_MAP.md').write_text(table)
print(json.dumps({'words':len(text.split()),'body_words':sum(x['body_words'] for x in records),'sha256':sha(text.encode()),'parts':[{k:x[k] for k in ['file','body_words']} for x in records]},indent=2))
