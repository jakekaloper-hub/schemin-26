/** Observer-only presentation state. No network, rendering, world writes, or canon authority. */
const ACTIVE=new Set(['PERMANENT_CANON','PROVISIONAL_CANON','INTERPRETIVE_CANON']);
const CAMERAS=new Set(['AERIAL','OVERHEAD','PANORAMIC','GROUND']);
const check=(ok,message)=>{if(!ok)throw new Error(message);};
const text=x=>typeof x==='string'&&x.trim().length>0;
function unique(values,label){
  check(Array.isArray(values)&&values.every(text),`INVALID_${label}`);
  check(new Set(values).size===values.length,`DUPLICATE_${label}`);
  return [...values];
}

/** Project active Atlas records; a viewer's visits cannot hide existing places.
 * Canon status is preserved. This projection does not authorize public release.
 */
export function projectAtlas(locations,visitedIds=[]){
  check(Array.isArray(locations),'INVALID_LOCATIONS');
  const visited=new Set(unique(visitedIds,'VISITS'));
  const active=locations.filter(x=>x&&/^LOC-/.test(x.id)&&ACTIVE.has(x.canon_status));
  unique(active.map(x=>x.id),'LOCATIONS');
  return active.map(x=>{
    check(text(x.name)&&text(x.physical_zone_id),'INVALID_LOCATION_IDENTITY');
    check(Array.isArray(x.abstract_position)&&x.abstract_position.length===2&&x.abstract_position.every(Number.isFinite),'INVALID_POSITION');
    const owners=x.owner_character_ids??(x.owner_character_id?[x.owner_character_id]:[]);
    return {
      id:x.id,name:x.name,canonStatus:x.canon_status,zoneId:x.physical_zone_id,
      position:[...x.abstract_position],ownerIds:unique(owners,'OWNERS'),
      landmarks:unique(x.persistent_landmarks??[],'LANDMARKS'),
      visible:true,visited:visited.has(x.id),publicationAuthorized:false,
    };
  });
}

/** Critical assets are real load/decode/first-frame barriers supplied by the renderer.
 * This state machine cannot certify those tasks; it consumes their completion signals.
 */
export function createObserver({locationIds,criticalAssetIds,reducedMotion=false,returning=false}){
  const locations=unique(locationIds,'LOCATIONS');
  const assets=unique(criticalAssetIds,'CRITICAL_ASSETS');
  check(assets.length>0,'EMPTY_CRITICAL_ASSETS');
  check(locations.every(x=>/^LOC-/.test(x)),'INVALID_LOCATION_ID');
  check(typeof reducedMotion==='boolean'&&typeof returning==='boolean','INVALID_PREFERENCES');
  return {
    phase:'LOADING',locationIds:locations,criticalAssetIds:assets,readyAssets:[],failedAssets:[],
    reducedMotion,returning,labels:'NONE',cameraMode:'AERIAL',locationId:null,visitedIds:[],
    reader:null,inputOwner:'WORLD',avatar:null,inhabitantInteractionAllowed:false,worldMutationAllowed:false,
  };
}

/** Pure transitions. Unknown actions fail rather than adding new visitor powers. */
export function transitionObserver(state,action){
  check(state&&action&&text(action.type),'INVALID_TRANSITION');
  const next=structuredClone(state);
  const worldInput=()=>check(next.phase==='EXPLORING'&&next.inputOwner==='WORLD','INPUT_OWNER_NOT_WORLD');
  switch(action.type){
    case 'asset_ready':
    case 'asset_failed': {
      check(next.criticalAssetIds.includes(action.id),'UNKNOWN_ASSET');
      check(['LOADING','FALLBACK'].includes(next.phase),'ASSET_SIGNAL_OUTSIDE_LOADING');
      if(next.phase==='FALLBACK')return next;
      if(action.type==='asset_failed'){
        next.failedAssets.push(action.id);next.phase='FALLBACK';return next;
      }
      if(!next.readyAssets.includes(action.id))next.readyAssets.push(action.id);
      if(next.readyAssets.length===next.criticalAssetIds.length){
        next.phase=next.reducedMotion||next.returning?'EXPLORING':'REVEALING';
      }
      return next;
    }
    case 'retry':
      check(next.phase==='FALLBACK','RETRY_OUTSIDE_FALLBACK');
      return createObserver({locationIds:next.locationIds,criticalAssetIds:next.criticalAssetIds,reducedMotion:next.reducedMotion,returning:next.returning});
    case 'reveal_finished':
    case 'skip_reveal':
      check(next.phase==='REVEALING','NOT_REVEALING');next.phase='EXPLORING';return next;
    case 'inspect':
      worldInput();check(next.locationIds.includes(action.id),'UNKNOWN_LOCATION');
      next.locationId=action.id;next.labels='ON_INSPECTION';
      if(!next.visitedIds.includes(action.id))next.visitedIds.push(action.id);
      return next;
    case 'world_view':
      worldInput();next.locationId=null;next.labels='NONE';next.cameraMode='AERIAL';return next;
    case 'camera':
      worldInput();check(CAMERAS.has(action.mode),'INVALID_CAMERA');next.cameraMode=action.mode;return next;
    case 'open_reader':
      worldInput();check(action.eligible===true&&text(action.publicationId),'PUBLICATION_NOT_ELIGIBLE');
      next.reader=action.publicationId;next.inputOwner='READER';return next;
    case 'close_reader':
      check(next.inputOwner==='READER','NO_READER_OPEN');next.reader=null;next.inputOwner='WORLD';return next;
    default:
      throw new Error(`ACTION_NOT_ALLOWED:${action.type}`);
  }
}
