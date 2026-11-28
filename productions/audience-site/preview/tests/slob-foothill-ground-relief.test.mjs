import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)}),original=JSON.stringify(bindings);
const id='LOC-SLOB-FOOTHILL-CAMP';
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
const current=a=>a.locations.find(l=>l.id===id);
const ground=a=>current(a)?.group.children.find(o=>o.name==='Rough training ground');

test('only the source Foothill Camp contains candidate physical training relief',()=>{
 const record=source.locations.find(l=>l.id===id);
 assert.equal(record.canon_status,'PROVISIONAL_CANON');
 assert.deepEqual(record.persistent_landmarks,['tailgate yard','rough training ground']);
 const a=build(),s=current(a),o=ground(a);
 assert.ok(o&&s);assert.equal(a.locations.length,20);assert.equal(a.water.length,4);
 assert.equal(s.group.children.filter(x=>x.name==='Rough training ground').length,1);
 assert.deepEqual(s.sourceLandmarks,record.persistent_landmarks);
 assert.equal(s.group.userData.canonStatus,record.canon_status);
 assert.equal(o.userData.sourceLandmark,'rough training ground');
 assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.ok(s.group.children.some(x=>x.name==='Tailgate yard'));
 assert.ok(s.group.children.some(x=>x.name==='Timber brace'));
 for(const other of a.locations.filter(l=>l.id!==id))
  assert.equal(other.group.children.filter(x=>x.name==='Rough training ground').length,0);
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);assert.equal(JSON.stringify(bindings),original);
 a.dispose();
});

test('one static recessed, shaded surface preserves original transform and bounds deterministically',()=>{
 const a=build(),o=ground(a),geo=o.geometry,p=geo.getAttribute('position'),c=geo.getAttribute('color');
 assert.equal(geo.type,'BoxGeometry');
 assert.deepEqual([geo.parameters.width,geo.parameters.height,geo.parameters.depth],[3.7,.1,4]);
 assert.deepEqual([geo.parameters.widthSegments,geo.parameters.heightSegments,geo.parameters.depthSegments],[36,1,40]);
 assert.deepEqual(o.position.toArray(),[3,.25,2.5]);assert.deepEqual(o.scale.toArray(),[1,1,1]);
 assert.equal(o.material.vertexColors,true);assert.equal(o.material.roughness,.99);
 assert.equal(p.count,c.count);assert.ok(p.count>=3300&&p.count<3600);
 let carved=0,edge=0,low=1,high=0;
 for(let i=0;i<p.count;i++){
  const x=p.getX(i),y=p.getY(i),z=p.getZ(i);
  assert.ok([x,y,z].every(Number.isFinite));
  assert.ok(Math.abs(x)<=1.850001&&Math.abs(z)<=2.000001);
  assert.ok(y>=-.050001&&y<=.050001);
  if(y<.049&&y>-.049)carved++;
  if((Math.abs(x)>1.849||Math.abs(z)>1.999)&&Math.abs(y-.05)<.00001)edge++;
  for(const shade of [c.getX(i),c.getY(i),c.getZ(i)]){
   assert.ok(Number.isFinite(shade)&&shade>.12&&shade<.65);
   low=Math.min(low,shade);high=Math.max(high,shade);
  }
 }
 assert.ok(carved>800);assert.ok(edge>100);assert.ok(high-low>.2);
 const b=build(),copy=ground(b);
 assert.deepEqual(p.array,copy.geometry.getAttribute('position').array);
 assert.deepEqual(c.array,copy.geometry.getAttribute('color').array);
 a.dispose();b.dispose();
});

test('El Niño global calm retains ordinary water motion; explicit pause and cleanup remain intact',()=>{
 const a=build(),o=ground(a),snapshot=o.geometry.getAttribute('position').array.slice();
 a.tick(1.3,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===1.3));
 a.tick(4.7,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===4.7));
 a.tick(10,{globalCalm:true,storm:6,paused:true});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===4.7));
 assert.deepEqual(o.geometry.getAttribute('position').array,snapshot);
 let gCount=0,mCount=0;
 o.geometry.addEventListener('dispose',()=>gCount++);
 o.material.addEventListener('dispose',()=>mCount++);
 a.dispose();a.dispose();a.tick(12);
 assert.equal(gCount,1);assert.equal(mCount,1);
 assert.equal(JSON.stringify(bindings),original);
});
