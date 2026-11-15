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

export function buildObserverCatalog({locations,weatherRegions,worldState,revision}){
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
  return {
    schemaVersion:1,authority:'DERIVED_PRESENTATION_ONLY',sourceRevision:revision,
    stateAsOf:worldState.as_of,coordinateSpace:locations.coordinate_space,
    locations:projectAtlas(locations.locations),weatherRegions:regions,
    observer:{avatar:null,worldMutationAllowed:false,inhabitantInteractionAllowed:false,unvisitedLocationsVisible:true,openingLabels:'NONE'},
    worldClock:{timeZone:'America/New_York',solarModel:'NOT_CONNECTED'},
    renderReady:false,publicationAuthorized:false,runtimeIntegration:'NOT_MOUNTED',
    liveResultAdapter:'NOT_CONNECTED',baselineWeatherAdapter:'NOT_CONNECTED',
    missingRenderPrerequisites:['APPROVED_WORLD_COMPOSITION','RENDERER_ASSET_READINESS_ADAPTER','WORLD_CAMERA_GEOMETRY','CURRENT_WORLD_STATE_RECONCILIATION'],
  };
}

export function buildFromRepository(root,output){
  const paths={locations:'world/data/locations.json',weatherRegions:'world/data/weather_regions.json',worldState:'world/data/current_world_state.json'};
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
