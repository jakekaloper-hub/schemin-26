import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {wetlandGroundContactWeight,applyWetlandGroundContact} from '../three-world.mjs';

const source=readFileSync(new URL('../three-world.mjs',import.meta.url),'utf8');
const anchor=[12,0,-8];
function geometry(){
 const g=new THREE.BufferGeometry();
 const rows=[
  [12,3,-8], [19,3,-8], [31,3,-8], [60,3,50],
  [12,10,-8], [13,1,-8] // architecture/vegetation, not terrain
 ];
 const packed=new Float32Array(rows.flatMap(([x,y,z])=>[x,y,z, 0,1,0, .8,.65,.45]));
 const buffer=new THREE.InterleavedBuffer(packed,9);
 g.setAttribute('position',new THREE.InterleavedBufferAttribute(buffer,3,0));
 g.setAttribute('normal',new THREE.InterleavedBufferAttribute(buffer,3,3));
 g.setAttribute('color',new THREE.InterleavedBufferAttribute(buffer,3,6));
 return g;
}
test('source-anchored damp ground tint decays smoothly and never defines a new shoreline',()=>{
 assert.equal(wetlandGroundContactWeight(12,-8,anchor),1);
 assert.equal(wetlandGroundContactWeight(12+10.5*1.65,-8,anchor),0);
 assert.equal(wetlandGroundContactWeight(200,200,anchor),0);
 const m=wetlandGroundContactWeight(23,-8,anchor);
 assert.ok(m>0&&m<1);
 assert.throws(()=>wetlandGroundContactWeight(0,0,[Infinity,0,0]),/INVALID_WETLAND_CONTACT_ANCHOR/);
 assert.throws(()=>wetlandGroundContactWeight(0,0,[0,0]),/INVALID_WETLAND_CONTACT_ANCHOR/);
});
test('only pre-existing terrain color changes, without geometry, normals, later site assets or randomness',()=>{
 const a=geometry(),b=geometry();
 const beforePos=Array.from(a.getAttribute('position').data.array);
 const ca=a.getAttribute('color');
 const originals=Array.from({length:ca.count},(_,i)=>[ca.getX(i),ca.getY(i),ca.getZ(i)]);
 assert.equal(applyWetlandGroundContact(a,anchor,4),2);
 assert.equal(applyWetlandGroundContact(b,anchor,4),2);
 assert.deepEqual(Array.from(a.getAttribute('position').data.array),Array.from(b.getAttribute('position').data.array));
 for(let i=0;i<ca.count;i++){
  for(let j=0;j<3;j++){
   const current=[ca.getX(i),ca.getY(i),ca.getZ(i)][j];
   if(i===0||i===1)assert.ok(current<originals[i][j]);
   else assert.equal(current,originals[i][j]);
  }
 }
 // Interleaved mesh contains later object vertices: only the terrain prefix may change.
 assert.deepEqual(Array.from(a.getAttribute('position').data.array).filter((_,i)=>i%9<6),beforePos.filter((_,i)=>i%9<6));
 assert.ok(ca.data.version>0);
 assert.throws(()=>applyWetlandGroundContact(a,anchor,0),/INVALID_WETLAND_CONTACT_GEOMETRY/);
 assert.throws(()=>applyWetlandGroundContact(a,anchor,7),/INVALID_WETLAND_CONTACT_GEOMETRY/);
 a.dispose();b.dispose();
});
test('the only live call is keyed to the exact source ID and first terrain-grid triangles',()=>{
 assert.match(source,/const swampBinding=bindings\.find\(b=>b\.id==='LOC-MUD-DOGS-SWAMP'\)/);
 assert.match(source,/if\(swampBinding\)applyWetlandGroundContact\(geometry,swampBinding\.anchor,terrainGrid\*terrainGrid\*6\)/);
 assert.match(source,/const terrainGrid=160/);
 assert.match(source,/const swampSite=regional\.locations\.find\(l=>l\.id==='LOC-MUD-DOGS-SWAMP'\)/);
 assert.doesNotMatch(wetlandGroundContactWeight.toString()+applyWetlandGroundContact.toString(),/Math\.random|Date\(|fetch\(|uStorm|weather|worldState/);
});
