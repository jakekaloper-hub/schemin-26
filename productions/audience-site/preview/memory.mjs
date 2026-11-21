/** Private edition views. These inspect supplied historical art, never mutate world state.
 * A bound memory is not approved present-day environment geometry or a public release. */
const requireValue=(ok,message)=>{if(!ok)throw Error(message);};
const nonempty=x=>typeof x==='string'&&x.trim().length>0;
const hash=x=>typeof x==='string'&&/^[a-f0-9]{64}$/.test(x);
export function validateMemoryIndex(index,locationIds){
 requireValue(index?.schemaVersion===1&&index.scope==='PRIVATE_LOCAL'&&index.publicationAuthorized===false,'PRIVATE_SOURCE_CONTEXT_REQUIRED');
 requireValue(hash(index.source?.sha256)&&nonempty(index.source?.fileName)&&Number.isInteger(index.source?.season)&&Number.isInteger(index.source?.week),'INVALID_SOURCE');
 requireValue(Array.isArray(locationIds)&&Array.isArray(index.memories),'INVALID_INDEX');
 const known=new Set(locationIds),ids=new Set(),places=new Set();
 for(const m of index.memories){
  requireValue(nonempty(m.id)&&!ids.has(m.id)&&!places.has(m.locationId),'DUPLICATE_OR_INVALID_MEMORY');ids.add(m.id);places.add(m.locationId);
  requireValue(known.has(m.locationId),'UNKNOWN_LOCATION');
  requireValue(nonempty(m.title)&&Array.isArray(m.pages)&&m.pages.length>0,'INVALID_MEMORY');
  requireValue(Number.isInteger(m.entryIndex)&&m.entryIndex>=0&&m.entryIndex<m.pages.length,'INVALID_ENTRY');
  const pages=new Set();
  for(const p of m.pages){
   requireValue(nonempty(p.id)&&!pages.has(p.id),'DUPLICATE_PAGE');pages.add(p.id);
   requireValue(Number.isInteger(p.pdfPage)&&p.pdfPage>0&&hash(p.sha256)&&p.width>0&&p.height>0&&nonempty(p.title)&&nonempty(p.alt),'INVALID_PAGE');
   requireValue(/^assets\/[A-Za-z0-9_.-]+\.(jpg|png)$/.test(p.path),'INVALID_ASSET_PATH');
   requireValue(Array.isArray(p.crop)&&p.crop.length===4&&p.crop.every(v=>Number.isFinite(v)&&v>=0&&v<=1)&&p.crop[2]>p.crop[0]&&p.crop[3]>p.crop[1],'INVALID_CROP');
  }
 }
 return structuredClone(index);
}
export function memoryForLocation(index,locationId){return index.memories.find(m=>m.locationId===locationId)||null;}
export function openMemory(index,locationId,camera){
 const m=memoryForLocation(index,locationId);requireValue(m,'NO_MEMORY_FOR_LOCATION');
 requireValue(index.scope==='PRIVATE_LOCAL'&&index.publicationAuthorized===false,'PRIVATE_SOURCE_CONTEXT_REQUIRED');
 requireValue(camera?.target?.length===3&&[...camera.target,camera.distance,camera.yaw,camera.pitch].every(Number.isFinite),'INVALID_RETURN_CAMERA');
 return {memoryId:m.id,locationId,season:index.source.season,week:index.source.week,pageIndex:m.entryIndex,view:'SCENE',status:'LOADING',loadToken:1,returnCamera:structuredClone(camera),inputOwner:'MEMORY',liveWeatherAllowed:false,worldMutationAllowed:false};
}
export function navigateMemory(session,index,delta){
 requireValue(Number.isInteger(delta),'INVALID_PAGE_DELTA');const m=index.memories.find(x=>x.id===session.memoryId);requireValue(m,'UNKNOWN_MEMORY');
 const pageIndex=Math.max(0,Math.min(m.pages.length-1,session.pageIndex+delta));
 if(pageIndex===session.pageIndex)return structuredClone(session);
 return {...structuredClone(session),pageIndex,loadToken:session.loadToken+1,status:'LOADING'};
}
export function memoryAssetResult(session,token,ok){
 if(token!==session.loadToken)return structuredClone(session);
 requireValue(typeof ok==='boolean','INVALID_ASSET_RESULT');return {...structuredClone(session),status:ok?'READY':'FAILED'};
}
export function memoryView(session,view){requireValue(['SCENE','FOLIO'].includes(view),'INVALID_MEMORY_VIEW');return {...structuredClone(session),view};}
export function closeMemory(session){return {camera:structuredClone(session.returnCamera),locationId:session.locationId,inputOwner:'WORLD'};}
export function memoryCoverage(index,locationIds){const linked=new Set(index.memories.map(m=>m.locationId));return {total:locationIds.length,linked:locationIds.filter(id=>linked.has(id)).length,unlinked:locationIds.filter(id=>!linked.has(id)),publicationAuthorized:false};}
