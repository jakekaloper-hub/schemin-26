/* Week 11 live editor patch — run inside connected tldraw exec with exact source JSON.
 * This file does not open a board, contact a server, promote staff, or approve art.
 * Modes: inspect; titles; import (one G-code); stage (explicit verified folios).
 * Always inspect a live page first. An unknown operation must be re-inspected. */
async function runW11Tldraw(editor, helpers, data, request) {
  const { mode, scene, folios = [], inspected = false } = request || {};
  if (editor.getCurrentPageId() !== data.page_id) throw Error('WRONG_OR_UNCONFIRMED_PAGE');
  const all = () => editor.getCurrentPageShapes();
  const shapes = new Map(all().map(s => [s.id,s]));
  const folia = data.folia;
  const lookup = id => editor.getShape(id);
  if (folia.length !== 35 || data.gallery.length !== 6) throw Error('BAD_SOURCE_MANIFEST');
  const missing = folia.flatMap(f => [f.card_id,f.review_id]).filter(id => !shapes.has(id));
  if (missing.length) throw Error('EXISTING_CARD_PAIR_MISSING: '+missing.join(','));
  const read = shape => (shape?.props?.richText?.content || []).map(p=>(p.content||[]).map(n=>n.text||'').join('')).filter(Boolean);
  const readImage = id => { const s=lookup(id);return s?{id:s.id,type:s.type,assetId:s.props?.assetId,x:s.x,y:s.y,w:s.props?.w,h:s.props?.h}:null; };
  if (mode==='inspect') {
    return {page:editor.getCurrentPageId(),shapes:all().length,originalPairs:35,
      folios:folia.map(f=>({folio:f.id,title:f.title,production:read(lookup(f.card_id)),review:read(lookup(f.review_id)),diagram:!!lookup('shape:w11-frame-v1-'+f.id.toLowerCase())})),
      gallery:data.gallery.map(g=>({scene:g.scene,observed:readImage(g.id)})),
      authority:'LIVE_INSPECTION_ONLY_NOT_RENDER_ACCEPTANCE'};
  }
  if (!inspected) throw Error('FRESH_INSPECTION_REQUIRED');
  if (mode==='titles') {
    const patch=[],changed=[],held=[];
    for(const f of folia.filter(f=>['F19','F20'].includes(f.id))){
      const old=f.id==='F19'?'One clean paw':'Back at the post';
      for(const id of [f.card_id,f.review_id]){
        const s=lookup(id);if(s.type!=='geo'){held.push({id,reason:'TYPE'});continue}
        const rt=JSON.parse(JSON.stringify(s.props.richText));
        const p=(rt.content||[]).find(p=>(p.content||[]).some(n=>(n.text||'').trim()));
        const txt=(p?.content||[]).map(n=>n.text||'').join('');
        if (txt.includes(f.title)) continue;
        if(!txt.includes(old)){held.push({id,reason:'UNEXPECTED_HEADING',txt});continue}
        p.content=[{type:'text',text:txt.replace(old,f.title),marks:[{type:'bold'}]}];
        patch.push({id,type:'geo',props:{richText:rt}});changed.push(id);
      }
    }
    if(patch.length)editor.updateShapes(patch);
    return {changed,held,readback:changed.map(id=>({id,heading:read(lookup(id))[0]}))};
  }
  const anchorId='shape:w11-visual-integration-origin-v1';
  const anchor = () => {
    const old=lookup(anchorId);if(old)return{x:old.x,y:old.y};
    const ext=all().reduce((a,s)=>Math.max(a,(editor.getShapePageBounds(s.id)?.maxX ?? (s.x+(s.props?.w||0)))),0);
    const x=ext+500,y=350;
    editor.createShape({id:anchorId,type:'geo',x,y,props:{geo:'rectangle',w:2250,h:80,color:'grey',fill:'none',dash:'solid',size:'m',richText:helpers.toRichText('WEEK 11 • SOURCE-BOUND SHOT GALLERY / EDITABLE CAMERA BLOCKING • PREPRODUCTION ONLY')}});
    const a=lookup(anchorId);if(!a)throw Error('ANCHOR_NOT_READ_BACK');
    return {x:a.x,y:a.y};
  };
  if(mode==='import'){
    const i=data.gallery.findIndex(x=>x.scene===scene);
    if(i<0)throw Error('UNKNOWN_SCENE');
    const g=data.gallery[i];
    const existing=readImage(g.id);
    if(existing){if(existing.type!=='image'||!existing.assetId)throw Error('TARGET_ID_COLLISION');
      return {state:'EXISTING_ASSET_NEEDS_VISUAL_SOURCE_COMPARISON',scene,existing};}
    const origin=anchor();
    const result=await helpers.addImage(g.url,{id:g.id,x:origin.x+(i%2)*1250,y:origin.y+120+Math.floor(i/2)*800,w:1120});
    const actual=readImage(g.id);
    if(!actual||actual.type!=='image'||!actual.assetId)throw Error('IMPORT_READBACK_MISSING');
    if(result.assetId&&actual.assetId!==result.assetId)throw Error('ASSET_ID_READBACK_MISMATCH');
    return {state:'IMPORTED_AND_SHAPE_READ_BACK_PENDING_SCREENSHOT',scene,sourceSha256:g.sha256,actual,result};
  }
  if(mode==='stage'){
    if(!Array.isArray(folios)||!folios.length||new Set(folios).size!==folios.length||folios.some(x=>!folia.find(f=>f.id===x)))throw Error('EXPLICIT_REVIEWED_FOLIO_LIST_REQUIRED');
    const origin=anchor();
    const add=[],existing=[];
    const geo=(id,x,y,w,h,color,fill,label,url='')=>({id,type:'geo',x,y,props:{geo:'rectangle',w,h,color,fill,dash:'solid',size:'s',align:'start',verticalAlign:'start',richText:helpers.toRichText(label),url}});
    for(const fid of folios){
      const f=folia.find(x=>x.id===fid), n=Number(fid.slice(1))-1, stem='shape:w11-frame-v1-'+fid.toLowerCase(), x=origin.x+(n%7)*435,y=origin.y+2640+Math.floor(n/7)*775;
      const defs=[geo(stem,x,y,360,640,'grey','none','',f.source),geo(stem+'-label',x,y-62,360,57,'grey','none',f.id+' / '+f.title,f.source),geo(stem+'-type',x+16,y+568,328,56,'grey','none','LETTERING / SAFE')];
      for(const [i,b] of f.boxes.entries()){
        const [label,a,c,w,h,color]=b;
        defs.push(geo(stem+'-b'+i,x+a*2,y+c*2,w*2,h*2,color,'semi',h<20?'':label));
      }
      for(const shape of defs){
        const present=lookup(shape.id);
        if(present){
          if(present.type!=='geo'||Math.abs(present.x-shape.x)>1||Math.abs(present.y-shape.y)>1)throw Error('EXISTING_DIAGRAM_POSITION_OR_TYPE_CONFLICT '+shape.id);
          existing.push(shape.id);
        } else add.push(shape);
      }
    }
    if(add.length)editor.createShapes(add);
    const missingAfter=add.filter(s=>!lookup(s.id)).map(s=>s.id);
    if(missingAfter.length)throw Error('SHAPE_READBACK_MISSING '+missingAfter.join(','));
    return {state:'EDITABLE_BLOCKING_SHAPE_IDS_READ_BACK_PENDING_VISUAL_INSPECTION',folios,added:add.map(s=>s.id),existing,originalPairs:35};
  }
  throw Error('UNKNOWN_MODE');
}
if(typeof module!=='undefined'&&module.exports)module.exports={runW11Tldraw};
