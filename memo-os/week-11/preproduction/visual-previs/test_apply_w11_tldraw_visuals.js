'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {runW11Tldraw}=require('./apply_w11_tldraw_visuals');
const data=require('./W11_EDITABLE_PORTRAIT_BLOCKING.json');
function mock(){
 const map=new Map();let page=data.page_id;let importCount=0;
 const rt=text=>({type:'doc',content:[{type:'paragraph',content:[{type:'text',text}]}]});
 for(const f of data.folia){
  for(const id of [f.card_id,f.review_id]){
   const label=f.id==='F19'?'One clean paw':f.id==='F20'?'Back at the post':f.title;
   map.set(id,{id,type:'geo',x:10,y:10,props:{w:626,h:427,richText:rt(f.id+'  '+label)}});
  }
 }
 const editor={getCurrentPageId:()=>page,getCurrentPageShapes:()=>[...map.values()],getShape:id=>map.get(id),
 getShapePageBounds:id=>({maxX:map.get(id).x+(map.get(id).props.w||0)}),
 createShape:s=>{if(map.has(s.id))throw Error('DUPLICATE');map.set(s.id,s)},
 createShapes:ss=>{for(const s of ss)editor.createShape(s)},
 updateShapes:ss=>{for(const s of ss){const old=map.get(s.id);map.set(s.id,{...old,props:{...old.props,...s.props}})}}};
 const helpers={toRichText:rt,addImage:async(url,opts)=>{importCount++;const a='asset:test-'+importCount;editor.createShape({id:opts.id,type:'image',x:opts.x,y:opts.y,props:{w:opts.w,h:630,assetId:a}});return {shapeId:opts.id,assetId:a}}};
 return {editor,helpers,map,setPage:p=>page=p,imports:()=>importCount};
}
test('inspect verifies every existing folio pair; no mutations',async()=>{
 const m=mock(),r=await runW11Tldraw(m.editor,m.helpers,data,{mode:'inspect'});
 assert.equal(r.originalPairs,35);assert.equal(r.folios.length,35);assert.equal(r.gallery.length,6);assert.equal(m.map.size,70);
});
test('reject wrong page, missing cards, or unsurveyed editing',async()=>{
 const m=mock();m.setPage('page:other');
 await assert.rejects(runW11Tldraw(m.editor,m.helpers,data,{mode:'inspect'}),/WRONG_OR_UNCONFIRMED_PAGE/);
 m.setPage(data.page_id);await assert.rejects(runW11Tldraw(m.editor,m.helpers,data,{mode:'import',scene:'G01'}),/FRESH_INSPECTION_REQUIRED/);
 m.map.delete(data.folia[0].card_id);await assert.rejects(runW11Tldraw(m.editor,m.helpers,data,{mode:'inspect'}),/EXISTING_CARD_PAIR_MISSING/);
});
test('titles patch exactly four stale headings; safe replay makes zero changes',async()=>{
 const m=mock();let r=await runW11Tldraw(m.editor,m.helpers,data,{mode:'titles',inspected:true});
 assert.equal(r.changed.length,4);assert.ok(r.readback.every(x=>/The wrong turn|The road that comes back/.test(x.heading)));
 r=await runW11Tldraw(m.editor,m.helpers,data,{mode:'titles',inspected:true});assert.equal(r.changed.length,0);
});
test('six imported assets and stable IDs are read back; no duplicate re-import',async()=>{
 const m=mock();for(const g of data.gallery){let r=await runW11Tldraw(m.editor,m.helpers,data,{mode:'import',scene:g.scene,inspected:true});assert.ok(r.actual.assetId);assert.equal(r.actual.id,g.id)}
 assert.equal(m.imports(),6);await runW11Tldraw(m.editor,m.helpers,data,{mode:'import',scene:'G01',inspected:true});assert.equal(m.imports(),6);
});
test('35 editable distinct diagram groups add without touching 70 cards; repeat adds none',async()=>{
 const m=mock(),original=new Map(m.map),ids=data.folia.map(f=>f.id);
 const r=await runW11Tldraw(m.editor,m.helpers,data,{mode:'stage',folios:ids,inspected:true});assert.equal(r.folios.length,35);
 assert.ok(r.added.length>140);assert.equal(new Set(r.added).size,r.added.length);
 for(const [id,s] of original)assert.equal(m.map.get(id),s);
 const second=await runW11Tldraw(m.editor,m.helpers,data,{mode:'stage',folios:ids,inspected:true});assert.equal(second.added.length,0);
});
test('detect unexpected diagram collision and require explicit folio list',async()=>{
 const m=mock();await assert.rejects(runW11Tldraw(m.editor,m.helpers,data,{mode:'stage',inspected:true}),/EXPLICIT_REVIEWED_FOLIO_LIST_REQUIRED/);
 m.map.set('shape:w11-frame-v1-f01',{id:'shape:w11-frame-v1-f01',type:'image',x:1,y:1,props:{w:1,h:1}});
 await assert.rejects(runW11Tldraw(m.editor,m.helpers,data,{mode:'stage',folios:['F01'],inspected:true}),/EXISTING_DIAGRAM_POSITION_OR_TYPE_CONFLICT/);
});
