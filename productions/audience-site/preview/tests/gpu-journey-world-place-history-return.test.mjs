import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {join} from 'node:path';
import {createHash} from 'node:crypto';
const dir=new URL('../evidence/gpu-journey-world-place-history-return-20261123/',import.meta.url);
const read=(name)=>readFileSync(new URL(name,dir));
const manifest=JSON.parse(read('manifest.json'));
const stageOrder=['WORLD','PLACE','HISTORY','SAME_PLACE_RETURN','WORLD_RETURN','CALM_WATERFALL'];
const originals=['01-unlabeled-world.png','02-country-club-jackson.png','03-recorded-jackson-history.png',
 '04-return-same-jackson-view.png','05-return-unlabeled-world.png','06-waterfall-temple-global-calm.png'];
test('hardware evidence pins exact pre-commit source and unpublished safety boundaries',()=>{
 assert.equal(manifest.sourceSha,'60fcbfd1d3ec8c835cb307ff22f6ae5e8f03f89c');
 assert.equal(manifest.kind,'UNPUBLISHED_REAL_GPU_JOURNEY_EVIDENCE');
 assert.equal(manifest.sourceStateAsOf,'end_of_week_3_2026');
 assert.equal(manifest.publicationAuthorized,false);
 assert.equal(manifest.originalMemoImages,0);
 assert.equal(manifest.visualAcceptance,'NOT_REVIEWED');
 assert.equal(manifest.atlasLocations,23);
 assert.match(manifest.gpu,/ANGLE Metal Renderer: Apple M3 Pro/);
 assert.doesNotMatch(manifest.gpu,/Software Rasterizer|SwiftShader|llvmpipe/i);
 assert.deepEqual(manifest.externalRequests,[]);
 assert.deepEqual(manifest.errors,[]);
});
test('six genuine PNGs retain exact dimensions and independently checked content hashes',()=>{
 assert.deepEqual(manifest.stages.map(stage=>stage.stage),stageOrder);
 assert.deepEqual(manifest.stages.map(stage=>stage.file),originals);
 for(const stage of manifest.stages){
  const bytes=read(stage.file);
  assert.equal(bytes.subarray(0,8).toString('hex'),'89504e470d0a1a0a');
  assert.equal(bytes.readUInt32BE(16),stage.width);
  assert.equal(bytes.readUInt32BE(20),stage.height);
  assert.equal(stage.width,1440);assert.equal(stage.height,813);
  assert.equal(createHash('sha256').update(bytes).digest('hex'),stage.sha256);
 }
 assert.equal(new Set(manifest.stages.map(s=>s.sha256)).size,6,'all stages should be independently captured');
});
test('real journey preserved recorded Jackson camera, current atlas and history isolation',()=>{
 assert.equal(manifest.historyLocationId,'LOC-COUNTRY-CLUB-JACKSON');
 assert.ok(manifest.historyEntryCount>=1);
 assert.equal(manifest.historyCameraPreserved,true);
 assert.equal(manifest.historyWaterPaused,true);
 assert.equal(manifest.preHistoryWaterAdvanced,true);
 assert.equal(manifest.resumedWaterAfterHistory,true);
 assert.ok(manifest.stages[1].waterTime>0);
 assert.ok(manifest.stages[2].waterTime>=manifest.stages[1].waterTime);
 assert.ok(manifest.historyPausedWaterSampleStart>0);
 assert.equal(manifest.historyPausedWaterSampleStart,manifest.historyPausedWaterSampleEnd);
 assert.equal(manifest.stages[2].waterTime,manifest.historyPausedWaterSampleEnd);
 assert.ok(manifest.stages[3].waterTime>manifest.stages[2].waterTime);
 assert.deepEqual(manifest.stages.map(s=>s.locationId),[
  null,'LOC-COUNTRY-CLUB-JACKSON','LOC-COUNTRY-CLUB-JACKSON',
  'LOC-COUNTRY-CLUB-JACKSON',null,'LOC-TDS-WATERFALL-TEMPLE']);
 const before=manifest.stages[1].camera,after=manifest.stages[3].camera;
 for(const key of ['distance','yaw','pitch'])
  assert.ok(Math.abs(before[key]-after[key])<=0.003,'camera changed: '+key);
 for(let i=0;i<3;i++)assert.ok(Math.abs(before.target[i]-after.target[i])<=0.003,'target changed');
 assert.equal(manifest.elNinoSyntheticLossStatus,'GLOBAL_CALM');
 assert.deepEqual(manifest.stormZonesDuringCalm,[]);
 assert.equal(manifest.ordinaryWaterAdvancedDuringCalm,true);
});
test('offline artifact renders a keyboard-operable stage inspection with no remote resources',()=>{
 const html=read('inspection.html').toString('utf8');
 assert.equal((html.match(/data-step="\d"/g)||[]).length,6);
 assert.match(html,/ArrowLeft/);assert.match(html,/ArrowRight/);
 assert.match(html,/aria-current/);assert.match(html,/manifest\.json/);
 for(const name of originals)assert.ok(html.includes(name),'missing offline capture link '+name);
 assert.doesNotMatch(html,/<script[^>]+src=/i);
 assert.doesNotMatch(html,/<(?:link|img|script)[^>]+(?:src|href)=["']https?:/i);
 assert.match(html,/not a published visitor site/);
});

