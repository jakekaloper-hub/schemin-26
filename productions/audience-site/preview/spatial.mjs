/** Preview-only spatial interpretation. Source IDs/XY remain upstream; relief is not canon. */
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
export function atlasToScene(p){if(!Array.isArray(p)||p.length!==2||!p.every(Number.isFinite))throw new Error('INVALID_ATLAS_POSITION');return [(p[0]-50)*2,0,(50-p[1])*2];}
export function spatialBindings(catalog){
 if(!catalog||!Array.isArray(catalog.locations))throw new Error('MISSING_ATLAS');
 const seen=new Set();return catalog.locations.map(p=>{if(!/^LOC-/.test(p.id)||seen.has(p.id))throw new Error('INVALID_OR_DUPLICATE_LOCATION');seen.add(p.id);return {...structuredClone(p),anchor:atlasToScene(p.position),visible:true};});
}
export function defaultCamera(){return {target:[0,0,0],distance:280,yaw:-.23,pitch:.78};}
/** Rebase a navigation destination onto the nearest equivalent yaw.
 * This is applied ONLY on a place/world/view transition, never to user drag:
 * an intentional multi-turn orbit must not have its pointer movement discarded.
 * A source-bound view transform does not alter place coordinates or identity.
 */
export function shortestCameraYawArc(from,to){
 if(!Number.isFinite(from)||!Number.isFinite(to))throw Error('INVALID_CAMERA_YAW');
 const turn=Math.PI*2,raw=to-from;
 const arc=((raw+Math.PI)%turn+turn)%turn-Math.PI;
 return arc===-Math.PI&&raw>0?Math.PI:arc;
}
export function nearestObserverViewYaw(current,desired){
 const valid=c=>c&&Array.isArray(c.target)&&c.target.length===3&&
  [c.distance,c.pitch,c.yaw,...c.target].every(Number.isFinite);
 if(!valid(current)||!valid(desired))throw Error('INVALID_CAMERA_VIEW');
 const difference=desired.yaw-current.yaw;
 return {...desired,yaw:Math.abs(difference)<=Math.PI?desired.yaw:current.yaw+shortestCameraYawArc(current.yaw,desired.yaw),target:[...desired.target]};
}
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

/** Source-anchor-only regional view; never filters or repositions Atlas places. */
export function regionOverviewCamera(bindings,zoneId,aspect=16/9){
  if(!Array.isArray(bindings)||typeof zoneId!=='string'||!zoneId||!Number.isFinite(aspect)||aspect<=0)throw Error('INVALID_REGIONAL_VIEW');
  const points=bindings.filter(p=>p.zoneId===zoneId);
  if(!points.length)throw Error('UNKNOWN_REGION');
  if(points.some(p=>!Array.isArray(p.anchor)||p.anchor.length!==3||!p.anchor.every(Number.isFinite)))throw Error('INVALID_REGIONAL_ANCHOR');
  const xs=points.map(p=>p.anchor[0]),zs=points.map(p=>p.anchor[2]);
  const target=[(Math.min(...xs)+Math.max(...xs))/2,4,(Math.min(...zs)+Math.max(...zs))/2],yaw=.15,pitch=.88;
  const right=[Math.cos(yaw),0,-Math.sin(yaw)];
  const up=[-Math.sin(yaw)*Math.sin(pitch),Math.cos(pitch),-Math.cos(yaw)*Math.sin(pitch)];
  const approach=[Math.sin(yaw)*Math.cos(pitch),Math.sin(pitch),Math.cos(yaw)*Math.cos(pitch)];
  const dot=(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
  let horizontal=0,vertical=0,depth=0;
  for(const p of points){
    const offset=p.anchor.map((v,i)=>v-target[i]);
    horizontal=Math.max(horizontal,Math.abs(dot(offset,right)));
    vertical=Math.max(vertical,Math.abs(dot(offset,up)));
    depth=Math.max(depth,Math.abs(dot(offset,approach)));
  }
  // Match the existing Three/fallback 41.25-degree perspective and responsive
  // camera fit. Margins cover candidate structures, not new physical topology.
  const halfFov=Math.tan(41.25*Math.PI/360);
  const required=Math.max((horizontal+16)/(halfFov*aspect),(vertical+12)/halfFov)+depth+10;
  const widthFit=Math.max(1,1.25/aspect),nearFit=Math.min(widthFit,1.25);
  // Both existing renderers switch fit at distance >100; invert that exact
  // rule so portrait views never crop the inherited anchor envelope.
  const distance=required<=100*nearFit?required/nearFit:Math.max(100.01,required/widthFit);
  if(!Number.isFinite(distance)||distance>280)throw Error('REGION_OUTSIDE_CAMERA_BUDGET');
  return {target,distance:Math.max(12,distance),yaw,pitch};
}
