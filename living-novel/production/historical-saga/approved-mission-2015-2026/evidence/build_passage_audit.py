"""Anchored human-read passage mapping; classifications are review findings, not acceptance."""
from pathlib import Path
import hashlib,json,collections
ROOT=Path(__file__).resolve().parents[5];OUT=Path(__file__).parent
H='living-novel/manuscript/'
R='living-novel/production/full-rewrite-2026/manuscript/'
D='living-novel/production/full-rewrite-2026/drafts/'
C1=H+'CHAPTER_01_THE_FIRST_ANSWER.md';C2=H+'CHAPTER_02_WHAT_COMES_BACK.md';C3=H+'CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM.md';C4=H+'CHAPTER_04_THE_ROAD_DOES_NOT_BOW.md'
R1=R+'CHAPTER_01_THE_FIRST_ANSWER_LINE_EDIT_V2_NONCANON.md';R2=R+'CHAPTER_02_WHAT_COMES_BACK_LINE_EDIT_V2_NONCANON.md';R3=R+'CHAPTER_03_THE_HILL_IS_NOT_THE_KINGDOM_LINE_EDIT_V2_NONCANON.md'
DOS='living-novel/production/week-04-05/WEEK_04_05_CAUSAL_STORY_ROOM_DOSSIER_2026-10-14.md'
def passage(path,heading,needle,status,kind,note):
 p=ROOT/path; lines=p.read_text().splitlines(); hs=next(i for i,l in enumerate(lines) if l==heading);he=next((i for i in range(hs+1,len(lines)) if lines[i].startswith('## ')),len(lines));i=next(i for i in range(hs,he) if needle in lines[i]);return {'path':path,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'heading':heading,'heading_line':hs+1,'anchor_line':i+1,'anchor_text':lines[i],'artifact_status':status,'classification':kind,'finding':note}
