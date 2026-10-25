from pathlib import Path
import re, hashlib,json
p=Path(__file__).resolve().parent.parent; out=p/'era-completion'
def sections(f, predicate):
 s=(p/f).read_text(); ms=list(re.finditer(r'^## (.+)$',s,re.M)); result=[]
 for i,m in enumerate(ms):
  if predicate(m.group(1)):
   body=s[m.end():ms[i+1].start() if i+1<len(ms) else len(s)].strip()
   result.append((f,m.group(1),body))
 return result
parts=sections('era-completion/EARLY_ERA_SEQUENCE_CHAIN.md',lambda x:x.startswith('Sequence '))
e=sections('ensemble-expansion/ENSEMBLE_READING_ASSEMBLY.md',lambda x:True)
parts+=e[:2]
parts+=sections('era-completion/MIDDLE_ERA_SEQUENCE_CHAIN.md',lambda x:x.startswith('Sequence '))
parts+=sections('feature-development/FEATURE_READING_ASSEMBLY.md',lambda x:True)
parts+=e[2:13]
parts+=sections('reading-unit/THE_PART_YOU_OFFER.md',lambda x:x.startswith('II. The chair'))
parts+=e[13:]
text='# What remains between us — chronological saga development reading\n\nNONCANON / proposed cinematic adaptation. Selected scenes span 2015–2025 and the verified 2026 sixth-contest boundary. This reading combines existing accepted development with newly reviewed selections; it is not a completed screenplay, a runtime claim or canon approval. Original manuscripts and DogTable screenplay remain unchanged. Unnamed historical owners remain unknown. Literary continuity is not independent historical verification.\n\nThree movements: obligations and records (2015–20); company and control (2021–25); distributed agency (2026). Numbered units aid review, not one film or chapter per year. Exact provenance and review scope accompany this reader. Within-year cuts imply neither measured travel time nor precise simultaneity. The new dialogue, compression and blocking remain proposals.\n'
records=[]
for i,(f,t,b) in enumerate(parts,1):
 original=b; edits=[]
 def change(old,new,reason):
  global b
  assert old in b, (t,old[:60])
  b=b.replace(old,new)
  edits.append({'old':old,'new':new,'reason':reason})
 for line in original.splitlines():
  if re.match(r'^(END (SEQUENCE|OF MODULE|OF MOVEMENT)|CUT TO BLACK\.|\*Exit consequence:|\*\*Adaptation boundary:|\*\*Companion splice:)',line):
   change(line,'','Move editorial boundary commentary to provenance map; preserve original module.')
 if 'What stays behind' in t:
  change('WILSON stands beside the bench.', 'WILSON, one integrated gorilla-centaur with four legs, stands beside the bench.', 'Current approved morphology; no historical backdating.')
  change('MARA','TIMBER CARRIER','Functional cue avoids asserting identity with early-era Mara; M26 also names this carrier Mara, identity unestablished.')
  change('Mara','the timber carrier','Same identity boundary; no claim these are different people.')
 if 'The edge' in t:
  change('Zach stands beyond their shade.', 'Zach, called Duckhook in the earlier contest, stands beyond their shade.', 'CHAR-ZACH-WILSON registry and existing2025 source alias.')
 if 'A route given away' in t:
  change("Bobby has Jake's boot in his mouth.", "Bobby, a four-legged speaking principal, has Jake's boot in his mouth.", 'Positive source-visible orientation without guessing species.')
 if 'A door made narrow' in t:
  change('An awning rises.', '*Scene contract: M34 attributes these effects to El Niño. His interior and speech are not staged; ordinary rain elsewhere is not automatically his action.*\n\nAn awning rises.', 'Bounded source attribution, no weather-only body redefinition.')
 if 'The sample' in t:
  change('PHILLIP enters:', 'PHILLIP, previously called Pitts, enters:', 'CHAR-PHILLIP-PITTS registry; anatomy applies to this2026scene only.')
 if 'What the visit buys' in t:
  old='CUT: after Jake cancels a visit. Used bowls and no clean water. The assistant can fetch water quickly, but Jake adds a bowl, the chest, the tablecloth.\n\n“You cancelled her?”\n\n“I did not need the whole visit.”\n\n“You need the pieces of it.”\n\nJake asks for water alone.'
  new='CUT: after Jake cancels a visit. Used bowls and no clean water. He asks the assistant for water alone.'
  change(old,new,'Compress another corrective exchange; retain canceled visit and lost scheduling consequence.')
 if 'Something worth playing' in t:
  for opening,ending in [('CUT: buttons on Jake',"the other man's humming."),('On a later visit the woman proposes exchanging sides midway','not a cue for her to teach him a lesson.')]:
   start=b.index(opening);end=b.index(ending,start)+len(ending)
   change(b[start:end],'','Remove repeated failed-control demonstration; preserve real play, earned wins, driver time boundary and nuts payoff.')
 if i in (1,9,24):
  label={1:'MOVEMENT I — WHAT A ROOM CAN KEEP / 2015–20',9:'MOVEMENT II — WHAT COMPANY PERMITS / 2021–25',24:'MOVEMENT III — WHAT REMAINS IN USE / 2026'}[i]
  first=b.splitlines()[0]
  change(first, '**'+label+'**\n\n'+first, 'Orient larger chronological movement, not one-film-per-year packaging.')
 b=re.sub(r'\n{3,}','\n\n',b).strip()

 title=re.sub(r'^(Sequence \d+ — |\d+\. |II\. )','',t)
 text+=f'\n## {i}. {title}\n\n{b}\n'
 records.append({'unit':i,'title':title,'source':f,'source_heading':t,'source_sha256':hashlib.sha256((p/f).read_bytes()).hexdigest(),'body_sha256':hashlib.sha256(b.encode()).hexdigest(),'original_body_sha256':hashlib.sha256(original.encode()).hexdigest(),'edits':edits})
(out/'SAGA_READING_ASSEMBLY.md').write_text(text)
(out/'SAGA_READING_SOURCE_MAP.json').write_text(json.dumps({'status':'NONCANON','assembly_sha256':hashlib.sha256(text.encode()).hexdigest(),'units':records},indent=2)+'\n')
print(len(parts),len(text.split()),hashlib.sha256(text.encode()).hexdigest())
