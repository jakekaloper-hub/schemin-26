from pathlib import Path
import copy,html,json
ROOT=Path(__file__).resolve().parent
FILE=ROOT/'Week_9_Approval_Review_Full_Names.json'
a=json.loads(FILE.read_text()); E=lambda x:html.escape(str(x))

# Reuse the same current publication payload for reading review and page geometry.
def tabular(f):
    p=f['publication_payload'];pid=f['page_id'];rows=p['rows']
    if pid=='W09-P03':
        return '<div class="scores">'+''.join('<div class="scorecard"><div><span>'+E(r['home'])+'</span><b>'+E(r['points'])+'</b></div><div><span>'+E(r['away'])+'</span><b>'+E(r['away_points'])+'</b></div><small>Winning margin: '+E(r['margin'])+'</small></div>' for r in rows)+'</div>'
    specs={
      'W09-P24':[('team','Team'),('record','Record'),('seed','Current seed')],
      'W09-P25':[('power_rank','Order'),('team','Team'),('scoring_form_index','Index')],
      'W09-P26':[('home','Home'),('away','Away')],
      'W09-P40':[('team','Team'),('current_seed','Current seed'),('projected_rank','Projected rank')],
      'W09-P37':[('team','Fantasy team'),('players','Observed reserve occupants')]}
    cols=specs.get(pid,[(k,k.replace('_',' ').title()) for k in (list(rows[0]) if rows else [])])
    # Observe source names rather than guess row aliases silently.
    if pid=='W09-P24':
        cols=[('team','Team'),('record','Record'),('current_seed','Current seed')]
    def cell(r,k):
        v=r.get(k)
        if v is None:raise ValueError(f'Missing published field {pid}.{k}; keys={list(r)}')
        return '<br>'.join(E(x) for x in v) if isinstance(v,list) else E(v)
    return '<table class="data-table '+('reserve' if pid=='W09-P37' else 'ranking' if pid=='W09-P25' else '')+'"><thead><tr>'+''.join('<th>'+E(h)+'</th>' for k,h in cols)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+cell(r,k)+'</td>' for k,h in cols)+'</tr>' for r in rows)+'</tbody></table>'

def result_panel(f):
    r=f['publication_payload']['score_panel']
    if not r:return ''
    return '<div class="result"><div><span>'+E(r['home'])+'</span><b>'+E(r['home_score'])+'</b></div><div><span>'+E(r['away'])+'</span><b>'+E(r['away_score'])+'</b></div><small>Winning margin: '+E(r['margin'])+'</small></div>'

def cards(f):
    return ''.join('<section class="report"><h3>'+E(c['label'])+'</h3><h4>'+E(c['heading'])+'</h4><p>'+E(c['text'])+'</p></section>' for c in f['publication_payload']['cards'])

