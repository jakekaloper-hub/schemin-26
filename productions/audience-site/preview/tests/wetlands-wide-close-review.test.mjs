import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {createHash} from 'node:crypto';
const root=new URL('../evidence/',import.meta.url);
const original=new URL('gpu-wetlands-exact-0736e071-20261123/',root);
const closer=new URL('gpu-wetlands-closeup-20261123/',root);
const a=JSON.parse(readFileSync(new URL('manifest.json',original),'utf8'));
const b=JSON.parse(readFileSync(new URL('manifest.json',closer),'utf8'));
const page=readFileSync(new URL('gpu-wetlands-wide-close-review-20261123/inspection.html',root),'utf8');
const places=[['jackson','LOC-COUNTRY-CLUB-JACKSON'],['temple','LOC-TDS-WATERFALL-TEMPLE'],['mud-dogs','LOC-MUD-DOGS-SWAMP']];
const phases=['01-moving','02-moving','03-paused-a','04-paused-b'];
test('two distinct actual GPU recording sources retain historical/weather/publication firewalls',()=>{
 assert.equal(a.sourceRevision,'0736e071e4fcd3c70deea60e565293ccfde2230b');
 assert.equal(b.sourceRevision,'fb7a0091af71912e616fffb840c9deb6da1cb3b2');
 for(const m of [a,b]){assert.equal(m.status,'CANDIDATE_NOT_APPROVED');assert.equal(m.publicationAuthorized,false);assert.equal(m.renderer,'three-webgl2');assert.match(m.gpu,/Apple M3 Pro/);assert.equal(m.weatherStatus,'GLOBAL_CALM');assert.equal(m.ordinaryWaterAdvanced,true);assert.equal(m.pausedSceneHashesEqual,true);assert.equal(m.sourceUnchanged,true);assert.equal(m.captures.length,12);}
 assert.ok(page.includes(a.sourceRevision)&&page.includes(b.sourceRevision));
 assert.match(page,/independent recordings, not synchronized frames or pixel-registered viewpoints/i);
});
test('all 24 selectable source photos exist and match original immutable manifest SHA-256',()=>{
 for(const [slug,id] of places){const camera=b.closeupCameras.find(c=>c.placeId===id);assert.ok(camera&&camera.observedCloseupCamera.distance<camera.sourceCamera.distance*.9);
  assert.ok(page.includes('data-place="'+slug+'"'));
  for(const phase of phases)for(const [dir,m,file] of [[original,a,slug+'-'+phase+'.png'],[closer,b,slug+'-close-'+phase+'.png']]){
   const record=m.captures.find(c=>c.placeId===id&&c.file===file);assert.ok(record,'missing record '+file);
   const path=new URL(file,dir);assert.ok(existsSync(path),'missing image '+file);
   const bytes=readFileSync(path);assert.equal(bytes.length,record.bytes);
   assert.equal(bytes.readUInt32BE(16),1440);assert.equal(bytes.readUInt32BE(20),813);
   assert.equal(createHash('sha256').update(bytes).digest('hex'),record.sha256);
  }
 }
});
test('every original and closer site advances with ordinary time, then is pixel-identical under pause',()=>{
 for(const m of [a,b])for(const [,id] of places){const s=m.captures.filter(c=>c.placeId===id);
 assert.deepEqual(s.map(x=>x.motionState),['MOVING','MOVING','PAUSED','PAUSED']);
 assert.ok(s[1].waterTime>s[0].waterTime+.2);assert.notEqual(s[0].sha256,s[1].sha256);
 assert.equal(s[2].waterTime,s[3].waterTime);assert.equal(s[2].sha256,s[3].sha256);
 }
});
test('offline interactive viewer covers three places/four phases, no external scripts, no source writes',()=>{
 assert.equal((page.match(/data-place="/g)||[]).length,3);assert.equal((page.match(/data-frame="/g)||[]).length,4);
 for(const phase of phases)assert.ok(page.includes('data-frame="'+phase+'"'));
 assert.ok(page.includes("selectedPlace+'-close-'+selectedFrame+'.png'"));
 assert.ok(page.includes("selectedPlace+'-'+selectedFrame+'.png'"));
 assert.ok(page.includes("b.addEventListener('click'"));
 assert.ok(!/<(?:script|link|iframe)[^>]+(?:src|href)="https?:/i.test(page));
 assert.ok(!/\b(?:fetch|XMLHttpRequest|sendBeacon|WebSocket)\s*\(/.test(page));
 const script=page.match(/<script>([\s\S]*?)<\/script>/)?.[1];
 assert.ok(script);assert.doesNotThrow(()=>new Function(script));
});
