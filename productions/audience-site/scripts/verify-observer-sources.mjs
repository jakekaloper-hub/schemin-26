#!/usr/bin/env node
/** Integration proof against the actual checked-out repository, never test-fabricated canon. */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {resolve} from 'node:path';
import {createHash} from 'node:crypto';
import {buildFromRepository} from './build-observer-catalog.mjs';
import {projectAtlas,createObserver,transitionObserver} from '../src/observer-world.mjs';
const root=fileURLToPath(new URL('../../../',import.meta.url));
const sourcePaths=['world/data/locations.json','world/data/weather_regions.json','world/data/current_world_state.json'];
const fingerprint=()=>sourcePaths.map(path=>createHash('sha256').update(readFileSync(resolve(root,path))).digest('hex'));
const before=fingerprint();
const a=buildFromRepository(root),b=buildFromRepository(root);
assert.deepEqual(a,b,'same source revision must produce identical catalog');
const raw=JSON.parse(readFileSync(resolve(root,sourcePaths[0]),'utf8'));
const allVisited=projectAtlas(raw.locations,a.locations.map(x=>x.id));
assert.deepEqual(a.locations.map(x=>x.id),allVisited.map(x=>x.id));
assert.equal(a.locations.length,raw.locations.length,'inspect rather than silently drop existing Atlas record');
assert.equal(new Set(a.locations.map(x=>x.id)).size,a.locations.length);
assert.ok(a.locations.some(x=>x.id==='LOC-COUNTRY-CLUB-JACKSON'));
assert.ok(a.weatherRegions.some(x=>x.id==='WX-EASTERN-STORM'));
const s=createObserver({locationIds:a.locations.map(x=>x.id),criticalAssetIds:['catalog','world-first-frame']});
const loading=transitionObserver(s,{type:'asset_ready',id:'catalog'});
assert.equal(loading.phase,'LOADING','catalog readiness alone is not rendered-world readiness');
assert.deepEqual(fingerprint(),before,'source files must remain byte-identical');
console.log(JSON.stringify({state:'OBSERVER_SOURCE_INTEGRATION_PASS',sourceRevision:a.sourceRevision,locations:a.locations.length,weatherRegions:a.weatherRegions.length,stateAsOf:a.stateAsOf,sourceFilesUnchanged:true,renderReady:a.renderReady,runtimeIntegration:a.runtimeIntegration}));