def reader():
    md=['# Week 9 — Content approval review','', '35 pages. Full established names. Correct selected endings. Not approved for image generation or release.','', '**Review decisions:** retain the disclosed scoring-form index; present Reserve Watch only as fantasy roster occupancy; retain The Chili Cheesers hosting D0nkey K0ng as the proposed Week 10 Game of the Week.','', '**Persistence:** this revision is a prepared local change set against GitHub commit '+a['clearance']['base_commit']+'. Repository write actions were unavailable; it has NOT been committed.','']
    sections=[]
    for f in a['folios']:
        p=f['publication_payload'];main=''
        md += [f"## {f['reading_position']:02d}. {p['headline']}",'',p['deck'],'']
        if p['body']:main+='<p>'+E(p['body'])+'</p>';md +=[p['body'],'']
        for pov in p['pov']:
            main+='<section class="pov"><h3>'+E(pov['name'])+' · '+E(pov['side'].title())+' viewpoint</h3><p>'+E(pov['text'])+'</p></section>'
            md +=['### '+pov['name']+' — '+pov['side'].title()+' viewpoint','',pov['text'],'']
        if p.get('stakes'): main+='<p class="source">'+E(p['stakes'])+'</p>';md +=[p['stakes'],'']
        if p['teasers']:main+='<p class="teasers">'+' · '.join(E(t) for t in p['teasers'])+'</p>'
        if p['cards']:
            main+=cards(f)
            for c in p['cards']:md+=['### '+c['label']+' — '+c['heading'],'',c['text'],'']
        if p['rows']:
            main+='<div class="table-wrap">'+tabular(f)+'</div>'
            keys=list(p['rows'][0]);md+=['| '+' | '.join(k.replace('_',' ').title() for k in keys)+' |','|'+'|'.join('---' for _ in keys)+'|']
            for r in p['rows']:md.append('| '+' | '.join('; '.join(map(str,r[k])) if isinstance(r[k],list) else str(r[k]) if r[k] is not None else 'Not reported' for k in keys)+' |')
            md+=['']
        if p['score_panel']:main+=result_panel(f);md+=['**Result:** '+p['score_panel']['home']+' '+p['score_panel']['home_score']+' — '+p['score_panel']['away']+' '+p['score_panel']['away_score'],'']
        if p['sports_note']:main+='<aside>'+E(p['sports_note'])+'</aside>';md+=['**Football context:** '+p['sports_note'],'']
        production='<p><strong>Exact cast:</strong> '+E('; '.join(b['full_name'] for b in f['cast_binding']) or 'No principal character required')+'</p>'
        if f.get('final_visual_direction'):production+='<p>'+E(f['final_visual_direction'])+'</p>'
        production+='<p>Established character sources and identifiers are unchanged. Physical scene, reference attachment and final-pixel review remain required. The opposite ending is excluded from the active scene.</p>'
        sections.append('<article id="'+f['page_id']+'"><div class="kicker">'+str(f['reading_position']).zfill(2)+' / 35 · '+f['page_id']+'</div><h2>'+E(p['headline'])+'</h2><p class="deck">'+E(p['deck'])+'</p>'+main+'<details><summary>Production boundary — not printed in the memo</summary>'+production+'</details></article>')
    style='''*{box-sizing:border-box}body{margin:0;background:#10191b;color:#f4eddf;font:18px/1.6 Georgia,serif}header,main{max-width:1040px;margin:auto;padding:26px}header{border-bottom:1px solid #b69c65}h1,h2,h3,h4{line-height:1.2}h1{font-size:36px}h2{font-size:30px}.banner{border-left:4px solid #d2b77e;padding:14px 20px;background:#1c292a;font-family:system-ui;font-size:15px}article{padding:32px 0;border-bottom:1px solid #68614e}.kicker,.deck,aside,details,table,nav,.source{font-family:system-ui}.kicker{color:#dec18a;font-size:14px}.deck{color:#d8c8aa}.source{font-size:14px}nav{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:5px;font-size:14px}nav a{color:#eed4a2;padding:8px;min-height:44px}a:focus-visible,summary:focus-visible{outline:3px solid #f0cb77}.pov,.report,aside{border:1px solid #75684e;padding:14px 18px;margin:16px 0}.report h3,.report h4{margin:5px 0}.table-wrap{overflow:auto}table{width:100%;border-collapse:collapse;font-size:16px}td,th{padding:10px;border-bottom:1px solid #53605a;text-align:left;vertical-align:top}th{color:#dec18a}.result,.scorecard{padding:14px 18px;border:1px solid #716448;margin:14px 0;font-family:system-ui}.result div,.scorecard div{display:flex;justify-content:space-between;gap:16px}.result small,.scorecard small{color:#ceb98f}details{font-size:14px;margin-top:18px;color:#d2d8d3}summary{cursor:pointer;min-height:44px}p,td{overflow-wrap:anywhere}@media(max-width:500px){header,main{padding:16px}body{font-size:17px}h1{font-size:28px}h2{font-size:26px}table{font-size:14px}td,th{padding:8px 4px}}'''
    nav=''.join('<a href="#'+f['page_id']+'">'+str(f['reading_position'])+'. '+E(f['publication_payload']['headline'])+'</a>' for f in a['folios'])
    intro='<h1>Week 9 · Approval Review</h1><p>Full established character names. Thirty-five pages. Six decided outcomes.</p><div class="banner"><strong>Content review, not final artwork.</strong> This revised copy is prepared for your approval. It has not been committed to GitHub in this session. Source acceptance, permission to render, and release approval remain ungranted.<br><br><strong>Editorial recommendation:</strong> publish the transparent scoring-form index under that name; limit Reserve Watch to observed fantasy slots; keep The Chili Cheesers versus D0nkey K0ng as the proposed Week 10 spotlight.</div><p>The text below is the proposed reader copy. Production instructions are separated into expandable notes. Approving this document does not approve an unseen image or invent a source-acceptance receipt.</p>'
    doc='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Week 9 · Approval Review</title><style>'+style+'</style></head><body><header>'+intro+'<nav aria-label="Issue contents">'+nav+'</nav></header><main>'+''.join(sections)+'</main></body></html>'
    (ROOT/'Week_9_Approval_Review_Full_Names.html').write_text(doc)
    (ROOT/'Week_9_Approval_Review_Full_Names.md').write_text('\n'.join(md).rstrip()+'\n')

