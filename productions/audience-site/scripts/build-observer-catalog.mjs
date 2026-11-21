#!/usr/bin/env node
/** Private derived observer catalog. Reads World Engine; never writes world or publication data. */
import {readFileSync,mkdirSync,writeFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {resolve,dirname} from 'node:path';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {projectAtlas} from '../src/observer-world.mjs';
const check=(ok,error)=>{if(!ok)throw new Error(error);};
const strings=x=>Array.isArray(x)&&x.length>0&&x.every(s=>typeof s==='string'&&s.length>0);

/** Project historical World Memory as read-only candidate records. Never infer current state. */
export function projectLocationHistory(worldMemory,locations){
  if(worldMemory===undefined)return {status:'NOT_CONNECTED',publicationAuthorized:false,events:[]};
  check(worldMemory?.status==='RELEASE_CANDIDATE'&&Array.isArray(worldMemory.events),'HISTORY_AUTHORITY_INVALID');
  const known=new Set(locations.map(p=>p.id)),seen=new Set();
  const cleanStrings=(values,error)=>{check(Array.isArray(values)&&values.every(v=>typeof v==='string'&&v.trim().length>0),error);return [...values];};
  const events=worldMemory.events.map(e=>{
    check(e&&typeof e.event_id==='string'&&/^EVT-[A-Z0-9-]+$/.test(e.event_id),'INVALID_HISTORY_ID');
    check(!seen.has(e.event_id),'DUPLICATE_HISTORY_ID');seen.add(e.event_id);
    check(known.has(e.location),'UNKNOWN_HISTORY_LOCATION');
    check(e.memory_class==='HISTORICAL'&&Number.isInteger(e.week)&&e.week>0&&/^\d{4}$/.test(e.era),'INVALID_HISTORY_PERIOD');
    const sourceReceipts=cleanStrings(e.source,'INVALID_HISTORY_RECEIPT');
    check(sourceReceipts.length>0&&sourceReceipts.every(p=>/^[A-Za-z0-9_./-]+$/.test(p)&&!p.split('/').includes('..')&&!p.startsWith('/')),'INVALID_HISTORY_RECEIPT');
    check(typeof e.current_relevance==='boolean'&&(e.expiry_condition===null||typeof e.expiry_condition==='string')&&(e.superseded_by===null||typeof e.superseded_by==='string'),'INVALID_HISTORY_QUALIFIER');
    return {
      id:e.event_id,locationId:e.location,year:Number(e.era),week:e.week,memoryClass:e.memory_class,
      tags:cleanStrings(e.secondary_tags,'INVALID_HISTORY_TAGS'),
      effects:{physical:cleanStrings(e.physical_effect,'INVALID_HISTORY_EFFECT'),social:cleanStrings(e.social_effect,'INVALID_HISTORY_EFFECT'),reputation:cleanStrings(e.reputation_effect,'INVALID_HISTORY_EFFECT'),institutional:cleanStrings(e.institutional_effect,'INVALID_HISTORY_EFFECT')},
      sourceReceipts,currentRelevanceAtSource:e.current_relevance,expiryCondition:e.expiry_condition,supersededBy:e.superseded_by,
      publicationAuthorized:false,sourceStatus:'RELEASE_CANDIDATE',
    };
  });
  return {status:'RELEASE_CANDIDATE',source:'world/data/world_memory.json',publicationAuthorized:false,events};
}

export function buildObserverCatalog({locations,weatherRegions,worldState,worldMemory,revision}){
  check(typeof revision==='string'&&/^[a-f0-9]{40}$/.test(revision),'EXACT_SOURCE_REVISION_REQUIRED');
  check(typeof worldState?.as_of==='string'&&worldState.as_of.length>0,'WORLD_STATE_AS_OF_REQUIRED');
  check(typeof locations?.coordinate_space==='string','COORDINATE_SPACE_REQUIRED');
  check(Array.isArray(weatherRegions?.weather_regions),'WEATHER_REGIONS_REQUIRED');
  const ids=new Set();
  const regions=weatherRegions.weather_regions.map(r=>{
    check(r&&typeof r.id==='string'&&r.id.startsWith('WX-'),'WEATHER_ID_REQUIRED');
    check(!ids.has(r.id),'DUPLICATE_WEATHER_ID');ids.add(r.id);
    check(strings(r.propagation_order)&&r.propagation_order.every(x=>x.startsWith('REG-'))&&new Set(r.propagation_order).size===r.propagation_order.length,'WEATHER_ORDER_REQUIRED');
    check(strings(r.source_zone_ids)&&r.source_zone_ids.every(x=>r.propagation_order.includes(x)),'WEATHER_SOURCE_ZONE_REQUIRED');
    return {id:r.id,source_zone_ids:[...r.source_zone_ids],propagation_order:[...r.propagation_order]};
  });
  const projected=projectAtlas(locations.locations);
  return {
    schemaVersion:1,authority:'DERIVED_PRESENTATION_ONLY',sourceRevision:revision,
    stateAsOf:worldState.as_of,coordinateSpace:locations.coordinate_space,
    locations:projected,weatherRegions:regions,history:projectLocationHistory(worldMemory,projected),
    observer:{avatar:null,worldMutationAllowed:false,inhabitantInteractionAllowed:false,unvisitedLocationsVisible:true,openingLabels:'NONE'},
    worldClock:{timeZone:'America/New_York',solarModel:'NOT_CONNECTED'},
    renderReady:false,publicationAuthorized:false,runtimeIntegration:'NOT_MOUNTED',
    liveResultAdapter:'NOT_CONNECTED',baselineWeatherAdapter:'NOT_CONNECTED',
    missingRenderPrerequisites:['APPROVED_WORLD_COMPOSITION','RENDERER_ASSET_READINESS_ADAPTER','WORLD_CAMERA_GEOMETRY','CURRENT_WORLD_STATE_RECONCILIATION'],
  };
}

export function buildFromRepository(root,output){
  const paths={locations:'world/data/locations.json',weatherRegions:'world/data/weather_regions.json',worldState:'world/data/current_world_state.json',worldMemory:'world/data/world_memory.json'};
  const input={},hashes={};
  for(const [key,path]of Object.entries(paths)){
    const bytes=readFileSync(resolve(root,path));input[key]=JSON.parse(bytes.toString('utf8'));
    hashes[path]=createHash('sha256').update(bytes).digest('hex');
  }
  const revision=execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim();
  const data={...buildObserverCatalog({...input,revision}),sourceHashes:hashes};
  const bytes=JSON.stringify(data,null,2)+'\n';
  if(output){mkdirSync(dirname(output),{recursive:true});writeFileSync(output,bytes);}
  return data;
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){
  const root=fileURLToPath(new URL('../../../',import.meta.url));
  const output=resolve(root,process.argv[2]??'productions/audience-site/dist/observer-candidate.json');
  const data=buildFromRepository(root,output);
  console.log(JSON.stringify({state:'OBSERVER_CATALOG_BUILT',locations:data.locations.length,weatherRegions:data.weatherRegions.length,stateAsOf:data.stateAsOf,renderReady:data.renderReady,sourceRevision:data.sourceRevision,output}));
}
