import test from 'node:test';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {createTerrainSurfaceTexture,applyTerrainPlanarUVs} from '../three-world.mjs';

const source=readFileSync(new URL('../three-world.mjs',import.meta.url),'utf8');
const hash=b=>createHash('sha256').update(b).digest('hex');

test('reusable, deterministic atlas terrain detail uses one bounded, repeatable in-memory texture',()=>{
 const a=createTerrainSurfaceTexture(THREE),b=createTerrainSurfaceTexture(THREE);
 assert.ok(a.isDataTexture);assert.equal(a.image.width,128);assert.equal(a.image.height,128);
 assert.equal(a.image.data.byteLength,128*128*4);assert.equal(a.colorSpace,THREE.SRGBColorSpace);
 assert.equal(a.wrapS,THREE.RepeatWrapping);assert.equal(a.wrapT,THREE.RepeatWrapping);
 assert.equal(a.minFilter,THREE.LinearMipmapLinearFilter);assert.equal(a.magFilter,THREE.LinearFilter);
 assert.equal(a.generateMipmaps,true);assert.equal(a.anisotropy,4);
 assert.equal(hash(a.image.data),hash(b.image.data));
 assert.equal(hash(a.image.data),'72a989844aa9964a14c577d617838461a699c1ac4a71f7f87654b02dbb4fa058','source-controlled albedo fingerprint');
 for(let y=0;y<128;y++)for(let c=0;c<3;c++){
  const left=(y*128)*4+c,right=(y*128+127)*4+c;
  assert.ok(Math.abs(a.image.data[left]-a.image.data[right])<=4,'periodic tile has no harsh seam');
 }
 const channels=[];for(let i=0;i<a.image.data.length;i+=4){
  const rgba=a.image.data;assert.equal(rgba[i+3],255);
  for(let c=0;c<3;c++)assert.ok(rgba[i+c]>=170&&rgba[i+c]<=255,'albedo stays plausibly bounded');
  channels.push(rgba[i]);
 }
 assert.ok(Math.max(...channels)-Math.min(...channels)>20,'ground is more than one flat swatch');
 assert.throws(()=>createTerrainSurfaceTexture(THREE,31),/INVALID_TERRAIN_TEXTURE_SIZE/);
 assert.throws(()=>createTerrainSurfaceTexture(THREE,1024),/INVALID_TERRAIN_TEXTURE_SIZE/);
 let disposed=0;a.addEventListener('dispose',()=>disposed++);
 a.dispose();b.dispose();assert.equal(disposed,1);
});

test('UVs follow existing local XZ world positions, preserve source geometry and tile at fixed world scale',()=>{
 const geometry=new THREE.BufferGeometry();
 const positions=[0,2,0,32,6,-64,-128,10,192,64,2,64];
 geometry.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));
 geometry.setAttribute('normal',new THREE.Float32BufferAttribute([0,1,0,0,1,0,0,1,0,0,1,0],3));
 const before=Array.from(geometry.getAttribute('position').array);
 assert.equal(applyTerrainPlanarUVs(THREE,geometry),geometry);
 assert.deepEqual(Array.from(geometry.getAttribute('uv').array),[0,0,.5,-1,-2,3,1,1]);
 assert.deepEqual(Array.from(geometry.getAttribute('position').array),before);
 assert.deepEqual(Array.from(geometry.getAttribute('normal').array),[0,1,0,0,1,0,0,1,0,0,1,0]);
 assert.throws(()=>applyTerrainPlanarUVs(THREE,geometry,0),/INVALID_TERRAIN_TILE_SIZE/);
 geometry.dispose();
});

test('surface detail only extends existing terrain PBR; animated water and source-bound sites remain independent',()=>{
 assert.match(source,/applyTerrainPlanarUVs\(THREE,geometry\);/);
 assert.match(source,/const terrainTexture=createTerrainSurfaceTexture\(THREE\);/);
 assert.match(source,/new THREE\.MeshStandardMaterial\(\{map:terrainTexture,vertexColors:true,roughness:\.93,side:THREE\.DoubleSide\}\)/);
 assert.match(source,/terrainMaterial\.dispose\(\);terrainTexture\.dispose\(\);/);
 assert.match(source,/const specialIds=\['LOC-TDS-WATERFALL-TEMPLE','LOC-MUD-DOGS-SWAMP','LOC-COUNTRY-CLUB-JACKSON'/);
 assert.match(source,/const oceanMaterial=createBaseWaterMaterial\(THREE\);/);
 assert.match(source,/new THREE\.PlaneGeometry\(800,800,70,70\)/);
 assert.match(source,/if\(!paused\)lastTime=time;regional\.tick\(lastTime,\{paused\}\)/);
 assert.match(source,/oceanMaterial\.uniforms\.uTime\.value=lastTime/);
 assert.doesNotMatch(createTerrainSurfaceTexture.toString(),/Math\.random|fetch\(|Date\.now|uStorm|worldState|canonical/);
});
