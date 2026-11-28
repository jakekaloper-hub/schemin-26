import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import * as THREE from '../vendor/three.module.js';
import {createTerrainSurfaceTexture,createTerrainSurfaceNormalTexture,terrainSurfaceNormal} from '../three-world.mjs';

const source=readFileSync(new URL('../three-world.mjs',import.meta.url),'utf8');
const digest=data=>createHash('sha256').update(data).digest('hex');

test('normal relief is deterministic, bounded, neutral-space and owned by one disposable 128-square texture',()=>{
 const a=createTerrainSurfaceNormalTexture(THREE),b=createTerrainSurfaceNormalTexture(THREE);
 assert.equal(a.image.width,128);assert.equal(a.image.height,128);
 assert.equal(a.image.data.byteLength,65536);assert.equal(a.colorSpace,THREE.NoColorSpace);
 assert.equal(a.wrapS,THREE.RepeatWrapping);assert.equal(a.wrapT,THREE.RepeatWrapping);
 assert.equal(a.minFilter,THREE.LinearMipmapLinearFilter);assert.equal(a.magFilter,THREE.LinearFilter);
 assert.equal(a.generateMipmaps,true);assert.equal(a.anisotropy,4);
 assert.equal(digest(a.image.data),digest(b.image.data));
 assert.equal(digest(a.image.data),'fe3453e255c4ad06d042a9fe874dd9cb72f97d7ccbbc067c95c4a1caccc0d8d0','terrain normal relief source fingerprint');
 let deviation=0;
 for(let i=0;i<a.image.data.length;i+=4){
  const x=a.image.data[i]/127.5-1,y=a.image.data[i+1]/127.5-1,z=a.image.data[i+2]/127.5-1;
  const length=Math.hypot(x,y,z);
  assert.ok(Number.isFinite(length)&&Math.abs(length-1)<.015,'packed normal remains unit length');
  assert.ok(z>.78,'microrelief cannot invert ground orientation');
  assert.equal(a.image.data[i+3],255);
  deviation=Math.max(deviation,Math.abs(a.image.data[i]-128),Math.abs(a.image.data[i+1]-128));
 }
 assert.ok(deviation>6,'light-responsive relief is not a flat normal');
 assert.ok(deviation<80,'microrelief cannot overpower existing topography');
 assert.throws(()=>createTerrainSurfaceNormalTexture(THREE,31),/INVALID_TERRAIN_TEXTURE_SIZE/);
 assert.throws(()=>createTerrainSurfaceNormalTexture(THREE,128,0),/INVALID_TERRAIN_TILE_SIZE/);
 let released=0;a.addEventListener('dispose',()=>released++);a.dispose();b.dispose();assert.equal(released,1);
});

test('normal derivatives respect physical atlas XZ tile scale and seamless periodic texture sampling',()=>{
 for(const [u,v] of [[.121,.314],[.77,.61],[.025,.93]]){
  const a=terrainSurfaceNormal(u,v),b=terrainSurfaceNormal(u+1,v+1);
  assert.ok(a.every((component,i)=>Math.abs(component-b[i])<1e-9),'periodic terrain tangent is identical at each repeated tile');
  assert.ok(Math.abs(Math.hypot(...a)-1)<1e-12);
  const smallerSlope=terrainSurfaceNormal(u,v,128,128);
  assert.ok(Math.hypot(smallerSlope[0],smallerSlope[1])<=Math.hypot(a[0],a[1]),'doubling world tile scale cannot intensify normal slope');
 }
 const size=128,x=35,y=83,uv=[(x+.5)/size,(y+.5)/size];
 const expected=terrainSurfaceNormal(...uv,size,64);
 const data=createTerrainSurfaceNormalTexture(THREE,size).image.data;
 const i=(y*size+x)*4;
 for(let c=0;c<3;c++)assert.ok(Math.abs(data[i+c]/127.5-1-expected[c])<=1/127.5);
 assert.throws(()=>terrainSurfaceNormal(Infinity,.5),/INVALID_TERRAIN_NORMAL_SAMPLE/);
 assert.throws(()=>terrainSurfaceNormal(.5,.5,128,-1),/INVALID_TERRAIN_NORMAL_SAMPLE/);
});

test('one existing terrain mesh receives relief without rewriting geography, old albedo, water clocks or site history',()=>{
 assert.match(source,/const terrainNormalTexture=createTerrainSurfaceNormalTexture\(THREE\);/);
 assert.match(source,/normalMap:terrainNormalTexture,normalScale:new THREE\.Vector2\(\.7,\.7\)/);
 assert.match(source,/terrainMaterial\.dispose\(\);terrainTexture\.dispose\(\);terrainNormalTexture\.dispose\(\)/);
 assert.match(source,/applyTerrainPlanarUVs\(THREE,geometry\);/);
 assert.match(source,/const oceanMaterial=createBaseWaterMaterial\(THREE,shorelineTexture\);/);
 assert.match(source,/if\(!paused\)lastTime=time;regional\.tick\(lastTime,\{paused\}\)/);
 assert.doesNotMatch(createTerrainSurfaceNormalTexture.toString(),/Math\.random|fetch\(|Date\.now|uStorm|worldState|canonical/);
 const albedo=createTerrainSurfaceTexture(THREE);
 assert.equal(digest(albedo.image.data),'72a989844aa9964a14c577d617838461a699c1ac4a71f7f87654b02dbb4fa058','the prior validated terrain albedo remains untouched');
 albedo.dispose();
});
