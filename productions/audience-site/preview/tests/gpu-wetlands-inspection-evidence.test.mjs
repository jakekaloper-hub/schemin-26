import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { join } from 'node:path';

const evidenceDir=fileURLToPath(new URL('../evidence/gpu-wetlands-temporal-20261122/',import.meta.url));
const manifest=JSON.parse(readFileSync(join(evidenceDir,'manifest.json'),'utf8'));
const html=readFileSync(join(evidenceDir,'inspection.html'),'utf8');
const sourceRevision='3c2acb6cf58b33d977f7220fe15b2b82182a54c0';
const places=['LOC-COUNTRY-CLUB-JACKSON','LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP'];

test('physical-GPU Wetlands evidence is pinned to a source revision and denies publication authority',()=>{
 assert.equal(manifest.sourceRevision,sourceRevision);
 assert.equal(manifest.status,'CANDIDATE_NOT_APPROVED');
 assert.equal(manifest.publicationAuthorized,false);
 assert.equal(manifest.renderer,'three-webgl2');
 assert.match(manifest.gpu,/Apple M3 Pro/);
 assert.doesNotMatch(manifest.gpu,/SwiftShader|Software Rasterizer|llvmpipe/i);
 assert.equal(manifest.weatherStatus,'GLOBAL_CALM');
 assert.equal(manifest.ordinaryWaterAdvanced,true);
 assert.equal(manifest.cameraViewHeld,true);
 assert.equal(manifest.pausedSceneHashesEqual,true);
 assert.equal(manifest.sourceUnchanged,true);
 assert.deepEqual(manifest.sites.map(site=>site.placeId),places);
 assert.equal(manifest.captures.length,12);
});

test('all 12 original hardware screenshot bytes match their manifest SHA-256 and 1440x813 PNG dimensions',()=>{
 const captures=manifest.captures;
 const names=new Set(captures.map(cap=>cap.file));
 assert.equal(names.size,12);
 const actual=readdirSync(evidenceDir).filter(name=>name.endsWith('.png'));
 assert.deepEqual(actual.sort(),[...names].sort());
 for(const cap of captures){
  assert.match(cap.file,/^(jackson|temple|mud-dogs)-0[1-4]-(moving|paused-a|paused-b)\.png$/);
  assert.ok(places.includes(cap.placeId));
  const bytes=readFileSync(join(evidenceDir,cap.file));
  assert.equal(bytes.subarray(0,8).toString('hex'),'89504e470d0a1a0a');
  assert.equal(bytes.readUInt32BE(16),1440);
  assert.equal(bytes.readUInt32BE(20),813);
  assert.equal(bytes.length,cap.bytes);
  assert.equal(createHash('sha256').update(bytes).digest('hex'),cap.sha256);
 }
});

test('each source place has advancing moving clocks and exact duplicated paused screenshot bytes',()=>{
 for(const placeId of places){
  const records=manifest.captures.filter(record=>record.placeId===placeId);
  assert.equal(records.length,4);
  assert.deepEqual(records.map(record=>record.motionState),['MOVING','MOVING','PAUSED','PAUSED']);
  assert.ok(records[1].waterTime>records[0].waterTime+0.2);
  assert.notEqual(records[0].sha256,records[1].sha256);
  assert.equal(records[2].waterTime,records[3].waterTime);
  assert.equal(records[2].sha256,records[3].sha256);
  assert.equal(records[0].width,records[2].width);
  assert.equal(records[0].height,records[2].height);
  assert.equal(manifest.sites.find(site=>site.placeId===placeId).pausedSceneHashesEqual,true);
  assert.equal(manifest.sites.find(site=>site.placeId===placeId).movingSceneChanged,true);
 }
});

test('offline inspection HTML references exactly those 12 images and offers working local compare controls',()=>{
 assert.ok(html.includes(sourceRevision));
 for(const placeId of places)assert.ok(html.includes('data-site="'+placeId+'"'));
 const imageNames=[...html.matchAll(/<img src="([^"]+\.png)"/g)].map(match=>match[1]);
 assert.deepEqual(imageNames.sort(),manifest.captures.map(cap=>cap.file).sort());
 assert.equal((html.match(/data-compare/g)||[]).length,7); // six figures plus the selector in the script
 assert.equal((html.match(/class="diff"/g)||[]).length,6);
 assert.match(html,/Difference view/);
 assert.match(html,/CANDIDATE_NOT_APPROVED/);
 assert.match(html,/whole-scene motion/i);
 assert.match(html,/not independent water-only pixel attribution/i);
 assert.doesNotMatch(html,/<(?:script|link|iframe)[^>]+(?:src|href)="https?:/i);
 assert.doesNotMatch(html,/\b(?:fetch|XMLHttpRequest|sendBeacon)\s*\(/);
 const script=html.match(/<script>([\s\S]*?)<\/script>/)?.[1];
 assert.ok(script,'Missing inline comparison controller');
 assert.doesNotThrow(()=>new Function(script));
});
