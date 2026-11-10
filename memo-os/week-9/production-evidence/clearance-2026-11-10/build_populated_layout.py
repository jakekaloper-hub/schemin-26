"""Compose a measurable text/data rehearsal from the exact approval folios.
No artwork is generated; no data, authority, or approval flag is promoted.
"""
from pathlib import Path
import json,html,re
W=Path(__file__).resolve().parents[2]
a=json.loads((W/'WEEK_9_FINAL_APPROVAL_FOLIOS_2026-11-10.json').read_text())
base=(W/'WEEK_9_FULL_PAGE_LAYOUT_REHEARSAL_2026-11-09.html').read_text()
css=re.search(r'<style>(.*?)</style>',base,re.S).group(1)
css+='''.art[data-zone=landscape]{padding:12px}.art[data-zone=landscape] p{display:none}.reserve-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;height:100%}.reserve-group{padding:14px 18px;border:1px solid #8b7d60}.reserve-group h3{font:600 32px/39px system-ui;margin:0 0 8px;color:#e0bb70}.reserve-group p{font:36px/44px system-ui;margin:0}.scoreline{display:flex;justify-content:space-between;gap:18px;font:36px/43px system-ui}.score-panel{margin:12px 0;border-block:1px solid #b99859;padding:8px 0}.fact-caption{font:34px/45px system-ui!important;margin:12px 0 0!important}.table-note{font:34px/45px system-ui!important}.report{padding:18px 22px}.report h2{font:600 32px/39px system-ui;margin:0 0 8px}.report .label{font:600 26px/32px system-ui;color:#e0bb70;margin-bottom:8px}.report p{font:36px/47px system-ui}.data .scoreboard td{height:65px}.data .pair-end td{border-bottom:3px solid #b99859}.data .winner td{background:#283c35}.data table{table-layout:fixed}.data th,.data td{overflow-wrap:normal}.data td:first-child{width:auto}.copy .compact{font:34px/45px system-ui!important}'''
esc=lambda v:html.escape(str(v))
keys={
 'W09-P24':[('team','Team'),('record','Record'),('current_seed','Seed'),('points_for','Points for')],
 'W09-P25':[('power_rank','Rank'),('team','Team'),('scoring_form_index','Index')],
 'W09-P40':[('team','Team'),('current_seed','Current seed'),('projected_rank','Projected rank')],
 'W09-P26':[('home','Home'),('home_record','Record'),('away','Away'),('away_record','Record')]}
widths={'W09-P24':[50,15,10,25],'W09-P25':[10,65,25],'W09-P40':[60,20,20],'W09-P26':[36,14,36,14]}

def table(f):
 pid=f['page_id']
 if pid=='W09-P03':
  rows=[]
  for i,r in enumerate(f['data_rows'],1):
   for side in ['home','away']:
    score=r['points'] if side=='home' else r['away_points'];cl=('winner ' if r[side]==r['winner'] else '')+('pair-end' if side=='away' else '')
    rows.append('<tr class="'+cl+'"><td>'+str(i)+'</td><td>'+esc(r[side])+'</td><td>'+esc(score)+'</td></tr>')
  return '<table class="scoreboard"><colgroup><col style="width:8%"><col style="width:70%"><col style="width:22%"></colgroup><thead><tr><th>Game</th><th>Team</th><th>Points</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table>'
 cols=keys[pid]
 return '<table><colgroup>'+''.join('<col style="width:'+str(v)+'%">' for v in widths[pid])+'</colgroup><thead><tr>'+''.join('<th>'+esc(label)+'</th>' for _,label in cols)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(r[key])+'</td>' for key,_ in cols)+'</tr>' for r in f['data_rows'])+'</tbody></table>'

def reserve(f):
 groups={}
 for r in f['data_rows']:groups.setdefault(r['team'],[]).append(r['player'])
 return '<div class="reserve-grid">'+''.join('<section class="reserve-group"><h3>'+esc(t)+'</h3>'+''.join('<p>'+esc(n)+'</p>' for n in names)+'</section>' for t,names in groups.items())+'</div>'

