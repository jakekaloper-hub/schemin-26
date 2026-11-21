import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)});
const before=JSON.stringify(bindings),id='LOC-TDS-CHILI-SHARED-MARCH';
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
function get(a){
 const site=a.locations.find(x=>x.id===id);
 assert.ok(site);
 const deck=site.group.children.filter(x=>x.name==='Watercourse crossing');
 assert.equal(deck.length,1,'one physical source watercourse crossing');
 return {site,deck:deck[0]};
}

test('Shared March crossing only retains its original source identity, railings, water and landmarks',()=>{
 const record=source.locations.find(x=>x.id===id);
 assert.equal(record.canon_status,'INTERPRETIVE_CANON');
 assert.deepEqual(record.persistent_landmarks,
  ['mixed caravan settlement','watercourse crossing','stable-and-market quarter']);
 const a=build(),{site,deck}=get(a);
 assert.equal(a.locations.length,20);assert.equal(a.water.length,4);
 assert.deepEqual(site.sourceLandmarks,record.persistent_landmarks);
 assert.equal(site.group.userData.canonStatus,record.canon_status);
 assert.equal(deck.userData.sourceLandmark,'watercourse crossing');
 assert.equal(deck.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(deck.userData.plankCount,13);
 assert.deepEqual(deck.position.toArray(),[0,0,2.8]);
 assert.equal(site.group.children.filter(x=>x.name==='Shared March swaying bank reeds · candidate').length,1);
 assert.equal(site.group.children.filter(x=>x.name==='Moving watercourse crossing candidate').length,1);
 const rails=site.group.children.filter(x=>x.isMesh&&
  Math.abs(Math.abs(x.position.x)-1.1)<1e-9&&Math.abs(x.position.y-1.175)<1e-9&&
  Math.abs(x.position.z-2.8)<1e-9);
 assert.equal(rails.length,2,'the old crossing guardrails survive');
 for(const l of a.locations.filter(x=>x.id!==id))
  assert.equal(l.group.children.filter(x=>x.userData.plankCount===13).length,0,l.id);
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);assert.equal(JSON.stringify(bindings),before);
 a.dispose();
});

test('thirteen separated real planks, support stringers, bounded wear and deterministic vertex colors',()=>{
 const a=build(),{deck}=get(a),b=build(),other=get(b).deck;
 const geo=deck.geometry,pos=geo.getAttribute('position'),color=geo.getAttribute('color');
 assert.equal(geo.type,'BufferGeometry');assert.equal(deck.material.isMeshStandardMaterial,true);
 assert.equal(deck.material.vertexColors,true);assert.equal(deck.material.roughness,.96);
 assert.equal(deck.material.metalness,0);assert.ok(pos.count>13*24&&pos.count<550);
 assert.equal(pos.count,color.count);assert.ok(geo.index.count>600);
 assert.deepEqual(Array.from(pos.array),Array.from(other.geometry.getAttribute('position').array));
 assert.deepEqual(Array.from(color.array),Array.from(other.geometry.getAttribute('color').array));
 assert.deepEqual(Array.from(geo.index.array),Array.from(other.geometry.index.array));
 let minX=Infinity,maxX=-Infinity,minY=Infinity,maxY=-Infinity,minZ=Infinity,maxZ=-Infinity;
 const plankEnds=new Set();let supports=0;
 for(let i=0;i<pos.count;i++){
  const x=pos.getX(i),y=pos.getY(i),z=pos.getZ(i);
  assert.ok([x,y,z].every(Number.isFinite));
  minX=Math.min(minX,x);maxX=Math.max(maxX,x);
  minY=Math.min(minY,y);maxY=Math.max(maxY,y);
  minZ=Math.min(minZ,z);maxZ=Math.max(maxZ,z);
  if(y>.79)plankEnds.add(z.toFixed(5));
  if(y<.7)supports++;
  for(const c of [color.getX(i),color.getY(i),color.getZ(i)])
   assert.ok(c>.10&&c<.70,'bounded natural wood tone');
 }
 assert.ok(minX>=-1.150001&&maxX<=1.150001);
 assert.ok(minY>=.499999&&maxY<=.800001);
 assert.ok(minZ>=-2.150001&&maxZ<=2.150001);
 assert.equal(plankEnds.size,26,'two physically distinct Z ends for each of 13 boards');
 const ends=[...plankEnds].map(Number).sort((a,b)=>a-b);
 let seams=0;for(let i=1;i<ends.length;i++)if(Math.abs(ends[i]-ends[i-1]-.024)<.00003)seams++;
 assert.equal(seams,12,'twelve genuine daylight seams, not painted lines');
 assert.ok(supports>=24,'continuous physical deck stringers underneath');
 assert.equal(JSON.stringify(bindings),before);a.dispose();b.dispose();
});

test('candidate bridge adds no weather clock: normal water/reed motion in El Niño calm, pause, one-time disposal',()=>{
 const a=build(),{deck}=get(a);
 const water=a.water.find(x=>x.kind==='watercourse crossing');
 const reeds=a.locations.find(x=>x.id===id).group.children.find(x=>x.name==='Shared March swaying bank reeds · candidate');
 assert.ok(water);assert.ok(reeds);
 a.tick(1.25,{globalCalm:true,storm:0});
 assert.equal(water.material.uniforms.uTime.value,1.25);
 assert.equal(reeds.material.uniforms.uTime.value,1.25);
 a.tick(3.5,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.5));
 assert.equal(reeds.material.uniforms.uTime.value,3.5);
 a.tick(9,{paused:true,globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===3.5));
 assert.equal(reeds.material.uniforms.uTime.value,3.5);
 let geometryDisposed=0,materialDisposed=0;
 deck.geometry.addEventListener('dispose',()=>geometryDisposed++);
 deck.material.addEventListener('dispose',()=>materialDisposed++);
 assert.equal(JSON.stringify(bindings),before);
 a.dispose();a.dispose();a.tick(11);
 assert.equal(geometryDisposed,1);assert.equal(materialDisposed,1);
 assert.equal(water.material.uniforms.uTime.value,3.5);
});