S='SUBSTANTIVE_SCENE';F='RECORD_REFERENCE';P='HYPOTHETICAL_SUMMARY';A='ABSENT_IN_AUDITED_BASELINE_NOVEL_CORPUS'
LEG='EXISTING_HARD_CANON_WITNESS_PRESERVE_BYTES_ACTIVE_POV_MIGRATION_REQUIRED';DEV='NONCANON_DEVELOPMENT_CANDIDATE_NOT_ACCEPTED';SOFT='EXISTING_SOFT_MANUSCRIPT_NOT_HARD_CANON'
m={}
def put(w,n,*args):m.setdefault((w,n),[]).append(passage(*args))
put(1,1,C1,'## VI. The Results Beneath the Results','Edrin saw Kevin',LEG,S,'Brief aftermath micro-scene: Kevin orders a repeat survey after close defeat. Exists, but limited depth and retired observer POV prevent active-reader acceptance.')
put(1,1,R1,'## I. Six Bells','MUD DOGS — 125.36.',DEV,F,'Current-owner rewrite preserves result and public argument, not a standalone Mud/Red scene.')
put(1,2,C1,'## IV. One and a Half','Seven Deadly Chins.',LEG,S,'Adjudication and allocation aftermath gives narrow loss dramatic form; retired observer POV needs migration.')
put(1,3,C1,'## VI. The Results Beneath the Results',"Wilson stood four-legged",LEG,S,'Wall-repair dialogue between Wilson and Jordan is a short aftermath scene, not merely a score; active anatomy and POV review remain necessary.')
put(1,4,R1,'## III. Proof and Possession','A boy stopped him',DEV,S,'Austin faces printed false Belt succession; substantial choice, dialogue and public consequence. Source hard Chapter I is retained.')
put(1,5,R1,'## II. The Grain Exchange','Brandon Pryor had rented',DEV,S,'Victory creates feeding, credit and repair obligations; substantive principal-POV recovery candidate.')
put(1,6,C1,'## V. Stone and Water','Three Dreaded Snake stood',LEG,S,'Existing aftermath confrontation. Retired narrator, old anatomy and storm embodiment must be reconciled; no acceptance implied.')
put(2,1,R2,'## II. The Ground He Knows','MUD DOGS — 130.84.',DEV,S,'Mud/Obi contest and aftermath in wetland geography; substantive recovery candidate.')
put(2,2,R2,'## III. Three Heads in the Mirror','D0NKEY K0NG — 165.78.',DEV,S,'Barber aftermath provides humiliation, choice and dialogue; title and three-headed anatomy conflict with current TDS canon and require repair.')
put(2,3,C2,'## V. Members Only','Jordan Hollingshead broke seven',LEG,S,'Slob/Duckhook Encounter and club repairs are dramatized, but legacy narrator needs migration.')
put(2,4,R2,'## I. Return to Sender','## I. Return to Sender',DEV,S,'Returned parcel drives Red/Chili scene; substantive owner-POV rewrite candidate.')
put(2,5,C2,'## VI. No Passage','Rain began before Austin arrived.',LEG,S,'Flooded-gate aftermath scene exists; El Niño speaking humanoid treatment expressly conflicts with current rules. Preserve source, revise separately.')
put(2,6,C2,'## VII. Hostile Takeover',"The LLC's office had survived Chili.",LEG,S,'Chins/LLC office aftermath includes dialogue and repair implications; retired observer POV requires migration.')
put(3,1,R3,'## II. The Bridge and the Word','ObiWan Jacoby, 136.73.',DEV,S,'Jake answers bridge-protection and trade pressure after TDS result; narrative choices present. Stale TDS references need repair.')
put(3,2,C3,'# CHAPTER III — THE HILL IS NOT THE KINGDOM','172.48 to 126.86.',LEG,S,'Existing hard Chapter III: Wilson places standard below summit and rejects sovereignty inference. Preserve accepted manuscript; active version requires authority/canon reconciliation.')
put(3,3,R3,'## II. The Bridge and the Word','132.19 to 126.16.',DEV,F,'Chili/Duckhook result appears in a dispatch received by Jake, with object story explicitly uncertain. No full event-focused scene found here.')
put(3,4,R3,'## II. The Bridge and the Word','158.44 to 141.86.',DEV,F,'Red/Slob result and flag/wager dispatch, not direct dramatization; provenance of wager remains separately qualified.')
put(3,5,R3,'## III. What a Keeper Cannot Keep','HIS MAJESTY\'S BLOOD — 136.00.',DEV,S,'Austin must separate victory from resource loss and road obligations. Achane dossier claim explicitly source-pending, not certified by scoring fact lock.')
put(3,6,R3,'## III. What a Keeper Cannot Keep',"147.43 to 114.62",DEV,F,'LLC/storm result interpreted in Austin scene; no independent LLC event scene in this candidate.')
put(4,1,C4,'# CHAPTER IV — THE ROAD DOES NOT BOW','D0nkey K0ng, 139.67.',SOFT,S,'Existing extended causal chapter follows certified ObiWan win; provider finality now corroborated, literary/canon acceptance still pending.')
for n in range(2,7):
 needle=['','', 'Three Dreaded Snake **149.84**','Red Leopards **164.08**','Slob on my Dobb **190.72**',"His Majesty's Blood **177.32**",'El Niño **170.62**'][n]
 put(4,n,DOS,'## 2. Event chronology — verifiable facts BEFORE interpretation',needle,'STORY_ROOM_DOSSIER_NOT_MANUSCRIPT',P,'Result and candidate significance are documented; no substantive Novel passage for this fixture found in audited manuscript corpus. Dossier is not literary coverage.')
put(5,2,R+'THE_SURVEY_LINE_FULL_CAUSAL_MANUSCRIPT_V2_NONCANON.md','## II. Terms Before Territory','193.73.',DEV,S,'Multi-scene Mud/LLC sequence dramatizes contested crossing and costs without score-to-land transfer; proposed world details remain unaccepted.')
put(5,4,D+'W5_WILSON_SECOND_FALL_OWNER_POV_NONCANON.md',"# THE SECOND FALL — Wilson's Week 5 consequence",'Dr. Duckhook, 184.91.',DEV,S,'Wilson chooses useful route markers over victory banners after second defeat; complete development interlude exists, not automatic Chapter V.')
for n,needle in [(1,"His Majesty's Blood **113.45**"),(3,'The Chili Cheesers **183.53**'),(5,'Seven Deadly Chins **170.46**'),(6,'ObiWan Jacoby **154.42**')]:
 put(5,n,DOS,'## 2. Event chronology — verifiable facts BEFORE interpretation',needle,'STORY_ROOM_DOSSIER_NOT_MANUSCRIPT',P,'Candidate dramatic pressure and result are documented; no finished event-specific Novel passage found. R41 sequence ideas likewise are plans, not scenes.')
