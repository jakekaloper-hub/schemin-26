import json,pathlib,re,html,hashlib
repo=pathlib.Path.home()/'Developer/ai/schemin-visual-local/repo'
out=pathlib.Path.home()/'Developer/ai/schemin-visual-local/week8-review'
domains=json.loads((repo/'world/data/owner_domains.json').read_text())['domains']
locs={x['id']:x for x in json.loads((repo/'world/data/locations.json').read_text())['locations']}
by={x['team_id']:x for x in domains}
specs=[
('The Place We Once Knew',6,7,'LOC-TDS-CHILI-SHARED-MARCH',['Two familiar arrivals','The shared settlement','Memory / present match cut','The first strike','Paths become traps','The final meeting']),
('Hostile Ground',2,4,'LOC-RED-RUINS',['Predator / intruder overture','Coastal infiltration','Reversal in the ruins','Exposed-height confrontation']),
("The Storm That Wouldn't Leave",1,9,'LOC-TRADE-JEDI-MOUNTAIN-BASE',['Order / storm overture','First failed defense','The mountain siege','Escalating setbacks','The final passage']),
('The Last Light',10,12,'LOC-MUD-DOGS-SWAMP',['Hunter / hunted overture','The disturbed trail','The narrowing channel','Last-light confrontation']),
('The Fallen Giant',5,11,'LOC-DK-HIGHLAND-STRONGHOLD',['Challenger / giant overture','Highland battlefield','First collision','Momentum reversal','Final stand']),
('The Weight of a Crown',3,8,'LOC-SLOB-FOOTHILL-CAMP',['Champion / contender overture','The challenge','Ceremonial confidence breaks','The reckoning'])]
refs={}
for d in domains:
 t=(repo/'canon/characters'/d['character_id']/'REFERENCE_MANIFEST.yaml').read_text()
 p=re.search(r'owner_crop_path:\s*"?([^"\n]+)',t)
 h=re.search(r'owner_crop_sha256:\s*"?([0-9a-f]{64})',t)
 path=repo/p.group(1).strip() if p else None
 digest=hashlib.sha256(path.read_bytes()).hexdigest() if path and path.exists() else None
 refs[d['team_id']]={'character_id':d['character_id'],'manifest':str(repo/'canon/characters'/d['character_id']/'REFERENCE_MANIFEST.yaml'),'crop':str(path) if path else None,'exists':bool(path and path.exists()),'hash_verified':bool(h and digest==h.group(1)),'render_mount_proven':False}
packets=[]
for title,home,away,loc,beats in specs:
 for n,beat in enumerate(beats,1):
  packets.append({'packet_id':f'W08-{home:02d}-{n:02d}','story':title,'home_team_id':home,'away_team_id':away,'location_id':loc,'location_canon_status':locs[loc]['canon_status'],'shot':beat,'canvas':[1080,1920],'layout':('two equal 1080x960 POV panels' if n==1 else 'flexible full bleed or sequential panels'),'copy_safe_zone':'keep editorial text within x=90..990, y=140..1760; final placement requires proof','reference_ids':[by[home]['character_id'],by[away]['character_id']],'result_branch':'NONE until ESPN winner decided' if n<len(beats) else 'A home wins / B away wins; both provisional','qa':'NOT RUN'})
data={'status':'PROVISIONAL','world_state_as_of':'end_of_week_3_2026','note':'Week 4-7 state reconciliation required. Registered connectivity does not prove travel timing. GOTW neutral venue approval pending.','references':refs,'packets':packets,'issue_sections':['Cover / midseason overture','Division races and seven playoff berths','Week 7 consequences','GOTW six beats','Five other matchup sequences','Pittsys Book (verified only)','Results / power movement','Week 9 closing']}
(out/'week8_packets.json').write_text(json.dumps(data,indent=2))
css='body{background:#11151c;color:#f0e9db;font:16px system-ui;margin:24px}h1{color:#f5d79d}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.card{background:#222b37;padding:16px;border:1px solid #657181;border-radius:10px;min-height:220px}.tag{color:#d2b37b;font-size:12px}img{height:145px;max-width:48%;object-fit:contain}small{color:#bfc7d1} @media(max-width:800px){.grid{grid-template-columns:1fr}}'
cards=[]
for p in packets:
 names=[by[p['home_team_id']]['team'],by[p['away_team_id']]['team']]
 imgs=''.join('<img src="file://'+refs[k]['crop']+'">' for k in (p['home_team_id'],p['away_team_id'])) if p['shot'].lower().find('overture')>=0 or p['shot'].lower().find('arrivals')>=0 else ''
 cards.append(f'<article class="card"><div class="tag">{p["packet_id"]} · {html.escape(p["location_id"])} · {p["location_canon_status"]}</div><h3>{html.escape(p["shot"])}</h3><p>{html.escape(p["story"])}</p>{imgs}<p><small>{html.escape(" / ".join(names))} · {p["layout"]}</small></p></article>')
page='<!doctype html><meta charset="utf-8"><title>Schemin Week 8 Previs</title><style>'+css+'</style><h1>SCHEMIN 26 · WEEK 8 STORYBOARD CONTACT SHEET</h1><p>PROVISIONAL · 28 compositions · 1080 × 1920 masters · NOT FINAL ART · NOT APPROVED</p><div class="grid">'+''.join(cards)+'</div>'
(out/'contact_sheet.html').write_text(page)
print(json.dumps({'packets':len(packets),'verified_crops':sum(x['hash_verified'] for x in refs.values()),'files':[str(out/'week8_packets.json'),str(out/'contact_sheet.html')]}))
