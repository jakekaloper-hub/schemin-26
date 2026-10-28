// Presentation coordinates only; canonical positions remain unmodified.
export function projectPoint({x,y}){return {x:90+Number(x)*8.2,y:650-Number(y)*5.8};}
export function readRoute(hash){const [path,query='']=String(hash||'#home').replace(/^#/,'').split('?');const [page='home',...parts]=path.split('/');try{return {page:page||'home',id:decodeURIComponent(parts.join('/')),query};}catch{return {page:'missing',id:'',query:''};}}
export function chooseMemo(memos,id){return id?memos.find(m=>m.id===id&&m.releaseState==='RELEASED')||null:null;}
export function clampPage(value,count){const n=Number(value);return Math.max(1,Math.min(Math.max(1,count),Number.isFinite(n)?Math.floor(n):1));}
export function loadPreference(key,fallback,storage){try{const raw=(storage||localStorage).getItem('schemin-experience:'+key);return raw===null?fallback:JSON.parse(raw);}catch{return fallback;}}
export function savePreference(key,value,storage){try{(storage||localStorage).setItem('schemin-experience:'+key,JSON.stringify(value));}catch{/* Browsing never depends on storage. */}}
export function relatedRecords(records,field,id){return records.filter(record=>Array.isArray(record[field])&&record[field].includes(id));}
export function routeNeighbors(route,id){const stops=[route.from,...(route.via_location_ids||(route.via_location_id?[route.via_location_id]:[])),route.to];const i=stops.indexOf(id);return i<0?[]:[stops[i-1],stops[i+1]].filter(Boolean);}
export function artForUse(assets,id,use='page'){const a=assets?.[id];return a?.status==='REVIEWED_PRESENTATION'&&(a.allowedUses||['page']).includes(use)?a:null;}