def layout():
    sheets=[]
    for f in a['folios']:
        p=f['publication_payload'];pid=f['page_id'];z=copy.deepcopy(f['layout']['zones']);kind=f['layout']['archetype']
        if f['is_finale']:
            z={'header':[60,50,960,250],'art':[60,325,960,620],'body':[60,970,960,540],'score':[60,1530,960,180],'evidence':[60,1730,960,125]}
        if kind=='report_cards' and pid!='W09-P37':
            z={'header':[60,50,960,250],'landscape':[60,325,960,100],'report_cards':[60,445,960,1220],'note':[60,1685,960,170]}
        if pid=='W09-P37':z={'header':[60,50,960,230],'table':[60,310,960,1375],'note':[60,1710,960,145]}
        if kind=='realm':z={'header':[60,50,960,250],'landscape':[60,325,960,100],'report_cards':[60,445,960,1220],'note':[60,1685,960,170]}
        parts=[]
        for name,b in z.items():
            cl='copy';content=''
            if name=='header':content='<div class="kicker">SCHEMIN ’26 / WEEK 9 <span>'+str(f['reading_position']).zfill(2)+'</span></div><h1>'+E(p['headline'])+'</h1><p class="deck">'+E(p['deck'])+'</p>';cl='header'
            elif name in ['home_pov','away_pov']:
                pov=p['pov'][0 if name=='home_pov' else 1];content='<p>'+E(pov['text'])+'</p>'
            elif name=='matchup_ribbon':content='<p class="ribbon">HOME VIEWPOINT / AWAY VIEWPOINT</p>'
            elif name=='stakes':content='<p class="minor">'+E(p.get('stakes',''))+'</p>'
            elif name=='table':content=tabular(f);cl='data'
            elif name=='report_cards':content=cards(f);cl='reports'
            elif name=='note':content='<p class="minor">'+E(p['body'])+'</p>'
            elif name=='body':content='<p>'+E(p['body'])+'</p>'
            elif name=='score':content=result_panel(f);cl='resultbox'
            elif name=='evidence':content='<p class="minor">'+E(p['sports_note'])+'</p>'
            elif name=='legend':content='<p class="minor">'+E(p['body'])+'</p>'
            else:
                label='Established scene artwork — not generated'
                if name in ['home_art','away_art']:label=p['pov'][0 if name=='home_art' else 1]['name']+' · established appearance'
                if name=='map':label='Canonical Commonwealth map · twelve home markers and six hosted events · final labels not assembled'
                content='<span>ART AREA · NOT GENERATED</span>'+('' if name=='landscape' else '<p>'+E(label)+'</p>');cl='art'
            x,y,w,h=b
            parts.append(f'<section class="zone {cl}" data-zone="{name}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'+content+'</section>')
        f['layout']['zones']=z;f['layout']['clearance_adjustment']='Final-value/full-name typographic review. Art has not been accepted.'
        sheets.append('<article class="sheet" data-page="'+pid+'" id="'+pid+'" hidden>'+''.join(parts)+'<footer>TYPE AND DATA PROOF · NOT FINISHED ARTWORK</footer></article>')
    css='''*{box-sizing:border-box}body{margin:0;background:#182421;color:#f3ead8;font:16px/1.5 system-ui}nav{position:sticky;top:0;z-index:9;background:#182421;padding:10px;display:flex;gap:8px;flex-wrap:wrap;align-items:center}button,select{font:inherit;padding:8px;min-height:44px;max-width:100%;background:#283d32;color:white;border:1px solid #bda06b}button:focus-visible,select:focus-visible{outline:3px solid #e6c36c}.notice{margin:12px auto;max-width:900px;padding:0 16px}.stage{position:relative;margin:0 auto 25px;overflow:hidden}.sheet{position:absolute;width:1080px;height:1920px;background:#101a1d;border:3px solid #c1a064;transform-origin:top left}.sheet[hidden]{display:none}.zone{position:absolute;overflow:hidden}.kicker{font:24px/30px system-ui;letter-spacing:2px;color:#d9b773}.kicker span{float:right}h1{font:600 58px/1.05 Georgia;margin:16px 0 12px}p.deck{font:36px/1.18 system-ui;margin:0;color:#e6d8ba}.copy p{font:42px/55px Georgia;margin:0}.copy p.minor{font:34px/45px system-ui;margin:0}.copy p.ribbon{font:28px/58px system-ui;text-align:center}.art{background:linear-gradient(160deg,#536a60,#223b39 55%,#172829);border:1px solid #6d8370;text-align:center;padding:20px;display:flex;flex-direction:column;align-items:center;justify-content:center}.art span{font:24px/35px system-ui;color:#e4d0a5}.art p{font:28px/38px system-ui;color:#d0dfd7;margin:10px;max-width:850px}.data table{border-collapse:collapse;width:100%;font:38px/47px system-ui}.data th{font:30px/36px system-ui;color:#dabb83;text-align:left;padding:12px;border-bottom:2px solid #b99859}.data td{padding:12px;height:75px;border-bottom:1px solid #53605a;vertical-align:top}.data td:first-child{min-width:70px}.data table:not(.reserve) td:nth-child(1){width:55%}.data table.ranking{table-layout:fixed}.data table.ranking th:first-child,.data table.ranking td:first-child{width:12%}.data table.ranking th:nth-child(2),.data table.ranking td:nth-child(2){width:67%}.data table.ranking th:nth-child(3),.data table.ranking td:nth-child(3){width:21%}.data table.reserve td:first-child{width:44%}.data table.reserve td{padding:12px;line-height:47px}.scores{display:grid;grid-template-rows:repeat(6,1fr);height:100%;gap:14px}.scorecard{padding:9px 16px;border:1px solid #8a7758;font:38px/47px system-ui}.scorecard div,.result div{display:flex;justify-content:space-between;gap:15px}.scorecard small,.result small{font:30px/36px system-ui;color:#d1ba8f}.result{padding:7px 14px;border:1px solid #9c815b;font:38px/48px system-ui}.reports{display:flex;flex-direction:column;gap:18px}.report{flex:1;min-height:0;padding:20px 24px;border:1px solid #8b7d60;background:#1c2a29}.report h3{font:600 30px/36px system-ui;letter-spacing:.4px;margin:0 0 8px;color:#e0bb70}.report h4{font:600 36px/44px Georgia;margin:0 0 12px}.report p{font:36px/47px system-ui;margin:0}footer{position:absolute;bottom:18px;left:60px;font:20px/24px system-ui;color:#c9b78e}.report.overflow,.zone.overflow{outline:4px solid red}@media(max-width:500px){nav{font-size:13px}.notice{font-size:12px}}'''
    ids=[f['page_id'] for f in a['folios']]
    script='const ids='+json.dumps(ids)+''';let current=ids[0];function fit(){let s=Math.min((document.documentElement.clientWidth-24)/1080,.65);document.querySelector('.stage').style.width=1080*s+'px';document.querySelector('.stage').style.height=1920*s+'px';document.querySelectorAll('.sheet').forEach(p=>p.style.transform='scale('+s+')')}function show(id){current=id;document.querySelectorAll('.sheet').forEach(p=>p.hidden=p.dataset.page!==id);document.querySelector('#choose').value=id;fit()}function inspect(){let issues=[];document.querySelectorAll('.sheet').forEach(p=>{let h=p.hidden;p.hidden=false;p.querySelectorAll('.zone,.report').forEach(z=>{if(z.scrollHeight>z.clientHeight+2||z.scrollWidth>z.clientWidth+2)issues.push({page:p.dataset.page,zone:z.dataset.zone||z.className,height:z.clientHeight,needed:z.scrollHeight,width:z.clientWidth,neededWidth:z.scrollWidth})});p.hidden=h});return issues}document.querySelector('#choose').onchange=e=>show(e.target.value);document.querySelector('#prev').onclick=()=>show(ids[Math.max(0,ids.indexOf(current)-1)]);document.querySelector('#next').onclick=()=>show(ids[Math.min(ids.length-1,ids.indexOf(current)+1)]);addEventListener('resize',fit);show(ids.includes(location.hash.slice(1))?location.hash.slice(1):ids[0]);'''
    menu=''.join('<option value="'+f['page_id']+'">'+str(f['reading_position'])+' · '+E(f['publication_payload']['headline'])+'</option>' for f in a['folios'])
    doc='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Week 9 · Populated layout review</title><style>'+css+'</style></head><body><nav><strong>WEEK 9 · POPULATED TYPE REVIEW</strong><button id="prev">Previous</button><select id="choose" aria-label="Choose page">'+menu+'</select><button id="next">Next</button></nav><p class="notice">Full character names and reported final values. Illustrated regions remain placeholders. This proof does not grant source acceptance, permission to generate images, or publication approval.</p><main class="stage">'+''.join(sheets)+'</main><script>'+script+'</script></body></html>'
    (ROOT/'Week_9_Populated_Layout_Review.html').write_text(doc)
    (ROOT/'Week_9_Approval_Review_Full_Names.json').write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':
    reader();layout();print('Built35 reading and populated typographic folios. Image regions remain placeholders.')
