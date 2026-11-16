/** Preview-only spatial interpretation. Source IDs/XY remain upstream; relief is not canon. */
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
export function atlasToScene(p){if(!Array.isArray(p)||p.length!==2||!p.every(Number.isFinite))throw new Error('INVALID_ATLAS_POSITION');return [(p[0]-50)*2,0,(50-p[1])*2];}
export function spatialBindings(catalog){
 if(!catalog||!Array.isArray(catalog.locations))throw new Error('MISSING_ATLAS');
 const seen=new Set();return catalog.locations.map(p=>{if(!/^LOC-/.test(p.id)||seen.has(p.id))throw new Error('INVALID_OR_DUPLICATE_LOCATION');seen.add(p.id);return {...structuredClone(p),anchor:atlasToScene(p.position),visible:true};});
}
export function defaultCamera(){return {target:[0,0,0],distance:280,yaw:-.23,pitch:.78};}
export function cameraStep(c,{zoom=0,pitch=0,yaw=0,panX=0,panZ=0,inputOwner='WORLD'}={}){
 if(inputOwner!=='WORLD')return structuredClone(c);
 if(![zoom,pitch,yaw,panX,panZ].every(Number.isFinite))throw new Error('INVALID_CAMERA_DELTA');
 return {target:[clamp(c.target[0]+panX,-110,110),c.target[1],clamp(c.target[2]+panZ,-110,110)],distance:clamp(c.distance+zoom,12,280),yaw:c.yaw+yaw,pitch:clamp(c.pitch+pitch,.2,1.48)};
}
export function modeCamera(mode,target=[0,0,0]){
 const settings={AERIAL:[166,.93,.05],OVERHEAD:[202,1.48,0],PANORAMIC:[180,.38,.18],GROUND:[24,.28,.12]};
 if(!settings[mode])throw new Error('UNKNOWN_VIEW');const [distance,pitch,yaw]=settings[mode];return {target:[...target],distance,pitch,yaw};
}
export function locationCamera(bindings,id){const p=bindings.find(p=>p.id===id);if(!p)throw new Error('UNKNOWN_LOCATION');return {...modeCamera('GROUND',p.anchor),distance:30,pitch:.65};}
export function illustrativeLight(hour){if(!Number.isFinite(hour)||hour<0||hour>=24)throw new Error('INVALID_HOUR');const day=Math.max(0,Math.sin((hour-6)/12*Math.PI));return {strength:.32+day*.68,direction:[-.65,.25+day*.9,.25],solarModel:'ILLUSTRATIVE_NOT_ASTRONOMICAL'};}
export function previewMetadata(c){return {sourceRevision:c.sourceRevision,sourceStateAsOf:c.stateAsOf,publicationAuthorized:false,visualAcceptance:'NOT_REVIEWED',weatherSource:'NOT_CONNECTED',geometry:'PROCEDURAL_SPATIAL_STUDY_NOT_CANONICAL_GEOMETRY',inhabitants:'NOT_IMPLEMENTED'};}
