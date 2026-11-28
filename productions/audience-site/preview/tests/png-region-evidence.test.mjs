import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {decodeRgbPng,changedPixels} from '../tools/png-region-evidence.mjs';

const evidence=new URL('../evidence/gpu-waterfall-motion-pause-20261121/',import.meta.url);
const manifest=JSON.parse(readFileSync(new URL('manifest.json',evidence),'utf8'));
const sha=bytes=>createHash('sha256').update(bytes).digest('hex');
const frames=manifest.captures.map(shot=>{
 const bytes=readFileSync(new URL(shot.file,evidence));
 assert.equal(sha(bytes),shot.sha256,'Manifest SHA mismatch for '+shot.file);
 assert.equal(bytes.length,shot.bytes,'Manifest byte count mismatch for '+shot.file);
 const decoded=decodeRgbPng(bytes);
 assert.deepEqual([decoded.width,decoded.height],[shot.width,shot.height]);
 return decoded;
});

// Coordinates measured on the retained 1440x813 source-bound Temple screenshots.
// The sheet region is fully inside the visible waterfall, the pool region catches
// the existing plunge basin. No assertion of physically segmented water pixels.
const SHEET=[575,360,604,443];
const PLUNGE=[551,469,610,495];
const STATIC_GROUND=[730,565,785,622];

test('source-pinned Temple captures show regional water changes, not camera/global frame drift',()=>{
 assert.equal(manifest.placeId,'LOC-TDS-WATERFALL-TEMPLE');
 assert.equal(manifest.weatherStatus,'GLOBAL_CALM');
 assert.equal(manifest.sourceRevision,'1bb6f58935e610edd1c828a1996790cc3aa29e68');
 assert.equal(manifest.sourceUnchanged,true);
 assert.equal(manifest.cameraViewHeld,true);
 assert.deepEqual(manifest.captures.map(x=>x.motionState),['MOVING','MOVING','PAUSED','PAUSED']);
 assert.ok(manifest.captures[1].waterTime>manifest.captures[0].waterTime);
 assert.equal(manifest.captures[2].waterTime,manifest.captures[3].waterTime);
 const sheet=changedPixels(frames[0],frames[1],SHEET);
 const plunge=changedPixels(frames[0],frames[1],PLUNGE);
 const staticGround=changedPixels(frames[0],frames[1],STATIC_GROUND);
 assert.ok(sheet.changed>=20,'No substantial falling-sheet-region motion: '+sheet.changed);
 assert.ok(plunge.changed>=20,'No substantial plunge-region motion: '+plunge.changed);
 assert.equal(staticGround.changed,0,'Static ground moved '+staticGround.changed+' pixels; camera stability unproven');
 assert.equal(changedPixels(frames[2],frames[3],SHEET).changed,0,'Waterfall region changed under explicit pause');
 assert.equal(changedPixels(frames[2],frames[3],PLUNGE).changed,0,'Plunge region changed under explicit pause');
});

test('region decoder rejects malformed, oversized and unsupported PNG inputs',()=>{
 assert.throws(()=>decodeRgbPng(Buffer.from('not-png')),/INVALID_PNG_SIGNATURE/);
 const image=Buffer.from([137,80,78,71,13,10,26,10,0,0,0,13,73,72,68,82,0,0,0,1,0,0,0,1,16,2,0,0,0,0,0,0,0]);
 assert.throws(()=>decodeRgbPng(image),/PNG_FORMAT_UNSUPPORTED/);
 assert.throws(()=>changedPixels(frames[0],frames[1],[-1,0,10,10]),/PIXEL_REGION_OUT_OF_BOUNDS/);
 assert.throws(()=>changedPixels(frames[0],frames[1],[0,0,1441,813]),/PIXEL_REGION_OUT_OF_BOUNDS/);
});
