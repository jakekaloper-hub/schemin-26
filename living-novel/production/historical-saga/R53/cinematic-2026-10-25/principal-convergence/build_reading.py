from pathlib import Path
import re,json,hashlib
base=Path(__file__).resolve().parent.parent
out=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def section(file,heading):
 text=(base/file).read_text(); matches=list(re.finditer(r'^## (.+)$',text,re.M))
 ix=next(i for i,m in enumerate(matches) if m.group(1)==heading)
 return text[matches[ix].end():matches[ix+1].start() if ix+1<len(matches) else len(text)].strip()
def ref(file,heading,start=None,end=None):
 full=section(file,heading);text=full
 if start:text=text[text.index(start):]
 if end:text=text[:text.index(end)]
 return {'file':file,'heading':heading,'start':start,'end':end,'file_sha256':sha((base/file).read_bytes()),'section_sha256':sha(full.encode()),'fragment_sha256':sha(text.strip().encode())},text.strip()
oldfile='era-completion/SAGA_READING_ASSEMBLY.md'
oldtitles=re.findall(r'^## (.+)$',(base/oldfile).read_text(),re.M)
mapfile='principal-convergence/MAP_ORIGIN_SEQUENCES.md';kp='principal-convergence/KEVIN_PHILLIP_SEQUENCES.md';ja='principal-convergence/JORDAN_AUSTIN_SEQUENCES.md'
records=[]; bodies=[]
def add(title,refs,edits=[]):
 provenance=[];chunks=[]
 for args in refs:
  r,b=ref(*args);provenance.append(r);chunks.append(b)
 body='\n\n'.join(chunks)
 edits=list(edits)
 if 'END OF SEQUENCE.' in body:edits.append({'old':'END OF SEQUENCE.','new':'','reason':'Remove inherited module ending inside continuousreading.'})
 for edit in edits:
  assert edit['old'] in body, (title,edit['old'][:40])
  body=body.replace(edit['old'],edit['new'])
 body=re.sub(r'\n{3,}','\n\n',body).strip()
 records.append({'unit':len(records)+1,'title':title,'fragments':provenance,'edits':edits,'body_sha256':sha(body.encode())});bodies.append(body)
def new(file,title):
 edits=[]
 if title=='Sequence 2 — The brace':
  edits=[{'old':'Phillip holds a rail against his armored torso.','new':'Phillip, called Pitts in the earlier contest, holds a rail against his armored torso: one reptilian humanoid body with exactly three serpent heads.','reason':'Move existing alias and approved2026 body orientation to first2026 appearance, without backdating morphology.'}]
 if title=='Sequence 4 — The hand at the edge':
  edits += [{'old':'Today. Tomorrow is what I’m offering.','new':'Tomorrow is what I’m offering.','reason':'Remove unneeded inferred customer-day specificity.'}] if 'Today. Tomorrow is what I’m offering.' in section(file,title) else [{'old':"Today. Tomorrow is what I'm offering.",'new':"Tomorrow is what I'm offering.",'reason':'Remove unneeded inferred customer-day specificity.'}]
  edits.append({'old':'I wanted people to stop being surprised I could stand beside you.','new':'I wanted people to stop being surprised to see me standing.','reason':'Retain source corporeal self-representation rather than narrow it to status beside Austin.'})
 add(title.split(' — ',1)[-1],[(file,title)],edits)
for n,t in enumerate(oldtitles,1):
 title=re.sub(r'^\d+\. ','',t)
 if n==6:
  a='INT. THE ROOM — LATER THAT YEAR';z='FINAL LOWER-LADDER WINDOW';m='Sequence 1 — At the crossing';split='LATER IN2018'
  add('The keeper and the shared map — 2018',[(oldfile,t,None,a),(mapfile,m,None,split),(oldfile,t,a,z),(mapfile,m,split,None),(oldfile,t,z,None)])
 else:
  edits=[]
  if n==7:
   summary="Jake altered the printer’s block without permission. His reversed arrow required an insert repair, delaying the assistant’s separately paid oil-label order. Three distributed originals remain unrecovered after a defective sheet circulated; the six corrected sheets cannot recall them."
   edits=[{'old':summary,'new':'','reason':'Origins now staged immediately before this settlement; remove recap while retaining counts in scenes and source evidence.'}]
  add(title,[(oldfile,t)],edits)
 if n==6:
  for title2 in ['Sequence 2 — Twenty explanations','Sequence 3 — The road without him','Sequence 4 — The block he touched']:new(mapfile,title2)
 if n==25:
  new(kp,'Sequence 1 — Before the meal');new(ja,'Sequence A — The meal before the account')
 if n==28:
  new(kp,'Sequence 2 — The brace');new(ja,'Sequence B — Breakfast for fewer people')
 if n==30:new(kp,'Sequence 3 — Start with the crossed-out one')
 if n==35:
  new(kp,'Sequence 4 — The hand at the edge');new(ja,'Sequence C — The stores he kept')
text='''# What remains between us — principal convergence reading

NONCANON proposed cinematic adaptation. This continuous revision preserves the prior reading as a separate artifact and integrates source-grounded origins and principal choices into its chronology. New civilian incidents are adapted literary proposals, not verified historical events. Unknown owners and period venues remain unknown. No Manning interior/speech, original screenplay change, canon promotion or future result is supplied. Three movements retain their cards; within-period cuts imply neither simultaneous clock time nor measured travel. This is a selected development reading, not a finished screenplay, runtime or production claim.
'''
for r,b in zip(records,bodies):text+=f"\n## {r['unit']}. {r['title']}\n\n{b}\n"
(out/'SAGA_READING_ASSEMBLY.md').write_text(text)
(out/'SAGA_READING_SOURCE_MAP.json').write_text(json.dumps({'status':'NONCANON','assembly_sha256':sha(text.encode()),'normalization':'Join fragments with two newlines; apply each replacement to all occurrences; collapse 3+ newlines to two; strip body boundaries.','units':records},indent=2)+'\n')
print(len(records),len(text.split()),sha(text.encode()))
