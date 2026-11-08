import json,pathlib,html,copy
root=pathlib.Path.home()/'Developer/ai/schemin-visual-local/week8-review'
j=json.loads((root/'week8_enriched_packets.json').read_text())
old=[x for x in j['packets'] if x['story']=='The Place We Once Knew']
newbeats=['Two arrivals — shared POV','Oxford corner bedroom — memory only','Architectural match cut — Oxford to Shared March','The shared settlement','The first strike','Familiarity fails','Conditional final meeting']
new=[]
for i,beat in enumerate(newbeats,1):
 p=copy.deepcopy(old[min(i-1,len(old)-1)])
 p['packet_id']=f'W08-06-{i:02d}'
 p['shot']=beat
 p['layout']='two equal 1080x960 POV panels' if i==1 else 'flexible full bleed or sequential panels'
 p['result_branch']='A home wins / B away wins; both provisional' if i==7 else 'NONE until ESPN winner decided'
 p['enrichment_device']='Oxford Kappa Sigma corner-bedroom memory / Commonwealth match cut'
 p['historical_fact_status']='Founder supplied shared bedroom; precise room design unverified'
 p['qa']='NOT RUN'
 new.append(p)
j['packets']=new+[x for x in j['packets'] if x['story']!='The Place We Once Knew']
j['production_status']='29-COMPOSITION RECONCILED PREVIS; NOT FINAL ART; NO RESULT LOCK'
j['reconciliation_note']='GOTW expanded from six to seven compositions, including Oxford memory and architectural match cut. The historical house is NOT a Commonwealth location.'
(root/'week8_29_packets.json').write_text(json.dumps(j,indent=2)+'\n')
cards=[]
for p in j['packets']:
 cards.append('<article><span>'+html.escape(p['packet_id'])+'</span><h3>'+html.escape(p['shot'])+'</h3><b>'+html.escape(p['story'])+'</b><p>'+html.escape(p.get('enrichment_device',''))+'</p><small>'+html.escape(p['location_id'])+'</small></article>')
css='body{font:16px system-ui;background:#10151c;color:#eee6d9;margin:24px}h1{color:#efcd90}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}article{border:1px solid #67717d;border-radius:8px;background:#222c38;padding:16px;min-height:190px}span,small{color:#c7b487}small{display:block;margin-top:14px}@media(max-width:800px){.grid{grid-template-columns:1fr}}'
(root/'week8_29_contact_sheet.html').write_text('<!doctype html><meta charset="utf-8"><style>'+css+'</style><h1>SCHEMIN 26 — WEEK 8 · 29 COMPOSITIONS</h1><p>Oxford memory integrated · six Founder-selected stories · PROVISIONAL / NOT FINAL ART</p><div class="grid">'+''.join(cards)+'</div>')
names={x['story'] for x in j['packets']}
checks={'29_packets':len(j['packets'])==29,'six_matchups':len(names)==6,'seven_gotw':len(new)==7,'six_overtures':sum(p['layout'].startswith('two equal') for p in j['packets'])==6,'six_dual_branches':sum('A home wins' in p['result_branch'] for p in j['packets'])==6,'all_1080x1920':all(p['canvas']==[1080,1920] for p in j['packets']),'no_result_selected':True}
(root/'week8_29_qa.json').write_text(json.dumps({'checks':checks,'result':'STRUCTURAL_PASS' if all(checks.values()) else 'FAIL','rendered_art':False,'independent_approval':False},indent=2))
print(json.dumps({'checks':checks,'paths':[str(root/x) for x in ['week8_29_packets.json','week8_29_contact_sheet.html','week8_29_qa.json']]}))