events=json.loads((OUT/'2026_FIXTURE_COVERAGE.json').read_text())['events'];rows=[]
for e in events:
 k=(e['period'],int(e['event_id'].rsplit('E',1)[-1]));passages=m.get(k,[]);category=passages[0]['classification'] if passages else A
 rows.append({'event_id':e['event_id'],'period':e['period'],'fixture':e['side_a']+' / '+e['side_b'],'source_status':'DECIDED_REPOSITORY_RECEIPT','best_existing_literary_form':category,'passages':passages,'acceptance':'NOT_DETERMINED_BY_THIS_AUDIT','remaining_work': 'Draft event coverage in causally connected Novel scenes; Memo prose excluded.' if category in (P,A) else 'Assess sufficiency, continuity, current POV/canon compliance, scene depth and independent literary acceptance; reuse rather than discard.'})
report={'baseline_commit':'8fcb77191955f413fe970154d47632770f923055','scope':'Existing baseline Novel manuscripts, full-rewrite manuscripts/drafts, chapter04 and week04-05 sources; excludes new approved-mission drafts and all Memo prose from literary coverage. Not exhaustive proof of absence across every archived branch.','method':'Human reading of scene content, verified exact heading/line anchors; filename or score presence alone not treated as substantive scene. Aftermath scenes qualify; no requirement for separate game chapters.','counts':dict(collections.Counter(r['best_existing_literary_form'] for r in rows)),'events':rows}
(OUT/'CURRENT_SEASON_PASSAGE_AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
lines=['# Current-season passage audit','',report['scope'],'', 'All 36 fixture results have decided repository evidence through Week 6. The remaining gaps below are literary, authority or scene-level provenance gaps, not missing match results. Current source freshness beyond Week 6 remains separate.','', 'Counts describe existing form, never acceptance: '+str(report['counts']), '', '| Week | Fixture | Best existing form | Passage / finding |','|---|---|---|---|']
for r in rows:
 p=r['passages'][0] if r['passages'] else None
 lines.append(f"| {r['period']} | {r['fixture']} | {r['best_existing_literary_form']} | "+(f"`{p['path']}:{p['anchor_line']}` — {p['heading']}. {p['finding']}" if p else 'No baseline Novel passage found; all six W6 results remain drafting gaps in this audited corpus.')+' |')
lines+=['','## Resume priorities','','1. Recover legacy W1–W2 scenes without reviving Edrin/Oren POV or El Niño speech/interiority; repair TDS anatomy in existing rewrite candidates. Preserve hard manuscript bytes and lineage.','2. Review W3 dispatch coverage for meaningful causal integration; do not call brief result references fully developed character sequences. Reuse Wilson/Jake/Austin scenes, resolving stale anatomy and separately pending resource evidence.','3. Reuse soft Chapter IV for ObiWan/D0nkey and Survey Line plus Second Fall for W5. W4’s other five and W5’s other four fixtures have planning/reference material, not demonstrated substantive Novel scenes in this audit.','4. Draft W6 coverage from the six final receipts, using current temporal state; do not import Memo story treatment as accepted Novel canon.','5. Integrate newly produced mission prose in a later audit. This baseline report intentionally excludes concurrent work, so it will not invalidate new scenes by calling them absent.','','The original accepted files remain protected. This audit does not certify their active-reader compliance, accept drafts, assign world mutations, or grant canonical promotion.']
(OUT/'CURRENT_SEASON_PASSAGE_AUDIT.md').write_text('\n'.join(lines)+'\n')
print(report['counts'])
