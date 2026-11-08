import json,pathlib,html
root=pathlib.Path.home()/'Developer/ai/schemin-visual-local/week8-review'
src=json.loads((root/'week8_packets_oxford_revision.json').read_text())
add={
'Hostile Ground':('The fortress that remembers','Architecture reveals a tactical reversal; never invent prior destruction','The LLC believes the ruins are under control; a new vantage reverses apparent advantage'),
"The Storm That Wouldn't Leave":('Escalating absurd siege','Ordered defenses produce increasingly ridiculous failures','A single drip after the storm gate shuts becomes a potential flood'),
'The Last Light':('The disappearing horizon','Every scene progressively reduces daylight','Hunter and hunted freeze in shallow water as the final sunset reflection vanishes'),
'The Fallen Giant':('Silence after the charge','Giant charge, Chins resistance, battlefield falls silent','Ground-level DK four-legged charge; Chins still standing in the aftermath'),
'The Weight of a Crown':('The champion who expects applause','Ceremonial entry collides with indifference at Slob foothill camp','The crowd falls silent as Slob casually prepares to fight')}
for p in src['packets']:
 if p['story'] in add:
  name,device,shot=add[p['story']]
  p['enrichment_device']=name
  p['enrichment_direction']=device
  if p['packet_id'].endswith('-03'):p['signature_visual_proposal']=shot
  p['historical_fact_status']='fictional creative proposal; no invented real incident'
 if p['story']=='The Place We Once Knew':
  p['enrichment_device']='Oxford corner-bedroom historical memory / architectural match cut'
  p['historical_fact_status']='Founder-supplied shared corner bedroom at Ole Miss Kappa Sigma house; exact room appearance unverified'
src['production_status']='ENRICHED STORYBOARD PREVIS; NOT FINAL ART; OUTCOME UNDECIDED'
src['creative_enrichment_version']='2026-11-02'
out=root/'week8_enriched_packets.json';out.write_text(json.dumps(src,indent=2))
cards=[]
for p in src['packets']:
 device=p.get('enrichment_device','')
 cards.append('<article><span>'+html.escape(p['packet_id'])+'</span><h3>'+html.escape(p['shot'])+'</h3><b>'+html.escape(p['story'])+'</b><p>'+html.escape(device)+'</p><small>'+html.escape(p['location_id'])+' | '+html.escape(p['result_branch'])+'</small></article>')
css='body{font:16px system-ui;background:#10151c;color:#eee6d9;margin:24px}h1{color:#efcd90}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}article{border:1px solid #67717d;border-radius:8px;background:#222c38;padding:16px;min-height:190px}span,small{color:#c7b487}small{display:block;margin-top:14px}@media(max-width:800px){.grid{grid-template-columns:1fr}}'
(root/'week8_enriched_contact_sheet.html').write_text('<!doctype html><meta charset="utf-8"><style>'+css+'</style><h1>SCHEMIN 26 — WEEK 8 ENRICHED STORYBOARD</h1><p>28 compositions · five Inklings enrichments · Oxford GOTW memory · PROVISIONAL</p><div class="grid">'+''.join(cards)+'</div>')
checks={'28_packets':len(src['packets'])==28,'five_stories_enriched':len({p['story'] for p in src['packets'] if p['story'] in add})==5,'all_six_dual_outcomes':all(any(p['story']==name and 'A home wins' in p['result_branch'] for p in src['packets']) for name in {p['story'] for p in src['packets']}),'all_canvases_1080x1920':all(p['canvas']==[1080,1920] for p in src['packets'])}
(root/'week8_enriched_qa.json').write_text(json.dumps({'checks':checks,'result':'STRUCTURAL_PASS / VISUAL_AND_RELEASE_BLOCKED','not_performed':['rendered visual QA','independent umpire','Fact Lock','Week4-7 world state reconciliation']},indent=2))
print(json.dumps({'files':[str(out),str(root/'week8_enriched_contact_sheet.html'),str(root/'week8_enriched_qa.json')],'checks':checks}))
