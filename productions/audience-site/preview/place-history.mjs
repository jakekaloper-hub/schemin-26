/** Observer-only source World Memory reading. History is never a current-state feed. */
const check=(truth,code)=>{if(!truth)throw Error(code);};
export function historyForLocation(catalog,locationId){
  check(catalog?.locations?.some(p=>p.id===locationId),'UNKNOWN_LOCATION');
  const index=catalog.history;
  check(index?.publicationAuthorized===false&&['RELEASE_CANDIDATE','NOT_CONNECTED'].includes(index.status),'HISTORY_AUTHORITY_INVALID');
  const placeIds=new Set(catalog.locations.map(x=>x.id));
  check(index.events.every(x=>placeIds.has(x.locationId)&&x.publicationAuthorized===false),'HISTORY_LOCATION_DRIFT');
  return structuredClone(index.events.filter(x=>x.locationId===locationId));
}
export function openPlaceHistory(catalog,locationId,camera){
  const entries=historyForLocation(catalog,locationId);check(entries.length>0,'NO_HISTORY');
  check(camera?.target?.length===3&&[...camera.target,camera.yaw,camera.pitch,camera.distance].every(Number.isFinite),'INVALID_RETURN_CAMERA');
  return {locationId,returnCamera:structuredClone(camera),entries,inputOwner:'HISTORY',worldMutationAllowed:false,liveWeatherAllowed:false,publicationAuthorized:false};
}
export function closePlaceHistory(session){
  check(session?.inputOwner==='HISTORY'&&session.returnCamera,'NO_HISTORY_SESSION');
  return {locationId:session.locationId,camera:structuredClone(session.returnCamera),inputOwner:'WORLD'};
}
