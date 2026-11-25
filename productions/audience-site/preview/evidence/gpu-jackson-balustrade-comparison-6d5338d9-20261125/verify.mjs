import assert from 'node:assert/strict';
import {readFileSync,writeFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {decodeRgbPng,changedPixels} from '../../tools/png-region-evidence.mjs';
const read=p=>readFileSync(new URL(p,import.meta.url));
const hash=b=>createHash('sha256').update(b).digest('hex');
const before=JSON.parse(read('before/manifest.json')),after=JSON.parse(read('after/manifest.json'));
assert.equal(before.sourceSha,'22b37d6f583cbcbf7358a409716c6bfc133a8e1b');
assert.equal(after.sourceSha,'6d5338d90c090050ffa18d71cddb126c79759f51');
assert.equal(after.observerSha256,'1c40d133bef8b2032b7f16e50ac276fec6274aa88e8f0c86cef983af2dfc7868');
for(const m of [before,after]){
 assert.equal(m.preset,'jackson');assert.equal(m.atlasLocations,23);
 assert.equal(m.sourceStateAsOf,'end_of_week_3_2026');
 assert.equal(m.publicationAuthorized,false);assert.equal(m.visualAcceptance,'NOT_REVIEWED');
 assert.equal(m.weather,'SYNTHETIC_GLOBAL_CALM');
 assert.equal(m.browserErrors,0);assert.equal(m.externalRequests,0);
 assert.match(m.gpu,/Apple M3 Pro/);assert.equal(m.frames.length,4);
}
for(const key of ['gpu','syntheticUtc','sourceStateAsOf','weather'])assert.equal(before[key],after[key]);
const comparisons=[];
for(const [stage,distance] of [['standard',60],['closer',30]]){
 const images=[],frames=[];
 for(const [dir,m] of [['before',before],['after',after]]){
  const f=m.frames.find(x=>x.file===stage+'.png'),r=m.frames.find(x=>x.file===stage+'-repeat.png');
  assert.ok(f.retained&&!r.retained);
  assert.equal(f.sha256,r.sha256);assert.deepEqual(f.camera,r.camera);
  assert.equal(f.waterTime,0);assert.equal(r.waterTime,0);
  assert.equal(f.locationId,'LOC-COUNTRY-CLUB-JACKSON');assert.equal(f.camera.distance,distance);
  const b=read(dir+'/'+f.file);assert.equal(b.length,f.bytes);assert.equal(hash(b),f.sha256);
  const image=decodeRgbPng(b);assert.equal(image.width,1440);assert.equal(image.height,813);
  assert.equal(image.width,f.width);assert.equal(image.height,f.height);
  images.push(image);frames.push(f);
 }
 assert.deepEqual(frames[0].camera,frames[1].camera);
 const [a,b]=images;
 const delta=changedPixels(a,b,[0,0,a.width,a.height],{minDelta:2});
 assert.ok(delta.changed>0);
 let minX=a.width,minY=a.height,maxX=-1,maxY=-1;
 for(let y=0;y<a.height;y++)for(let x=0;x<a.width;x++){
  const i=(y*a.width+x)*a.channels;
  if([0,1,2].some(c=>Math.abs(a.pixels[i+c]-b.pixels[i+c])>=2)){
   minX=Math.min(minX,x);minY=Math.min(minY,y);maxX=Math.max(maxX,x);maxY=Math.max(maxY,y);
  }
 }
 comparisons.push({stage,camera:frames[0].camera,waterTime:0,...delta,
  changedFraction:delta.changed/delta.total,minimumRgbChannelDelta:2,
  changedPixelBounds:[minX,minY,maxX+1,maxY+1],
  scope:'Whole viewport; includes any induced shading changes, not an isolated bridge mask.'});
}
const result={kind:'CONTROLLED_PHYSICAL_GPU_JACKSON_BALUSTRADE_COMPARISON',status:'CANDIDATE_NOT_APPROVED',
 publicationAuthorized:false,baseline:before.sourceSha,refined:after.sourceSha,
 gpu:after.gpu,syntheticUtc:after.syntheticUtc,weather:after.weather,sourceStateAsOf:after.sourceStateAsOf,
 atlasLocations:23,sourceOnly:true,matchedCamera:true,matchedWaterPhase:true,stableRepeatPairs:4,
 browserErrors:0,externalRequests:0,
 captureToolSha256:hash(read('../../tools/temple-static-capture.mjs')),comparisons};
const serialized=JSON.stringify(result,null,2)+'\n';
if(process.argv.includes('--record'))writeFileSync(new URL('comparison.json',import.meta.url),serialized,{flag:'wx'});
else assert.equal(read('comparison.json').toString(),serialized,'COMPARISON_DRIFT');
console.log(serialized);
