import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,statSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {join,dirname} from 'node:path';

const dir=fileURLToPath(new URL('../evidence/gpu-waterfall-motion-pause-20261121/',import.meta.url));
const html=readFileSync(join(dir,'inspection.html'),'utf8');
const manifest=JSON.parse(readFileSync(join(dir,'manifest.json'),'utf8'));
const names=['01-temple-global-calm.png','02-temple-global-calm.png','03-temple-paused-a.png','04-temple-paused-b.png'];
const source='1bb6f58935e610edd1c828a1996790cc3aa29e68';

test('read-only visual evidence pairs exactly the source-pinned physical-GPU PNGs',()=>{
 assert.equal(manifest.sourceRevision,source);
 assert.equal(manifest.placeId,'LOC-TDS-WATERFALL-TEMPLE');
 assert.equal(manifest.weatherStatus,'GLOBAL_CALM');
 assert.equal(manifest.publicationAuthorized,false);
 assert.deepEqual(manifest.captures.map(c=>c.file),names);
 assert.match(html,new RegExp('data-source-revision="'+source+'"'));
 const references=[...html.matchAll(/<img src="([^"]+)"[^>]*>/g)].map(x=>x[1]);
 assert.deepEqual(references,names,'no untracked image or remote substitution');
 for(const entry of manifest.captures){
  const buffer=readFileSync(join(dir,entry.file));
  assert.equal(buffer.length,entry.bytes,entry.file);
  assert.equal(createHash('sha256').update(buffer).digest('hex'),entry.sha256,entry.file);
  assert.equal(buffer.readUInt32BE(16),1440);assert.equal(buffer.readUInt32BE(20),813);
 }
 assert.equal(manifest.captures[0].motionState,'MOVING');
 assert.equal(manifest.captures[1].motionState,'MOVING');
 assert.ok(manifest.captures[1].waterTime>manifest.captures[0].waterTime);
 assert.notEqual(manifest.captures[0].sha256,manifest.captures[1].sha256);
 assert.equal(manifest.captures[2].motionState,'PAUSED');
 assert.equal(manifest.captures[3].motionState,'PAUSED');
 assert.equal(manifest.captures[2].waterTime,manifest.captures[3].waterTime);
 assert.equal(manifest.captures[2].sha256,manifest.captures[3].sha256);
});

test('offline inspection exposes paired interactive comparison and pixel-region provenance without publication or network',()=>{
 assert.match(html,/<figure data-comparison="moving">/);
 assert.match(html,/<figure data-comparison="paused">/);
 assert.match(html,/id="moving-wipe"/);
 assert.match(html,/id="paused-wipe"/);
 assert.equal((html.match(/data-difference aria-pressed="false"/g)||[]).length,2);
 assert.match(html,/marker\.style\.left=\(100\*x0\/1440\)/);
 assert.match(html,/marker\.style\.top=\(100\*y0\/813\)/);
 for(const region of ['575,360,603,442','551,469,609,494','730,565,784,621'])
  assert.ok(html.includes('['+region+']'),'source-image ROI must be marked: '+region);
 assert.match(html,/CANDIDATE_NOT_APPROVED/);
 assert.match(html,/publication not authorized/);
 assert.match(html,/FRAME UNAVAILABLE/);
 assert.match(html,/addEventListener\('error',failure\)/);
 assert.doesNotMatch(html,/\bfetch\s*\(|https?:\/\/|<iframe|<script[^>]+src=|XMLHttpRequest|localStorage|WebSocket|serviceWorker|writeWorld|createEvent/);
 assert.equal((html.match(/<script>/g)||[]).length,1);
 assert.equal((html.match(/<html lang="en">/g)||[]).length,1);
 assert.ok(statSync(join(dir,'inspection.html')).size<15000,'small no-dependency inspection artifact');
});
