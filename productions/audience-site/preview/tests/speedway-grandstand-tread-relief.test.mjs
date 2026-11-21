import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from '../vendor/three.module.js';
import {projectAtlas} from '../../src/observer-world.mjs';
import {spatialBindings} from '../spatial.mjs';
import {buildAtlasSiteAssets} from '../atlas-site-assets.mjs';

const source=JSON.parse(readFileSync(new URL('../../../../world/data/locations.json',import.meta.url),'utf8'));
const bindings=spatialBindings({locations:projectAtlas(source.locations)}),before=JSON.stringify(bindings);
const id='LOC-SOUTHERN-SPEEDWAY';
const build=()=>buildAtlasSiteAssets(THREE,bindings,()=>4);
const site=a=>a.locations.find(x=>x.id===id);
const tiers=a=>site(a)?.group.children.filter(x=>x.name==='Grandstand tier')||[];

test('source-defined Speedway retains all eight original grandstand levels and its racecourse',()=>{
 const record=source.locations.find(x=>x.id===id),a=build(),s=site(a),t=tiers(a);
 assert.equal(record.canon_status,'PROVISIONAL_CANON');
 assert.deepEqual(record.persistent_landmarks,['oval/race course','grandstand']);
 assert.ok(s);assert.equal(a.locations.length,20);assert.equal(a.water.length,4);
 assert.equal(s.group.userData.locationId,id);
 assert.deepEqual(s.sourceLandmarks,record.persistent_landmarks);
 assert.equal(s.group.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
 assert.equal(t.length,8);
 assert.equal(s.group.children.filter(x=>x.name==='Rutted oval race course · candidate').length,1);
 assert.equal(s.group.children.filter(x=>x.name==='Pitched roof candidate').length,2);
 assert.ok(s.group.children.some(x=>x.userData.sourceLandmark==='grandstand'));
 for(const z of [-5.7,5.7])for(let row=0;row<4;row++){
  const center=z+Math.sign(z)*row*.55;
  assert.equal(t.filter(x=>Math.abs(x.position.z-center)<1e-6&&Math.abs(x.position.y-(.45+row*.36))<1e-6).length,1);
 }
 assert.ok(a.locations.filter(x=>x.id!==id).every(x=>!x.group.children.some(o=>o.name==='Grandstand tier')));
 assert.equal(a.worldMutationAllowed,false);assert.equal(a.weatherMutationAllowed,false);
 assert.deepEqual(a.principalCharacters,[]);assert.equal(JSON.stringify(bindings),before);
 a.dispose();
});

test('all eight static tiers have deterministic, physically incised treads within the original boxes',()=>{
 const a=build(),b=build(),t=tiers(a),second=tiers(b);
 assert.equal(t.length,8);assert.equal(second.length,8);
 assert.ok(t.every(x=>x.material===t[0].material));
 assert.equal(t[0].material.vertexColors,true);assert.equal(t[0].material.roughness,.98);
 let worn=0,seams=0,variation=0;
 for(let k=0;k<8;k++){
  const o=t[k],g=o.geometry,p=g.getAttribute('position'),c=g.getAttribute('color'),normal=g.getAttribute('normal');
  assert.equal(g.type,'BoxGeometry');
  assert.deepEqual(o.userData.originalDimensions,[8,.4,.55]);
  assert.equal(o.userData.visualAuthority,'CANDIDATE_NOT_APPROVED');
  assert.equal(g.parameters.widthSegments,32);assert.equal(g.parameters.heightSegments,4);assert.equal(g.parameters.depthSegments,6);
  assert.equal(c.count,p.count);assert.ok(p.count<=900);assert.ok(g.index.count<=4400);
  assert.deepEqual(p.array,second[k].geometry.getAttribute('position').array);
  assert.deepEqual(c.array,second[k].geometry.getAttribute('color').array);
  let low=Infinity,high=-Infinity,localWear=0,untouchedRim=0,localSeams=0;
  for(let i=0;i<p.count;i++){
   const x=p.getX(i),y=p.getY(i),z=p.getZ(i);
   assert.ok([x,y,z].every(Number.isFinite));
   assert.ok(Math.abs(x)<=4.000001&&Math.abs(y)<=.200001&&Math.abs(z)<=.275001,'original tier box envelope');
   for(const value of [c.getX(i),c.getY(i),c.getZ(i)]){
    assert.ok(Number.isFinite(value)&&value>0&&value<1);
    low=Math.min(low,value);high=Math.max(high,value);
   }
   if(normal.getY(i)>.65&&Math.abs(z)<.15){
    if(y<.176)localWear++;
   }
   if(Math.abs(Math.abs(z)-.275)<.000001&&normal.getY(i)>.65){
    assert.ok(Math.abs(y-.2)<.000001,'original top side rim');
    untouchedRim++;
   }
   if(Math.abs(z)<.275-.002&&Math.abs(z)>.25&&y>- .1&&y<.16)localSeams++;
  }
  assert.ok(localWear>=6,'recessed tread surface');
  assert.ok(untouchedRim>=25,'top edge intact');
  assert.ok(high-low>.07,'multiple deterministic mineral shades');
  worn+=localWear;seams+=localSeams;variation+=high-low;
 }
 assert.ok(worn>=48);assert.ok(variation>.56);
 assert.equal(JSON.stringify(bindings),before);a.dispose();b.dispose();
});

test('candidate tiers remain static during El Niño calm; ordinary water, pause and once-only cleanup are intact',()=>{
 const a=build(),t=tiers(a),original=t.map(o=>o.geometry.getAttribute('position').array.slice());
 a.tick(1.3,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===1.3));
 a.tick(4.2,{globalCalm:true,storm:0});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===4.2));
 a.tick(8,{paused:true,globalCalm:true,storm:9});
 assert.ok(a.water.every(w=>w.material.uniforms.uTime.value===4.2));
 for(let i=0;i<t.length;i++)assert.deepEqual(t[i].geometry.getAttribute('position').array,original[i]);
 let geometryDisposals=0,materialDisposals=0;
 t[0].geometry.addEventListener('dispose',()=>geometryDisposals++);
 t[0].material.addEventListener('dispose',()=>materialDisposals++);
 a.dispose();a.dispose();a.tick(10);
 assert.equal(geometryDisposals,1);assert.equal(materialDisposals,1);
 assert.equal(JSON.stringify(bindings),before);
});
