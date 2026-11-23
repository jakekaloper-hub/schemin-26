import test from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFileSync,mkdtempSync,writeFileSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {spawnSync} from 'node:child_process';
import {WETLAND_TEMPORAL_SITES} from '../tools/temporal-evidence.mjs';

const tool=new URL('../tools/webgl2-journey-smoke.mjs',import.meta.url);
const evidence=new URL('../evidence/gpu-wetlands-closeup-20261123/',import.meta.url);
const source=readFileSync(tool,'utf8');
const run=args=>spawnSync(process.execPath,[tool.pathname,...args],{encoding:'utf8',timeout:10000});

test('closeup optical evidence refuses existing output directories before launching Chrome',()=>{
 const dir=mkdtempSync(join(tmpdir(),'wetlands-closeup-refuse-'));
 try{
  writeFileSync(join(dir,'keep.txt'),'preserve-me');
  const result=run(['/tmp/not-an-observer.html','--wetlands-closeup-dir',dir]);
  assert.notEqual(result.status,0);
  assert.match(result.stderr,/CLOSEUP_DIRECTORY_EXISTS/);
  assert.equal(readFileSync(join(dir,'keep.txt'),'utf8'),'preserve-me');
 }finally{rmSync(dir,{recursive:true,force:true});}
});
test('closeup mode remains mutually exclusive with prior capture modes and requires destination',()=>{
 const mixed=run(['/tmp/missing-observer.html','--wetlands-closeup-dir','/tmp/one','--wetlands-temporal-dir','/tmp/two']);
 assert.notEqual(mixed.status,0);
 assert.match(mixed.stderr,/Optional capture argument/);
 const missing=run(['/tmp/missing-observer.html','--wetlands-closeup-dir']);
 assert.notEqual(missing.status,0);
 assert.match(missing.stderr,/Optional capture argument/);
});
test('physical candidate uses spectator wheel, enforces held camera and preserves history/calm checks',()=>{
 assert.match(source,/Input\.dispatchMouseEvent/);
 assert.match(source,/type:'mouseWheel'/);
 assert.match(source,/close\.distance<before\.distance\*\.9/);
 assert.match(source,/assertHistoricalViewRestored\(close/);
 assert.match(source,/verifyWetlandsTemporalSequences\(wetlandCloseupCaptures\)/);
 assert.match(source,/PHYSICAL_GPU_THREE_SITE_CLOSE_PERSPECTIVE/);
 assert.match(source,/publicationAuthorized:false/);
 assert.match(source,/await click\('#openHistory'\)/);
 assert.match(source,/ordinary water continued during global weather calm/);
 assert.match(source,/assert\.deepEqual\(externalRequests,\[\]/);
});
test('retained three-site physical GPU closeups hash-match 12 PNGs, advance in motion and freeze on pause',()=>{
 const m=JSON.parse(readFileSync(new URL('manifest.json',evidence),'utf8'));
 assert.equal(m.sourceRevision,'fb7a0091af71912e616fffb840c9deb6da1cb3b2');
 assert.equal(m.status,'CANDIDATE_NOT_APPROVED');
 assert.equal(m.publicationAuthorized,false);
 assert.equal(m.weatherStatus,'GLOBAL_CALM');
 assert.equal(m.renderer,'three-webgl2');
 assert.match(m.gpu,/Apple M3 Pro/);
 assert.equal(m.allCurrentPlacesVisible,true);
 assert.equal(m.originalHistoryJourneyPassed,true);
 assert.equal(m.closeupCameras.length,WETLAND_TEMPORAL_SITES.length);
 assert.equal(m.captures.length,WETLAND_TEMPORAL_SITES.length*4);
 for(let i=0;i<WETLAND_TEMPORAL_SITES.length;i++){
  const place=WETLAND_TEMPORAL_SITES[i],shot=m.captures.slice(i*4,i*4+4);
  const camera=m.closeupCameras[i];
  assert.equal(camera.placeId,place.placeId);
  assert.ok(camera.observedCloseupCamera.distance<camera.sourceCamera.distance*.9);
  assert.ok(camera.observedCloseupCamera.distance>=5);
  assert.deepEqual(shot.map(c=>c.motionState),['MOVING','MOVING','PAUSED','PAUSED']);
  assert.ok(shot[1].waterTime>shot[0].waterTime+.2);
  assert.equal(shot[2].waterTime,shot[3].waterTime);
  assert.equal(m.sites[i].placeId,place.placeId);
  assert.equal(m.sites[i].movingSceneChanged,true);
  assert.equal(m.sites[i].pausedSceneHashesEqual,true);
  for(const c of shot){
   assert.equal(c.placeId,place.placeId);
   assert.match(c.file,/\.png$/);
   const bytes=readFileSync(new URL(c.file,evidence));
   assert.equal(bytes.length,c.bytes);
   assert.equal(createHash('sha256').update(bytes).digest('hex'),c.sha256);
   assert.equal(c.width,1440);assert.equal(c.height,813);
  }
  assert.notEqual(shot[0].sha256,shot[1].sha256);
  assert.equal(shot[2].sha256,shot[3].sha256);
 }
});
