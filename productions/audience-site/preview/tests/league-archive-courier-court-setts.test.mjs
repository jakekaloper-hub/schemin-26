import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)});
const original=JSON.stringify(bindings);
const id='LOC-LEAGUE-ARCHIVE',build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
function locate(a){
 const site=a.locations.find(l=>l.id===id);
 assert.ok(site);
 const court=site.group.children.filter(o=>o.name==='Courier court');
 assert.equal(court.length,1,'the same single courier court mesh');
 return {site,court:court[0]};
}

test('Archive paving only belongs to source-recorded courier court, not a new world or historical claim',()=>{
 const record=source.locations.find(l=>l.id===id);
 assert.equal(record.canon_status,'INTERPRETIVE_CANON');
 assert.deepEqual(record.persistent_landmarks,['record halls','ledger vaults','courier court']);
 const a=build(),{site,court}=locate(a);
 assert.equal(a.locations.length,20);assert.equal(a.water.length,4);
 assert.deepEqual(site.sourceLandmarks,record.persistent_landmarks);
 assert.equal(site.group.userData.canonStatus,record.canon_status);
 assert.equal(court.userData.sourceLandmark,'courier court');
 assert.equal(court.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(court.userData.settCount,51);
 assert.deepEqual(court.position.toArray(),[0,.51,2.1]);
 assert.equal(site.group.children.filter(o=>o.name==='Masonry arch candidate').length,1);
 for(const other of a.locations.filter(l=>l.id!==id))
  assert.equal(other.group.children.filter(o=>o.userData.settCount===51).length,0,other.id);
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);assert.equal(JSON.stringify(bindings),original);
 a.dispose();
});

test('51 staggered physical setts remain in exact original 5.8 × .1 × 4.3 bounds with real inset grooves',()=>{
 const a=build(),court=locate(a).court,b=build(),copy=locate(b).court;
 const geo=court.geometry,p=geo.getAttribute('position'),color=geo.getAttribute('color');
 assert.equal(geo.type,'BufferGeometry');assert.ok(p.count>1000&&p.count<1500);
 assert.equal(p.count,color.count);assert.equal(geo.index.count%3,0);
 assert.equal(court.material.isMeshStandardMaterial,true);
 assert.equal(court.material.vertexColors,true);assert.equal(court.material.roughness,.96);
 assert.equal(court.material.metalness,0);assert.equal(court.castShadow,false);
 assert.deepEqual(Array.from(p.array),Array.from(copy.geometry.getAttribute('position').array));
 assert.deepEqual(Array.from(color.array),Array.from(copy.geometry.getAttribute('color').array));
 assert.deepEqual(Array.from(geo.index.array),Array.from(copy.geometry.index.array));
 let minX=Infinity,maxX=-Infinity,minY=Infinity,maxY=-Infinity,minZ=Infinity,maxZ=-Infinity;
 const firstRowX=new Set(),highs=new Set();
 for(let i=0;i<p.count;i++){
  const x=p.getX(i),y=p.getY(i),z=p.getZ(i);
  assert.ok([x,y,z].every(Number.isFinite));
  minX=Math.min(minX,x);maxX=Math.max(maxX,x);
  minY=Math.min(minY,y);maxY=Math.max(maxY,y);
  minZ=Math.min(minZ,z);maxZ=Math.max(maxZ,z);
  if(y>.027&&Math.abs(z-(-2.15+(.018/2)))<.0001)firstRowX.add(x.toFixed(5));
  if(y>.03)highs.add(y.toFixed(4));
  for(const c of [color.getX(i),color.getY(i),color.getZ(i)])
   assert.ok(Number.isFinite(c)&&c>.25&&c<.65);
 }
 assert.ok(minX>=-2.90001&&maxX<=2.90001);
 assert.ok(minY>=-.05001&&maxY<=.05001);
 assert.ok(minZ>=-2.15001&&maxZ<=2.15001);
 const x=[...firstRowX].map(Number).sort((a,b)=>a-b);
 let grooves=0;
 for(let i=1;i<x.length;i++)if(Math.abs(x[i]-x[i-1]-.018)<.00004)grooves++;
 assert.equal(grooves,7,'seven real mortar-width gaps in the eight unshifted front-row tiles');
 assert.ok(highs.size>=3,'actual shallow stone-height variation, not painted texture alone');
 assert.equal(JSON.stringify(bindings),original);a.dispose();b.dispose();
});

test('static archive details preserve ordinary water in El Niño calm, pause and single cleanup',()=>{
 const a=build(),court=locate(a).court;
 assert.equal(court.material.uniforms,undefined);
 a.tick(2,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===2));
 a.tick(5.3,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===5.3));
 a.tick(12,{paused:true,globalCalm:true,storm:5});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===5.3));
 let geometryDisposals=0,materialDisposals=0;
 court.geometry.addEventListener('dispose',()=>geometryDisposals++);
 court.material.addEventListener('dispose',()=>materialDisposals++);
 a.dispose();a.dispose();a.tick(15);
 assert.equal(geometryDisposals,1);assert.equal(materialDisposals,1);
 assert.equal(JSON.stringify(bindings),original);
});