def reports(f):
 return ''.join('<section class="report"><div class="label">'+esc(c['label'])+'</div><h2>'+esc(c['heading'])+'</h2><p>'+esc(c['text'])+'</p></section>' for c in f['report_cards'])

articles=[]
for f in a['folios']:
 c=f['copy'];pid=f['page_id'];parts=[]
 for name,rect in f['layout']['zones'].items():
  klass='copy'
  if name=='header':
   klass='header';content='<div class="kicker">SCHEMIN ’26 / WEEK 9 <span>'+str(f['reading_position'])+' / 35</span></div><h1>'+esc(c['headline'])+'</h1><p class="deck">'+esc(c['deck'])+'</p>'
  elif name in ['home_pov','away_pov']:content='<p class="pov">'+esc(c['pov'][name.split('_')[0]])+'</p>'
  elif name=='matchup_ribbon':klass='ribbonbox';content='<p class="ribbon">HOME PERSPECTIVE / AWAY PERSPECTIVE</p>'
  elif name=='stakes':content='<p class="minor">Entering Week 9: '+esc(f.get('entering_records',{}).get('home',''))+' against '+esc(f.get('entering_records',{}).get('away',''))+'.</p>'
  elif name=='table':klass='data';content=table(f)
  elif name=='reserve_groups':content=reserve(f)
  elif name in ['report_cards','division_panels']:content=reports(f)
  elif name in ['note','consequence']:content='<p class="minor">'+esc(f.get('publication_note',c['body']))+'</p>'
  elif name=='legend':content='<h2>The six host locations</h2><p class="minor">Country Club of Jackson · Mud Dogs Swamp · Red Leopard Ruins · Chili Stable · Highland Stronghold · Slob Foothill Camp</p>'
  elif name=='body':
   content='<p>'+esc(c['body'])+'</p>'
   if f.get('score_panel'):
    r=f['score_panel'];content+='<div class="score-panel">'+''.join('<div class="scoreline"><span>'+esc(r[side])+'</span><b>'+esc(r[side+'_score'])+'</b></div>' for side in ['home','away'])+'</div>'
    if f.get('football_caption'):content+='<p class="fact-caption">'+esc(f['football_caption'])+'</p>'
  else:
   klass='art';names=', '.join(x['full_name'] for x in f['character_identity']);content='<div class="art-label">ART AREA · NOT GENERATED</div><p>'+esc(names or 'Existing Commonwealth geography / environmental presentation')+'</p><div class="horizon"></div>'
  x,y,width,height=rect
  parts.append(f'<section class="zone {klass}" data-zone="{name}" style="left:{x}px;top:{y}px;width:{width}px;height:{height}px">{content}</section>')
 articles.append('<article class="sheet" id="'+pid+'" data-page="'+pid+'" hidden>'+''.join(parts)+'<footer>CONTENT AND DATA REHEARSAL · NOT FINISHED ART</footer></article>')
ids=[f['page_id'] for f in a['folios']]
script=re.search(r'<script>(.*?)</script>',base,re.S).group(1);script=re.sub(r'const ids=\[.*?\];',lambda _:'const ids='+json.dumps(ids)+';',script,count=1)
nav='<nav><strong>WEEK 9 / POPULATED APPROVAL REHEARSAL</strong><button id="prev">Previous</button><select id="choose" aria-label="Page">'+''.join('<option value="'+f['page_id']+'">'+str(f['reading_position'])+' · '+esc(f['copy']['headline'])+'</option>' for f in a['folios'])+'</select><button id="next">Next</button></nav>'
doc='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Week 9 populated approval rehearsal</title><style>'+css+'</style></head><body>'+nav+'<p class="notice">Full character names and source-bound numbers. The colored art areas are placeholders, not finished images. This verifies text geometry only; map labels and actual images still require review.</p><main class="stage">'+''.join(articles)+'</main><script>'+script+'</script></body></html>'
(W/'WEEK_9_FINAL_APPROVAL_LAYOUT_2026-11-10.html').write_text(doc)
print('Built35 populated approval-layout states; no source or artwork approval.')
