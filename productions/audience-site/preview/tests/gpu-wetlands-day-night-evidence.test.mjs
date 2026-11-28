import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,readdirSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {join} from 'node:path';
import {decodeRgbPng,changedPixels} from '../tools/png-region-evidence.mjs';
const dir=fileURLToPath(new URL('../evidence/gpu-wetlands-day-night-20261124/',import.meta.url));
const m=JSON.parse(readFileSync(join(dir,'manifest.json'),'utf8'));
const sites=['LOC-COUNTRY-CLUB-JACKSON','LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP'];
test('clock comparison evidence is source-pinned, synthetic, and not publication or art authority',()=>{
 assert.equal(m.sourceRevision,'c3a94b76798c60712c2f7474ec3d8d1ab823eee5');
 assert.equal(m.status,'CANDIDATE_NOT_APPROVED');
 assert.equal(m.publicationAuthorized,false);
 assert.equal(m.renderer,'three-webgl2');
 assert.match(m.gpu,/Apple M3 Pro/);
 assert.equal(m.weatherStatus,'GLOBAL_CALM');
 for(const key of ['syntheticClock','cameraViewHeld','waterPhaseHeld','ordinaryWaterAdvanced','originalHistoryJourneyPassed','sourceUnchanged'])assert.equal(m[key],true);
 assert.equal(m.captures.length,6);
 assert.deepEqual([...new Set(m.captures.map(x=>x.placeId))],sites);
 assert.deepEqual(readdirSync(dir).filter(x=>x.endsWith('.png')).sort(),m.captures.map(x=>x.file).sort());
});
for(const placeId of sites)test(placeId+' synthetic noon and midnight render at the same camera and water phase with visible pixel contrast',()=>{
 const [day,night]=m.captures.filter(x=>x.placeId===placeId);
 assert.deepEqual([day.period,night.period],['noon','midnight']);
 assert.deepEqual([day.syntheticUtc,night.syntheticUtc],['2026-11-24T17:00:00.000Z','2026-11-24T05:00:00.000Z']);
 assert.deepEqual(day.camera,night.camera);
 assert.equal(day.waterTime,night.waterTime);
 assert.ok(night.frames>day.frames);
 const decoded=[day,night].map(x=>{
  const bytes=readFileSync(join(dir,x.file));
  assert.equal(bytes.length,x.bytes);
  assert.equal(createHash('sha256').update(bytes).digest('hex'),x.sha256);
  const image=decodeRgbPng(bytes);
  assert.equal(image.width,x.width);
  assert.equal(image.height,x.height);
  return image;
 });
 const [a,b]=decoded;
 const delta=changedPixels(a,b,[0,0,a.width,a.height],{minDelta:8});
 assert.ok(delta.changed/delta.total>.25,'Expected substantive whole-frame change');
 function mean(image){let total=0;for(let i=0;i<image.pixels.length;i+=image.channels)total+=.2126*image.pixels[i]+.7152*image.pixels[i+1]+.0722*image.pixels[i+2];return total/(image.width*image.height);}
 const light=mean(a),dark=mean(b);
 assert.ok(light>dark+15,'Expected nighttime whole-frame brightness reduction');
 console.log(JSON.stringify({placeId,changed:delta.changed,total:delta.total,noonMean:light,midnightMean:dark}));
});
