import test from 'node:test';
import assert from 'node:assert/strict';
import {existsSync} from 'node:fs';
const target=new URL('../scripts/build-observer-catalog.mjs',import.meta.url);
const api=existsSync(target)?await import(target.href):null;
const inputs=()=>({
 locations:{coordinate_space:'schemin-local-v1 (abstract, non-metric)',locations:[{id:'LOC-ONE',name:'One',canon_status:'PERMANENT_CANON',physical_zone_id:'REG-ONE',abstract_position:[1,2]}]},
 weatherRegions:{weather_regions:[{id:'WX-EASTERN-STORM',source_zone_ids:['REG-ONE'],propagation_order:['REG-ONE'],effects:['road washout']}]},
 worldState:{as_of:'end_of_week_3_2026',locations:{}},revision:'a'.repeat(40),
});
const build=(x=inputs())=>{assert.ok(api,'Observer catalog implementation is missing');return api.buildObserverCatalog(x);};
test('catalog derives existing IDs and preserves source as-of instead of claiming current world state',()=>{const c=build();assert.equal(c.locations.length,1);assert.equal(c.stateAsOf,'end_of_week_3_2026');assert.equal(c.sourceRevision,'a'.repeat(40));assert.equal(c.coordinateSpace,'schemin-local-v1 (abstract, non-metric)');});
test('catalog is deterministic, explicitly private/candidate and not render-ready',()=>{const a=build(),b=build();assert.deepEqual(a,b);assert.equal(a.authority,'DERIVED_PRESENTATION_ONLY');assert.equal(a.renderReady,false);assert.equal(a.publicationAuthorized,false);assert.equal(a.runtimeIntegration,'NOT_MOUNTED');});
test('catalog does not copy destructive weather consequences into render effects',()=>{const c=build();assert.equal(JSON.stringify(c).includes('road washout'),false);assert.deepEqual(c.weatherRegions[0].propagation_order,['REG-ONE']);});
test('missing world-state date and unknown commit revision are rejected',()=>{let x=inputs();delete x.worldState.as_of;assert.throws(()=>build(x),/STATE_AS_OF/);x=inputs();x.revision='main';assert.throws(()=>build(x),/REVISION/);});
test('catalog has no live weather or league result claims until adapters are attached',()=>{const c=build();assert.equal(c.liveResultAdapter,'NOT_CONNECTED');assert.equal(c.baselineWeatherAdapter,'NOT_CONNECTED');assert.ok(c.missingRenderPrerequisites.includes('APPROVED_WORLD_COMPOSITION'));});
test('duplicate weather regions and duplicate/empty propagation entries fail',()=>{let x=inputs();x.weatherRegions.weather_regions.push({...x.weatherRegions.weather_regions[0]});assert.throws(()=>build(x),/DUPLICATE_WEATHER/);x=inputs();x.weatherRegions.weather_regions[0].propagation_order=[];assert.throws(()=>build(x),/WEATHER_ORDER/);});
